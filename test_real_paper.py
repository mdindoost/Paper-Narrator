#!/usr/bin/env python3
"""Test Stage 1 with Real PDF Paper"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append('src')
sys.path.append('.')

# Import existing components and enhanced analyzer
try:
    from pdf_processor import PDFProcessor
    from enhanced_analyzer import EnhancedPaperAnalyzer
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)


def test_real_paper_analysis(pdf_path: str):
    """Test Stage 1 analysis with a real PDF paper"""
    
    print("🔬 Testing Stage 1 with REAL PDF Paper")
    print("=" * 60)
    
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print(f"📄 Loading PDF: {pdf_file.name}")
    
    # Initialize processors
    pdf_processor = PDFProcessor()
    analyzer = EnhancedPaperAnalyzer()
    
    # Test connections
    if not analyzer.test_connection():
        print("❌ Ollama connection failed")
        return False
    
    print("✅ Ollama connection successful")
    
    try:
        # Step 1: Extract text from PDF
        print("\n📖 Step 1: Extracting text from PDF...")
        paper_data = pdf_processor.process_paper(pdf_path)
        raw_text = paper_data["raw_text"]
        
        print(f"✅ Extracted {len(raw_text):,} characters")
        print(f"📊 Text preview: {raw_text[:200]}...")
        
        # Step 2: Enhanced section detection
        print("\n🔍 Step 2: Detecting critical sections...")
        core_sections = analyzer.enhanced_section_detection(raw_text)
        
        print(f"\n📋 Found sections:")
        for section, content in core_sections.items():
            print(f"   ✅ {section}: {len(content)} characters")
            if len(content) > 100:
                print(f"      Preview: {content[:100]}...")
            else:
                print(f"      Content: {content}")
        
        if not core_sections:
            print("❌ No critical sections found!")
            print("🔧 Trying manual section search...")
            
            # Manual fallback - look for common patterns
            text_lower = raw_text.lower()
            
            # Try to find abstract manually
            abstract_start = text_lower.find('abstract')
            if abstract_start > -1:
                abstract_end = text_lower.find('\n\n', abstract_start + 100)
                if abstract_end > -1:
                    abstract = raw_text[abstract_start:abstract_end].strip()
                    core_sections['abstract'] = abstract
                    print(f"   ✅ Manual abstract: {len(abstract)} characters")
            
            # Try to find conclusion manually
            for conclusion_word in ['conclusion', 'conclusions', 'concluding remarks']:
                conclusion_start = text_lower.find(conclusion_word)
                if conclusion_start > -1:
                    conclusion_end = text_lower.find('references', conclusion_start)
                    if conclusion_end == -1:
                        conclusion_end = conclusion_start + 1000  # Take next 1000 chars
                    conclusion = raw_text[conclusion_start:conclusion_end].strip()
                    core_sections['conclusion'] = conclusion
                    print(f"   ✅ Manual conclusion: {len(conclusion)} characters")
                    break
        
        if not core_sections:
            print("❌ Could not find any critical sections in the paper")
            return False
        
        # Step 3: Stage 1 analysis
        print(f"\n🧠 Step 3: Running Stage 1 analysis...")
        print(f"Analyzing {len(core_sections)} sections with enhanced analyzer...")
        
        core_understanding = analyzer.stage1_core_understanding_analysis(core_sections)
        
        # Step 4: Display results
        print(f"\n📊 STAGE 1 ANALYSIS RESULTS")
        print("=" * 50)
        
        print(f"\n🎯 FIELD CLASSIFICATION:")
        print(f"   {core_understanding.field_classification}")
        
        print(f"\n📖 RESEARCH STORY ARC:")
        if core_understanding.research_story_arc:
            for key, value in core_understanding.research_story_arc.items():
                print(f"   • {key.replace('_', ' ').title()}: {value}")
        else:
            print("   ❌ No story elements parsed")
        
        print(f"\n🔍 CONFIDENCE ASSESSMENT:")
        if core_understanding.confidence_assessment:
            for key, value in core_understanding.confidence_assessment.items():
                print(f"   • {key.replace('_', ' ').title()}: {value}")
        else:
            print("   ❌ No confidence elements parsed")
        
        print(f"\n⚔️ DEBATE SEED POINTS ({len(core_understanding.debate_seed_points)}):")
        if core_understanding.debate_seed_points:
            for i, point in enumerate(core_understanding.debate_seed_points, 1):
                print(f"   {i}. {point}")
        else:
            print("   ❌ No debate points generated")
        
        print(f"\n🔧 TECHNICAL ELEMENTS ({len(core_understanding.key_technical_elements)}):")
        if core_understanding.key_technical_elements:
            for i, element in enumerate(core_understanding.key_technical_elements, 1):
                print(f"   {i}. {element}")
        else:
            print("   ❌ No technical elements extracted")
        
        # Quality assessment - Updated for comprehensive analysis
        print(f"\n📈 COMPREHENSIVE QUALITY ASSESSMENT:")
        
        quality_score = 0
        max_score = 15  # Increased for comprehensive evaluation
        
        if core_understanding.field_classification != "General Research":
            quality_score += 2
            print("   ✅ Specific field identified (+2)")
        
        if len(core_understanding.research_story_arc) >= 5:  # Increased expectation
            quality_score += 3
            print("   ✅ Comprehensive research story (+3)")
        elif len(core_understanding.research_story_arc) >= 3:
            quality_score += 2
            print("   ✅ Good research story (+2)")
        
        if len(core_understanding.debate_seed_points) >= 8:  # Target 8+ debate points
            quality_score += 4
            print("   ✅ Excellent debate depth (8+ points) (+4)")
        elif len(core_understanding.debate_seed_points) >= 5:
            quality_score += 3
            print("   ✅ Good debate coverage (5-7 points) (+3)")
        elif len(core_understanding.debate_seed_points) >= 3:
            quality_score += 2
            print("   ✅ Basic debate points (3-4 points) (+2)")
        
        if len(core_understanding.key_technical_elements) >= 6:  # Increased technical depth
            quality_score += 3
            print("   ✅ Comprehensive technical analysis (+3)")
        elif len(core_understanding.key_technical_elements) >= 3:
            quality_score += 2
            print("   ✅ Good technical coverage (+2)")
        
        if len(core_understanding.confidence_assessment) >= 4:  # More detailed confidence analysis
            quality_score += 2
            print("   ✅ Detailed confidence assessment (+2)")
        elif len(core_understanding.confidence_assessment) >= 2:
            quality_score += 1
            print("   ✅ Basic confidence assessment (+1)")
        
        # Bonus points for sophisticated content
        sophisticated_keywords = ['methodology', 'statistical', 'reproducibility', 'generalizability', 'evidence', 'validation']
        if any(keyword in str(core_understanding.debate_seed_points).lower() for keyword in sophisticated_keywords):
            quality_score += 1
            print("   ✅ Sophisticated academic language (+1)")
        
        print(f"\n🏆 COMPREHENSIVE QUALITY SCORE: {quality_score}/{max_score}")
        
        if quality_score >= 12:
            print("🌟 OUTSTANDING - Maximum depth achieved, ready for Stage 2!")
        elif quality_score >= 9:
            print("✅ EXCELLENT - High quality analysis, ready for Stage 2!")
        elif quality_score >= 6:
            print("⚠️ GOOD - Decent analysis, could use more depth")
        else:
            print("❌ NEEDS IMPROVEMENT - Insufficient depth for academic debates")
        
        # Detailed feedback
        print(f"\n📊 DEPTH ANALYSIS:")
        print(f"   📖 Research Story Elements: {len(core_understanding.research_story_arc)}/8 (target: problem, gap, solution, methodology, findings, contributions, significance, implications)")
        print(f"   🔍 Confidence Factors: {len(core_understanding.confidence_assessment)}/7 (target: language, claims, statistics, limitations, uncertainty, reproducibility, generalizability)")
        print(f"   ⚔️ Debate Points: {len(core_understanding.debate_seed_points)}/10+ (target: methodology, evidence, novelty, generalizability, practical, reproducibility, comparison, future work)")
        print(f"   🔧 Technical Elements: {len(core_understanding.key_technical_elements)}/8+ (target: algorithms, metrics, datasets, design, statistics, validation, baselines, complexity)")
        
        # Show sample content quality
        if core_understanding.debate_seed_points:
            print(f"\n🎯 SAMPLE DEBATE POINTS QUALITY:")
            for i, point in enumerate(core_understanding.debate_seed_points[:3], 1):
                point_length = len(point)
                sophistication = sum(1 for word in ['methodology', 'statistical', 'reproducibility', 'generalizability', 'validation', 'evidence', 'baseline', 'control'] if word in point.lower())
                print(f"   {i}. Length: {point_length} chars, Sophistication: {sophistication}/8")
                print(f"      \"{point[:80]}{'...' if len(point) > 80 else ''}\"")
        
        # Next steps based on quality
        print(f"\n🎯 NEXT STEPS:")
        if quality_score >= 9:
            print("   1. ✅ Stage 1 comprehensive analysis working excellently")
            print("   2. 🚀 READY TO IMPLEMENT Stage 2: Evidence Hunting")
            print("   3. 🎭 Connect to personality system for sophisticated debates")
            print("   4. 🎬 Generate expert-level academic discussions")
        elif quality_score >= 6:
            print("   1. 🔧 Minor improvements to increase depth")
            print("   2. 📈 Aim for 8+ debate points and 6+ technical elements")
            print("   3. 🎯 Then move to Stage 2 implementation")
        else:
            print("   1. 🔧 Significant improvements needed")
            print("   2. 📝 Enhance prompts for more comprehensive extraction")
            print("   3. 🤖 Adjust AI parameters for deeper analysis")
            print("   4. 🔄 Re-test before Stage 2")
        
        return quality_score >= 6  # Lowered threshold slightly for comprehensive test
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    
    print("🚀 AI Paper Narrator - Real Paper Testing")
    print("Testing Enhanced Stage 1 Analysis")
    print("-" * 60)
    
    # Default paper path
    default_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = default_path
    
    print(f"📄 Testing with: {pdf_path}")
    
    success = test_real_paper_analysis(pdf_path)
    
    if success:
        print(f"\n🎉 REAL PAPER TEST SUCCESSFUL!")
        print(f"✅ Stage 1 analysis working with real academic papers")
        print(f"🚀 Ready to implement Stage 2: Evidence Hunting")
    else:
        print(f"\n🔧 REAL PAPER TEST NEEDS IMPROVEMENT")
        print(f"❌ Stage 1 analysis needs refinement")
        print(f"🔍 Check the quality assessment above for specific issues")


if __name__ == "__main__":
    main()
