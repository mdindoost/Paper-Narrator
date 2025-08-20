"""Simplified Audio Generator using only Edge-TTS"""

import os
import asyncio
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
import json

try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False


@dataclass
class AudioSegment:
    speaker: str
    text: str
    audio_file: str
    duration: float
    segment_type: str


@dataclass
class VoiceProfile:
    name: str
    personality: str
    voice_id: str
    speaking_rate: str


class SimpleAudioGenerator:
    """Simplified audio generator using only Edge-TTS"""
    
    def __init__(self, output_dir: str = "data/output/audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.voice_profiles = {
            "dr_ava": VoiceProfile(
                name="Dr. Ava D.",
                personality="Enthusiastic Researcher", 
                voice_id="en-US-AriaNeural",  # Enthusiastic female
                speaking_rate="medium"
            ),
            "prof_marcus": VoiceProfile(
                name="Prof. Marcus Webb",
                personality="Critical Analyst",
                voice_id="en-US-GuyNeural",  # Professional male
                speaking_rate="medium"
            )
        }
        
        print(f"🎙️ Simple Audio Generator Initialized")
        if HAS_EDGE_TTS:
            print("✅ Using Edge-TTS (Microsoft) - High quality voices")
        else:
            print("❌ Edge-TTS not available - install with: pip install edge-tts")
    
    def check_requirements(self) -> bool:
        """Check if Edge-TTS is available"""
        return HAS_EDGE_TTS
    
    def generate_youtube_intro(self, paper_title: str) -> str:
        """Generate dramatic YouTube intro"""
        intro_text = f"""What happens when you give two brilliant researchers the same groundbreaking paper and completely opposite viewpoints? 

Welcome to Research Rundown! 

Today's explosive topic: '{paper_title}' - a research study that promises to be revolutionary. But is it revolutionary breakthrough or overblown hype? 

Dr. Ava D. and Prof. Marcus Webb are about to find out!"""
        
        return intro_text
    
    async def text_to_speech_edge(self, text: str, voice_id: str, output_file: str) -> float:
        """Generate speech using Edge TTS"""
        communicate = edge_tts.Communicate(text, voice_id)
        await communicate.save(output_file)
        
        # Estimate duration
        word_count = len(text.split())
        duration = (word_count / 150) * 60  # ~150 words per minute
        return duration
    
    def generate_audio_segment(self, text: str, speaker: str, segment_type: str = "conversation") -> AudioSegment:
        """Generate audio for one segment"""
        
        # Determine voice profile
        if "ava" in speaker.lower():
            profile = self.voice_profiles["dr_ava"]
        else:
            profile = self.voice_profiles["prof_marcus"]
        
        # Create output filename
        timestamp = int(time.time() * 1000)
        safe_speaker = speaker.replace(" ", "_").replace(".", "")
        output_file = self.output_dir / f"{safe_speaker}_{segment_type}_{timestamp}.wav"
        
        # Generate audio
        try:
            duration = asyncio.run(self.text_to_speech_edge(text, profile.voice_id, str(output_file)))
            
            print(f"   🎵 Generated: {speaker} ({duration:.1f}s)")
            
            return AudioSegment(
                speaker=speaker,
                text=text,
                audio_file=str(output_file),
                duration=duration,
                segment_type=segment_type
            )
            
        except Exception as e:
            print(f"   ❌ Error generating audio for {speaker}: {e}")
            raise
    
    def create_conversation_audio(self, conversation_script) -> List[AudioSegment]:
        """Convert conversation script to audio"""
        
        print("🎙️ Generating conversation audio with Edge-TTS...")
        
        audio_segments = []
        
        # 1. YouTube intro
        paper_title = conversation_script.paper_topic
        intro_text = self.generate_youtube_intro(paper_title)
        
        print("   📺 Generating YouTube intro...")
        intro_segment = self.generate_audio_segment(intro_text, "Narrator", "intro")
        audio_segments.append(intro_segment)
        
        # 2. Conversation turns
        print(f"   💬 Generating {len(conversation_script.turns)} conversation turns...")
        
        for turn in conversation_script.turns:
            speaker_name = turn.speaker
            if "Sarah" in speaker_name:
                speaker_name = "Dr. Ava D."
            
            segment = self.generate_audio_segment(turn.content, speaker_name, "conversation")
            audio_segments.append(segment)
        
        # 3. Conclusion
        if conversation_script.conclusion:
            print("   🏁 Generating conclusion...")
            conclusion_segment = self.generate_audio_segment(
                conversation_script.conclusion, "Narrator", "conclusion"
            )
            audio_segments.append(conclusion_segment)
        
        return audio_segments
    
    def combine_audio_simple(self, segments: List[AudioSegment], output_file: str) -> Dict:
        """Simple audio combination using ffmpeg or fallback"""
        
        print(f"🎵 Combining {len(segments)} audio segments...")
        
        # Create list of files to combine
        file_list = []
        for segment in segments:
            file_list.append(segment.audio_file)
        
        try:
            # Try ffmpeg first (best quality)
            if self._has_ffmpeg():
                self._combine_with_ffmpeg(file_list, output_file)
                method = "ffmpeg"
            else:
                # Fallback: copy first file as demo
                subprocess.run(["cp", file_list[0], output_file], check=True)
                method = "simple_copy"
                print("   ⚠️  Using simple copy - install ffmpeg for proper audio combination")
                
        except Exception as e:
            print(f"   ⚠️  Audio combination failed: {e}")
            # Ultimate fallback
            subprocess.run(["cp", file_list[0], output_file], check=True)
            method = "fallback"
        
        total_duration = sum(segment.duration for segment in segments)
        
        return {
            "output_file": output_file,
            "total_duration": total_duration,
            "num_segments": len(segments),
            "method": method,
            "segments": [{"speaker": seg.speaker, "duration": seg.duration, "type": seg.segment_type} for seg in segments]
        }
    
    def _has_ffmpeg(self) -> bool:
        """Check if ffmpeg is available"""
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _combine_with_ffmpeg(self, file_list: List[str], output_file: str):
        """Combine audio files using ffmpeg"""
        
        # Create input list for ffmpeg
        input_list_file = self.output_dir / "input_list.txt"
        
        with open(input_list_file, 'w') as f:
            for audio_file in file_list:
                f.write(f"file '{audio_file}'\n")
        
        # Combine with ffmpeg
        subprocess.run([
            "ffmpeg", "-f", "concat", "-safe", "0", "-i", str(input_list_file),
            "-c", "copy", "-y", output_file
        ], check=True, capture_output=True)
        
        # Cleanup
        input_list_file.unlink()
    
    def generate_complete_audio(self, conversation_script, base_filename: str) -> Dict:
        """Complete audio generation pipeline"""
        
        print("🎬 Starting audio generation for YouTube...")
        
        if not self.check_requirements():
            raise Exception("Edge-TTS not available. Install with: pip install edge-tts")
        
        # Generate audio segments
        segments = self.create_conversation_audio(conversation_script)
        
        # Output file
        output_file = self.output_dir / f"{base_filename}_youtube_audio.wav"
        
        # Combine audio
        result = self.combine_audio_simple(segments, str(output_file))
        
        # Save metadata
        metadata_file = self.output_dir / f"{base_filename}_audio_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        result["metadata_file"] = str(metadata_file)
        
        print(f"🎉 YouTube audio generation complete!")
        print(f"   🎵 Audio: {output_file}")
        print(f"   📊 Duration: {result['total_duration']:.1f}s ({result['total_duration']/60:.1f} min)")
        
        return result


def main():
    """Test the simple audio generator"""
    
    print("🧪 Testing Simple Audio Generator...")
    
    generator = SimpleAudioGenerator()
    
    if not generator.check_requirements():
        print("❌ Edge-TTS not available")
        print("Install with: pip install edge-tts")
        return
    
    # Test audio generation
    test_text = "Hello! I'm Dr. Ava D., and I'm excited to discuss this groundbreaking research!"
    
    try:
        segment = generator.generate_audio_segment(test_text, "Dr. Ava D.", "test")
        print(f"✅ Test audio generated: {segment.audio_file}")
        
        # Test intro
        intro = generator.generate_youtube_intro("Optimized WCC Algorithms")
        print(f"✅ YouTube intro: {intro[:50]}...")
        
        print(f"\n🎉 Simple audio system working!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
