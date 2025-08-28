#!/usr/bin/env python3
"""
Full Transparency Debug Test
Save as: test_debug_full_transparency.py (in root directory)

Shows EXACTLY what we ask the AI, what it responds, and how we parse it.
Complete transparency for debugging analysis issues.
"""

import sys
import os
import re  # Added missing import
from pathlib import Path
import time

# Add src directory to path
sys.path.append('src')
sys.path.append('.')

# Import components
try:
    from pdf_processor import PDFProcessor
    from enhanced_analyzer import EnhancedPaperAnalyzer
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


class DebugEnhancedAnalyzer(EnhancedPaperAnalyzer):
    """Debug version that shows all prompts and responses"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debug_step = 0
    
    def debug_step_separator(self, title: str):
        """Visual separator for debug steps"""
        self.debug_step += 1
        print(f"\n{'='*100}")
        print(f"🔍 DEBUG STEP {self.debug_step}: {title}")
        print(f"{'='*100}")
    
    def _call_ollama(self, prompt: str, max_length: int = 2000) -> str:
        """Debug version that shows full prompt and response"""
        
        self.debug_step_separator("OLLAMA API CALL")
        
        print(f"📤 PROMPT BEING SENT TO AI:")
        print(f"{'─'*80}")
        print(prompt)
        print(f"{'─'*80}")
        print(f"📊 Prompt length: {len(prompt)} characters")
        print(f"📊 Max response length: {max_length}")
        
        print(f"\n⏳ Sending to Ollama... (this may take 30-60 seconds)")
        start_time = time.time()
        
        # Call parent method
        response = super()._call_ollama(prompt, max_length)
        
        elapsed_time = time.time() - start_time
        
        print(f"\n📥 AI RESPONSE RECEIVED:")
        print(f"{'─'*80}")
        print(response)
        print(f"{'─'*80}")
        print(f"📊 Response length: {len(response)} characters")
        print(f"⏱️ Response time: {elapsed_time:.1f} seconds")
        
        if "Error" in response:
            print(f"❌ ERROR DETECTED IN RESPONSE!")
        else:
            print(f"✅ Response received successfully")
        
        input(f"\n⏸️  PRESS ENTER to continue to next step...")
        
        return response
    
    def debug_enhanced_section_detection(self, text: str):
        """Debug version of section detection"""
        
        self.debug_step_separator("ENHANCED SECTION DETECTION")
        
        print(f"📄 INPUT TEXT INFO:")
        print(f"   Total length: {len(text):,} characters")
        print(f"   First 200 chars: {text[:200]}")
        print(f"   Last 200 chars: {text[-200:]}")
        
        print(f"\n🔍 SEARCHING FOR SECTIONS...")
        
        # Call parent method but intercept each section found
        sections = {}
        text_lower = text.lower()
        
        # Manual section detection with debug output
        section_searches = {
            'title': 'Paper Title',
            'abstract': 'Abstract Section', 
            'conclusion': 'Conclusion Section',
            'future_work': 'Future Work Section'
        }
        
        for section_name, description in section_searches.items():
            print(f"\n🔎 SEARCHING FOR: {description}")
            
            if section_name == 'title':
                # Title extraction logic with debug
                print(f"   Method: Looking for title before authors/institutions")
                
                # Look for author pattern
                author_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+|Computer Science Department|University)', text[:1000])
                if author_match:
                    potential_title = text[:author_match.start()].strip()
                    potential_title = re.sub(r'[*†‡]', '', potential_title).strip()
                    if 20 <= len(potential_title) <= 200:
                        sections[section_name] = potential_title
                        print(f"   ✅ FOUND: {potential_title}")
                        print(f"   📍 Location: Characters 0-{author_match.start()}")
                    else:
                        print(f"   ❌ Title candidate too short/long: {len(potential_title)} chars")
                else:
                    print(f"   ❌ No author pattern found for title extraction")
            
            elif section_name == 'abstract':
                print(f"   Method: Looking for 'abstract' keyword + content")
                abstract_pos = text_lower.find('abstract')
                if abstract_pos >= 0:
                    print(f"   📍 Found 'abstract' at position {abstract_pos}")
                    
                    # Extract content after 'abstract'
                    start = abstract_pos + len('abstract')
                    while start < len(text) and text[start] in ' :\n\t':
                        start += 1
                    
                    # Find end
                    end_keywords = ['introduction', 'keywords', '1.', 'method']
                    end = len(text)
                    for keyword in end_keywords:
                        keyword_pos = text_lower.find(keyword, start)
                        if keyword_pos != -1:
                            end = min(end, keyword_pos)
                    
                    # Limit length
                    end = min(end, start + 2000)
                    
                    if end > start:
                        abstract_content = text[start:end].strip()
                        if len(abstract_content) > 50:
                            sections[section_name] = abstract_content
                            print(f"   ✅ FOUND: {len(abstract_content)} characters")
                            print(f"   📍 Location: Characters {start}-{end}")
                            print(f"   📄 Preview: {abstract_content[:100]}...")
                        else:
                            print(f"   ❌ Abstract content too short: {len(abstract_content)} chars")
                    else:
                        print(f"   ❌ Invalid abstract boundaries: start={start}, end={end}")
                else:
                    print(f"   ❌ Keyword 'abstract' not found in text")
            
            elif section_name == 'conclusion':
                print(f"   Method: Looking for 'conclusion' keyword + content")
                conclusion_keywords = ['conclusion', 'conclusions', 'concluding remarks']
                
                found = False
                for keyword in conclusion_keywords:
                    keyword_pos = text_lower.find(keyword)
                    if keyword_pos >= 0:
                        print(f"   📍 Found '{keyword}' at position {keyword_pos}")
                        
                        start = keyword_pos + len(keyword)
                        while start < len(text) and text[start] in ' :\n\t':
                            start += 1
                        
                        # Find end
                        end_keywords = ['references', 'acknowledgments', 'appendix']
                        end = len(text)
                        for end_keyword in end_keywords:
                            end_pos = text_lower.find(end_keyword, start)
                            if end_pos != -1:
                                end = min(end, end_pos)
                        
                        end = min(end, start + 2000)
                        
                        if end > start:
                            conclusion_content = text[start:end].strip()
                            if len(conclusion_content) > 50:
                                sections[section_name] = conclusion_content
                                print(f"   ✅ FOUND: {len(conclusion_content)} characters")
                                print(f"   📍 Location: Characters {start}-{end}")
                                print(f"   📄 Preview: {conclusion_content[:100]}...")
                                found = True
                                break
                
                if not found:
                    print(f"   ❌ No conclusion section found")
            
            elif section_name == 'future_work':
                print(f"   Method: Looking for 'future work' keywords")
                future_keywords = ['future work', 'future research', 'future directions']
                
                found = False
                for keyword in future_keywords:
                    keyword_pos = text_lower.find(keyword)
                    if keyword_pos >= 0:
                        print(f"   📍 Found '{keyword}' at position {keyword_pos}")
                        
                        start = keyword_pos + len(keyword)
                        end = min(len(text), start + 1000)
                        
                        future_content = text[start:end].strip()
                        if len(future_content) > 50:
                            sections[section_name] = future_content
                            print(f"   ✅ FOUND: {len(future_content)} characters")
                            print(f"   📄 Preview: {future_content[:100]}...")
                            found = True
                            break
                
                if not found:
                    print(f"   ❌ No future work section found")
        
        print(f"\n📊 SECTION DETECTION SUMMARY:")
        for section, content in sections.items():
            print(f"   ✅ {section}: {len(content)} characters")
        
        if not sections:
            print(f"   ❌ NO SECTIONS FOUND!")
        
        input(f"\n⏸️  PRESS ENTER to continue...")
        
        return sections
    
    def debug_stage1_analysis(self, core_sections):
        """Debug version of Stage 1 analysis"""
        
        self.debug_step_separator("STAGE 1 CORE UNDERSTANDING ANALYSIS")
        
        print(f"📋 INPUT SECTIONS FOR ANALYSIS:")
        for section, content in core_sections.items():
            print(f"   {section.upper()}: {len(content)} characters")
            print(f"   Preview: {content[:150]}...")
            print()
        
        # Show the exact prompt that will be sent
        print(f"🎯 ABOUT TO GENERATE COMPREHENSIVE ANALYSIS PROMPT...")
        
        # Call parent method which will trigger our debug _call_ollama
        result = self.stage1_core_understanding_analysis(core_sections)
        
        return result
    
    def debug_parse_response(self, response: str, title: str):
        """Debug the parsing process"""
        
        self.debug_step_separator(f"PARSING: {title}")
        
        print(f"📥 RESPONSE TO PARSE:")
        print(f"{'─'*80}")
        print(response)
        print(f"{'─'*80}")
        
        print(f"\n🔍 PARSING PROCESS:")
        lines = response.split('\n')
        print(f"   Total lines: {len(lines)}")
        
        current_section = None
        parsed_data = {}
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            if not line_stripped:
                continue
            
            print(f"   Line {i+1}: {line_stripped}")
            
            # Check for section headers
            line_upper = line_stripped.upper()
            if any(keyword in line_upper for keyword in ['RESEARCH STORY', 'STORY ARC']):
                current_section = 'story'
                print(f"      📖 DETECTED SECTION: Research Story")
                continue
            elif any(keyword in line_upper for keyword in ['CONFIDENCE', 'ASSESSMENT']):
                current_section = 'confidence'
                print(f"      🔍 DETECTED SECTION: Confidence Assessment")
                continue
            elif any(keyword in line_upper for keyword in ['FIELD', 'CLASSIFICATION']):
                current_section = 'field'
                print(f"      🎯 DETECTED SECTION: Field Classification")
                continue
            elif any(keyword in line_upper for keyword in ['TECHNICAL', 'ELEMENTS']):
                current_section = 'technical'
                print(f"      🔧 DETECTED SECTION: Technical Elements")
                continue
            elif any(keyword in line_upper for keyword in ['DEBATE', 'SEED']):
                current_section = 'debate'
                print(f"      ⚔️ DETECTED SECTION: Debate Points")
                continue
            
            # Parse content based on current section
            if current_section:
                print(f"      📝 PARSING IN SECTION: {current_section}")
                
                if ':' in line_stripped:
                    key, value = line_stripped.split(':', 1)
                    key_clean = key.strip('- *').lower().replace(' ', '_')
                    value_clean = value.strip()
                    print(f"         KEY: {key_clean}")
                    print(f"         VALUE: {value_clean}")
                    
                    if current_section not in parsed_data:
                        parsed_data[current_section] = {}
                    parsed_data[current_section][key_clean] = value_clean
                
                elif line_stripped.startswith(('-', '•', '*')) and len(line_stripped) > 20:
                    point = line_stripped.strip('- •*').strip()
                    print(f"         BULLET POINT: {point}")
                    
                    if current_section not in parsed_data:
                        parsed_data[current_section] = []
                    if not isinstance(parsed_data[current_section], list):
                        parsed_data[current_section] = []
                    parsed_data[current_section].append(point)
        
        print(f"\n📊 PARSING RESULTS:")
        for section, content in parsed_data.items():
            if isinstance(content, dict):
                print(f"   {section.upper()}: {len(content)} key-value pairs")
                for key, value in content.items():
                    print(f"      {key}: {value[:60]}{'...' if len(value) > 60 else ''}")
            elif isinstance(content, list):
                print(f"   {section.upper()}: {len(content)} items")
                for item in content:
                    print(f"      • {item[:60]}{'...' if len(item) > 60 else ''}")
        
        input(f"\n⏸️  PRESS ENTER to continue...")
        
        return parsed_data


def test_full_transparency_debug(pdf_path: str):
    """Test with complete transparency and debug output"""
    
    print("🔍 FULL TRANSPARENCY DEBUG TEST")
    print("See exactly what we ask the AI and what it responds")
    print("=" * 100)
    
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print(f"📄 Paper: {pdf_file.name}")
    print(f"📍 Path: {pdf_path}")
    
    # Initialize debug processors
    pdf_processor = PDFProcessor()
    debug_analyzer = DebugEnhancedAnalyzer()
    
    # Test connection
    if not debug_analyzer.test_connection():
        print("❌ Ollama connection failed")
        return False
    
    print("✅ Ollama connection successful")
    
    try:
        # ================== PDF EXTRACTION DEBUG ==================
        debug_analyzer.debug_step_separator("PDF TEXT EXTRACTION")
        
        print("📖 Extracting text from PDF...")
        paper_data = pdf_processor.process_paper(pdf_path)
        raw_text = paper_data["raw_text"]
        
        print(f"✅ Extraction complete:")
        print(f"   📊 Total characters: {len(raw_text):,}")
        print(f"   📊 Total words (approx): {len(raw_text.split()):,}")
        print(f"   📊 PDF sections found: {list(paper_data['sections'].keys())}")
        print(f"   📊 Processing chunks: {paper_data['metadata']['num_chunks']}")
        
        print(f"\n📄 FULL TEXT PREVIEW (First 500 characters):")
        print(f"{'─'*80}")
        print(raw_text[:500])
        print(f"{'─'*80}")
        
        print(f"\n📄 FULL TEXT PREVIEW (Last 500 characters):")
        print(f"{'─'*80}")
        print(raw_text[-500:])
        print(f"{'─'*80}")
        
        input(f"\n⏸️  PRESS ENTER to continue to section detection...")
        
        # ================== SECTION DETECTION DEBUG ==================
        core_sections = debug_analyzer.debug_enhanced_section_detection(raw_text)
        
        if not core_sections:
            print("❌ No core sections found - cannot continue analysis")
            return False
        
        # ================== STAGE 1 ANALYSIS DEBUG ==================
        core_understanding = debug_analyzer.debug_stage1_analysis(core_sections)
        
        # ================== FINAL RESULTS WITH SOURCES ==================
        debug_analyzer.debug_step_separator("FINAL RESULTS WITH SOURCES")
        
        print(f"📊 COMPLETE ANALYSIS RESULTS:")
        print(f"{'─'*80}")
        
        print(f"\n🎯 FIELD CLASSIFICATION:")
        print(f"   Result: {core_understanding.field_classification}")
        print(f"   Source: AI analysis of sections {list(core_sections.keys())}")
        
        print(f"\n📖 RESEARCH STORY ARC ({len(core_understanding.research_story_arc)} elements):")
        for key, value in core_understanding.research_story_arc.items():
            print(f"   {key}: {value}")
        
        print(f"\n🔍 CONFIDENCE ASSESSMENT ({len(core_understanding.confidence_assessment)} factors):")
        for key, value in core_understanding.confidence_assessment.items():
            print(f"   {key}: {value}")
        
        print(f"\n⚔️ DEBATE POINTS ({len(core_understanding.debate_seed_points)} points):")
        for i, point in enumerate(core_understanding.debate_seed_points, 1):
            print(f"   {i}. {point}")
        
        print(f"\n🔧 TECHNICAL ELEMENTS ({len(core_understanding.key_technical_elements)} elements):")
        for i, element in enumerate(core_understanding.key_technical_elements, 1):
            print(f"   {i}. {element}")
        
        # ================== ANALYSIS VALIDATION ==================
        debug_analyzer.debug_step_separator("ANALYSIS VALIDATION")
        
        print(f"🔍 CHECKING IF ANALYSIS MATCHES YOUR PAPER...")
        
        # Check field classification
        print(f"\n🎯 FIELD CLASSIFICATION CHECK:")
        print(f"   AI Result: {core_understanding.field_classification}")
        print(f"   Does this match your paper? (You mentioned it's not relevant)")
        
        # Show what drove this classification
        if core_sections.get('abstract'):
            abstract_keywords = core_sections['abstract'].lower()
            ml_keywords = ['machine learning', 'neural', 'deep learning', 'algorithm', 'model']
            network_keywords = ['network', 'graph', 'node', 'edge', 'community']
            
            ml_count = sum(1 for kw in ml_keywords if kw in abstract_keywords)
            network_count = sum(1 for kw in network_keywords if kw in abstract_keywords)
            
            print(f"   ML keywords found in abstract: {ml_count}")
            print(f"   Network keywords found in abstract: {network_count}")
            print(f"   This likely drove the 'Machine Learning - Network Science' classification")
        
        # Check debate points relevance
        print(f"\n⚔️ DEBATE POINTS RELEVANCE CHECK:")
        if core_understanding.debate_seed_points:
            print(f"   Number of debate points: {len(core_understanding.debate_seed_points)}")
            print(f"   Do these points relate to your paper's actual content?")
            for i, point in enumerate(core_understanding.debate_seed_points[:3], 1):
                print(f"   {i}. {point[:100]}...")
        else:
            print(f"   ❌ NO DEBATE POINTS GENERATED - This is a problem!")
        
        print(f"\n📝 RECOMMENDATIONS FOR IMPROVEMENT:")
        if core_understanding.field_classification != "General Research" and "not relevant" in input("Is the field classification relevant to your paper? (yes/no): ").lower():
            print(f"   🔧 Field classification is wrong - need to improve prompts")
        
        if len(core_understanding.debate_seed_points) < 5:
            print(f"   🔧 Too few debate points - need deeper analysis")
        
        if len(core_understanding.key_technical_elements) < 3:
            print(f"   🔧 Insufficient technical details - need better extraction")
        
        return True
        
    except Exception as e:
        print(f"❌ Debug test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main debug function with user interaction"""
    
    print("🔍 AI Paper Narrator - FULL TRANSPARENCY DEBUG")
    print("Complete visibility into prompts, responses, and parsing")
    print("-" * 100)
    
    # Default paper path
    default_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = default_path
    
    print(f"📄 Debug testing with: {pdf_path}")
    print(f"\n⚠️  This test will show you EVERYTHING:")
    print(f"   • Exact prompts sent to AI")
    print(f"   • Complete AI responses")
    print(f"   • Step-by-step parsing")
    print(f"   • Source of every piece of information")
    print(f"   • Interactive pauses for review")
    
    confirm = input(f"\n❓ Ready to start comprehensive debug? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Debug cancelled.")
        return
    
    success = test_full_transparency_debug(pdf_path)
    
    if success:
        print(f"\n✅ DEBUG TEST COMPLETED!")
        print(f"Now you can see exactly where each piece of analysis comes from")
        print(f"Use this information to identify and fix any issues")
    else:
        print(f"\n❌ DEBUG TEST HAD ISSUES")
        print(f"Review the detailed output above to identify problems")


if __name__ == "__main__":
    main()