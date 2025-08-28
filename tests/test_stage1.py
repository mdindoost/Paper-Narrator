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
        print(f"📊 Text preview: {raw_text[:5000]}...")
        
        # Step 2: DIRECT section detection on raw text (bypass old processor)
        print("\n🔍 Step 2: Enhanced section detection on raw text...")
        print("(Bypassing old PDF processor section detection)")
        
        # Use enhanced analyzer directly on raw text
        core_sections = analyzer.enhanced_section_detection(raw_text)
        
        print(f"\n📋 Enhanced detection results:")
        for section, content in core_sections.items():
            print(f"   ✅ {section}: {len(content)} characters")
            # Show more preview for debugging
            preview = content.replace('\n', ' ')[:150]
            print(f"      Preview: {preview}...")
        
        if not core_sections:
            print("❌ Enhanced section detection also failed!")
            print("🔧 Trying direct text analysis...")
            
            # Last resort: analyze the raw text directly
            core_sections = {
                'full_text': raw_text[:5000]  # First 5000 chars
            }
            print(f"   ⚠️ Using first 5000 characters as fallback")
        
        elif len(core_sections) == 1 and 'title' in core_sections:
            print("⚠️ Only title found - adding text chunks for analysis")
            # Add some text chunks for analysis
            chunks = [raw_text[i:i+2000] for i in range(0, len(raw_text), 2000)]
            for i, chunk in enumerate(chunks[:3]):  # First 3 chunks
                if any(word in chunk.lower() for word in ['abstract', 'introduction', 'method', 'result']):
                    core_sections[f'chunk_{i}'] = chunk
        
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
        
        # Quality assessment
        print(f"\n📈 QUALITY ASSESSMENT:")
        
        quality_score = 0
        if core_understanding.field_classification != "General Research":
            quality_score += 2
            print("   ✅ Specific field identified (+2)")
        
        if len(core_understanding.research_story_arc) >= 3:
            quality_score += 2
            print("   ✅ Complete research story (+2)")
        
        if len(core_understanding.debate_seed_points) >= 3:
            quality_score += 3
            print("   ✅ Multiple debate points generated (+3)")
        
        if len(core_understanding.key_technical_elements) >= 2:
            quality_score += 2
            print("   ✅ Technical elements identified (+2)")
        
        if len(core_understanding.confidence_assessment) >= 2:
            quality_score += 1
            print("   ✅ Confidence assessment complete (+1)")
        
        print(f"\n🏆 OVERALL QUALITY SCORE: {quality_score}/10")
        
        if quality_score >= 7:
            print("✅ EXCELLENT - Ready for Stage 2!")
        elif quality_score >= 5:
            print("⚠️ GOOD - Minor improvements needed")
        else:
            print("❌ POOR - Significant improvements needed")
        
        # Next steps
        print(f"\n🎯 NEXT STEPS:")
        if quality_score >= 5:
            print("   1. ✅ Stage 1 working well")
            print("   2. 🚀 Implement Stage 2: Full paper analysis")
            print("   3. 🎭 Connect to personality system")
            print("   4. 🎬 Generate sophisticated debates")
        else:
            print("   1. 🔧 Improve section detection")
            print("   2. 📝 Enhance parsing logic")
            print("   3. 🤖 Adjust AI prompts")
            print("   4. 🔄 Re-test with this paper")
        
        return quality_score >= 5
        
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