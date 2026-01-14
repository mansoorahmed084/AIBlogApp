# Fix Deployment Error: ModuleNotFoundError: No module named 'application'

## Problem
The deployment is failing with: `ModuleNotFoundError: No module named 'application'`

## Root Cause
Elastic Beanstalk is trying to import 'application' directly instead of using the correct WSGI path `config.wsgi:application`.

## Solution Applied

### ✅ Files Created/Updated:

1. **Procfile** - Created with correct WSGI path:
   ```
   web: gunicorn config.wsgi:application --bind 0.0.0.0:8000
   ```

2. **requirements.txt** - Added gunicorn:
   ```
   gunicorn==23.0.0
   ```

3. **.ebextensions/01_python.config** - Already configured correctly:
   ```
   WSGIPath: config.wsgi:application
   ```

## Next Steps

### Option 1: Redeploy (Recommended)

```bash
cd C:\temp\AI\AI_blog_app\backend
eb deploy
```

This will upload the new Procfile and requirements.txt.

### Option 2: Terminate and Recreate (If redeploy doesn't work)

```bash
# Terminate current environment
eb terminate ai-blog-env

# Wait for termination (takes 5-10 minutes)

# Create new environment
eb create ai-blog-env --instance-type t3.small --single
```

## Verify Files Are Correct

Make sure these files exist and have correct content:

### Procfile (in backend folder):
```
web: gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### requirements.txt should include:
```
Django==6.0.1
asgiref==3.11.0
sqlparse==0.5.5
tzdata==2025.2
gunicorn==23.0.0
```

### .ebextensions/01_python.config:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: config.wsgi:application
```

## After Deployment

Once deployment succeeds:

1. **Check status:**
   ```bash
   eb status
   ```

2. **Open application:**
   ```bash
   eb open
   ```

3. **View logs if issues:**
   ```bash
   eb logs
   ```

## Expected Result

After successful deployment, you should see:
- Environment status: "Ready"
- Health: "Ok"
- Your Django app accessible via the CNAME URL
