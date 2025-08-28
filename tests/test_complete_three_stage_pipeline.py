#!/usr/bin/env python3
"""
Complete Three-Stage Pipeline Test
Save as: test_complete_three_stage_pipeline.py (in root directory)

Tests the complete sophisticated analysis pipeline:
Stage 1: Core Understanding (Title + Abstract + Conclusion + Future Works)
Stage 2: Evidence Hunting (Full paper with claim-evidence mapping)
Stage 3: Sophisticated Debates (Expert-level evidence-based discussions)
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append('src')
sys.path.append('.')

# Import all components
try:
    from pdf_processor import PDFProcessor
    from two_stage_analyzer import TwoStageAnalyzer
    from stage3_sophisticated_debates import Stage3SophisticatedDebates
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have all required files:")
    print("  - src/pdf_processor.py")
    print("  - src/enhanced_analyzer.py") 
    print("  - src/stage2_evidence_hunter.py")
    print("  - src/two_stage_analyzer.py")
    print("  - src/stage3_sophisticated_debates.py")
    sys.exit(1)


def test_complete_three_stage_pipeline(pdf_path: str, max_topics: int = 3, exchanges_per_topic: int = 4):
    """Test complete three-stage sophisticated analysis pipeline"""
    
    print("🚀 COMPLETE THREE-STAGE SOPHISTICATED ANALYSIS")
    print("Stage 1: Core Understanding → Stage 2: Evidence Hunting → Stage 3: Expert Debates")
    print("=" * 90)
    
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print(f"📄 Processing: {pdf_file.name}")
    print(f"⚙️ Settings: {max_topics} topics, {exchanges_per_topic} exchanges per topic")
    
    # Initialize all processors
    pdf_processor = PDFProcessor()
    two_stage_analyzer = TwoStageAnalyzer()
    debate_generator = Stage3SophisticatedDebates()
    
    # Test all connections
    print(f"\n🔧 Testing connections...")
    
    if not two_stage_analyzer.test_connection():
        print("❌ Two-stage analyzer connection failed")
        return False
    print("✅ Two-stage analyzer ready")
    
    if not debate_generator.test_connection():
        print("❌ Debate generator connection failed")
        return False
    print("✅ Debate generator ready")
    
    try:
        # ================== PDF PROCESSING ==================
        print(f"\n{'='*25} PDF PROCESSING {'='*25}")
        
        print("📖 Extracting PDF content...")
        paper_data = pdf_processor.process_paper(pdf_path)
        raw_text = paper_data["raw_text"]
        print(f"✅ Extracted {len(raw_text):,} characters from PDF")
        
        # ================== STAGE 1 + 2: COMPREHENSIVE ANALYSIS ==================
        print(f"\n{'='*20} STAGE 1 + 2: COMPREHENSIVE ANALYSIS {'='*20}")
        
        print("🔍 Running two-stage comprehensive analysis...")
        complete_analysis = two_stage_analyzer.analyze_paper_complete(raw_text)
        
        # Display two-stage results summary
        print(f"\n📊 TWO-STAGE ANALYSIS SUMMARY:")
        print(f"   🎯 Field: {complete_analysis.core_understanding.field_classification}")
        print(f"   📖 Research story elements: {len(complete_analysis.core_understanding.research_story_arc)}")
        print(f"   ⚔️ Stage 1 debate points: {len(complete_analysis.core_understanding.debate_seed_points)}")
        print(f"   🔍 Evidence mappings: {len(complete_analysis.comprehensive_evidence.evidence_mappings)}")
        print(f"   🔬 Technical details: {len(complete_analysis.comprehensive_evidence.technical_deep_dive.algorithms_detailed) + len(complete_analysis.comprehensive_evidence.technical_deep_dive.performance_metrics)}")
        print(f"   🏆 Analysis quality: {complete_analysis.analysis_quality_score}/20")
        print(f"   🎬 Debate ready: {'✅ YES' if complete_analysis.ready_for_debates else '❌ NO'}")
        
        if not complete_analysis.ready_for_debates:
            print(f"\n⚠️ Analysis quality insufficient for sophisticated debates")
            print(f"   Minimum score needed: 12, Got: {complete_analysis.analysis_quality_score}")
            print(f"   Proceeding anyway for testing purposes...")
        
        # Show key evidence mappings
        evidence = complete_analysis.comprehensive_evidence.evidence_mappings
        if evidence:
            print(f"\n📋 KEY EVIDENCE MAPPINGS:")
            for i, mapping in enumerate(evidence[:3], 1):
                print(f"   {i}. CLAIM: {mapping.claim[:60]}...")
                print(f"      EVIDENCE: {mapping.evidence_strength.upper()}")
                if mapping.supporting_evidence:
                    print(f"      SUPPORT: {mapping.supporting_evidence[0][:50]}...")
        
        # Show debate ammunition
        ammunition = complete_analysis.comprehensive_evidence.expert_debate_ammunition
        print(f"\n⚔️ DEBATE AMMUNITION PREVIEW:")
        print(f"   😊 Optimist points: {len(ammunition.get('optimist', []))}")
        print(f"   🤨 Skeptic points: {len(ammunition.get('skeptic', []))}")
        
        if ammunition.get('optimist'):
            print(f"   😊 Sample optimist: {ammunition['optimist'][0][:60]}...")
        if ammunition.get('skeptic'):
            print(f"   🤨 Sample skeptic: {ammunition['skeptic'][0][:60]}...")
        
        # ================== STAGE 3: SOPHISTICATED DEBATES ==================
        print(f"\n{'='*20} STAGE 3: SOPHISTICATED DEBATES {'='*20}")
        
        print(f"🎭 Generating sophisticated evidence-based debates...")
        print(f"   📊 Using {len(complete_analysis.core_understanding.debate_seed_points)} debate points from Stage 1")
        print(f"   🔍 Using {len(evidence)} evidence mappings from Stage 2")
        
        sophisticated_debate = debate_generator.generate_sophisticated_debate(
            complete_analysis, max_topics, exchanges_per_topic
        )
        
        # ================== DISPLAY COMPLETE RESULTS ==================
        print(f"\n{'='*20} SOPHISTICATED DEBATE RESULTS {'='*20}")
        
        print(f"📄 PAPER: {sophisticated_debate.paper_title}")
        print(f"🎯 FIELD: {sophisticated_debate.field}")
        print(f"🏆 SOPHISTICATION SCORE: {sophisticated_debate.sophistication_score}/100")
        
        print(f"\n📊 DEBATE STATISTICS:")
        print(f"   🎭 Total turns: {sophisticated_debate.total_turns}")
        print(f"   📚 Evidence citations: {len(sophisticated_debate.evidence_citations)}")
        print(f"   🔬 Technical concepts: {len(sophisticated_debate.technical_concepts_discussed)}")
        print(f"   🎯 Topics covered: {len(sophisticated_debate.debate_topics)}")
        
        # Show debate topics
        print(f"\n🎯 SOPHISTICATED DEBATE TOPICS:")
        for i, topic in enumerate(sophisticated_debate.debate_topics, 1):
            print(f"   {i}. {topic}")
        
        # Show sample sophisticated exchanges
        print(f"\n💬 SAMPLE SOPHISTICATED EXCHANGES:")
        print("-" * 60)
        
        for i, turn in enumerate(sophisticated_debate.turns[:6]):  # Show first 6 turns
            speaker_emoji = "😊" if "Ava" in turn.speaker else "🤨"
            print(f"\n{speaker_emoji} **{turn.speaker}** ({turn.argument_type}):")
            print(f"{turn.content}")
            
            if turn.evidence_cited:
                print(f"   📚 Evidence: {', '.join(turn.evidence_cited[:2])}")
        
        if len(sophisticated_debate.turns) > 6:
            print(f"\n... and {len(sophisticated_debate.turns) - 6} more sophisticated turns")
        
        # ================== QUALITY ASSESSMENT ==================
        print(f"\n{'='*20} COMPLETE PIPELINE QUALITY ASSESSMENT {'='*20}")
        
        pipeline_score = 0
        max_pipeline_score = 30
        
        # Stage 1 + 2 quality (15 points)
        if complete_analysis.analysis_quality_score >= 15:
            pipeline_score += 8
            print("   ✅ Outstanding two-stage analysis (+8)")
        elif complete_analysis.analysis_quality_score >= 12:
            pipeline_score += 6
            print("   ✅ Excellent two-stage analysis (+6)")
        elif complete_analysis.analysis_quality_score >= 8:
            pipeline_score += 4
            print("   ✅ Good two-stage analysis (+4)")
        else:
            pipeline_score += 2
            print("   ⚠️ Basic two-stage analysis (+2)")
        
        # Stage 3 sophistication (15 points)
        if sophisticated_debate.sophistication_score >= 80:
            pipeline_score += 7
            print("   ✅ Outstanding debate sophistication (+7)")
        elif sophisticated_debate.sophistication_score >= 60:
            pipeline_score += 5
            print("   ✅ High debate sophistication (+5)")
        elif sophisticated_debate.sophistication_score >= 40:
            pipeline_score += 3
            print("   ✅ Moderate debate sophistication (+3)")
        else:
            pipeline_score += 1
            print("   ⚠️ Basic debate sophistication (+1)")
        
        # Evidence integration quality (10 points)
        citation_density = len(sophisticated_debate.evidence_citations) / sophisticated_debate.total_turns if sophisticated_debate.total_turns else 0
        if citation_density >= 1.0:
            pipeline_score += 5
            print("   ✅ Excellent evidence integration (+5)")
        elif citation_density >= 0.5:
            pipeline_score += 3
            print("   ✅ Good evidence integration (+3)")
        elif citation_density >= 0.2:
            pipeline_score += 2
            print("   ✅ Basic evidence integration (+2)")
        
        # Technical depth integration (5 points)
        unique_concepts = len(set(sophisticated_debate.technical_concepts_discussed))
        if unique_concepts >= 8:
            pipeline_score += 3
            print("   ✅ High technical depth (+3)")
        elif unique_concepts >= 4:
            pipeline_score += 2
            print("   ✅ Moderate technical depth (+2)")
        elif unique_concepts >= 2:
            pipeline_score += 1
            print("   ✅ Basic technical depth (+1)")
        
        # Field adaptation (5 points)
        if complete_analysis.core_understanding.field_classification != "General Research":
            pipeline_score += 2
            print("   ✅ Field-specific adaptation (+2)")
        
        print(f"\n🏆 COMPLETE PIPELINE SCORE: {pipeline_score}/{max_pipeline_score}")
        
        if pipeline_score >= 25:
            print("🌟 OUTSTANDING - Sophisticated academic-quality debates ready!")
            print("🎬 Perfect for high-quality YouTube content!")
        elif pipeline_score >= 20:
            print("✅ EXCELLENT - High-quality evidence-based debates generated!")
            print("🎬 Ready for sophisticated YouTube content!")
        elif pipeline_score >= 15:
            print("⚠️ GOOD - Solid debates with room for improvement")
            print("🎬 Suitable for YouTube with minor enhancements")
        else:
            print("❌ NEEDS IMPROVEMENT - Enhance analysis depth before production")
        
        # Detailed breakdown
        print(f"\n📈 SOPHISTICATION BREAKDOWN:")
        print(f"   📊 Evidence citations per turn: {citation_density:.2f}")
        print(f"   🔬 Unique technical concepts: {unique_concepts}")
        print(f"   📝 Average turn length: {sum(len(turn.content) for turn in sophisticated_debate.turns) / len(sophisticated_debate.turns):.0f} chars")
        print(f"   🎯 Field-specific expertise: {complete_analysis.core_understanding.field_classification}")
        
        # Success criteria
        success = pipeline_score >= 15 and sophisticated_debate.sophistication_score >= 40
        
        print(f"\n🎯 PIPELINE SUCCESS: {'✅ YES' if success else '❌ NO'}")
        
        if success:
            print(f"\n🚀 NEXT STEPS:")
            print(f"   1. ✅ Three-stage analysis pipeline working excellently")
            print(f"   2. 🎵 Ready to integrate with audio generation (Stage 4)")
            print(f"   3. 🎥 Ready to integrate with video generation (Stage 5)")
            print(f"   4. 🎬 Generate sophisticated YouTube content!")
        else:
            print(f"\n🔧 IMPROVEMENT NEEDED:")
            print(f"   1. 📈 Enhance analysis depth (current: {complete_analysis.analysis_quality_score}/20)")
            print(f"   2. 🎭 Improve debate sophistication (current: {sophisticated_debate.sophistication_score}/100)")
            print(f"   3. 📚 Increase evidence citation density (current: {citation_density:.2f})")
            print(f"   4. 🔄 Re-test before production integration")
        
        return success
        
    except Exception as e:
        print(f"❌ Error during three-stage pipeline: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    
    print("🚀 AI Paper Narrator - Complete Three-Stage Pipeline Test")
    print("Testing Enhanced Stage 1 + Stage 2 + Stage 3 Sophisticated Debates")
    print("-" * 90)
    
    # Default paper path
    default_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        max_topics = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        exchanges_per_topic = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    else:
        pdf_path = default_path
        max_topics = 3
        exchanges_per_topic = 4
    
    print(f"📄 Testing with: {pdf_path}")
    print(f"⚙️ Settings: {max_topics} topics, {exchanges_per_topic} exchanges per topic")
    
    success = test_complete_three_stage_pipeline(pdf_path, max_topics, exchanges_per_topic)
    
    if success:
        print(f"\n🎉 THREE-STAGE PIPELINE TEST SUCCESSFUL!")
        print(f"✅ Stage 1: Core understanding with comprehensive analysis")
        print(f"✅ Stage 2: Evidence hunting with claim-evidence mapping")
        print(f"✅ Stage 3: Sophisticated evidence-based expert debates")
        print(f"✅ Field-specific expertise adaptation")
        print(f"✅ Academic-quality technical discussions")
        print(f"\n🎬 READY FOR YOUTUBE INTEGRATION!")
        print(f"🔗 Next: Integrate with existing audio/video pipeline")
    else:
        print(f"\n🔧 THREE-STAGE PIPELINE NEEDS IMPROVEMENT")
        print(f"❌ Check quality assessments above for specific issues")
        print(f"🔍 Debug individual stages before YouTube integration")


if __name__ == "__main__":
    main()
