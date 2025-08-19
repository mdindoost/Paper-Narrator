"""Final fixed summarizer with working strengths/weaknesses parser"""

import requests
import json
import re
from typing import Dict, List


class FinalFixedPaperSummarizerV2:
    def __init__(self, model_name: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
    
    def _call_ollama(self, prompt: str, max_length: int = 1500) -> str:
        """Make a request to Ollama API"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": max_length
            }
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=180)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "").strip()
            
        except requests.RequestException as e:
            raise Exception(f"Ollama API error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON decode error: {str(e)}")
    
    def intelligent_section_detection(self, text: str) -> Dict[str, str]:
        """Enhanced section detection"""
        section_patterns = {
            'abstract': [r'\n\s*ABSTRACT\s*\n', r'\n\s*Abstract\s*\n'],
            'introduction': [r'\n\s*INTRODUCTION\s*\n', r'\n\s*Introduction\s*\n', r'\n\s*1\.?\s*Introduction\s*\n'],
            'methods': [r'\n\s*METHODS\s*\n', r'\n\s*METHODOLOGY\s*\n', r'\n\s*Methods\s*\n'],
            'results': [r'\n\s*RESULTS\s*\n', r'\n\s*Results\s*\n'],
            'discussion': [r'\n\s*DISCUSSION\s*\n', r'\n\s*Discussion\s*\n'],
            'conclusion': [r'\n\s*CONCLUSION\s*\n', r'\n\s*Conclusion\s*\n']
        }
        
        all_matches = []
        for section_name, patterns in section_patterns.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, text, re.IGNORECASE))
                for match in matches:
                    all_matches.append((match.start(), section_name, match.group().strip()))
        
        all_matches.sort(key=lambda x: x[0])
        
        sections = {}
        for i, (start_pos, section_name, match_text) in enumerate(all_matches):
            start_idx = start_pos + len(match_text)
            
            if i + 1 < len(all_matches):
                end_idx = all_matches[i + 1][0]
            else:
                end_idx = len(text)
            
            section_text = text[start_idx:end_idx].strip()
            if section_text and len(section_text) > 100:
                sections[section_name] = section_text
        
        return sections
    
    def comprehensive_analysis(self, text: str) -> Dict[str, List[str]]:
        """Generate comprehensive strengths and weaknesses with FIXED parsing"""
        
        prompt = f"""
Analyze this research paper and identify specific strengths and weaknesses.

**Strengths:**
1. [strength 1]
2. [strength 2] 
3. [strength 3]
4. [strength 4]
5. [strength 5]

**Weaknesses:**
1. [weakness 1]
2. [weakness 2]
3. [weakness 3]
4. [weakness 4]
5. [weakness 5]

Be specific and detailed. Focus on methodology, data quality, novelty, and practical impact.

Paper text: {text[:3500]}
"""
        
        analysis = self._call_ollama(prompt, max_length=1000)
        
        # Use the FIXED parser that handles the actual AI format
        return self._parse_ai_strengths_weaknesses(analysis)
    
    def _parse_ai_strengths_weaknesses(self, text: str) -> Dict[str, List[str]]:
        """FIXED parser for AI response with numbered lists and markdown"""
        
        strengths = []
        weaknesses = []
        current_section = None
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Remove markdown formatting and check for section headers
            clean_line = line.replace('**', '').replace('*', '').strip()
            
            if 'strengths:' in clean_line.lower():
                current_section = 'strengths'
                continue
            elif 'weaknesses:' in clean_line.lower():
                current_section = 'weaknesses'
                continue
            
            # Look for numbered items (1., 2., 3.) or bullet points
            if current_section and (
                line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.')) or
                line.startswith('-') or 
                line.startswith('•')
            ):
                # Extract the content after the number/bullet
                if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.')):
                    # Handle "1. **Title**: Description" format
                    parts = line.split('.', 1)
                    if len(parts) > 1:
                        content = parts[1].strip()
                        # Remove markdown bold from title
                        content = content.replace('**', '')
                        if content and len(content) > 10:
                            if current_section == 'strengths':
                                strengths.append(content)
                            else:
                                weaknesses.append(content)
                else:
                    # Handle "- item" format
                    content = line.replace('-', '').replace('•', '').strip()
                    if content and len(content) > 10:
                        if current_section == 'strengths':
                            strengths.append(content)
                        else:
                            weaknesses.append(content)
        
        # Distribute into categories
        mid_s = len(strengths) // 2 if len(strengths) > 1 else 1
        mid_w = len(weaknesses) // 2 if len(weaknesses) > 1 else 1
        
        return {
            'methodological_strengths': strengths[:mid_s],
            'theoretical_contributions': strengths[mid_s:],
            'practical_significance': [],
            'methodological_weaknesses': weaknesses[:mid_w],
            'data_limitations': weaknesses[mid_w:],
            'conceptual_issues': []
        }
    
    def generate_detailed_discussion_topics(self, summary: Dict[str, str], 
                                          analysis: Dict[str, List[str]]) -> List[Dict[str, str]]:
        """Generate paper-specific discussion topics with FIXED parsing"""
        
        prompt = f"""
Based on this research paper, create 5 debate topics. For each topic, provide the question and two opposing viewpoints.

Paper topic: {summary.get('main_topic', 'Research paper')}
Key finding: {summary.get('key_finding', 'Novel research findings')}

Format each topic exactly like this:

**TOPIC 1:** [Question about the research]
**OPTIMIST:** [Positive viewpoint]
**SKEPTIC:** [Critical viewpoint]

**TOPIC 2:** [Another question]
**OPTIMIST:** [Positive viewpoint]
**SKEPTIC:** [Critical viewpoint]

Continue for 5 topics total.
"""
        
        topics_text = self._call_ollama(prompt, max_length=1500)
        
        # Use the FIXED parser that handles markdown
        topics = self._parse_discussion_topics_fixed(topics_text)
        
        return topics
    
    def _parse_discussion_topics_fixed(self, text: str) -> List[Dict[str, str]]:
        """FIXED parser that handles markdown formatting"""
        
        topics = []
        current_topic = {}
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Handle markdown formatting - remove ** and look for keywords
            clean_line = line.replace('**', '').strip()
            
            if clean_line.startswith('TOPIC') and ':' in clean_line:
                # Save previous topic
                if current_topic and 'question' in current_topic:
                    topics.append(current_topic)
                
                # Start new topic
                question = clean_line.split(':', 1)[-1].strip()
                current_topic = {
                    'question': question, 
                    'controversy': '', 
                    'optimist_view': '', 
                    'skeptic_view': ''
                }
                
            elif clean_line.startswith('OPTIMIST') and ':' in clean_line:
                if current_topic:
                    current_topic['optimist_view'] = clean_line.split(':', 1)[-1].strip()
                    
            elif clean_line.startswith('SKEPTIC') and ':' in clean_line:
                if current_topic:
                    current_topic['skeptic_view'] = clean_line.split(':', 1)[-1].strip()
        
        # Add the last topic
        if current_topic and 'question' in current_topic:
            topics.append(current_topic)
        
        return topics[:5]
    
    def deep_paper_analysis(self, paper_data: Dict) -> Dict:
        """Deep analysis with FIXED parsing for everything"""
        print("🔍 Starting deep analysis with FIXED parsing for strengths/weaknesses...")
        
        # Section detection
        enhanced_sections = self.intelligent_section_detection(paper_data["raw_text"])
        print(f"📖 Detected sections: {list(enhanced_sections.keys())}")
        
        # Prepare analysis text
        analysis_text = ""
        priority_order = ['abstract', 'introduction', 'methods', 'results', 'discussion', 'conclusion']
        
        for section in priority_order:
            if section in enhanced_sections:
                analysis_text += f"\n\n{section.upper()}:\n{enhanced_sections[section][:1500]}"
        
        if not analysis_text.strip():
            analysis_text = paper_data["raw_text"][:5000]
        
        print(f"📝 Analysis text length: {len(analysis_text):,} characters")
        
        # Generate summary
        print("📋 Generating summary...")
        summary = self.summarize_abstract(analysis_text)
        
        # FIXED comprehensive analysis
        print("🔬 Analyzing strengths/weaknesses with FIXED parser...")
        comprehensive_analysis = self.comprehensive_analysis(analysis_text)
        
        # FIXED discussion topics  
        print("💬 Generating paper-specific discussion topics with FIXED parser...")
        detailed_topics = self.generate_detailed_discussion_topics(summary, comprehensive_analysis)
        
        total_strengths = sum(len(v) for k, v in comprehensive_analysis.items() 
                            if any(word in k for word in ['strength', 'contribution', 'significance']))
        total_weaknesses = sum(len(v) for k, v in comprehensive_analysis.items() 
                             if any(word in k for word in ['weakness', 'limitation', 'issues']))
        
        print(f"✅ Analysis complete: {total_strengths} strengths, {total_weaknesses} weaknesses, {len(detailed_topics)} topics")
        
        return {
            "enhanced_sections": enhanced_sections,
            "summary": summary,
            "comprehensive_analysis": comprehensive_analysis,
            "detailed_discussion_topics": detailed_topics,
            "analysis_depth": {
                "sections_found": len(enhanced_sections),
                "total_strengths": total_strengths,
                "total_weaknesses": total_weaknesses,
                "discussion_topics": len(detailed_topics),
                "analysis_text_length": len(analysis_text)
            }
        }
    
    def summarize_abstract(self, text: str) -> Dict[str, str]:
        """Generate detailed summary"""
        prompt = f"""
Analyze this research paper and provide a summary:

**Main Topic:** [What is this paper about]
**Key Finding:** [The primary result]  
**Method:** [How they did it]
**Significance:** [Why it matters]

Paper: {text[:3000]}
"""
        
        summary = self._call_ollama(prompt, max_length=600)
        
        sections = {"main_topic": "", "key_finding": "", "method": "", "significance": ""}
        
        lines = summary.split('\n')
        current_section = None
        
        section_patterns = {
            'Main Topic:': 'main_topic',
            'Key Finding:': 'key_finding',
            'Method:': 'method',
            'Significance:': 'significance'
        }
        
        for line in lines:
            line = line.strip()
            for pattern, section_key in section_patterns.items():
                if pattern in line:
                    sections[section_key] = line.split(':', 1)[-1].strip().replace('**', '')
                    current_section = section_key
                    break
            else:
                if line and current_section and not line.startswith('**'):
                    sections[current_section] += " " + line
        
        return sections

    def test_connection(self) -> bool:
        """Test connection"""
        try:
            test_response = self._call_ollama("Hello", max_length=10)
            return len(test_response) > 0
        except:
            return False
