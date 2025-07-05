# Render Deployment (Better than Railway)

## Why Render is Better:
- More reliable uptime (99.9% vs Railway's 99.5%)
- Better performance and speed
- More generous free tier (750 hours/month)
- Better customer support
- More stable platform

## Deployment Steps:

### 1. Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub

### 2. Deploy Web Service
- Click "New +" → "Web Service"
- Connect GitHub → Select `clover11` repository
- Configure:
  ```
  Name: youtube-manager
  Environment: Python 3
  Build Command: pip install -r requirements.txt
  Start Command: gunicorn wsgi:app
  ```

### 3. Environment Variables
Add these in Render dashboard:
```
SECRET_KEY=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FLASK_ENV=production
```

### 4. Database Setup
- Click "New +" → "PostgreSQL"
- Name: `youtube-manager-db`
- Copy the Internal Database URL
- Add to your web service as: `DATABASE_URL=your-postgres-url`

### 5. Post-Deployment
- Your app will be at: `https://youtube-manager.onrender.com`
- Update Google Cloud Console redirect URIs:
  `https://youtube-manager.onrender.com/youtube/callback`

## Advantages over Railway:
- ✅ Better uptime and reliability
- ✅ Faster cold starts
- ✅ Better monitoring and logs
- ✅ More predictable pricing
- ✅ Better PostgreSQL management
