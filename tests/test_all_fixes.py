#!/usr/bin/env python3
"""
Test All Audio and Integration Fixes
Save as: test_all_fixes.py (in root directory)

Tests:
1. Text cleanup - removes symbols, fixes broken sentences
2. Voice differentiation - different voices for each speaker  
3. Enhanced introduction - uses new Claims→Challenges intro
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append('src')
sys.path.append('.')

try:
    from audio_generator_fixed_enhanced import FixedEnhancedAudioGenerator
    from integrated_enhanced_pipeline import IntegratedEnhancedPipeline
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have:")
    print("  - audio_generator_fixed_enhanced.py in src/")
    print("  - integrated_enhanced_pipeline.py in src/")
    sys.exit(1)


def test_text_cleanup():
    """Test the enhanced text cleanup functionality"""
    
    print("🧹 TESTING TEXT CLEANUP")
    print("=" * 50)
    
    generator = FixedEnhancedAudioGenerator()
    
    # Test problematic texts
    test_texts = [
        "This is a *claim* with astercs and evidence for claim that shows...",
        "As a computer science expert, I think this **methodology** is interesting...",
        "The results show [supporting evidence] but there are potential challenges...",
        "This sentence is broken.. and has multiple...periods and    spaces.",
        "Evidence for claim 1 shows that the algorithm achieves* performance.",
        "From a machine learning perspective, the data demonstrates good results."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTest {i}:")
        print(f"   Original: {text}")
        
        cleaned = generator.enhanced_text_cleanup(text)
        print(f"   Cleaned:  {cleaned}")
        
        # Check if common issues were fixed
        issues_fixed = []
        if "*" not in cleaned:
            issues_fixed.append("asterisks removed")
        if "astercs" not in cleaned:
            issues_fixed.append("'astercs' fixed") 
        if "evidence for claim" not in cleaned:
            issues_fixed.append("'evidence for claim' replaced")
        if not any(phrase in cleaned.lower() for phrase in ["as a", "expert", "perspective"]):
            issues_fixed.append("explicit expertise removed")
        
        print(f"   Issues Fixed: {', '.join(issues_fixed) if issues_fixed else 'none detected'}")
    
    print(f"\n✅ Text cleanup test complete!")


def test_voice_differentiation():
    """Test that different speakers get different voices"""
    
    print("\n🎤 TESTING VOICE DIFFERENTIATION")
    print("=" * 50)
    
    generator = FixedEnhancedAudioGenerator()
    
    test_speakers = [
        "Narrator",
        "Dr. Ava D.", 
        "Prof. Marcus Webb",
        "Sarah Chen",  # Alternative name for Dr. Ava
        "Marcus Webb"   # Alternative name for Prof. Marcus
    ]
    
    voice_assignments = {}
    
    for speaker in test_speakers:
        profile = generator.get_speaker_voice_profile(speaker)
        voice_assignments[speaker] = profile.voice_id
        print(f"   {speaker:20} → {profile.voice_id:20} ({profile.description})")
    
    # Check for differentiation
    unique_voices = set(voice_assignments.values())
    print(f"\n📊 Voice Analysis:")
    print(f"   Total speakers tested: {len(test_speakers)}")
    print(f"   Unique voices assigned: {len(unique_voices)}")
    
    if len(unique_voices) >= 3:
        print(f"   ✅ Good voice differentiation!")
    else:
        print(f"   ⚠️ Limited voice differentiation")
    
    # Check specific issue: Marcus and Narrator should be different
    marcus_voice = voice_assignments.get("Prof. Marcus Webb")
    narrator_voice = voice_assignments.get("Narrator")
    
    if marcus_voice != narrator_voice:
        print(f"   ✅ Marcus and Narrator have different voices!")
    else:
        print(f"   ❌ Marcus and Narrator have same voice - needs fix")


def test_enhanced_introduction():
    """Test that enhanced introduction is used instead of generic one"""
    
    print("\n🎬 TESTING ENHANCED INTRODUCTION INTEGRATION")
    print("=" * 50)
    
    # Test with minimal pipeline
    pdf_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ Test PDF not found: {pdf_path}")
        print("   Please provide path to test PDF")
        return False
    
    try:
        pipeline = IntegratedEnhancedPipeline()
        
        if not pipeline.check_prerequisites():
            print("❌ Pipeline prerequisites not met")
            return False
        
        print("🚀 Running minimal pipeline test for introduction...")
        
        # Just test the introduction generation part
        paper_data = pipeline.pdf_processor.process_paper(pdf_path)
        raw_text = paper_data["raw_text"]
        
        core_sections = pipeline.enhanced_analyzer.enhanced_section_detection(raw_text)
        if not core_sections:
            print("❌ No core sections found")
            return False
        
        # Get Stage 1 understanding
        stage1 = pipeline.enhanced_analyzer.stage1_simple_understanding(core_sections)
        print(f"✅ Stage 1 - Paper Topic: {stage1.paper_topic}")
        print(f"✅ Stage 1 - Key Finding: {stage1.key_finding}")
        
        # Get Stage 2 results (minimal)
        print("📊 Running minimal Stage 2 for introduction material...")
        stage2 = pipeline.enhanced_analyzer.stage2_enhanced_claims_challenges(stage1, raw_text[:8000])
        
        # Generate enhanced introduction
        enhanced_intro = pipeline.enhanced_dialogue_generator.generate_enhanced_introduction(stage1, stage2)
        
        print(f"\n🎬 ENHANCED INTRODUCTION GENERATED:")
        print("─" * 60)
        print(enhanced_intro)
        print("─" * 60)
        
        # Check if it uses paper-specific content
        paper_specific_checks = []
        
        if stage1.paper_topic.lower() in enhanced_intro.lower():
            paper_specific_checks.append("✅ Uses actual paper topic")
        else:
            paper_specific_checks.append("❌ Missing paper topic")
        
        if any(word in enhanced_intro.lower() for word in stage1.key_finding.lower().split()[:3]):
            paper_specific_checks.append("✅ References key finding")
        else:
            paper_specific_checks.append("❌ Missing key finding reference")
        
        if "research rundown" in enhanced_intro.lower():
            paper_specific_checks.append("✅ Uses show branding")
        else:
            paper_specific_checks.append("❌ Missing show branding")
        
        # Check that it's not the old generic intro
        generic_phrases = ["what happens when you give two brilliant researchers", "groundbreaking paper", "completely opposite viewpoints"]
        if not any(phrase in enhanced_intro.lower() for phrase in generic_phrases):
            paper_specific_checks.append("✅ Not using old generic template")
        else:
            paper_specific_checks.append("⚠️ May be using old generic template")
        
        print(f"\n📊 INTRODUCTION QUALITY CHECKS:")
        for check in paper_specific_checks:
            print(f"   {check}")
        
        passed_checks = sum(1 for check in paper_specific_checks if check.startswith("✅"))
        total_checks = len(paper_specific_checks)
        
        print(f"\n🏆 Introduction Score: {passed_checks}/{total_checks}")
        
        if passed_checks >= 3:
            print("✅ Enhanced introduction working well!")
            return True
        else:
            print("⚠️ Introduction needs improvement")
            return False
        
    except Exception as e:
        print(f"❌ Enhanced introduction test failed: {e}")
        return False


def test_complete_integration():
    """Test that all fixes work together"""
    
    print("\n🚀 TESTING COMPLETE INTEGRATION")
    print("=" * 50)
    
    pdf_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ Test PDF not found: {pdf_path}")
        return False
    
    try:
        pipeline = IntegratedEnhancedPipeline()
        
        if not pipeline.check_prerequisites():
            print("❌ Prerequisites not met")
            return False
        
        print("🎯 Running complete integration test...")
        print("   (This will take several minutes)")
        
        # Run complete pipeline with minimal exchanges for testing
        complete_result, conversation_script, audio_result, stage1, stage2 = pipeline.process_paper_enhanced_pipeline(
            pdf_path, max_exchanges=2  # Minimal for testing
        )
        
        print(f"\n✅ COMPLETE INTEGRATION TEST RESULTS:")
        print(f"   🎯 Paper Topic: {stage1.paper_topic}")
        print(f"   💡 Key Finding: {stage1.key_finding}")
        print(f"   📋 Claims Analyzed: {len(stage2.paper_claims)}")
        print(f"   💬 Dialogue Turns: {conversation_script.total_turns}")
        print(f"   🎵 Audio Duration: {audio_result['total_duration']:.1f}s")
        print(f"   🎭 Voice Profiles Used: {len(audio_result.get('voice_profiles_used', []))}")
        print(f"   🧹 Text Cleanup Applied: {audio_result.get('text_cleanup_applied', False)}")
        
        # Verify audio file exists
        audio_file = Path(audio_result['output_file'])
        if audio_file.exists():
            print(f"   ✅ Audio file created: {audio_file.name}")
            file_size = audio_file.stat().st_size / (1024 * 1024)  # MB
            print(f"   📁 File size: {file_size:.1f} MB")
        else:
            print(f"   ❌ Audio file not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Complete integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    
    print("🧪 COMPREHENSIVE FIXES TEST SUITE")
    print("Testing all audio and integration fixes")
    print("=" * 80)
    
    test_results = []
    
    # Test 1: Text Cleanup
    test_results.append(("Text Cleanup", test_text_cleanup()))
    
    # Test 2: Voice Differentiation
    test_results.append(("Voice Differentiation", test_voice_differentiation()))
    
    # Test 3: Enhanced Introduction
    test_results.append(("Enhanced Introduction", test_enhanced_introduction()))
    
    # Test 4: Complete Integration (optional - takes time)
    run_full_test = input("\n❓ Run complete integration test? (takes several minutes) (y/N): ").strip().lower()
    if run_full_test in ['y', 'yes']:
        test_results.append(("Complete Integration", test_complete_integration()))
    
    # Final Results
    print(f"\n{'='*80}")
    print("🏆 FINAL TEST RESULTS")
    print(f"{'='*80}")
    
    passed = 0
    for test_name, result in test_results:
        if result:
            print(f"   ✅ {test_name}: PASSED")
            passed += 1
        else:
            print(f"   ❌ {test_name}: FAILED")
    
    total = len(test_results)
    print(f"\n📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL FIXES WORKING CORRECTLY!")
        print("✅ Ready for high-quality YouTube content generation!")
    elif passed >= total * 0.75:
        print("⚠️ Most fixes working - minor issues to address")
    else:
        print("❌ Multiple issues need fixing before production use")


if __name__ == "__main__":
    main()
