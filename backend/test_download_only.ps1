# Test YouTube Audio Download Only
# This tests just the download functionality to diagnose issues

Write-Host "YouTube Audio Download Test" -ForegroundColor Cyan
Write-Host "===========================" -ForegroundColor Cyan
Write-Host ""

$testUrl = "https://www.youtube.com/watch?v=skMzCAga-dg"
Write-Host "Test URL: $testUrl" -ForegroundColor Yellow
Write-Host ""

# Change to backend directory
$backendDir = Join-Path $PSScriptRoot "."
Set-Location $backendDir
Write-Host "Working directory: $(Get-Location)" -ForegroundColor Gray
Write-Host ""

$testCode = @"
import sys
import os
import tempfile

# Add current directory to path
sys.path.insert(0, r'$backendDir')

try:
    from config.blog_generator import YouTubeBlogGenerator
    
    print('Initializing YouTubeBlogGenerator...')
    generator = YouTubeBlogGenerator()
    
    print(f'Testing download of: $testUrl')
    print('')
    
    # Test download
    audio_file = generator.download_audio('$testUrl')
    
    if audio_file and os.path.exists(audio_file):
        file_size = os.path.getsize(audio_file) / (1024 * 1024)  # Size in MB
        print('')
        print('=' * 60)
        print('SUCCESS! Audio downloaded')
        print('=' * 60)
        print(f'File: {audio_file}')
        print(f'Size: {file_size:.2f} MB')
        print('=' * 60)
        
        # Clean up
        try:
            os.unlink(audio_file)
            print('Temporary file cleaned up')
        except:
            pass
        
        sys.exit(0)
    else:
        print('')
        print('=' * 60)
        print('ERROR: Audio download failed')
        print('=' * 60)
        print('Could not download or find audio file')
        print('=' * 60)
        sys.exit(1)
        
except Exception as e:
    import traceback
    print('')
    print('=' * 60)
    print('EXCEPTION occurred')
    print('=' * 60)
    print(f'Error: {str(e)}')
    print('')
    traceback.print_exc()
    sys.exit(1)
"@

Write-Host "Running download test..." -ForegroundColor Green
Write-Host ""

$testCode | python

$result = $LASTEXITCODE

Write-Host ""

if ($result -eq 0) {
    Write-Host "✓ Download test PASSED!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Run: .\test_blog_generator.ps1 (full pipeline test)" -ForegroundColor Yellow
    Write-Host "  2. Or test in the web app" -ForegroundColor Yellow
} else {
    Write-Host "✗ Download test FAILED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Check if FFmpeg is installed: ffmpeg -version" -ForegroundColor White
    Write-Host "  2. Check internet connection" -ForegroundColor White
    Write-Host "  3. Try a different YouTube URL" -ForegroundColor White
    Write-Host "  4. Check if yt-dlp is up to date: pip install --upgrade yt-dlp" -ForegroundColor White
}

Write-Host ""
