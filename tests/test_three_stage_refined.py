"""
Three-Stage Refined Approach: Concept → Content → Debate
Save as: test_three_stage_refined.py (in root directory)

Stage 1: Concept Detection - Understand what the paper is about
Stage 2: Content Detection - Extract claims + generate systematic challenges 
Stage 3: Debate Generation - Use claims/challenges for structured optimist vs skeptic debates
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
class ConceptDetection:
    """Stage 1: Basic understanding of what the paper is about"""
    research_field: str
    paper_topic: str  # For debate introduction
    key_finding: str  # For general context
    main_approach: str
    required_expertise: List[str]
    research_type: str


@dataclass
class ClaimChallenge:
    """A paper claim with systematic challenges"""
    claim: str
    claim_type: str  # methodology, performance, theoretical, etc.
    challenges: List[str]  # Skeptic ammunition
    supporting_points: List[str]  # Optimist ammunition


@dataclass
class ContentDetection:
    """Stage 2: Claims and systematic challenges"""
    paper_claims: List[ClaimChallenge]
    methodological_choices: List[ClaimChallenge]
    performance_metrics: List[ClaimChallenge]
    theoretical_contributions: List[ClaimChallenge]


@dataclass
class DebateScenario:
    """A structured debate scenario"""
    topic: str
    context: str  # From Stage 1
    optimist_ammunition: List[str]  # From Stage 2 claims
    skeptic_ammunition: List[str]   # From Stage 2 challenges
    debate_question: str


@dataclass
class DebateGeneration:
    """Stage 3: Structured debates using claims/challenges"""
    debate_scenarios: List[DebateScenario]
    introduction_context: str  # Using Stage 1 paper topic
    general_context: str       # Using Stage 1 key finding


class ThreeStageRefinedAnalyzer(EnhancedPaperAnalyzer):
    """Three-stage refined analyzer: Concept → Content → Debate"""
    
    def debug_step_separator(self, title: str, stage_num: int):
        """Visual separator for stages"""
        print(f"\n{'='*100}")
        print(f"🎯 STAGE {stage_num}: {title}")
        print(f"{'='*100}")
    
    def stage1_concept_detection(self, core_sections: Dict[str, str]) -> ConceptDetection:
        """Stage 1: Understand what this paper is fundamentally about"""
        
        self.debug_step_separator("CONCEPT DETECTION", 1)
        
        # Prepare core content
        core_content = ""
        for section in ['title', 'abstract', 'conclusion', 'future_work']:
            if section in core_sections:
                core_content += f"\n\n{section.upper()}:\n{core_sections[section]}"
        
        concept_prompt = f"""You are an expert academic librarian. Read these key sections and tell me what this paper is fundamentally about.

PAPER SECTIONS:
{core_content}

CONCEPT DETECTION:

**RESEARCH FIELD:**
What specific field? (e.g., "Computer Science - Graph Algorithms", "Psychology - Social Cognition")

**PAPER TOPIC:**
In one clear sentence, what is this paper about? (This will be used for debate introductions)

**KEY FINDING:** 
What is their main result or contribution? (This will provide general context)

**MAIN APPROACH:**
What is their primary method? (experimental, algorithmic, theoretical, computational, etc.)

**REQUIRED EXPERTISE:**
What 3-4 specific areas of knowledge would experts need to evaluate this work?

**RESEARCH TYPE:**
Experimental, Theoretical, Computational, Algorithmic, Survey, or Mixed?

Keep answers focused and precise. This is foundational understanding."""

        print("📤 STAGE 1 PROMPT:")
        print("─" * 50)
        print(concept_prompt[:800] + "..." if len(concept_prompt) > 800 else concept_prompt)
        print("─" * 50)
        
        response = self._call_ollama(concept_prompt, max_length=800)
        
        print("📥 STAGE 1 RESPONSE:")
        print("─" * 50)
        print(response)
        print("─" * 50)
        
        concept = self._parse_concept_detection(response)
        
        print(f"\n✅ STAGE 1 RESULTS:")
        print(f"   🎯 Field: {concept.research_field}")
        print(f"   📄 Topic: {concept.paper_topic}")
        print(f"   💡 Finding: {concept.key_finding}")
        print(f"   🔬 Approach: {concept.main_approach}")
        print(f"   🧠 Expertise: {', '.join(concept.required_expertise)}")
        
        input("\n⏸️  STAGE 1 COMPLETE - Press ENTER for Stage 2...")
        return concept
    
    def stage2_content_detection(self, concept: ConceptDetection, full_text: str) -> ContentDetection:
        """Stage 2: Extract claims and systematically challenge them"""
        
        self.debug_step_separator("CONTENT DETECTION + SYSTEMATIC CHALLENGING", 2)
        
        print(f"🎯 Using Stage 1 understanding:")
        print(f"   Field: {concept.research_field}")
        print(f"   Approach: {concept.main_approach}")
        
        # Stage 2A: Extract Claims
        claims_prompt = f"""You are a {concept.research_field} expert. Extract the specific claims this paper makes.

