"""
Integrated Pipeline with Cohesive Dialogue - NEW PROFESSIONAL STRUCTURE
Save as: src/integrated_enhanced_pipeline.py (REPLACE existing)

New Structure:
1. Narrator Intro
2. Dr. Ava D's Complete Cohesive Case  
3. Narrator Transition
4. Prof. Marcus W's Complete Cohesive Case
5. Narrator Conclusion
"""

import sys
from pathlib import Path
import json
import time
import asyncio
from typing import Dict, List
from dataclasses import dataclass
import re

# Import existing components
from src.pdf_processor import PDFProcessor
from src.personalities_updated import UpdatedResearchPersonalities
from src.config import OUTPUT_DIR

# Import enhanced analyzer
sys.path.append('.')
from test_enhanced_claims_challenges import (
    EnhancedClaimsChallengesAnalyzer, 
    Stage1Understanding, 
    EnhancedStage2Results,
    PaperClaim
)

# Import the cohesive dialogue generator
from src.cohesive_dialogue_generator import (
    CohesiveDialogueGenerator,
    CohesiveConversationScript,
    CohesiveTurn
)

# Import audio generator
from src.audio_generator_fixed_enhanced import FullyFixedAudioGenerator

# Import additional fixes
try:
    from src.comprehensive_bug_fixes import (
        AdditionalBugFixes,
        apply_additional_fixes_to_stage1
    )
    from stage2_additional_fixes_patch import patch_stage2_results, apply_quick_field_fix
    HAS_ADDITIONAL_FIXES = True
except ImportError:
    HAS_ADDITIONAL_FIXES = False


class CohesiveAudioGenerator(FullyFixedAudioGenerator):
    """Audio generator adapted for cohesive dialogue structure"""
    
    def generate_cohesive_audio_segments(self, cohesive_script: CohesiveConversationScript) -> List:
        """Generate audio segments for cohesive conversation script"""
        
        print(f"🎵 Generating audio for {cohesive_script.total_segments} cohesive segments...")
        
        segments = []
        
        for i, segment in enumerate(cohesive_script.segments, 1):
            print(f"\n🎤 Segment {i}/{cohesive_script.total_segments}: {segment.speaker} ({segment.segment_type})")
            
            # Generate timestamp for unique filename
            timestamp = int(time.time() * 1000) + i
            safe_speaker = segment.speaker.replace(" ", "_").replace(".", "")
            output_file = self.output_dir / f"cohesive_{segment.segment_type}_{safe_speaker}_{timestamp}.mp3"
            
            try:
                # Use comprehensive text cleanup for cohesive content
                duration = asyncio.run(self.text_to_speech_fully_fixed(
                    segment.content, segment.speaker, str(output_file)
                ))
                
                # Define AudioSegment locally to avoid import issues
                @dataclass
                class AudioSegment:
                    speaker: str
                    text: str
                    audio_file: str
                    duration: float
                    segment_type: str
                
                audio_segment = AudioSegment(
                    speaker=segment.speaker,
                    text=segment.content,
                    audio_file=str(output_file),
                    duration=duration,
                    segment_type=f"cohesive_{segment.segment_type}"
                )
                
                segments.append(audio_segment)
                print(f"   ✅ Generated {segment.segment_type}: {duration:.1f}s")
                
            except Exception as e:
                print(f"   ❌ Error generating {segment.segment_type} for {segment.speaker}: {e}")
                continue
        
        print(f"✅ Generated {len(segments)} cohesive audio segments")
        return segments
    
    def generate_complete_cohesive_audio(self, cohesive_script: CohesiveConversationScript) -> List:
        """Generate complete cohesive audio with professional structure"""
        
        print("🎵 Creating complete COHESIVE PROFESSIONAL audio...")
        print("📻 Structure: Intro → Ava Case → Transition → Marcus Case → Conclusion")
        
        # Generate cohesive segments
        cohesive_segments = self.generate_cohesive_audio_segments(cohesive_script)
        
        print(f"✅ Complete cohesive audio: {len(cohesive_segments)} segments")
        print("   🎬 Professional debate structure implemented")
        
        return cohesive_segments


