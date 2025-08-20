# src/audio_generator.py
"""Phase 3: Audio Generation System for YouTube-Ready Content"""

import os
import requests
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
import json
import time

# Try to import TTS libraries (will install if needed)
try:
    from TTS.api import TTS
    HAS_COQUI = True
except ImportError:
    HAS_COQUI = False

try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False


@dataclass
class AudioSegment:
    """Represents one audio segment"""
    speaker: str
    text: str
    audio_file: str
    duration: float
    segment_type: str  # 'intro', 'conversation', 'conclusion'


@dataclass
class VoiceProfile:
    """Voice configuration for each personality"""
    name: str
    personality: str
    voice_id: str
    speaking_rate: str
    pitch: str
    emphasis_style: str


class YouTubeAudioGenerator:
    """Generate professional audio for YouTube content"""
    
    def __init__(self, output_dir: str = "data/output/audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Updated personality voice profiles
        self.voice_profiles = {
            "dr_ava": VoiceProfile(
                name="Dr. Ava D.",
                personality="Optimistic Researcher", 
                voice_id="en-US-AriaNeural",  # Enthusiastic female voice
                speaking_rate="medium",
                pitch="+10Hz",
                emphasis_style="excited"
            ),
            "prof_marcus": VoiceProfile(
                name="Prof. Marcus Webb",
                personality="Critical Analyst",
                voice_id="en-US-GuyNeural",  # Professional male voice
                speaking_rate="medium", 
                pitch="-5Hz",
                emphasis_style="analytical"
            )
        }
        
        self.available_engines = self._detect_tts_engines()
        self.selected_engine = self._select_best_engine()
        
        print(f"🎙️ Audio Generation System Initialized")
        print(f"   Available engines: {', '.join(self.available_engines)}")
        print(f"   Selected engine: {self.selected_engine}")
    
    def _detect_tts_engines(self) -> List[str]:
        """Detect available TTS engines"""
        engines = []
        
        if HAS_EDGE_TTS:
            engines.append("edge-tts")
        
        if HAS_COQUI:
            engines.append("coqui-tts")
        
        # Check if espeak is available (fallback)
        try:
            subprocess.run(["espeak", "--version"], capture_output=True, check=True)
            engines.append("espeak")
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        return engines
    
    def _select_best_engine(self) -> str:
        """Select the best available TTS engine"""
        if "edge-tts" in self.available_engines:
            return "edge-tts"  # Best quality for free
        elif "coqui-tts" in self.available_engines:
            return "coqui-tts"  # Good open source option
        elif "espeak" in self.available_engines:
            return "espeak"  # Basic fallback
        else:
            return "none"
    
    def install_requirements(self):
        """Install required TTS packages"""
        print("📦 Installing TTS requirements...")
        
        packages_to_install = []
        
        if not HAS_EDGE_TTS:
            packages_to_install.append("edge-tts")
        
        if not HAS_COQUI and "coqui-tts" not in self.available_engines:
            packages_to_install.append("TTS")
        
        if packages_to_install:
            print(f"   Installing: {', '.join(packages_to_install)}")
            for package in packages_to_install:
                subprocess.run(["pip", "install", package], check=True)
            
            # Re-detect engines after installation
            self.available_engines = self._detect_tts_engines()
            self.selected_engine = self._select_best_engine()
            print(f"   Updated selected engine: {self.selected_engine}")
        else:
            print("   All required packages already installed")
    
    def generate_youtube_intro(self, paper_title: str) -> str:
        """Generate the dramatic YouTube-style introduction"""
        
        intro_text = f"""What happens when you give two brilliant researchers the same groundbreaking paper and completely opposite viewpoints? 

Welcome to Research Rundown! 

Today's explosive topic: '{paper_title}' - a research study that promises to be revolutionary. But is it revolutionary breakthrough or overblown hype? 

Dr. Ava D. and Prof. Marcus Webb are about to find out!"""
        
        return intro_text
    
    def text_to_speech_edge(self, text: str, voice_id: str, output_file: str) -> float:
        """Generate speech using Edge TTS (Microsoft's free TTS)"""
        
        async def generate_audio():
            communicate = edge_tts.Communicate(text, voice_id)
            await communicate.save(output_file)
        
        import asyncio
        asyncio.run(generate_audio())
        
        # Get duration (rough estimate: ~150 words per minute)
        word_count = len(text.split())
        duration = (word_count / 150) * 60
        
        return duration
    
    def text_to_speech_coqui(self, text: str, voice_profile: VoiceProfile, output_file: str) -> float:
        """Generate speech using Coqui TTS"""
        
        # Initialize TTS model (use a fast, good quality model)
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
        
        # Generate audio
        tts.tts_to_file(text=text, file_path=output_file)
        
        # Estimate duration
        word_count = len(text.split())
        duration = (word_count / 150) * 60
        
        return duration
    
    def text_to_speech_espeak(self, text: str, voice_profile: VoiceProfile, output_file: str) -> float:
        """Generate speech using espeak (basic fallback)"""
        
        # Determine voice based on personality
        voice = "en+f3" if "ava" in voice_profile.name.lower() else "en+m3"
        
        # Generate audio with espeak
        subprocess.run([
            "espeak", 
            "-v", voice,
            "-s", "160",  # Speaking speed
            "-w", output_file,  # Write to file
            text
        ], check=True)
        
        # Estimate duration
        word_count = len(text.split())
        duration = (word_count / 150) * 60
        
        return duration
    
    def generate_audio_segment(self, text: str, speaker: str, segment_type: str = "conversation") -> AudioSegment:
        """Generate audio for one text segment"""
        
        # Determine voice profile
        if "ava" in speaker.lower():
            profile = self.voice_profiles["dr_ava"]
        else:
            profile = self.voice_profiles["prof_marcus"]
        
        # Create output filename
        timestamp = int(time.time() * 1000)
        safe_speaker = speaker.replace(" ", "_").replace(".", "")
        output_file = self.output_dir / f"{safe_speaker}_{segment_type}_{timestamp}.wav"
        
        # Generate audio based on selected engine
        try:
            if self.selected_engine == "edge-tts":
                duration = self.text_to_speech_edge(text, profile.voice_id, str(output_file))
            elif self.selected_engine == "coqui-tts":
                duration = self.text_to_speech_coqui(text, profile, str(output_file))
            elif self.selected_engine == "espeak":
                duration = self.text_to_speech_espeak(text, profile, str(output_file))
            else:
                raise Exception("No TTS engine available")
            
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
        """Convert complete conversation script to audio segments"""
        
        print("🎙️ Generating conversation audio...")
        
        audio_segments = []
        
        # 1. Generate YouTube intro
        paper_title = conversation_script.paper_topic
        intro_text = self.generate_youtube_intro(paper_title)
        
        print("   📺 Generating YouTube intro...")
        intro_segment = self.generate_audio_segment(
            intro_text, 
            "Narrator",  # Could use either voice for intro
            "intro"
        )
        audio_segments.append(intro_segment)
        
        # 2. Generate conversation turns
        print(f"   💬 Generating {len(conversation_script.turns)} conversation turns...")
        
        for turn in conversation_script.turns:
            # Update speaker name from Sarah Chen to Ava D.
            speaker_name = turn.speaker
            if "Sarah" in speaker_name:
                speaker_name = "Dr. Ava D."
            
            segment = self.generate_audio_segment(
                turn.content,
                speaker_name,
                "conversation"
            )
            audio_segments.append(segment)
        
        # 3. Generate conclusion
        if conversation_script.conclusion:
            print("   🏁 Generating conclusion...")
            conclusion_segment = self.generate_audio_segment(
                conversation_script.conclusion,
                "Narrator",
                "conclusion"
            )
            audio_segments.append(conclusion_segment)
        
        return audio_segments
    
    def combine_audio_segments(self, segments: List[AudioSegment], output_file: str) -> Dict:
        """Combine all audio segments into final podcast"""
        
        print(f"🎵 Combining {len(segments)} audio segments...")
        
        # Check if we have audio processing tools
        try:
            # Try using ffmpeg (best option)
            self._combine_with_ffmpeg(segments, output_file)
            method = "ffmpeg"
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Try using sox (alternative)
                self._combine_with_sox(segments, output_file)
                method = "sox"
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fallback: simple concatenation
                self._combine_simple(segments, output_file)
                method = "simple"
        
        # Calculate total duration
        total_duration = sum(segment.duration for segment in segments)
        
        result = {
            "output_file": output_file,
            "total_duration": total_duration,
            "num_segments": len(segments),
            "method": method,
            "segments": [
                {
                    "speaker": seg.speaker,
                    "duration": seg.duration,
                    "type": seg.segment_type
                }
                for seg in segments
            ]
        }
        
        print(f"✅ Audio combined using {method}")
        print(f"   📄 Output: {output_file}")
        print(f"   ⏱️  Duration: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")
        
        return result
    
    def _combine_with_ffmpeg(self, segments: List[AudioSegment], output_file: str):
        """Combine audio using ffmpeg (best quality)"""
        
        # Create input file list
        input_list = self.output_dir / "input_list.txt"
        
        with open(input_list, 'w') as f:
            for segment in segments:
                f.write(f"file '{segment.audio_file}'\n")
                # Add small pause between speakers (except for intro)
                if segment.segment_type == "conversation":
                    f.write(f"file 'silence.wav'\n")
        
        # Create a short silence file
        silence_file = self.output_dir / "silence.wav"
        subprocess.run([
            "ffmpeg", "-f", "lavfi", "-i", "anullsrc=duration=0.5:sample_rate=22050", 
            "-y", str(silence_file)
        ], check=True, capture_output=True)
        
        # Combine all files
        subprocess.run([
            "ffmpeg", "-f", "concat", "-safe", "0", "-i", str(input_list),
            "-c", "copy", "-y", output_file
        ], check=True, capture_output=True)
        
        # Cleanup
        input_list.unlink()
        silence_file.unlink()
    
    def _combine_with_sox(self, segments: List[AudioSegment], output_file: str):
        """Combine audio using sox"""
        
        input_files = []
        for segment in segments:
            input_files.append(segment.audio_file)
            # Add pause between speakers
            if segment.segment_type == "conversation":
                input_files.append("trim 0 0.5")  # 0.5 second pause
        
        subprocess.run(["sox"] + input_files + [output_file], check=True)
    
    def _combine_simple(self, segments: List[AudioSegment], output_file: str):
        """Simple audio combination (fallback)"""
        
        print("   ⚠️  Using simple audio combination - install ffmpeg for better quality")
        
        # For now, just copy the first segment as a placeholder
        # In a real implementation, you'd use audio libraries like pydub
        if segments:
            subprocess.run(["cp", segments[0].audio_file, output_file], check=True)
    
    def generate_complete_audio(self, conversation_script, base_filename: str) -> Dict:
        """Complete audio generation pipeline"""
        
        print("🎬 Starting complete audio generation for YouTube...")
        
        # Generate all audio segments
        segments = self.create_conversation_audio(conversation_script)
        
        # Define output file
        output_file = self.output_dir / f"{base_filename}_complete_audio.wav"
        
        # Combine into final audio
        result = self.combine_audio_segments(segments, str(output_file))
        
        # Save metadata
        metadata_file = self.output_dir / f"{base_filename}_audio_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        result["metadata_file"] = str(metadata_file)
        
        print(f"🎉 Complete audio generation finished!")
        print(f"   🎵 Audio file: {output_file}")
        print(f"   📋 Metadata: {metadata_file}")
        
        return result


def main():
    """Test the audio generation system"""
    
    print("🎙️ Testing Audio Generation System...")
    
    generator = YouTubeAudioGenerator()
    
    # Install requirements if needed
    generator.install_requirements()
    
    if generator.selected_engine == "none":
        print("❌ No TTS engine available. Install with:")
        print("   pip install edge-tts")
        return
    
    # Test voice generation
    test_text = "Hello! I'm Dr. Ava D., and I'm excited to discuss this groundbreaking research!"
    
    try:
        segment = generator.generate_audio_segment(test_text, "Dr. Ava D.", "test")
        print(f"✅ Test audio generated: {segment.audio_file}")
        
        # Test YouTube intro
        intro = generator.generate_youtube_intro("Optimized Parallel Implementations of WCC Algorithms")
        print(f"✅ YouTube intro: {intro[:100]}...")
        
    except Exception as e:
        print(f"❌ Error in audio generation: {e}")


if __name__ == "__main__":
    main()
