"""
Quick Patch for Stage 2 Additional Fixes
Save as: stage2_additional_fixes_patch.py

This patches the existing test_enhanced_claims_challenges.py
to apply additional fixes for ** symbols and other issues.
"""

import re

def patch_stage2_results(stage2_results):
    """Apply additional fixes to Stage 2 results"""
    
    print("🔧 APPLYING ADDITIONAL FIXES TO STAGE 2 RESULTS...")
    
    # Fix introduction material
    if hasattr(stage2_results, 'introduction_material'):
        intro_material = stage2_results.introduction_material
        
        # Fix paper topic
        if 'paper_topic' in intro_material:
            intro_material['paper_topic'] = re.sub(r'\*+', '', intro_material['paper_topic']).strip()
            print(f"   ✅ Fixed paper topic: {intro_material['paper_topic'][:50]}...")
        
        # Fix key finding
        if 'key_finding' in intro_material:
            intro_material['key_finding'] = re.sub(r'\*+', '', intro_material['key_finding']).strip()
            print(f"   ✅ Fixed key finding: {intro_material['key_finding'][:50]}...")
        
        # Fix research field
        if 'research_field' in intro_material:
            intro_material['research_field'] = re.sub(r'\*+', '', intro_material['research_field']).strip()
            print(f"   ✅ Fixed research field: {intro_material['research_field']}")
        
        # Fix intro hook
        if 'intro_hook' in intro_material:
            original_hook = intro_material['intro_hook']
            # Remove ** symbols
            fixed_hook = re.sub(r'\*+', '', original_hook)
            # Fix the paper reference
            fixed_hook = re.sub(r'\*\*\s*this paper', intro_material.get('paper_topic', 'this research'), fixed_hook)
            intro_material['intro_hook'] = fixed_hook
            print(f"   ✅ Fixed intro hook: {fixed_hook[:80]}...")
    
    print("   ✅ STAGE 2 ADDITIONAL FIXES APPLIED")
    return stage2_results

def apply_quick_field_fix(stage1_understanding):
    """Quick fix for stage1 field classification"""
    
    print("🔧 APPLYING QUICK FIELD FIX...")
    
    if hasattr(stage1_understanding, 'research_field'):
        original_field = stage1_understanding.research_field
        
        # Remove ** symbols
        cleaned = re.sub(r'\*+', '', original_field).strip()
        
        # Extract subfield if present
        if ' - ' in cleaned:
            parts = cleaned.split(' - ', 1)
            if len(parts) > 1:
                subfield = parts[1].strip()
                if len(subfield) > 5:
                    cleaned = subfield
        
        stage1_understanding.research_field = cleaned
        print(f"   ✅ Field fixed: {original_field} → {cleaned}")
    
    if hasattr(stage1_understanding, 'key_finding'):
        original_finding = stage1_understanding.key_finding
        cleaned_finding = re.sub(r'\*+', '', original_finding).strip()
        stage1_understanding.key_finding = cleaned_finding
        print(f"   ✅ Key finding fixed: {cleaned_finding[:50]}...")
    
    return stage1_understanding
