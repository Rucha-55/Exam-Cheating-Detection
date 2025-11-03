# Render Deployment Guide

This guide will help you deploy the **Exam Cheating Detection** project on Render.

## Prerequisites

1. **GitHub Account** - Repository must be pushed to GitHub
2. **Render Account** - Sign up at [https://render.com](https://render.com)
3. **GitHub Personal Access Token** (optional, for private repos)

---

## Step 1: Prepare Your Repository

Ensure all deployment files are in your GitHub repository:

- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Deployment configuration
- ✅ `render.yaml` - Render service definition
- ✅ `build.sh` - Build script
- ✅ `.env.example` - Environment variable template
- ✅ `.gitignore` - Git ignore rules

**Push to GitHub:**
```bash
cd c:\Users\rucha\OneDrive\Desktop\Rucha
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

---

## Step 2: Connect GitHub to Render

1. Go to [https://render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Select **"Deploy an existing Git repository"**
4. Paste your GitHub repository URL:
   ```
   https://github.com/Rucha-55/Exam-Cheating-Detection.git
   ```
5. Click **"Connect"** and authorize GitHub access

---

## Step 3: Configure the Web Service

1. **Service Name:** `exam-cheating-detection` (or your preferred name)
2. **Environment:** `Python 3`
3. **Build Command:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Start Command:**
   ```bash
   gunicorn app:app
   ```
5. **Plan:** Select `Free` (or upgrade for better performance)

---

## Step 4: Set Environment Variables

1. In the Render dashboard, scroll to **"Environment"**
2. Add the following variables:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `PYTHON_VERSION` | `3.10.0` |

3. For any additional variables needed by your app, add them from your `.env.example`

---

## Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will start building and deploying your application
3. Wait for the deployment to complete (usually 5-10 minutes)
4. Once successful, you'll see a URL like: `https://exam-cheating-detection-xxxx.onrender.com`

---

## Step 6: Access Your Application

Your app is now live! Visit:
```
https://exam-cheating-detection-xxxx.onrender.com
```

Health check endpoint:
```
https://exam-cheating-detection-xxxx.onrender.com/health
```

---

## Troubleshooting

### Deployment Fails
- Check **Logs** tab in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify `requirements.txt` format (one package per line)

### App Not Starting
```bash
# Check startup logs in Render dashboard
# Look for errors in "gunicorn app:app" command
```

### Model File Not Found
- Ensure `cheating_model_best.pt` is tracked by Git (or upload separately)
- Or configure to download model from cloud storage on startup

### Port Issues
- Render automatically assigns a PORT environment variable
- The app.py reads `PORT` from environment, so it should work automatically

---

## Enable Auto-Deployment from GitHub

1. In Render dashboard, go to service settings
2. Enable **"Auto-Deploy"** for the `main` branch
3. Now every push to GitHub will trigger automatic redeployment

---

## Performance Tips

### For Free Tier:
- App will spin down after 15 minutes of inactivity (restart takes ~30 seconds)
- Recommended for testing/demo purposes

### Upgrade to Paid:
- Click **"Settings"** → **"Instance Type"** → Choose a paid plan
- Ensures always-on performance

---

## Environment Variables

Create a `.env` file locally (not committed to Git):

```
FLASK_ENV=production
PYTHON_VERSION=3.10.0
```

Example `.env.example` (safe to commit):
```
FLASK_ENV=development
PYTHON_VERSION=3.10.0
```

---

## Deployment Architecture

```
GitHub Repository (Exam-Cheating-Detection)
        ↓
    Render CI/CD
        ↓
   Build Phase (pip install -r requirements.txt)
        ↓
   Deploy Phase (gunicorn app:app)
        ↓
   Live Web Service
        ↓
   https://exam-cheating-detection-xxxx.onrender.com
```

---

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Flask Deployment Best Practices](https://flask.palletsprojects.com/deployment/)
- [Gunicorn Configuration](https://gunicorn.org/)

---

## Support

If you encounter issues:
1. Check Render **Logs** for error messages
2. Verify all files are committed to GitHub
3. Contact Render support or check their documentation

---

**Happy Deploying! 🚀**

Your Exam Cheating Detection system is now ready for production use on Render!
