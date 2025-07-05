# Vercel Deployment Guide

## 🚀 Deploy to Vercel (Recommended)

**Why Vercel is excellent:**
- ✅ Lightning-fast global CDN
- ✅ Automatic HTTPS certificates
- ✅ Zero-config deployments
- ✅ Excellent for production Flask apps
- ✅ Great developer experience
- ✅ Free tier with generous limits

## Prerequisites

1. **GitHub Account** - Your code is already pushed
2. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
3. **YouTube API Credentials** - From Google Cloud Console

## Step-by-Step Deployment

### 1. Sign Up for Vercel
- Go to [vercel.com](https://vercel.com)
- Click "Sign Up"
- Choose "Continue with GitHub"

### 2. Import Your Project
- Click "New Project"
- Select your `clover11` repository
- Vercel will auto-detect it as a Python app

### 3. Configure Environment Variables
In the Vercel dashboard, add these environment variables:

```bash
# Flask Configuration
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production

# Database Configuration
DATABASE_URL=postgresql://username:password@hostname:port/database

# Google OAuth Configuration (YouTube API)
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
GOOGLE_OAUTH_PROJECT_ID=your-google-project-id
GOOGLE_OAUTH_REDIRECT_URIS=https://your-app-name.vercel.app/youtube/oauth2callback
```

**Important Notes:**
- Replace `your-app-name` with your actual Vercel app name
- For `DATABASE_URL`: Use a free PostgreSQL from [Neon](https://neon.tech) or [Supabase](https://supabase.com)
- For Google OAuth variables: Get these from your Google Cloud Console

### 4. Deploy
- Click "Deploy"
- Vercel will automatically build and deploy your app
- Your app will be available at: `https://your-app-name.vercel.app`

### 5. Post-Deployment Setup

#### Update YouTube API Settings
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to APIs & Services → Credentials
3. Edit your OAuth 2.0 Client ID
4. Add your Vercel domain to authorized redirect URIs:
   ```
   https://your-app-name.vercel.app/youtube/oauth2callback
   ```

#### Test Your Application
1. Visit your Vercel URL
2. Test user registration/login
3. Test YouTube OAuth connection
4. Upload a test video

## Database Options for Vercel

### Option 1: Neon (Recommended - Free)
1. Go to [neon.tech](https://neon.tech)
2. Sign up and create a free database
3. Copy the connection string
4. Add as `DATABASE_URL` in Vercel

### Option 2: Supabase
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Get PostgreSQL connection string
4. Add as `DATABASE_URL` in Vercel

### Option 3: Vercel Postgres (Paid)
1. In Vercel dashboard, go to Storage
2. Create Postgres database
3. Connection string will be auto-added

## File Structure (Already Configured)

```
clover/
├── vercel.json         ✅ Configured
├── runtime.txt         ✅ Python 3.11
├── requirements.txt    ✅ Dependencies
├── wsgi.py            ✅ Entry point
├── app/               ✅ Flask application
└── ...
```

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key for sessions | ✅ Yes |
| `GOOGLE_OAUTH_CLIENT_ID` | YouTube API client ID | ✅ Yes |
| `GOOGLE_OAUTH_CLIENT_SECRET` | YouTube API client secret | ✅ Yes |
| `GOOGLE_OAUTH_PROJECT_ID` | Google Cloud project ID | ✅ Yes |
| `GOOGLE_OAUTH_REDIRECT_URIS` | Comma-separated redirect URIs for OAuth | ✅ Yes |
| `DATABASE_URL` | PostgreSQL connection string | ✅ Yes |
| `FLASK_ENV` | Set to "production" | ✅ Yes |

## Troubleshooting

### Common Issues:

1. **Build Fails**
   - Check Python version in `runtime.txt`
   - Verify all dependencies in `requirements.txt`

2. **Database Connection Issues**
   - Ensure `DATABASE_URL` is correctly formatted
   - Check database is accessible from external connections

3. **YouTube OAuth Not Working**
   - Verify redirect URIs in Google Cloud Console
   - Check `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`

### Vercel Logs
- Go to Vercel dashboard
- Click on your deployment
- View "Functions" tab for logs

## Scaling & Performance

- **CDN**: Vercel automatically serves static files via CDN
- **Edge Functions**: Your Flask app runs on Vercel's edge network
- **Caching**: Configure caching headers for better performance

## Custom Domain (Optional)

1. In Vercel dashboard, go to "Domains"
2. Add your custom domain
3. Update DNS records as instructed
4. Update YouTube API redirect URIs with new domain

## Security Best Practices

- ✅ Always use HTTPS (automatic with Vercel)
- ✅ Keep secrets in environment variables
- ✅ Regular dependency updates
- ✅ Monitor logs for suspicious activity

## Next Steps After Deployment

1. **Monitor Performance** - Use Vercel analytics
2. **Set Up Monitoring** - Consider Sentry for error tracking
3. **Backup Database** - Regular backups of your data
4. **Update Dependencies** - Keep packages updated

---

Your Flask YouTube Management Platform is now ready for production! 🎉
