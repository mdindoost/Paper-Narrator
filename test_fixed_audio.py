#!/usr/bin/env python3
"""Test the fixed audio generator"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_fixed_system():
    print("🧪 Testing Fixed Audio System...")
    
    try:
        from audio_generator_fixed import FixedAudioGenerator
        
        generator = FixedAudioGenerator()
        
        if not generator.check_requirements():
            print("❌ Edge-TTS not available")
            return False
        
        print("✅ Fixed audio generator loaded")
        
        # Test name cleaning
        test_text = "Hello Dr. Chen! I'm excited to discuss this with Sarah."
        cleaned = generator.clean_dialogue_text(test_text)
        
        print(f"✅ Name cleaning test:")
        print(f"   Before: {test_text}")
        print(f"   After:  {cleaned}")
        
        if "Dr. Ava D." in cleaned and "Sarah" not in cleaned:
            print("✅ Name cleaning working correctly")
            return True
        else:
            print("❌ Name cleaning not working")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if test_fixed_system():
        print("\n🎉 Fixed audio system ready!")
        print("\nRun with:")
        print("   python3 run_phase3_fixed.py your_paper.pdf 5 3")
    else:
        print("\n❌ Fixed system has issues")
