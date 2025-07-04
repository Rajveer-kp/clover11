# Deployment Guide for Clover11 YouTube Management Dashboard

## Deploy to Railway with Custom Domain (clover11.me)

Railway is an excellent platform for hosting Flask applications and supports custom domains like your clover11.me.

### 1. **Push Your Code to GitHub**
   - Make sure your code is in the GitHub repository: `https://github.com/Rajveer-kp/clover11.git`
   - Ensure you have the following files in your repository:
     - `requirements.txt` - Lists all Python dependencies
     - `Procfile` - Contains `web: gunicorn wsgi:app`
     - `runtime.txt` - Specifies the Python version
     - `wsgi.py` - Entry point for the application

### 2. **Sign up for Railway**
   - Go to [Railway.app](https://railway.app)
   - Sign up with your GitHub account

### 3. **Create a New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Find and select your repository: `Rajveer-kp/clover11`
   - Allow Railway to access your repository

### 4. **Configure Environment Variables**
   - Railway will automatically detect your Python project
   - Add required environment variables in the "Variables" tab:
     - SECRET_KEY: [your-secret-key]
     - FLASK_ENV: production
     - YOUTUBE_CLIENT_ID: [your-youtube-client-id]
     - YOUTUBE_CLIENT_SECRET: [your-youtube-client-secret]
     - ADSENSE_CLIENT_ID: [your-adsense-client-id]
     - DATABASE_URL: (if using a production database)

### 5. **Deploy Your Application**
   - Railway will automatically build and deploy your app
   - Monitor the build logs to ensure everything is working
   - Once deployed, you'll get a temporary domain like `https://your-app-name.railway.app`

### 6. **Set Up Custom Domain (clover11.me)**
   - In Railway's project settings, go to the "Settings" tab
   - Find the "Domains" section
   - Click "Generate Domain" (to get a temporary domain first)
   - Click "Custom Domain"
   - Enter your domain: `clover11.me`
   - Railway will provide DNS configuration instructions

### 7. **Configure DNS for clover11.me**
   - Go to your domain registrar (where you purchased clover11.me)
   - Add the CNAME record as instructed by Railway
     - Type: CNAME
     - Name: @ (or leave blank for root domain)
     - Value: [the Railway-provided domain]
   - If your registrar doesn't support CNAME at the root domain:
     - Use the A records provided by Railway instead
   - Wait for DNS propagation (can take up to 24 hours)

### 8. **Update OAuth and API Configurations**
   - Update your Google OAuth settings to include your new domain
   - Add `https://clover11.me` to the list of authorized redirect URIs
   - Update AdSense configuration to include your new domain

## Post-Deployment Verification

After deployment, verify the following:
- YouTube OAuth connection works correctly
- AdSense ads display properly
- Video upload and approval functions work
- All pages load without errors
- Database connections function properly

## Important Production Considerations

1. **Environment Variables**: All sensitive credentials should be stored as environment variables in Railway, not hardcoded.

2. **Database**: 
   - The current setup uses SQLite which is not ideal for production
   - Railway offers PostgreSQL which you can provision directly in your project
   - Update your Flask app's database configuration to use the DATABASE_URL environment variable

3. **File Storage**:
   - Uploaded files in `/pending_uploads` and `/temp_uploads` won't persist on Railway's ephemeral filesystem
   - Consider using a cloud storage solution like AWS S3 or Google Cloud Storage for video files
   - Update your code to store/retrieve files from cloud storage

4. **Scaling**:
   - Railway allows you to adjust resources as needed
   - Monitor your application's performance and scale accordingly

5. **Monitoring**:
   - Enable Railway's built-in monitoring
   - Set up alerts for critical errors or performance issues

6. **Backup**:
   - Regularly backup your database
   - If using Railway's PostgreSQL, backups are handled automatically

7. **HTTPS**:
   - Railway automatically provides HTTPS for your custom domain
   - Ensure all assets are loaded over HTTPS to avoid mixed content warnings

## Step-by-Step Deployment Commands

Here are the exact commands to push your code to GitHub and deploy to Railway:

```bash
# Navigate to your project directory
cd c:\Users\rajve\Desktop\clover

# Initialize Git repository (if not already done)
git init

# Add all files to git
git add .

# Commit your changes
git commit -m "Prepare for Railway deployment"

# Add your GitHub repository as remote
git remote add origin https://github.com/Rajveer-kp/clover11.git

# Push to GitHub
git push -u origin main
```

After pushing to GitHub, follow the Railway deployment steps in the guide above.
