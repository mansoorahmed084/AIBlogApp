#!/usr/bin/env python
"""
Check if all requirements are installed
Run with: python check_requirements.py
"""
import sys
import subprocess
import shutil

def check_python_package(package_name, import_name=None):
    """Check if a Python package is installed"""
    if import_name is None:
        import_name = package_name.replace('-', '_')
    
    try:
        __import__(import_name)
        return True, None
    except ImportError:
        return False, f"Missing: {package_name} (install with: pip install {package_name})"

def check_system_command(command):
    """Check if a system command is available"""
    if shutil.which(command):
        try:
            result = subprocess.run([command, '-version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            version_line = result.stdout.split('\n')[0] if result.stdout else 'Unknown'
            return True, version_line
        except:
            return True, "Installed (version check failed)"
    return False, f"Not found: {command}"

def main():
    print("=" * 60)
    print("Checking Requirements for YouTube Blog Generator")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Check Python packages
    print("Python Packages:")
    print("-" * 60)
    
    packages = [
        ("Django", "django"),
        ("yt-dlp", "yt_dlp"),
        ("openai-whisper", "whisper"),
        ("requests", "requests"),
        ("openai", "openai"),
        ("google-genai", "google.genai"),
        ("ffmpeg-python", "ffmpeg"),
    ]
    
    for package_name, import_name in packages:
        installed, message = check_python_package(package_name, import_name)
        if installed:
            print(f"  ✓ {package_name}")
        else:
            print(f"  ✗ {message}")
            all_ok = False
    
    print()
    
    # Check system commands
    print("System Commands:")
    print("-" * 60)
    
    # Check FFmpeg
    ffmpeg_ok, ffmpeg_msg = check_system_command('ffmpeg')
    if ffmpeg_ok:
        print(f"  ✓ FFmpeg: {ffmpeg_msg}")
    else:
        print(f"  ⚠ FFmpeg: {ffmpeg_msg}")
        print("     Note: App will work without FFmpeg, but WAV conversion requires it")
        print("     Install: choco install ffmpeg OR see INSTALL_FFMPEG.md")
    
    # Check FFprobe (part of FFmpeg)
    ffprobe_ok, ffprobe_msg = check_system_command('ffprobe')
    if ffprobe_ok:
        print(f"  ✓ FFprobe: {ffprobe_msg}")
    elif not ffmpeg_ok:
        print(f"  ⚠ FFprobe: Not found (comes with FFmpeg)")
    
    print()
    
    # Check API keys
    print("API Keys:")
    print("-" * 60)
    
    import os
    
    # Groq
    groq_file = r"C:\temp\AI\secret keys\groq_api_key.txt"
    if os.path.exists(groq_file):
        key = open(groq_file, 'r').read().strip()
        if key:
            print(f"  ✓ Groq API key: Found in file")
        else:
            print(f"  ✗ Groq API key: File exists but is empty")
            all_ok = False
    else:
        if os.environ.get('GROQ_API_KEY'):
            print(f"  ✓ Groq API key: Found in environment")
        else:
            print(f"  ⚠ Groq API key: Not found (optional for blog generation)")
    
    # AssemblyAI
    assemblyai_file = r"C:\temp\AI\secret keys\assemblyAI_key.txt"
    if os.path.exists(assemblyai_file):
        key = open(assemblyai_file, 'r').read().strip()
        if key:
            print(f"  ✓ AssemblyAI API key: Found in file")
        else:
            print(f"  ✗ AssemblyAI API key: File exists but is empty")
    else:
        if os.environ.get('ASSEMBLYAI_API_KEY'):
            print(f"  ✓ AssemblyAI API key: Found in environment")
        else:
            print(f"  ⚠ AssemblyAI API key: Not found (optional for transcription)")
    
    print()
    print("=" * 60)
    
    if all_ok:
        print("✓ All required packages are installed!")
        print()
        print("Optional:")
        print("  - FFmpeg: For audio conversion (app works without it)")
        print("  - API keys: For transcription and blog generation")
    else:
        print("✗ Some requirements are missing")
        print()
        print("Install missing packages with:")
        print("  pip install -r requirements.txt")
    
    print("=" * 60)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
