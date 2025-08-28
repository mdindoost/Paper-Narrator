"""
Comprehensive Bug Fixes for New Issues Found
These are additional fixes needed beyond the original 6 bugs

Issues to Fix:
- Key finding ** symbols 
- Redundant "The authors claim"
- Text cleanup artifacts (1:, ..)
- Conclusion ** symbols and paper name
"""

import re
from typing import Dict, Any

class AdditionalBugFixes:
    """Additional fixes for newly discovered issues"""
    
    def __init__(self):
        pass
    
    def fix_key_finding_symbols(self, key_finding: str) -> str:
        """Fix ** symbols in key finding"""
        if not key_finding:
            return key_finding
        
        print(f"🔧 FIXING KEY FINDING: {key_finding[:50]}...")
        
        # Remove ** symbols from beginning and throughout
        cleaned = re.sub(r'\*+', '', key_finding).strip()
        
        # Remove any leading "The authors" duplication patterns
        cleaned = re.sub(r'^The authors\s+The authors', 'The authors', cleaned, flags=re.IGNORECASE)
        
        print(f"   ✅ FIXED TO: {cleaned[:50]}...")
        return cleaned
    
    def create_smart_introduction(self, paper_topic: str, key_finding: str, research_field: str, natural_summary: str) -> str:
        """Create introduction without redundant 'The authors claim'"""
        
        print(f"🎬 CREATING SMART INTRODUCTION:")
        print(f"   📄 Topic: {paper_topic[:50]}...")
        print(f"   💡 Finding: {key_finding[:50]}...")
        
        # Clean the key finding first
        clean_key_finding = self.fix_key_finding_symbols(key_finding)
        
        # Check if key finding already starts with "The authors" or similar
        author_patterns = [
            r'^The authors?\b',
            r'^This paper\b', 
            r'^We\b',
            r'^Our\b',
            r'^The research\b'
        ]
        
        starts_with_author = any(re.match(pattern, clean_key_finding, re.IGNORECASE) for pattern in author_patterns)
        
        if starts_with_author:
            # Don't add "The authors claim" - use the finding directly
            claim_text = clean_key_finding.lower()
            print(f"   🔧 Using direct finding (already has subject)")
        else:
            # Add "The authors claim" only if needed
            claim_text = f"the authors claim {clean_key_finding.lower()}"
            print(f"   🔧 Adding 'authors claim' prefix")
        
        # Create smart introduction
        enhanced_intro = f"""What happens when two brilliant researchers examine the same {research_field.lower()} study and reach completely opposite conclusions?

Welcome to Research Rundown!

Today's fascinating topic: {paper_topic}

{claim_text.capitalize()}, promising to revolutionize how we approach this field. But is this a genuine breakthrough or are we looking at overstated results?

Our analysis reveals {natural_summary} - setting up the perfect storm for an academic showdown.

Dr. Ava D. sees game-changing potential, while Prof. Marcus W. has serious methodological concerns. 

Let the evidence-based battle begin!"""

        print(f"   ✅ SMART INTRO CREATED")
        return enhanced_intro
    
    def fix_text_cleanup_artifacts(self, text: str) -> str:
        """Fix text cleanup artifacts like '1:', '..' etc."""
        
        if not text or not text.strip():
            return text
        
        print(f"🧹 FIXING ARTIFACTS: {text[:50]}...")
        
        cleaned = text
        
        # Fix numbered artifacts from "Evidence Analysis 1" etc.
        cleaned = re.sub(r'\bevidence shows that \d+:\s*"?', 'evidence shows that ', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\bthe data demonstrates \d+:\s*"?', 'the data demonstrates ', cleaned, flags=re.IGNORECASE)
        
        # Fix double periods and multiple periods
        cleaned = re.sub(r'\.{2,}', '.', cleaned)
        
        # Fix broken quotations
        cleaned = re.sub(r'"\s*$', '', cleaned)  # Remove trailing quotes
        cleaned = re.sub(r'^\s*"', '', cleaned)  # Remove leading quotes
        
        # Fix spacing around parentheses
        cleaned = re.sub(r'\s*\(\s*e\.g\.\s*,\s*([^)]+)\s*\)', r' (e.g., \1)', cleaned)
        
        # Fix comma spacing
        cleaned = re.sub(r'\s*,\s*', ', ', cleaned)
        
        # Fix sentence spacing
        cleaned = re.sub(r'\.\s*([a-z])', r'. \1', cleaned)
        
        print(f"   ✅ ARTIFACTS FIXED: {cleaned[:50]}...")
        return cleaned
    
    def create_proper_conclusion(self, paper_topic: str, research_field: str) -> str:
        """Create conclusion with proper paper name and no ** symbols"""
        
        print(f"🎯 CREATING PROPER CONCLUSION:")
        print(f"   📄 Paper: {paper_topic}")
        print(f"   🎯 Field: {research_field}")
        
        # Clean paper topic and field
        clean_topic = re.sub(r'\*+', '', paper_topic).strip()
        clean_field = re.sub(r'\*+', '', research_field).strip()
        
        # Create natural conclusion
        proper_conclusion = f"""And there you have it - a fascinating debate about {clean_field.lower()} research on {clean_topic.lower()}.

Dr. Ava D. highlighted the innovative potential and breakthrough possibilities, while Prof. Marcus W. raised critical questions about methodology and evidence quality.

The verdict? This work appears promising but requires further validation. As always in academic research, the devil is in the details.

Thanks for joining us on Research Rundown, where we dive deep into the papers shaping our world. Until next time, keep questioning, keep discovering!"""

        print(f"   ✅ PROPER CONCLUSION CREATED")
        return proper_conclusion
    
    def comprehensive_tts_cleanup(self, text: str, for_test: bool = False) -> str:
        """Enhanced TTS cleanup with artifact fixes"""
        
        if not text or not text.strip():
            return text
        
        cleaned = text
        
        # Apply artifact fixes first
        cleaned = self.fix_text_cleanup_artifacts(cleaned)
        
        # Fix double periods and ellipsis for TTS
        if not for_test:
            # For TTS, convert multiple periods to single with proper spacing
            cleaned = re.sub(r'\.{2,}', '.', cleaned)
            
            # Ensure sentences end properly
            if cleaned and not cleaned.endswith(('.', '!', '?')):
                cleaned += '.'
        
        # Fix dashes for better TTS flow (dashes become pauses)
        # Replace double dashes with single for cleaner pauses
        cleaned = re.sub(r'--+', ' - ', cleaned)
        
        return cleaned.strip()


# Integration functions to apply these fixes

def apply_additional_fixes_to_stage1(stage1_understanding):
    """Apply additional fixes to Stage 1 results"""
    fixer = AdditionalBugFixes()
    
    if hasattr(stage1_understanding, 'key_finding'):
        stage1_understanding.key_finding = fixer.fix_key_finding_symbols(stage1_understanding.key_finding)
    
    return stage1_understanding

def apply_additional_fixes_to_introduction(stage1, stage2):
    """Apply additional fixes to introduction generation"""
    fixer = AdditionalBugFixes()
    
    # Get components
    paper_topic = stage2.introduction_material.get("paper_topic", stage1.paper_topic)
    key_finding = stage1.key_finding
    research_field = stage1.research_field
    
    # Calculate natural summary
    strong_count = sum(1 for claim in stage2.paper_claims if claim.evidence_strength in ['strong', 'moderate'])
    weak_count = sum(1 for claim in stage2.paper_claims if claim.evidence_strength in ['weak', 'insufficient'])
    
    # Natural summary logic
    if strong_count == 0:
        strong_desc = "no particularly strong"
    elif strong_count == 1:
        strong_desc = "one strong"
    elif strong_count <= 3:
        strong_desc = "a few strong"
    elif strong_count <= 6:
        strong_desc = "several strong"
    else:
        strong_desc = "many strong"
    
    if weak_count == 0:
        weak_desc = "no questionable"
    elif weak_count == 1:
        weak_desc = "one questionable"
    elif weak_count <= 3:
        weak_desc = "a few questionable"
    else:
        weak_desc = "several questionable"
    
    if strong_count > weak_count and strong_count > 0:
        natural_summary = f"{strong_desc} claims with {weak_desc} concerns"
    elif weak_count > strong_count and weak_count > 0:
        natural_summary = f"{weak_desc} claims alongside {strong_desc} evidence"
    elif strong_count > 0 and weak_count > 0:
        natural_summary = f"mixed evidence with {strong_desc} and {weak_desc} claims"
    elif strong_count > 0:
        natural_summary = f"{strong_desc} claims to examine"
    else:
        natural_summary = "complex claims that need careful analysis"
    
    # Create smart introduction
    smart_introduction = fixer.create_smart_introduction(paper_topic, key_finding, research_field, natural_summary)
    
    return smart_introduction

def apply_additional_fixes_to_conclusion(stage1, stage2):
    """Apply additional fixes to conclusion generation"""
    fixer = AdditionalBugFixes()
    
    paper_topic = stage2.introduction_material.get("paper_topic", stage1.paper_topic)
    research_field = stage1.research_field
    
    return fixer.create_proper_conclusion(paper_topic, research_field)

def apply_additional_fixes_to_dialogue_content(conversation_script):
    """Apply additional fixes to all dialogue content"""
    fixer = AdditionalBugFixes()
    
    # Fix introduction
    if hasattr(conversation_script, 'introduction'):
        conversation_script.introduction = fixer.comprehensive_tts_cleanup(conversation_script.introduction)
    
    # Fix all dialogue turns
    if hasattr(conversation_script, 'turns'):
        for turn in conversation_script.turns:
            if hasattr(turn, 'content'):
                turn.content = fixer.comprehensive_tts_cleanup(turn.content)
    
    # Fix conclusion
    if hasattr(conversation_script, 'conclusion'):
        conversation_script.conclusion = fixer.comprehensive_tts_cleanup(conversation_script.conclusion)
    
    return conversation_script


# Test the fixes
def test_additional_fixes():
    """Test the additional fixes"""
    
    print("🧪 TESTING ADDITIONAL BUG FIXES")
    print("="*60)
    
    fixer = AdditionalBugFixes()
    
    # Test 1: Key finding symbols
    test_key_finding = "** The authors demonstrate that their approach achieves breakthrough results"
    fixed_finding = fixer.fix_key_finding_symbols(test_key_finding)
    print(f"✅ Key Finding Fix:")
    print(f"   Before: {test_key_finding}")
    print(f"   After:  {fixed_finding}")
    
    # Test 2: Artifact cleanup
    test_artifacts = 'evidence shows that 1: "We address this scalability gap by developing..'
    fixed_artifacts = fixer.fix_text_cleanup_artifacts(test_artifacts)
    print(f"\n✅ Artifact Fix:")
    print(f"   Before: {test_artifacts}")
    print(f"   After:  {fixed_artifacts}")
    
    # Test 3: Smart introduction (no redundancy)
    paper_topic = "Parallel Community Detection Algorithms"
    key_finding = "The authors demonstrate breakthrough scalability results"
    research_field = "Algorithms and Network Analysis"
    natural_summary = "several strong claims with few concerns"
    
    smart_intro = fixer.create_smart_introduction(paper_topic, key_finding, research_field, natural_summary)
    print(f"\n✅ Smart Introduction (first 200 chars):")
    print(f"   {smart_intro[:200]}...")
    
    # Test 4: Proper conclusion
    proper_conclusion = fixer.create_proper_conclusion(paper_topic, research_field)
    print(f"\n✅ Proper Conclusion (first 200 chars):")
    print(f"   {proper_conclusion[:200]}...")


if __name__ == "__main__":
    test_additional_fixes()
