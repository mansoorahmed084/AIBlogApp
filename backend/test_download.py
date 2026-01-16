#!/usr/bin/env python
"""
Test YouTube audio download functionality
Run with: python test_download.py
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 60)
    print("YouTube Audio Download Test")
    print("=" * 60)
    print()
    
    test_url = "https://www.youtube.com/watch?v=skMzCAga-dg"
    print(f"Test URL: {test_url}")
    print()
    
    try:
        from config.blog_generator import YouTubeBlogGenerator
        
        print("Initializing YouTubeBlogGenerator...")
        generator = YouTubeBlogGenerator()
        
        print(f"Testing download of: {test_url}")
        print()
        
        # Test download
        audio_file = generator.download_audio(test_url)
        
        if audio_file and os.path.exists(audio_file):
            file_size = os.path.getsize(audio_file) / (1024 * 1024)  # Size in MB
            print()
            print("=" * 60)
            print("SUCCESS! Audio downloaded")
            print("=" * 60)
            print(f"File: {audio_file}")
            print(f"Size: {file_size:.2f} MB")
            print("=" * 60)
            
            # Clean up
            try:
                os.unlink(audio_file)
                print("\nTemporary file cleaned up")
            except:
                pass
            
            return True
        else:
            print()
            print("=" * 60)
            print("ERROR: Audio download failed")
            print("=" * 60)
            print("Could not download or find audio file")
            print("=" * 60)
            return False
            
    except Exception as e:
        import traceback
        print()
        print("=" * 60)
        print("EXCEPTION occurred")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✓ Download test PASSED!")
        print("\nNext steps:")
        print("  1. Run: python test_simple.py (full pipeline test)")
        print("  2. Or test in the web app")
    else:
        print("\n✗ Download test FAILED")
        print("\nTroubleshooting:")
        print("  1. Check if FFmpeg is installed: ffmpeg -version")
        print("  2. Check internet connection")
        print("  3. Try a different YouTube URL")
        print("  4. Update yt-dlp: pip install --upgrade yt-dlp")
    
    sys.exit(0 if success else 1)
