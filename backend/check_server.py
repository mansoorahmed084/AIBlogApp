#!/usr/bin/env python
"""
Quick script to check if Django server is running and test the endpoint
"""
import requests
import sys

def check_server():
    base_url = "http://127.0.0.1:8000"
    
    print("=" * 60)
    print("Django Server Check")
    print("=" * 60)
    print()
    
    # Check if server is running
    try:
        print(f"Checking if server is running at {base_url}...")
        response = requests.get(base_url, timeout=5)
        print(f"✓ Server is running (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("✗ Server is NOT running!")
        print()
        print("Start the server with:")
        print("  cd C:\\temp\\AI\\AI_blog_app\\backend")
        print("  python manage.py runserver")
        return False
    except Exception as e:
        print(f"✗ Error checking server: {e}")
        return False
    
    print()
    
    # Check generate-blog endpoint
    try:
        print(f"Checking generate-blog endpoint...")
        # This will fail without auth, but we can check if endpoint exists
        response = requests.post(
            f"{base_url}/generate-blog/",
            data={'youtube_url': 'test'},
            timeout=5
        )
        print(f"✓ Endpoint exists (Status: {response.status_code})")
        if response.status_code == 403:
            print("  (403 is expected - need to be logged in)")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to endpoint")
        return False
    except Exception as e:
        print(f"  Note: {e}")
    
    print()
    print("=" * 60)
    print("Server check complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Make sure Django server is running")
    print("  2. Open browser console (F12) and check for errors")
    print("  3. Try generating a blog and check the Network tab")
    
    return True

if __name__ == "__main__":
    try:
        check_server()
    except KeyboardInterrupt:
        print("\n\nCheck cancelled")
        sys.exit(1)
