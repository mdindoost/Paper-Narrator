# test_images.py
#!/usr/bin/env python3
"""Test image loading independently"""

from pathlib import Path
from moviepy.editor import ImageClip, VideoFileClip

def test_image_loading():
    print("Testing image loading...")
    
    # Test each image individually
    images = {
        "HOST": "data/materials/HOST.JPG",
        "AVA": "data/materials/AVA.JPG", 
        "MARCUS": "data/materials/MARCUS.JPG"
    }
    
    for name, path in images.items():
        print(f"\n🖼️  Testing {name}: {path}")
        
        if not Path(path).exists():
            print(f"   ❌ File does not exist")
            continue
            
        try:
            # Try to load image
            clip = ImageClip(path, duration=2)
            print(f"   ✅ Loaded: {clip.size} pixels")
            
            # Test if we can create a simple video
            output_test = f"test_{name.lower()}.mp4"
            clip.write_videofile(output_test, fps=1, verbose=False, logger=None)
            print(f"   ✅ Video created: {output_test}")
            
            clip.close()
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test logo
    print(f"\n🎬 Testing LOGO: data/materials/LOGO.MOV")
    if Path("data/materials/LOGO.MOV").exists():
        try:
            logo = VideoFileClip("data/materials/LOGO.MOV")
            print(f"   ✅ Logo loaded: {logo.duration}s, {logo.size}")
            logo.close()
        except Exception as e:
            print(f"   ❌ Logo error: {e}")
    else:
        print(f"   ❌ Logo file not found")

if __name__ == "__main__":
    test_image_loading()