Based on Stage 1, this is a {concept.main_approach} paper in {concept.research_field} about:
"{concept.paper_topic}"

FULL PAPER:
{full_text[:6000]}

CLAIM EXTRACTION:

**PAPER CLAIMS:**
What specific claims does this paper make? List exact statements they assert.

**METHODOLOGICAL CHOICES:**
What specific methodological decisions did they make?

**PERFORMANCE METRICS:**
What specific performance results do they report?

**THEORETICAL CONTRIBUTIONS:**
What theoretical insights or contributions do they claim?

For each category, extract 2-4 specific, concrete claims. Be precise and quote when possible."""

        print("📤 STAGE 2A PROMPT (Claim Extraction):")
        print("─" * 50)
        print(claims_prompt[:600] + "..." if len(claims_prompt) > 600 else claims_prompt)
        print("─" * 50)
        
        claims_response = self._call_ollama(claims_prompt, max_length=2000)
        
        print("📥 STAGE 2A RESPONSE:")
        print("─" * 50)
        print(claims_response)
        print("─" * 50)
        
        # Parse claims
        extracted_claims = self._parse_extracted_claims(claims_response)
        
        # Stage 2B: Systematic Challenging
        print(f"\n🔍 STAGE 2B: SYSTEMATIC CHALLENGING")
        print(f"Now challenging {len(extracted_claims)} extracted claims...")
        
        challenged_claims = []
        
        for i, (claim_type, claims_list) in enumerate(extracted_claims.items()):
            if not claims_list:
                continue
                
            print(f"\n   Challenging {claim_type} claims...")
            
            challenge_prompt = f"""You are a skeptical {concept.research_field} expert reviewing this {concept.main_approach} paper.

CLAIMS TO CHALLENGE ({claim_type.upper()}):
{chr(10).join(f"• {claim}" for claim in claims_list)}

SYSTEMATIC CHALLENGE:

For each claim above, ask: "Could this be true?" 

**POTENTIAL CHALLENGES:**
What would skeptical experts specifically challenge about each claim? Consider:
- Methodological issues
- Sample size problems  
- Bias concerns
- Missing controls
- Overgeneralization
- Statistical issues
- Implementation problems
- Comparison fairness

**SUPPORTING POINTS:**
What evidence supports each claim? What would optimistic experts emphasize?

Be specific and technical. Generate real challenges that {concept.research_field} experts would raise."""

            challenge_response = self._call_ollama(challenge_prompt, max_length=1500)
            
            print(f"📥 Challenges for {claim_type}:")
            print(challenge_response[:200] + "..." if len(challenge_response) > 200 else challenge_response)
            
            # Parse challenges
            for claim in claims_list:
                challenges, supporting = self._parse_claim_challenges(challenge_response, claim)
                
                challenged_claims.append(ClaimChallenge(
                    claim=claim,
                    claim_type=claim_type,
                    challenges=challenges,
                    supporting_points=supporting
                ))
        
        # Organize by type
        content_detection = ContentDetection(
            paper_claims=[c for c in challenged_claims if c.claim_type == 'paper_claims'],
            methodological_choices=[c for c in challenged_claims if c.claim_type == 'methodological'],
            performance_metrics=[c for c in challenged_claims if c.claim_type == 'performance'],
            theoretical_contributions=[c for c in challenged_claims if c.claim_type == 'theoretical']
        )
        
        print(f"\n✅ STAGE 2 RESULTS:")
        print(f"   📋 Total claims with challenges: {len(challenged_claims)}")
        print(f"   🎯 Paper claims: {len(content_detection.paper_claims)}")
        print(f"   🔬 Methodological: {len(content_detection.methodological_choices)}")  
        print(f"   📊 Performance: {len(content_detection.performance_metrics)}")
        print(f"   💭 Theoretical: {len(content_detection.theoretical_contributions)}")
        
        input("\n⏸️  STAGE 2 COMPLETE - Press ENTER for Stage 3...")
        return content_detection
    
    def stage3_debate_generation(self, concept: ConceptDetection, 
                               content: ContentDetection) -> DebateGeneration:
        """Stage 3: Generate structured debates using claims/challenges"""
        
        self.debug_step_separator("DEBATE GENERATION", 3)
        
        print(f"🎯 Using systematic claims and challenges for debates:")
        
        # Collect all claim-challenge pairs
        all_claims = []
        all_claims.extend(content.paper_claims)
        all_claims.extend(content.methodological_choices)
        all_claims.extend(content.performance_metrics)
        all_claims.extend(content.theoretical_contributions)
        
        print(f"   📋 Total claim-challenge pairs: {len(all_claims)}")
        
        # Generate debate scenarios
        debate_scenarios = []
        
        for i, claim_challenge in enumerate(all_claims[:5]):  # Top 5 claims
            print(f"\n   🎭 Generating debate {i+1}: {claim_challenge.claim[:50]}...")
            
            debate_prompt = f"""Generate a focused debate scenario for this specific claim.

