# PowerShell script to add FFmpeg to PATH
# Run as Administrator: Right-click PowerShell -> "Run as Administrator"

Write-Host "FFmpeg PATH Setup" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "WARNING: This script should be run as Administrator" -ForegroundColor Yellow
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
}

# Find FFmpeg
Write-Host "Searching for FFmpeg..." -ForegroundColor Green
$ffmpegPath = $null

# Check PATH first
$ffmpegInPath = Get-Command ffmpeg -ErrorAction SilentlyContinue
if ($ffmpegInPath) {
    $ffmpegPath = $ffmpegInPath.Source
    Write-Host "  ✓ Found in PATH: $ffmpegPath" -ForegroundColor Green
} else {
    # Check common locations
    $commonPaths = @(
        "C:\ffmpeg\bin\ffmpeg.exe",
        "C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        "C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
        "$env:USERPROFILE\ffmpeg\bin\ffmpeg.exe"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            $ffmpegPath = $path
            Write-Host "  ✓ Found: $ffmpegPath" -ForegroundColor Green
            break
        }
    }
    
    # Check WindowsApps
    if (-not $ffmpegPath) {
        $windowsApps = Get-ChildItem "C:\Program Files\WindowsApps" -Recurse -Filter "ffmpeg.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($windowsApps) {
            $ffmpegPath = $windowsApps.FullName
            Write-Host "  ✓ Found in WindowsApps: $ffmpegPath" -ForegroundColor Yellow
            Write-Host "    Note: This is from a Windows Store app. Consider installing FFmpeg properly." -ForegroundColor Yellow
        }
    }
}

if (-not $ffmpegPath) {
    Write-Host "  ✗ FFmpeg not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Install FFmpeg first:" -ForegroundColor Yellow
    Write-Host "  1. choco install ffmpeg" -ForegroundColor White
    Write-Host "  2. OR winget install ffmpeg" -ForegroundColor White
    Write-Host "  3. OR download from https://ffmpeg.org/download.html" -ForegroundColor White
    exit 1
}

# Get directory
$ffmpegDir = Split-Path $ffmpegPath -Parent
Write-Host ""
Write-Host "FFmpeg directory: $ffmpegDir" -ForegroundColor Cyan
Write-Host ""

# Check if already in PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
$pathParts = $currentPath -split ';'

if ($pathParts -contains $ffmpegDir) {
    Write-Host "✓ FFmpeg directory is already in PATH (User)" -ForegroundColor Green
} else {
    Write-Host "Adding to PATH..." -ForegroundColor Yellow
    
    # Add to User PATH
    $newPath = $currentPath
    if ($newPath -and -not $newPath.EndsWith(';')) {
        $newPath += ';'
    }
    $newPath += $ffmpegDir
    
    try {
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Host "✓ Added to User PATH" -ForegroundColor Green
        Write-Host ""
        Write-Host "IMPORTANT: Restart your terminal/PowerShell for changes to take effect!" -ForegroundColor Yellow
    } catch {
        Write-Host "✗ Failed to add to PATH: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "Manual steps:" -ForegroundColor Yellow
        Write-Host "  1. Open System Properties -> Environment Variables" -ForegroundColor White
        Write-Host "  2. Edit 'Path' under User variables" -ForegroundColor White
        Write-Host "  3. Add: $ffmpegDir" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "Verification:" -ForegroundColor Cyan
Write-Host "  After restarting terminal, run: ffmpeg -version" -ForegroundColor White
Write-Host ""
