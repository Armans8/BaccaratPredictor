# Baccarat Outcome Predictor

A web application that predicts baccarat outcomes based on pattern recognition. The app analyzes your input history to predict whether the next outcome will be Player (P), Banker (B), or Tie (T).

## Features

- Records outcome history with P, B, T buttons
- Analyzes patterns to predict next outcome
- Visual display of prediction confidence
- Delete Previous and Reset Session functionality
- Mobile-responsive design

## Deployment Guide for Render

Follow these steps to deploy the Baccarat Predictor on Render's free tier:

### 1. Create a Render Account

- Go to [Render.com](https://render.com/) and create a free account
- Verify your email address

### 2. Download the Project and Create a GitHub Repository

- Download this project as a ZIP file from Replit
- Extract the ZIP file to your computer
- Create a new GitHub repository (if you don't have a GitHub account, sign up at [GitHub.com](https://github.com/))
- Upload all files to your GitHub repository

### 3. Set Up Your Render Web Service

- Log in to your Render dashboard
- Click the "New +" button and select "Web Service"
- Connect your GitHub account if prompted
- Select the repository containing your Baccarat Predictor
- Configure the web service with these settings:
  - **Name**: baccarat-predictor (or any name you prefer)
  - **Environment**: Python 3
  - **Region**: Choose the one closest to you
  - **Branch**: main (or your default branch)
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `gunicorn main:app`
  - Leave all other settings as default

### 4. Set Environment Variables

- Once your service is created, go to the "Environment" tab
- Add the following environment variable:
  - Key: `SESSION_SECRET`
  - Value: Create a random string (you can use a password generator)
- Click "Save Changes"

### 5. Deploy Your Application

- Render will automatically build and deploy your application
- Wait for the deployment to complete (this may take a few minutes)
- Once deployed, you'll see a URL like `https://your-app-name.onrender.com`
- Click on this URL to access your Baccarat Predictor

### Troubleshooting

If your deployment fails, check the logs in the Render dashboard for error messages. Common issues include:

- Missing requirements
- Incorrect start command
- Syntax errors in the code

## Using the Application

1. Click P, B, or T buttons to record outcomes as they happen in your baccarat game
2. The prediction bar will update with the predicted next outcome
3. Use "Delete Previous" to remove the last entry if you made a mistake
4. Use "Reset Session" to clear all history and start fresh

## Notes

- The free tier on Render will spin down after periods of inactivity
- The first request after inactivity may take 30-60 seconds to load
- The app will run continuously once it's active again

## Local Development

If you want to run the application locally:

1. Install Python 3.7 or higher
2. Install the required packages: `pip install flask gunicorn`
3. Run the application: `python main.py`
4. Open your browser to `http://localhost:5000`