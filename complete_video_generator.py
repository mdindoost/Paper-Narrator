#!/usr/bin/env python3
"""
COMPLETE AI PAPER NARRATOR VIDEO GENERATION PACKAGE
Save as: complete_video_generator.py

CURRENT STATUS:
✅ Audio pipeline FULLY WORKING with cohesive 5-segment structure
✅ All 10 bugs fixed (symbols, names, prefixes, voices, etc.)
✅ Professional dialogue: Intro → Ava Case → Transition → Marcus Case → Conclusion
✅ Three distinct voices: Narrator (AriaNeural), Dr. Ava D. (JennyNeural), Prof. Marcus W. (ChristopherNeural)

CURRENT AUDIO OUTPUT LOCATION:
data/output/audio/[PAPER_NAME]_COHESIVE_youtube.wav

THIS FILE CREATES YOUTUBE-READY VIDEOS FROM YOUR EXISTING AUDIO
"""

import sys
import json
import time
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any

# Video generation imports
try:
    import moviepy.editor as mp
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    HAS_VIDEO_DEPS = True
except ImportError as e:
    print(f"❌ Missing video dependencies: {e}")
    print("Install with: pip install moviepy pillow numpy")
    HAS_VIDEO_DEPS = False

# Audio analysis imports  
try:
    import librosa
    import matplotlib.pyplot as plt
    HAS_AUDIO_ANALYSIS = True
except ImportError:
    print("⚠️ Audio analysis not available - install with: pip install librosa matplotlib")
    HAS_AUDIO_ANALYSIS = False


@dataclass
class VideoSegment:
    """Video segment with timing information"""
    speaker: str
    start_time: float
    duration: float
    segment_type: str
    text_preview: str = ""