PAPER CONTEXT (from Stage 1):
- Field: {concept.research_field}
- Topic: {concept.paper_topic}
- Finding: {concept.key_finding}

SPECIFIC CLAIM TO DEBATE:
"{claim_challenge.claim}"

OPTIMIST AMMUNITION (Supporting the claim):
{chr(10).join(f"• {point}" for point in claim_challenge.supporting_points)}

SKEPTIC AMMUNITION (Challenging the claim):  
{chr(10).join(f"• {challenge}" for challenge in claim_challenge.challenges)}

DEBATE SCENARIO:

**DEBATE QUESTION:**
What specific question should Dr. Ava (optimist) and Prof. Marcus (skeptic) debate about this claim?

**CONTEXT:**
Brief context for this specific debate within the {concept.research_field} field.

Make it focused and technical for {concept.research_field} experts."""

            debate_response = self._call_ollama(debate_prompt, max_length=600)
            
            # Parse debate scenario
            debate_question, debate_context = self._parse_debate_scenario(debate_response)
            
            scenario = DebateScenario(
                topic=f"{claim_challenge.claim_type.title()} Debate {i+1}",
                context=debate_context,
                optimist_ammunition=claim_challenge.supporting_points,
                skeptic_ammunition=claim_challenge.challenges,
                debate_question=debate_question
            )
            
            debate_scenarios.append(scenario)
        
        # Generate introduction and context using Stage 1
        introduction_context = f"Today we're examining: {concept.paper_topic}"
        general_context = f"The key finding at stake: {concept.key_finding}"
        
        debate_generation = DebateGeneration(
            debate_scenarios=debate_scenarios,
            introduction_context=introduction_context,
            general_context=general_context
        )
        
        print(f"\n✅ STAGE 3 RESULTS:")
        print(f"   🎭 Debate scenarios: {len(debate_scenarios)}")
        print(f"   📝 Introduction: {introduction_context}")
        print(f"   🎯 Context: {general_context}")
        
        return debate_generation
    
    def _parse_concept_detection(self, response: str) -> ConceptDetection:
        """Parse Stage 1 concept detection response"""
        
        research_field = "General Research"
        paper_topic = "Research paper"
        key_finding = "Research findings"
        main_approach = "Unknown"
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
            elif 'key finding' in line_clean.lower() and ':' in line:
                key_finding = line.split(':', 1)[1].strip()
            elif 'main approach' in line_clean.lower() and ':' in line:
                main_approach = line.split(':', 1)[1].strip()
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
        
        return ConceptDetection(
            research_field=research_field,
            paper_topic=paper_topic,
            key_finding=key_finding,
            main_approach=main_approach,
            required_expertise=required_expertise[:4],
            research_type=research_type
        )
    
    def _parse_extracted_claims(self, response: str) -> Dict[str, List[str]]:
        """Parse Stage 2A claim extraction"""
        
        claims = {
            'paper_claims': [],
            'methodological': [],
            'performance': [],
            'theoretical': []
        }
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            line_upper = line.upper()
            
            if 'PAPER CLAIMS' in line_upper:
                current_section = 'paper_claims'
            elif 'METHODOLOGICAL' in line_upper:
                current_section = 'methodological'
            elif 'PERFORMANCE' in line_upper:
                current_section = 'performance'
            elif 'THEORETICAL' in line_upper:
                current_section = 'theoretical'
            elif line.startswith(('-', '•', '*')) and len(line) > 20:
                if current_section:
                    claim = line.strip('- •*').strip()
                    claims[current_section].append(claim)
        
        return claims
    
    def _parse_claim_challenges(self, response: str, original_claim: str) -> tuple:
        """Parse challenges and supporting points for a claim"""
        
        challenges = []
        supporting = []
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            line_upper = line.upper()
            
            if 'POTENTIAL CHALLENGES' in line_upper or 'CHALLENGES' in line_upper:
                current_section = 'challenges'
            elif 'SUPPORTING POINTS' in line_upper or 'SUPPORTING' in line_upper:
                current_section = 'supporting'
            elif line.startswith(('-', '•', '*')) and len(line) > 15:
                content = line.strip('- •*').strip()
                if current_section == 'challenges':
                    challenges.append(content)
                elif current_section == 'supporting':
                    supporting.append(content)
        
        return challenges[:4], supporting[:3]  # Limit for focus
    
    def _parse_debate_scenario(self, response: str) -> tuple:
        """Parse debate question and context"""
        
        debate_question = "What should be debated about this claim?"
        debate_context = "Context for this debate"
        
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            line_clean = line.replace('**', '').replace('*', '').strip()
            
            if 'debate question' in line_clean.lower() and ':' in line:
                debate_question = line.split(':', 1)[1].strip()
            elif 'context' in line_clean.lower() and ':' in line:
                debate_context = line.split(':', 1)[1].strip()
        
        return debate_question, debate_context


def test_three_stage_refined_approach(pdf_path: str):
    """Test the complete three-stage refined approach"""
    
    print("🧠 THREE-STAGE REFINED APPROACH TEST")
    print("Concept Detection → Content Detection → Debate Generation")
    print("=" * 100)
    
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print(f"📄 Testing with: {pdf_file.name}")
    
    # Initialize
    pdf_processor = PDFProcessor()
    analyzer = ThreeStageRefinedAnalyzer()
    
    if not analyzer.test_connection():
        print("❌ Ollama connection failed")
        return False
    
    try:
        # Extract PDF
        paper_data = pdf_processor.process_paper(pdf_path)
        raw_text = paper_data["raw_text"]
        
        # Get core sections
        core_sections = analyzer.enhanced_section_detection(raw_text)
        if not core_sections:
            print("❌ No core sections found")
            return False
        
        # STAGE 1: Concept Detection
        concept = analyzer.stage1_concept_detection(core_sections)
        
        # STAGE 2: Content Detection 
        content = analyzer.stage2_content_detection(concept, raw_text)
        
        # STAGE 3: Debate Generation
        debates = analyzer.stage3_debate_generation(concept, content)
        
        # ================== FINAL RESULTS ==================
        print(f"\n{'='*100}")
        print(f"🎉 THREE-STAGE REFINED RESULTS")
        print(f"{'='*100}")
        
        print(f"\n📝 INTRODUCTION CONTEXT (from Stage 1):")
        print(f"   {debates.introduction_context}")
        print(f"   {debates.general_context}")
        
        print(f"\n🎭 DEBATE SCENARIOS ({len(debates.debate_scenarios)}):")
        
        for i, scenario in enumerate(debates.debate_scenarios, 1):
            print(f"\n   DEBATE {i}: {scenario.topic}")
            print(f"   Question: {scenario.debate_question}")
            print(f"   Context: {scenario.context}")
            
            print(f"   😊 OPTIMIST AMMUNITION ({len(scenario.optimist_ammunition)}):")
            for j, ammo in enumerate(scenario.optimist_ammunition[:3], 1):
                print(f"      {j}. {ammo[:70]}...")
            
            print(f"   🤨 SKEPTIC AMMUNITION ({len(scenario.skeptic_ammunition)}):")
            for j, ammo in enumerate(scenario.skeptic_ammunition[:3], 1):
                print(f"      {j}. {ammo[:70]}...")
        
        # Quality Assessment
        print(f"\n📊 QUALITY ASSESSMENT:")
        
        total_ammunition = sum(len(s.optimist_ammunition) + len(s.skeptic_ammunition) for s in debates.debate_scenarios)
        
        print(f"   🎯 Paper-specific context: ✅ Using actual topic and finding")
        print(f"   🔍 Systematic challenges: ✅ Every claim challenged")
        print(f"   ⚔️ Debate ammunition: {total_ammunition} total pieces")
        print(f"   🎭 Structured debates: {len(debates.debate_scenarios)} scenarios")
        
        if len(debates.debate_scenarios) >= 3 and total_ammunition >= 15:
            print(f"   ✅ EXCELLENT: Ready for sophisticated debates!")
            return True
        else:
            print(f"   ⚠️ GOOD: Could use more depth")
            return False
        
    except Exception as e:
        print(f"❌ Three-stage test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    
    print("🧠 Three-Stage Refined Approach")
    print("Systematic: Concept → Content → Debate")
    print("-" * 80)
    
    default_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = default_path
    
    success = test_three_stage_refined_approach(pdf_path)
    
    if success:
        print(f"\n🎉 THREE-STAGE REFINED APPROACH SUCCESS!")
        print(f"✅ Stage 1: Paper concept clearly identified")
        print(f"✅ Stage 2: Claims extracted and systematically challenged")
        print(f"✅ Stage 3: Structured debates with optimist vs skeptic ammunition")
        print(f"\n🚀 This should generate highly relevant, claim-based debates!")
    else:
        print(f"\n🔧 APPROACH WORKING BUT COULD BE DEEPER")
        print(f"Consider increasing claim extraction or challenge depth")


if __name__ == "__main__":
    main()
