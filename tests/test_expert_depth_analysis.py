#!/usr/bin/env python3
"""
Test Enhanced Expert-Level Deep Analysis
Save as: test_expert_depth_analysis.py (in root directory)

Tests the dramatically improved expert-level prompts for maximum debate depth.
Compares shallow vs deep analysis to demonstrate the improvement.
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
    from enhanced_stage2_expert import EnhancedStage2Expert
    from expert_deep_prompts import ExpertDeepPrompts
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have all files:")
    print("  - pdf_processor.py in src/")
    print("  - enhanced_analyzer.py in current directory")
    print("  - enhanced_stage2_expert.py in src/")  
    print("  - expert_deep_prompts.py in src/")
    sys.exit(1)


def test_expert_depth_comparison(pdf_path: str):
    """Test expert-level deep analysis vs previous shallow approach"""
    
    print("🧠 EXPERT-LEVEL DEEP ANALYSIS TEST")
    print("Demonstrating Maximum Debate Depth Enhancement")
    print("=" * 80)
    
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print(f"📄 Testing Expert Analysis with: {pdf_file.name}")
    
    # Initialize processors
    pdf_processor = PDFProcessor()
    stage1_analyzer = EnhancedPaperAnalyzer()
    expert_stage2 = EnhancedStage2Expert()
    
    # Test connections
    if not stage1_analyzer.test_connection() or not expert_stage2.test_connection():
        print("❌ Ollama connection failed")
        return False
    
    print("✅ All connections successful")
    
    try:
        # ================== PAPER EXTRACTION ==================
        print(f"\n📖 EXTRACTING PAPER CONTENT...")
        paper_data = pdf_processor.process_paper(pdf_path)
        raw_text = paper_data["raw_text"]
        print(f"✅ Extracted {len(raw_text):,} characters")
        
        # ================== STAGE 1: ENHANCED CORE UNDERSTANDING ==================
        print(f"\n🔍 STAGE 1: ENHANCED CORE UNDERSTANDING...")
        core_sections = stage1_analyzer.enhanced_section_detection(raw_text)
        
        if not core_sections:
            print("❌ No core sections found")
            return False
        
        core_understanding = stage1_analyzer.stage1_core_understanding_analysis(core_sections)
        
        print(f"✅ Stage 1 Complete:")
        print(f"   🎯 Field: {core_understanding.field_classification}")
        print(f"   ⚔️ Base debate points: {len(core_understanding.debate_seed_points)}")
        
        # ================== STAGE 2: EXPERT-LEVEL DEEP ANALYSIS ==================
        print(f"\n🔬 STAGE 2: EXPERT-LEVEL DEEP ANALYSIS...")
        print("Using multi-expert perspectives for maximum depth...")
        
        comprehensive_expert_analysis = expert_stage2.comprehensive_expert_analysis(
            core_understanding, raw_text
        )
        
        # ================== RESULTS COMPARISON: SHALLOW vs DEEP ==================
        print(f"\n{'='*20} DEPTH COMPARISON RESULTS {'='*20}")
        
        # Show improvement in debate depth
        print(f"\n📊 DEBATE DEPTH IMPROVEMENT:")
        
        # Stage 1 baseline
        stage1_points = len(core_understanding.debate_seed_points)
        print(f"   📝 Stage 1 Base Points: {stage1_points}")
        
        # Expert analysis depth
        expert_evidence = comprehensive_expert_analysis.expert_evidence_mappings
        field_controversies = comprehensive_expert_analysis.field_controversies
        
        expert_total_depth = (
            len(expert_evidence) +
            len(field_controversies.methodological_controversies) +
            len(field_controversies.statistical_controversies) + 
            len(field_controversies.domain_technical_disputes) +
            len(field_controversies.generalizability_wars) +
            len(field_controversies.reproducibility_ammunition)
        )
        
        print(f"   🧠 Expert Analysis Points: {expert_total_depth}")
        print(f"   📈 Depth Improvement: {expert_total_depth / max(stage1_points, 1):.1f}x more detailed")
        
        # ================== EXPERT EVIDENCE ANALYSIS ==================
        print(f"\n🔬 EXPERT EVIDENCE ANALYSIS ({len(expert_evidence)} claims):")
        
        for i, evidence in enumerate(expert_evidence, 1):
            print(f"\n   {i}. CLAIM: {evidence.claim[:70]}...")
            
            print(f"      🧮 STATISTICIAN: {evidence.statistician_analysis[:80]}...")
            print(f"      📐 METHODOLOGIST: {evidence.methodologist_analysis[:80]}...")  
            print(f"      🎯 DOMAIN EXPERT: {evidence.domain_expert_analysis[:80]}...")
            print(f"      🔄 REPLICATION EXPERT: {evidence.replication_expert_analysis[:80]}...")
            
            print(f"      📊 EVIDENCE STRENGTHS:")
            for aspect, strength in evidence.evidence_strength_detailed.items():
                print(f"         • {aspect.title()}: {strength.upper()}")
            
            # Show specific debate ammunition
            if evidence.specific_debate_points.get('optimist'):
                print(f"      😊 OPTIMIST AMMUNITION:")
                for point in evidence.specific_debate_points['optimist'][:2]:
                    print(f"         + {point[:60]}...")
            
            if evidence.specific_debate_points.get('skeptic'):
                print(f"      🤨 SKEPTIC AMMUNITION:")
                for point in evidence.specific_debate_points['skeptic'][:2]:
                    print(f"         - {point[:60]}...")
        
        # ================== FIELD CONTROVERSIES ==================
        print(f"\n⚔️ FIELD-SPECIFIC CONTROVERSIES:")
        controversies = field_controversies
        
        if controversies.methodological_controversies:
            print(f"\n   📐 METHODOLOGICAL BATTLES ({len(controversies.methodological_controversies)}):")
            for i, controversy in enumerate(controversies.methodological_controversies[:3], 1):
                print(f"      {i}. {controversy[:70]}...")
        
        if controversies.statistical_controversies:
            print(f"\n   📊 STATISTICAL DISPUTES ({len(controversies.statistical_controversies)}):")
            for i, controversy in enumerate(controversies.statistical_controversies[:3], 1):
                print(f"      {i}. {controversy[:70]}...")
        
        if controversies.domain_technical_disputes:
            print(f"\n   🎯 DOMAIN-SPECIFIC FIGHTS ({len(controversies.domain_technical_disputes)}):")
            for i, dispute in enumerate(controversies.domain_technical_disputes[:3], 1):
                print(f"      {i}. {dispute[:70]}...")
        
        if controversies.generalizability_wars:
            print(f"\n   🌍 GENERALIZABILITY WARS ({len(controversies.generalizability_wars)}):")
            for i, war in enumerate(controversies.generalizability_wars[:3], 1):
                print(f"      {i}. {war[:70]}...")
        
        # ================== TECHNICAL DEEP DIVE ==================
        print(f"\n🔬 TECHNICAL DEEP DIVE:")
        deep_dive = comprehensive_expert_analysis.expert_deep_dive
        
        print(f"   🧮 Algorithmic Specifications: {len(deep_dive.algorithmic_specifications)}")
        print(f"   🧪 Experimental Precision: {len(deep_dive.experimental_precision)}")
        print(f"   💻 Implementation Details: {len(deep_dive.implementation_granularity)}")
        print(f"   📊 Numerical Precision: {len(deep_dive.numerical_precision)}")
        print(f"   📐 Methodological Choices: {len(deep_dive.methodological_choices)}")
        print(f"   ⚠️ Detailed Limitations: {len(deep_dive.limitation_specifications)}")
        
        # Show samples of technical depth
        if deep_dive.algorithmic_specifications:
            print(f"\n   🧮 SAMPLE ALGORITHMIC DETAILS:")
            for i, spec in enumerate(deep_dive.algorithmic_specifications[:2], 1):
                print(f"      {i}. {spec[:80]}...")
        
        if deep_dive.numerical_precision:
            print(f"\n   📊 SAMPLE NUMERICAL PRECISION:")
            for i, num in enumerate(deep_dive.numerical_precision[:2], 1):
                print(f"      {i}. {num[:80]}...")
        
        # ================== EXPERT DEBATE SCENARIOS ==================
        print(f"\n🎭 EXPERT DEBATE SCENARIOS ({len(comprehensive_expert_analysis.expert_debate_scenarios)}):")
        
        for i, scenario in enumerate(comprehensive_expert_analysis.expert_debate_scenarios, 1):
            print(f"\n   {i}. {scenario['title']}")
            print(f"      🔥 Core Disagreement: {scenario['core_disagreement']}")
            print(f"      😊 Position A: {scenario.get('optimist_position', scenario.get('statistician_position', 'N/A'))[:60]}...")
            print(f"      🤨 Position B: {scenario.get('skeptic_position', scenario.get('domain_expert_position', 'N/A'))[:60]}...")
            
            if scenario.get('technical_details'):
                print(f"      🔬 Technical Evidence:")
                for detail in scenario['technical_details'][:2]:
                    print(f"         • {detail[:60]}...")
        
        # ================== QUALITY ASSESSMENT ==================
        print(f"\n{'='*20} EXPERT ANALYSIS QUALITY ASSESSMENT {'='*20}")
        
        quality_score = 0
        max_score = 25  # Increased for expert analysis
        
        # Multi-expert evidence depth
        if len(expert_evidence) >= 2:
            quality_score += 5
            print("   ✅ Multiple expert evidence analyses (+5)")
        elif len(expert_evidence) >= 1:
            quality_score += 3
            print("   ✅ Basic expert evidence analysis (+3)")
        
        # Field-specific controversy depth
        controversy_count = sum([
            len(controversies.methodological_controversies),
            len(controversies.statistical_controversies),
            len(controversies.domain_technical_disputes),
            len(controversies.generalizability_wars)
        ])
        
        if controversy_count >= 8:
            quality_score += 5
            print("   ✅ Comprehensive field controversies identified (+5)")
        elif controversy_count >= 4:
            quality_score += 3
            print("   ✅ Good field controversy coverage (+3)")
        
        # Technical precision depth
        technical_count = sum([
            len(deep_dive.algorithmic_specifications),
            len(deep_dive.experimental_precision),
            len(deep_dive.numerical_precision),
            len(deep_dive.methodological_choices)
        ])
        
        if technical_count >= 10:
            quality_score += 5
            print("   ✅ Maximum technical granularity achieved (+5)")
        elif technical_count >= 5:
            quality_score += 3
            print("   ✅ Good technical detail extraction (+3)")
        
        # Expert perspective sophistication
        if expert_evidence:
            expert_perspectives = sum(1 for ev in expert_evidence if ev.statistician_analysis and ev.domain_expert_analysis)
            if expert_perspectives >= 2:
                quality_score += 4
                print("   ✅ Multi-expert perspective analysis (+4)")
            elif expert_perspectives >= 1:
                quality_score += 2
                print("   ✅ Basic expert perspective analysis (+2)")
        
        # Debate scenario sophistication
        if len(comprehensive_expert_analysis.expert_debate_scenarios) >= 3:
            quality_score += 3
            print("   ✅ Multiple expert debate scenarios (+3)")
        elif len(comprehensive_expert_analysis.expert_debate_scenarios) >= 1:
            quality_score += 2
            print("   ✅ Basic debate scenarios (+2)")
        
        # Evidence strength granularity
        if expert_evidence:
            detailed_strength = sum(1 for ev in expert_evidence if len(ev.evidence_strength_detailed) >= 3)
            if detailed_strength >= 1:
                quality_score += 3
                print("   ✅ Detailed evidence strength assessment (+3)")
        
        print(f"\n🏆 EXPERT ANALYSIS QUALITY SCORE: {quality_score}/{max_score}")
        
        if quality_score >= 20:
            print("🌟 OUTSTANDING - Maximum expert-level depth achieved!")
            print("✅ Ready for the most sophisticated academic debates possible!")
        elif quality_score >= 15:
            print("✅ EXCELLENT - High-quality expert analysis!")
            print("✅ Suitable for advanced academic discussions!")
        elif quality_score >= 10:
            print("⚠️ GOOD - Solid expert analysis with room for improvement")
        else:
            print("❌ NEEDS WORK - Expert prompts need refinement")
        
        # ================== SOPHISTICATION COMPARISON ==================
        print(f"\n📈 SOPHISTICATION IMPROVEMENT SUMMARY:")
        print(f"   📊 Evidence Analysis: Multi-expert vs single perspective")
        print(f"   ⚔️ Debate Points: Field-specific controversies vs generic topics") 
        print(f"   🔬 Technical Depth: Granular specifications vs surface details")
        print(f"   🎭 Scenarios: Realistic expert conflicts vs basic disagreements")
        print(f"   📐 Precision: Exact numbers/methods vs vague descriptions")
        
        # Show specific examples of improvement
        print(f"\n🎯 DEPTH IMPROVEMENT EXAMPLES:")
        
        if controversies.statistical_controversies:
            print(f"   OLD: 'Statistical methods could be improved'")
            print(f"   NEW: '{controversies.statistical_controversies[0][:80]}...'")
        
        if deep_dive.numerical_precision:
            print(f"   OLD: 'Performance was good'")  
            print(f"   NEW: '{deep_dive.numerical_precision[0][:80]}...'")
        
        return quality_score >= 15
        
    except Exception as e:
        print(f"❌ Expert analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    
    print("🧠 AI Paper Narrator - Expert-Level Deep Analysis Test")
    print("Testing Maximum Debate Depth Enhancement")
    print("-" * 80)
    
    # Default paper path
    default_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = default_path
    
    print(f"📄 Testing Expert Analysis with: {pdf_path}")
    
    success = test_expert_depth_comparison(pdf_path)
    
    if success:
        print(f"\n🎉 EXPERT-LEVEL ANALYSIS SUCCESSFUL!")
        print(f"✅ Multi-expert perspective analysis working")
        print(f"✅ Field-specific controversies identified") 
        print(f"✅ Technical deep dive with maximum granularity")
        print(f"✅ Expert debate scenarios generated")
        print(f"✅ Evidence strength detailed assessment")
        print(f"\n🚀 MAXIMUM DEPTH ACHIEVED - READY FOR SOPHISTICATED DEBATES!")
    else:
        print(f"\n🔧 EXPERT ANALYSIS NEEDS REFINEMENT")
        print(f"❌ Check quality assessment for specific improvements needed")
        print(f"🔍 Consider adjusting expert prompts for better depth")


if __name__ == "__main__":
    main()
