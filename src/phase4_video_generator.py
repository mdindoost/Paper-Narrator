"""Phase 4 Video Generator - PIL-based Text (No ImageMagick Required)"""

import json
import time
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
import numpy as np

try:
    from moviepy.editor import (
        AudioFileClip, ImageClip, CompositeVideoClip,
        ColorClip, concatenate_videoclips
    )
    from PIL import Image, ImageDraw, ImageFont
    HAS_MOVIEPY = True
    HAS_PIL = True
except ImportError as e:
    print(f"Import error: {e}")
    HAS_MOVIEPY = False
    HAS_PIL = False

from config import OUTPUT_DIR


@dataclass
class VideoSegment:
    """Represents one video segment with timing"""
    speaker: str
    duration: float
    start_time: float
    end_time: float
    segment_type: str
    speaker_color: str


class YouTubeVideoGenerator:
    """Generate YouTube-ready videos with speaker identification (PIL-based)"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir) if output_dir else OUTPUT_DIR / "video"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Video settings
        self.width = 1920
        self.height = 1080
        self.fps = 24
        
        # Color scheme (RGB tuples for PIL)
        self.colors = {
            "background": (26, 26, 46),     # Dark blue academic
            "narrator": (255, 215, 0),      # Gold for narrator
            "dr_ava": (74, 222, 128),       # Green for optimistic Dr. Ava
            "prof_marcus": (248, 113, 113), # Red for skeptical Prof. Marcus
            "text": (255, 255, 255)         # White text
        }
        
        print("🎬 YouTube Video Generator Initialized (PIL-based)")
        print(f"📏 Resolution: {self.width}x{self.height} @ {self.fps}fps")
    
    def check_requirements(self) -> bool:
        """Check if moviepy and PIL are available"""
        return HAS_MOVIEPY and HAS_PIL
    
    def get_speaker_color(self, speaker: str) -> Tuple[int, int, int]:
        """Get RGB color for speaker"""
        speaker_lower = speaker.lower()
        
        if "narrator" in speaker_lower:
            return self.colors["narrator"]
        elif "ava" in speaker_lower or "sarah" in speaker_lower:
            return self.colors["dr_ava"]
        elif "marcus" in speaker_lower or "webb" in speaker_lower:
            return self.colors["prof_marcus"]
        else:
            return self.colors["text"]
    
    def clean_speaker_name(self, speaker: str) -> str:
        """Clean and format speaker name for display"""
        if "narrator" in speaker.lower():
            return "NARRATOR"
        elif "ava" in speaker.lower() or "sarah" in speaker.lower():
            return "DR. AVA D."
        elif "marcus" in speaker.lower() or "webb" in speaker.lower():
            return "PROF. MARCUS WEBB"
        else:
            return speaker.upper()
    
    def create_text_image(self, text: str, font_size: int, color: Tuple[int, int, int], 
                         width: int, height: int, y_position: int = None) -> Image.Image:
        """Create text image using PIL"""
        
        # Create image
        img = Image.new('RGB', (width, height), self.colors["background"])
        draw = ImageDraw.Draw(img)
        
        # Try to load a font, fallback to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center text
        x = (width - text_width) // 2
        if y_position is None:
            y = (height - text_height) // 2
        else:
            y = y_position
        
        # Draw text
        draw.text((x, y), text, font=font, fill=color)
        
        return img
    
    def create_speaker_video_segment(self, speaker: str, duration: float, segment_type: str):
        """Create video segment for one speaker using PIL"""
        
        # Clean speaker name and get color
        display_name = self.clean_speaker_name(speaker)
        speaker_color = self.get_speaker_color(speaker)
        
        # Create background image
        background_img = Image.new('RGB', (self.width, self.height), self.colors["background"])
        draw = ImageDraw.Draw(background_img)
        
        # Add speaker name (large, centered)
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        except:
            font_large = ImageFont.load_default()
        
        # Get text size and center it
        bbox = draw.textbbox((0, 0), display_name, font=font_large)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2
        
        draw.text((x, y), display_name, font=font_large, fill=speaker_color)
        
        # Add segment type indicator (smaller, bottom)
        type_indicator = ""
        if segment_type == "intro":
            type_indicator = "INTRODUCTION"
        elif segment_type == "conclusion":
            type_indicator = "CONCLUSION"
        else:
            type_indicator = "DISCUSSION"
        
        try:
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        except:
            font_small = ImageFont.load_default()
        
        # Add type indicator at bottom
        bbox_small = draw.textbbox((0, 0), type_indicator, font=font_small)
        text_width_small = bbox_small[2] - bbox_small[0]
        x_small = (self.width - text_width_small) // 2
        y_small = self.height - 150
        
        draw.text((x_small, y_small), type_indicator, font=font_small, fill=self.colors["text"])
        
        # Convert PIL image to numpy array for MoviePy
        img_array = np.array(background_img)
        
        # Create ImageClip
        image_clip = ImageClip(img_array, duration=duration)
        
        return image_clip
    
    def parse_audio_metadata(self, metadata_file: str) -> List[VideoSegment]:
        """Parse Phase 3 audio metadata for video timing"""
        
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        segments = []
        current_time = 0.0
        
        for segment_data in metadata.get("segments", []):
            speaker = segment_data["speaker"]
            duration = segment_data["duration"]
            segment_type = segment_data.get("type", "conversation")
            
            video_segment = VideoSegment(
                speaker=speaker,
                duration=duration,
                start_time=current_time,
                end_time=current_time + duration,
                segment_type=segment_type,
                speaker_color=self.get_speaker_color(speaker)
            )
            
            segments.append(video_segment)
            current_time += duration
        
        return segments
    
    def create_title_sequence(self, paper_title: str, duration: float = 5.0):
        """Create opening title sequence using PIL"""
        
        # Create title image
        img = Image.new('RGB', (self.width, self.height), self.colors["background"])
        draw = ImageDraw.Draw(img)
        
        # Try to load fonts
        try:
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 96)
            font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        except:
            font_title = font_subtitle = font_small = ImageFont.load_default()
        
        # Main title
        main_title = "RESEARCH RUNDOWN"
        bbox = draw.textbbox((0, 0), main_title, font=font_title)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, 200), main_title, font=font_title, fill=self.colors["narrator"])
        
        # Paper title (truncated if too long)
        display_title = paper_title[:60] + "..." if len(paper_title) > 60 else paper_title
        bbox = draw.textbbox((0, 0), display_title, font=font_subtitle)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, 400), display_title, font=font_subtitle, fill=self.colors["text"])
        
        # Subtitle
        subtitle = "AI Researchers Debate the Latest Research"
        bbox = draw.textbbox((0, 0), subtitle, font=font_small)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, 600), subtitle, font=font_small, fill=self.colors["text"])
        
        # Convert to MoviePy
        img_array = np.array(img)
        title_clip = ImageClip(img_array, duration=duration)
        
        return title_clip
    
    def create_end_sequence(self, duration: float = 3.0):
        """Create ending sequence using PIL"""
        
        # Create end image
        img = Image.new('RGB', (self.width, self.height), self.colors["background"])
        draw = ImageDraw.Draw(img)
        
        # Try to load fonts
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        except:
            font_large = font_medium = ImageFont.load_default()
        
        # Thank you message
        thanks_text = "THANKS FOR WATCHING"
        bbox = draw.textbbox((0, 0), thanks_text, font=font_large)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, 400), thanks_text, font=font_large, fill=self.colors["narrator"])
        
        # Subscribe message
        subscribe_text = "Subscribe for More Research Rundowns"
        bbox = draw.textbbox((0, 0), subscribe_text, font=font_medium)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, 600), subscribe_text, font=font_medium, fill=self.colors["text"])
        
        # Convert to MoviePy
        img_array = np.array(img)
        end_clip = ImageClip(img_array, duration=duration)
        
        return end_clip
    
    def generate_complete_video(self, audio_file: str, metadata_file: str, 
                              paper_title: str, base_filename: str) -> Dict:
        """Generate complete YouTube video using PIL (no ImageMagick)"""
        
        print("🎬 Generating YouTube video with PIL-based text...")
        
        if not self.check_requirements():
            raise Exception("moviepy or PIL not available")
        
        # Load audio
        print("🎵 Loading audio...")
        audio_clip = AudioFileClip(audio_file)
        total_duration = audio_clip.duration
        
        print(f"📊 Audio duration: {total_duration:.1f}s ({total_duration/60:.1f} min)")
        
        # Parse metadata for video segments
        print("📋 Parsing audio metadata...")
        video_segments = self.parse_audio_metadata(metadata_file)
        print(f"🎭 Found {len(video_segments)} video segments")
        
        # Create video clips for each segment
        print("🎬 Creating video segments with PIL...")
        video_clips = []
        
        for i, segment in enumerate(video_segments):
            print(f"   📝 Segment {i+1}: {segment.speaker} ({segment.duration:.1f}s)")
            
            video_clip = self.create_speaker_video_segment(
                segment.speaker,
                segment.duration,
                segment.segment_type
            )
            
            video_clips.append(video_clip)
        
        # Concatenate all video segments
        print("🎞️ Concatenating video segments...")
        main_video = concatenate_videoclips(video_clips, method="compose")
        
        # Add title sequence
        print("🎬 Adding PIL-based title sequence...")
        title_seq = self.create_title_sequence(paper_title, duration=3.0)
        
        # Add end sequence
        print("🏁 Adding PIL-based end sequence...")
        end_seq = self.create_end_sequence(duration=2.0)
        
        # Combine everything
        print("🎥 Assembling final video...")
        final_video = concatenate_videoclips([
            title_seq,
            main_video,
            end_seq
        ], method="compose")
        
        # Set audio
        final_video = final_video.set_audio(audio_clip)
        
        # Export video
        output_file = self.output_dir / f"{base_filename}_YOUTUBE_final.mp4"
        print(f"💾 Exporting video to: {output_file}")
        
        # Export with YouTube-optimized settings
        final_video.write_videofile(
            str(output_file),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            preset='medium',
            ffmpeg_params=['-crf', '23']
        )
        
        # Generate result metadata
        result = {
            "video_file": str(output_file),
            "video_duration": final_video.duration,
            "audio_duration": total_duration,
            "resolution": f"{self.width}x{self.height}",
            "fps": self.fps,
            "num_segments": len(video_segments),
            "segments": [
                {
                    "speaker": seg.speaker,
                    "duration": seg.duration,
                    "start_time": seg.start_time,
                    "end_time": seg.end_time,
                    "type": seg.segment_type
                }
                for seg in video_segments
            ],
            "file_size_mb": output_file.stat().st_size / (1024 * 1024) if output_file.exists() else 0
        }
        
        # Save video metadata
        video_metadata_file = self.output_dir / f"{base_filename}_video_metadata.json"
        with open(video_metadata_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        result["metadata_file"] = str(video_metadata_file)
        
        print(f"✅ YouTube video complete!")
        print(f"   🎥 Video: {output_file}")
        print(f"   📊 Duration: {final_video.duration:.1f}s ({final_video.duration/60:.1f} min)")
        print(f"   💾 Size: {result['file_size_mb']:.1f} MB")
        print(f"   📋 Metadata: {video_metadata_file}")
        
        return result
