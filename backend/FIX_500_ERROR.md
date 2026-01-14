# Fix 500 Server Error

## Issues Found and Fixed

### 1. Template Paths Issue ✅ FIXED
**Problem**: Templates were pointing to `BASE_DIR.parent / 'templates'` which doesn't exist on the server.

**Fix**: 
- Changed to `BASE_DIR / 'templates'`
- Created `backend/templates/` directory
- Copied all HTML files to `backend/templates/`

### 2. ALLOWED_HOSTS ✅ UPDATED
**Problem**: May not include the specific Elastic Beanstalk domain.

**Fix**: Added specific EB domain to ALLOWED_HOSTS.

### 3. Static Files ✅ FIXED
**Problem**: STATICFILES_DIRS pointing to non-existent directory.

**Fix**: Updated to use `BASE_DIR / 'static'` (will be empty but won't cause errors).

## Next Steps

### 1. Redeploy with fixes:
```bash
cd C:\temp\AI\AI_blog_app\backend
eb deploy
```

### 2. Check logs after deployment:
```bash
eb logs --stream
```

### 3. Test the application:
```bash
eb open
```

## If Still Getting 500 Error

### Check Django Error Logs:
```bash
eb logs | Select-String -Pattern "Traceback|Error|Exception" -Context 10
```

### Common Causes:
1. **Template not found** - Check templates are in `backend/templates/`
2. **Database migration issues** - Check migrations ran
3. **Missing environment variables** - Verify SECRET_KEY is set
4. **Import errors** - Check requirements.txt has all dependencies

### Enable DEBUG temporarily (for testing):
```bash
eb setenv DEBUG=True
eb deploy
```

This will show detailed error messages (disable after fixing!).

## Files Changed:
- ✅ `config/settings.py` - Fixed template paths and ALLOWED_HOSTS
- ✅ Created `backend/templates/` directory
- ✅ Copied HTML files to `backend/templates/`
