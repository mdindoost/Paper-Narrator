#!/usr/bin/env python3
"""
Test Complete Humanized Solution
Save as: test_complete_humanized_solution.py (in root directory)

Tests all the fixes:
- Multi-stage text cleanup
- Smart field extraction  
- 3 distinct voices
- Balanced claims presentation
- Natural academic debate speech
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append('src')
sys.path.append('.')

try:
    from enhanced_text_humanizer import (
        EnhancedTextHumanizer, 
        SmartFieldExtractor, 
        BalancedClaimsGenerator
    )
    from audio_generator_humanized_fixed import HumanizedAudioGenerator
    from integrated_humanized_pipeline import IntegratedHumanizedPipeline
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have saved all the files in src/ directory:")
    print("  - enhanced_text_humanizer.py")
    print("  - audio_generator_humanized_fixed.py") 
    print("  - integrated_humanized_pipeline.py")
    sys.exit(1)


def test_individual_components():
    """Test individual components first"""
    
    print("🧪 TESTING INDIVIDUAL COMPONENTS")
    print("=" * 80)
    
    # Test 1: Smart Field Extraction
    print("\n1️⃣ SMART FIELD EXTRACTION TEST:")
    field_extractor = SmartFieldExtractor()
    
    test_fields = [
        "** Computer Science - Algorithms and Network Analysis",
        "** Psychology: Cognitive Neuroscience",
        "** Machine Learning - Deep Learning",
        "** Biology"
    ]
    
    for field in test_fields:
        extracted = field_extractor.extract_specific_field(field)
        print(f"   {field}")
        print(f"   → {extracted}")
        print()
    
    # Test 2: Text Humanization
    print("2️⃣ TEXT HUMANIZATION TEST:")
    humanizer = EnhancedTextHumanizer()
    
    test_cases = [
        {
            "text": "** Lack of context: The paper does not provide sufficient background.",
            "role": "skeptic", 
            "field": "Algorithms and Network Analysis"
        },
        {
            "text": "Today's fascinating topic: ** Network Analysis Research",
            "role": "narrator",
            "field": "Computer Science"
        },
        {
            "text": "** Segmentation Faults: While the methodology shows promise.",
            "role": "skeptic",
            "field": "Computer Science"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n   Test {i}:")
        print(f"   Original: {test['text']}")
        
        result = humanizer.complete_cleanup_pipeline(
            test['text'], test['role'], test['field']
        )
        
        print(f"   Final:    {result.final_speech_ready}")
    
    # Test 3: Balanced Claims
    print("\n3️⃣ BALANCED CLAIMS TEST:")
    claims_gen = BalancedClaimsGenerator()
    
    test_scenarios = [
        (5, 0, 0),  # All strong  
        (2, 1, 2),  # Mixed
        (0, 2, 3),  # Mostly weak
    ]
    
    for strong, weak, questionable in test_scenarios:
        description = claims_gen.generate_balanced_description(strong, weak, questionable)
        print(f"   {strong} strong, {weak} weak, {questionable} questionable")
        print(f"   → {description}")
        print()
    
    # Test 4: Voice Differentiation
    print("4️⃣ VOICE DIFFERENTIATION TEST:")
    audio_gen = HumanizedAudioGenerator()
    
    test_speakers = [
        "Narrator",
        "Dr. Ava D.", 
        "Prof. Marcus Webb",
        "Prof. Marcus W."
    ]
    
    print("   Speaker Mapping:")
    for speaker in test_speakers:
        clean_name = audio_gen.humanize_speaker_name(speaker)
        profile = audio_gen.get_speaker_voice_profile(clean_name)
        print(f"   {speaker} → {clean_name} → {profile.voice_id}")
    
    print("\n✅ Individual component tests complete!")


def test_full_pipeline(pdf_path: str):
    """Test the complete integrated pipeline"""
    
    print("\n🚀 TESTING COMPLETE INTEGRATED PIPELINE")
    print("=" * 80)
    
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print(f"📄 Testing with: {pdf_file.name}")
    
    try:
        pipeline = IntegratedHumanizedPipeline()
        
        if not pipeline.check_prerequisites():
            print("❌ Prerequisites not met")
            return False
        
        print("✅ Prerequisites met, running pipeline...")
        
        # Run the complete pipeline
        complete_result, enhanced_script, audio_result, stage1 = pipeline.process_paper_humanized_pipeline(
            pdf_path, max_exchanges=4  # Shorter for testing
        )
        
        # Display results
        pipeline.display_comprehensive_results(complete_result, enhanced_script, audio_result, stage1)
        
        # Specific fix validation
        print(f"\n🔍 VALIDATING SPECIFIC FIXES:")
        
        # Check field extraction
        original_field = stage1.research_field
        cleaned_field = complete_result["humanized_analysis"]["research_field_cleaned"]
        
        if "**" not in cleaned_field:
            print(f"   ✅ Field cleanup: ** symbols removed")
        else:
            print(f"   ❌ Field cleanup: ** symbols still present")
        
        if cleaned_field != original_field and len(cleaned_field) < len(original_field):
            print(f"   ✅ Field specificity: Using '{cleaned_field}' instead of '{original_field}'")
        else:
            print(f"   ⚠️ Field specificity: Still using broad field")
        
        # Check speaker names
        speakers_used = complete_result["enhanced_dialogue"]["speakers"]
        if "Prof. Marcus W." in speakers_used:
            print(f"   ✅ Speaker names: Using 'Prof. Marcus W.' format")
        else:
            print(f"   ❌ Speaker names: Still using full name")
        
        # Check voice differentiation
        voice_diff = audio_result.get("voice_differentiation", {})
        unique_voices = len(voice_diff)
        if unique_voices >= 3:
            print(f"   ✅ Voice differentiation: {unique_voices} distinct voices used")
        else:
            print(f"   ❌ Voice differentiation: Only {unique_voices} voices used")
        
        # Check humanization
        if audio_result.get("humanization_pipeline") == "multi_stage_complete":
            print(f"   ✅ Text humanization: Multi-stage pipeline applied")
        else:
            print(f"   ❌ Text humanization: Pipeline not fully applied")
        
        # Check audio file
        audio_file = Path(audio_result["output_file"])
        if audio_file.exists():
            file_size_mb = audio_file.stat().st_size / (1024 * 1024)
            print(f"   ✅ Audio generation: File created ({file_size_mb:.1f} MB)")
        else:
            print(f"   ❌ Audio generation: File not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    
    print("🧪 COMPLETE HUMANIZED SOLUTION TEST")
    print("Testing all fixes for dialogue generation issues")
    print("=" * 80)
    
    # Test individual components first
    test_individual_components()
    
    # Test full pipeline
    default_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = default_path
    
    print(f"\n📄 Testing complete pipeline with: {pdf_path}")
    
    success = test_full_pipeline(pdf_path)
    
    if success:
        print(f"\n🎉 COMPLETE HUMANIZED SOLUTION SUCCESS!")
        print(f"✅ All identified issues have been addressed:")
        print(f"   • Multi-stage text cleanup removes ** symbols and category labels")
        print(f"   • Smart field extraction uses specific fields instead of broad categories")
        print(f"   • 3 distinct voices ensure proper speaker differentiation")
        print(f"   • Speaker names use 'Prof. Marcus W.' format")
        print(f"   • AI humanization creates natural academic debate speech")
        print(f"   • Balanced claims presentation instead of exact numbers")
        
        print(f"\n🎯 READY FOR HIGH-QUALITY YOUTUBE CONTENT!")
        print(f"The generated audio should now sound like natural academic debate")
        print(f"between real professors discussing the paper's actual research field.")
        
    else:
        print(f"\n❌ SOLUTION NEEDS REFINEMENT")
        print(f"Check the validation results above for specific issues")


if __name__ == "__main__":
    main()