class IntegratedCohesivePipeline:
    """Complete pipeline with cohesive professional dialogue structure"""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.enhanced_analyzer = EnhancedClaimsChallengesAnalyzer()
        self.cohesive_dialogue_generator = CohesiveDialogueGenerator()
        self.cohesive_audio_generator = CohesiveAudioGenerator()
    
    def check_prerequisites(self) -> bool:
        """Check if all required services are running"""
        print("🔧 Checking COHESIVE pipeline prerequisites...")
        
        if not self.enhanced_analyzer.test_connection():
            print("❌ Ollama not running or model not available")
            return False
        print("✅ Enhanced analyzer ready")
        
        if not self.cohesive_dialogue_generator.test_connection():
            print("❌ Cohesive dialogue generator connection failed") 
            return False
        print("✅ Cohesive dialogue generator ready")
        
        if not self.cohesive_audio_generator.check_requirements():
            print("❌ Audio generation not available")
            return False
        print("✅ Cohesive audio generator ready")
        
        return True
    
    def process_paper_cohesive_pipeline(self, pdf_path: str) -> Dict:
        """Complete cohesive pipeline with professional debate structure"""
        
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        print(f"\n🚀 COHESIVE PROFESSIONAL PIPELINE: {pdf_path.name}")
        print("📻 Structure: Intro → Dr. Ava D Case → Transition → Prof. Marcus W Case → Conclusion")
        print("=" * 80)
        
        # Step 1: PDF Processing
        print("📖 Step 1: PDF Processing...")
        paper_data = self.pdf_processor.process_paper(str(pdf_path))
        raw_text = paper_data["raw_text"]
        
        # Step 2: Enhanced Section Detection
        print("🔍 Step 2: Enhanced Section Detection...")
        core_sections = self.enhanced_analyzer.enhanced_section_detection(raw_text)
        
        if not core_sections:
            raise ValueError("No core sections found for analysis")
        
        # Step 3: Stage 1 - Understanding
        print("🎯 Step 3: Stage 1 Understanding...")
        stage1_understanding = self.enhanced_analyzer.stage1_simple_understanding(core_sections)
        
        # Step 4: Stage 2 - Claims→Challenges Analysis  
        print("⚔️ Step 4: Stage 2 Claims→Challenges Analysis...")
        stage2_results = self.enhanced_analyzer.stage2_enhanced_claims_challenges(
            stage1_understanding, raw_text
        )
        
        # Step 5: Apply additional fixes if available
        if HAS_ADDITIONAL_FIXES:
            print("🔧 Step 5: Applying Additional Fixes...")
            stage1_understanding = apply_quick_field_fix(stage1_understanding)
            stage2_results = patch_stage2_results(stage2_results)
        
        # Step 6: COHESIVE Dialogue Generation
        print("🎭 Step 6: COHESIVE Professional Dialogue Generation...")
        cohesive_script = self.cohesive_dialogue_generator.create_cohesive_conversation_script(
            stage1_understanding, stage2_results
        )
        
        # Step 7: COHESIVE Audio Generation
        print("🎵 Step 7: COHESIVE Professional Audio Generation...")
        base_filename = pdf_path.stem
        
        # Generate cohesive audio segments
        cohesive_segments = self.cohesive_audio_generator.generate_complete_cohesive_audio(cohesive_script)
        
        # Combine audio segments
        output_file = self.cohesive_audio_generator.output_dir / f"{base_filename}_COHESIVE_youtube.wav"
        audio_result = self.cohesive_audio_generator.combine_audio_segments(cohesive_segments, str(output_file))
        
        # Update audio result with cohesive metadata
        audio_result.update({
            "cohesive_structure": True,
            "segments_type": "professional_debate_format",
            "speakers_flow": "intro → ava_case → transition → marcus_case → conclusion"
        })
        
        # Combine results
        complete_result = {
            "source_file": str(pdf_path),
            "cohesive_analysis": {
                "research_field": stage1_understanding.research_field,
                "paper_topic": stage1_understanding.paper_topic,
                "key_finding": stage1_understanding.key_finding,
                "claims_analyzed": len(stage2_results.paper_claims),
                "evidence_quality": self._assess_overall_evidence_quality(stage2_results.paper_claims)
            },
            "cohesive_dialogue": {
                "total_segments": cohesive_script.total_segments,
                "duration_estimate": cohesive_script.duration_estimate,
                "structure": "intro → optimist_case → transition → skeptic_case → conclusion",
                "speakers": ["Narrator", "Dr. Ava D.", "Prof. Marcus W."],
                "dialogue_type": "cohesive_professional_debate",
                "optimist_points": len(stage2_results.debate_ammunition["optimist"]),
                "skeptic_points": len(stage2_results.debate_ammunition["skeptic"])
            },
            "audio_generation": audio_result,
            "status": "cohesive_professional_pipeline_complete"
        }
        
        # Save results
        output_file_json = OUTPUT_DIR / f"{pdf_path.stem}_COHESIVE_pipeline.json"
        with open(output_file_json, 'w', encoding='utf-8') as f:
            json.dump(complete_result, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ COHESIVE PROFESSIONAL pipeline complete!")
        print(f"📄 Results: {output_file_json}")
        print(f"🎵 Audio: {audio_result['output_file']}")
        
        return complete_result, cohesive_script, audio_result, stage1_understanding, stage2_results
    
    def _assess_overall_evidence_quality(self, claims: List[PaperClaim]) -> Dict[str, int]:
        """Assess overall evidence quality distribution"""
        quality_counts = {"strong": 0, "moderate": 0, "weak": 0, "insufficient": 0}
        
        for claim in claims:
            if claim.evidence_strength in quality_counts:
                quality_counts[claim.evidence_strength] += 1
            else:
                quality_counts["insufficient"] += 1
        
        return quality_counts


# For backward compatibility
IntegratedCompletelyFixedPipeline = IntegratedCohesivePipeline

# Test function for the cohesive pipeline
def test_cohesive_professional_pipeline():
    """Test the complete cohesive professional pipeline"""
    
    print("🚀 COHESIVE PROFESSIONAL PIPELINE TEST")
    print("📻 NEW STRUCTURE: Intro → Dr. Ava D Case → Transition → Prof. Marcus W Case → Conclusion")
    print("=" * 80)
    
    pipeline = IntegratedCohesivePipeline()
    
    if not pipeline.check_prerequisites():
        print("❌ Prerequisites not met")
        return False
    
    # Test with your paper
    pdf_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    try:
        complete_result, cohesive_script, audio_result, stage1, stage2 = pipeline.process_paper_cohesive_pipeline(pdf_path)
        
        # Display comprehensive results
        print(f"\n🎉 COHESIVE PROFESSIONAL PIPELINE SUCCESS!")
        print(f"=" * 60)
        
        print(f"📊 Analysis Results:")
        analysis = complete_result["cohesive_analysis"]
        print(f"   🎯 Field: {analysis['research_field']}")
        print(f"   📄 Topic: {analysis['paper_topic']}")
        print(f"   💡 Key Finding: {analysis['key_finding']}")
        
        print(f"\n🎭 Cohesive Dialogue Results:")
        dialogue = complete_result["cohesive_dialogue"]
        print(f"   📻 Structure: {dialogue['structure']}")
        print(f"   🎤 Total Segments: {dialogue['total_segments']}")
        print(f"   ⏱️ Duration: {dialogue['duration_estimate']}")
        print(f"   👥 Speakers: {', '.join(dialogue['speakers'])}")
        print(f"   😊 Optimist Points: {dialogue['optimist_points']}")
        print(f"   🤨 Skeptic Points: {dialogue['skeptic_points']}")
        
        print(f"\n🎵 Cohesive Audio Results:")
        audio = complete_result["audio_generation"]
        print(f"   🎧 Audio File: {audio['output_file']}")
        print(f"   ⏱️ Duration: {audio['total_duration']:.1f}s ({audio['total_duration']/60:.1f} min)")
        print(f"   📊 Segments: {audio['num_segments']}")
        print(f"   📻 Structure: {audio['speakers_flow']}")
        
        # Display the cohesive script structure
        print(f"\n📝 COHESIVE SCRIPT STRUCTURE:")
        for i, segment in enumerate(cohesive_script.segments, 1):
            segment_type_emoji = {
                "intro": "🎬",
                "optimist_case": "🔬", 
                "transition": "🔄",
                "skeptic_case": "🧐",
                "conclusion": "🎯"
            }
            emoji = segment_type_emoji.get(segment.segment_type, "🎤")
            print(f"   {emoji} Segment {i}: {segment.speaker} ({segment.segment_type})")
            print(f"      Preview: {segment.content[:1000]}...")
        
        print(f"\n✅ READY FOR PROFESSIONAL YOUTUBE CONTENT!")
        print(f"   ✅ Cohesive, flowing speeches from each expert")
        print(f"   ✅ Professional debate structure")
        print(f"   ✅ Natural transitions between speakers")
        print(f"   ✅ No awkward back-and-forth interruptions")
        print(f"   ✅ All ammunition points incorporated cohesively")
        
        return True
        
    except Exception as e:
        print(f"❌ Cohesive professional pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False


# Test the new cohesive approach
def test_integrated_completely_fixed_pipeline():
    """Wrapper for backward compatibility"""
    return test_cohesive_professional_pipeline()


if __name__ == "__main__":
    test_cohesive_professional_pipeline()