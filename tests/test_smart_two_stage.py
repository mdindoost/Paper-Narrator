"""
Smart Two-Stage Analysis Approach
Save as: test_smart_two_stage.py (in root directory)

Stage 1: Simple field identification and expertise mapping
Stage 2: Targeted analysis based on Stage 1 findings
"""

import sys
import os
import re
import time
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List

# Add src directory to path
sys.path.append('src')
sys.path.append('.')

try:
    from pdf_processor import PDFProcessor
    from enhanced_analyzer import EnhancedPaperAnalyzer
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


@dataclass
class Stage1Understanding:
    """Simple understanding from title/abstract/conclusion"""
    research_field: str
    paper_topic: str
    main_approach: str
    key_finding: str
    required_expertise: List[str]
    research_type: str  # experimental, theoretical, computational, etc.


@dataclass
class Stage2Analysis:
    """Detailed analysis based on Stage 1 understanding"""
    detailed_methodology: List[str]
    specific_contributions: List[str]
    evidence_assessment: List[str]
    field_specific_debates: List[str]
    expert_level_details: List[str]


class SmartTwoStageAnalyzer(EnhancedPaperAnalyzer):
    """Two-stage analyzer: simple understanding -> targeted analysis"""
    
    def debug_step_separator(self, title: str, step_num: int):
        """Visual separator for debug steps"""
        print(f"\n{'='*100}")
        print(f"🎯 STAGE {step_num}: {title}")
        print(f"{'='*100}")
    
    def stage1_simple_understanding(self, core_sections: Dict[str, str]) -> Stage1Understanding:
        """Stage 1: Simple field identification and expertise mapping"""
        
        self.debug_step_separator("SIMPLE UNDERSTANDING & FIELD IDENTIFICATION", 1)
        
        # Prepare core content
        core_content = ""
        for section in ['title', 'abstract', 'conclusion', 'future_work']:
            if section in core_sections:
                core_content += f"\n\n{section.upper()}:\n{core_sections[section]}"
        
        # SIMPLE Stage 1 Prompt - Just understand what this paper is about
        stage1_prompt = f"""You are an academic librarian helping to categorize research papers. Your job is to quickly understand what this paper is about and what kind of expertise would be needed to properly evaluate it.

PAPER SECTIONS TO READ:
{core_content}

SIMPLE UNDERSTANDING TASK:

**RESEARCH FIELD:**
What specific field of research is this? Be precise (e.g., "Computer Science - Graph Theory", "Psychology - Cognitive Neuroscience", "Medicine - Cardiology")

**PAPER TOPIC:**  
In one sentence, what is this paper about?

**MAIN APPROACH:**
What is their primary method or approach? (experimental study, algorithm development, theoretical analysis, etc.)

**KEY FINDING:**
What is their main result or contribution?

**REQUIRED EXPERTISE:**
What specific expertise would someone need to properly evaluate this paper? List 3-5 specific areas of knowledge.

**RESEARCH TYPE:**
Is this: Experimental, Theoretical, Computational, Survey/Review, Case Study, or Mixed?

Keep answers brief and focused. This is just initial understanding, not deep analysis."""

        print("📤 STAGE 1 PROMPT (Simple Understanding):")
        print("─" * 80)
        print(stage1_prompt)
        print("─" * 80)
        
        response = self._call_ollama(stage1_prompt, max_length=800)
        
        print("\n📥 STAGE 1 RESPONSE:")
        print("─" * 80)
        print(response)
        print("─" * 80)
        
        # Parse Stage 1 response
        understanding = self._parse_stage1_understanding(response)
        
        print(f"\n📊 STAGE 1 RESULTS:")
        print(f"   🎯 Research Field: {understanding.research_field}")
        print(f"   📄 Paper Topic: {understanding.paper_topic}")
        print(f"   🔬 Main Approach: {understanding.main_approach}")
        print(f"   💡 Key Finding: {understanding.key_finding}")
        print(f"   🧠 Required Expertise: {', '.join(understanding.required_expertise)}")
        print(f"   📊 Research Type: {understanding.research_type}")
        
        input("\n⏸️  STAGE 1 COMPLETE - Press ENTER to continue to Stage 2...")
        
        return understanding
    
    def stage2_targeted_analysis(self, stage1_understanding: Stage1Understanding, 
                               full_text: str) -> Stage2Analysis:
        """Stage 2: Detailed analysis based on Stage 1 understanding"""
        
        self.debug_step_separator("TARGETED ANALYSIS BASED ON STAGE 1", 2)
        
        print(f"🎯 USING STAGE 1 FINDINGS TO GUIDE ANALYSIS:")
        print(f"   Field: {stage1_understanding.research_field}")
        print(f"   Expertise Needed: {', '.join(stage1_understanding.required_expertise)}")
        print(f"   Research Type: {stage1_understanding.research_type}")
        
        # Create targeted Stage 2 prompt based on Stage 1 findings
        field = stage1_understanding.research_field
        expertise = stage1_understanding.required_expertise
        research_type = stage1_understanding.research_type
        
        # Generate field-specific analysis prompt
        stage2_prompt = f"""You are a senior expert in {field} with deep knowledge in: {', '.join(expertise)}.

In Stage 1, we identified this paper as:
- Field: {field}
- Topic: {stage1_understanding.paper_topic}
- Approach: {stage1_understanding.main_approach}
- Type: {research_type}

Now analyze the FULL PAPER with your {field} expertise:

FULL PAPER TEXT:
{full_text[:8000]}  # More text for detailed analysis

TARGETED EXPERT ANALYSIS:

**DETAILED METHODOLOGY ({research_type} Analysis):**
As a {field} expert, analyze their specific methods:
- [What exact techniques/procedures did they use?]
- [How appropriate are these methods for {field} research?]
- [What are the strengths/weaknesses from a {field} perspective?]

**SPECIFIC CONTRIBUTIONS:**
What are their specific contributions to {field}?
- [Novel theoretical insights]
- [Methodological innovations] 
- [Empirical findings]
- [Practical applications]

**EVIDENCE ASSESSMENT:**
Evaluate their evidence quality using {field} standards:
- [How strong is their evidence by {field} standards?]
- [What evidence is missing that {field} experts would expect?]
- [How does this compare to typical {field} research?]

**FIELD-SPECIFIC DEBATES:**
What would {field} experts specifically debate about this work?
- [Technical disagreements experts in {field} would have]
- [Methodological choices that would be controversial]
- [Theoretical positions that would spark debate]

**EXPERT-LEVEL DETAILS:**
Technical details that only {field} experts would focus on:
- [Specific parameters, measurements, or specifications]
- [Implementation details crucial for evaluation]
- [Assumptions or limitations that affect validity]

Focus on what matters most to {field} experts. Use your specialized knowledge."""

        print("📤 STAGE 2 PROMPT (Targeted Expert Analysis):")
        print("─" * 80)
        print(stage2_prompt[:1000] + "..." if len(stage2_prompt) > 1000 else stage2_prompt)
        print("─" * 80)
        print(f"📊 Full prompt length: {len(stage2_prompt)} characters")
        
        response = self._call_ollama(stage2_prompt, max_length=3000)
        
        print("\n📥 STAGE 2 RESPONSE:")
        print("─" * 80)
        print(response)
        print("─" * 80)
        
        # Parse Stage 2 response
        analysis = self._parse_stage2_analysis(response)
        
        return analysis
    
    def compare_stages(self, stage1: Stage1Understanding, stage2: Stage2Analysis):
        """Compare Stage 1 vs Stage 2 for consistency"""
        
        self.debug_step_separator("STAGE COMPARISON & VALIDATION", 3)
        
        print("🔍 CONSISTENCY CHECK:")
        print(f"   Stage 1 said this is {stage1.research_field} research")
        print(f"   Stage 2 analysis should reflect {stage1.research_field} expertise")
        
        print(f"\n📊 STAGE 1 vs STAGE 2 COMPARISON:")
        
        print(f"\n🎯 FIELD RELEVANCE:")
        print(f"   Stage 1 Field: {stage1.research_field}")
        field_keywords = stage1.research_field.lower().split()
        
        # Check if Stage 2 debates mention field-relevant terms
        stage2_text = ' '.join(stage2.field_specific_debates).lower()
        field_matches = sum(1 for keyword in field_keywords if keyword in stage2_text)
        print(f"   Stage 2 field keyword matches: {field_matches}/{len(field_keywords)}")
        
        print(f"\n🔬 EXPERTISE ALIGNMENT:")
        print(f"   Stage 1 Required Expertise: {', '.join(stage1.required_expertise)}")
        
        expertise_text = ' '.join(stage2.expert_level_details).lower()
        expertise_matches = 0
        for expertise in stage1.required_expertise:
            if any(word in expertise_text for word in expertise.lower().split()):
                expertise_matches += 1
        print(f"   Stage 2 expertise alignment: {expertise_matches}/{len(stage1.required_expertise)}")
        
        print(f"\n✅ QUALITY ASSESSMENT:")
        if field_matches >= len(field_keywords) // 2:
            print(f"   ✅ Good field relevance")
        else:
            print(f"   ❌ Poor field relevance - analysis seems generic")
        
        if expertise_matches >= len(stage1.required_expertise) // 2:
            print(f"   ✅ Good expertise alignment")
        else:
            print(f"   ❌ Poor expertise alignment - analysis not specialized enough")
        
        return field_matches >= len(field_keywords) // 2 and expertise_matches >= len(stage1.required_expertise) // 2
    
    def _parse_stage1_understanding(self, response: str) -> Stage1Understanding:
        """Parse simple Stage 1 response"""
        
        # Initialize defaults
        research_field = "General Research"
        paper_topic = "Research paper"
        main_approach = "Unknown approach"
        key_finding = "Research findings"
        required_expertise = []
        research_type = "Unknown"
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            line_clean = line.replace('**', '').replace('*', '').strip()
            
            if 'research field' in line_clean.lower() and ':' in line:
                research_field = line.split(':', 1)[1].strip()
            elif 'paper topic' in line_clean.lower() and ':' in line:
                paper_topic = line.split(':', 1)[1].strip()
            elif 'main approach' in line_clean.lower() and ':' in line:
                main_approach = line.split(':', 1)[1].strip()
            elif 'key finding' in line_clean.lower() and ':' in line:
                key_finding = line.split(':', 1)[1].strip()
            elif 'research type' in line_clean.lower() and ':' in line:
                research_type = line.split(':', 1)[1].strip()
            elif 'required expertise' in line_clean.lower():
                current_section = 'expertise'
                if ':' in line:
                    expertise_text = line.split(':', 1)[1].strip()
                    if expertise_text:
                        required_expertise.extend([e.strip() for e in expertise_text.split(',')])
            elif current_section == 'expertise' and line.startswith(('-', '•', '*')):
                expertise_item = line.strip('- •*').strip()
                if expertise_item:
                    required_expertise.append(expertise_item)
        
        return Stage1Understanding(
            research_field=research_field,
            paper_topic=paper_topic,
            main_approach=main_approach,
            key_finding=key_finding,
            required_expertise=required_expertise[:5],  # Limit to 5
            research_type=research_type
        )
    
    def _parse_stage2_analysis(self, response: str) -> Stage2Analysis:
        """Parse detailed Stage 2 response"""
        
        detailed_methodology = []
        specific_contributions = []
        evidence_assessment = []
        field_specific_debates = []
        expert_level_details = []
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            line_upper = line.upper()
            
            # Section detection
            if 'DETAILED METHODOLOGY' in line_upper:
                current_section = 'methodology'
            elif 'SPECIFIC CONTRIBUTIONS' in line_upper:
                current_section = 'contributions'
            elif 'EVIDENCE ASSESSMENT' in line_upper:
                current_section = 'evidence'
            elif 'FIELD-SPECIFIC DEBATES' in line_upper or 'FIELD SPECIFIC DEBATES' in line_upper:
                current_section = 'debates'
            elif 'EXPERT-LEVEL DETAILS' in line_upper or 'EXPERT LEVEL DETAILS' in line_upper:
                current_section = 'details'
            elif line.startswith(('-', '•', '*', '[')) and len(line) > 20:
                # Extract content
                content = line.strip('- •*[]').strip()
                if current_section == 'methodology':
                    detailed_methodology.append(content)
                elif current_section == 'contributions':
                    specific_contributions.append(content)
                elif current_section == 'evidence':
                    evidence_assessment.append(content)
                elif current_section == 'debates':
                    field_specific_debates.append(content)
                elif current_section == 'details':
                    expert_level_details.append(content)
        
        return Stage2Analysis(
            detailed_methodology=detailed_methodology,
            specific_contributions=specific_contributions,
            evidence_assessment=evidence_assessment,
            field_specific_debates=field_specific_debates,
            expert_level_details=expert_level_details
        )


