"""
Enhanced Multi-Stage Text Cleanup & Humanization
Save as: src/enhanced_text_humanizer.py

Multi-stage pipeline: Raw Text → Technical Cleanup → AI Humanization → Natural Speech
"""

import requests
import json
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class CleanupResult:
    """Result of text cleanup process"""
    original_text: str
    stage1_markdown_cleanup: str
    stage2_category_removal: str
    stage3_format_fixes: str
    stage4_humanized: str
    final_speech_ready: str


class EnhancedTextHumanizer:
    """Multi-stage text cleanup and humanization system"""
    
    def __init__(self, model_name: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
    
    def _call_ollama(self, prompt: str, max_length: int = 500) -> str:
        """Call Ollama for AI humanization"""
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
            response = requests.post(self.api_url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except Exception as e:
            print(f"⚠️ AI humanization failed, using cleaned text: {e}")
            return ""
    
    def stage1_markdown_cleanup(self, text: str) -> str:
        """Stage 1: Remove all markdown symbols and formatting artifacts"""
        
        print(f"🧹 Stage 1: Markdown cleanup for: {text[:50]}...")
        
        cleaned = text
        
        # Remove markdown formatting
        cleaned = re.sub(r'\*{2,}', '', cleaned)  # Remove ** and ***
        cleaned = re.sub(r'\*', '', cleaned)       # Remove single *
        cleaned = re.sub(r'#{1,6}\s*', '', cleaned)  # Remove # headers
        cleaned = re.sub(r'_{2,}', '', cleaned)    # Remove __
        cleaned = re.sub(r'`{1,3}', '', cleaned)   # Remove ` code formatting
        cleaned = re.sub(r'\[.*?\]', '', cleaned)  # Remove [brackets]
        cleaned = re.sub(r'\(.*?\)', '', cleaned)  # Remove (parentheses) content
        
        # Clean up whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.strip()
        
        print(f"   ✅ Markdown removed: {cleaned[:50]}...")
        return cleaned
    
    def stage2_category_removal(self, text: str) -> str:
        """Stage 2: Remove category labels and prefixes"""
        
        print(f"🏷️ Stage 2: Category removal for: {text[:50]}...")
        
        cleaned = text
        
        # Remove common category prefixes that appear in ammunition
        category_prefixes = [
            r'Lack of context:\s*',
            r'Segmentation Faults?:\s*',
            r'Methodological concerns?:\s*', 
            r'Statistical issues?:\s*',
            r'Evidence gaps?:\s*',
            r'Reproducibility problems?:\s*',
            r'Sample size issues?:\s*',
            r'Validity concerns?:\s*',
            r'Generalization problems?:\s*',
            r'Data quality:\s*',
            r'Experimental design:\s*',
            r'Control groups?:\s*',
            r'Bias detection:\s*',
            r'Confounding variables?:\s*'
        ]
        
        for prefix_pattern in category_prefixes:
            cleaned = re.sub(prefix_pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Remove numbered list prefixes
        cleaned = re.sub(r'^\d+\.\s*', '', cleaned)
        cleaned = re.sub(r'^[-•*]\s*', '', cleaned)
        
        # Clean up
        cleaned = cleaned.strip()
        if cleaned and not cleaned[0].isupper():
            cleaned = cleaned[0].upper() + cleaned[1:] if len(cleaned) > 1 else cleaned.upper()
        
        print(f"   ✅ Categories removed: {cleaned[:50]}...")
        return cleaned
    
    def stage3_format_fixes(self, text: str) -> str:
        """Stage 3: Fix broken formatting and incomplete sentences"""
        
        print(f"🔧 Stage 3: Format fixes for: {text[:50]}...")
        
        cleaned = text
        
        # Fix broken sentence patterns
        cleaned = re.sub(r'\.\s*[a-z]', lambda m: '. ' + m.group()[-1].upper(), cleaned)
        
        # Fix incomplete sentences that end abruptly
        if cleaned and not cleaned.endswith(('.', '!', '?')):
            # If sentence seems incomplete, try to make it complete
            if len(cleaned.split()) < 3:
                cleaned = f"The analysis shows that {cleaned.lower()}"
            cleaned += "."
        
        # Fix double spaces and punctuation
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = re.sub(r'\.{2,}', '.', cleaned)
        cleaned = re.sub(r'\s+([.!?])', r'\1', cleaned)
        
        # Remove trailing incomplete words or artifacts
        words = cleaned.split()
        if words and len(words[-1]) < 2:  # Remove very short trailing words
            cleaned = ' '.join(words[:-1])
            if not cleaned.endswith(('.', '!', '?')):
                cleaned += '.'
        
        print(f"   ✅ Format fixed: {cleaned[:50]}...")
        return cleaned
    
    def stage4_ai_humanization(self, text: str, speaker_role: str, research_field: str) -> str:
        """Stage 4: AI humanization to make it sound like natural academic debate"""
        
        print(f"🤖 Stage 4: AI humanization for {speaker_role}...")
        
        if not text.strip():
            return text
        
        # Create role-specific humanization prompt
        if "optimist" in speaker_role.lower() or "ava" in speaker_role.lower():
            personality_prompt = """You are Dr. Ava D., an enthusiastic and optimistic researcher who gets excited about breakthrough potential. You speak with genuine academic enthusiasm but remain professional."""
            
        elif "skeptic" in speaker_role.lower() or "marcus" in speaker_role.lower():
            personality_prompt = """You are Prof. Marcus W., a methodologically rigorous and skeptical academic who focuses on evidence quality and research validity. You speak with measured concern and professional skepticism."""
            
        else:  # Narrator/Host
            personality_prompt = """You are a professional podcast host introducing academic research topics. You speak clearly and engagingly to make complex topics accessible."""
        
        humanization_prompt = f"""{personality_prompt}

RESEARCH FIELD: {research_field}

ORIGINAL ACADEMIC CONTENT: "{text}"

TASK: Convert this academic content into natural, engaging speech that sounds like a real professor speaking in a podcast debate. 

REQUIREMENTS:
- Make it sound conversational but professional
- Remove any remaining category labels or technical artifacts
- Keep the core meaning but make it flow naturally
- Sound like genuine academic discussion, not robotic points
- Use "I think", "I'm concerned", "What excites me", etc.
- Maximum 2-3 sentences
- End with complete thought

NATURAL ACADEMIC SPEECH:"""

        humanized = self._call_ollama(humanization_prompt, max_length=400)
        
        if not humanized or len(humanized.strip()) < 10:
            # Fallback: basic humanization if AI fails
            humanized = self._fallback_humanization(text, speaker_role)
        
        print(f"   ✅ Humanized: {humanized[:50]}...")
        return humanized
    
    def _fallback_humanization(self, text: str, speaker_role: str) -> str:
        """Fallback humanization if AI fails"""
        
        if "optimist" in speaker_role.lower() or "ava" in speaker_role.lower():
            return f"What excites me about this is that {text.lower()}"
        elif "skeptic" in speaker_role.lower() or "marcus" in speaker_role.lower():
            return f"I'm concerned that {text.lower()}"
        else:
            return text
    
    def complete_cleanup_pipeline(self, text: str, speaker_role: str = "neutral", 
                                research_field: str = "research") -> CleanupResult:
        """Complete multi-stage cleanup and humanization pipeline"""
        
        print(f"\n🔄 COMPLETE CLEANUP PIPELINE for {speaker_role}")
        print(f"Original: {text}")
        
        # Stage 1: Markdown cleanup
        stage1_result = self.stage1_markdown_cleanup(text)
        
        # Stage 2: Category removal
        stage2_result = self.stage2_category_removal(stage1_result)
        
        # Stage 3: Format fixes
        stage3_result = self.stage3_format_fixes(stage2_result)
        
        # Stage 4: AI humanization
        stage4_result = self.stage4_ai_humanization(stage3_result, speaker_role, research_field)
        
        # Final speech preparation
        final_result = self.prepare_for_speech(stage4_result)
        
        result = CleanupResult(
            original_text=text,
            stage1_markdown_cleanup=stage1_result,
            stage2_category_removal=stage2_result,
            stage3_format_fixes=stage3_result,
            stage4_humanized=stage4_result,
            final_speech_ready=final_result
        )
        
        print(f"Final: {final_result}")
        print("=" * 60)
        
        return result
    
    def prepare_for_speech(self, text: str) -> str:
        """Final preparation for TTS"""
        
        # Ensure proper sentence structure for speech
        cleaned = text.strip()
        
        # Fix common TTS issues
        cleaned = re.sub(r'\be\.g\.\s*', 'for example ', cleaned)
        cleaned = re.sub(r'\bi\.e\.\s*', 'that is ', cleaned)
        cleaned = re.sub(r'\betc\.?\s*', 'and so on ', cleaned)
        cleaned = re.sub(r'\bvs\.?\s*', 'versus ', cleaned)
        
        # Ensure ends properly
        if cleaned and not cleaned.endswith(('.', '!', '?')):
            cleaned += '.'
        
        return cleaned


class SmartFieldExtractor:
    """Extract the most specific part of field classification"""
    
    @staticmethod
    def extract_specific_field(raw_field: str) -> str:
        """Extract most specific field from raw classification"""
        
        print(f"🎯 Extracting specific field from: {raw_field}")
        
        # Clean up markdown first
        cleaned = re.sub(r'\*+', '', raw_field)
        cleaned = cleaned.strip()
        
        # Look for pattern: "Broad Field - Specific Field" 
        if ' - ' in cleaned:
            parts = cleaned.split(' - ')
            if len(parts) >= 2:
                # Use the most specific (last) part
                specific = parts[-1].strip()
                print(f"   ✅ Extracted specific: {specific}")
                return specific
        
        # Look for pattern: "Broad Field: Specific Field"
        if ': ' in cleaned:
            parts = cleaned.split(': ')
            if len(parts) >= 2:
                specific = parts[-1].strip()
                print(f"   ✅ Extracted specific: {specific}")
                return specific
        
        # Fallback: use full field but clean it
        print(f"   ⚠️ Using full field: {cleaned}")
        return cleaned


class BalancedClaimsGenerator:
    """Generate balanced claims description instead of exact numbers"""
    
    @staticmethod
    def generate_balanced_description(strong_claims: int, weak_claims: int, 
                                    questionable_claims: int) -> str:
        """Generate balanced description of claims"""
        
        total_claims = strong_claims + weak_claims + questionable_claims
        
        if total_claims == 0:
            return "interesting research claims with mixed evidence quality"
        
        # Calculate proportions
        strong_ratio = strong_claims / total_claims if total_claims > 0 else 0
        weak_ratio = (weak_claims + questionable_claims) / total_claims if total_claims > 0 else 0
        
        if strong_ratio >= 0.7:
            return "compelling evidence supporting most claims, though some methodological questions remain"
        elif strong_ratio >= 0.4:
            return "mixed evidence - some strong supporting data alongside significant methodological concerns"
        elif strong_ratio >= 0.2:
            return "intriguing claims but substantial evidence gaps and methodological challenges"
        else:
            return "ambitious claims that require much stronger evidence and methodological rigor"


# Test function to demonstrate the pipeline
def test_cleanup_pipeline():
    """Test the complete cleanup and humanization pipeline"""
    
    print("🧪 TESTING COMPLETE CLEANUP PIPELINE")
    print("=" * 80)
    
    humanizer = EnhancedTextHumanizer()
    field_extractor = SmartFieldExtractor()
    
    # Test field extraction
    test_fields = [
        "** Computer Science - Algorithms and Network Analysis",
        "** Psychology: Cognitive Neuroscience", 
        "Medicine - Cardiology",
        "** Machine Learning"
    ]
    
    print("\n🎯 FIELD EXTRACTION TESTS:")
    for field in test_fields:
        specific = field_extractor.extract_specific_field(field)
        print(f"   {field} → {specific}")
    
    # Test text cleanup
    test_cases = [
        {
            "text": "** Lack of context: The paper does not provide sufficient background information for the algorithmic approach.",
            "role": "skeptic_marcus",
            "field": "Algorithms and Network Analysis"
        },
        {
            "text": "** Segmentation Faults: While the methodology shows promise, there are implementation concerns.",
            "role": "skeptic_marcus", 
            "field": "Computer Science"
        },
        {
            "text": "** Strong evidence: The experimental results demonstrate significant improvements in network efficiency.",
            "role": "optimist_ava",
            "field": "Network Analysis"
        },
        {
            "text": "Today's fascinating topic: ** Algorithms and Network Analysis research",
            "role": "narrator",
            "field": "Computer Science"
        }
    ]
    
    print(f"\n🧹 TEXT CLEANUP TESTS:")
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        result = humanizer.complete_cleanup_pipeline(
            test_case["text"],
            test_case["role"], 
            test_case["field"]
        )
        
        print(f"ORIGINAL: {result.original_text}")
        print(f"FINAL:    {result.final_speech_ready}")
    
    # Test balanced claims
    claims_gen = BalancedClaimsGenerator()
    
    print(f"\n⚖️ BALANCED CLAIMS TESTS:")
    test_claims = [
        (5, 0, 0),  # All strong
        (2, 1, 2),  # Mixed  
        (0, 2, 3),  # Mostly weak
        (1, 0, 1)   # Balanced
    ]
    
    for strong, weak, questionable in test_claims:
        description = claims_gen.generate_balanced_description(strong, weak, questionable)
        print(f"   {strong} strong, {weak} weak, {questionable} questionable → {description}")


if __name__ == "__main__":
    test_cleanup_pipeline()
