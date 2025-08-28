"""
Enhanced Claims → Challenges Approach (Fully Flexible)
Save as: test_enhanced_claims_challenges.py (in root directory)

No hard coding - works for ANY paper type and field.
Stage 1: Simple Understanding → Stage 2: Claims → Challenges → Evidence Assessment
"""

import sys
import os
import re
import time
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple

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
    """Simple understanding from core sections"""
    research_field: str
    paper_topic: str
    main_approach: str
    key_finding: str
    required_expertise: List[str]
    research_type: str


@dataclass
class PaperClaim:
    """A specific claim from the paper with evidence and challenges"""
    claim_text: str
    supporting_evidence: List[str]
    potential_challenges: List[str]
    evidence_strength: str


@dataclass
class EnhancedStage2Results:
    """Enhanced Stage 2 results with claims, challenges, and debate ammunition"""
    paper_claims: List[PaperClaim]
    debate_ammunition: Dict[str, List[str]]  # optimist vs skeptic
    introduction_material: Dict[str, str]  # for debate intro
    evidence_assessment: Dict[str, str]


class EnhancedClaimsChallengesAnalyzer(EnhancedPaperAnalyzer):
    """Flexible analyzer using claims → challenges approach"""
    
    def debug_step_separator(self, title: str, step: str):
        """Visual separator for debug steps"""
        print(f"\n{'='*100}")
        print(f"🎯 {step}: {title}")
        print(f"{'='*100}")
    
    def stage1_simple_understanding(self, core_sections: Dict[str, str]) -> Stage1Understanding:
        """Stage 1: Simple field identification (same as before)"""
        
        self.debug_step_separator("SIMPLE UNDERSTANDING & FIELD IDENTIFICATION", "STAGE 1")
        
        # Prepare core content
        core_content = ""
        for section in ['title', 'abstract', 'conclusion', 'future_work']:
            if section in core_sections:
                core_content += f"\n\n{section.upper()}:\n{core_sections[section]}"
        
        # Flexible Stage 1 prompt - works for any field
        stage1_prompt = f"""You are an academic librarian categorizing research papers. Quickly understand what this paper is about.

PAPER SECTIONS:
{core_content}

UNDERSTANDING TASK (be brief and specific):

**RESEARCH FIELD:**
What specific field is this? (e.g., "Computer Science - Algorithms", "Psychology - Cognitive", "Biology - Genetics", etc.)

**PAPER TOPIC:**  
In one sentence: what is this paper about?

**MAIN APPROACH:**
What is their primary method? (experimental, theoretical, computational, analytical, survey, etc.)

**KEY FINDING:**
What is their main result or contribution?

**REQUIRED EXPERTISE:**
What 3-5 specific expertise areas would someone need to evaluate this paper?

**RESEARCH TYPE:**
Experimental, Theoretical, Computational, Survey, Case Study, or Mixed?

Keep answers concise and field-appropriate."""

        print("📤 STAGE 1 PROMPT:")
        print("─" * 50)
        print(stage1_prompt[:800] + "..." if len(stage1_prompt) > 800 else stage1_prompt)
        print("─" * 50)
        
        response = self._call_ollama(stage1_prompt, max_length=800)
        
        print("\n📥 STAGE 1 RESPONSE:")
        print("─" * 50)
        print(response)
        print("─" * 50)
        
        understanding = self._parse_stage1_understanding(response)
        
        print(f"\n📊 STAGE 1 RESULTS:")
        print(f"   🎯 Field: {understanding.research_field}")
        print(f"   📄 Topic: {understanding.paper_topic}")
        print(f"   🔬 Approach: {understanding.main_approach}")
        print(f"   💡 Key Finding: {understanding.key_finding}")
        print(f"   🧠 Expertise: {', '.join(understanding.required_expertise)}")
        print(f"   📊 Type: {understanding.research_type}")
        
        # input("\n⏸️  STAGE 1 COMPLETE - Press ENTER for Enhanced Stage 2...")
        
        return understanding
    
    def stage2_enhanced_claims_challenges(self, stage1: Stage1Understanding, 
                                        full_text: str) -> EnhancedStage2Results:
        """Enhanced Stage 2: Claims → Challenges → Evidence Assessment"""
        
        self.debug_step_separator("ENHANCED CLAIMS → CHALLENGES ANALYSIS", "STAGE 2")
        
        print(f"🎯 USING STAGE 1 FINDINGS:")
        print(f"   Field: {stage1.research_field}")
        print(f"   Topic: {stage1.paper_topic}")
        print(f"   Type: {stage1.research_type}")
        
        # Stage 2A: Extract Claims
        claims = self._extract_paper_claims(stage1, full_text)
        
        # Stage 2B: Challenge Claims  
        challenged_claims = self._challenge_claims(stage1, claims, full_text)
        
        # Stage 2C: Assess Evidence
        evidence_assessment = self._assess_evidence_strength(stage1, challenged_claims)
        
        # Generate debate ammunition
        debate_ammunition = self._generate_debate_ammunition(stage1, challenged_claims)
        
        # Prepare introduction material
        introduction_material = self._prepare_introduction_material(stage1, challenged_claims)
        
        return EnhancedStage2Results(
            paper_claims=challenged_claims,
            debate_ammunition=debate_ammunition,
            introduction_material=introduction_material,
            evidence_assessment=evidence_assessment
        )
    
    def _extract_paper_claims(self, stage1: Stage1Understanding, full_text: str) -> List[str]:
        """Stage 2A: Extract specific claims from the paper"""
        
        print("\n🎯 STAGE 2A: EXTRACTING PAPER CLAIMS")
        
        # Dynamic prompt based on Stage 1 findings
        claims_prompt = f"""You are a {stage1.research_field} expert reviewing a {stage1.research_type.lower()} paper.

PAPER CONTEXT:
Topic: {stage1.paper_topic}
Key Finding: {stage1.key_finding}
Required Expertise: {', '.join(stage1.required_expertise)}

FULL PAPER TEXT:
{full_text[:6000]}

TASK: Extract the paper's main claims and contributions with supporting evidence.

**MAIN CLAIMS:**
List 5 specific claims the authors make:

1. [Specific claim about methodology/approach]
2. [Specific claim about results/performance]  
3. [Specific claim about significance/impact]
4. [Specific claim about novelty/contribution]
5. [Specific claim about applications/implications]

**SUPPORTING EVIDENCE:**
For each claim, what evidence do they provide?

1. [Evidence for claim 1]
2. [Evidence for claim 2]
3. [Evidence for claim 3]
4. [Evidence for claim 4]
5. [Evidence for claim 5]

Be specific and quote/reference exact details from the paper."""

        print("📤 CLAIMS EXTRACTION PROMPT:")
        print("─" * 50)
        print(claims_prompt[:600] + "..." if len(claims_prompt) > 600 else claims_prompt)
        print("─" * 50)
        
        claims_response = self._call_ollama(claims_prompt, max_length=2000)
        
        print("\n📥 CLAIMS RESPONSE:")
        print("─" * 50)
        print(claims_response)
        print("─" * 50)
        
        # Parse claims and evidence
        claims_with_evidence = self._parse_claims_and_evidence(claims_response)
        
        print(f"\n📊 EXTRACTED {len(claims_with_evidence)} CLAIMS:")
        for i, (claim, evidence) in enumerate(claims_with_evidence, 1):
            print(f"   {i}. CLAIM: {claim[:80]}...")
            print(f"      EVIDENCE: {evidence[:80]}...")
        
        # input("\n⏸️  Press ENTER for Claims Challenge Analysis...")
        
        return claims_with_evidence
    
    def _challenge_claims(self, stage1: Stage1Understanding, 
                         claims_with_evidence: List[Tuple[str, str]], 
                         full_text: str) -> List[PaperClaim]:
        """Stage 2B: Challenge each claim with expert skepticism"""
        
        print("\n🎯 STAGE 2B: CHALLENGING CLAIMS WITH EXPERT SKEPTICISM")
        
        challenged_claims = []
        
        for i, (claim, evidence) in enumerate(claims_with_evidence, 1):
            print(f"\n🔍 CHALLENGING CLAIM {i}: {claim[:60]}...")
            
            # Dynamic challenge prompt - no hard coding
            challenge_prompt = f"""You are a skeptical {stage1.research_field} expert reviewing this {stage1.research_type.lower()} paper.

PAPER CONTEXT:
Field: {stage1.research_field}
Required Expertise: {', '.join(stage1.required_expertise)}

SPECIFIC CLAIM TO CHALLENGE:
"{claim}"

AUTHOR'S EVIDENCE:
"{evidence}"

EXPERT SKEPTICAL ANALYSIS:

**COULD THIS BE TRUE?**
As a {stage1.research_field} expert, what are your concerns about this claim?

**POTENTIAL CHALLENGES:**
What would experts in {stage1.research_field} challenge about this claim?
- [Challenge 1: methodological concern]
- [Challenge 2: evidence quality concern] 
- [Challenge 3: scope/generalization concern]
- [Challenge 4: comparison/baseline concern]
- [Challenge 5: interpretation concern]

**WHAT COULD GO WRONG?**
What assumptions, limitations, or gaps could undermine this claim?

**MISSING EVIDENCE:**
What evidence would strengthen this claim that might be missing?

Be specific and technical - think like an expert peer reviewer."""

            challenge_response = self._call_ollama(challenge_prompt, max_length=1500)
            
            # Parse challenges
            challenges = self._parse_claim_challenges(challenge_response)
            
            # Create PaperClaim object
            paper_claim = PaperClaim(
                claim_text=claim,
                supporting_evidence=[evidence],
                potential_challenges=challenges,
                evidence_strength="to_be_assessed"
            )
            
            challenged_claims.append(paper_claim)
            
            print(f"   ✅ Generated {len(challenges)} challenges for this claim")
        
        # input("\n⏸️  Press ENTER for Evidence Strength Assessment...")
        
        return challenged_claims
    
    def _assess_evidence_strength(self, stage1: Stage1Understanding, 
                                challenged_claims: List[PaperClaim]) -> Dict[str, str]:
        """Stage 2C: Assess evidence strength for each claim"""
        
        print("\n🎯 STAGE 2C: EVIDENCE STRENGTH ASSESSMENT")
        
        evidence_assessment = {}
        
        for i, claim_obj in enumerate(challenged_claims, 1):
            print(f"\n📊 ASSESSING EVIDENCE STRENGTH FOR CLAIM {i}")
            
            # Flexible evidence assessment prompt
            assessment_prompt = f"""You are a {stage1.research_field} expert evaluating evidence quality.

CLAIM: "{claim_obj.claim_text}"

SUPPORTING EVIDENCE: "{claim_obj.supporting_evidence[0]}"

POTENTIAL CHALLENGES: {'; '.join(claim_obj.potential_challenges[:3])}

EVIDENCE ASSESSMENT:

**EVIDENCE STRENGTH:**
Rate the evidence as: STRONG, MODERATE, WEAK, or INSUFFICIENT

**ASSESSMENT REASONING:**
Why did you give this rating? Consider:
- Quality of methodology for {stage1.research_type} research
- Appropriateness for {stage1.research_field} standards
- Strength relative to the claim being made

**WHAT WOULD CONVINCE SKEPTICS:**
What additional evidence would make this claim more convincing?

Be objective and consider both the claim's ambition and the evidence provided."""

            assessment_response = self._call_ollama(assessment_prompt, max_length=800)
            
            # Extract strength rating
            strength = self._extract_evidence_strength(assessment_response)
            claim_obj.evidence_strength = strength
            
            evidence_assessment[f"claim_{i}"] = assessment_response
            
            print(f"   📊 Evidence Strength: {strength.upper()}")
        
        return evidence_assessment
    
    def _generate_debate_ammunition(self, stage1: Stage1Understanding, 
                                  claims: List[PaperClaim]) -> Dict[str, List[str]]:
        """Generate optimist vs skeptic debate ammunition"""
        
        print("\n🎯 GENERATING DEBATE AMMUNITION")
        
        optimist_ammunition = []
        skeptic_ammunition = []
        
        for claim in claims:
            # Optimist ammunition: strong claims + evidence
            if claim.evidence_strength in ['strong', 'moderate']:
                optimist_point = f"{claim.claim_text} - {claim.supporting_evidence[0][:100]}..."
                optimist_ammunition.append(optimist_point)
            
            # Skeptic ammunition: challenges + weak evidence
            for challenge in claim.potential_challenges[:2]:  # Top 2 challenges
                skeptic_ammunition.append(challenge)
            
            if claim.evidence_strength in ['weak', 'insufficient']:
                skeptic_point = f"Weak evidence for claim: {claim.claim_text[:80]}..."
                skeptic_ammunition.append(skeptic_point)
        
        print(f"   😊 Optimist points: {len(optimist_ammunition)}")
        print(f"   🤨 Skeptic points: {len(skeptic_ammunition)}")
        
        return {
            "optimist": optimist_ammunition,
            "skeptic": skeptic_ammunition
        }
    
    def _prepare_introduction_material(self, stage1: Stage1Understanding, 
                                     claims: List[PaperClaim]) -> Dict[str, str]:
        """Prepare material for debate introduction using Stage 1 results"""
        
        print("\n🎯 PREPARING INTRODUCTION MATERIAL")
        
        # Use Stage 1 paper topic and key finding as requested
        paper_topic = stage1.paper_topic
        key_finding = stage1.key_finding
        research_field = stage1.research_field
        
        # Count strong vs weak claims for intro tension
        strong_claims = sum(1 for claim in claims if claim.evidence_strength in ['strong', 'moderate'])
        weak_claims = sum(1 for claim in claims if claim.evidence_strength in ['weak', 'insufficient'])
        
        introduction_material = {
            "paper_topic": paper_topic,
            "key_finding": key_finding,
            "research_field": research_field,
            "debate_tension": f"{strong_claims} strong claims vs {weak_claims} questionable claims",
            "intro_hook": f"Today we're examining {research_field.lower()} research on {paper_topic.lower()}. The authors claim {key_finding.lower()}, but is this genuine breakthrough or overstated results?"
        }
        
        print(f"   🎬 Intro hook: {introduction_material['intro_hook'][:100]}...")
        
        return introduction_material
    
    def _parse_stage1_understanding(self, response: str) -> Stage1Understanding:
        """Parse Stage 1 response (flexible for any field)"""
        
        # Initialize defaults
        research_field = "General Research"
        paper_topic = "Research paper"
        main_approach = "Unknown"
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
            required_expertise=required_expertise[:5],
            research_type=research_type
        )
    
    def _parse_claims_and_evidence(self, response: str) -> List[Tuple[str, str]]:
        """Parse claims and their supporting evidence"""
        
        claims_with_evidence = []
        
        # Look for numbered claims and evidence sections
        lines = response.split('\n')
        claims = []
        evidence = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if 'MAIN CLAIMS' in line.upper():
                current_section = 'claims'
                continue
            elif 'SUPPORTING EVIDENCE' in line.upper():
                current_section = 'evidence'
                continue
            
            # Extract numbered items
            if line.startswith(('1.', '2.', '3.', '4.', '5.')):
                content = line.split('.', 1)[1].strip()
                content = content.strip('[]')  # Remove brackets if present
                
                if current_section == 'claims':
                    claims.append(content)
                elif current_section == 'evidence':
                    evidence.append(content)
        
        # Pair claims with evidence
        for i in range(min(len(claims), len(evidence))):
            claims_with_evidence.append((claims[i], evidence[i]))
        
        # If we have more claims than evidence, pair with empty evidence
        for i in range(len(evidence), len(claims)):
            claims_with_evidence.append((claims[i], "No specific evidence provided"))
        
        return claims_with_evidence
    
    def _parse_claim_challenges(self, response: str) -> List[str]:
        """Parse challenges from response"""
        
        challenges = []
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith(('-', '•', '*', '[')) and len(line) > 30:
                challenge = line.strip('- •*[]').strip()
                if challenge and len(challenge) > 20:
                    challenges.append(challenge)
        
        return challenges[:5]  # Top 5 challenges
    
    def _extract_evidence_strength(self, response: str) -> str:
        """Extract evidence strength rating"""
        
        response_upper = response.upper()
        
        if 'STRONG' in response_upper and 'INSUFFICIENT' not in response_upper:
            return 'strong'
        elif 'MODERATE' in response_upper:
            return 'moderate'
        elif 'WEAK' in response_upper:
            return 'weak'
        elif 'INSUFFICIENT' in response_upper:
            return 'insufficient'
        else:
            return 'unknown'


