"""Enhanced Two-Stage Paper Analyzer - Stage 1: Core Understanding"""

import requests
import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class CoreUnderstanding:
    """Structure for Stage 1 analysis results"""
    research_story_arc: Dict[str, str]
    confidence_assessment: Dict[str, str]
    debate_seed_points: List[str]
    field_classification: str
    key_technical_elements: List[str]


class EnhancedPaperAnalyzer:
    """Two-stage paper analyzer with academic-grade depth"""
    
    def __init__(self, model_name: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
    
    def _call_ollama(self, prompt: str, max_length: int = 2000) -> str:
        """Enhanced Ollama API call with longer responses for deep analysis"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.6,  # Lower temperature for more focused analysis
                "top_p": 0.9,
                "num_predict": max_length
            }
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=300)  # Longer timeout
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except Exception as e:
            return f"[Analysis Error: {str(e)}]"
    
    def enhanced_section_detection(self, text: str) -> Dict[str, str]:
        """ROBUST section detection that handles poorly formatted PDFs"""
        
        sections = {}
        text_lower = text.lower()
        
        print(f"🔍 ROBUST Section Detection - Text length: {len(text)}")
        print(f"📄 First 300 chars: {text[:300]}")
        
        # ROBUST patterns that work with continuous text (no line breaks required)
        robust_patterns = {
            'title': [
                # Extract from beginning until authors/institution
                r'^(.*?)(?=\s*(?:authors?|university|college|institute|department|\*|abstract))',
                # Extract first substantial line
                r'^([^.!?]{20,200}?)(?=\s*[A-Z][a-z]+ [A-Z][a-z]+)',  # Before author names
            ],
            'abstract': [
                # Most robust - find "Abstract" followed by content until next major section
                r'\babstract\b[:\s]*(.*?)(?=\s*(?:keywords?|introduction|1\.|method|algorithm|background|related work|motivation))',
                # Alternative - until numbered section
                r'\babstract\b[:\s]*(.*?)(?=\s*\d+\.?\s*[A-Z])',
                # Simple version - next 1000 chars after "abstract"
                r'\babstract\b[:\s]*(.{200,1500}?)(?=\s*(?:keywords?|introduction|1\.))',
            ],
            'conclusion': [
                # Find conclusion section content
                r'\b(?:conclusions?|concluding remarks?)\b[:\s]*(.*?)(?=\s*(?:references?|acknowledgments?|appendix|bibliography))',
                # Until references section
                r'\b(?:conclusions?)\b[:\s]*(.*?)(?=\s*references?)',
                # Simple version
                r'\b(?:conclusions?)\b[:\s]*(.{200,1500}?)(?=\s*(?:references?|acknowledgments?))',
            ],
            'future_work': [
                # Future work sections
                r'\b(?:future work|future research|future directions?)\b[:\s]*(.*?)(?=\s*(?:conclusions?|references?|acknowledgments?))',
                # Within conclusion, look for future work
                r'(?:future work|future research)[:\s]*([^.]*(?:\.[^.]*){1,3})',
            ]
        }
        
        # Try robust extraction
        for section_name, patterns in robust_patterns.items():
            section_text = self._robust_extract_section(text, text_lower, patterns)
            if section_text:
                cleaned = self._clean_section_text(section_text)
                if len(cleaned) > 50:  # Ensure substantial content
                    sections[section_name] = cleaned
                    print(f"✅ ROBUST: Found {section_name}: {len(cleaned)} characters")
                    print(f"   Preview: {cleaned[:100]}...")
        
        # FALLBACK: Manual keyword search for critical sections
        if 'abstract' not in sections:
            abstract_text = self._manual_keyword_extract(text, 'abstract', next_keywords=['introduction', 'keywords', '1.'])
            if abstract_text:
                sections['abstract'] = abstract_text
                print(f"✅ MANUAL: Found abstract: {len(abstract_text)} characters")
        
        if 'conclusion' not in sections:
            conclusion_text = self._manual_keyword_extract(text, 'conclusion', next_keywords=['references', 'acknowledgments', 'appendix'])
            if conclusion_text:
                sections['conclusion'] = conclusion_text
                print(f"✅ MANUAL: Found conclusion: {len(conclusion_text)} characters")
        
        # Extract title from beginning if not found
        if 'title' not in sections:
            # Look for title in first part before authors
            title_candidates = []
            
            # Method 1: Before author pattern
            author_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+|Computer Science Department|University)', text[:1000])
            if author_match:
                potential_title = text[:author_match.start()].strip()
                # Clean up
                potential_title = re.sub(r'[*†‡]', '', potential_title).strip()
                if 20 <= len(potential_title) <= 200:
                    title_candidates.append(potential_title)
            
            # Method 2: Look for longest meaningful line in first 500 chars
            for line in text[:500].split('.'):
                line = line.strip()
                if 20 <= len(line) <= 150 and not any(word in line.lower() for word in ['university', 'department', 'email', 'abstract']):
                    title_candidates.append(line)
            
            if title_candidates:
                # Pick the longest reasonable candidate
                best_title = max(title_candidates, key=len)
                sections['title'] = self._clean_section_text(best_title)
                print(f"✅ EXTRACTED: title: {sections['title']}")
        
        print(f"📊 ROBUST Detection Results: {list(sections.keys())}")
        return sections
    
    def _robust_extract_section(self, text: str, text_lower: str, patterns: List[str]) -> Optional[str]:
        """Robust extraction that handles continuous text"""
        for pattern in patterns:
            try:
                matches = list(re.finditer(pattern, text_lower, re.DOTALL | re.IGNORECASE))
                if matches:
                    match = matches[0]
                    if len(match.groups()) > 0:
                        # Extract from original text to preserve case
                        start = match.start(1)
                        end = match.end(1)
                        extracted = text[start:end].strip()
                        if len(extracted) > 50:  # Ensure substantial content
                            return extracted
            except Exception as e:
                print(f"⚠️ Pattern error: {e}")
                continue
        return None
    
    def _manual_keyword_extract(self, text: str, keyword: str, next_keywords: List[str], max_length: int = 2000) -> Optional[str]:
        """Manual extraction by finding keyword and extracting until next major section"""
        text_lower = text.lower()
        
        # Find the keyword
        keyword_pos = text_lower.find(keyword.lower())
        if keyword_pos == -1:
            return None
        
        # Start after the keyword (skip the keyword itself)
        start = keyword_pos + len(keyword)
        
        # Skip any immediate punctuation/whitespace
        while start < len(text) and text[start] in ' :\n\t':
            start += 1
        
        # Find the end by looking for next major section
        end = len(text)
        for next_keyword in next_keywords:
            next_pos = text_lower.find(next_keyword.lower(), start)
            if next_pos != -1:
                end = min(end, next_pos)
        
        # Limit to reasonable length
        end = min(end, start + max_length)
        
        if end > start:
            extracted = text[start:end].strip()
            if len(extracted) > 50:
                return extracted
        
        return None
    
    def _extract_section_with_patterns(self, text: str, text_lower: str, patterns: List[str]) -> Optional[str]:
        """Extract section using multiple patterns"""
        for pattern in patterns:
            matches = list(re.finditer(pattern, text_lower, re.DOTALL | re.MULTILINE | re.IGNORECASE))
            if matches:
                match = matches[0]
                if len(matches[0].groups()) > 0:
                    # Extract from original text to preserve case
                    start = match.start(1)
                    end = match.end(1)
                    return text[start:end].strip()
                else:
                    # Take content after the header
                    start = match.end()
                    # Find end by looking for next major section
                    end_patterns = [r'\n\s*(?:\d+\.|\b(?:introduction|method|result|discussion|reference)\b)']
                    for end_pattern in end_patterns:
                        end_match = re.search(end_pattern, text_lower[start:], re.IGNORECASE)
                        if end_match:
                            end = start + end_match.start()
                            break
                    else:
                        end = min(start + 2000, len(text))  # Limit to reasonable length
                    
                    return text[start:end].strip()
        return None
    
    def _clean_section_text(self, text: str) -> str:
        """Clean extracted section text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove page numbers and headers
        text = re.sub(r'\n\d+\n', '\n', text)
        # Remove author information patterns
        text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\d+\b', '', text)
        return text.strip()
    
    def stage1_core_understanding_analysis(self, core_sections: Dict[str, str]) -> CoreUnderstanding:
        """Stage 1: Deep analysis of core sections only"""
        
        print("🔍 Stage 1: Analyzing core sections for deep understanding...")
        
        # Prepare the core content
        core_content = ""
        for section in ['title', 'abstract', 'conclusion', 'future_work']:
            if section in core_sections:
                core_content += f"\n\n{section.upper()}:\n{core_sections[section]}"
        
        if not core_content.strip():
            raise ValueError("No core sections found for analysis")
        
        # Stage 1 Analysis Prompt - Academic Grade
        stage1_prompt = f"""You are an expert academic researcher and peer reviewer. Analyze ONLY the title, abstract, conclusion, and future works sections of this research paper. Provide a deep, critical analysis following this EXACT structure:

CORE SECTIONS TO ANALYZE:
{core_content}

REQUIRED ANALYSIS STRUCTURE:

**1. RESEARCH STORY ARC:**
- Core Problem: [What specific problem does this address?]
- Claimed Solution: [What approach/methodology do they propose?] 
- Key Findings: [What are their main results/contributions?]
- Claimed Significance: [Why do they say this matters?]

**2. CONFIDENCE ASSESSMENT:**
- Author Confidence Level: [How confident are they in their claims? Quote specific language]
- Acknowledged Limitations: [What gaps do they admit in future works?]
- Language Analysis: [Are they using modest language or making strong claims?]
- Overclaim Detection: [Any claims that seem stronger than likely evidence?]

**3. FIELD CLASSIFICATION:**
- Primary Domain: [Specific field, not just "Computer Science" but "Machine Learning - Natural Language Processing"]
- Required Expertise: [What specific knowledge would experts need to evaluate this?]
- Current Field Debates: [What ongoing controversies in this field does this touch on?]

**4. TECHNICAL ELEMENTS:**
- Methodology Type: [Experimental, theoretical, computational, etc.]
- Key Technical Decisions: [What methodological choices did they make?]
- Measurable Claims: [Any specific numbers, percentages, or metrics mentioned?]
- Scope Boundaries: [What are the stated limits of their work?]

**5. DEBATE SEED POINTS:**
- Methodology Concerns: [What could skeptics criticize about their approach?]
- Evidence Gaps: [What's missing between claims and likely supporting evidence?]
- Scope Disputes: [Where might experts disagree about generalizability?]
- Innovation Claims: [Are their novelty claims justified or overstated?]

Be specific, quote exact phrases, and provide evidence-based analysis. Focus on generating sophisticated debate points that academic experts would actually argue about."""

        # Get the analysis
        analysis_response = self._call_ollama(stage1_prompt, max_length=2500)
        
        # Parse the structured response
        parsed_analysis = self._parse_stage1_response(analysis_response)
        
        print(f"✅ Stage 1 Complete: {parsed_analysis.field_classification}")
        return parsed_analysis
    
    def _parse_stage1_response(self, response: str) -> CoreUnderstanding:
        """Parse the structured Stage 1 response - FIXED"""
        
        print("🔍 DEBUG: Parsing AI response...")
        print(f"Response length: {len(response)} characters")
        print("="*50)
        print(response[:500] + "..." if len(response) > 500 else response)
        print("="*50)
        
        # Initialize structures
        research_story = {}
        confidence_assessment = {}
        debate_points = []
        field_classification = "General Research"
        technical_elements = []
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # More flexible section detection
            line_upper = line.upper()
            
            if any(keyword in line_upper for keyword in ['RESEARCH STORY', 'STORY ARC']):
                current_section = 'story'
                print(f"📖 Found story section: {line}")
                continue
            elif any(keyword in line_upper for keyword in ['CONFIDENCE', 'ASSESSMENT']):
                current_section = 'confidence'
                print(f"🔍 Found confidence section: {line}")
                continue
            elif any(keyword in line_upper for keyword in ['FIELD', 'CLASSIFICATION', 'DOMAIN']):
                current_section = 'field'
                print(f"🎯 Found field section: {line}")
                continue
            elif any(keyword in line_upper for keyword in ['TECHNICAL', 'ELEMENTS']):
                current_section = 'technical'
                print(f"🔧 Found technical section: {line}")
                continue
            elif any(keyword in line_upper for keyword in ['DEBATE', 'SEED']):
                current_section = 'debate'
                print(f"⚔️ Found debate section: {line}")
                continue
            
            # Parse content - more flexible patterns
            if current_section == 'story':
                if ':' in line and any(word in line.lower() for word in ['problem', 'solution', 'finding', 'significance']):
                    key, value = line.split(':', 1)
                    key_clean = key.strip('- *').lower().replace(' ', '_')
                    research_story[key_clean] = value.strip()
                    print(f"  📝 Story: {key_clean} = {value[:50]}")
            
            elif current_section == 'confidence':
                if ':' in line and any(word in line.lower() for word in ['confidence', 'limitation', 'language', 'claim']):
                    key, value = line.split(':', 1)
                    key_clean = key.strip('- *').lower().replace(' ', '_')
                    confidence_assessment[key_clean] = value.strip()
                    print(f"  🔍 Confidence: {key_clean} = {value[:50]}")
            
            elif current_section == 'field':
                if 'domain' in line.lower() and ':' in line:
                    field_classification = line.split(':', 1)[1].strip()
                    print(f"  🎯 Field: {field_classification}")
                elif line.startswith(('-', '•', '*')) and len(line) > 15:
                    element = line.strip('- •*').strip()
                    technical_elements.append(element)
                    print(f"  🔧 Tech element: {element[:50]}")
            
            elif current_section == 'technical':
                if line.startswith(('-', '•', '*')) and len(line) > 15:
                    element = line.strip('- •*').strip()
                    technical_elements.append(element)
                    print(f"  🔧 Tech element: {element[:50]}")
            
            elif current_section == 'debate':
                if line.startswith(('-', '•', '*')) and len(line) > 15:
                    point = line.strip('- •*').strip()
                    debate_points.append(point)
                    print(f"  ⚔️ Debate point: {point[:50]}")
        
        print(f"\n📊 PARSING RESULTS:")
        print(f"  Story elements: {len(research_story)}")
        print(f"  Confidence elements: {len(confidence_assessment)}")
        print(f"  Debate points: {len(debate_points)}")
        print(f"  Technical elements: {len(technical_elements)}")
        print(f"  Field: {field_classification}")
        
        return CoreUnderstanding(
            research_story_arc=research_story,
            confidence_assessment=confidence_assessment,
            debate_seed_points=debate_points,
            field_classification=field_classification,
            key_technical_elements=technical_elements
        )
    
    def test_connection(self) -> bool:
        """Test Ollama connection"""
        try:
            test_response = self._call_ollama("Hello", max_length=10)
            return len(test_response) > 0 and "Error" not in test_response
        except:
            return False


# Test function for Stage 1
def test_stage1_analysis():
    """Test the Stage 1 core understanding analysis"""
    
    print("🧪 Testing Stage 1: Core Understanding Analysis")
    print("=" * 60)
    
    analyzer = EnhancedPaperAnalyzer()
    
    # Test connection
    if not analyzer.test_connection():
        print("❌ Ollama connection failed")
        return False
    
    print("✅ Ollama connection successful")
    
    # Sample paper sections for testing
    test_sections = {
        'title': 'Optimizing Graph Neural Networks for Large-Scale Social Network Analysis',
        'abstract': '''Social networks have become increasingly complex, with billions of users and intricate relationship patterns. Traditional graph analysis methods struggle with scalability and accuracy when applied to large-scale social networks. This paper presents GraphOptim, a novel approach that combines advanced graph neural networks with distributed computing techniques to achieve superior performance in social network analysis tasks. Our method demonstrates a 45% improvement in node classification accuracy and 60% reduction in computational time compared to existing state-of-the-art approaches. We evaluate our approach on three large-scale datasets including Twitter, Facebook, and LinkedIn networks with over 10 million nodes each. The results show significant improvements in community detection, influence prediction, and user behavior analysis. Our findings suggest that GraphOptim could revolutionize how we analyze and understand large-scale social networks.''',
        'conclusion': '''In this work, we have presented GraphOptim, a breakthrough approach for large-scale social network analysis that addresses the critical limitations of existing methods. Our experimental results demonstrate substantial improvements across multiple metrics and datasets. The 45% accuracy improvement and 60% computational efficiency gains represent significant advances for the field. However, we acknowledge certain limitations in our current approach, particularly regarding privacy preservation and real-time processing capabilities. The methodology shows promise for broader applications beyond social networks, potentially extending to biological networks and recommendation systems.''',
        'future_work': '''Future research directions include: (1) Developing privacy-preserving mechanisms to protect user data while maintaining analysis accuracy, (2) Implementing real-time processing capabilities for dynamic network analysis, (3) Extending the methodology to other types of networks such as biological and financial networks, (4) Investigating the scalability limits of the approach with networks exceeding 100 million nodes, and (5) Developing interpretability mechanisms to better understand the model's decision-making process. These extensions would address current limitations and broaden the applicability of our approach.'''
    }
    
    try:
        # Run Stage 1 analysis
        core_understanding = analyzer.stage1_core_understanding_analysis(test_sections)
        
        # Display results
        print("\n📋 STAGE 1 ANALYSIS RESULTS:")
        print("=" * 50)
        
        print(f"\n🎯 FIELD CLASSIFICATION:")
        print(f"   {core_understanding.field_classification}")
        
        print(f"\n📖 RESEARCH STORY ARC:")
        for key, value in core_understanding.research_story_arc.items():
            print(f"   • {key.replace('_', ' ').title()}: {value}")
        
        print(f"\n🔍 CONFIDENCE ASSESSMENT:")
        for key, value in core_understanding.confidence_assessment.items():
            print(f"   • {key.replace('_', ' ').title()}: {value}")
        
        print(f"\n⚔️ DEBATE SEED POINTS:")
        for i, point in enumerate(core_understanding.debate_seed_points, 1):
            print(f"   {i}. {point}")
        
        print(f"\n🔧 TECHNICAL ELEMENTS:")
        for i, element in enumerate(core_understanding.key_technical_elements, 1):
            print(f"   {i}. {element}")
        
        print(f"\n✅ STAGE 1 TEST SUCCESSFUL!")
        print(f"   • Field identified: {core_understanding.field_classification}")
        print(f"   • Story elements: {len(core_understanding.research_story_arc)}")
        print(f"   • Debate points: {len(core_understanding.debate_seed_points)}")
        print(f"   • Technical elements: {len(core_understanding.key_technical_elements)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Stage 1 test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_stage1_analysis()
    if success:
        print(f"\n🎉 Ready for Stage 2 implementation!")
    else:
        print(f"\n🔧 Fix Stage 1 issues before proceeding")