#!/bin/bash

echo "🚀 Deploying Emotion Avatar to Heroku..."
echo "=========================================="

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Installing..."
    echo "Please install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please login to Heroku..."
    heroku login
fi

# Create Heroku app
echo "📦 Creating Heroku app..."
APP_NAME="emotion-avatar-$(date +%s)"
heroku create $APP_NAME

# Add buildpacks
echo "🔧 Adding buildpacks..."
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-apt

# Deploy
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open the app
echo "🌐 Opening your app..."
heroku open

echo "✅ Deployment complete!"
echo "🔗 Your app URL: https://$APP_NAME.herokuapp.com"
echo "📊 View logs: heroku logs --tail -a $APP_NAME" 