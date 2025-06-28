#!/bin/bash

echo "🚀 Emotion Avatar Deployment Script"
echo "=================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
fi

# Add all files
echo "📦 Adding files to Git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Deploy Emotion Avatar Web App"

# Set main branch
echo "🌿 Setting main branch..."
git branch -M main

# Check if remote exists
if ! git remote get-url origin &> /dev/null; then
    echo "🔗 Adding GitHub remote..."
    echo "Please enter your GitHub repository URL:"
    echo "Example: https://github.com/aryansoni13/Real_Time_Face_Emotion_Avatar.git"
    read -p "Repository URL: " repo_url
    git remote add origin "$repo_url"
fi

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "🌐 Next Steps:"
echo "1. Go to Railway.app or Render.com"
echo "2. Connect your GitHub repository"
echo "3. Deploy your app!"
echo ""
echo "📖 See GITHUB_DEPLOYMENT.md for detailed instructions"
echo ""
echo "🎉 Your emotion avatar is ready to go live!" 