class AIPaperNarratorVideoGenerator:
    """Complete video generator for AI Paper Narrator project"""
    
    def __init__(self):
        self.width = 1920
        self.height = 1080 
        self.fps = 24
        
        # Speaker colors (based on your current setup)
        self.speaker_colors = {
            'Narrator': '#ffd93d',        # Yellow
            'Dr. Ava D.': '#00d4aa',      # Teal (optimistic)
            'Prof. Marcus W.': '#ff6b6b'  # Red (skeptical)
        }
        
        # Segment type styling
        self.segment_styles = {
            'intro': {'bg': '#1a1a2e', 'accent': '#ffd93d'},
            'optimist_case': {'bg': '#0d4d3d', 'accent': '#00d4aa'},
            'transition': {'bg': '#2a2a2e', 'accent': '#ffd93d'},
            'skeptic_case': {'bg': '#4d1a1a', 'accent': '#ff6b6b'},
            'conclusion': {'bg': '#1a1a2e', 'accent': '#ffd93d'}
        }
    
    def check_dependencies(self) -> bool:
        """Check if all required dependencies are available"""
        if not HAS_VIDEO_DEPS:
            return False
        return True
    
    def analyze_existing_audio(self, audio_file: str) -> List[VideoSegment]:
        """Analyze your existing cohesive audio file to create segments"""
        
        print(f"🎵 Analyzing existing audio: {audio_file}")
        
        if not Path(audio_file).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        # Load audio to get duration
        audio_clip = mp.AudioFileClip(audio_file)
        total_duration = audio_clip.duration
        print(f"   📊 Total duration: {total_duration:.1f}s ({total_duration/60:.1f} minutes)")
        
        # Based on your current cohesive structure, estimate segments
        # This is the typical structure from your working pipeline
        estimated_segments = [
            VideoSegment("Narrator", 0, 15, "intro", "Welcome to Research Rundown..."),
            VideoSegment("Dr. Ava D.", 15, total_duration * 0.4, "optimist_case", "This research shows incredible potential..."),
            VideoSegment("Narrator", 15 + total_duration * 0.4, 8, "transition", "Fascinating perspective from Dr. Ava D..."),
            VideoSegment("Prof. Marcus W.", 15 + total_duration * 0.4 + 8, total_duration * 0.4, "skeptic_case", "I have serious concerns about this methodology..."),
            VideoSegment("Narrator", total_duration - 20, 20, "conclusion", "And there you have it - a fascinating debate...")
        ]
        
        # Adjust durations to match actual total
        actual_content_duration = total_duration - 43  # Total minus intro, transition, conclusion
        
        # Recalculate with proper timing
        segments = [
            VideoSegment("Narrator", 0, 15, "intro", "Welcome to Research Rundown..."),
            VideoSegment("Dr. Ava D.", 15, actual_content_duration * 0.5, "optimist_case", "This research demonstrates breakthrough potential..."),
            VideoSegment("Narrator", 15 + actual_content_duration * 0.5, 8, "transition", "Fascinating perspective from Dr. Ava D. Now let's hear Prof. Marcus W's analysis..."),
            VideoSegment("Prof. Marcus W.", 15 + actual_content_duration * 0.5 + 8, actual_content_duration * 0.5, "skeptic_case", "Hold on, I have serious concerns about this analysis..."),
            VideoSegment("Narrator", total_duration - 20, 20, "conclusion", "Thanks for joining us on Research Rundown...")
        ]
        
        print(f"   🎬 Created {len(segments)} video segments:")
        for i, seg in enumerate(segments, 1):
            print(f"      {i}. {seg.speaker} ({seg.segment_type}): {seg.start_time:.1f}s - {seg.start_time + seg.duration:.1f}s ({seg.duration:.1f}s)")
        
        audio_clip.close()
        return segments
    
    def create_speaker_background(self, speaker: str, segment_type: str, duration: float) -> mp.VideoClip:
        """Create background visual for speaker segment"""
        
        # Get colors for this segment
        style = self.segment_styles.get(segment_type, self.segment_styles['intro'])
        speaker_color = self.speaker_colors.get(speaker, '#ffffff')
        
        # Create background image
        img = Image.new('RGB', (self.width, self.height), color=style['bg'])
        draw = ImageDraw.Draw(img)
        
        # Add speaker name
        try:
            # Try to load a decent font
            font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 84)
            font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 48)
        except:
            # Fallback to default
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Main speaker name
        speaker_text = speaker
        bbox = draw.textbbox((0, 0), speaker_text, font=font_large)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2 - 50
        
        draw.text((x, y), speaker_text, fill=speaker_color, font=font_large)
        
        # Add segment type subtitle
        if segment_type != 'transition':
            subtitle_text = {
                'intro': 'Research Rundown Host',
                'optimist_case': 'The Optimistic Analysis',
                'skeptic_case': 'The Critical Analysis', 
                'conclusion': 'Research Rundown Host'
            }.get(segment_type, segment_type.title())
            
            bbox_sub = draw.textbbox((0, 0), subtitle_text, font=font_small)
            sub_width = bbox_sub[2] - bbox_sub[0]
            sub_x = (self.width - sub_width) // 2
            sub_y = y + text_height + 20
            
            draw.text((sub_x, sub_y), subtitle_text, fill=style['accent'], font=font_small)
        
        # Add decorative elements
        if segment_type in ['optimist_case', 'skeptic_case']:
            # Add accent line
            line_y = self.height - 100
            draw.rectangle([200, line_y, self.width - 200, line_y + 8], fill=style['accent'])
        
        # Save temporary image
        temp_image = f"temp_{speaker.replace(' ', '_').replace('.', '')}_{segment_type}.png"
        img.save(temp_image)
        
        # Create video clip
        clip = mp.ImageClip(temp_image, duration=duration)
        
        # Add subtle zoom effect for longer segments
        if duration > 60:  # Long segments (Ava and Marcus cases)
            clip = clip.resize(lambda t: 1 + 0.01 * t/duration)  # Subtle zoom
        
        # Clean up temp file
        Path(temp_image).unlink()
        
        return clip
    
    def create_title_screen(self, paper_info: Dict[str, str]) -> mp.VideoClip:
        """Create opening title screen with paper information"""
        
        # Create title background
        img = Image.new('RGB', (self.width, self.height), color='#0a0a1e')
        draw = ImageDraw.Draw(img)
        
        try:
            font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 96)
            font_subtitle = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 54)
            font_paper = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 36)
        except:
            font_title = font_subtitle = font_paper = ImageFont.load_default()
        
        # Main title
        title = "Research Rundown"
        bbox = draw.textbbox((0, 0), title, font=font_title)
        title_width = bbox[2] - bbox[0]
        title_x = (self.width - title_width) // 2
        title_y = 300
        
        draw.text((title_x, title_y), title, fill='#ffd93d', font=font_title)
        
        # Paper topic
        paper_topic = paper_info.get('paper_topic', 'Academic Research Analysis')
        if len(paper_topic) > 60:
            paper_topic = paper_topic[:60] + "..."
        
        bbox_paper = draw.textbbox((0, 0), paper_topic, font=font_subtitle)
        paper_width = bbox_paper[2] - bbox_paper[0]
        paper_x = (self.width - paper_width) // 2
        paper_y = title_y + 120
        
        draw.text((paper_x, paper_y), paper_topic, fill='#00d4aa', font=font_subtitle)
        
        # Debate subtitle
        debate_text = "Dr. Ava D. vs Prof. Marcus W."
        bbox_debate = draw.textbbox((0, 0), debate_text, font=font_paper)
        debate_width = bbox_debate[2] - bbox_debate[0]
        debate_x = (self.width - debate_width) // 2
        debate_y = paper_y + 80
        
        draw.text((debate_x, debate_y), debate_text, fill='#ff6b6b', font=font_paper)
        
        # Save and create clip
        temp_image = "temp_title.png"
        img.save(temp_image)
        
        clip = mp.ImageClip(temp_image, duration=3).crossfadein(0.5).crossfadeout(0.5)
        
        Path(temp_image).unlink()
        return clip
    
    def generate_youtube_video(self, audio_file: str, paper_info: Dict[str, str] = None, output_file: str = None) -> str:
        """Generate complete YouTube-ready video from your existing audio"""
        
        if not self.check_dependencies():
            raise RuntimeError("Missing required dependencies for video generation")
        
        print(f"🎬 GENERATING YOUTUBE VIDEO")
        print(f"📁 Audio source: {audio_file}")
        print("=" * 80)
        
        # Analyze audio to get segments
        segments = self.analyze_existing_audio(audio_file)
        
        # Load audio
        audio_clip = mp.AudioFileClip(audio_file)
        total_duration = audio_clip.duration
        
        print(f"🎥 Creating video segments...")
        
        # Create video segments
        video_clips = []
        
        # Optional: Add title screen
        if paper_info:
            title_screen = self.create_title_screen(paper_info)
            video_clips.append(title_screen)
            # Adjust audio to account for title screen
            audio_clip = audio_clip.set_start(3)
        
        # Create main content segments
        for i, segment in enumerate(segments, 1):
            print(f"   🎨 Segment {i}: {segment.speaker} ({segment.segment_type}) - {segment.duration:.1f}s")
            
            # Create visual for this segment
            visual_clip = self.create_speaker_background(
                segment.speaker, 
                segment.segment_type, 
                segment.duration
            )
            
            # Position in timeline
            start_time = segment.start_time
            if paper_info:  # Account for title screen
                start_time += 3
                
            visual_clip = visual_clip.set_start(start_time)
            video_clips.append(visual_clip)
        
        print(f"🎼 Combining {len(video_clips)} video elements...")
        
        # Combine all video clips
        final_video = mp.CompositeVideoClip(video_clips)
        
        # Add audio
        final_video = final_video.set_audio(audio_clip)
        
        # Set final duration
        final_video = final_video.set_duration(audio_clip.duration + (3 if paper_info else 0))
        
        # Output file
        if not output_file:
            audio_path = Path(audio_file)
            output_file = audio_path.parent.parent / "video" / f"{audio_path.stem}_YOUTUBE.mp4"
            output_file.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"🎥 Rendering final video...")
        print(f"📊 Resolution: {self.width}x{self.height} @ {self.fps}fps")
        print(f"📁 Output: {output_file}")
        print("⏳ This may take several minutes...")
        
        # Render video
        final_video.write_videofile(
            str(output_file),
            fps=self.fps,
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
        
        # Get final stats
        final_size = Path(output_file).stat().st_size / (1024 * 1024)  # MB
        
        print(f"\n🎉 VIDEO GENERATION COMPLETE!")
        print(f"=" * 60)
        print(f"📁 Video File: {output_file}")
        print(f"📊 File Size: {final_size:.1f} MB")
        print(f"⏱️ Duration: {(audio_clip.duration + (3 if paper_info else 0))/60:.1f} minutes")
        print(f"🎥 Format: MP4 (H.264 + AAC)")
        print(f"📺 Resolution: {self.width}x{self.height}")
        print(f"✅ Ready for YouTube upload!")
        
        return str(output_file)


def find_latest_audio_file() -> str:
    """Find the latest generated cohesive audio file"""
    
    audio_dir = Path("data/output/audio")
    
    if not audio_dir.exists():
        raise FileNotFoundError("No audio output directory found")
    
    # Look for cohesive audio files
    cohesive_files = list(audio_dir.glob("*_COHESIVE_youtube.wav"))
    
    if not cohesive_files:
        # Fall back to any wav files
        cohesive_files = list(audio_dir.glob("*.wav"))
    
    if not cohesive_files:
        raise FileNotFoundError("No audio files found in data/output/audio/")
    
    # Get the most recent
    latest_file = max(cohesive_files, key=lambda x: x.stat().st_mtime)
    
    print(f"🎵 Found audio file: {latest_file}")
    return str(latest_file)


def extract_paper_info(audio_file: str) -> Dict[str, str]:
    """Extract paper information from filename and results"""
    
    audio_path = Path(audio_file)
    paper_name = audio_path.stem.replace("_COHESIVE_youtube", "").replace("_", " ")
    
    # Look for corresponding results JSON
    results_dir = Path("data/output")
    possible_results = [
        results_dir / f"{audio_path.stem.replace('_COHESIVE_youtube', '')}_STREAMLINED_results.json",
        results_dir / f"{audio_path.stem.replace('_COHESIVE_youtube', '')}_COHESIVE_pipeline.json",
        results_dir / f"{audio_path.stem.replace('_COHESIVE_youtube', '')}_pipeline.json"
    ]
    
    paper_info = {
        'paper_topic': paper_name,
        'research_field': 'Academic Research',
        'key_finding': 'Research findings and analysis'
    }
    
    # Try to load from results file
    for results_file in possible_results:
        if results_file.exists():
            try:
                with open(results_file, 'r') as f:
                    results = json.load(f)
                
                # Extract paper info from results
                if 'cohesive_analysis' in results:
                    analysis = results['cohesive_analysis']
                    paper_info.update({
                        'paper_topic': analysis.get('paper_topic', paper_info['paper_topic']),
                        'research_field': analysis.get('research_field', paper_info['research_field']),
                        'key_finding': analysis.get('key_finding', paper_info['key_finding'])
                    })
                    break
                elif 'paper_analysis' in results:
                    analysis = results['paper_analysis']
                    paper_info.update({
                        'paper_topic': analysis.get('paper_topic', paper_info['paper_topic']),
                        'research_field': analysis.get('research_field', paper_info['research_field']),
                        'key_finding': analysis.get('key_finding', paper_info['key_finding'])
                    })
                    break
            except:
                continue
    
    print(f"📄 Paper Info:")
    print(f"   📋 Topic: {paper_info['paper_topic']}")
    print(f"   🎯 Field: {paper_info['research_field']}")
    print(f"   💡 Finding: {paper_info['key_finding'][:60]}...")
    
    return paper_info


def main():
    """Main video generation function"""
    
    print("🎬 AI PAPER NARRATOR - VIDEO GENERATION")
    print("YouTube-Ready Video Creator")
    print("=" * 80)
    
    try:
        # Check for audio file
        if len(sys.argv) > 1:
            audio_file = sys.argv[1]
        else:
            audio_file = find_latest_audio_file()
        
        if not Path(audio_file).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        # Extract paper information
        paper_info = extract_paper_info(audio_file)
        
        # Generate video
        generator = AIPaperNarratorVideoGenerator()
        
        output_video = generator.generate_youtube_video(
            audio_file=audio_file,
            paper_info=paper_info
        )
        
        print(f"\n🚀 SUCCESS! YouTube video ready:")
        print(f"📁 {output_video}")
        print(f"\n📋 NEXT STEPS:")
        print(f"1. Review the video file")
        print(f"2. Upload to YouTube") 
        print(f"3. Add description and tags")
        print(f"4. Your AI Paper Narrator is ready for the world!")
        
    except Exception as e:
        print(f"❌ Video generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    main()
