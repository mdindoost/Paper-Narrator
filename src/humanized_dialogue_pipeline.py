"""
Humanized Dialogue Pipeline - Natural Academic Conversations
Save as: src/humanized_dialogue_pipeline.py

Refines existing pipeline to make dialogue more human and natural.
Keeps structure but adds humanization layer for authentic academic conversations.
"""

import sys
import os
import re
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

# Import existing components
sys.path.append('.')
from integrated_enhanced_pipeline import (
    IntegratedEnhancedPipeline, 
    ConversationScript,
    ConversationTurn
)


@dataclass
class VoiceProfile:
    name: str
    voice_id: str
    description: str
    gender: str


class HumanizedDialogueRefiner:
    """Refines dialogue to sound more human and natural"""
    
    def __init__(self, ollama_model: str = "llama3.1:8b"):
        self.ollama_model = ollama_model
        self.api_url = "http://localhost:11434/api/generate"
        
        # CORRECTED: Voice assignments based on your specifications
        self.voice_profiles = {
            "host": VoiceProfile("Host", "en-US-GuyNeural", "Professional male narrator", "male"),
            "dr_ava": VoiceProfile("Dr. Ava D.", "en-US-JennyNeural", "Enthusiastic female researcher", "female"), 
            "prof_marcus": VoiceProfile("Prof. Marcus W.", "en-US-ChristopherNeural", "Skeptical male professor", "male")
        }
        
        print("🎭 Humanized Dialogue Refiner Initialized")
        print("Voice Assignments:")
        for key, profile in self.voice_profiles.items():
            print(f"   {profile.name}: {profile.voice_id} ({profile.gender} - {profile.description})")
    
    def _call_ollama(self, prompt: str, max_length: int = 800) -> str:
        """Call Ollama for humanization"""
        import requests
        import json
        
        payload = {
            "model": self.ollama_model,
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
            return f"[Humanization error: {str(e)}]"
    
    def clean_field_classification(self, field_text: str) -> str:
        """Extract the most specific field part and remove formatting"""
        
        # Remove markdown symbols
        cleaned = re.sub(r'\*+', '', field_text).strip()
        
        # If it has " - " split and take the most specific part (after the dash)
        if ' - ' in cleaned:
            parts = cleaned.split(' - ')
            # Take the last part (most specific)
            specific_field = parts[-1].strip()
            return specific_field
        
        return cleaned
    
    def remove_category_labels(self, text: str) -> str:
        """Remove category label prefixes that make dialogue robotic"""
        
        # Common category labels to remove
        category_patterns = [
            r'^[A-Z][a-z\s]+:\s*',  # "Lack of context: ", "Segmentation Faults: "
            r'^[A-Z][A-Z\s]+:\s*',  # "WEAK EVIDENCE: "
            r'^\d+\.\s*[A-Z][^:]+:\s*',  # "1. Sample Size Issues: "
            r'^-\s*[A-Z][^:]+:\s*',  # "- Statistical Problems: "
        ]
        
        cleaned = text
        for pattern in category_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.MULTILINE)
        
        return cleaned.strip()
    
    def humanize_introduction(self, introduction: str, research_field: str, 
                            paper_topic: str, key_finding: str) -> str:
        """Humanize the introduction with cleaned field and natural language"""
        
        print("🎬 Humanizing introduction...")
        
        # Clean the field classification
        clean_field = self.clean_field_classification(research_field)
        
        # Remove formatting artifacts
        clean_intro = re.sub(r'\*+', '', introduction)
        clean_intro = re.sub(r'#{1,6}\s*', '', clean_intro)
        
        # Fix broken sentences like "Today's fascinating topic: **"
        clean_intro = re.sub(r':\s*\*+\s*', ': ', clean_intro)
        clean_intro = re.sub(r'\*+\s*([A-Z])', r'\1', clean_intro)  # "** Computer" -> "Computer"
        
        # Replace field references with cleaned version
        if clean_field != research_field:
            clean_intro = clean_intro.replace(research_field, clean_field)
        
        # Fix the claims counting issue
        claims_pattern = r'(\d+)\s+strong claims vs\s+(\d+)\s+questionable claims'
        clean_intro = re.sub(claims_pattern, 'compelling evidence alongside some methodological concerns', clean_intro)
        
        # Humanization prompt
        humanization_prompt = f"""Transform this podcast introduction to sound more natural and engaging. Keep the same structure and information, but make it flow better and sound like a real host speaking naturally.

ORIGINAL INTRODUCTION:
{clean_intro}

REQUIREMENTS:
- Keep it enthusiastic and professional
- Remove any remaining formatting artifacts
- Make it sound conversational and natural
- Keep the research focus on {clean_field}
- Maintain the setup for the debate between Dr. Ava D. and Prof. Marcus W.

NATURAL INTRODUCTION:"""

        humanized = self._call_ollama(humanization_prompt, max_length=600)
        
        if "error" not in humanized.lower():
            return humanized
        else:
            # Fallback: manual cleanup
            return self._manual_introduction_cleanup(clean_intro, clean_field)
    
    def _manual_introduction_cleanup(self, intro: str, field: str) -> str:
        """Manual fallback for introduction cleanup"""
        
        # Basic cleanup patterns
        intro = re.sub(r'\*+', '', intro)
        intro = re.sub(r':\s*\*+\s*', ': ', intro)
        intro = re.sub(r'\d+ strong claims vs \d+ questionable claims', 
                      'compelling evidence alongside some methodological questions', intro)
        
        return intro.strip()
    
    def humanize_dialogue_turn(self, turn: ConversationTurn) -> ConversationTurn:
        """Humanize individual dialogue turn to sound natural"""
        
        print(f"🎭 Humanizing turn: {turn.speaker}")
        
        # Step 1: Remove category labels
        cleaned_content = self.remove_category_labels(turn.content)
        
        # Step 2: Remove markdown and formatting
        cleaned_content = re.sub(r'\*+', '', cleaned_content)
        cleaned_content = re.sub(r'#{1,6}\s*', '', cleaned_content)
        
        # Step 3: Determine speaker personality for humanization
        if "ava" in turn.speaker.lower() or "sarah" in turn.speaker.lower():
            speaker_style = "enthusiastic and optimistic researcher who gets excited about potential breakthroughs"
        elif "marcus" in turn.speaker.lower() or "webb" in turn.speaker.lower():
            speaker_style = "methodical and skeptical professor who focuses on rigorous evidence and potential flaws"
        else:
            speaker_style = "neutral academic"
        
        # Step 4: Humanization prompt
        humanization_prompt = f"""Transform this academic point into natural, conversational dialogue. The speaker is {turn.speaker}, a {speaker_style}.

ORIGINAL CONTENT:
{cleaned_content}

REQUIREMENTS:
- Make it sound like a real person speaking in an academic discussion
- Keep the core arguments but make the language natural and conversational
- Remove any remaining category labels or robotic language
- Show the speaker's personality through their word choice and tone
- Keep it to 2-3 sentences maximum
- Make it engaging for a podcast audience

NATURAL DIALOGUE:"""

        humanized_content = self._call_ollama(humanization_prompt, max_length=400)
        
        if "error" in humanized_content.lower():
            # Fallback: basic cleanup
            humanized_content = self._manual_dialogue_cleanup(cleaned_content, turn.speaker)
        
        # Create new turn with humanized content
        return ConversationTurn(
            speaker=turn.speaker,
            speaker_role=turn.speaker_role,
            content=humanized_content,
            topic=turn.topic,
            turn_number=turn.turn_number,
            source_type=turn.source_type
        )
    
    def _manual_dialogue_cleanup(self, content: str, speaker: str) -> str:
        """Manual fallback for dialogue cleanup"""
        
        # Basic cleanup
        content = self.remove_category_labels(content)
        content = re.sub(r'\*+', '', content)
        
        # Add natural speaking patterns based on speaker
        if "ava" in speaker.lower():
            if not content.startswith(("I think", "I believe", "What's exciting", "I'm fascinated")):
                content = f"What's fascinating is that {content.lower()}"
        elif "marcus" in speaker.lower():
            if not content.startswith(("I'm concerned", "I have doubts", "My concern", "I'm skeptical")):
                content = f"I'm concerned about {content.lower()}"
        
        return content
    
    def humanize_conclusion(self, conclusion: str) -> str:
        """Humanize the conclusion"""
        
        print("🎯 Humanizing conclusion...")
        
        # Clean formatting
        clean_conclusion = re.sub(r'\*+', '', conclusion)
        clean_conclusion = re.sub(r'#{1,6}\s*', '', clean_conclusion)
        
        # Humanization prompt
        humanization_prompt = f"""Make this podcast conclusion sound more natural and engaging. Keep the same information but make it flow better as natural speech.

ORIGINAL CONCLUSION:
{clean_conclusion}

REQUIREMENTS:
- Sound like a real podcast host wrapping up the discussion
- Keep it warm and engaging
- Maintain the academic focus
- Make it conversational and natural

NATURAL CONCLUSION:"""

        humanized = self._call_ollama(humanization_prompt, max_length=400)
        
        if "error" not in humanized.lower():
            return humanized
        else:
            return clean_conclusion
    
    def refine_conversation_script(self, script: ConversationScript, 
                                 research_field: str) -> ConversationScript:
        """Refine entire conversation script for natural human dialogue"""
        
        print("🎭 REFINING CONVERSATION SCRIPT FOR NATURAL DIALOGUE")
        print("=" * 60)
        
        # 1. Humanize introduction
        humanized_introduction = self.humanize_introduction(
            script.introduction, research_field, script.paper_topic, script.key_finding
        )
        
        # 2. Humanize each dialogue turn
        humanized_turns = []
        for turn in script.turns:
            # Fix speaker name (Webb -> W.)
            if "Webb" in turn.speaker:
                turn.speaker = turn.speaker.replace("Webb", "W.")
            
            humanized_turn = self.humanize_dialogue_turn(turn)
            humanized_turns.append(humanized_turn)
        
        # 3. Humanize conclusion
        humanized_conclusion = self.humanize_conclusion(script.conclusion)
        
        # 4. Create refined script
        refined_script = ConversationScript(
            title=script.title,
            paper_topic=script.paper_topic,
            introduction=humanized_introduction,
            turns=humanized_turns,
            conclusion=humanized_conclusion,
            total_turns=len(humanized_turns),
            duration_estimate=script.duration_estimate,
            research_field=self.clean_field_classification(research_field),
            key_finding=script.key_finding
        )
        
        print(f"✅ Script refinement complete:")
        print(f"   🎬 Introduction: Humanized and cleaned")
        print(f"   💬 Dialogue turns: {len(humanized_turns)} turns humanized")
        print(f"   🎯 Conclusion: Natural and engaging")
        print(f"   🎯 Field: {refined_script.research_field}")
        
        return refined_script
    
    def get_voice_profile(self, speaker: str) -> VoiceProfile:
        """Get correct voice profile for speaker"""
        
        speaker_lower = speaker.lower()
        
        if "narrator" in speaker_lower or "host" in speaker_lower:
            return self.voice_profiles["host"]
        elif "ava" in speaker_lower or "sarah" in speaker_lower:
            return self.voice_profiles["dr_ava"]
        elif "marcus" in speaker_lower or "webb" in speaker_lower:
            return self.voice_profiles["prof_marcus"]
        else:
            return self.voice_profiles["host"]  # Default


