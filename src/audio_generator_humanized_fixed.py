"""
Audio Generator with Humanization & Fixed Voices
Save as: src/audio_generator_humanized_fixed.py

Features:
- Multi-stage text cleanup and humanization
- 3 distinct voices (Host, Dr. Ava D., Prof. Marcus W.)
- Natural academic debate speech
"""

import os
import asyncio
import subprocess
import time
import re
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass
import json

try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False

from enhanced_text_humanizer import EnhancedTextHumanizer, SmartFieldExtractor


@dataclass
class AudioSegment:
    speaker: str
    original_text: str
    humanized_text: str
    audio_file: str
    duration: float
    segment_type: str
    voice_used: str


@dataclass
class VoiceProfile:
    name: str
    voice_id: str
    description: str
    personality_type: str


class HumanizedAudioGenerator:
    """Audio generator with multi-stage humanization and proper voice differentiation"""
    
    def __init__(self, output_dir: str = "data/output/audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # FIXED: 3 completely different voices
        self.voice_profiles = {
            "narrator": VoiceProfile(
                "Narrator", 
                "en-US-AriaNeural",  # Professional female narrator
                "Professional podcast host",
                "neutral"
            ),
            "dr_ava": VoiceProfile(
                "Dr. Ava D.", 
                "en-US-JennyNeural",  # Enthusiastic female researcher
                "Enthusiastic female researcher",
                "optimist"
            ),
            "prof_marcus": VoiceProfile(
                "Prof. Marcus W.", 
                "en-US-GuyNeural",  # CHANGED: Male voice, different from narrator
                "Skeptical male professor",
                "skeptic"
            )
        }
        
        # Initialize humanizer
        self.text_humanizer = EnhancedTextHumanizer()
        self.field_extractor = SmartFieldExtractor()
        
        print(f"🎙️ Humanized Audio Generator Initialized")
        print("✅ Voice differentiation:")
        for key, profile in self.voice_profiles.items():
            print(f"   {profile.name}: {profile.voice_id} ({profile.description})")
    
    def check_requirements(self) -> bool:
        return HAS_EDGE_TTS
    
    def get_speaker_voice_profile(self, speaker: str) -> VoiceProfile:
        """Get appropriate voice profile for speaker with proper differentiation"""
        
        speaker_lower = speaker.lower()
        
        # Map speaker names to voice profiles
        if any(word in speaker_lower for word in ["narrator", "host", "welcome"]):
            return self.voice_profiles["narrator"]
        elif any(word in speaker_lower for word in ["ava", "sarah", "dr."]):
            return self.voice_profiles["dr_ava"]
        elif any(word in speaker_lower for word in ["marcus", "webb", "prof."]):
            return self.voice_profiles["prof_marcus"]
        else:
            # Default to narrator for unknown speakers
            return self.voice_profiles["narrator"]
    
    def humanize_speaker_name(self, speaker: str) -> str:
        """Convert speaker names to preferred format"""
        
        if "Prof. Marcus Webb" in speaker:
            return "Prof. Marcus W."
        elif "Professor Marcus Webb" in speaker:
            return "Prof. Marcus W."
        elif "Marcus Webb" in speaker:
            return "Prof. Marcus W."
        else:
            return speaker
    
    async def generate_humanized_speech(self, text: str, speaker: str, 
                                      research_field: str, output_file: str) -> float:
        """Generate speech with complete humanization pipeline"""
        
        print(f"\n🎤 Generating humanized speech for {speaker}")
        
        # Step 1: Clean speaker name
        clean_speaker = self.humanize_speaker_name(speaker)
        
        # Step 2: Get voice profile
        voice_profile = self.get_speaker_voice_profile(clean_speaker)
        
        # Step 3: Multi-stage text cleanup and humanization
        cleanup_result = self.text_humanizer.complete_cleanup_pipeline(
            text=text,
            speaker_role=voice_profile.personality_type,
            research_field=research_field
        )
        
        # Step 4: Generate speech with humanized text
        final_text = cleanup_result.final_speech_ready
        
        print(f"   🎯 Voice: {voice_profile.voice_id}")
        print(f"   📝 Original: {text[:60]}...")
        print(f"   ✨ Humanized: {final_text[:60]}...")
        
        try:
            communicate = edge_tts.Communicate(final_text, voice_profile.voice_id)
            await communicate.save(output_file)
            
            # Get accurate duration
            duration = self._get_audio_duration(output_file)
            print(f"   ✅ Generated: {duration:.1f}s")
            
            return duration, cleanup_result
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            raise
    
    def _get_audio_duration(self, audio_file: str) -> float:
        """Get accurate audio duration"""
        try:
            result = subprocess.run([
                "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                "-of", "csv=p=0", audio_file
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return float(result.stdout.strip())
        except:
            pass
        
        # Fallback estimation
        return 3.0
    
    def generate_enhanced_introduction_audio(self, introduction_text: str, 
                                           research_field: str) -> AudioSegment:
        """Generate humanized introduction audio"""
        
        print("🎬 Generating enhanced introduction with field-specific humanization...")
        
        # Clean up field first
        clean_field = self.field_extractor.extract_specific_field(research_field)
        
        timestamp = int(time.time() * 1000)
        output_file = self.output_dir / f"humanized_intro_{timestamp}.mp3"
        
        duration, cleanup_result = asyncio.run(
            self.generate_humanized_speech(
                introduction_text, "narrator", clean_field, str(output_file)
            )
        )
        
        return AudioSegment(
            speaker="Narrator",
            original_text=introduction_text,
            humanized_text=cleanup_result.final_speech_ready,
            audio_file=str(output_file),
            duration=duration,
            segment_type="enhanced_intro",
            voice_used=self.voice_profiles["narrator"].voice_id
        )
    
    def generate_humanized_dialogue_segments(self, conversation_script, 
                                          research_field: str) -> List[AudioSegment]:
        """Generate dialogue segments with complete humanization"""
        
        print(f"💬 Generating {len(conversation_script.turns)} humanized dialogue segments...")
        
        # Clean up field
        clean_field = self.field_extractor.extract_specific_field(research_field)
        
        segments = []
        
        for i, turn in enumerate(conversation_script.turns, 1):
            print(f"\n--- Turn {i}/{len(conversation_script.turns)} ---")
            
            # Generate unique filename
            timestamp = int(time.time() * 1000) + i
            clean_speaker = self.humanize_speaker_name(turn.speaker)
            safe_speaker = clean_speaker.replace(" ", "_").replace(".", "")
            output_file = self.output_dir / f"humanized_{safe_speaker}_{timestamp}.mp3"
            
            try:
                duration, cleanup_result = asyncio.run(
                    self.generate_humanized_speech(
                        turn.content, turn.speaker, clean_field, str(output_file)
                    )
                )
                
                voice_profile = self.get_speaker_voice_profile(clean_speaker)
                
                segment = AudioSegment(
                    speaker=clean_speaker,
                    original_text=turn.content,
                    humanized_text=cleanup_result.final_speech_ready,
                    audio_file=str(output_file),
                    duration=duration,
                    segment_type="dialogue",
                    voice_used=voice_profile.voice_id
                )
                
                segments.append(segment)
                
            except Exception as e:
                print(f"❌ Error generating dialogue for {turn.speaker}: {e}")
                continue
        
        print(f"✅ Generated {len(segments)} humanized dialogue segments")
        return segments
    
    def generate_humanized_conclusion_audio(self, conclusion_text: str, 
                                          research_field: str) -> AudioSegment:
        """Generate humanized conclusion audio"""
        
        print("🎯 Generating humanized conclusion...")
        
        # Clean up field
        clean_field = self.field_extractor.extract_specific_field(research_field)
        
        timestamp = int(time.time() * 1000)
        output_file = self.output_dir / f"humanized_conclusion_{timestamp}.mp3"
        
        duration, cleanup_result = asyncio.run(
            self.generate_humanized_speech(
                conclusion_text, "narrator", clean_field, str(output_file)
            )
        )
        
        return AudioSegment(
            speaker="Narrator",
            original_text=conclusion_text,
            humanized_text=cleanup_result.final_speech_ready,
            audio_file=str(output_file),
            duration=duration,
            segment_type="enhanced_conclusion",
            voice_used=self.voice_profiles["narrator"].voice_id
        )
    
    def create_complete_humanized_audio(self, conversation_script, 
                                      research_field: str) -> List[AudioSegment]:
        """Create complete audio with full humanization pipeline"""
        
        print("🎵 Creating complete humanized audio...")
        
        all_segments = []
        
        # 1. Humanized Introduction
        intro_segment = self.generate_enhanced_introduction_audio(
            conversation_script.introduction, research_field
        )
        all_segments.append(intro_segment)
        
        # 2. Humanized Dialogue
        dialogue_segments = self.generate_humanized_dialogue_segments(
            conversation_script, research_field
        )
        all_segments.extend(dialogue_segments)
        
        # 3. Humanized Conclusion
        conclusion_segment = self.generate_humanized_conclusion_audio(
            conversation_script.conclusion, research_field
        )
        all_segments.append(conclusion_segment)
        
        print(f"✅ Complete humanized audio: {len(all_segments)} segments")
        return all_segments
    
    def combine_humanized_segments(self, segments: List[AudioSegment], 
                                 output_file: str) -> Dict:
        """Combine humanized segments with detailed metadata"""
        
        print(f"🎵 Combining {len(segments)} humanized segments...")
        
        converted_files = []
        total_duration = 0
        segment_info = []
        
        for i, segment in enumerate(segments):
            converted_file = self.output_dir / f"humanized_{i:02d}.wav"
            
            try:
                # Convert to WAV
                subprocess.run([
                    "ffmpeg", "-i", segment.audio_file,
                    "-acodec", "pcm_s16le", "-ar", "22050", "-ac", "1",
                    "-y", str(converted_file)
                ], check=True, capture_output=True)
                
                converted_files.append(str(converted_file))
                total_duration += segment.duration
                
                segment_info.append({
                    "speaker": segment.speaker,
                    "duration": segment.duration,
                    "type": segment.segment_type,
                    "voice_used": segment.voice_used,
                    "original_text": segment.original_text[:100],
                    "humanized_text": segment.humanized_text[:100],
                    "humanization_applied": True
                })
                
                print(f"   ✅ {segment.speaker} ({segment.voice_used}): {segment.duration:.1f}s")
                
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Failed to convert {segment.audio_file}: {e}")
                continue
        
        # Combine with SOX
        if converted_files:
            try:
                subprocess.run(["sox"] + converted_files + [str(output_file)], check=True)
                print(f"   ✅ Humanized audio combination successful!")
                
                # Cleanup temporary files
                for conv_file in converted_files:
                    Path(conv_file).unlink()
                
                # Voice usage summary
                voice_usage = {}
                for segment in segments:
                    voice_usage[segment.voice_used] = voice_usage.get(segment.voice_used, 0) + 1
                
                return {
                    "output_file": output_file,
                    "total_duration": total_duration,
                    "num_segments": len(segments),
                    "method": "humanized_audio_generation",
                    "segments": segment_info,
                    "voice_differentiation": voice_usage,
                    "humanization_pipeline": "multi_stage_complete",
                    "voices_used": list(voice_usage.keys())
                }
                
            except subprocess.CalledProcessError as e:
                raise Exception(f"Humanized audio combination failed: {e}")
        
        raise Exception("No segments to combine")
    
    def generate_complete_humanized_audio(self, conversation_script, base_filename: str) -> Dict:
        """Complete humanized audio generation with all enhancements"""
        
        print("🚀 COMPLETE HUMANIZED AUDIO GENERATION")
        print("✅ Multi-stage text cleanup")
        print("✅ AI humanization")  
        print("✅ 3 distinct voices")
        print("✅ Natural academic debate speech")
        
        if not self.check_requirements():
            raise Exception("Edge-TTS not available")
        
        # Extract research field for humanization context
        research_field = getattr(conversation_script, 'research_field', 'Research')
        
        # Generate all humanized segments
        segments = self.create_complete_humanized_audio(conversation_script, research_field)
        
        # Output file
        output_file = self.output_dir / f"{base_filename}_HUMANIZED_youtube.wav"
        
        # Combine with humanization metadata
        result = self.combine_humanized_segments(segments, str(output_file))
        
        # Save humanization metadata
        metadata_file = self.output_dir / f"{base_filename}_humanized_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        result["metadata_file"] = str(metadata_file)
        
        print(f"\n🎉 HUMANIZED AUDIO COMPLETE!")
        print(f"   🎵 Audio: {output_file}")
        print(f"   ⏱️ Duration: {result['total_duration']:.1f}s ({result['total_duration']/60:.1f} min)")
        print(f"   🎭 Voices: {len(result['voices_used'])} distinct voices")
        print(f"   🤖 Humanization: ✅ AI-enhanced natural speech")
        print(f"   📝 Text Cleanup: ✅ Multi-stage pipeline applied")
        
        # Voice differentiation summary
        print(f"   🎤 Voice Usage:")
        for voice, count in result['voice_differentiation'].items():
            print(f"      {voice}: {count} segments")
        
        return result


# Test function
def test_humanized_audio_generation():
    """Test the humanized audio generation"""
    
    print("🧪 TESTING HUMANIZED AUDIO GENERATION")
    print("=" * 80)
    
    generator = HumanizedAudioGenerator()
    
    if not generator.check_requirements():
        print("❌ Requirements not met")
        return False
    
    # Test voice profiles
    print("\n🎤 VOICE PROFILE TEST:")
    test_speakers = ["Narrator", "Dr. Ava D.", "Prof. Marcus Webb", "Prof. Marcus W."]
    
    for speaker in test_speakers:
        profile = generator.get_speaker_voice_profile(speaker)
        clean_name = generator.humanize_speaker_name(speaker)
        print(f"   {speaker} → {clean_name} → {profile.voice_id} ({profile.personality_type})")
    
    # Test text humanization (without full audio generation)
    print("\n🧹 TEXT HUMANIZATION TEST:")
    test_texts = [
        "** Computer Science - Algorithms and Network Analysis",
        "** Lack of context: The paper does not provide sufficient information.",
        "Today's fascinating topic: ** Network Analysis Research"
    ]
    
    for text in test_texts:
        specific_field = generator.field_extractor.extract_specific_field(text)
        print(f"   {text} → {specific_field}")
    
    print("\n✅ Humanized audio generation system ready!")
    return True


if __name__ == "__main__":
    test_humanized_audio_generation()
