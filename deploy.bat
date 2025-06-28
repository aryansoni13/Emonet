@echo off
echo 🚀 Emotion Avatar Deployment Script
echo ==================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed. Please install Git first.
    pause
    exit /b 1
)

REM Check if we're in a git repository
if not exist ".git" (
    echo 📁 Initializing Git repository...
    git init
)

REM Add all files
echo 📦 Adding files to Git...
git add .

REM Commit changes
echo 💾 Committing changes...
git commit -m "Deploy Emotion Avatar Web App"

REM Set main branch
echo 🌿 Setting main branch...
git branch -M main

REM Check if remote exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo 🔗 Adding GitHub remote...
    echo Please enter your GitHub repository URL:
    echo Example: https://github.com/aryansoni13/Real_Time_Face_Emotion_Avatar.git
    set /p repo_url="Repository URL: "
    git remote add origin "%repo_url%"
)

REM Push to GitHub
echo ⬆️  Pushing to GitHub...
git push -u origin main

echo.
echo ✅ Successfully pushed to GitHub!
echo.
echo 🌐 Next Steps:
echo 1. Go to Railway.app or Render.com
echo 2. Connect your GitHub repository
echo 3. Deploy your app!
echo.
echo 📖 See GITHUB_DEPLOYMENT.md for detailed instructions
echo.
echo 🎉 Your emotion avatar is ready to go live!
pause 