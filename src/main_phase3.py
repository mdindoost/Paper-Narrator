"""Phase 3 Integration - Complete AI Paper Narrator with Audio Generation"""

import sys
from pathlib import Path
import json
from typing import Dict
from pdf_processor import PDFProcessor
from summarizer_final_fixed_v2 import FinalFixedPaperSummarizerV2 as FinalFixedPaperSummarizer
from robust_pipeline_integration import RobustDialogueEngine as FixedDialogueEngine
from audio_generator_simple_reliable import ReliableAudioGenerator as YouTubeAudioGenerator
from config import OUTPUT_DIR


class PaperNarratorPhase3:
    """Complete AI Paper Narrator with Audio Generation for YouTube"""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.summarizer = FinalFixedPaperSummarizer()
        self.dialogue_engine = FixedDialogueEngine()
        self.audio_generator = YouTubeAudioGenerator()
    
    def check_prerequisites(self) -> bool:
        """Check if all required services are running"""
        print("🔧 Checking Phase 3 prerequisites...")
        
        # Check Ollama connection
        if not self.summarizer.test_connection():
            print("❌ Ollama not running or model not available")
            return False
        print("✅ Ollama connection successful")
        
        # Check dialogue engine
        if not self.dialogue_engine.test_connection():
            print("❌ Dialogue engine connection failed")
            return False
        print("✅ Dialogue engine ready")
        
        # Check audio generation capabilities
        if not self.audio_generator.check_requirements(): print("❌ Edge-TTS not available"); return False
        if not self.audio_generator.check_requirements():
            print("❌ No TTS engine available")
            print("   Install with: pip install edge-tts")
            return False
        print(f"✅ Audio engine ready: Edge-TTS")
        
        return True
    
    def process_paper_complete_audio(self, pdf_path: str, 
                                   max_topics: int = 2,
                                   exchanges_per_topic: int = 2) -> Dict:
        """Complete pipeline: PDF → Analysis → Dialogue → Audio"""
        
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        print(f"\n🎬 Processing for YouTube: {pdf_path.name}")
        print("=" * 80)
        
        # Step 1: Phase 1 analysis
        print("Step 1: Paper Analysis...")
        paper_data = self.pdf_processor.process_paper(str(pdf_path))
        analysis_results = self.summarizer.deep_paper_analysis(paper_data)
        
        # Step 2: Phase 2 dialogue with updated personalities
        print(f"\nStep 2: Generating Dr. Ava D. vs Prof. Marcus Webb dialogue...")
        conversation_script = self.dialogue_engine.create_full_conversation(
            analysis_results,
            max_topics=max_topics,
            exchanges_per_topic=exchanges_per_topic
        )
        
        # Update speaker names in conversation script for audio generation
        for turn in conversation_script.turns:
            if "Sarah" in turn.speaker:
                turn.speaker = "Dr. Ava D."
        
        # Step 3: Phase 3 audio generation
        print(f"\nStep 3: Generating professional audio for YouTube...")
        
        base_filename = pdf_path.stem
        audio_result = self.audio_generator.generate_complete_audio(
            conversation_script, 
            base_filename
        )
        
        # Combine all results
        complete_result = {
            "source_file": str(pdf_path),
            "phase1_analysis": {
                "extraction": paper_data["metadata"],
                "analysis_depth": analysis_results["analysis_depth"]
            },
            "phase2_dialogue": {
                "total_turns": conversation_script.total_turns,
                "duration_estimate": conversation_script.duration_estimate,
                "speakers": ["Dr. Ava D.", "Prof. Marcus Webb"]
            },
            "phase3_audio": audio_result,
            "status": "complete_with_audio"
        }
        
        # Save complete results
        output_file = OUTPUT_DIR / f"{pdf_path.stem}_COMPLETE_phase3.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(complete_result, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Complete results saved to: {output_file}")
        return complete_result, conversation_script, audio_result
    
    def display_complete_results(self, results: Dict, conversation_script, audio_result: Dict):
        """Display complete Phase 3 results"""
        
        print("\n" + "="*80)
        print("🎬 PHASE 3 COMPLETE - YOUTUBE-READY AUDIO GENERATED")
        print("="*80)
        
        # Analysis Summary
        phase1 = results["phase1_analysis"]
        print(f"\n📋 ANALYSIS COMPLETED:")
        print(f"   • Strengths identified: {phase1['analysis_depth']['total_strengths']}")
        print(f"   • Weaknesses identified: {phase1['analysis_depth']['total_weaknesses']}")
        print(f"   • Discussion topics: {phase1['analysis_depth']['discussion_topics']}")
        
        # Dialogue Summary
        phase2 = results["phase2_dialogue"]
        print(f"\n🎭 DIALOGUE GENERATED:")
        print(f"   • Speakers: {', '.join(phase2['speakers'])}")
        print(f"   • Total turns: {phase2['total_turns']}")
        print(f"   • Script duration: {phase2['duration_estimate']}")
        
        # Audio Summary
        phase3 = audio_result
        print(f"\n🎵 AUDIO GENERATED:")
        print(f"   • Audio file: {phase3['output_file']}")
        print(f"   • Total duration: {phase3['total_duration']:.1f} seconds ({phase3['total_duration']/60:.1f} minutes)")
        print(f"   • Audio segments: {phase3['num_segments']}")
        print(f"   • Processing method: {phase3['method']}")
        
        # Segment breakdown
        print(f"\n📊 AUDIO SEGMENTS:")
        for i, segment in enumerate(phase3['segments'], 1):
            print(f"   {i}. {segment['speaker']} ({segment['type']}): {segment['duration']:.1f}s")
        
        print(f"\n🎉 YOUTUBE-READY CONTENT COMPLETE!")
        print(f"📄 Paper analyzed and debated by AI personalities")
        print(f"🎙️ Professional audio generated: {phase3['output_file']}")
        print(f"🚀 Ready for Phase 4 (Video Creation)")


def main():
    """Phase 3 main entry point"""
    
    print("🎬 AI Paper Narrator - Phase 3")
    print("Complete Analysis + Dialogue + Audio Generation")
    print("-" * 60)
    
    narrator = PaperNarratorPhase3()
    
    # Check prerequisites
    if not narrator.check_prerequisites():
        sys.exit(1)
    
    # Get parameters
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        max_topics = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        exchanges_per_topic = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    else:
        pdf_path = input("\n📁 Enter path to PDF file: ").strip().strip('"')
        print(f"\n⚙️  Audio Generation Settings:")
        max_topics = int(input(f"   📊 Max topics for discussion (default 2): ") or "2")
        exchanges_per_topic = int(input(f"   💬 Exchanges per topic (default 2): ") or "2")
    
    try:
        # Process with complete audio generation
        results, conversation_script, audio_result = narrator.process_paper_complete_audio(
            pdf_path, max_topics, exchanges_per_topic
        )
        
        # Display results
        narrator.display_complete_results(results, conversation_script, audio_result)
        
        # Final YouTube readiness check
        audio_file = Path(audio_result['output_file'])
        if audio_file.exists():
            print(f"\n🎥 YouTube Content Ready!")
            print(f"   📁 Audio file: {audio_file}")
            print(f"   ⏱️  Duration: {audio_result['total_duration']/60:.1f} minutes")
            print(f"   🎤 Speakers: Dr. Ava D. (optimistic) & Prof. Marcus Webb (skeptical)")
            print(f"\n📋 Next Steps:")
            print(f"   1. Listen to audio: play {audio_file}")
            print(f"   2. Phase 4: Add visuals for complete YouTube video")
        else:
            print(f"\n⚠️  Audio file not found: {audio_file}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
