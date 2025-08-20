#!/usr/bin/env python3
"""Direct FFmpeg combination"""

from pathlib import Path
import subprocess
import glob

def combine_with_ffmpeg():
    audio_dir = Path("data/output/audio")
    
    # Get all .wav files (which are actually MP3)
    audio_files = sorted(audio_dir.glob("*.wav"))
    
    print(f"🎵 Combining {len(audio_files)} files with FFmpeg...")
    
    # Create input list for FFmpeg
    input_list = audio_dir / "ffmpeg_input.txt"
    
    with open(input_list, 'w') as f:
        for audio_file in audio_files:
            # Tell FFmpeg to treat as MP3 format
            f.write(f"file '{audio_file}'\n")
    
    output_file = audio_dir / "FFMPEG_combined_youtube.wav"
    
    try:
        # Use FFmpeg to combine, forcing input format as MP3
        cmd = [
            "ffmpeg", 
            "-f", "concat", 
            "-safe", "0", 
            "-i", str(input_list),
            "-f", "mp3",  # Force input format as MP3
            "-acodec", "pcm_s16le",  # Convert to WAV codec
            "-ar", "22050",  # Set sample rate
            "-y", str(output_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ FFmpeg combination successful!")
            print(f"   📁 Output: {output_file}")
            
            # Clean up
            input_list.unlink()
            return str(output_file)
        else:
            print(f"❌ FFmpeg failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ FFmpeg error: {e}")
        return None

if __name__ == "__main__":
    result = combine_with_ffmpeg()
    if result:
        print(f"🎉 YouTube audio ready: {result}")
