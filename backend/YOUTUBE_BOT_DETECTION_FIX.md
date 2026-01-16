# YouTube Bot Detection Fix

## Problem
**Error**: `Sign in to confirm you're not a bot. Use --cookies-from-browser or --cookies for the authentication.`

**Cause**: YouTube is blocking yt-dlp requests because they appear to come from a bot/server.

## Solution Applied

Updated `blog_generator.py` to include:
1. **User Agent**: Set to Chrome browser user agent string
2. **Android Client**: Use Android player client (less strict bot detection)

### Changes Made:
- Added `user_agent` to yt-dlp options
- Added `extractor_args` with Android client preference
- Applied to both `get_video_info()` and `download_audio()` methods

## Testing

Try generating a blog post again. The YouTube bot detection should be bypassed.

## If Issue Persists

If YouTube still blocks requests, try these alternatives:

### Option 1: Use Cookies (Most Reliable)
1. Export YouTube cookies from your browser
2. Save cookies file to EC2 instance
3. Update `blog_generator.py` to use cookies:

```python
ydl_opts = {
    # ... other options ...
    'cookiefile': '/path/to/cookies.txt',
}
```

### Option 2: Try Different Client
Update `extractor_args` to use different clients:

```python
'extractor_args': {
    'youtube': {
        'player_client': ['ios', 'android', 'web'],  # Try iOS first
    }
}
```

### Option 3: Use YouTube API (Paid)
For production, consider using YouTube Data API v3 (requires API key, has quotas).

## Current Status

✅ **Fix Deployed**: User agent and Android client configured
🔄 **Testing**: Try generating a blog post now

## Monitoring

Check logs if it still fails:
```bash
eb logs
Get-Content .elasticbeanstalk\logs\latest\*\var\log\web.stdout.log | Select-String -Pattern "youtube|bot|error"
```
