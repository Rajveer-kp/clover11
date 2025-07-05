# Environment Variables Guide

## 🔐 Required Environment Variables

This guide covers all environment variables needed for deploying the YouTube Management Platform on any cloud platform.

## Core Environment Variables

### Flask Application
```bash
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
```

### Google OAuth (YouTube API)
```bash
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
GOOGLE_OAUTH_PROJECT_ID=your-google-project-id
GOOGLE_OAUTH_REDIRECT_URIS=https://your-domain.com/youtube/oauth2callback
```

### Database
```bash
DATABASE_URL=postgresql://username:password@hostname:port/database
```

## Getting Google OAuth Credentials

### 1. Go to Google Cloud Console
- Visit [Google Cloud Console](https://console.cloud.google.com)
- Create a new project or select existing one

### 2. Enable YouTube Data API v3
- Go to "APIs & Services" > "Library"
- Search for "YouTube Data API v3"
- Click "Enable"

### 3. Create OAuth 2.0 Credentials
- Go to "APIs & Services" > "Credentials"
- Click "Create Credentials" > "OAuth 2.0 Client ID"
- Choose "Web application"
- Name: "YouTube Manager"

### 4. Configure OAuth Settings
- **Authorized JavaScript origins**: Add your domain
  ```
  https://your-domain.com
  ```
- **Authorized redirect URIs**: Add callback URL
  ```
  https://your-domain.com/youtube/oauth2callback
  ```

### 5. Get Your Credentials
- **Client ID**: Copy the client ID
- **Client Secret**: Copy the client secret
- **Project ID**: Found in project settings

## Platform-Specific Instructions

### Vercel
```bash
# Add in Vercel dashboard under Settings > Environment Variables
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
GOOGLE_OAUTH_PROJECT_ID=your-project-id
GOOGLE_OAUTH_REDIRECT_URIS=https://your-app.vercel.app/youtube/oauth2callback
SECRET_KEY=your-secret-key
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host:port/db
```

### Railway
```bash
# Add in Railway dashboard under Variables tab
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
GOOGLE_OAUTH_PROJECT_ID=your-project-id
GOOGLE_OAUTH_REDIRECT_URIS=https://your-app.railway.app/youtube/oauth2callback
SECRET_KEY=your-secret-key
FLASK_ENV=production
# DATABASE_URL is auto-provided by Railway
```

### DigitalOcean App Platform
```bash
# Add in DigitalOcean dashboard under Settings > Environment Variables
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
GOOGLE_OAUTH_PROJECT_ID=your-project-id
GOOGLE_OAUTH_REDIRECT_URIS=https://your-app.ondigitalocean.app/youtube/oauth2callback
SECRET_KEY=your-secret-key
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host:port/db
```

### Render
```bash
# Add in Render dashboard under Environment tab
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
GOOGLE_OAUTH_PROJECT_ID=your-project-id
GOOGLE_OAUTH_REDIRECT_URIS=https://your-app.onrender.com/youtube/oauth2callback
SECRET_KEY=your-secret-key
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host:port/db
```

## Security Best Practices

### 1. Secret Key Generation
Generate a strong secret key:
```python
import secrets
secret_key = secrets.token_hex(32)
print(secret_key)
```

### 2. Environment Variable Security
- ✅ Never commit secrets to version control
- ✅ Use platform environment variable managers
- ✅ Rotate secrets regularly
- ✅ Use different secrets for dev/staging/prod

### 3. OAuth Security
- ✅ Only add necessary redirect URIs
- ✅ Use HTTPS in production
- ✅ Keep client secrets secure
- ✅ Monitor OAuth usage in Google Console

## Development vs Production

### Development (.env file)
```bash
# For local development only - never commit this file!
SECRET_KEY=dev-secret-key-only
FLASK_ENV=development
GOOGLE_OAUTH_CLIENT_ID=your-dev-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-dev-client-secret
GOOGLE_OAUTH_PROJECT_ID=your-project-id
GOOGLE_OAUTH_REDIRECT_URIS=http://localhost:5000/youtube/oauth2callback
DATABASE_URL=sqlite:///instance/site.db
```

### Production
- Use platform-specific environment variable managers
- Never use localhost URLs in production
- Always use HTTPS
- Use production databases (PostgreSQL)

## Troubleshooting

### Common Issues:

1. **"OAuth Error: redirect_uri_mismatch"**
   - Check redirect URIs in Google Cloud Console
   - Ensure exact match with deployed domain
   - Include `/youtube/oauth2callback` path

2. **"Invalid client_id"**
   - Verify `GOOGLE_OAUTH_CLIENT_ID` is correct
   - Check for extra spaces or characters
   - Ensure environment variable is set

3. **"Application not found"**
   - Verify `GOOGLE_OAUTH_PROJECT_ID` is correct
   - Ensure YouTube Data API v3 is enabled

4. **Database Connection Errors**
   - Check `DATABASE_URL` format
   - Ensure database is accessible from deployment platform
   - Verify username/password are correct

## Environment Variable Validation

The app includes fallback values for development, but production deployments should set all variables explicitly:

```python
# In youtube_auth.py - environment variables are checked
GOOGLE_OAUTH_CLIENT_ID=os.getenv('GOOGLE_OAUTH_CLIENT_ID', 'fallback-for-dev')
GOOGLE_OAUTH_CLIENT_SECRET=os.getenv('GOOGLE_OAUTH_CLIENT_SECRET', 'fallback-for-dev')
```

## Next Steps

1. ✅ Set up environment variables on your chosen platform
2. ✅ Configure Google OAuth with correct redirect URIs
3. ✅ Test OAuth flow after deployment
4. ✅ Monitor logs for any configuration issues
5. ✅ Set up database backups and monitoring

---

Your environment is now properly configured for secure production deployment! 🔐
