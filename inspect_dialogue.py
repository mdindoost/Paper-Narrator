#!/usr/bin/env python3
"""
Fixed Dialogue Inspector - Updated imports for FIXED classes
Save as: inspect_dialogue.py (REPLACE existing file)
"""

import sys
import os
from pathlib import Path
import json

# Add src directory to path
sys.path.append('src')
sys.path.append('.')

try:
    from src.integrated_enhanced_pipeline import IntegratedCompletelyFixedPipeline  # FIXED import
    from src.audio_generator_fixed_enhanced import FullyFixedAudioGenerator   # FIXED import
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you've saved the FIXED files to the src/ directory")
    sys.exit(1)


def inspect_dialogue_generation(pdf_path: str):
    """Generate dialogue and show exactly what text is sent to TTS"""
    
    print("🔍 DIALOGUE INSPECTOR - FIXED VERSION")
    print("Shows exact text being sent to TTS engine with ALL bug fixes")
    print("=" * 80)
    
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    try:
        pipeline = IntegratedCompletelyFixedPipeline()  # FIXED class name
        
        if not pipeline.check_prerequisites():
            print("❌ Prerequisites not met")
            return False
        
        print("🚀 Generating FULLY FIXED dialogue for inspection...")
        
        # Generate dialogue WITHOUT audio (just text)
        paper_data = pipeline.pdf_processor.process_paper(pdf_path)
        raw_text = paper_data["raw_text"]
        
        core_sections = pipeline.enhanced_analyzer.enhanced_section_detection(raw_text)
        stage1 = pipeline.enhanced_analyzer.stage1_simple_understanding(core_sections)
        stage2 = pipeline.enhanced_analyzer.stage2_enhanced_claims_challenges(stage1, raw_text)
        
        # Apply additional fixes to remove ** symbols and other issues
        try:
            from stage2_additional_fixes_patch import patch_stage2_results, apply_quick_field_fix
            stage1 = apply_quick_field_fix(stage1)
            stage2 = patch_stage2_results(stage2)
            print("✅ Additional fixes applied to Stage 1 & 2 results")
        except ImportError:
            print("⚠️ Additional fixes not available - some ** symbols may remain")
        
        conversation_script = pipeline.completely_fixed_dialogue_generator.create_completely_fixed_conversation_script(  # FIXED method name
            stage1, stage2, max_exchanges=4
        )
        
        # Display full dialogue structure
        print(f"\n📊 FULLY FIXED DIALOGUE STRUCTURE:")
        print(f"   📝 Title: {conversation_script.title}")
        print(f"   👥 Total Turns: {conversation_script.total_turns}")
        print(f"   ⏱️ Duration Estimate: {conversation_script.duration_estimate}")
        print(f"   🎯 Research Field: {conversation_script.research_field}")  # Should be FIXED
        
        # Show introduction
        print(f"\n🎬 INTRODUCTION TEXT (FIXED):")
        print("="*60)
        print(conversation_script.introduction)
        print("="*60)
        
        # Show each dialogue turn
        print(f"\n💬 DIALOGUE TURNS (ALL FIXES APPLIED):")
        
        for i, turn in enumerate(conversation_script.turns, 1):
            print(f"\n" + "─"*60)
            print(f"TURN {i}: {turn.speaker}")  # Should show FIXED names
            print(f"Role: {turn.speaker_role}")
            print(f"Topic: {turn.topic}")
            print(f"Source: {turn.source_type}")
            print("─"*60)
            print("ORIGINAL TEXT:")
            print(turn.content)
            print("─"*30)
            
            # Show what text cleanup does with FIXED version
            audio_gen = FullyFixedAudioGenerator()  # FIXED class name
            
            # Show both test mode and TTS mode
            cleaned_text_test = audio_gen.comprehensive_text_cleanup(turn.content, for_test=True)
            cleaned_text_tts = audio_gen.comprehensive_text_cleanup(turn.content, for_test=False)
            
            print("CLEANED TEXT (Test Mode - no periods):")
            print(cleaned_text_test)
            print("CLEANED TEXT (TTS Mode - with periods):")
            print(cleaned_text_tts)
            
            # Show voice assignment
            voice_profile = audio_gen.get_speaker_voice_profile(turn.speaker)
            print(f"VOICE ASSIGNED: {voice_profile.voice_id} ({voice_profile.description})")
            
            print("─"*60)
        
        # Show conclusion
        print(f"\n🎯 CONCLUSION TEXT (FIXED):")
        print("="*60)
        print(conversation_script.conclusion)
        print("="*60)
        
        # Save full dialogue to file for easy review
        output_file = "dialogue_inspection_report_FIXED.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("DIALOGUE INSPECTION REPORT - FULLY FIXED VERSION\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Paper: {pdf_file.name}\n")
            f.write(f"Field: {stage1.research_field}\n")  # Should be FIXED
            f.write(f"Topic: {stage1.paper_topic}\n")
            f.write(f"Key Finding: {stage1.key_finding}\n\n")
            
            f.write("INTRODUCTION (FIXED):\n")
            f.write("-"*40 + "\n")
            f.write(conversation_script.introduction + "\n\n")
            
            f.write("DIALOGUE TURNS (ALL FIXES APPLIED):\n")
            f.write("-"*40 + "\n")
            
            for i, turn in enumerate(conversation_script.turns, 1):
                f.write(f"\nTURN {i}: {turn.speaker}\n")  # FIXED names
                f.write(f"Topic: {turn.topic}\n")
                f.write("Original Text:\n")
                f.write(turn.content + "\n")
                
                audio_gen = FullyFixedAudioGenerator()
                cleaned_tts = audio_gen.comprehensive_text_cleanup(turn.content, for_test=False)
                f.write("Cleaned Text (TTS):\n")
                f.write(cleaned_tts + "\n")
                
                voice = audio_gen.get_speaker_voice_profile(turn.speaker)
                f.write(f"Voice: {voice.voice_id}\n")
                f.write("-"*40 + "\n")
            
            f.write(f"\nCONCLUSION (FIXED):\n")
            f.write("-"*40 + "\n")
            f.write(conversation_script.conclusion + "\n")
        
        print(f"\n✅ FULLY FIXED DIALOGUE INSPECTION COMPLETE!")
        print(f"📄 Full report saved to: {output_file}")
        print(f"\nShould show all 6 bug fixes:")
        print(f"   ✅ Bug 1&2: No ** symbols in field/intro")
        print(f"   ✅ Bug 3: Natural language summaries") 
        print(f"   ✅ Bug 4: Prof. Marcus W. (not Webb)")
        print(f"   ✅ Bug 5: No artificial prefixes")
        print(f"   ✅ Bug 6: Three distinct voices assigned")
        
        return True
        
    except Exception as e:
        print(f"❌ FULLY FIXED dialogue inspection failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def quick_text_cleanup_test():
    """Quick test of FIXED text cleanup function"""
    
    print("\n🧹 QUICK TEXT CLEANUP TEST - FIXED VERSION")
    print("="*50)
    
    audio_gen = FullyFixedAudioGenerator()  # FIXED class name
    
    # Test specific problematic texts with FIXED expectations
    test_cases = [
        ("This is a *claim* with astercs and evidence for claim shows good results.", "natural speech"),
        ("As a computer science expert, I believe the **methodology** is sound.", "no expertise mentions"),
        ("The [supporting evidence] demonstrates that potential challenges exist.", "no brackets"),
        ("Lack of context: Evidence for claim 1 indicates significant results.", "no artificial prefixes"),
        ("Prof. Marcus Webb believes the approach is flawed.", "Prof. Marcus W.")
    ]
    
    for i, (test_text, expected_fix) in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Original:  {test_text}")
        
        # Test both modes
        cleaned_test = audio_gen.comprehensive_text_cleanup(test_text, for_test=True)
        cleaned_tts = audio_gen.comprehensive_text_cleanup(test_text, for_test=False)
        
        print(f"Test Mode: {cleaned_test}")
        print(f"TTS Mode:  {cleaned_tts}")
        print(f"Fix Type:  {expected_fix}")


def quick_voice_test():
    """Quick test of FIXED voice assignments"""
    
    print("\n🎤 QUICK VOICE ASSIGNMENT TEST - FIXED VERSION")
    print("="*50)
    
    audio_gen = FullyFixedAudioGenerator()  # FIXED class name
    
    test_speakers = [
        "Narrator",
        "Dr. Ava D.",
        "Prof. Marcus W.",  # Should be FIXED name 
        "Sarah Chen",
        "Marcus Webb"
    ]
    
    voice_map = {}
    for speaker in test_speakers:
        profile = audio_gen.get_speaker_voice_profile(speaker)
        voice_map[speaker] = profile.voice_id
        print(f"{speaker:20} → {profile.voice_id}")
    
    # Check for issues
    narrator_voice = voice_map.get("Narrator")
    marcus_voice = voice_map.get("Prof. Marcus W.")
    ava_voice = voice_map.get("Dr. Ava D.")
    
    print(f"\nFIXED Voice Analysis:")
    if narrator_voice == marcus_voice:
        print(f"❌ PROBLEM: Narrator and Marcus have same voice ({narrator_voice})")
    else:
        print(f"✅ Narrator and Marcus have different voices")
    
    unique_voices = len(set(voice_map.values()))
    print(f"✅ Total unique voices: {unique_voices}/3 expected")


def main():
    """Main inspection function"""
    
    print("🔍 DIALOGUE INSPECTION TOOL - FULLY FIXED VERSION")
    print("See exactly what FIXED text is sent to TTS engine")
    print("-" * 60)
    
    # Quick tests first
    quick_text_cleanup_test()
    quick_voice_test()
    
    # Full dialogue inspection
    default_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = default_path
    
    print(f"\n📄 Inspecting FULLY FIXED dialogue for: {pdf_path}")
    
    success = inspect_dialogue_generation(pdf_path)
    
    if success:
        print(f"\n📋 NEXT STEPS:")
        print(f"   1. Open 'dialogue_inspection_report_FIXED.txt'")
        print(f"   2. Verify all 6 bug fixes are working")
        print(f"   3. Check that speaker names, field classification, etc. are FIXED")
        print(f"\nIf everything looks good, proceed to full audio generation!")
    else:
        print(f"\n❌ FIXED inspection failed - check error messages above")


if __name__ == "__main__":
    main()