# Elastic Beanstalk Deployment Guide

## Quick Answer

**Yes!** `eb deploy` will update your latest code on EC2, and once deployed, your app will be accessible from **any PC** via the Elastic Beanstalk URL.

## Deployment Process

### 1. Deploy Latest Code

```powershell
cd C:\temp\AI\AI_blog_app\backend
eb deploy
```

This will:
- ✅ Upload your latest code to EC2
- ✅ Run database migrations
- ✅ Collect static files
- ✅ Restart the application
- ✅ Make it accessible from anywhere via the EB URL

### 2. Access from Any PC

After deployment, your app will be accessible at:
- **EB URL**: `http://your-app-name.region.elasticbeanstalk.com`
- Or your custom domain if configured

**Anyone with the URL can access it from any PC, anywhere in the world!**

## Pre-Deployment Checklist

### 1. Set Environment Variables on EB

Set your API keys as environment variables on Elastic Beanstalk:

```powershell
# Set Groq API key
eb setenv GROQ_API_KEY="your-groq-api-key"

# Set AssemblyAI API key (optional)
eb setenv ASSEMBLYAI_API_KEY="your-assemblyai-key"

# Set Django secret key
eb setenv SECRET_KEY="your-secret-key-here"

# Set debug mode (should be False for production)
eb setenv DEBUG=False
```

**OR** use the EB console:
1. Go to AWS Console → Elastic Beanstalk → Your Environment → Configuration
2. Software → Environment Properties
3. Add environment variables

### 2. FFmpeg Installation

FFmpeg will be automatically installed on EC2 via the `.ebextensions/05_install_ffmpeg.config` file.

**Note:** The first deployment may take longer as FFmpeg installs.

### 3. Whisper Model Download

On first use, Whisper will download the model (~150MB for "base" model). This happens automatically when someone generates their first blog post.

## Deployment Commands

### Deploy Latest Code
```powershell
eb deploy
```

### Check Deployment Status
```powershell
eb status
eb health
```

### View Logs
```powershell
eb logs
```

### Open in Browser
```powershell
eb open
```

### Set Environment Variables
```powershell
eb setenv VARIABLE_NAME="value"
```

### View Environment Variables
```powershell
eb printenv
```

## Important Notes for Production

### 1. API Keys on EC2

**File-based API keys won't work on EC2** - you need to use environment variables:

- ❌ `C:\temp\AI\secret keys\groq_api_key.txt` (won't exist on EC2)
- ✅ `GROQ_API_KEY` environment variable (works on EC2)

Set them with:
```powershell
eb setenv GROQ_API_KEY="your-key"
eb setenv ASSEMBLYAI_API_KEY="your-key"
```

### 2. FFmpeg on EC2

FFmpeg will be installed automatically via `.ebextensions/05_install_ffmpeg.config`.

If installation fails, you can SSH into the instance and install manually:
```powershell
eb ssh
# Then inside EC2:
sudo dnf install -y epel-release
sudo dnf install -y https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm
sudo dnf install -y ffmpeg
```

### 3. Database

- SQLite database (`db.sqlite3`) will be created on EC2
- **Note:** SQLite on EC2 is not persistent across deployments by default
- For production, consider using RDS (PostgreSQL/MySQL)

### 4. Static Files

Static files are collected automatically via `.ebextensions/04_collectstatic.config`.

### 5. File Storage

Temporary audio files are stored in `/tmp` on EC2, which is fine for temporary processing.

## Step-by-Step Deployment

### First Time Setup

1. **Navigate to backend directory:**
   ```powershell
   cd C:\temp\AI\AI_blog_app\backend
   ```

2. **Initialize EB (if not done):**
   ```powershell
   eb init
   ```

3. **Create environment (if not exists):**
   ```powershell
   eb create your-app-name
   ```

4. **Set environment variables:**
   ```powershell
   eb setenv GROQ_API_KEY="your-key" ASSEMBLYAI_API_KEY="your-key" DEBUG=False
   ```

5. **Deploy:**
   ```powershell
   eb deploy
   ```

### Subsequent Deployments

Just run:
```powershell
eb deploy
```

## Accessing Your Deployed App

### Get Your App URL

```powershell
eb status
```

Look for "CNAME" - that's your app URL:
```
CNAME: your-app-name.us-east-1.elasticbeanstalk.com
```

### Open in Browser

```powershell
eb open
```

Or manually visit: `http://your-app-name.region.elasticbeanstalk.com`

## Troubleshooting

### Check Deployment Logs
```powershell
eb logs
```

### SSH into EC2 Instance
```powershell
eb ssh
```

### Check if FFmpeg is Installed
```powershell
eb ssh
ffmpeg -version
```

### Check Environment Variables
```powershell
eb printenv
```

### Restart Application
```powershell
eb restart
```

## Cost Considerations

- **EC2 Instance**: ~$10-30/month (t2.micro/t2.small)
- **Data Transfer**: Usually free tier covers it
- **Storage**: Minimal for this app

**Total estimated cost: ~$10-30/month** (depending on instance size)

## Security Notes

1. ✅ Set `DEBUG=False` in production
2. ✅ Use strong `SECRET_KEY`
3. ✅ Don't commit API keys to git
4. ✅ Use HTTPS (configure SSL certificate in EB)
5. ✅ Set up proper `ALLOWED_HOSTS`

## Summary

- ✅ `eb deploy` updates your code on EC2
- ✅ App is accessible from any PC via EB URL
- ✅ FFmpeg installs automatically
- ✅ Environment variables needed for API keys
- ✅ First deployment takes longer (FFmpeg + model downloads)

Your app will be live and accessible from anywhere once deployed! 🚀
