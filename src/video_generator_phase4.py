"""Phase 4 Video Generator - Create YouTube-ready videos from Phase 3 audio output"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass

# MoviePy imports with error handling
try:
    import moviepy
    print(f"📦 MoviePy version: {moviepy.__version__}")
    
    from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, ColorClip, CompositeVideoClip
    print("✅ MoviePy imported successfully")
except ImportError as e:
    print(f"❌ MoviePy import error: {e}")
    print("🔧 Try installing a compatible version:")
    print("   pip uninstall moviepy")
    print("   pip install moviepy==1.0.3")
    sys.exit(1)

@dataclass
class VideoSegment:
    """Represents one video segment with timing"""
    speaker: str
    text: str
    start_time: float
    duration: float
    segment_type: str

@dataclass 
class VideoConfig:
    """Video generation configuration"""
    width: int = 1920
    height: int = 1080
    fps: int = 24
    background_color: str = "#1a1a2e"  # Dark blue
    title_color: str = "#ffffff"
    ava_color: str = "#00d4aa"  # Teal for Dr. Ava (optimistic)
    marcus_color: str = "#ff6b6b"  # Red for Prof. Marcus (skeptical)
    narrator_color: str = "#ffd93d"  # Yellow for narrator
    font_size: int = 48
    title_font_size: int = 72
    font: str = "Arial-Bold"

class YouTubeVideoGenerator:
    """Generate YouTube-ready videos from Phase 3 output"""
    
    def __init__(self, config: VideoConfig = None):
        self.config = config or VideoConfig()
        print(f"🎬 YouTube Video Generator Initialized")
        print(f"   📺 Resolution: {self.config.width}x{self.config.height}")
        print(f"   🎨 Background: {self.config.background_color}")
    
    def load_phase3_data(self, phase3_json_path: str) -> Dict:
        """Load Phase 3 results and extract video data"""
        with open(phase3_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        audio_result = data["phase3_audio"]
        audio_file = audio_result["output_file"]
        
        if not Path(audio_file).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        print(f"📁 Loaded Phase 3 data:")
        print(f"   🎵 Audio: {audio_file}")
        print(f"   ⏱️  Duration: {audio_result['total_duration']:.1f}s")
        print(f"   📊 Segments: {audio_result['num_segments']}")
        
        return data
    
    def extract_conversation_segments(self, phase3_data: Dict) -> List[VideoSegment]:
        """Extract timed conversation segments from Phase 3 data"""
        
        # Get audio segments with timing
        audio_segments = phase3_data["phase3_audio"]["segments"]
        
        # We need to reconstruct the conversation text
        # For now, we'll create segments based on the audio timing
        video_segments = []
        current_time = 0.0
        
        for i, segment in enumerate(audio_segments):
            speaker = segment["speaker"]
            duration = segment["duration"]
            segment_type = segment["type"]
            
            # Create appropriate text based on segment type and speaker
            if segment_type == "intro":
                text = f"Welcome to Research Rundown!\n\nToday's Topic: Community Detection Algorithms\n\nFeaturing: Dr. Ava D. vs Prof. Marcus Webb"
            elif segment_type == "conclusion":
                text = f"Thank you for joining Research Rundown!\n\nWhat did you think of this debate?\n\nSubscribe for more research discussions!"
            else:
                # Conversation segment - create speaker-appropriate text
                if "Ava" in speaker or "Dr." in speaker:
                    text = f"Dr. Ava D. discusses the innovative aspects of WCC and CM algorithms, highlighting their potential for large-scale network analysis..."
                else:
                    text = f"Prof. Marcus Webb raises critical questions about the methodology and questions the claimed performance improvements..."
            
            video_segments.append(VideoSegment(
                speaker=speaker,
                text=text,
                start_time=current_time,
                duration=duration,
                segment_type=segment_type
            ))
            
            current_time += duration
        
        print(f"📝 Created {len(video_segments)} video segments")
        return video_segments
    
    def create_text_clip(self, text: str, speaker: str, duration: float):
        """Create a text clip with speaker-specific styling"""
        
        # Choose color based on speaker
        if "Ava" in speaker or "Dr." in speaker:
            color = self.config.ava_color
            speaker_label = "Dr. Ava D. (Optimistic Researcher)"
        elif "Marcus" in speaker or "Prof." in speaker:
            color = self.config.marcus_color  
            speaker_label = "Prof. Marcus Webb (Critical Analyst)"
        else:
            color = self.config.narrator_color
            speaker_label = "Narrator"
        
        # Create speaker name clip
        speaker_clip = TextClip(
            speaker_label,
            fontsize=self.config.font_size - 8,
            color=color,
            font=self.config.font,
            size=(self.config.width - 200, None)
        ).set_position(('center', 'top')).set_margin(50)
        
        # Create main text clip
        main_text_clip = TextClip(
            text,
            fontsize=self.config.font_size,
            color=self.config.title_color,
            font=self.config.font,
            size=(self.config.width - 200, None),
            method='caption'
        ).set_position('center')
        
        # Combine speaker name and text
        combined = CompositeVideoClip([
            speaker_clip,
            main_text_clip.set_position(('center', 'center'))
        ], size=(self.config.width, self.config.height))
        
        return combined.set_duration(duration)
    
    def create_title_screen(self, paper_topic: str):
        """Create opening title screen"""
        
        title_text = f"Research Rundown\n\n{paper_topic}\n\nDr. Ava D. vs Prof. Marcus Webb"
        
        title_clip = TextClip(
            title_text,
            fontsize=self.config.title_font_size,
            color=self.config.title_color,
            font=self.config.font,
            size=(self.config.width - 100, None),
            method='caption'
        ).set_position('center').set_duration(5)
        
        background = ColorClip(
            size=(self.config.width, self.config.height),
            color=self.config.background_color
        ).set_duration(5)
        
        return CompositeVideoClip([background, title_clip])
    
    def generate_complete_video(self, phase3_json_path: str, output_filename: str = None) -> str:
        """Generate complete YouTube-ready video"""
        
        print("🎬 Starting YouTube video generation...")
        
        # Load Phase 3 data
        phase3_data = self.load_phase3_data(phase3_json_path)
        
        # Extract conversation segments
        video_segments = self.extract_conversation_segments(phase3_data)
        
        # Get audio file
        audio_file = phase3_data["phase3_audio"]["output_file"]
        audio_clip = AudioFileClip(audio_file)
        
        print(f"🎵 Loaded audio: {audio_clip.duration:.1f}s")
        
        # Create background
        background = ColorClip(
            size=(self.config.width, self.config.height),
            color=self.config.background_color
        ).set_duration(audio_clip.duration)
        
        # Create video clips for each segment
        video_clips = []
        
        for segment in video_segments:
            print(f"   📝 Creating clip: {segment.speaker} ({segment.duration:.1f}s)")
            
            text_clip = self.create_text_clip(
                segment.text,
                segment.speaker,
                segment.duration
            ).set_start(segment.start_time)
            
            video_clips.append(text_clip)
        
        # Combine all video elements
        print("🎬 Compositing final video...")
        final_video = CompositeVideoClip([background] + video_clips)
        
        # Add audio
        final_video = final_video.set_audio(audio_clip)
        
        # Set output filename
        if not output_filename:
            base_name = Path(phase3_json_path).stem.replace("_COMPLETE_phase3", "")
            output_filename = f"data/output/video/{base_name}_YOUTUBE_final.mp4"
        
        # Create output directory
        output_path = Path(output_filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Render video
        print(f"🎥 Rendering video to: {output_filename}")
        print("   ⚠️  This may take several minutes...")
        
        final_video.write_videofile(
            output_filename,
            fps=self.config.fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            verbose=False,
            logger=None
        )
        
        # Cleanup
        audio_clip.close()
        final_video.close()
        
        print(f"✅ Video generation complete!")
        print(f"   📁 Output: {output_filename}")
        print(f"   📊 Duration: {audio_clip.duration:.1f}s ({audio_clip.duration/60:.1f} minutes)")
        print(f"   📺 Resolution: {self.config.width}x{self.config.height}")
        
        return output_filename


def main():
    """Phase 4 main entry point"""
    
    print("🎬 AI Paper Narrator - Phase 4")
    print("YouTube Video Generation")
    print("-" * 60)
    
    if len(sys.argv) < 2:
        print("Usage: python video_generator_phase4.py <phase3_json_file>")
        print("Example: python video_generator_phase4.py data/output/WCC_and_CM_Paper_Complex_Networks-1_COMPLETE_phase3.json")
        sys.exit(1)
    
    phase3_json_path = sys.argv[1]
    
    if not Path(phase3_json_path).exists():
        print(f"❌ Phase 3 JSON file not found: {phase3_json_path}")
        sys.exit(1)
    
    try:
        # Create video generator with YouTube-optimized settings
        config = VideoConfig(
            width=1920,
            height=1080,
            fps=24,
            background_color="#1a1a2e",
            font_size=52,
            title_font_size=76
        )
        
        generator = YouTubeVideoGenerator(config)
        
        # Generate video
        output_file = generator.generate_complete_video(phase3_json_path)
        
        print(f"\n🎉 PHASE 4 COMPLETE!")
        print(f"🎬 YouTube-ready video: {output_file}")
        print(f"📺 Ready to upload to YouTube!")
        
        # Display final summary
        file_size_mb = Path(output_file).stat().st_size / (1024 * 1024)
        print(f"\n📊 FINAL VIDEO STATS:")
        print(f"   📁 File size: {file_size_mb:.1f} MB")
        print(f"   🎥 Format: MP4 (H.264 + AAC)")
        print(f"   📺 Resolution: 1920x1080 @ 24fps")
        print(f"   🎤 Speakers: Dr. Ava D. (Teal) & Prof. Marcus Webb (Red)")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
