"""Simplified Reliable Audio Generator - SOX Primary Method"""

import os
import asyncio
import subprocess
import time
from pathlib import Path
from typing import Dict, List
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
    voice_id: str


class ReliableAudioGenerator:
    """Simplified reliable audio generator using SOX (no FFmpeg complexity)"""
    
    def __init__(self, output_dir: str = "data/output/audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.voice_profiles = {
            "dr_ava": VoiceProfile("Dr. Ava D.", "en-US-AriaNeural"),
            "prof_marcus": VoiceProfile("Prof. Marcus Webb", "en-US-GuyNeural")
        }
        
        print(f"🎙️ Reliable Audio Generator Initialized")
        print("✅ Using SOX for reliable audio combination")
    
    def check_requirements(self) -> bool:
        return HAS_EDGE_TTS
    
    def clean_dialogue_text(self, text: str) -> str:
        """Fix name references"""
        cleaned = text.replace("Dr. Chen", "Dr. Ava D.")
        cleaned = cleaned.replace("Dr. Sarah Chen", "Dr. Ava D.")
        cleaned = cleaned.replace("Sarah", "Ava")
        return cleaned
    
    def generate_youtube_intro(self, paper_title: str) -> str:
        """Generate YouTube intro"""
        return f"""What happens when you give two brilliant researchers the same groundbreaking paper and completely opposite viewpoints? 

Welcome to Research Rundown! 

Today's explosive topic: '{paper_title}' - a research study that promises to be revolutionary. But is it revolutionary breakthrough or overblown hype? 

Dr. Ava D. and Prof. Marcus Webb are about to find out!"""
    
    async def text_to_speech_edge(self, text: str, voice_id: str, output_file: str) -> float:
        """Generate speech with accurate timing"""
        cleaned_text = self.clean_dialogue_text(text)
        communicate = edge_tts.Communicate(cleaned_text, voice_id)
        await communicate.save(output_file)
        
        # Get exact duration
        try:
            result = subprocess.run([
                "ffprobe", "-v", "quiet", "-show_entries", "format=duration", 
                "-of", "csv=p=0", output_file
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return float(result.stdout.strip())
        except:
            pass
        
        # Fallback estimation
        word_count = len(cleaned_text.split())
        return (word_count / 150) * 60
    
    def generate_audio_segment(self, text: str, speaker: str, segment_type: str) -> AudioSegment:
        """Generate one audio segment"""
        if "ava" in speaker.lower():
            profile = self.voice_profiles["dr_ava"]
        else:
            profile = self.voice_profiles["prof_marcus"]
        
        timestamp = int(time.time() * 1000)
        safe_speaker = speaker.replace(" ", "_").replace(".", "")
        output_file = self.output_dir / f"{safe_speaker}_{segment_type}_{timestamp}.mp3"
        
        try:
            duration = asyncio.run(self.text_to_speech_edge(text, profile.voice_id, str(output_file)))
            print(f"   🎵 Generated: {speaker} ({duration:.1f}s)")
            
            return AudioSegment(speaker, text, str(output_file), duration, segment_type)
        except Exception as e:
            print(f"   ❌ Error generating {speaker}: {e}")
            raise
    
    def create_conversation_audio(self, conversation_script) -> List[AudioSegment]:
        """Generate all audio segments"""
        print("🎙️ Generating reliable conversation audio...")
        
        segments = []
        
        # Intro
        intro_text = self.generate_youtube_intro(conversation_script.paper_topic)
        segments.append(self.generate_audio_segment(intro_text, "Narrator", "intro"))
        
        # Conversation
        for turn in conversation_script.turns:
            speaker_name = "Dr. Ava D." if "Sarah" in turn.speaker or "Chen" in turn.speaker else turn.speaker
            cleaned_content = self.clean_dialogue_text(turn.content)
            segments.append(self.generate_audio_segment(cleaned_content, speaker_name, "conversation"))
        
        # Conclusion
        if conversation_script.conclusion:
            cleaned_conclusion = self.clean_dialogue_text(conversation_script.conclusion)
            segments.append(self.generate_audio_segment(cleaned_conclusion, "Narrator", "conclusion"))
        
        return segments
    
    def combine_audio_reliable(self, segments: List[AudioSegment], output_file: str) -> Dict:
        """Reliable audio combination using SOX (no FFmpeg complexity)"""
        
        print(f"🎵 Reliable combination of {len(segments)} segments with SOX...")
        
        # Convert all to consistent WAV format
        converted_files = []
        total_duration = 0
        
        for i, segment in enumerate(segments):
            converted_file = self.output_dir / f"reliable_{i:02d}.wav"
            
            try:
                # Convert to standard WAV format
                subprocess.run([
                    "ffmpeg", "-i", segment.audio_file, 
                    "-acodec", "pcm_s16le", "-ar", "22050", "-ac", "1",
                    "-y", str(converted_file)
                ], check=True, capture_output=True)
                
                converted_files.append(str(converted_file))
                total_duration += segment.duration
                print(f"   ✅ Converted {segment.speaker} ({segment.duration:.1f}s)")
                
            except subprocess.CalledProcessError:
                print(f"   ❌ Failed to convert {segment.audio_file}")
                continue
        
        # Combine with SOX (reliable method)
        if converted_files:
            try:
                subprocess.run(["sox"] + converted_files + [str(output_file)], check=True)
                print(f"   ✅ SOX combination successful!")
                
                # Clean up converted files
                for conv_file in converted_files:
                    Path(conv_file).unlink()
                
                return {
                    "output_file": output_file,
                    "total_duration": total_duration,
                    "num_segments": len(segments),
                    "method": "sox_reliable",
                    "segments": [
                        {"speaker": seg.speaker, "duration": seg.duration, "type": seg.segment_type}
                        for seg in segments
                    ]
                }
                
            except subprocess.CalledProcessError as e:
                raise Exception(f"SOX combination failed: {e}")
        
        raise Exception("No files to combine")
    
    def generate_complete_audio(self, conversation_script, base_filename: str) -> Dict:
        """Complete reliable audio generation"""
        
        print("🎬 Starting reliable YouTube audio generation...")
        
        if not self.check_requirements():
            raise Exception("Edge-TTS not available")
        
        # Generate segments
        segments = self.create_conversation_audio(conversation_script)
        
        # Output file
        output_file = self.output_dir / f"{base_filename}_RELIABLE_youtube.wav"
        
        # Reliable combination
        result = self.combine_audio_reliable(segments, str(output_file))
        
        # Save metadata
        metadata_file = self.output_dir / f"{base_filename}_reliable_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        result["metadata_file"] = str(metadata_file)
        
        print(f"🎉 Reliable YouTube audio complete!")
        print(f"   🎵 Audio: {output_file}")
        print(f"   📊 Duration: {result['total_duration']:.1f}s ({result['total_duration']/60:.1f} min)")
        print(f"   ✅ Method: {result['method']} (no FFmpeg complexity)")
        
        return result
