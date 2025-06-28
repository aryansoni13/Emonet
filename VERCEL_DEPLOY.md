# 🚀 Vercel Deployment Guide for Emotion Avatar

## 📋 Prerequisites

- GitHub repository with your emotion avatar code
- Vercel account (free)
- All files committed to GitHub

## 🎯 Step-by-Step Deployment

### Step 1: Prepare Your Repository

Make sure all files are committed to GitHub:

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 2: Go to Vercel

1. **Visit [Vercel.com](https://vercel.com)**
2. **Sign up/Login** with your GitHub account
3. **Click "New Project"**

### Step 3: Import Your Repository

1. **Select "Import Git Repository"**
2. **Find and select** your emotion avatar repository
3. **Click "Import"**

### Step 4: Configure Project

Vercel will auto-detect it's a Python project. Configure:

- **Project Name**: `emotion-avatar` (or your preferred name)
- **Framework Preset**: `Other` (Vercel will auto-detect Python)
- **Root Directory**: `./` (leave as default)
- **Build Command**: Leave empty (Vercel handles this)
- **Output Directory**: Leave empty
- **Install Command**: `pip install -r requirements.txt`

### Step 5: Environment Variables (Optional)

Add these if needed:
- `PYTHONPATH`: `.`
- `FLASK_ENV`: `production`

### Step 6: Deploy

1. **Click "Deploy"**
2. **Wait 2-3 minutes** for build and deployment
3. **Your site will be live!**

## ✅ What Vercel Does Automatically

- ✅ Detects Python Flask app
- ✅ Installs dependencies from `requirements.txt`
- ✅ Uses `vercel.json` for configuration
- ✅ Creates serverless functions
- ✅ Provides HTTPS and CDN
- ✅ Auto-deploys on git push

## 🔗 Your Live URL

After deployment, you'll get:
- **Production URL**: `https://your-project-name.vercel.app`
- **Preview URLs**: For each branch/PR

## 📱 Test Your Deployment

1. **Visit your Vercel URL**
2. **Click "Start Camera"**
3. **Allow camera access**
4. **Test emotion detection**

## 🔄 Automatic Deployments

Every time you push to GitHub:
- Vercel automatically rebuilds and deploys
- Preview deployments for pull requests
- Instant rollbacks if needed

## 🛠️ Troubleshooting

### Common Issues:

1. **Build Fails**:
   - Check `requirements.txt` is correct
   - Ensure all files are committed
   - Check Vercel build logs

2. **OpenCV Issues**:
   - Vercel supports OpenCV via `requirements.txt`
   - The `vercel.json` handles Python configuration

3. **Port Issues**:
   - Vercel handles port automatically
   - Updated `app.py` uses environment port

### Debug Commands:

```bash
# Check Vercel logs
vercel logs

# Redeploy
vercel --prod

# Check status
vercel ls
```

## 🎉 Success!

Your emotion avatar is now:
- 🌐 Live on the internet
- 📱 Mobile responsive
- ⚡ Fast with CDN
- 🔒 Secure with HTTPS
- 🔄 Auto-updating

## 📊 Vercel Dashboard

Access your Vercel dashboard to:
- View analytics
- Check deployment status
- Manage domains
- Monitor performance

## 🔗 Share Your App

Share your Vercel URL:
- **Main URL**: `https://your-project-name.vercel.app`
- **Works on all devices**
- **No installation required**

---

**Your Emotion Avatar is now live on Vercel! 🎭✨** 