def test_smart_two_stage_approach(pdf_path: str):
    """Test the smart two-stage approach"""
    
    print("🧠 SMART TWO-STAGE ANALYSIS TEST")
    print("Stage 1: Simple Understanding → Stage 2: Targeted Analysis")
    print("=" * 100)
    
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print(f"📄 Testing with: {pdf_file.name}")
    
    # Initialize processors
    pdf_processor = PDFProcessor()
    smart_analyzer = SmartTwoStageAnalyzer()
    
    if not smart_analyzer.test_connection():
        print("❌ Ollama connection failed")
        return False
    
    try:
        # Extract PDF
        paper_data = pdf_processor.process_paper(pdf_path)
        raw_text = paper_data["raw_text"]
        
        # Enhanced section detection
        core_sections = smart_analyzer.enhanced_section_detection(raw_text)
        
        if not core_sections:
            print("❌ No core sections found")
            return False
        
        print(f"✅ Found sections: {list(core_sections.keys())}")
        
        # STAGE 1: Simple Understanding
        stage1_understanding = smart_analyzer.stage1_simple_understanding(core_sections)
        
        # STAGE 2: Targeted Analysis
        stage2_analysis = smart_analyzer.stage2_targeted_analysis(stage1_understanding, raw_text)
        
        # Display Stage 2 results
        print(f"\n📊 STAGE 2 DETAILED RESULTS:")
        print(f"   🔬 Methodology points: {len(stage2_analysis.detailed_methodology)}")
        for i, point in enumerate(stage2_analysis.detailed_methodology[:3], 1):
            print(f"      {i}. {point[:80]}...")
        
        print(f"   💡 Contributions: {len(stage2_analysis.specific_contributions)}")
        for i, contrib in enumerate(stage2_analysis.specific_contributions[:3], 1):
            print(f"      {i}. {contrib[:80]}...")
        
        print(f"   📊 Evidence assessment: {len(stage2_analysis.evidence_assessment)}")
        for i, evidence in enumerate(stage2_analysis.evidence_assessment[:3], 1):
            print(f"      {i}. {evidence[:80]}...")
        
        print(f"   ⚔️ Field-specific debates: {len(stage2_analysis.field_specific_debates)}")
        for i, debate in enumerate(stage2_analysis.field_specific_debates[:3], 1):
            print(f"      {i}. {debate[:80]}...")
        
        print(f"   🎯 Expert details: {len(stage2_analysis.expert_level_details)}")
        for i, detail in enumerate(stage2_analysis.expert_level_details[:3], 1):
            print(f"      {i}. {detail[:80]}...")
        
        # STAGE 3: Comparison & Validation
        consistency_good = smart_analyzer.compare_stages(stage1_understanding, stage2_analysis)
        
        print(f"\n🎯 FINAL ASSESSMENT:")
        if consistency_good:
            print("✅ EXCELLENT: Stages are consistent and field-relevant!")
            print("✅ Analysis properly targeted based on paper's actual field")
        else:
            print("⚠️ INCONSISTENT: Stage 2 analysis doesn't match Stage 1 field identification")
            print("🔧 Need to improve Stage 2 prompts for better field alignment")
        
        return consistency_good
        
    except Exception as e:
        print(f"❌ Smart two-stage test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    
    print("🧠 Smart Two-Stage Analysis Approach")
    print("Testing: Simple Understanding → Targeted Expert Analysis")
    print("-" * 80)
    
    default_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = default_path
    
    print(f"📄 Testing smart approach with: {pdf_path}")
    
    success = test_smart_two_stage_approach(pdf_path)
    
    if success:
        print(f"\n🎉 SMART TWO-STAGE APPROACH SUCCESS!")
        print(f"✅ Stage 1: Correctly identified field and required expertise")
        print(f"✅ Stage 2: Analysis properly targeted to that field")
        print(f"✅ Consistency: Both stages align and are relevant")
        print(f"\n🚀 This approach should give much more relevant analysis!")
    else:
        print(f"\n🔧 APPROACH NEEDS REFINEMENT")
        print(f"Check the stage comparison for specific issues")


if __name__ == "__main__":
    main()
