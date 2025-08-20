# src/audio_generator_fixed.py
"""Fixed Audio Generator with Automated Combination and Correct Names"""

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


class FixedAudioGenerator:
    """Fixed audio generator with automated combination and correct names"""
    
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
        
        print(f"🎙️ Fixed Audio Generator Initialized")
        print("✅ Using Edge-TTS with automated combination")
    
    def check_requirements(self) -> bool:
        """Check if Edge-TTS is available"""
        return HAS_EDGE_TTS
    
    def clean_dialogue_text(self, text: str) -> str:
        """Fix name references in dialogue text"""
        
        # Replace any references to "Dr. Chen" or "Sarah" with "Dr. Ava D."
        cleaned_text = text.replace("Dr. Chen", "Dr. Ava D.")
        cleaned_text = cleaned_text.replace("Dr. Sarah Chen", "Dr. Ava D.")
        cleaned_text = cleaned_text.replace("Sarah", "Ava")
        
        return cleaned_text
    
    def generate_youtube_intro(self, paper_title: str) -> str:
        """Generate dramatic YouTube intro"""
        intro_text = f"""What happens when you give two brilliant researchers the same groundbreaking paper and completely opposite viewpoints? 

Welcome to Research Rundown! 

Today's explosive topic: '{paper_title}' - a research study that promises to be revolutionary. But is it revolutionary breakthrough or overblown hype? 

Dr. Ava D. and Prof. Marcus Webb are about to find out!"""
        
        return intro_text
    
    async def text_to_speech_edge(self, text: str, voice_id: str, output_file: str) -> float:
        """Generate speech using Edge TTS with correct timing"""
        
        # Clean the text first
        cleaned_text = self.clean_dialogue_text(text)
        
        communicate = edge_tts.Communicate(cleaned_text, voice_id)
        await communicate.save(output_file)
        
        # Get actual duration from the file (more accurate)
        try:
            # Use ffprobe to get exact duration
            result = subprocess.run([
                "ffprobe", "-v", "quiet", "-show_entries", "format=duration", 
                "-of", "csv=p=0", output_file
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                duration = float(result.stdout.strip())
            else:
                # Fallback to word count estimation
                word_count = len(cleaned_text.split())
                duration = (word_count / 150) * 60
        except:
            # Ultimate fallback
            word_count = len(cleaned_text.split())
            duration = (word_count / 150) * 60
        
        return duration
    
    def generate_audio_segment(self, text: str, speaker: str, segment_type: str = "conversation") -> AudioSegment:
        """Generate audio for one segment with correct timing"""
        
        # Determine voice profile
        if "ava" in speaker.lower():
            profile = self.voice_profiles["dr_ava"]
        else:
            profile = self.voice_profiles["prof_marcus"]
        
        # Create output filename
        timestamp = int(time.time() * 1000)
        safe_speaker = speaker.replace(" ", "_").replace(".", "")
        output_file = self.output_dir / f"{safe_speaker}_{segment_type}_{timestamp}.mp3"  # Use .mp3 extension
        
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
        """Convert conversation script to audio with proper naming"""
        
        print("🎙️ Generating conversation audio with fixed names...")
        
        audio_segments = []
        
        # 1. YouTube intro
        paper_title = conversation_script.paper_topic
        intro_text = self.generate_youtube_intro(paper_title)
        
        print("   📺 Generating YouTube intro...")
        intro_segment = self.generate_audio_segment(intro_text, "Narrator", "intro")
        audio_segments.append(intro_segment)
        
        # 2. Conversation turns with corrected names
        print(f"   💬 Generating {len(conversation_script.turns)} conversation turns...")
        
        for turn in conversation_script.turns:
            # Fix speaker names
            speaker_name = turn.speaker
            if "Sarah" in speaker_name or "Chen" in speaker_name:
                speaker_name = "Dr. Ava D."
            
            # Clean the content text
            cleaned_content = self.clean_dialogue_text(turn.content)
            
            segment = self.generate_audio_segment(cleaned_content, speaker_name, "conversation")
            audio_segments.append(segment)
        
        # 3. Conclusion
        if conversation_script.conclusion:
            print("   🏁 Generating conclusion...")
            cleaned_conclusion = self.clean_dialogue_text(conversation_script.conclusion)
            conclusion_segment = self.generate_audio_segment(
                cleaned_conclusion, "Narrator", "conclusion"
            )
            audio_segments.append(conclusion_segment)
        
        return audio_segments
    
    def combine_audio_automated(self, segments: List[AudioSegment], output_file: str) -> Dict:
        """Automated audio combination with correct timing"""
        
        print(f"🎵 Automated combination of {len(segments)} segments...")
        
        # Create ordered file list
        ordered_files = []
        total_calculated_duration = 0
        
        for i, segment in enumerate(segments):
            ordered_files.append(segment.audio_file)
            total_calculated_duration += segment.duration
            print(f"   {i+1}. {segment.speaker} ({segment.segment_type}): {segment.duration:.1f}s")
        
        print(f"   📊 Expected total duration: {total_calculated_duration:.1f}s ({total_calculated_duration/60:.1f} min)")
        
        # Method 1: FFmpeg with explicit format and no re-encoding
        try:
            # Create input list
            input_list = self.output_dir / "auto_input_list.txt"
            
            with open(input_list, 'w') as f:
                for audio_file in ordered_files:
                    f.write(f"file '{audio_file}'\n")
            
            # Use FFmpeg to concatenate without re-encoding (preserves timing)
            cmd = [
                "ffmpeg", 
                "-f", "concat", 
                "-safe", "0", 
                "-i", str(input_list),
                "-c", "copy",  # Copy without re-encoding to preserve timing
                "-y", str(output_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Verify actual duration
                duration_result = subprocess.run([
                    "ffprobe", "-v", "quiet", "-show_entries", "format=duration", 
                    "-of", "csv=p=0", output_file
                ], capture_output=True, text=True)
                
                if duration_result.returncode == 0:
                    actual_duration = float(duration_result.stdout.strip())
                    print(f"   ✅ FFmpeg combination successful!")
                    print(f"   📊 Actual duration: {actual_duration:.1f}s ({actual_duration/60:.1f} min)")
                    
                    # Clean up
                    input_list.unlink()
                    
                    return {
                        "output_file": output_file,
                        "total_duration": actual_duration,
                        "calculated_duration": total_calculated_duration,
                        "num_segments": len(segments),
                        "method": "ffmpeg_copy",
                        "segments": [
                            {
                                "speaker": seg.speaker,
                                "duration": seg.duration,
                                "type": seg.segment_type
                            }
                            for seg in segments
                        ]
                    }
                else:
                    raise Exception("Could not verify duration")
            else:
                raise Exception(f"FFmpeg failed: {result.stderr}")
                
        except Exception as e:
            print(f"   ⚠️  FFmpeg copy failed: {e}")
            
            # Fallback: Convert to WAV and combine
            return self._combine_with_conversion(segments, output_file)
    
    def _combine_with_conversion(self, segments: List[AudioSegment], output_file: str) -> Dict:
        """Fallback: Convert to consistent format and combine"""
        
        print("   🔄 Using conversion fallback...")
        
        # Convert all to same format first
        converted_files = []
        total_duration = 0
        
        for i, segment in enumerate(segments):
            converted_file = self.output_dir / f"conv_{i:02d}.wav"
            
            try:
                subprocess.run([
                    "ffmpeg", "-i", segment.audio_file, 
                    "-acodec", "pcm_s16le", "-ar", "22050", "-ac", "1",
                    "-y", str(converted_file)
                ], check=True, capture_output=True)
                
                converted_files.append(str(converted_file))
                total_duration += segment.duration
                
            except subprocess.CalledProcessError:
                print(f"     ❌ Failed to convert {segment.audio_file}")
        
        # Combine converted files
        if converted_files:
            try:
                # Use sox for reliable combination
                subprocess.run(["sox"] + converted_files + [str(output_file)], check=True)
                
                # Clean up converted files
                for conv_file in converted_files:
                    Path(conv_file).unlink()
                
                return {
                    "output_file": output_file,
                    "total_duration": total_duration,
                    "calculated_duration": total_duration,
                    "num_segments": len(segments),
                    "method": "sox_conversion",
                    "segments": [
                        {"speaker": seg.speaker, "duration": seg.duration, "type": seg.segment_type}
                        for seg in segments
                    ]
                }
                
            except subprocess.CalledProcessError as e:
                raise Exception(f"Sox combination failed: {e}")
        
        raise Exception("No files to combine")
    
    def generate_complete_audio(self, conversation_script, base_filename: str) -> Dict:
        """Complete automated audio generation pipeline"""
        
        print("🎬 Starting automated audio generation for YouTube...")
        
        if not self.check_requirements():
            raise Exception("Edge-TTS not available. Install with: pip install edge-tts")
        
        # Generate audio segments with cleaned names
        segments = self.create_conversation_audio(conversation_script)
        
        # Output file
        output_file = self.output_dir / f"{base_filename}_AUTOMATED_youtube.wav"
        
        # Automated combination
        result = self.combine_audio_automated(segments, str(output_file))
        
        # Save metadata
        metadata_file = self.output_dir / f"{base_filename}_auto_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        result["metadata_file"] = str(metadata_file)
        
        print(f"🎉 Automated YouTube audio generation complete!")
        print(f"   🎵 Audio: {output_file}")
        print(f"   📊 Duration: {result['total_duration']:.1f}s ({result['total_duration']/60:.1f} min)")
        print(f"   ✅ All names corrected (Dr. Ava D., Prof. Marcus Webb)")
        
        return result


def main():
    """Test the fixed audio generator"""
    
    print("🧪 Testing Fixed Audio Generator...")
    
    generator = FixedAudioGenerator()
    
    if not generator.check_requirements():
        print("❌ Edge-TTS not available")
        return
    
    # Test name cleaning
    test_text = "Hello Dr. Chen! I'm excited to discuss this with Sarah and Dr. Sarah Chen."
    cleaned = generator.clean_dialogue_text(test_text)
    print(f"✅ Name cleaning test:")
    print(f"   Before: {test_text}")
    print(f"   After:  {cleaned}")
    
    print(f"\n🎉 Fixed audio system ready!")


if __name__ == "__main__":
    main()
