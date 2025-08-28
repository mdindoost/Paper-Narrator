"""
Sophisticated Pipeline Integration with Existing YouTube System
Save as: src/sophisticated_pipeline_integration.py

Integrates the three-stage sophisticated analysis (Stage 1 + 2 + 3) with your existing
audio generation and video pipeline for YouTube content creation.

REPLACES: dialogue_generator_fixed.py with sophisticated evidence-based debates
INTEGRATES WITH: audio_generator_simple_reliable.py and phase4_video_generator.py
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass

# Import existing system components
from two_stage_analyzer import TwoStageAnalyzer, CompleteAnalysis
from stage3_sophisticated_debates import Stage3SophisticatedDebates, SophisticatedDebate


@dataclass
class SophisticatedConversationScript:
    """Sophisticated conversation script compatible with existing audio pipeline"""
    title: str
    paper_topic: str
    introduction: str
    turns: List['SophisticatedConversationTurn']
    conclusion: str
    total_turns: int
    duration_estimate: str
    sophistication_score: int
    evidence_citations: List[str]


@dataclass
class SophisticatedConversationTurn:
    """Enhanced conversation turn with evidence and technical depth"""
    speaker: str
    speaker_role: str
    content: str
    topic: str
    turn_number: int
    evidence_cited: List[str]
    technical_depth: str
    argument_type: str


class SophisticatedPipelineIntegration:
    """Integration layer for sophisticated analysis with YouTube pipeline"""
    
    def __init__(self, model_name: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.two_stage_analyzer = TwoStageAnalyzer(model_name, base_url)
        self.debate_generator = Stage3SophisticatedDebates(model_name, base_url)
    
    def create_sophisticated_conversation(self, paper_data: Dict, 
                                        max_topics: int = 3, 
                                        exchanges_per_topic: int = 4) -> SophisticatedConversationScript:
        """
        CREATE SOPHISTICATED CONVERSATION - REPLACES dialogue_generator_fixed.py
        
        This method replaces the create_full_conversation method in your existing system
        with sophisticated evidence-based debates.
        
        Args:
            paper_data: Paper data from pdf_processor (same format as existing system)
            max_topics: Number of debate topics
            exchanges_per_topic: Number of exchanges per topic
            
        Returns:
            SophisticatedConversationScript: Compatible with existing audio pipeline
        """
        
        print("🎭 Creating sophisticated evidence-based conversation...")
        
        # Step 1: Run comprehensive two-stage analysis
        raw_text = paper_data["raw_text"]
        complete_analysis = self.two_stage_analyzer.analyze_paper_complete(raw_text)
        
        if not complete_analysis.ready_for_debates:
            print(f"⚠️ Analysis quality below optimal ({complete_analysis.analysis_quality_score}/20)")
            print("   Proceeding with available evidence...")
        
        # Step 2: Generate sophisticated debate
        sophisticated_debate = self.debate_generator.generate_sophisticated_debate(
            complete_analysis, max_topics, exchanges_per_topic
        )
        
        # Step 3: Convert to format compatible with existing audio pipeline
        conversation_script = self._convert_to_conversation_script(
            sophisticated_debate, complete_analysis
        )
        
        print(f"✅ Sophisticated conversation created!")
        print(f"   🎭 {conversation_script.total_turns} turns with evidence citations")
        print(f"   🏆 Sophistication score: {conversation_script.sophistication_score}/100")
        
        return conversation_script
    
    def _convert_to_conversation_script(self, sophisticated_debate: SophisticatedDebate, 
                                      complete_analysis: CompleteAnalysis) -> SophisticatedConversationScript:
        """Convert sophisticated debate to format compatible with existing audio pipeline"""
        
        # Generate YouTube-style introduction
        introduction = self._generate_youtube_introduction(
            sophisticated_debate.paper_title, 
            complete_analysis.core_understanding.field_classification
        )
        
        # Convert debate turns to conversation turns
        conversation_turns = []
        for turn in sophisticated_debate.turns:
            conversation_turn = SophisticatedConversationTurn(
                speaker=turn.speaker,
                speaker_role=turn.speaker_role,
                content=turn.content,
                topic=sophisticated_debate.debate_topics[0] if sophisticated_debate.debate_topics else "Research Discussion",
                turn_number=turn.turn_number,
                evidence_cited=turn.evidence_cited,
                technical_depth=turn.technical_depth,
                argument_type=turn.argument_type
            )
            conversation_turns.append(conversation_turn)
        
        # Generate sophisticated conclusion
        conclusion = self._generate_sophisticated_conclusion(
            sophisticated_debate.paper_title,
            complete_analysis.core_understanding.field_classification,
            sophisticated_debate.sophistication_score
        )
        
        # Calculate duration (same logic as original system)
        total_words = sum(len(turn.content.split()) for turn in conversation_turns)
        total_words += len(introduction.split()) + len(conclusion.split())
        duration_minutes = max(1, total_words // 150)
        
        return SophisticatedConversationScript(
            title=f"Research Rundown: {sophisticated_debate.paper_title}",
            paper_topic=sophisticated_debate.paper_title,
            introduction=introduction,
            turns=conversation_turns,
            conclusion=conclusion,
            total_turns=len(conversation_turns),
            duration_estimate=f"~{duration_minutes} minutes",
            sophistication_score=sophisticated_debate.sophistication_score,
            evidence_citations=sophisticated_debate.evidence_citations
        )
    
    def _generate_youtube_introduction(self, paper_title: str, field: str) -> str:
        """Generate engaging YouTube introduction for sophisticated content"""
        
        field_descriptor = self._get_field_descriptor(field)
        
        introduction = f"""What happens when two brilliant {field_descriptor} researchers analyze the same groundbreaking paper with completely opposite viewpoints?

