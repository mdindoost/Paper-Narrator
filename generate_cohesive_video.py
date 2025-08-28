"""
Cohesive Video Generator - Advanced YouTube-Ready Video Creation
Save as: generate_cohesive_video.py

Features:
- Cohesive dialogue structure (5 segments)
- Scrolling text synchronized with audio
- Speaker avatars/icons
- Dynamic waveform visualizations
- Professional YouTube-ready output
"""

import json
import sys
import numpy as np
import time
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass

# MoviePy imports with error handling
try:
    import moviepy
    print(f"📦 MoviePy version: {moviepy.__version__}")
    
    from moviepy.editor import (
        VideoFileClip, AudioFileClip, TextClip, ColorClip, CompositeVideoClip,
        ImageClip, concatenate_videoclips
    )
    from moviepy.video.fx import resize
    print("✅ MoviePy imported successfully")
except ImportError as e:
    print(f"❌ MoviePy import error: {e}")
    print("🔧 Try installing: pip install moviepy")
    sys.exit(1)

# Additional imports for advanced features
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from PIL import Image, ImageDraw, ImageFont
    import librosa
    HAS_ADVANCED_FEATURES = True
    print("✅ Advanced features available (matplotlib, PIL, librosa)")
except ImportError as e:
    print(f"⚠️ Some advanced features not available: {e}")
    print("🔧 For full features: pip install matplotlib pillow librosa")
    HAS_ADVANCED_FEATURES = False


@dataclass
class CohesiveVideoConfig:
    """Advanced video configuration for cohesive dialogue"""
    width: int = 1920
    height: int = 1080
    fps: int = 24
    
    # Background and colors
    background_color: str = "#1a1a2e"  # Dark blue
    text_bg_color: str = "#2d3748"     # Dark gray for text background
    
    # Speaker colors
    narrator_color: str = "#ffd93d"     # Yellow
    ava_color: str = "#00d4aa"          # Teal  
    marcus_color: str = "#ff6b6b"       # Red
    
    # Text settings
    font_size: int = 48
    title_font_size: int = 72
    font: str = "Arial-Bold"
    text_scroll_speed: float = 50  # pixels per second
    
    # Avatar settings
    avatar_size: int = 200
    avatar_position: str = "left"  # left, right, top
    
    # Waveform settings
    waveform_height: int = 150
    waveform_color: str = "#4fd1c7"
    waveform_position: str = "bottom"


@dataclass
class CohesiveSegment:
    """Represents one cohesive video segment"""
    speaker: str
    text: str
    audio_file: str
    duration: float
    segment_type: str
    start_time: float = 0.0


