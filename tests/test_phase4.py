#!/usr/bin/env python3
"""Test Phase 4 Video Generation Independently"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from phase4_video_generator import YouTubeVideoGenerator


def test_phase4_standalone():
    """Test Phase 4 video generation using any available Phase 3 outputs"""
    
    print("🎬 Testing Phase 4 Video Generation")
    print("=" * 60)
    
    # Initialize generator
    generator = YouTubeVideoGenerator()
    
    # Check requirements
    if not generator.check_requirements():
        print("❌ Missing requirements:")
        print("   Install with: pip install moviepy")
        return False
    
    print("✅ moviepy available")
    
    # Find any available Phase 3 outputs
    audio_dir = Path("data/output/audio")
    audio_files = list(audio_dir.glob("*_RELIABLE_youtube.wav"))
    
    if not audio_files:
        print(f"❌ No audio files found in {audio_dir}")
        print("   Run Phase 3 first with: python3 run_phase3_reliable.py path/to/paper.pdf")
        return False
    
    # Use the most recent audio file
    audio_file = max(audio_files, key=lambda f: f.stat().st_mtime)
    base_filename = audio_file.name.replace("_RELIABLE_youtube.wav", "")
    metadata_file = audio_dir / f"{base_filename}_reliable_metadata.json"
    
    if not metadata_file.exists():
        print(f"❌ Metadata file not found: {metadata_file}")
        print("   Re-run Phase 3 to generate complete outputs")
        return False
    
    print(f"✅ Audio file found: {audio_file}")
    print(f"✅ Metadata file found: {metadata_file}")
    print(f"📋 Using paper: {base_filename}")
    
    # Extract paper title from base filename or use generic
    paper_title = base_filename.replace("_", " ").replace("-", " ").title()
    if "WCC" in paper_title and "CM" in paper_title:
        paper_title = "Optimizing Community Detection Methods for Large-Scale Networks"
    
    print(f"\\n🎯 Generating video for: {paper_title}")
    print(f"📁 Audio source: {audio_file}")
    print(f"📋 Metadata source: {metadata_file}")
    
    try:
        # Generate video
        result = generator.generate_complete_video(
            str(audio_file),
            str(metadata_file),
            paper_title,
            base_filename
        )
        
        # Display results
        print(f"\\n🎉 Video generation successful!")
        print(f"📹 Output file: {result['video_file']}")
        print(f"⏱️ Video duration: {result['video_duration']:.1f}s ({result['video_duration']/60:.1f} min)")
        print(f"🔊 Audio duration: {result['audio_duration']:.1f}s ({result['audio_duration']/60:.1f} min)")
        print(f"📏 Resolution: {result['resolution']}")
        print(f"🎬 FPS: {result['fps']}")
        print(f"💾 File size: {result['file_size_mb']:.1f} MB")
        print(f"🎭 Video segments: {result['num_segments']}")
        
        # Segment breakdown
        print(f"\\n📊 Segment breakdown:")
        for i, segment in enumerate(result['segments'][:5], 1):
            print(f"   {i}. {segment['speaker']} ({segment['type']}): {segment['duration']:.1f}s")
        
        if len(result['segments']) > 5:
            print(f"   ... and {len(result['segments']) - 5} more segments")
        
        # File verification
        video_path = Path(result['video_file'])
        if video_path.exists():
            print(f"\\n✅ Video file created successfully")
            print(f"📁 Location: {video_path}")
            print(f"💾 Size: {video_path.stat().st_size / (1024*1024):.1f} MB")
            
            print(f"\\n🎥 To play the video:")
            print(f"   - VLC: vlc '{video_path}'")
            print(f"   - System player: open '{video_path}' (Mac) or xdg-open '{video_path}' (Linux)")
            
            print(f"\\n🚀 Ready for YouTube upload!")
        else:
            print(f"❌ Video file not found: {video_path}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Video generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    
    success = test_phase4_standalone()
    
    if success:
        print(f"\\n🎉 Phase 4 test completed successfully!")
        print(f"🎬 YouTube-ready video generated")
        print(f"🚀 Ready for integration into full pipeline")
    else:
        print(f"\\n❌ Phase 4 test failed")
        print(f"🔧 Check dependencies and Phase 3 outputs")
        sys.exit(1)


if __name__ == "__main__":
    main()