class HumanizedEnhancedPipeline:
    """Enhanced pipeline with humanization layer"""
    
    def __init__(self):
        self.base_pipeline = IntegratedEnhancedPipeline()
        self.dialogue_refiner = HumanizedDialogueRefiner()
    
    def check_prerequisites(self) -> bool:
        """Check prerequisites"""
        return self.base_pipeline.check_prerequisites()
    
    def process_paper_humanized(self, pdf_path: str, max_exchanges: int = 6) -> tuple:
        """Process paper with humanized dialogue refinement"""
        
        print("🚀 HUMANIZED ENHANCED PIPELINE")
        print("Base analysis + Dialogue humanization for natural conversations")
        print("=" * 80)
        
        # Step 1-6: Run base pipeline
        complete_result, conversation_script, audio_result, stage1, stage2 = (
            self.base_pipeline.process_paper_enhanced_pipeline(pdf_path, max_exchanges)
        )
        
        # Step 7: Humanize dialogue
        print("\n🎭 Step 7: Humanizing Dialogue for Natural Conversations...")
        
        refined_script = self.dialogue_refiner.refine_conversation_script(
            conversation_script, stage1.research_field
        )
        
        # Step 8: Generate audio with humanized script and correct voices
        print("\n🎤 Step 8: Generating Audio with Humanized Dialogue...")
        
        # Update audio generator with correct voice profiles
        enhanced_audio_gen = self.base_pipeline.audio_generator
        enhanced_audio_gen.voice_profiles = {
            "narrator": enhanced_audio_gen.VoiceProfile("Narrator", "en-US-GuyNeural", "Professional male narrator"),
            "dr_ava": enhanced_audio_gen.VoiceProfile("Dr. Ava D.", "en-US-JennyNeural", "Enthusiastic female researcher"),
            "prof_marcus": enhanced_audio_gen.VoiceProfile("Prof. Marcus W.", "en-US-ChristopherNeural", "Skeptical male professor")
        }
        
        # Generate humanized audio
        base_filename = Path(pdf_path).stem
        humanized_audio_result = enhanced_audio_gen.generate_complete_enhanced_audio(
            refined_script, f"{base_filename}_HUMANIZED"
        )
        
        # Update results
        complete_result["humanized_dialogue"] = {
            "refinement_applied": True,
            "natural_conversations": True,
            "voice_corrections": "Host=Male, Ava=Female, Marcus=Male"
        }
        
        print(f"\n🎉 HUMANIZED PIPELINE COMPLETE!")
        print(f"✅ Natural, engaging academic conversations generated")
        print(f"✅ Correct voice assignments applied")
        print(f"✅ Category labels removed and content humanized")
        
        return (complete_result, refined_script, humanized_audio_result, 
                stage1, stage2)


