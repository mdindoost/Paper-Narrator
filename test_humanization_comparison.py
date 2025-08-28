#!/usr/bin/env python3
"""
Test Humanization - Before vs After Comparison
Save as: test_humanization_comparison.py (in root directory)

Shows the exact improvements made by the humanization pipeline
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append('src')
sys.path.append('.')

try:
    from humanized_dialogue_pipeline import HumanizedEnhancedPipeline, HumanizedDialogueRefiner
    from integrated_enhanced_pipeline import IntegratedEnhancedPipeline
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have:")
    print("  - humanized_dialogue_pipeline.py in src/")
    print("  - integrated_enhanced_pipeline.py in src/")
    sys.exit(1)


def test_text_cleanup_examples():
    """Show specific text cleanup improvements"""
    
    print("🧹 TEXT CLEANUP EXAMPLES")
    print("=" * 60)
    
    refiner = HumanizedDialogueRefiner()
    
    # Test field cleanup
    print("🎯 FIELD CLASSIFICATION CLEANUP:")
    test_fields = [
        "** Computer Science - Algorithms and Network Analysis",
        "Computer Science - Machine Learning",
        "Biology - Molecular Biology"
    ]
    
    for field in test_fields:
        cleaned = refiner.clean_field_classification(field)
        print(f"  Before: {field}")
        print(f"  After:  {cleaned}")
        print()
    
    # Test category label removal
    print("🏷️ CATEGORY LABEL REMOVAL:")
    test_ammunition = [
        "Lack of context: The paper does not provide sufficient background.",
        "Segmentation Faults: While it's clear that the approach works, there are issues.",
        "Sample Size Issues: The study only included 847 participants.",
        "Statistical Problems: Multiple comparisons were not corrected."
    ]
    
    for ammo in test_ammunition:
        cleaned = refiner.remove_category_labels(ammo)
        print(f"  Before: {ammo}")
        print(f"  After:  {cleaned}")
        print()


def test_voice_assignments():
    """Test correct voice assignments"""
    
    print("🎤 VOICE ASSIGNMENT CORRECTIONS")
    print("=" * 60)
    
    refiner = HumanizedDialogueRefiner()
    
    test_speakers = [
        "Host",
        "Narrator", 
        "Dr. Ava D.",
        "Sarah Chen",
        "Prof. Marcus Webb",
        "Prof. Marcus W."
    ]
    
    print("✅ CORRECTED VOICE ASSIGNMENTS:")
    for speaker in test_speakers:
        profile = refiner.get_voice_profile(speaker)
        print(f"  {speaker:20} → {profile.voice_id} ({profile.gender} - {profile.description})")


def test_humanization_examples():
    """Test AI humanization of dialogue"""
    
    print("\n🎭 HUMANIZATION EXAMPLES")
    print("=" * 60)
    
    refiner = HumanizedDialogueRefiner()
    
    # Test introduction cleanup
    print("🎬 INTRODUCTION HUMANIZATION:")
    sample_intro = """Today's fascinating topic: ** Algorithms and Network Analysis

The authors claim ** significant improvements in community detection algorithms. 