Welcome to Research Rundown - where evidence meets expertise!

Today we're diving deep into '{paper_title}' - and our expert researchers Dr. Ava D. and Prof. Marcus Webb are about to dissect every claim, every piece of evidence, and every methodological choice.

This isn't just opinion - this is evidence-based academic debate at its finest. Let's see what the data really says!"""
        
        return introduction
    
    def _get_field_descriptor(self, field: str) -> str:
        """Get field-appropriate descriptor for introduction"""
        
        field_lower = field.lower()
        
        if 'computer science' in field_lower or 'machine learning' in field_lower:
            return "computer science"
        elif 'biology' in field_lower or 'medical' in field_lower:
            return "biomedical"
        elif 'psychology' in field_lower or 'social' in field_lower:
            return "behavioral science"
        elif 'physics' in field_lower or 'engineering' in field_lower:
            return "engineering"
        else:
            return "research"
    
    def _generate_sophisticated_conclusion(self, paper_title: str, field: str, sophistication_score: int) -> str:
        """Generate sophisticated conclusion"""
        
        if sophistication_score >= 80:
            quality_phrase = "We've just witnessed a masterclass in evidence-based academic debate"
        elif sophistication_score >= 60:
            quality_phrase = "That was a rigorous analysis of the evidence"
        else:
            quality_phrase = "We've examined the key aspects of this research"
        
        conclusion = f"""{quality_phrase}. Dr. Ava D. and Prof. Marcus Webb brought their expertise to bear on '{paper_title}', examining not just the claims, but the evidence behind them.

This is what real academic discourse looks like - evidence-based, methodologically rigorous, and intellectually honest.

