#!/usr/bin/env python3
"""Test Phase 3 audio generation"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_audio_system():
    print("🧪 Testing Phase 3 Audio Generation...")
    
    try:
        from audio_generator import YouTubeAudioGenerator
        
        generator = YouTubeAudioGenerator()
        generator.install_requirements()
        
        print(f"✅ Audio generator initialized")
        print(f"   Available engines: {', '.join(generator.available_engines)}")
        print(f"   Selected engine: {generator.selected_engine}")
        
        # Test YouTube intro generation
        intro = generator.generate_youtube_intro("Optimized Parallel Implementations of WCC Algorithms")
        print(f"✅ YouTube intro generated:")
        print(f"   {intro[:100]}...")
        
        # Test audio generation (short test)
        test_text = "Hello! I'm Dr. Ava D., and I'm excited to discuss this groundbreaking research!"
        segment = generator.generate_audio_segment(test_text, "Dr. Ava D.", "test")
        
        print(f"✅ Test audio generated:")
        print(f"   File: {segment.audio_file}")
        print(f"   Duration: {segment.duration:.1f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Audio generation test failed: {e}")
        return False

if __name__ == "__main__":
    if test_audio_system():
        print("\n🎉 Phase 3 system ready!")
        print("\nUsage:")
        print("   python3 run_phase3.py your_paper.pdf")
        print("   python3 run_phase3.py your_paper.pdf 3 3  # 3 topics, 3 exchanges each")
    else:
        print("\n❌ Phase 3 system has issues")
