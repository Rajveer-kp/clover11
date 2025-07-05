# Deployment Guide

## Railway Deployment (Recommended)

### Prerequisites
1. GitHub account with your code pushed
2. YouTube API credentials from Google Cloud Console

### Steps:

1. **Go to Railway**
   - Visit [railway.app](https://railway.app)
   - Sign up/login with GitHub

2. **Deploy from GitHub**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `clover11` repository
   - Railway will auto-detect Flask app

3. **Configure Environment Variables**
   In Railway dashboard, add these variables:
   ```
   SECRET_KEY=your-secret-key-here
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   FLASK_ENV=production
   ```

4. **Database Setup**
   - Railway will automatically provide PostgreSQL
   - DATABASE_URL will be set automatically

5. **Deploy**
   - Railway will automatically deploy using your `railway.json`
   - Your app will be available at: `https://your-app-name.railway.app`

### Post-Deployment:

1. **Update YouTube API Settings**
   - Go to Google Cloud Console
   - Add your Railway domain to authorized redirect URIs:
     ```
     https://your-app-name.railway.app/youtube/callback
     ```

2. **Test Your App**
   - Visit your Railway URL
   - Test user registration/login
   - Test YouTube OAuth connection

---

## Alternative: Render Deployment

1. **Go to Render**
   - Visit [render.com](https://render.com)
   - Connect GitHub

2. **Create Web Service**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`

3. **Add Environment Variables** (same as Railway)

---

## Alternative: Heroku Deployment

1. **Install Heroku CLI**
2. **Create Procfile**:
   ```
   web: gunicorn wsgi:app
   ```
3. **Deploy**:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

---

## Environment Variables Needed:

- `SECRET_KEY`: Flask secret key
- `GOOGLE_CLIENT_ID`: From Google Cloud Console
- `GOOGLE_CLIENT_SECRET`: From Google Cloud Console  
- `FLASK_ENV`: Set to "production"
- `DATABASE_URL`: Automatically provided by Railway/Render/Heroku

## YouTube API Setup:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Enable YouTube Data API v3
3. Create OAuth 2.0 credentials
4. Add your deployment domain to authorized redirect URIs
