# PowerShell Test Script for YouTube Blog Generator
# This script tests the blog generation functionality step by step

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "YouTube Blog Generator - Test Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Test YouTube URL
$testUrl = "https://www.youtube.com/watch?v=skMzCAga-dg"
Write-Host "Test YouTube URL: $testUrl" -ForegroundColor Yellow
Write-Host ""

# Step 1: Check Python and required packages
Write-Host "Step 1: Checking Python and packages..." -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found! Please install Python." -ForegroundColor Red
    exit 1
}

# Check if we're in the right directory
$currentDir = Get-Location
Write-Host "  Current directory: $currentDir" -ForegroundColor Gray

# Step 2: Check required packages
Write-Host ""
Write-Host "Step 2: Checking required packages..." -ForegroundColor Green

$packages = @(
    "yt-dlp",
    "openai-whisper",
    "requests",
    "openai"
)

$missingPackages = @()
foreach ($package in $packages) {
    try {
        python -c "import $($package.Replace('-', '_'))" 2>&1 | Out-Null
        Write-Host "  ✓ $package installed" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ $package NOT installed" -ForegroundColor Red
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host ""
    Write-Host "Missing packages detected. Install with:" -ForegroundColor Yellow
    Write-Host "  pip install $($missingPackages -join ' ')" -ForegroundColor Yellow
    Write-Host ""
}

# Step 3: Check FFmpeg
Write-Host ""
Write-Host "Step 3: Checking FFmpeg..." -ForegroundColor Green
try {
    $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Host "  ✓ FFmpeg found: $($ffmpegVersion -split ' ' | Select-Object -First 3 -join ' ')" -ForegroundColor Green
} catch {
    Write-Host "  ✗ FFmpeg not found! Audio extraction will fail." -ForegroundColor Red
    Write-Host "    Download from: https://ffmpeg.org/download.html" -ForegroundColor Yellow
    Write-Host "    Or install with: choco install ffmpeg" -ForegroundColor Yellow
}

# Step 4: Check API keys
Write-Host ""
Write-Host "Step 4: Checking API keys..." -ForegroundColor Green

# Check Groq API key
$groqKeyFile = "C:\temp\AI\secret keys\groq_api_key.txt"
if (Test-Path $groqKeyFile) {
    $groqKey = Get-Content $groqKeyFile -Raw | ForEach-Object { $_.Trim() }
    if ($groqKey) {
        Write-Host "  ✓ Groq API key found in file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Groq API key file is empty" -ForegroundColor Red
    }
} else {
    $groqKey = $env:GROQ_API_KEY
    if ($groqKey) {
        Write-Host "  ✓ Groq API key found in environment variable" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Groq API key not found (file or env var)" -ForegroundColor Yellow
        Write-Host "    File: $groqKeyFile" -ForegroundColor Gray
        Write-Host "    Or set: `$env:GROQ_API_KEY='your-key'" -ForegroundColor Gray
    }
}

# Check AssemblyAI API key
$assemblyaiKeyFile = "C:\temp\AI\secret keys\assemblyAI_key.txt"
if (Test-Path $assemblyaiKeyFile) {
    $assemblyaiKey = Get-Content $assemblyaiKeyFile -Raw | ForEach-Object { $_.Trim() }
    if ($assemblyaiKey) {
        Write-Host "  ✓ AssemblyAI API key found in file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ AssemblyAI API key file is empty" -ForegroundColor Red
    }
} else {
    $assemblyaiKey = $env:ASSEMBLYAI_API_KEY
    if ($assemblyaiKey) {
        Write-Host "  ✓ AssemblyAI API key found in environment variable" -ForegroundColor Green
    } else {
        Write-Host "  ✗ AssemblyAI API key not found (optional)" -ForegroundColor Yellow
    }
}

# Step 5: Test YouTube video download
Write-Host ""
Write-Host "Step 5: Testing YouTube video download..." -ForegroundColor Green
Write-Host "  This may take a minute..." -ForegroundColor Gray

$testScript = @"
import sys
import os
sys.path.insert(0, r'$currentDir')

try:
    import yt_dlp
    from urllib.parse import urlparse
    
    url = r'$testUrl'
    print(f'Testing download of: {url}')
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', 'Unknown')
        duration = info.get('duration', 0)
        print(f'SUCCESS: Video found')
        print(f'Title: {title}')
        print(f'Duration: {duration} seconds')
        sys.exit(0)
except Exception as e:
    print(f'ERROR: {str(e)}')
    sys.exit(1)
"@

$testScript | python
$downloadTest = $LASTEXITCODE

if ($downloadTest -eq 0) {
    Write-Host "  ✓ YouTube video download test PASSED" -ForegroundColor Green
} else {
    Write-Host "  ✗ YouTube video download test FAILED" -ForegroundColor Red
    Write-Host "    Check your internet connection and YouTube URL" -ForegroundColor Yellow
}

# Step 6: Test full pipeline (if download works)
if ($downloadTest -eq 0) {
    Write-Host ""
    Write-Host "Step 6: Testing full pipeline (download + transcribe + generate)..." -ForegroundColor Green
    Write-Host "  This will take several minutes..." -ForegroundColor Gray
    Write-Host "  Press Ctrl+C to cancel" -ForegroundColor Yellow
    Write-Host ""
    
    $pipelineTest = @"
import sys
import os
sys.path.insert(0, r'$currentDir')

try:
    from config.blog_generator import YouTubeBlogGenerator
    
    url = r'$testUrl'
    print(f'Processing YouTube video: {url}')
    print('')
    
    generator = YouTubeBlogGenerator()
    result = generator.process_youtube_video(url)
    
    if result['success']:
        print('')
        print('=' * 50)
        print('SUCCESS! Blog post generated')
        print('=' * 50)
        print(f"Title: {result['blog_post']['title']}")
        print(f"Description: {result['blog_post']['description'][:100]}...")
        print(f"Content length: {len(result['blog_post']['content'])} characters")
        print('')
        sys.exit(0)
    else:
        print('')
        print('=' * 50)
        print('ERROR: Blog generation failed')
        print('=' * 50)
        print(f"Error: {result.get('error', 'Unknown error')}")
        print('')
        sys.exit(1)
        
except Exception as e:
    import traceback
    print('')
    print('=' * 50)
    print('EXCEPTION occurred')
    print('=' * 50)
    print(f"Error: {str(e)}")
    print('')
    traceback.print_exc()
    sys.exit(1)
"@
    
    Write-Host "Starting pipeline test..." -ForegroundColor Cyan
    $pipelineTest | python
    $pipelineResult = $LASTEXITCODE
    
    if ($pipelineResult -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "✓ ALL TESTS PASSED!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Red
        Write-Host "✗ PIPELINE TEST FAILED" -ForegroundColor Red
        Write-Host "========================================" -ForegroundColor Red
        Write-Host "Check the error message above for details" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "Skipping pipeline test (download test failed)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Test script completed!" -ForegroundColor Cyan
Write-Host ""