def test_humanized_pipeline():
    """Test the complete humanized pipeline"""
    
    print("🎭 TESTING HUMANIZED DIALOGUE PIPELINE")
    print("Generating natural academic conversations")
    print("=" * 80)
    
    pipeline = HumanizedEnhancedPipeline()
    
    if not pipeline.check_prerequisites():
        print("❌ Prerequisites not met")
        return False
    
    pdf_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    try:
        results = pipeline.process_paper_humanized(pdf_path, max_exchanges=6)
        complete_result, refined_script, audio_result, stage1, stage2 = results
        
        print(f"\n📊 HUMANIZED RESULTS SUMMARY:")
        print(f"   🎯 Research Field: {refined_script.research_field}")
        print(f"   📄 Paper Topic: {refined_script.paper_topic}")
        print(f"   💬 Dialogue Turns: {len(refined_script.turns)}")
        print(f"   🎤 Audio Duration: {audio_result['total_duration']:.1f}s")
        
        # Show sample of humanized dialogue
        print(f"\n🎭 SAMPLE HUMANIZED DIALOGUE:")
        print(f"Introduction: {refined_script.introduction[:100]}...")
        
        if refined_script.turns:
            first_turn = refined_script.turns[0]
            print(f"{first_turn.speaker}: {first_turn.content[:100]}...")
        
        print(f"\nConclusion: {refined_script.conclusion[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Humanized pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_humanized_pipeline()
