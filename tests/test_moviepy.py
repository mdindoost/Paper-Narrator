#!/usr/bin/env python3
"""Test MoviePy installation and imports"""

print("🔍 Testing MoviePy installation...")

# Test 1: Basic import
try:
    import moviepy
    print(f"✅ MoviePy imported: version {moviepy.__version__}")
except ImportError as e:
    print(f"❌ Cannot import moviepy: {e}")
    exit(1)

# Test 2: Editor module
try:
    from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, ColorClip, CompositeVideoClip
    print("✅ MoviePy editor modules imported successfully")
except ImportError as e:
    print(f"❌ Cannot import moviepy.editor: {e}")
    print("🔧 This suggests a broken MoviePy installation")
    
    # Try alternative import
    try:
        import moviepy.editor as mp
        print("✅ Alternative import worked")
    except ImportError:
        print("❌ Alternative import also failed")
        print("\n🛠️  SOLUTION:")
        print("   pip uninstall moviepy")
        print("   pip install moviepy==1.0.3")
        exit(1)

# Test 3: Create a simple clip
try:
    test_clip = ColorClip(size=(100, 100), color=(255, 0, 0)).set_duration(1)
    print("✅ Can create basic video clips")
    test_clip.close()
except Exception as e:
    print(f"❌ Cannot create video clips: {e}")

# Test 4: Check ffmpeg
try:
    import moviepy.config as config
    print(f"✅ FFmpeg path: {getattr(config, 'FFMPEG_BINARY', 'default')}")
except Exception as e:
    print(f"⚠️  FFmpeg check failed: {e}")

print("\n🎬 MoviePy test complete!")
print("If all tests passed, Phase 4 should work.")
