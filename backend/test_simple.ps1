# Simple Quick Test Script
# Tests just the YouTube download functionality

Write-Host "Quick YouTube Download Test" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

$testUrl = "https://www.youtube.com/watch?v=skMzCAga-dg"
Write-Host "Testing URL: $testUrl" -ForegroundColor Yellow
Write-Host ""

# Check if yt-dlp is installed
Write-Host "Checking yt-dlp..." -ForegroundColor Green
try {
    python -c "import yt_dlp; print('yt-dlp version:', yt_dlp.version.__version__)" 2>&1
    Write-Host "✓ yt-dlp is installed" -ForegroundColor Green
} catch {
    Write-Host "✗ yt-dlp is NOT installed" -ForegroundColor Red
    Write-Host "Install with: pip install yt-dlp" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Testing video info extraction..." -ForegroundColor Green

$testCode = @"
import yt_dlp
import sys

url = r'$testUrl'

try:
    ydl_opts = {
        'quiet': False,
        'no_warnings': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print('Extracting video info...')
        info = ydl.extract_info(url, download=False)
        
        print('')
        print('=' * 60)
        print('SUCCESS! Video info extracted:')
        print('=' * 60)
        print(f"Title: {info.get('title', 'N/A')}")
        print(f"Channel: {info.get('uploader', 'N/A')}")
        print(f"Duration: {info.get('duration', 0)} seconds")
        print(f"View Count: {info.get('view_count', 'N/A')}")
        print('=' * 60)
        sys.exit(0)
        
except Exception as e:
    print('')
    print('=' * 60)
    print('ERROR:', str(e))
    print('=' * 60)
    import traceback
    traceback.print_exc()
    sys.exit(1)
"@

$testCode | python

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Test PASSED - YouTube download should work!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "✗ Test FAILED - Check error above" -ForegroundColor Red
}

Write-Host ""
