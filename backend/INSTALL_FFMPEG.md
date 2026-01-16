# How to Install FFmpeg on Windows

FFmpeg is required to convert downloaded audio files to WAV format for better transcription compatibility.

## Quick Installation Methods

### Method 1: Using Chocolatey (Easiest)

1. **Install Chocolatey** (if not already installed):
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force
   [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
   iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. **Install FFmpeg**:
   ```powershell
   choco install ffmpeg
   ```

3. **Verify installation**:
   ```powershell
   ffmpeg -version
   ```

### Method 2: Manual Installation

1. **Download FFmpeg**:
   - Go to: https://www.gyan.dev/ffmpeg/builds/
   - Download "ffmpeg-release-essentials.zip" (or latest version)

2. **Extract**:
   - Extract to: `C:\ffmpeg`

3. **Add to PATH**:
   - Open System Properties → Environment Variables
   - Edit "Path" variable
   - Add: `C:\ffmpeg\bin`
   - Click OK

4. **Verify**:
   - Open new PowerShell window
   - Run: `ffmpeg -version`

### Method 3: Using Winget (Windows 10/11)

```powershell
winget install ffmpeg
```

## Verify Installation

After installation, verify FFmpeg works:

```powershell
ffmpeg -version
```

You should see version information. If you get "command not found", restart your terminal or add FFmpeg to PATH.

## Note

**The app will work without FFmpeg**, but it will download audio in its original format (usually .webm). Most transcription services can handle .webm files, but WAV format (converted by FFmpeg) provides better compatibility.

## Troubleshooting

### "ffmpeg not found" after installation
- Restart your terminal/PowerShell
- Check PATH: `$env:PATH -split ';' | Select-String ffmpeg`
- Manually add to PATH if needed

### Still having issues?
The app will download audio without FFmpeg, but you may need to ensure your transcription service supports the downloaded format (usually .webm works fine).
