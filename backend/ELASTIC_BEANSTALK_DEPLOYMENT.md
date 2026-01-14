# AWS Elastic Beanstalk Deployment Guide

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
3. **EB CLI** (Elastic Beanstalk Command Line Interface)
4. **Python 3.13** (or compatible version)

---

## Step 1: Install EB CLI

```bash
pip install awsebcli
```

Verify installation:
```bash
eb --version
```

---

## Step 2: Configure AWS Credentials

If not already configured:

```bash
aws configure
```

Enter:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `ap-south-1` (or your preferred region)
- Default output format: `json`

---

## Step 3: Initialize Elastic Beanstalk

Navigate to your backend directory:

```bash
cd C:\temp\AI\AI_blog_app\backend
```

Initialize EB:

```bash
eb init
```

**Configuration prompts:**
1. **Select a region**: Choose `ap-south-1` (Mumbai) or your preferred region
2. **Application name**: `ai-blog-generator` (or your choice)
3. **Python version**: Select `Python 3.13` (or latest available)
4. **SSH**: Choose `Yes` if you want SSH access
5. **Keypair**: Select existing or create new

This creates `.elasticbeanstalk/config.yml`

---

## Step 4: Create Environment

Create your first environment:

```bash
eb create ai-blog-env
```

**Or with specific options:**

```bash
eb create ai-blog-env \
  --instance-type t3.small \
  --region ap-south-1 \
  --platform "Python 3.13" \
  --single
```

**Options explained:**
- `--instance-type t3.small`: Small instance (cheaper, ~$15/month)
- `--single`: Single instance (no load balancer, cheaper)
- `--region`: Your preferred AWS region

**For production (with load balancer):**
```bash
eb create ai-blog-prod \
  --instance-type t3.medium \
  --region ap-south-1 \
  --platform "Python 3.13"
```

---

## Step 5: Set Environment Variables

Set Django secret key and other variables:

```bash
eb setenv SECRET_KEY="your-secret-key-here" DEBUG=False
```

**Or set multiple variables:**

```bash
eb setenv \
  SECRET_KEY="your-secret-key-here" \
  DEBUG=False \
  ALLOWED_HOST="yourdomain.com"
```

**Generate a secure secret key:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Step 6: Deploy Application

Deploy your application:

```bash
eb deploy
```

This will:
1. Create a zip file of your application
2. Upload to S3
3. Deploy to Elastic Beanstalk
4. Run migrations and collectstatic (via .ebextensions)

**First deployment takes 5-10 minutes**

---

## Step 7: Open Your Application

Open in browser:

```bash
eb open
```

Or get the URL:

```bash
eb status
```

Look for `CNAME` in the output.

---

## Step 8: View Logs

Check deployment logs:

```bash
eb logs
```

View real-time logs:

```bash
eb logs --stream
```

---

## Common Commands

### Check Status
```bash
eb status
```

### SSH into Instance
```bash
eb ssh
```

### Update Environment Variables
```bash
eb setenv VARIABLE_NAME="value"
```

### Deploy Updates
```bash
eb deploy
```

### Terminate Environment
```bash
eb terminate ai-blog-env
```

### List Environments
```bash
eb list
```

### Switch Environments
```bash
eb use ai-blog-env
```

---

## Project Structure

Your backend folder should have:

```
backend/
├── .ebextensions/
│   ├── 01_python.config
│   ├── 02_staticfiles.config
│   ├── 03_migrate.config
│   └── 04_collectstatic.config
├── .ebignore
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── staticfiles/ (created during deployment)
```

---

## Static Files Configuration

Static files are automatically collected during deployment via `.ebextensions/04_collectstatic.config`.

Your static files will be served from `/static/` URL path.

---

## Database Configuration

Currently using SQLite (db.sqlite3). For production, consider:

### Option 1: RDS PostgreSQL (Recommended)

1. Create RDS instance via AWS Console
2. Update settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}
```

3. Set environment variables:
```bash
eb setenv \
  RDS_DB_NAME=mydb \
  RDS_USERNAME=admin \
  RDS_PASSWORD=password \
  RDS_HOSTNAME=your-rds-endpoint.region.rds.amazonaws.com \
  RDS_PORT=5432
```

### Option 2: Keep SQLite (for testing only)

SQLite works but is not recommended for production.

---

## Troubleshooting

### Issue: Static files not loading

**Solution:**
1. Check `.ebextensions/02_staticfiles.config` exists
2. Verify `STATIC_ROOT` in settings.py
3. Run `eb deploy` again

### Issue: 500 Internal Server Error

**Solution:**
1. Check logs: `eb logs`
2. Verify `ALLOWED_HOSTS` includes Elastic Beanstalk domain
3. Check environment variables are set correctly

### Issue: Migration errors

**Solution:**
1. Check `.ebextensions/03_migrate.config` exists
2. Verify database connection
3. Check logs: `eb logs`

### Issue: Module not found

**Solution:**
1. Verify all dependencies in `requirements.txt`
2. Run `pip freeze > requirements.txt` locally
3. Redeploy: `eb deploy`

---

## Cost Estimation

### Single Instance (t3.small):
- **EC2 Instance**: ~$15/month
- **EBS Storage**: ~$1-2/month (10GB)
- **Data Transfer**: ~$5-10/month
- **Total**: ~$20-30/month

### With Load Balancer (t3.medium):
- **EC2 Instance**: ~$30/month
- **Load Balancer**: ~$16/month
- **EBS Storage**: ~$1-2/month
- **Data Transfer**: ~$10-20/month
- **Total**: ~$60-70/month

**Much cheaper than EKS!**

---

## Next Steps

1. ✅ Deploy successfully
2. ✅ Test your application
3. ✅ Set up custom domain (optional)
4. ✅ Configure RDS database (optional)
5. ✅ Set up SSL certificate (HTTPS)
6. ✅ Configure auto-scaling (optional)
7. ✅ Set up monitoring and alerts

---

## Quick Start Summary

```bash
# 1. Install EB CLI
pip install awsebcli

# 2. Navigate to backend
cd C:\temp\AI\AI_blog_app\backend

# 3. Initialize
eb init

# 4. Create environment
eb create ai-blog-env --instance-type t3.small --single

# 5. Set environment variables
eb setenv SECRET_KEY="your-secret-key" DEBUG=False

# 6. Deploy
eb deploy

# 7. Open
eb open
```

---

## Files Created

All necessary configuration files have been created:
- ✅ `requirements.txt`
- ✅ `.ebextensions/` (all config files)
- ✅ `.ebignore`
- ✅ Updated `settings.py` for production

You're ready to deploy! 🚀