def test_enhanced_claims_challenges(pdf_path: str):
    """Test the enhanced claims → challenges approach"""
    
    print("🧠 ENHANCED CLAIMS → CHALLENGES ANALYSIS TEST")
    print("Stage 1: Understanding → Stage 2: Claims → Challenges → Evidence → Debates")
    print("=" * 100)
    
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print(f"📄 Testing with: {pdf_file.name}")
    
    # Initialize processors
    pdf_processor = PDFProcessor()
    enhanced_analyzer = EnhancedClaimsChallengesAnalyzer()
    
    if not enhanced_analyzer.test_connection():
        print("❌ Ollama connection failed")
        return False
    
    try:
        # Extract PDF
        paper_data = pdf_processor.process_paper(pdf_path)
        raw_text = paper_data["raw_text"]
        
        # Enhanced section detection
        core_sections = enhanced_analyzer.enhanced_section_detection(raw_text)
        
        if not core_sections:
            print("❌ No core sections found")
            return False
        
        # STAGE 1: Simple Understanding
        stage1_understanding = enhanced_analyzer.stage1_simple_understanding(core_sections)
        
        # ENHANCED STAGE 2: Claims → Challenges → Evidence Assessment
        stage2_results = enhanced_analyzer.stage2_enhanced_claims_challenges(stage1_understanding, raw_text)
        
        # Display comprehensive results
        print(f"\n{'='*100}")
        print(f"🎉 ENHANCED ANALYSIS COMPLETE!")
        print(f"{'='*100}")
        
        # Introduction Material
        intro = stage2_results.introduction_material
        print(f"\n🎬 INTRODUCTION MATERIAL:")
        print(f"   📄 Paper Topic: {intro['paper_topic']}")
        print(f"   💡 Key Finding: {intro['key_finding']}")
        print(f"   🎯 Research Field: {intro['research_field']}")
        print(f"   🎭 Debate Tension: {intro['debate_tension']}")
        print(f"   🎤 Intro Hook: {intro['intro_hook']}")
        
        # Claims Analysis
        claims = stage2_results.paper_claims
        print(f"\n📋 CLAIMS ANALYSIS ({len(claims)} claims):")
        
        for i, claim in enumerate(claims, 1):
            print(f"\n   {i}. CLAIM: {claim.claim_text[:100]}...")
            print(f"      📊 Evidence Strength: {claim.evidence_strength.upper()}")
            print(f"      ✅ Supporting Evidence: {len(claim.supporting_evidence)} items")
            print(f"      ⚔️ Potential Challenges: {len(claim.potential_challenges)} items")
            
            if claim.potential_challenges:
                print(f"      🤨 Sample Challenge: {claim.potential_challenges[0][:80]}...")
        
        # Debate Ammunition
        ammunition = stage2_results.debate_ammunition
        print(f"\n⚔️ DEBATE AMMUNITION:")
        print(f"   😊 Optimist Points: {len(ammunition['optimist'])}")
        for i, point in enumerate(ammunition['optimist'][:3], 1):
            print(f"      {i}. {point[:400]}...")
        
        print(f"   🤨 Skeptic Points: {len(ammunition['skeptic'])}")
        for i, point in enumerate(ammunition['skeptic'][:3], 1):
            print(f"      {i}. {point[:400]}...")
        
        # Quality Assessment
        print(f"\n📊 QUALITY ASSESSMENT:")
        
        strong_claims = sum(1 for claim in claims if claim.evidence_strength == 'strong')
        moderate_claims = sum(1 for claim in claims if claim.evidence_strength == 'moderate')
        weak_claims = sum(1 for claim in claims if claim.evidence_strength in ['weak', 'insufficient'])
        
        print(f"   📈 Evidence Quality: {strong_claims} strong, {moderate_claims} moderate, {weak_claims} weak")
        print(f"   ⚔️ Debate Balance: {len(ammunition['optimist'])} vs {len(ammunition['skeptic'])} points")
        print(f"   🎬 Introduction Ready: ✅ Paper topic and key finding identified")
        
        total_score = len(claims) * 2 + len(ammunition['optimist']) + len(ammunition['skeptic'])
        
        print(f"   🏆 Total Content Score: {total_score}/50")
        
        if total_score >= 30:
            print("\n✅ EXCELLENT: Rich content for sophisticated debates!")
        elif total_score >= 20:
            print("\n✅ GOOD: Solid foundation for academic debates")  
        else:
            print("\n⚠️ MODERATE: May need more detailed analysis")
        
        return total_score >= 20
        
    except Exception as e:
        print(f"❌ Enhanced analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    
    print("🧠 Enhanced Claims → Challenges Analysis")
    print("Fully Flexible - Works with Any Paper Type")
    print("-" * 80)
    
    default_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = default_path
    
    success = test_enhanced_claims_challenges(pdf_path)
    
    if success:
        print(f"\n🎉 ENHANCED APPROACH SUCCESS!")
        print(f"✅ Paper-specific claims identified and challenged")
        print(f"✅ Evidence strength assessed for each claim")
        print(f"✅ Balanced debate ammunition generated")
        print(f"✅ Introduction material ready from Stage 1")
        print(f"\n🚀 Ready for sophisticated, paper-specific debates!")
    else:
        print(f"\n🔧 APPROACH NEEDS REFINEMENT")


if __name__ == "__main__":
    main()
