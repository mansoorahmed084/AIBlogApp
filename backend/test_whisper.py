#!/usr/bin/env python
"""
Test Whisper installation
Run with: python test_whisper.py
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("Whisper Installation Test")
print("=" * 60)
print()

# Test 1: Check if whisper can be imported
print("Test 1: Checking Whisper import...")
try:
    import whisper
    print("  [OK] Whisper imported successfully")
    print(f"  Module location: {whisper.__file__}")
    
    # Check if load_model exists
    if hasattr(whisper, 'load_model'):
        print("  [OK] load_model function available")
    else:
        print("  [ERROR] load_model function NOT found")
        
except ImportError as e:
    print(f"  [ERROR] Whisper import failed: {e}")
    print()
    print("Install Whisper with:")
    print("  pip install openai-whisper")
    sys.exit(1)
except Exception as e:
    print(f"  [ERROR] Error importing Whisper: {e}")
    sys.exit(1)

print()

# Test 2: Try loading a model (this downloads if not present)
print("Test 2: Testing model loading...")
print("  (This will download the 'tiny' model if not present - ~75MB)")
print()

try:
    model = whisper.load_model("tiny")
    print("  [OK] Model loaded successfully")
    print(f"  Model type: {type(model)}")
except Exception as e:
    print(f"  [ERROR] Model loading failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 60)
print("[SUCCESS] Whisper is properly installed and working!")
print("=" * 60)
print()
print("Available models:")
print("  - tiny: ~75MB, fastest, lowest accuracy")
print("  - base: ~150MB, good balance (recommended)")
print("  - small: ~500MB, better accuracy")
print("  - medium: ~1.5GB, high accuracy")
print("  - large: ~3GB, highest accuracy")
print()
