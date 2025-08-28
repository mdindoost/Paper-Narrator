"""
Cohesive Dialogue Generator - New Professional Structure
Save as: src/cohesive_dialogue_generator.py

New Structure:
1. Narrator Intro
2. Dr. Ava D's Complete Case (cohesive flowing speech)
3. Narrator Transition  
4. Prof. Marcus W's Complete Case (cohesive flowing speech)
5. Narrator Conclusion
"""

import requests
import json
import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from src.personalities_updated import UpdatedResearchPersonalities


@dataclass
class CohesiveTurn:
    """Represents one cohesive speech segment"""
    speaker: str
    speaker_role: str
    content: str
    segment_type: str  # "intro", "optimist_case", "transition", "skeptic_case", "conclusion"
    points_covered: List[str]  # The original ammunition points used


@dataclass
class CohesiveConversationScript:
    """Complete cohesive conversation script"""
    title: str
    paper_topic: str
    segments: List[CohesiveTurn]
    total_segments: int
    duration_estimate: str
    research_field: str
    key_finding: str


class CohesiveDialogueGenerator:
    """Generates cohesive, professional dialogue in debate format"""
    
    def __init__(self, model_name: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        self.personalities = UpdatedResearchPersonalities()
    
    def _clean_ai_response(self, response: str) -> str:
        """Clean AI response to remove meta-text and ensure proper speaker identity"""
        
        print(f"\n🔧 CLEANING AI RESPONSE:")
        print(f"Before cleaning: {response[:200]}...")
        
        cleaned = response.strip()
        
        # Remove meta-text that AI sometimes adds
        meta_patterns = [
            r'^Here is the.*?introduction[:\.]?\s*',
            r'^HOST:\s*',
            r'^NARRATOR:\s*', 
            r'^Dr\.?\s*Ava\s*D\.?:\s*',
            r'^Prof\.?\s*Marcus\s*W\.?:\s*',
            r'^Here is.*?analysis[:\.]?\s*',
            r'^Here is.*?speech[:\.]?\s*',
            r'^The following is.*?[:\.]?\s*'
        ]
        
        for pattern in meta_patterns:
            old_cleaned = cleaned
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
            if old_cleaned != cleaned:
                print(f"   ✅ Removed meta-text: {pattern}")
        
        # Fix incomplete names - REMOVED because AI generates correct names already
        # The issue was our patterns were matching and duplicating correct names
        name_fixes = [
            # Only fix actual wrong names, not incomplete ones
            (r'\bDr Rachel Chen\b', 'Dr. Ava D.'),
            (r'\bDr\. Rachel Chen\b', 'Dr. Ava D.'),  
            (r'\bDr Racheal Chen\b', 'Dr. Ava D.'),
            (r'\bDr\. Racheal Chen\b', 'Dr. Ava D.'),
            (r'\bRachel Chen\b', 'Dr. Ava D.'),
            (r'\bRacheal Chen\b', 'Dr. Ava D.')
        ]
        
        for wrong_pattern, correct_name in name_fixes:
            old_cleaned = cleaned
            cleaned = re.sub(wrong_pattern, correct_name, cleaned, flags=re.IGNORECASE)
            if old_cleaned != cleaned:
                print(f"   ✅ Fixed name pattern: {wrong_pattern} → {correct_name}")
        
        # Remove metadata that might slip through (USER'S SPECIFIC ISSUE)
        metadata_patterns = [
            r'\bestimation time[:\s]*[^.]*',
            r'\bduration[:\s]*[~\d\s]*minutes?[^.]*',
            r'\btotal[:\s]*\d+[^.]*',
            r'\bsegments?[:\s]*\d+[^.]*'
        ]
        
        for pattern in metadata_patterns:
            old_cleaned = cleaned
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
            if old_cleaned != cleaned:
                print(f"   ✅ Removed metadata: {pattern}")
        
        # Ensure external expert language (not author language)
        author_language_fixes = [
            (r'\bour research\b', 'this research'),
            (r'\bour study\b', 'this study'),
            (r'\bour findings\b', 'the findings'),
            (r'\bour methodology\b', 'the methodology'),
            (r'\bour approach\b', 'their approach'),
            (r'\bwe found\b', 'the authors found'),
            (r'\bwe discovered\b', 'the research shows'),
            (r'\bwe developed\b', 'the authors developed'),
            (r'\bour results\b', 'the results')
        ]
        
        for wrong_pattern, correct_replacement in author_language_fixes:
            old_cleaned = cleaned
            cleaned = re.sub(wrong_pattern, correct_replacement, cleaned, flags=re.IGNORECASE)
            if old_cleaned != cleaned:
                print(f"   ✅ Fixed author language: {wrong_pattern} → {correct_replacement}")
        
        # Clean up any double spaces or punctuation issues
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = re.sub(r'\s*([,.!?])', r'\1', cleaned)
        
        print(f"After cleaning: {cleaned[:200]}...")
        print(f"🔧 CLEANING COMPLETE")
        
        return cleaned.strip()
    
    def _call_ollama(self, prompt: str, max_length: int = 800) -> str:
        """Call Ollama API for dialogue generation"""
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
            response = requests.post(self.api_url, json=payload, timeout=120)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except Exception as e:
            return f"[Error generating cohesive response: {str(e)}]"
    
    def generate_narrator_intro(self, stage1, stage2) -> CohesiveTurn:
        """Generate professional narrator introduction"""
        
        print("🎬 Generating cohesive narrator introduction...")
        
        paper_topic = stage2.introduction_material.get("paper_topic", stage1.paper_topic)
        key_finding = stage1.key_finding
        research_field = stage1.research_field
        
        intro_prompt = f"""You are the narrator/host of "Research Rundown" podcast. Generate ONLY the narrator's introduction speech.

PAPER DETAILS:
Topic: {paper_topic}
Field: {research_field}
Key Finding: {key_finding}

Create a 30-45 second professional introduction. You are introducing a debate between:
- Dr. Ava D. (the optimistic researcher)
- Prof. Marcus W. (the skeptical analyst)

CRITICAL REQUIREMENTS:
- Start directly with "Welcome to Research Rundown!"
- Always use FULL NAMES: "Dr. Ava D." and "Prof. Marcus W." - NEVER just "Dr." or "Prof."
- Do NOT include any meta-text like "Here is the introduction" or "HOST:"
- Make it clear these are EXTERNAL EXPERTS analyzing the research, NOT the paper authors
- Keep it engaging and professional for YouTube audience

Generate ONLY the narrator's speech that will be read aloud:"""
        
        intro_content = self._call_ollama(intro_prompt, max_length=400)
        intro_content = self._clean_ai_response(intro_content)
        
        return CohesiveTurn(
            speaker="Narrator",
            speaker_role="Host",
            content=intro_content,
            segment_type="intro",
            points_covered=["introduction"]
        )
    
    def generate_dr_ava_cohesive_case(self, stage1, optimist_ammunition: List[str]) -> CohesiveTurn:
        """Generate Dr. Ava D's complete cohesive case"""
        
        print(f"🔬 Generating Dr. Ava D's cohesive case from {len(optimist_ammunition)} points...")
        
        # Get personality
        optimist_personality = self.personalities.get_personality("optimist")
        
        # Prepare ammunition for AI
        ammunition_text = "\n".join([f"- {point}" for point in optimist_ammunition])
        
        cohesive_prompt = f"""You are Dr. Ava D., an independent research expert analyzing this paper. You are NOT one of the paper authors.

PAPER CONTEXT (you are analyzing this research):
Field: {stage1.research_field}
Topic: {stage1.paper_topic}
Key Finding: {stage1.key_finding}

YOUR ROLE: Independent expert giving optimistic analysis of someone else's research.

YOUR AMMUNITION (evidence and positive points about this research):
{ammunition_text}

CRITICAL REQUIREMENTS:
- You are Dr. Ava D., analyzing this research as an EXTERNAL EXPERT
- Do NOT say "we did this" or "our research" - you are reviewing someone else's work
- Say things like "the authors achieved", "this research demonstrates", "the paper shows"
- Be enthusiastic about the research potential while being clear you're an outside analyst
- Do NOT include any meta-text or stage directions

Create a cohesive 2-3 minute speech that:
1. Opens with enthusiasm about the research potential
2. Presents 3-4 connected points that build on each other
3. Uses smooth transitions between points
4. Maintains your optimistic, visionary personality
5. Ends with exciting implications for the future

Make it flow like one natural speech. Sound enthusiastic but professional.

Dr. Ava D's analysis:"""
        
        cohesive_content = self._call_ollama(cohesive_prompt, max_length=1200)
        cohesive_content = self._clean_ai_response(cohesive_content)  # Clean the response
        
        return CohesiveTurn(
            speaker=optimist_personality.name,
            speaker_role=optimist_personality.role,
            content=cohesive_content,
            segment_type="optimist_case",
            points_covered=optimist_ammunition
        )
    
    def generate_narrator_transition(self) -> CohesiveTurn:
        """Generate narrator transition between speakers"""
        
        print("🔄 Generating narrator transition...")
        
        transition_content = "Fascinating perspective from Dr. Ava D. Now let's hear Prof. Marcus W's analysis of this research."
        
        return CohesiveTurn(
            speaker="Narrator",
            speaker_role="Host",
            content=transition_content,
            segment_type="transition",
            points_covered=["transition"]
        )
    
    def generate_prof_marcus_cohesive_case(self, stage1, skeptic_ammunition: List[str]) -> CohesiveTurn:
        """Generate Prof. Marcus W's complete cohesive case"""
        
        print(f"🧐 Generating Prof. Marcus W's cohesive case from {len(skeptic_ammunition)} points...")
        
        # Get personality
        skeptic_personality = self.personalities.get_personality("skeptic")
        
        # Prepare ammunition for AI
        ammunition_text = "\n".join([f"- {point}" for point in skeptic_ammunition])
        
        cohesive_prompt = f"""You are Prof. Marcus W., an independent research expert analyzing this paper. You are NOT one of the paper authors.

PAPER CONTEXT (you are analyzing this research):
Field: {stage1.research_field}
Topic: {stage1.paper_topic}
Key Finding: {stage1.key_finding}

YOUR ROLE: Independent expert giving critical analysis of someone else's research.

YOUR AMMUNITION (concerns and critical points about this research):
{ammunition_text}

CRITICAL REQUIREMENTS:
- You are Prof. Marcus W., analyzing this research as an EXTERNAL EXPERT
- Do NOT say "we did this" or "our methodology" - you are reviewing someone else's work
- Say things like "the authors claim", "this research lacks", "the paper fails to address"
- Be skeptical about the research while being clear you're an outside analyst
- Do NOT include any meta-text or stage directions

Create a cohesive 2-3 minute speech that:
1. Opens with measured skepticism about the claims
2. Presents 3-4 connected analytical concerns that build on each other  
3. Uses smooth transitions between points
4. Maintains your rigorous, methodical personality
5. Ends with what evidence would be needed to convince you

Make it flow like one natural analytical speech. Sound skeptical but fair and professional.

Prof. Marcus W's analysis:"""
        
        cohesive_content = self._call_ollama(cohesive_prompt, max_length=1200)
        cohesive_content = self._clean_ai_response(cohesive_content)  # Clean the response
        
        return CohesiveTurn(
            speaker=skeptic_personality.name,
            speaker_role=skeptic_personality.role,
            content=cohesive_content,
            segment_type="skeptic_case", 
            points_covered=skeptic_ammunition
        )
    
    def generate_narrator_conclusion(self, stage1, stage2) -> CohesiveTurn:
        """Generate professional narrator conclusion"""
        
        print("🎯 Generating cohesive narrator conclusion...")
        
        paper_topic = stage2.introduction_material.get("paper_topic", stage1.paper_topic)
        research_field = stage1.research_field
        
        conclusion_prompt = f"""You are the narrator/host concluding the "Research Rundown" podcast episode.

PAPER DETAILS:
Topic: {paper_topic}
Field: {research_field}

The debate just concluded between:
- Dr. Ava D. (optimistic about the research potential)
- Prof. Marcus W. (skeptical about methodology and evidence)

CRITICAL REQUIREMENTS:
- Always use FULL NAMES: "Dr. Ava D." and "Prof. Marcus W." - NEVER just "Dr." or "Prof."
- Do NOT include any metadata like "duration", "estimation time", or technical details
- Do NOT include any meta-text or stage directions
- Create a clean, natural conclusion that will be read aloud

Create a 30-45 second conclusion that:
- Summarizes the key tension in the debate using FULL NAMES
- Acknowledges both perspectives have merit  
- Notes this is typical of cutting-edge research
- Thanks listeners
- Sounds natural and professional

Generate ONLY the narrator's speech that will be read aloud:"""
        
        conclusion_content = self._call_ollama(conclusion_prompt, max_length=400)
        conclusion_content = self._clean_ai_response(conclusion_content)
        
        return CohesiveTurn(
            speaker="Narrator",
            speaker_role="Host",
            content=conclusion_content,
            segment_type="conclusion",
            points_covered=["conclusion"]
        )
    
    def create_cohesive_conversation_script(self, stage1, stage2) -> CohesiveConversationScript:
        """Create complete cohesive conversation script"""
        
        print("🎭 Creating COHESIVE conversation script...")
        print("Structure: Intro → Dr. Ava D → Transition → Prof. Marcus W → Conclusion")
        
        # Extract ammunition
        optimist_ammunition = stage2.debate_ammunition["optimist"]
        skeptic_ammunition = stage2.debate_ammunition["skeptic"]
        
        print(f"   📊 Optimist ammunition: {len(optimist_ammunition)} points")
        print(f"   📊 Skeptic ammunition: {len(skeptic_ammunition)} points")
        
        # Generate all segments
        segments = []
        
        # 1. Narrator Intro
        intro_segment = self.generate_narrator_intro(stage1, stage2)
        segments.append(intro_segment)
        
        # 2. Dr. Ava D's Complete Case
        ava_segment = self.generate_dr_ava_cohesive_case(stage1, optimist_ammunition)
        segments.append(ava_segment)
        
        # 3. Narrator Transition
        transition_segment = self.generate_narrator_transition()
        segments.append(transition_segment)
        
        # 4. Prof. Marcus W's Complete Case
        marcus_segment = self.generate_prof_marcus_cohesive_case(stage1, skeptic_ammunition)
        segments.append(marcus_segment)
        
        # 5. Narrator Conclusion
        conclusion_segment = self.generate_narrator_conclusion(stage1, stage2)
        segments.append(conclusion_segment)
        
        # Calculate duration estimate
        total_words = sum(len(segment.content.split()) for segment in segments)
        duration_minutes = max(1, total_words // 150)
        
        script = CohesiveConversationScript(
            title=f"Research Rundown: {stage1.paper_topic}",
            paper_topic=stage1.paper_topic,
            segments=segments,
            total_segments=len(segments),
            duration_estimate=f"~{duration_minutes} minutes",
            research_field=stage1.research_field,
            key_finding=stage1.key_finding
        )
        
        print(f"✅ Cohesive script complete:")
        print(f"   📝 Total segments: {len(segments)}")
        print(f"   ⏱️ Duration: ~{duration_minutes} minutes")
        print(f"   🎙️ Structure: Intro → Ava Case → Transition → Marcus Case → Conclusion")
        
        return script
    
    def format_cohesive_script_for_display(self, script: CohesiveConversationScript) -> str:
        """Format the cohesive conversation script for readable display"""
        
        output = []
        output.append("🎙️  " + "=" * 60)
        output.append(f"📻 {script.title}")
        output.append(f"⏱️  Estimated Duration: {script.duration_estimate}")
        output.append("🎙️  " + "=" * 60)
        
        for i, segment in enumerate(script.segments, 1):
            segment_type_emoji = {
                "intro": "🎬",
                "optimist_case": "🔬", 
                "transition": "🔄",
                "skeptic_case": "🧐",
                "conclusion": "🎯"
            }
            
            emoji = segment_type_emoji.get(segment.segment_type, "🎤")
            
            output.append(f"\n{emoji} SEGMENT {i}: {segment.segment_type.upper()}")
            output.append(f"Speaker: {segment.speaker}")
            output.append("-" * 60)
            output.append(segment.content)
            
            if segment.segment_type in ["optimist_case", "skeptic_case"]:
                output.append(f"\nPoints Covered: {len(segment.points_covered)}")
        
        output.append(f"\n📊 STATISTICS:")
        output.append(f"   • Total segments: {script.total_segments}")
        output.append(f"   • Estimated duration: {script.duration_estimate}")
        output.append(f"   • Structure: Professional debate format")
        
        return "\n".join(output)
    
    def test_connection(self) -> bool:
        """Test if Ollama is available"""
        try:
            test_response = self._call_ollama("Hello", max_length=10)
            return len(test_response) > 5 and "Error" not in test_response
        except:
            return False


# Test function
def test_cohesive_dialogue_generator():
    """Test the cohesive dialogue generator"""
    
    print("🧪 TESTING COHESIVE DIALOGUE GENERATOR")
    print("="*60)
    
    generator = CohesiveDialogueGenerator()
    
    if not generator.test_connection():
        print("❌ Ollama connection failed")
        return False
    
    print("✅ Ollama connection successful")
    
    # Create mock data for testing
    from dataclasses import dataclass
    from test_enhanced_claims_challenges import Stage1Understanding, EnhancedStage2Results
    
    # Mock Stage 1
    mock_stage1 = Stage1Understanding(
        research_field="Algorithms and Network Analysis",
        paper_topic="Parallel Community Detection in Large-Scale Networks",
        main_approach="Computational",
        key_finding="WCC and CM algorithms achieve breakthrough scalability results",
        required_expertise=["Graph Theory", "Parallel Computing"],
        research_type="Experimental"
    )
    
    # Mock Stage 2 with debate ammunition
    mock_stage2 = EnhancedStage2Results(
        paper_claims=[],  # Not needed for this test
        debate_ammunition={
            "optimist": [
                "The WCC algorithm shows 60% performance improvement over existing methods",
                "Chapel programming language enables exceptional parallel scalability", 
                "Testing on billion-edge graphs demonstrates real-world applicability",
                "Community detection accuracy improved by 40% compared to baseline methods",
                "The approach scales linearly with processor count up to 1024 cores"
            ],
            "skeptic": [
                "Testing limited to only three datasets may not represent broader applicability",
                "Chapel language adoption is limited, reducing practical implementation potential",
                "Scalability claims lack comparison with other modern parallel frameworks",
                "Memory requirements for billion-edge graphs may be prohibitive for most users",
                "Community detection accuracy metrics don't account for false positive rates",
                "Performance improvements may not justify the complexity of implementation",
                "Results may not generalize beyond the specific graph structures tested",
                "The preprocessing overhead could dominate runtime for smaller graphs"
            ]
        },
        introduction_material={
            "paper_topic": "Parallel Community Detection in Large-Scale Networks",
            "key_finding": "WCC and CM algorithms achieve breakthrough scalability results",
            "research_field": "Algorithms and Network Analysis"
        },
        evidence_assessment={}
    )
    
    try:
        # Generate cohesive script
        cohesive_script = generator.create_cohesive_conversation_script(mock_stage1, mock_stage2)
        
        # Display results
        formatted_output = generator.format_cohesive_script_for_display(cohesive_script)
        print(f"\n{formatted_output}")
        
        print(f"\n🎉 COHESIVE DIALOGUE TEST SUCCESSFUL!")
        print(f"   ✅ Generated {cohesive_script.total_segments} cohesive segments")
        print(f"   ✅ Professional debate structure implemented")
        print(f"   ✅ Duration: {cohesive_script.duration_estimate}")
        
        return True
        
    except Exception as e:
        print(f"❌ Cohesive dialogue test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_cohesive_dialogue_generator()