Our analysis reveals 5 strong claims vs 0 questionable claims - setting up the perfect storm for an academic showdown."""
    
    print("BEFORE:")
    print(sample_intro)
    print("\nAFTER:")
    humanized_intro = refiner.humanize_introduction(
        sample_intro, 
        "** Computer Science - Algorithms and Network Analysis",
        "Community detection algorithms",
        "Improved algorithmic performance"
    )
    print(humanized_intro)
    print()
    
    # Test dialogue humanization - create mock turn
    from integrated_enhanced_pipeline import ConversationTurn
    
    print("💬 DIALOGUE HUMANIZATION:")
    
    # Optimist turn example
    sample_optimist_content = "Lack of context: The paper shows impressive results with 60% improvement over baseline algorithms. Statistical significance: p < 0.001 demonstrates clear benefits."
    
    mock_optimist_turn = ConversationTurn(
        speaker="Dr. Ava D.",
        speaker_role="Enthusiastic Researcher", 
        content=sample_optimist_content,
        topic="Algorithm Performance",
        turn_number=1,
        source_type="claim_evidence"
    )
    
    print("OPTIMIST BEFORE:")
    print(f"  {mock_optimist_turn.content}")
    
    humanized_optimist = refiner.humanize_dialogue_turn(mock_optimist_turn)
    print("OPTIMIST AFTER:")
    print(f"  {humanized_optimist.content}")
    print()
    
    # Skeptic turn example
    sample_skeptic_content = "Segmentation Faults: While the results look promising, I'm concerned about the sample size of only 847 participants. Reproducibility Issues: The implementation details are insufficient for replication."
    
    mock_skeptic_turn = ConversationTurn(
        speaker="Prof. Marcus W.",
        speaker_role="Critical Analyst",
        content=sample_skeptic_content, 
        topic="Methodology Concerns",
        turn_number=2,
        source_type="challenge_critique"
    )
    
    print("SKEPTIC BEFORE:")
    print(f"  {mock_skeptic_turn.content}")
    
    humanized_skeptic = refiner.humanize_dialogue_turn(mock_skeptic_turn)
    print("SKEPTIC AFTER:")
    print(f"  {humanized_skeptic.content}")


def compare_full_pipeline_outputs(pdf_path: str):
    """Compare original vs humanized pipeline outputs"""
    
    print("\n🔄 FULL PIPELINE COMPARISON")
    print("=" * 60)
    
    # Test original pipeline
    print("🤖 RUNNING ORIGINAL PIPELINE...")
    original_pipeline = IntegratedEnhancedPipeline()
    
    if not original_pipeline.check_prerequisites():
        print("❌ Prerequisites not met for original pipeline")
        return
    
    # Test humanized pipeline  
    print("🎭 RUNNING HUMANIZED PIPELINE...")
    humanized_pipeline = HumanizedEnhancedPipeline()
    
    if not humanized_pipeline.check_prerequisites():
        print("❌ Prerequisites not met for humanized pipeline")
        return
    
    try:
        # Just test the first few steps to compare outputs
        paper_data = original_pipeline.pdf_processor.process_paper(pdf_path)
        raw_text = paper_data["raw_text"]
        
        core_sections = original_pipeline.enhanced_analyzer.enhanced_section_detection(raw_text)
        stage1 = original_pipeline.enhanced_analyzer.stage1_simple_understanding(core_sections)
        stage2 = original_pipeline.enhanced_analyzer.stage2_enhanced_claims_challenges(stage1, raw_text)
        
        # Generate original conversation
        original_script = original_pipeline.enhanced_dialogue_generator.create_enhanced_conversation_script(
            stage1, stage2, max_exchanges=2
        )
        
        # Generate humanized conversation
        refiner = HumanizedDialogueRefiner() 
        humanized_script = refiner.refine_conversation_script(original_script, stage1.research_field)
        
        # Compare results
        print(f"\n📊 COMPARISON RESULTS:")
        print(f"{'='*60}")
        
        print(f"\n🎯 FIELD CLASSIFICATION:")
        print(f"  Original:  {stage1.research_field}")
        print(f"  Humanized: {humanized_script.research_field}")
        
        print(f"\n🎬 INTRODUCTION COMPARISON:")
        print(f"  Original (first 100 chars):  {original_script.introduction[:100]}...")
        print(f"  Humanized (first 100 chars): {humanized_script.introduction[:100]}...")
        
        if original_script.turns and humanized_script.turns:
            print(f"\n💬 FIRST DIALOGUE TURN:")
            orig_turn = original_script.turns[0]
            human_turn = humanized_script.turns[0]
            
            print(f"  Original:  {orig_turn.content[:100]}...")
            print(f"  Humanized: {human_turn.content[:100]}...")
        
        print(f"\n✅ COMPARISON COMPLETE - Check the differences above!")
        
    except Exception as e:
        print(f"❌ Pipeline comparison failed: {e}")


def main():
    """Main comparison test"""
    
    print("🎭 HUMANIZATION IMPROVEMENT TEST")
    print("Compare before/after dialogue refinement")
    print("=" * 80)
    
    # Run individual tests
    test_text_cleanup_examples()
    test_voice_assignments()
    test_humanization_examples()
    
    # Full pipeline comparison
    default_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = default_path
    
    print(f"\n📄 Testing with paper: {pdf_path}")
    compare_full_pipeline_outputs(pdf_path)
    
    print(f"\n🎯 KEY IMPROVEMENTS:")
    print(f"   ✅ Field: '** Computer Science - X' → 'X' (most specific)")
    print(f"   ✅ Voice: Host=Male, Ava=Female, Marcus=Male")  
    print(f"   ✅ Text: 'Lack of context: The paper...' → 'I'm concerned that...'")
    print(f"   ✅ Natural: Academic ammunition → Human conversation")
    print(f"   ✅ Flow: Robotic bullets → Engaging dialogue")


if __name__ == "__main__":
    main()
