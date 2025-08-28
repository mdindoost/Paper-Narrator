#!/usr/bin/env python3
"""
Streamlined Paper to Audio Generator
Save as: generate_paper_audio.py (in root directory)

Complete pipeline: PDF → Analysis → Cohesive Dialogue → Audio
No interactive pauses - ready for video generation
"""

import sys
import os
import time
import asyncio
from pathlib import Path
import json
from dataclasses import dataclass

# Add src directory to path
sys.path.append('src')
sys.path.append('.')

try:
    from src.pdf_processor import PDFProcessor
    from test_enhanced_claims_challenges import EnhancedClaimsChallengesAnalyzer
    from src.cohesive_dialogue_generator import CohesiveDialogueGenerator
    from src.audio_generator_fixed_enhanced import FullyFixedAudioGenerator
    from src.config import OUTPUT_DIR
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all files are in their correct locations")
    sys.exit(1)


@dataclass
class AudioSegmentInfo:
    """Audio segment information for cohesive dialogue"""
    speaker: str
    text: str
    audio_file: str
    duration: float
    segment_type: str


class StreamlinedPaperToAudio:
    """Streamlined pipeline from PDF to audio without pauses"""
    
    def __init__(self):
        print("🎙️ Initializing Streamlined Paper to Audio Generator...")
        
        self.pdf_processor = PDFProcessor()
        self.enhanced_analyzer = EnhancedClaimsChallengesAnalyzer()
        self.cohesive_dialogue_generator = CohesiveDialogueGenerator()
        self.audio_generator = FullyFixedAudioGenerator()
        
        print("✅ All components initialized")
    
    def check_prerequisites(self) -> bool:
        """Check if all services are available"""
        print("🔧 Checking prerequisites...")
        
        # Check Ollama connection
        if not self.enhanced_analyzer.test_connection():
            print("❌ Ollama not running - start with: ollama serve")
            return False
        print("✅ Ollama connection successful")
        
        # Check cohesive dialogue generator
        if not self.cohesive_dialogue_generator.test_connection():
            print("❌ Cohesive dialogue generator connection failed")
            return False
        print("✅ Cohesive dialogue generator ready")
        
        # Check audio requirements
        if not self.audio_generator.check_requirements():
            print("❌ Edge-TTS not available - install with: pip install edge-tts")
            return False
        print("✅ Audio generation ready")
        
        return True
    
    def process_pdf_to_audio(self, pdf_path: str) -> dict:
        """Complete streamlined pipeline from PDF to audio"""
        
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            raise FileNotFoundError(f"❌ PDF not found: {pdf_path}")
        
        print(f"\n🚀 STREAMLINED PIPELINE: {pdf_file.name}")
        print("📻 Structure: PDF → Analysis → Cohesive Dialogue → Audio")
        print("=" * 80)
        
        start_time = time.time()
        
        # STEP 1: PDF Processing
        print("📖 Step 1: PDF Processing...")
        paper_data = self.pdf_processor.process_paper(str(pdf_path))
        raw_text = paper_data["raw_text"]
        print(f"   ✅ Extracted {len(raw_text):,} characters")
        
        # STEP 2: Enhanced Section Detection
        print("🔍 Step 2: Enhanced Section Detection...")
        core_sections = self.enhanced_analyzer.enhanced_section_detection(raw_text)
        print(f"   ✅ Found sections: {list(core_sections.keys())}")
        
        if not core_sections:
            raise ValueError("❌ No core sections found for analysis")
        
        # STEP 3: Stage 1 - Core Understanding (NO PAUSE)
        print("🎯 Step 3: Stage 1 Understanding...")
        # Comment out the pause in enhanced_analyzer.py
        stage1_understanding = self.enhanced_analyzer.stage1_simple_understanding(core_sections)
        print(f"   ✅ Field: {stage1_understanding.research_field}")
        print(f"   ✅ Topic: {stage1_understanding.paper_topic}")
        
        # STEP 4: Stage 2 - Claims→Challenges Analysis (NO PAUSE)  
        print("⚔️ Step 4: Stage 2 Claims→Challenges Analysis...")
        # Comment out the pause in enhanced_analyzer.py
        stage2_results = self.enhanced_analyzer.stage2_enhanced_claims_challenges(
            stage1_understanding, raw_text
        )
        
        optimist_points = len(stage2_results.debate_ammunition["optimist"])
        skeptic_points = len(stage2_results.debate_ammunition["skeptic"])
        print(f"   ✅ Generated {optimist_points} optimist points")
        print(f"   ✅ Generated {skeptic_points} skeptic points")
        
        # STEP 5: Apply Quick Fixes (Remove ** symbols)
        print("🔧 Step 5: Applying Quick Fixes...")
        try:
            from stage2_additional_fixes_patch import patch_stage2_results, apply_quick_field_fix
            stage1_understanding = apply_quick_field_fix(stage1_understanding)
            stage2_results = patch_stage2_results(stage2_results)
            print("   ✅ Additional fixes applied")
        except ImportError:
            print("   ⚠️ Additional fixes not available")
        
        # STEP 6: Cohesive Dialogue Generation
        print("🎭 Step 6: Cohesive Professional Dialogue Generation...")
        cohesive_script = self.cohesive_dialogue_generator.create_cohesive_conversation_script(
            stage1_understanding, stage2_results
        )
        print(f"   ✅ Generated {cohesive_script.total_segments} cohesive segments:")
        for segment in cohesive_script.segments:
            print(f"      🎤 {segment.speaker} ({segment.segment_type})")
        
        # STEP 7: Audio Generation with Cohesive Structure
        print("🎵 Step 7: Professional Audio Generation...")
        base_filename = pdf_file.stem
        
        # Generate audio for cohesive segments
        audio_segments = []
        
        for i, segment in enumerate(cohesive_script.segments, 1):
            print(f"   🎤 Generating {segment.segment_type}: {segment.speaker}")
            
            # Create unique filename
            timestamp = int(time.time() * 1000) + i
            safe_speaker = segment.speaker.replace(" ", "_").replace(".", "")
            output_file = self.audio_generator.output_dir / f"cohesive_{segment.segment_type}_{safe_speaker}_{timestamp}.mp3"
            
            try:
                # Generate audio with your fixed text cleanup
                import asyncio
                duration = asyncio.run(self.audio_generator.text_to_speech_fully_fixed(
                    segment.content, segment.speaker, str(output_file)
                ))
                
                # Create audio segment info
                audio_segments.append(AudioSegmentInfo(
                    speaker=segment.speaker,
                    text=segment.content,
                    audio_file=str(output_file),
                    duration=duration,
                    segment_type=segment.segment_type
                ))
                
                print(f"      ✅ Generated: {duration:.1f}s")
                
            except Exception as e:
                print(f"      ❌ Error generating {segment.segment_type}: {e}")
                continue
        
        # STEP 8: Combine Audio Segments
        print("🎼 Step 8: Combining Audio Segments...")
        final_audio_file = self.audio_generator.output_dir / f"{base_filename}_COHESIVE_youtube.wav"
        
        audio_result = self.audio_generator.combine_audio_segments(audio_segments, str(final_audio_file))
        
        # Calculate total time
        total_time = time.time() - start_time
        
        # Create comprehensive result
        complete_result = {
            "source_file": str(pdf_path),
            "processing_time": f"{total_time:.1f} seconds",
            "paper_analysis": {
                "research_field": stage1_understanding.research_field,
                "paper_topic": stage1_understanding.paper_topic,
                "key_finding": stage1_understanding.key_finding,
                "claims_analyzed": len(stage2_results.paper_claims),
                "optimist_points": optimist_points,
                "skeptic_points": skeptic_points
            },
            "cohesive_dialogue": {
                "structure": "intro → ava_case → transition → marcus_case → conclusion",
                "total_segments": cohesive_script.total_segments,
                "duration_estimate": cohesive_script.duration_estimate,
                "speakers": ["Narrator", "Dr. Ava D.", "Prof. Marcus W."]
            },
            "audio_output": {
                "final_audio_file": str(final_audio_file),
                "total_duration": audio_result['total_duration'],
                "segments_generated": len(audio_segments),
                "voice_profiles": [
                    "Narrator: en-US-AriaNeural",
                    "Dr. Ava D.: en-US-JennyNeural", 
                    "Prof. Marcus W.: en-US-ChristopherNeural"
                ]
            },
            "ready_for_video": True,
            "status": "streamlined_success"
        }
        
        # Save results
        output_json = OUTPUT_DIR / f"{pdf_file.stem}_STREAMLINED_results.json"
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(complete_result, f, indent=2, ensure_ascii=False)
        
        # Display final results
        print(f"\n🎉 STREAMLINED PIPELINE COMPLETE!")
        print(f"=" * 60)
        print(f"⏱️ Total Processing Time: {total_time:.1f} seconds")
        print(f"🎵 Final Audio: {final_audio_file}")
        print(f"📊 Duration: {audio_result['total_duration']:.1f}s ({audio_result['total_duration']/60:.1f} minutes)")
        print(f"🎤 Segments: {len(audio_segments)} professional segments")
        print(f"📄 Results: {output_json}")
        
        print(f"\n📻 COHESIVE STRUCTURE GENERATED:")
        for i, segment in enumerate(cohesive_script.segments, 1):
            duration = next((s.duration for s in audio_segments if s.segment_type == segment.segment_type), 0)
            print(f"   {i}. {segment.speaker} ({segment.segment_type}): {duration:.1f}s")
        
        print(f"\n✅ READY FOR VIDEO GENERATION!")
        
        return complete_result
    
    def display_cohesive_script(self, cohesive_script):
        """Display the cohesive script for review"""
        
        print(f"\n📝 COHESIVE SCRIPT PREVIEW:")
        print("=" * 60)
        
        for i, segment in enumerate(cohesive_script.segments, 1):
            segment_emojis = {
                "intro": "🎬",
                "optimist_case": "🔬",
                "transition": "🔄", 
                "skeptic_case": "🧐",
                "conclusion": "🎯"
            }
            
            emoji = segment_emojis.get(segment.segment_type, "🎤")
            print(f"\n{emoji} SEGMENT {i}: {segment.speaker.upper()} ({segment.segment_type})")
            print("-" * 40)
            print(f"{segment.content[:200]}...")
            if len(segment.content) > 200:
                print("... [content continues]")