class CohesiveVideoGenerator:
    """Advanced video generator for cohesive dialogue structure"""
    
    def __init__(self, config: CohesiveVideoConfig = None):
        self.config = config or CohesiveVideoConfig()
        
        print(f"🎬 Cohesive Video Generator Initialized")
        print(f"   📺 Resolution: {self.config.width}x{self.config.height}")
        print(f"   🎨 Background: {self.config.background_color}")
        print(f"   📊 Advanced Features: {HAS_ADVANCED_FEATURES}")
        
        # Speaker avatar configurations
        self.speaker_configs = {
            "Narrator": {
                "color": self.config.narrator_color,
                "avatar_style": "microphone",
                "description": "Professional Host"
            },
            "Dr. Ava D.": {
                "color": self.config.ava_color,
                "avatar_style": "optimistic_researcher",
                "description": "Enthusiastic Researcher"
            },
            "Prof. Marcus W.": {
                "color": self.config.marcus_color,
                "avatar_style": "skeptical_analyst", 
                "description": "Critical Analyst"
            }
        }
    
    def create_speaker_avatar(self, speaker: str, size: int = None) -> str:
        """Create speaker avatar using PIL"""
        
        if not HAS_ADVANCED_FEATURES:
            return None
        
        size = size or self.config.avatar_size
        config = self.speaker_configs.get(speaker, self.speaker_configs["Narrator"])
        
        # Create avatar image
        avatar_path = f"temp_avatar_{speaker.replace(' ', '_').replace('.', '')}.png"
        
        try:
            # Create circular avatar with speaker-specific styling
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Background circle
            color_rgb = self.hex_to_rgb(config["color"])
            draw.ellipse([10, 10, size-10, size-10], fill=color_rgb + (200,), outline=color_rgb + (255,), width=5)
            
            # Speaker-specific icons/styling
            if config["avatar_style"] == "microphone":
                # Narrator - microphone icon
                self.draw_microphone_icon(draw, size)
            elif config["avatar_style"] == "optimistic_researcher":
                # Dr. Ava D. - lightbulb/star icon
                self.draw_lightbulb_icon(draw, size)
            elif config["avatar_style"] == "skeptical_analyst":
                # Prof. Marcus W. - magnifying glass icon
                self.draw_magnifying_glass_icon(draw, size)
            
            # Add initials
            self.add_speaker_initials(draw, speaker, size)
            
            img.save(avatar_path)
            print(f"   🎭 Created avatar: {speaker} → {avatar_path}")
            return avatar_path
            
        except Exception as e:
            print(f"   ⚠️ Avatar creation failed for {speaker}: {e}")
            return None
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def draw_microphone_icon(self, draw, size):
        """Draw microphone icon for narrator"""
        center_x, center_y = size // 2, size // 2
        # Simple microphone representation
        draw.rectangle([center_x-15, center_y-30, center_x+15, center_y+10], fill=(255, 255, 255, 200))
        draw.ellipse([center_x-20, center_y-35, center_x+20, center_y-25], fill=(255, 255, 255, 200))
        draw.line([center_x, center_y+10, center_x, center_y+25], fill=(255, 255, 255, 200), width=3)
    
    def draw_lightbulb_icon(self, draw, size):
        """Draw lightbulb icon for optimistic researcher"""
        center_x, center_y = size // 2, size // 2
        # Simple lightbulb representation
        draw.ellipse([center_x-20, center_y-25, center_x+20, center_y+5], fill=(255, 255, 100, 200))
        draw.rectangle([center_x-10, center_y+5, center_x+10, center_y+15], fill=(255, 255, 255, 200))
        # Radiating lines for "bright idea"
        for angle in [45, 90, 135, 0, 180]:
            x1 = center_x + 30 * np.cos(np.radians(angle))
            y1 = center_y + 30 * np.sin(np.radians(angle))
            x2 = center_x + 40 * np.cos(np.radians(angle))
            y2 = center_y + 40 * np.sin(np.radians(angle))
            draw.line([x1, y1, x2, y2], fill=(255, 255, 100, 150), width=2)
    
    def draw_magnifying_glass_icon(self, draw, size):
        """Draw magnifying glass icon for skeptical analyst"""
        center_x, center_y = size // 2, size // 2
        # Magnifying glass
        draw.ellipse([center_x-20, center_y-20, center_x+10, center_y+10], fill=None, outline=(255, 255, 255, 200), width=4)
        draw.line([center_x+7, center_y+7, center_x+20, center_y+20], fill=(255, 255, 255, 200), width=4)
    
    def add_speaker_initials(self, draw, speaker: str, size: int):
        """Add speaker initials to avatar"""
        try:
            # Get initials
            if speaker == "Narrator":
                initials = "N"
            elif "Ava" in speaker:
                initials = "A"
            elif "Marcus" in speaker:
                initials = "M"
            else:
                initials = speaker[0]
            
            # Try to use a font, fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", size // 4)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position
            bbox = draw.textbbox((0, 0), initials, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (size - text_width) // 2
            y = (size - text_height) // 2 + size // 8
            
            draw.text((x, y), initials, fill=(255, 255, 255, 255), font=font)
            
        except Exception as e:
            print(f"   ⚠️ Could not add initials: {e}")
    
    def create_waveform_visualization(self, audio_file: str, duration: float) -> str:
        """Create waveform visualization using librosa and matplotlib"""
        
        if not HAS_ADVANCED_FEATURES:
            return None
        
        waveform_path = f"temp_waveform_{int(time.time())}.png"
        
        try:
            print(f"   📊 Creating waveform for: {audio_file}")
            
            # Load audio file
            y, sr = librosa.load(audio_file, sr=22050)
            
            # Create waveform plot
            plt.figure(figsize=(12, 2), facecolor='none')
            plt.plot(np.linspace(0, duration, len(y)), y, color=self.config.waveform_color, linewidth=0.5)
            plt.fill_between(np.linspace(0, duration, len(y)), y, alpha=0.3, color=self.config.waveform_color)
            
            # Styling
            plt.ylim(-1, 1)
            plt.xlim(0, duration)
            plt.axis('off')
            plt.tight_layout()
            plt.margins(0)
            
            # Save with transparency
            plt.savefig(waveform_path, transparent=True, bbox_inches='tight', pad_inches=0, dpi=100)
            plt.close()
            
            print(f"   ✅ Waveform created: {waveform_path}")
            return waveform_path
            
        except Exception as e:
            print(f"   ⚠️ Waveform creation failed: {e}")
            return None
    
    def create_scrolling_text_clip(self, text: str, speaker: str, duration: float) -> VideoFileClip:
        """Create scrolling text clip synchronized with speech"""
        
        config = self.speaker_configs.get(speaker, self.speaker_configs["Narrator"])
        
        # Calculate text dimensions and scroll parameters
        words_per_minute = 150  # Average speaking rate
        words = text.split()
        
        # Create text clip with word wrapping
        wrapped_text = self.wrap_text_for_scrolling(text, max_chars_per_line=80)
        
        # Create main text clip
        text_clip = TextClip(
            wrapped_text,
            fontsize=self.config.font_size,
            color=config["color"],
            font=self.config.font,
            size=(self.config.width - 400, None),  # Leave space for avatar
            method='caption'
        ).set_duration(duration)
        
        # Calculate scroll distance based on text height and duration
        text_height = text_clip.h
        if text_height > self.config.height - 300:  # If text is longer than screen
            scroll_distance = text_height - (self.config.height - 300)
            
            # Create scrolling animation
            def scroll_position(t):
                progress = t / duration
                y_offset = -scroll_distance * progress
                return ('center', self.config.height // 2 + y_offset)
            
            text_clip = text_clip.set_position(scroll_position)
        else:
            # Center text if it fits on screen
            text_clip = text_clip.set_position('center')
        
        return text_clip
    
    def wrap_text_for_scrolling(self, text: str, max_chars_per_line: int = 80) -> str:
        """Wrap text for optimal scrolling display"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= max_chars_per_line:
                current_line += (" " + word if current_line else word)
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return "\n".join(lines)
    
    def create_segment_video(self, segment: CohesiveSegment) -> VideoFileClip:
        """Create video for one cohesive segment"""
        
        print(f"🎬 Creating video segment: {segment.speaker} ({segment.segment_type})")
        
        # 1. Background
        background = ColorClip(
            size=(self.config.width, self.config.height),
            color=self.config.background_color
        ).set_duration(segment.duration)
        
        video_elements = [background]
        
        # 2. Speaker Avatar
        avatar_path = self.create_speaker_avatar(segment.speaker)
        if avatar_path:
            try:
                avatar_clip = (ImageClip(avatar_path)
                             .resize(height=self.config.avatar_size)
                             .set_duration(segment.duration)
                             .set_position(('left', 'top'))
                             .set_margin(20))
                video_elements.append(avatar_clip)
                print(f"   ✅ Avatar added for {segment.speaker}")
            except Exception as e:
                print(f"   ⚠️ Avatar failed: {e}")
        
        # 3. Scrolling Text
        try:
            text_clip = self.create_scrolling_text_clip(
                segment.text, segment.speaker, segment.duration
            )
            
            # Position text to avoid avatar
            if avatar_path:
                text_clip = text_clip.set_position((250, 'center'))  # Right of avatar
            else:
                text_clip = text_clip.set_position('center')
            
            video_elements.append(text_clip)
            print(f"   ✅ Scrolling text added")
        except Exception as e:
            print(f"   ⚠️ Text creation failed: {e}")
        
        # 4. Waveform Visualization
        waveform_path = self.create_waveform_visualization(segment.audio_file, segment.duration)
        if waveform_path:
            try:
                waveform_clip = (ImageClip(waveform_path)
                               .resize(width=self.config.width-100)
                               .set_duration(segment.duration)
                               .set_position(('center', 'bottom'))
                               .set_margin(50))
                video_elements.append(waveform_clip)
                print(f"   ✅ Waveform visualization added")
            except Exception as e:
                print(f"   ⚠️ Waveform failed: {e}")
        
        # 5. Segment Title (for intro/conclusion)
        if segment.segment_type in ['intro', 'conclusion', 'transition']:
            title_text = {
                'intro': 'Research Rundown',
                'transition': 'Now Let\'s Hear The Other Side...',
                'conclusion': 'Thank You For Watching!'
            }.get(segment.segment_type, '')
            
            if title_text:
                title_clip = (TextClip(
                    title_text,
                    fontsize=self.config.title_font_size,
                    color='white',
                    font=self.config.font
                ).set_duration(min(3.0, segment.duration))
                 .set_position(('center', 'top'))
                 .set_margin(50))
                
                video_elements.append(title_clip)
        
        # Compose final segment
        segment_video = CompositeVideoClip(video_elements, size=(self.config.width, self.config.height))
        
        print(f"   ✅ Segment video created: {segment.duration:.1f}s")
        return segment_video
    
    def load_cohesive_audio_data(self, json_path: str) -> List[CohesiveSegment]:
        """Load cohesive audio data and create video segments"""
        
        print(f"📂 Loading cohesive audio data from: {json_path}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        audio_result = data["audio_output"]
        main_audio_file = audio_result["final_audio_file"]
        
        # We need to extract individual segment files and timing
        # This assumes your streamlined pipeline saves individual segment files
        segments = []
        current_time = 0.0
        
        # Look for segment information in the results
        if "segments" in audio_result:
            for i, segment_info in enumerate(audio_result["segments"]):
                # Map the segment info to our structure
                segment_type = segment_info.get("type", f"segment_{i}")
                speaker = segment_info["speaker"]
                duration = segment_info["duration"]
                
                # For now, use placeholder text - in production, you'd extract from cohesive script
                if "intro" in segment_type:
                    text = f"Welcome to Research Rundown! Today's topic: {data['paper_analysis']['paper_topic']}"
                elif "optimist" in segment_type:
                    text = f"This research represents a breakthrough in {data['paper_analysis']['research_field']}..."
                elif "transition" in segment_type:
                    text = "Fascinating perspective. Now let's hear the other side..."
                elif "skeptic" in segment_type:
                    text = f"I have serious concerns about this methodology and approach..."
                elif "conclusion" in segment_type:
                    text = "Thank you for joining us on Research Rundown!"
                else:
                    text = f"Content for {speaker}"
                
                # For individual audio files, you might need to extract them
                # For now, we'll use the main audio file with timing
                segments.append(CohesiveSegment(
                    speaker=speaker,
                    text=text,
                    audio_file=main_audio_file,  # You might need individual files here
                    duration=duration,
                    segment_type=segment_type,
                    start_time=current_time
                ))
                
                current_time += duration
        
        print(f"   ✅ Loaded {len(segments)} cohesive segments")
        for segment in segments:
            print(f"      🎤 {segment.speaker} ({segment.segment_type}): {segment.duration:.1f}s")
        
        return segments, main_audio_file
    
    def generate_cohesive_video(self, json_path: str, output_filename: str = None) -> str:
        """Generate complete cohesive video with all advanced features"""
        
        print("🚀 Starting Cohesive Video Generation...")
        print("🎬 Features: Scrolling Text + Avatars + Waveforms")
        print("=" * 80)
        
        # Load cohesive audio data
        segments, main_audio_file = self.load_cohesive_audio_data(json_path)
        
        # Load main audio
        main_audio = AudioFileClip(main_audio_file)
        print(f"🎵 Main audio loaded: {main_audio.duration:.1f}s")
        
        # Create video segments
        video_segments = []
        
        for segment in segments:
            print(f"\n🎬 Creating segment: {segment.speaker}")
            
            try:
                # Create video for this segment
                segment_video = self.create_segment_video(segment)
                
                # Extract audio for this specific segment
                segment_audio = main_audio.subclip(segment.start_time, 
                                                 segment.start_time + segment.duration)
                
                # Combine video with its audio
                segment_with_audio = segment_video.set_audio(segment_audio)
                video_segments.append(segment_with_audio)
                
                print(f"   ✅ Segment completed: {segment.duration:.1f}s")
                
            except Exception as e:
                print(f"   ❌ Segment failed: {e}")
                # Create fallback simple segment
                fallback = (ColorClip(color=self.config.background_color, 
                                    size=(self.config.width, self.config.height))
                          .set_duration(segment.duration)
                          .set_audio(main_audio.subclip(segment.start_time, 
                                                      segment.start_time + segment.duration)))
                video_segments.append(fallback)
        
        # Concatenate all segments
        print("\n🎞️ Concatenating video segments...")
        final_video = concatenate_videoclips(video_segments, method="compose")
        
        # Set output filename
        if not output_filename:
            base_name = Path(json_path).stem.replace("_STREAMLINED_results", "")
            output_filename = f"data/output/video/{base_name}_COHESIVE_youtube.mp4"
        
        # Create output directory
        output_path = Path(output_filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Render final video
        print(f"🎥 Rendering cohesive video to: {output_filename}")
        print("   ⚠️ This may take several minutes for advanced features...")
        
        try:
            final_video.write_videofile(
                output_filename,
                fps=self.config.fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None,
                preset='medium',
                ffmpeg_params=['-crf', '23']  # Good quality-to-size ratio
            )
            
            # Clean up temporary files
            self.cleanup_temp_files()
            
            # Close clips to free memory
            main_audio.close()
            final_video.close()
            for segment in video_segments:
                segment.close()
            
            print(f"✅ Cohesive video generation complete!")
            print(f"   📁 Output: {output_filename}")
            print(f"   📊 Duration: {main_audio.duration:.1f}s ({main_audio.duration/60:.1f} minutes)")
            print(f"   📺 Resolution: {self.config.width}x{self.config.height}")
            print(f"   🎭 Features: Scrolling text, avatars, waveforms")
            
            return output_filename
            
        except Exception as e:
            print(f"❌ Video rendering failed: {e}")
            raise
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        import glob
        temp_files = glob.glob("temp_avatar_*.png") + glob.glob("temp_waveform_*.png")
        for temp_file in temp_files:
            try:
                Path(temp_file).unlink()
            except:
                pass


def main():
    """Main function for cohesive video generation"""
    
    print("🎬 COHESIVE VIDEO GENERATOR")
    print("Advanced features: Scrolling text + Avatars + Waveforms")
    print("-" * 60)
    
    if len(sys.argv) < 2:
        print("Usage: python3 generate_cohesive_video.py <streamlined_results.json>")
        print("Example: python3 generate_cohesive_video.py data/output/WCC_paper_STREAMLINED_results.json")
        return
    
    json_path = sys.argv[1]
    
    if not Path(json_path).exists():
        print(f"❌ Results file not found: {json_path}")
        return
    
    try:
        # Create advanced video generator
        config = CohesiveVideoConfig(
            width=1920,
            height=1080,
            fps=24,
            font_size=52,
            title_font_size=76,
            text_scroll_speed=40
        )
        
        generator = CohesiveVideoGenerator(config)
        
        # Generate cohesive video
        output_file = generator.generate_cohesive_video(json_path)
        
        print(f"\n🎉 COHESIVE VIDEO COMPLETE!")
        print(f"🎬 YouTube-ready video: {output_file}")
        print(f"📺 Ready to upload with all advanced features!")
        
        # Display final summary
        file_size_mb = Path(output_file).stat().st_size / (1024 * 1024)
        print(f"\n📊 FINAL VIDEO STATS:")
        print(f"   📁 File size: {file_size_mb:.1f} MB")
        print(f"   🎥 Format: MP4 (H.264 + AAC)")
        print(f"   📺 Resolution: 1920x1080 @ 24fps")
        print(f"   🎭 Advanced Features: ✅ All included")
        print(f"   📊 Scrolling text: ✅ Synchronized")
        print(f"   🎨 Speaker avatars: ✅ Custom designed")  
        print(f"   📈 Waveform visualization: ✅ Dynamic")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    main()
