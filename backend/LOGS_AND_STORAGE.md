# Logs and Storage Guide

## 📋 Which Logs to Check

### 1. **Django Application Logs** (Most Important)
```bash
eb logs
# Or view specific log file:
Get-Content .elasticbeanstalk\logs\latest\*\var\log\web.stdout.log
```

**What to look for:**
- Django errors (500, 404, etc.)
- Application exceptions
- Database errors
- Blog generation errors

### 2. **Elastic Beanstalk Engine Logs**
```bash
Get-Content .elasticbeanstalk\logs\latest\*\var\log\eb-engine.log
```

**What to look for:**
- Deployment errors
- Package installation failures
- Configuration issues

### 3. **Nginx Access/Error Logs**
```bash
Get-Content .elasticbeanstalk\logs\latest\*\var\log\nginx\access.log
Get-Content .elasticbeanstalk\logs\latest\*\var\log\nginx\error.log
```

**What to look for:**
- HTTP request/response codes
- 404 errors (missing URLs)
- 500 errors (server errors)

### 4. **Real-time Log Streaming**
```bash
eb logs --stream
```

This shows logs in real-time as they happen.

## 🔍 Common Issues Found in Logs

### Issue: 404 Error on `/accounts/login/`
**Cause**: Django's `@login_required` decorator redirects to default `/accounts/login/` which doesn't exist.

**Fix**: Added `LOGIN_URL = '/login/'` to `settings.py` ✅ (Already fixed!)

### Issue: "No space left on device"
**Cause**: EBS volume too small for PyTorch installation.

**Fix**: Removed `openai-whisper` from `requirements.txt` ✅ (Already fixed!)

## 💾 EBS Storage on t3.small EC2

### Is EBS Storage Free?
**No, EBS storage is NOT free.** You pay per GB per month.

### Current Setup
- **Default Volume Size**: 8 GB
- **Volume Type**: gp3
- **Monthly Cost**: ~$0.80 ($0.10 per GB/month)
- **Status**: ✅ Enough for current setup (API-based transcription)

### Can We Increase Size for PyTorch?
**Yes!** You can increase EBS volume size easily.

### Cost to Increase Storage

| Size | Monthly Cost | Can Fit PyTorch? |
|------|-------------|------------------|
| 8 GB (current) | ~$0.80 | ❌ No |
| 20 GB | ~$2.00 | ✅ Yes (~$1.20 extra/month) |
| 30 GB | ~$3.00 | ✅ Yes (~$2.20 extra/month) |
| 50 GB | ~$5.00 | ✅ Yes (~$4.20 extra/month) |

## 🚀 How to Increase EBS Storage

### Option 1: Via AWS Console (Easiest) ⭐ Recommended

1. Go to [AWS Elastic Beanstalk Console](https://console.aws.amazon.com/elasticbeanstalk)
2. Select environment: **ai-blog-env**
3. Click **Configuration** → **Capacity**
4. Under **Root volume**, change **Volume size** from `8` to `20` (or more)
5. Click **Apply**
6. Wait ~5-10 minutes for update

### Option 2: Via EB Extensions

Create `.ebextensions/06_ebs_volume.config`:

```yaml
option_settings:
  aws:autoscaling:launchconfiguration:
    RootVolumeSize: 20
    RootVolumeType: gp3
```

Then deploy:
```bash
eb deploy
```

## 📊 Total Monthly Cost Comparison

### Current Setup (API-based transcription):
- EC2 t3.small: ~$15/month
- EBS 8GB: ~$0.80/month
- Data Transfer: ~$5-10/month
- **Total: ~$20-25/month**

### With 20GB + Local Whisper:
- EC2 t3.small: ~$15/month
- EBS 20GB: ~$2.00/month
- Data Transfer: ~$5-10/month
- **Total: ~$22-27/month**

**Extra cost for local Whisper: Only ~$2/month!**

## ✅ Recommendation

**Current Status**: ✅ Fixed 404 error, using API-based transcription (FREE)

**If you want local Whisper**:
1. Increase EBS to 20GB via AWS Console (~$2/month extra)
2. Add `openai-whisper>=20231117` back to `requirements.txt`
3. Run `eb deploy`

**Note**: Local Whisper requires ~2-3GB disk space and takes longer to install on first deployment.

## 📝 Quick Commands

```bash
# View all logs
eb logs

# Stream logs in real-time
eb logs --stream

# View specific log file (PowerShell)
Get-Content .elasticbeanstalk\logs\latest\*\var\log\web.stdout.log | Select-Object -Last 100

# Check environment status
eb status

# Deploy updates
eb deploy
```