Thanks for joining us on Research Rundown. Subscribe for more evidence-based analysis of cutting-edge research, and remember - in science, the evidence always has the final word."""
        
        return conclusion
    
    def test_connection(self) -> bool:
        """Test if the sophisticated pipeline is ready"""
        return (self.two_stage_analyzer.test_connection() and 
                self.debate_generator.test_connection())


class SophisticatedDialogueEngine:
    """DROP-IN REPLACEMENT for FixedDialogueEngine in your existing system"""
    
    def __init__(self, model_name: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.integration = SophisticatedPipelineIntegration(model_name, base_url)
    
    def create_full_conversation(self, analysis_results: Dict, 
                               max_topics: int = 3, 
                               exchanges_per_topic: int = 4):
        """
        DROP-IN REPLACEMENT for create_full_conversation in dialogue_generator_fixed.py
        
        SAME INTERFACE as existing method, but with sophisticated evidence-based debates
        """
        
        print("🚀 Using sophisticated evidence-based dialogue generation...")
        
        # Convert analysis_results to paper_data format expected by sophisticated system
        paper_data = {
            "raw_text": self._extract_raw_text_from_analysis(analysis_results),
            "metadata": analysis_results.get("analysis_depth", {})
        }
        
        # Create sophisticated conversation
        sophisticated_script = self.integration.create_sophisticated_conversation(
            paper_data, max_topics, exchanges_per_topic
        )
        
        # Convert back to format expected by existing audio pipeline
        return self._convert_to_legacy_format(sophisticated_script)
    
    def _extract_raw_text_from_analysis(self, analysis_results: Dict) -> str:
        """Extract raw text from existing analysis results format"""
        
        # Try to reconstruct text from sections
        sections = analysis_results.get("enhanced_sections", {})
        
        raw_text = ""
        for section_name, content in sections.items():
            raw_text += f"\n\n{section_name.upper()}:\n{content}"
        
        # If no sections, try to get from summary
        if not raw_text.strip():
            summary = analysis_results.get("summary", {})
            for key, value in summary.items():
                raw_text += f"\n{key}: {value}"
        
        return raw_text.strip()
    
    def _convert_to_legacy_format(self, sophisticated_script: SophisticatedConversationScript):
        """Convert sophisticated script to legacy ConversationScript format"""
        
        # Import the legacy format (adjust import based on your existing structure)
        from dataclasses import dataclass
        
        @dataclass
        class LegacyConversationTurn:
            speaker: str
            speaker_role: str
            content: str
            topic: str
            turn_number: int
        
        @dataclass  
        class LegacyConversationScript:
            title: str
            paper_topic: str
            introduction: str
            turns: List[LegacyConversationTurn]
            conclusion: str
            total_turns: int
            duration_estimate: str
        
        # Convert turns
        legacy_turns = []
        for turn in sophisticated_script.turns:
            legacy_turn = LegacyConversationTurn(
                speaker=turn.speaker,
                speaker_role=turn.speaker_role,
                content=turn.content,
                topic=turn.topic,
                turn_number=turn.turn_number
            )
            legacy_turns.append(legacy_turn)
        
        # Create legacy script
        legacy_script = LegacyConversationScript(
            title=sophisticated_script.title,
            paper_topic=sophisticated_script.paper_topic,
            introduction=sophisticated_script.introduction,
            turns=legacy_turns,
            conclusion=sophisticated_script.conclusion,
            total_turns=sophisticated_script.total_turns,
            duration_estimate=sophisticated_script.duration_estimate
        )
        
        return legacy_script
    
    def test_connection(self) -> bool:
        """Test connection (same interface as existing system)"""
        return self.integration.test_connection()


# INTEGRATION INSTRUCTIONS FOR EXISTING SYSTEM
def integrate_with_existing_system():
    """
    INTEGRATION INSTRUCTIONS:
    
    To integrate sophisticated debates into your existing YouTube pipeline:
    
    1. REPLACE dialogue_generator_fixed.py imports:
       OLD: from dialogue_generator_fixed import FixedDialogueEngine
       NEW: from sophisticated_pipeline_integration import SophisticatedDialogueEngine as FixedDialogueEngine
    
    2. The rest of your pipeline (audio, video) works unchanged!
       - audio_generator_simple_reliable.py - no changes needed
       - phase4_video_generator.py - no changes needed
       - main_phase4.py - only change import
    
    3. ENHANCED FEATURES you get:
       - Evidence-based arguments with specific paper citations
       - Field-adaptive expertise (CS, biology, psychology, etc.)
       - Technical depth with algorithms, metrics, statistical details
       - Claim-evidence mapping for sophisticated debates
       - Academic-quality discussions that sound like real experts
    
    4. SAME INTERFACE:
       - Same method names (create_full_conversation)
       - Same parameters (max_topics, exchanges_per_topic)
       - Same return format (ConversationScript)
       - Same audio/video pipeline compatibility
    
    RESULT: Your existing YouTube pipeline now generates sophisticated academic debates
    instead of basic conversations!
    """
    pass


if __name__ == "__main__":
    print("🔗 Sophisticated Pipeline Integration Module")
    print("Drop-in replacement for basic dialogue generation")
    print("\nTo integrate with existing system:")
    print("1. Replace FixedDialogueEngine import")
    print("2. Keep all other components unchanged")
    print("3. Enjoy sophisticated evidence-based debates!")
    
    # Test the integration
    integration = SophisticatedPipelineIntegration()
    if integration.test_connection():
        print("\n✅ Integration ready!")
        print("🎬 Sophisticated YouTube debates await!")
    else:
        print("\n❌ Integration not ready - check Ollama connection")
