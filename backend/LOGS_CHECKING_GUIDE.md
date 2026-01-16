# How to Check Logs (When Streaming is Disabled)

## Problem
`eb logs --stream` returns error: "Instance log streaming is disabled"

## Solution: Use Alternative Methods

### Method 1: Download All Logs (Recommended) ✅
```bash
eb logs
```
This downloads all logs to `.elasticbeanstalk/logs/latest/`

### Method 2: View Specific Log Files (PowerShell)
```powershell
# Django application logs (most important)
Get-Content .elasticbeanstalk\logs\latest\*\var\log\web.stdout.log | Select-Object -Last 100

# Nginx access logs
Get-Content .elasticbeanstalk\logs\latest\*\var\log\nginx\access.log | Select-Object -Last 50

# Nginx error logs
Get-Content .elasticbeanstalk\logs\latest\*\var\log\nginx\error.log | Select-Object -Last 50

# Elastic Beanstalk engine logs
Get-Content .elasticbeanstalk\logs\latest\*\var\log\eb-engine.log | Select-Object -Last 50
```

### Method 3: SSH into Instance
```bash
eb ssh
# Then inside the instance:
tail -f /var/log/web.stdout.log
tail -f /var/log/nginx/access.log
```

### Method 4: View Logs via AWS Console
1. Go to AWS Console → Elastic Beanstalk
2. Select your environment: `ai-blog-env`
3. Click **Logs** → **Request Logs** → **Last 100 Lines**
4. Or click **Download Logs** for full logs

## What to Look For in Logs

### Common Errors:

1. **404 Not Found**
   - Look for: `WARNING ... Not Found: /some-url`
   - Fix: Check URL routing in `urls.py`

2. **500 Internal Server Error**
   - Look for: `ERROR ... Exception in ...`
   - Fix: Check traceback in logs

3. **Authentication Errors**
   - Look for: `DisallowedHost` or `Invalid HTTP_HOST`
   - Fix: Add IP/domain to `ALLOWED_HOSTS` in `settings.py`

4. **JSON Parsing Errors**
   - Look for: `Unexpected token '<', "<!DOCTYPE "...`
   - Fix: Server returning HTML instead of JSON (usually authentication issue)

## Recent Fix Applied

### Issue: JSON Parsing Error
**Error**: `Error: Unexpected token '<', "<!DOCTYPE "... is not valid JSON`

**Cause**: 
- User not logged in
- Django's `@login_required` decorator redirects to login page (HTML)
- JavaScript expects JSON but gets HTML

**Fix Applied**:
1. ✅ Removed `@login_required` decorator
2. ✅ Added manual authentication check
3. ✅ Return JSON error for AJAX requests instead of redirecting
4. ✅ Updated JavaScript to handle login_required responses

**Status**: ✅ Fixed and deployed!

## Quick Commands Reference

```bash
# Download all logs
eb logs

# View latest Django logs (PowerShell)
Get-Content .elasticbeanstalk\logs\latest\*\var\log\web.stdout.log | Select-Object -Last 100

# View latest Nginx access logs
Get-Content .elasticbeanstalk\logs\latest\*\var\log\nginx\access.log | Select-Object -Last 50

# SSH into instance
eb ssh

# Check environment status
eb status

# View logs via AWS Console
# Go to: AWS Console → Elastic Beanstalk → ai-blog-env → Logs
```
