#!/usr/bin/env python
"""
Find FFmpeg installation on Windows
Run with: python find_ffmpeg.py
"""
import os
import shutil
import subprocess

def find_ffmpeg():
    """Find FFmpeg installation"""
    print("=" * 60)
    print("FFmpeg Detection Tool")
    print("=" * 60)
    print()
    
    # Method 1: Check PATH
    print("Method 1: Checking PATH...")
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        print(f"  ✓ Found in PATH: {ffmpeg_path}")
        try:
            result = subprocess.run([ffmpeg_path, '-version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            version_line = result.stdout.split('\n')[0] if result.stdout else 'Unknown'
            print(f"  Version: {version_line}")
            return ffmpeg_path
        except Exception as e:
            print(f"  ⚠ Found but error checking version: {e}")
            return ffmpeg_path
    else:
        print("  ✗ Not found in PATH")
    
    print()
    
    # Method 2: Check common installation locations
    print("Method 2: Checking common installation locations...")
    common_paths = [
        r'C:\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe',
        os.path.expanduser(r'~\ffmpeg\bin\ffmpeg.exe'),
        r'C:\tools\ffmpeg\bin\ffmpeg.exe',
        r'C:\ProgramData\chocolatey\bin\ffmpeg.exe',
        r'C:\Program Files\ImageMagick-*\ffmpeg.exe',  # Sometimes bundled
    ]
    
    found_paths = []
    for path in common_paths:
        # Handle wildcards
        if '*' in path:
            import glob
            matches = glob.glob(path)
            for match in matches:
                if os.path.exists(match):
                    found_paths.append(match)
        elif os.path.exists(path):
            found_paths.append(path)
    
    if found_paths:
        print(f"  ✓ Found {len(found_paths)} installation(s):")
        for path in found_paths:
            print(f"    - {path}")
            try:
                result = subprocess.run([path, '-version'], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=5)
                version_line = result.stdout.split('\n')[0] if result.stdout else 'Unknown'
                print(f"      Version: {version_line}")
            except:
                pass
        return found_paths[0]
    else:
        print("  ✗ Not found in common locations")
    
    print()
    
    # Method 3: Search entire C: drive (slow, but thorough)
    print("Method 3: Searching for ffmpeg.exe...")
    print("  (This may take a while - press Ctrl+C to skip)")
    
    search_paths = [
        r'C:\Program Files',
        r'C:\Program Files (x86)',
        r'C:\tools',
        os.path.expanduser(r'~'),
    ]
    
    for search_path in search_paths:
        if not os.path.exists(search_path):
            continue
        
        print(f"  Searching: {search_path}...")
        try:
            for root, dirs, files in os.walk(search_path):
                # Skip system directories to speed up
                dirs[:] = [d for d in dirs if d not in ['Windows', '$Recycle.Bin', 'System Volume Information']]
                
                if 'ffmpeg.exe' in files:
                    found = os.path.join(root, 'ffmpeg.exe')
                    print(f"  ✓ Found: {found}")
                    return found
        except KeyboardInterrupt:
            print("  Search cancelled by user")
            break
        except Exception as e:
            print(f"  Error searching {search_path}: {e}")
    
    print()
    print("=" * 60)
    print("FFmpeg NOT FOUND")
    print("=" * 60)
    print()
    print("Installation options:")
    print("  1. Chocolatey: choco install ffmpeg")
    print("  2. Winget: winget install ffmpeg")
    print("  3. Manual: Download from https://ffmpeg.org/download.html")
    print("  4. See INSTALL_FFMPEG.md for detailed instructions")
    print()
    print("After installation:")
    print("  - Add FFmpeg to PATH, OR")
    print("  - Restart your terminal/PowerShell")
    print()
    
    return None

if __name__ == "__main__":
    result = find_ffmpeg()
    
    if result:
        print()
        print("=" * 60)
        print("RECOMMENDATION")
        print("=" * 60)
        print(f"FFmpeg found at: {result}")
        print()
        print("To make it available system-wide:")
        print("  1. Add to PATH:")
        bin_dir = os.path.dirname(result)
        print(f"     Add this directory to PATH: {bin_dir}")
        print()
        print("  2. Or restart your terminal after installation")
        print()
    else:
        print("\nNote: The app will work without FFmpeg,")
        print("      but audio conversion to WAV requires FFmpeg.")