def test_streamlined_pipeline(pdf_path: str = None):
    """Test the streamlined pipeline"""
    
    if pdf_path is None:
        pdf_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    print("🚀 TESTING STREAMLINED PAPER TO AUDIO PIPELINE")
    print("📻 No pauses - Direct generation for video preparation")
    print("=" * 80)
    
    try:
        pipeline = StreamlinedPaperToAudio()
        
        if not pipeline.check_prerequisites():
            print("❌ Prerequisites not met")
            return False
        
        # Process PDF to audio
        result = pipeline.process_pdf_to_audio(pdf_path)
        
        if result["status"] == "streamlined_success":
            print(f"\n🎉 STREAMLINED SUCCESS!")
            print(f"🎵 Audio ready: {result['audio_output']['final_audio_file']}")
            print(f"⏱️ Duration: {result['audio_output']['total_duration']/60:.1f} minutes")
            print(f"📻 Professional cohesive structure implemented")
            print(f"\n🎬 READY FOR VIDEO GENERATION!")
            return True
        else:
            print(f"❌ Pipeline failed")
            return False
            
    except Exception as e:
        print(f"❌ Streamlined pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def quick_audio_test():
    """Quick test to verify audio generation works"""
    
    print("🧪 QUICK AUDIO TEST")
    print("=" * 40)
    
    try:
        audio_gen = FullyFixedAudioGenerator()
        
        if not audio_gen.check_requirements():
            print("❌ Audio requirements not met")
            return False
        
        # Test all three voices
        test_texts = [
            ("Narrator", "Welcome to Research Rundown!"),
            ("Dr. Ava D.", "This is absolutely fascinating research with breakthrough potential!"),
            ("Prof. Marcus W.", "Hold on, I have serious concerns about this methodology.")
        ]
        
        print("Testing all three voices...")
        
        import asyncio
        
        for speaker, text in test_texts:
            output_file = f"test_{speaker.replace(' ', '_').replace('.', '')}.mp3"
            
            try:
                duration = asyncio.run(audio_gen.text_to_speech_fully_fixed(
                    text, speaker, output_file
                ))
                print(f"   ✅ {speaker}: {duration:.1f}s")
                
                # Clean up test file
                if os.path.exists(output_file):
                    os.remove(output_file)
                    
            except Exception as e:
                print(f"   ❌ {speaker}: {e}")
                return False
        
        print("✅ All voices working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Quick audio test failed: {e}")
        return False


def main():
    """Main function"""
    
    print("🎙️ STREAMLINED PAPER TO AUDIO GENERATOR")
    print("Direct pipeline: PDF → Analysis → Cohesive Dialogue → Audio")
    print("-" * 60)
    
    # Quick audio test first
    if not quick_audio_test():
        print("❌ Audio test failed - fix audio issues first")
        return
    
    # Get PDF path
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    print(f"\n📄 Processing: {pdf_path}")
    
    # Run streamlined pipeline
    success = test_streamlined_pipeline(pdf_path)
    
    if success:
        print(f"\n🎉 STREAMLINED PIPELINE SUCCESS!")
        print(f"✅ Professional cohesive audio generated")
        print(f"✅ No interactive pauses")
        print(f"✅ Ready for video generation")
        print(f"\n🎬 NEXT STEP: Video Generation")
        print(f"Your audio file is ready for video processing!")
    else:
        print(f"\n❌ Pipeline failed - check error messages above")


if __name__ == "__main__":
    main()
