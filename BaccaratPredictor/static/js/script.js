// Function to update the prediction display
function updatePredictionDisplay(prediction, opposite, confidence) {
    // Get the prediction and opposite bars
    const predictionBar = document.getElementById('prediction-bar');
    const oppositeBar = document.getElementById('opposite-bar');
    
    // Completely reset the classes to ensure no leftover styles
    predictionBar.className = 'prediction-bar';
    oppositeBar.className = 'opposite-bar';
    
    // Add proper background color class
    if (prediction === 'P') {
        predictionBar.classList.add('player-bg');
    } else if (prediction === 'B') {
        predictionBar.classList.add('banker-bg');
    } else {
        predictionBar.classList.add('tie-bg');
    }
    
    if (opposite === 'P') {
        oppositeBar.classList.add('player-bg');
    } else if (opposite === 'B') {
        oppositeBar.classList.add('banker-bg');
    } else {
        oppositeBar.classList.add('tie-bg');
    }
    
    // Adjust widths based on confidence
    if (prediction === 'T') {
        // For tie predictions, make the bar shorter
        predictionBar.style.width = '25%';
        oppositeBar.style.width = '75%';
    } else {
        // Normal confidence-based width
        const predictionWidth = Math.min(Math.max(confidence * 100, 40), 80);
        predictionBar.style.width = `${predictionWidth}%`;
        oppositeBar.style.width = `${100 - predictionWidth}%`;
    }
}

// Function to update the history display
function updateHistoryDisplay(history) {
    const historyDisplay = document.getElementById('history-display');
    historyDisplay.innerHTML = '';
    
    history.forEach(outcome => {
        const outcomeBox = document.createElement('div');
        outcomeBox.className = 'outcome-box';
        
        if (outcome === 'P') {
            outcomeBox.classList.add('player-bg');
        } else if (outcome === 'B') {
            outcomeBox.classList.add('banker-bg');
        } else {
            outcomeBox.classList.add('tie-bg');
        }
        
        outcomeBox.textContent = outcome;
        historyDisplay.appendChild(outcomeBox);
    });
}

// Function to add an outcome
function addOutcome(outcome) {
    $.ajax({
        url: '/add_outcome',
        method: 'POST',
        data: { outcome: outcome },
        success: function(response) {
            if (response.success) {
                updateHistoryDisplay(response.history);
                updatePredictionDisplay(response.prediction, response.opposite, response.confidence);
            } else {
                console.error("Error:", response.error);
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX error:", error);
        }
    });
}

// Function to delete the previous outcome
function deletePrevious() {
    $.ajax({
        url: '/delete_previous',
        method: 'POST',
        success: function(response) {
            if (response.success) {
                updateHistoryDisplay(response.history);
                updatePredictionDisplay(response.prediction, response.opposite, response.confidence);
            } else {
                console.error("Error:", response.error);
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX error:", error);
        }
    });
}

// Function to reset the session
function resetSession() {
    $.ajax({
        url: '/reset_session',
        method: 'POST',
        success: function(response) {
            if (response.success) {
                updateHistoryDisplay(response.history);
                updatePredictionDisplay(response.prediction, response.opposite, response.confidence);
            } else {
                console.error("Error:", response.error);
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX error:", error);
        }
    });
}

// Initialize the prediction display on page load
document.addEventListener('DOMContentLoaded', function() {
    // Get initial values from the server-rendered template
    const predictionElement = document.getElementById('prediction-bar');
    const oppositeElement = document.getElementById('opposite-bar');
    
    if (predictionElement && oppositeElement) {
        const prediction = predictionElement.classList.contains('player-bg') ? 'P' : 
                          predictionElement.classList.contains('banker-bg') ? 'B' : 'T';
        
        const opposite = oppositeElement.classList.contains('player-bg') ? 'P' : 
                         oppositeElement.classList.contains('banker-bg') ? 'B' : 'T';
        
        // Default confidence is 0.6
        updatePredictionDisplay(prediction, opposite, 0.6);
    }
});
