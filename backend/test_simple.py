#!/usr/bin/env python
"""
Simple Python test script for YouTube Blog Generator
Run with: python test_simple.py
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_youtube_download():
    """Test YouTube video download"""
    print("=" * 60)
    print("YouTube Blog Generator - Simple Test")
    print("=" * 60)
    print()
    
    test_url = "https://www.youtube.com/watch?v=skMzCAga-dg"
    print(f"Test URL: {test_url}")
    print()
    
    # Check yt-dlp
    try:
        import yt_dlp
        print(f"✓ yt-dlp installed (version: {yt_dlp.version.__version__})")
    except ImportError:
        print("✗ yt-dlp NOT installed")
        print("  Install with: pip install yt-dlp")
        return False
    
    # Test video info extraction
    try:
        print("\nTesting video info extraction...")
        ydl_opts = {'quiet': False}
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(test_url, download=False)
            
        print("\n" + "=" * 60)
        print("SUCCESS! Video info extracted:")
        print("=" * 60)
        print(f"Title: {info.get('title', 'N/A')}")
        print(f"Channel: {info.get('uploader', 'N/A')}")
        print(f"Duration: {info.get('duration', 0)} seconds")
        print("=" * 60)
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("ERROR:", str(e))
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False

def test_full_pipeline():
    """Test full pipeline"""
    print("\n" + "=" * 60)
    print("Testing Full Pipeline (Download + Transcribe + Generate)")
    print("=" * 60)
    print("This will take several minutes...")
    print()
    
    try:
        from config.blog_generator import YouTubeBlogGenerator
        
        test_url = "https://www.youtube.com/watch?v=skMzCAga-dg"
        generator = YouTubeBlogGenerator()
        
        result = generator.process_youtube_video(test_url)
        
        if result['success']:
            print("\n" + "=" * 60)
            print("SUCCESS! Blog post generated")
            print("=" * 60)
            print(f"Title: {result['blog_post']['title']}")
            print(f"Description: {result['blog_post']['description'][:100]}...")
            print(f"Content length: {len(result['blog_post']['content'])} characters")
            print("=" * 60)
            return True
        else:
            print("\n" + "=" * 60)
            print("ERROR: Blog generation failed")
            print("=" * 60)
            print(f"Error: {result.get('error', 'Unknown error')}")
            print("=" * 60)
            return False
            
    except Exception as e:
        print("\n" + "=" * 60)
        print("EXCEPTION:", str(e))
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Run simple test
    if test_youtube_download():
        print("\n✓ Basic test passed!")
        
        # Ask if user wants to run full pipeline test
        print("\nRun full pipeline test? (y/n): ", end="")
        try:
            response = input().strip().lower()
            if response == 'y':
                test_full_pipeline()
        except KeyboardInterrupt:
            print("\n\nTest cancelled by user")
    else:
        print("\n✗ Basic test failed - fix issues before running full pipeline")
