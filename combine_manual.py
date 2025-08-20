#!/usr/bin/env python3
"""Manual audio combination treating files as MP3"""

from pydub import AudioSegment
from pathlib import Path
import json
import glob

def combine_manually():
    audio_dir = Path("data/output/audio")
    
    print("🎵 Manual combination of Edge-TTS audio files...")
    
    # Get all audio files in chronological order
    audio_files = sorted(audio_dir.glob("*.wav"))
    
    # Try to load each file as MP3 (since Edge-TTS outputs MP3 with .wav extension)
    combined = AudioSegment.empty()
    
    for i, audio_file in enumerate(audio_files):
        try:
            print(f"   Loading {audio_file.name}...")
            
            # Load as MP3 since Edge-TTS outputs MP3 format
            audio = AudioSegment.from_mp3(str(audio_file))
            combined += audio
            
            # Add 0.8 second pause between segments (except after last)
            if i < len(audio_files) - 1:
                pause = AudioSegment.silent(duration=800)
                combined += pause
                
            print(f"     ✅ Added ({len(audio)/1000:.1f}s)")
            
        except Exception as e:
            print(f"     ❌ Failed to load {audio_file.name}: {e}")
            continue
    
    # Export final combined audio
    output_file = audio_dir / "MANUAL_combined_youtube.wav"
    combined.export(str(output_file), format="wav")
    
    duration_minutes = len(combined) / 1000 / 60
    
    print(f"\n✅ Manual combination complete!")
    print(f"   📁 File: {output_file}")
    print(f"   ⏱️  Duration: {len(combined)/1000:.1f} seconds ({duration_minutes:.1f} minutes)")
    print(f"   🎤 Files combined: {len(audio_files)}")
    
    return str(output_file)

if __name__ == "__main__":
    result = combine_manually()
    print(f"\n🎉 YouTube audio ready for testing!")
    print(f"🎧 Test with: play {result}")
