#!/usr/bin/env python3
"""
Test Stage 1 + Stage 2 Integration
Save as: test_stage1_stage2_integration.py (in root directory)

Tests the complete two-stage analysis:
1. Stage 1: Core Understanding (Title + Abstract + Conclusion + Future Works)
2. Stage 2: Evidence Hunting (Full paper analysis with claim-evidence mapping)
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append('src')
sys.path.append('.')

# Import components
try:
    from pdf_processor import PDFProcessor
    from enhanced_analyzer import EnhancedPaperAnalyzer
    from stage2_evidence_hunter import Stage2EvidenceHunter
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have:")
    print("  - pdf_processor.py in src/")
    print("  - enhanced_analyzer.py in current directory")
    print("  - stage2_evidence_hunter.py in src/")
    sys.exit(1)


def test_complete_two_stage_analysis(pdf_path: str):
    """Test complete Stage 1 + Stage 2 analysis pipeline"""
    
    print("🚀 COMPLETE TWO-STAGE ANALYSIS TEST")
    print("Stage 1: Core Understanding → Stage 2: Evidence Hunting")
    print("=" * 80)
    
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print(f"📄 Analyzing: {pdf_file.name}")
    
    # Initialize all processors
    pdf_processor = PDFProcessor()
    stage1_analyzer = EnhancedPaperAnalyzer()
    stage2_hunter = Stage2EvidenceHunter()
    
    # Test connections
    if not stage1_analyzer.test_connection():
        print("❌ Ollama connection failed for Stage 1")
        return False
    
    if not stage2_hunter.test_connection():
        print("❌ Ollama connection failed for Stage 2")
        return False
    
    print("✅ All connections successful")
    
    try:
        # ================== STAGE 1: CORE UNDERSTANDING ==================
        print(f"\n{'='*20} STAGE 1: CORE UNDERSTANDING {'='*20}")
        
        # Extract and process PDF
        print("📖 Extracting PDF content...")
        paper_data = pdf_processor.process_paper(pdf_path)
        raw_text = paper_data["raw_text"]
        print(f"✅ Extracted {len(raw_text):,} characters")
        
        # Enhanced section detection
        print("\n🔍 Stage 1: Detecting core sections...")
        core_sections = stage1_analyzer.enhanced_section_detection(raw_text)
        
        if not core_sections:
            print("❌ No core sections found - cannot proceed")
            return False
        
        print(f"✅ Found {len(core_sections)} core sections")
        for section, content in core_sections.items():
            print(f"   • {section}: {len(content)} characters")
        
        # Stage 1 comprehensive analysis
        print(f"\n🧠 Stage 1: Comprehensive core analysis...")
        core_understanding = stage1_analyzer.stage1_core_understanding_analysis(core_sections)
        
        # Display Stage 1 results
        print(f"\n📊 STAGE 1 RESULTS SUMMARY:")
        print(f"   🎯 Field: {core_understanding.field_classification}")
        print(f"   📖 Story elements: {len(core_understanding.research_story_arc)}")
        print(f"   🔍 Confidence factors: {len(core_understanding.confidence_assessment)}")
        print(f"   ⚔️ Debate points: {len(core_understanding.debate_seed_points)}")
        print(f"   🔧 Technical elements: {len(core_understanding.key_technical_elements)}")
        
        # ================== STAGE 2: EVIDENCE HUNTING ==================
        print(f"\n{'='*20} STAGE 2: EVIDENCE HUNTING {'='*20}")
        
        # Stage 2 comprehensive evidence analysis
        print("🔍 Stage 2: Comprehensive evidence hunting...")
        comprehensive_evidence = stage2_hunter.comprehensive_stage2_analysis(
            core_understanding, raw_text
        )
        
        # ================== DISPLAY COMPREHENSIVE RESULTS ==================
        print(f"\n{'='*20} COMPREHENSIVE ANALYSIS RESULTS {'='*20}")
        
        # Evidence Mappings
        print(f"\n📋 EVIDENCE-CLAIM MAPPINGS ({len(comprehensive_evidence.evidence_mappings)}):")
        for i, mapping in enumerate(comprehensive_evidence.evidence_mappings, 1):
            print(f"\n   {i}. CLAIM: {mapping.claim[:80]}...")
            print(f"      EVIDENCE STRENGTH: {mapping.evidence_strength.upper()}")
            
            if mapping.supporting_evidence:
                print(f"      ✅ SUPPORTING ({len(mapping.supporting_evidence)}):")
                for evidence in mapping.supporting_evidence[:2]:
                    print(f"         • {evidence[:60]}...")
            
            if mapping.contradictory_evidence:
                print(f"      ❌ CONTRADICTORY ({len(mapping.contradictory_evidence)}):")
                for evidence in mapping.contradictory_evidence[:2]:
                    print(f"         • {evidence[:60]}...")
            
            if mapping.evidence_location:
                print(f"      📍 LOCATIONS: {', '.join(mapping.evidence_location[:3])}")
        
        # Technical Deep Dive
        tech = comprehensive_evidence.technical_deep_dive
        print(f"\n🔬 TECHNICAL DEEP DIVE:")
        print(f"   🧮 Algorithms: {len(tech.algorithms_detailed)}")
        print(f"   🧪 Experimental Design: {len(tech.experimental_design)}")
        print(f"   📊 Statistical Results: {len(tech.statistical_results)}")
        print(f"   📈 Performance Metrics: {len(tech.performance_metrics)}")
        print(f"   💻 Implementation: {len(tech.implementation_details)}")
        print(f"   ⚖️ Comparisons: {len(tech.comparison_results)}")
        print(f"   ⚠️ Limitations: {len(tech.limitations_detailed)}")
        
        # Show sample technical details
        if tech.algorithms_detailed:
            print(f"\n   🧮 SAMPLE ALGORITHMS:")
            for alg in tech.algorithms_detailed[:2]:
                print(f"      • {alg[:80]}...")
        
        if tech.performance_metrics:
            print(f"\n   📈 SAMPLE PERFORMANCE:")
            for metric in tech.performance_metrics[:2]:
                print(f"      • {metric[:80]}...")
        
        # Methodology Analysis
        method = comprehensive_evidence.methodology_analysis
        print(f"\n📐 METHODOLOGY ANALYSIS:")
        print(f"   📊 Data Collection: {len(method.data_collection)}")
        print(f"   👥 Sample Info: {len(method.sample_characteristics)}")
        print(f"   🎛️ Controls: {len(method.control_measures)}")
        print(f"   ✅ Validation: {len(method.validation_approaches)}")
        print(f"   📊 Statistical Methods: {len(method.statistical_methods)}")
        print(f"   ⚠️ Potential Biases: {len(method.potential_biases)}")
        
        # Gaps and Overclaims
        print(f"\n🔍 CRITICAL ANALYSIS:")
        print(f"   📉 Evidence Gaps: {len(comprehensive_evidence.claim_evidence_gaps)}")
        print(f"   📢 Potential Overclaims: {len(comprehensive_evidence.overclaim_detection)}")
        
        if comprehensive_evidence.claim_evidence_gaps:
            print(f"\n   📉 EVIDENCE GAPS:")
            for gap in comprehensive_evidence.claim_evidence_gaps[:3]:
                print(f"      • {gap[:80]}...")
        
        if comprehensive_evidence.overclaim_detection:
            print(f"\n   📢 POTENTIAL OVERCLAIMS:")
            for overclaim in comprehensive_evidence.overclaim_detection[:3]:
                print(f"      • {overclaim[:80]}...")
        
        # Debate Ammunition
        ammunition = comprehensive_evidence.expert_debate_ammunition
        print(f"\n⚔️ EXPERT DEBATE AMMUNITION:")
        print(f"   😊 Optimist Points: {len(ammunition.get('optimist', []))}")
        print(f"   🤨 Skeptic Points: {len(ammunition.get('skeptic', []))}")
        
        if ammunition.get('optimist'):
            print(f"\n   😊 OPTIMIST AMMUNITION:")
            for point in ammunition['optimist'][:3]:
                print(f"      + {point[:70]}...")
        
        if ammunition.get('skeptic'):
            print(f"\n   🤨 SKEPTIC AMMUNITION:")
            for point in ammunition['skeptic'][:3]:
                print(f"      - {point[:70]}...")
        
        # ================== QUALITY ASSESSMENT ==================
        print(f"\n{'='*20} COMPREHENSIVE QUALITY ASSESSMENT {'='*20}")
        
        quality_score = 0
        max_score = 20
        
        # Stage 1 quality
        if core_understanding.field_classification != "General Research":
            quality_score += 2
            print("   ✅ Specific field identified (+2)")
        
        if len(core_understanding.debate_seed_points) >= 8:
            quality_score += 3
            print("   ✅ Excellent Stage 1 debate depth (+3)")
        elif len(core_understanding.debate_seed_points) >= 5:
            quality_score += 2
            print("   ✅ Good Stage 1 debate coverage (+2)")
        
        # Stage 2 quality
        if len(comprehensive_evidence.evidence_mappings) >= 3:
            quality_score += 3
            print("   ✅ Multiple evidence mappings (+3)")
        
        strong_evidence_count = sum(1 for m in comprehensive_evidence.evidence_mappings if m.evidence_strength == 'strong')
        if strong_evidence_count >= 1:
            quality_score += 2
            print(f"   ✅ Strong evidence found ({strong_evidence_count} claims) (+2)")
        
        if len(tech.algorithms_detailed) + len(tech.performance_metrics) >= 4:
            quality_score += 3
            print("   ✅ Comprehensive technical analysis (+3)")
        
        if len(method.potential_biases) + len(comprehensive_evidence.claim_evidence_gaps) >= 3:
            quality_score += 2
            print("   ✅ Critical analysis with gaps/biases identified (+2)")
        
        if len(ammunition.get('optimist', [])) >= 3 and len(ammunition.get('skeptic', [])) >= 3:
            quality_score += 3
            print("   ✅ Balanced debate ammunition generated (+3)")
        
        # Bonus for sophisticated analysis
        if any('statistical' in str(item).lower() for item in [tech.statistical_results, method.statistical_methods]):
            quality_score += 2
            print("   ✅ Statistical sophistication detected (+2)")
        
        print(f"\n🏆 COMPREHENSIVE QUALITY SCORE: {quality_score}/{max_score}")
        
        if quality_score >= 15:
            print("🌟 OUTSTANDING - Maximum depth achieved, ready for expert debates!")
        elif quality_score >= 12:
            print("✅ EXCELLENT - High quality two-stage analysis, ready for debates!")
        elif quality_score >= 8:
            print("⚠️ GOOD - Solid analysis, minor improvements possible")
        else:
            print("❌ NEEDS IMPROVEMENT - Enhance prompts or check paper complexity")
        
        # Final summary
        print(f"\n🎯 ANALYSIS COMPLETENESS:")
        print(f"   Stage 1: Core understanding ✅ ({len(core_understanding.debate_seed_points)} debate points)")
        print(f"   Stage 2: Evidence hunting ✅ ({len(comprehensive_evidence.evidence_mappings)} claim mappings)")
        print(f"   Technical depth: {'✅ Excellent' if len(tech.algorithms_detailed) + len(tech.performance_metrics) >= 4 else '⚠️ Moderate'}")
        print(f"   Debate readiness: {'✅ Ready' if quality_score >= 12 else '⚠️ Needs work'}")
        
        return quality_score >= 8
        
    except Exception as e:
        print(f"❌ Error during two-stage analysis: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    
    print("🚀 AI Paper Narrator - Complete Two-Stage Analysis Test")
    print("Testing Enhanced Stage 1 + Stage 2 Evidence Hunting")
    print("-" * 80)
    
    # Default paper path
    default_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = default_path
    
    print(f"📄 Testing with: {pdf_path}")
    
    success = test_complete_two_stage_analysis(pdf_path)
    
    if success:
        print(f"\n🎉 TWO-STAGE ANALYSIS SUCCESSFUL!")
        print(f"✅ Stage 1: Core understanding with comprehensive debate points")
        print(f"✅ Stage 2: Evidence hunting with claim-evidence mapping")
        print(f"✅ Technical deep dive with expert-level details")
        print(f"✅ Methodology analysis with bias detection")
        print(f"✅ Debate ammunition for optimist vs skeptic discussions")
        print(f"\n🚀 READY FOR STAGE 3: SOPHISTICATED DEBATE GENERATION")
    else:
        print(f"\n🔧 TWO-STAGE ANALYSIS NEEDS IMPROVEMENT")
        print(f"❌ Check quality assessment above for specific issues")
        print(f"🔍 Debug individual stages before proceeding")


if __name__ == "__main__":
    main()
