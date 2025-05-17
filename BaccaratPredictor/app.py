import os
import logging
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "baccarat-predictor-secret-key")

# Prediction logic functions
def analyze_patterns(history):
    """
    Analyzes patterns in history to predict next outcome
    Returns: (prediction, confidence)
    """
    if not history:
        return "B", 0.55  # Slight bias toward Banker as a starting point (statistical edge)
    
    # Count occurrences
    counts = {"P": 0, "B": 0, "T": 0}
    for outcome in history:
        counts[outcome] += 1
    
    # Check for streaks (3 or more of the same outcome)
    streak_length = 1
    current = history[-1]
    for i in range(len(history)-2, -1, -1):
        if history[i] == current:
            streak_length += 1
        else:
            break
    
    # Check for alternating pattern (chops)
    alternating = False
    if len(history) >= 4:
        if (history[-1] != history[-2] and 
            history[-2] != history[-3] and 
            history[-3] != history[-4]):
            alternating = True
    
    # Detect ties
    recent_ties = sum(1 for x in history[-5:] if x == "T") if len(history) >= 5 else 0
    
    # Calculate prediction
    if current == "T":
        # After a tie, predict the more frequent of P or B
        prediction = "B" if counts["B"] >= counts["P"] else "P"
        confidence = 0.6
    elif streak_length >= 3:
        # Long streaks tend to break
        prediction = "P" if current == "B" else "B"
        confidence = 0.55 + min(0.20, (streak_length - 3) * 0.05)
    elif alternating:
        # Continue alternating pattern
        prediction = "P" if current == "B" else "B"
        confidence = 0.65
    elif recent_ties >= 2:
        # After multiple recent ties, expect more P or B
        prediction = "P" if counts["P"] < counts["B"] else "B"
        confidence = 0.60
    else:
        # Default to the more common outcome with a slight edge
        if counts["P"] > counts["B"]:
            prediction = "P"
            confidence = 0.52 + min(0.18, (counts["P"] - counts["B"]) / len(history) * 0.5)
        else:
            prediction = "B"
            confidence = 0.55 + min(0.15, (counts["B"] - counts["P"]) / len(history) * 0.5)
    
    # Limit confidence to reasonable range
    confidence = min(0.85, confidence)
    
    # Only predict a tie in very specific circumstances (make tie prediction much rarer)
    should_predict_tie = False
    tie_probability = 0.0  # Initialize tie_probability
    
    # Only consider a tie if we have enough history to make a meaningful pattern
    if len(history) >= 6:
        # Look for specific patterns that might indicate a tie
        
        # Pattern 1: Recent ties - only if we've seen ties recently in a specific pattern
        if recent_ties >= 1:
            # Check for cyclical tie pattern (e.g., every 5-6 outcomes)
            tie_positions = [i for i, outcome in enumerate(history) if outcome == "T"]
            if len(tie_positions) >= 2:
                # Calculate distances between consecutive ties
                distances = [tie_positions[i] - tie_positions[i-1] for i in range(1, len(tie_positions))]
                # If distances are somewhat consistent, predict another tie
                if len(set(distances)) == 1 and len(history) - tie_positions[-1] == distances[0]:
                    should_predict_tie = True
                    tie_probability = 0.15  # Higher confidence for pattern-based tie prediction
        
        # Pattern 2: After a long sequence of alternating P and B (e.g., P-B-P-B-P-B)
        if len(history) >= 8 and not should_predict_tie:
            alternating_count = 0
            for i in range(len(history)-1):
                if history[i] != history[i+1] and history[i] in ["P", "B"] and history[i+1] in ["P", "B"]:
                    alternating_count += 1
                else:
                    alternating_count = 0
                    
            if alternating_count >= 6:  # At least 6 alternating P/B outcomes
                should_predict_tie = True
                tie_probability = 0.12
        
        # Pattern 3: After similar outcomes on both sides (balance)
        if not should_predict_tie and len(history) >= 10:
            if abs(counts["P"] - counts["B"]) <= 1 and counts["T"] == 0:
                # If we have a near-perfect balance and no ties yet
                should_predict_tie = True
                tie_probability = 0.10
    
    if should_predict_tie:
        return "T", tie_probability
    
    return prediction, confidence

def get_opposite(prediction):
    """Get the opposite outcome of the prediction"""
    if prediction == "P":
        return "B"
    elif prediction == "B":
        return "P"
    else:  # For Tie, return the most likely of P or B based on history
        if 'history' in session and session['history']:
            # Count P and B in history
            p_count = session['history'].count("P")
            b_count = session['history'].count("B")
            return "P" if b_count >= p_count else "B"
        return "B"  # Default to Banker for tie's opposite if no history

@app.route('/')
def index():
    # Initialize session history if it doesn't exist
    if 'history' not in session:
        session['history'] = []
    
    history = session['history']
    prediction, confidence = analyze_patterns(history)
    opposite = get_opposite(prediction)
    
    return render_template('index.html', 
                          history=history,
                          prediction=prediction,
                          opposite=opposite,
                          confidence=confidence)

@app.route('/add_outcome', methods=['POST'])
def add_outcome():
    outcome = request.form['outcome']
    
    # Validate the outcome
    if outcome not in ['P', 'B', 'T']:
        return jsonify({'success': False, 'error': 'Invalid outcome'})
    
    # Initialize history if it doesn't exist
    if 'history' not in session:
        session['history'] = []
    
    # Add the outcome to history
    history = session['history']
    history.append(outcome)
    session['history'] = history
    
    # Get new prediction
    prediction, confidence = analyze_patterns(history)
    opposite = get_opposite(prediction)
    
    return jsonify({
        'success': True,
        'history': history,
        'prediction': prediction,
        'opposite': opposite,
        'confidence': confidence
    })

@app.route('/delete_previous', methods=['POST'])
def delete_previous():
    if 'history' in session and session['history']:
        history = session['history']
        history.pop()
        session['history'] = history
        
        # Get new prediction
        prediction, confidence = analyze_patterns(history)
        opposite = get_opposite(prediction)
        
        return jsonify({
            'success': True,
            'history': history,
            'prediction': prediction,
            'opposite': opposite,
            'confidence': confidence
        })
    else:
        return jsonify({'success': False, 'error': 'No history to delete'})

@app.route('/reset_session', methods=['POST'])
def reset_session():
    session['history'] = []
    
    # Default prediction for empty history
    prediction, confidence = analyze_patterns([])
    opposite = get_opposite(prediction)
    
    return jsonify({
        'success': True,
        'history': [],
        'prediction': prediction,
        'opposite': opposite,
        'confidence': confidence
    })
