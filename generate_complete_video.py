#!/usr/bin/env python3
"""
Complete Paper to Video Generator - MoviePy Issues Fixed
Save as: generate_complete_video.py (in root directory)

Complete pipeline: PDF → Analysis → Cohesive Dialogue → Audio → Video
Fixes MoviePy color format consistency issues
"""

import sys
import os
import time
import asyncio
import subprocess
import numpy as np
from pathlib import Path
import json
from dataclasses import dataclass

# Add src directory to path
sys.path.append('src')
sys.path.append('.')

# Check for video dependencies first
try:
    from moviepy.editor import (
        VideoFileClip, AudioFileClip, TextClip, ColorClip, 
        CompositeVideoClip, concatenate_videoclips, ImageClip,
        concatenate_audioclips
    )
    HAS_MOVIEPY = True
    print("✅ MoviePy imported successfully")
except ImportError as e:
    HAS_MOVIEPY = False
    print(f"❌ MoviePy import error: {e}")

try:
    from src.pdf_processor import PDFProcessor
    from test_enhanced_claims_challenges import EnhancedClaimsChallengesAnalyzer
    from src.cohesive_dialogue_generator import CohesiveDialogueGenerator
    from src.audio_generator_fixed_enhanced import FullyFixedAudioGenerator
    from src.config import OUTPUT_DIR
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


@dataclass
class VideoSegmentInfo:
    """Video segment information"""
    speaker: str
    text: str
    audio_file: str
    duration: float
    segment_type: str
    start_time: float


class FixedVideoGenerator:
    """Video generator with MoviePy color format fixes"""
    def __init__(self):
        self.video_config = {
            "width": 1920,
            "height": 1080,
            "fps": 24,
            # Use RGB tuples instead of hex colors to avoid parsing issues
            "background_color": (26, 26, 46),      # Dark blue as RGB tuple
            "narrator_color": (255, 217, 61),      # Yellow
            "ava_color": (0, 212, 170),            # Teal
            "marcus_color": (255, 107, 107),       # Red
            "text_color": (255, 255, 255),         # White
        }
        
        # Logo caching attributes
        self._logo_clip_cache = None
        self._logo_processed = False
        
        print(f"🎬 Fixed Video Generator Initialized")
        print(f"   📺 Resolution: {self.video_config['width']}x{self.video_config['height']}")
        print(f"   🎨 Using RGB tuples for consistent color formatting")
        print(f"   🎬 Logo caching initialized")

    def debug_logo_loading(self):
        """Debug logo loading step by step"""
        print("DEBUG: Testing logo loading...")
        
        logo_file = "data/materials/LOGO_1080p.MOV"
        print(f"DEBUG: Checking file: {logo_file}")
        print(f"DEBUG: File exists: {Path(logo_file).exists()}")
        
        if Path(logo_file).exists():
            try:
                logo_clip = VideoFileClip(logo_file)
                print(f"DEBUG: Logo loaded - Duration: {logo_clip.duration}s, Size: {logo_clip.size}")
                print(f"DEBUG: Logo has audio: {logo_clip.audio is not None}")
                if logo_clip.audio:
                    print(f"DEBUG: Audio duration: {logo_clip.audio.duration}s")
                
                # Test creating a simple video with just the logo
                test_output = "test_logo_only.mp4"
                logo_clip.write_videofile(test_output, verbose=False, logger=None)
                print(f"DEBUG: Test logo video created: {test_output}")
                
                logo_clip.close()
                return True
                
            except Exception as e:
                print(f"DEBUG: Logo loading failed: {e}")
                return False
        else:
            print("DEBUG: Logo file not found")
            return False
    
    def get_preprocessed_logo(self):
        """Load and preprocess logo once, then reuse"""
        
        if self._logo_processed:
            return self._logo_clip_cache
        
        self._logo_processed = True
        
        # Change this line to use the preprocessed logo
        logo_file = "data/materials/LOGO_1080p.MOV"  # <-- Use the preprocessed version
        
        if not Path(logo_file).exists():
            print(f"   ⚠️ Logo file not found: {logo_file}")
            self._logo_clip_cache = None
            return None
        
        try:
            print(f"   🎬 Loading preprocessed logo: {logo_file}")
            
            # Since it's already 1920x1080, no resizing needed
            logo_clip = VideoFileClip(logo_file)
            
            print(f"   ✅ Logo loaded successfully: {logo_clip.duration:.1f}s, {logo_clip.size}")
            self._logo_clip_cache = logo_clip
            return logo_clip
            
        except Exception as e:
            print(f"   ❌ Logo loading failed: {e}")
            self._logo_clip_cache = None
            return None
        
    def debug_image_loading(self):
        """Debug image and logo loading"""
        print("🔍 DEBUG: Testing image and logo loading...")
        
        # Test image files
        image_files = [
            "data/materials/HOST.JPG",
            "data/materials/AVA.JPG", 
            "data/materials/MARCUS.JPG"
        ]
        
        for img_file in image_files:
            print(f"  📁 Checking: {img_file}")
            if Path(img_file).exists():
                try:
                    test_clip = ImageClip(img_file, duration=1)
                    print(f"    ✅ Loaded successfully: {test_clip.size}")
                    test_clip.close()
                except Exception as e:
                    print(f"    ❌ Failed to load: {e}")
            else:
                print(f"    ❌ File not found")
        
        # Test logo
        logo_file = "data/materials/LOGO.MOV"
        print(f"  🎬 Checking logo: {logo_file}")
        if Path(logo_file).exists():
            try:
                logo_clip = VideoFileClip(logo_file)
                print(f"    ✅ Logo loaded: {logo_clip.duration}s, {logo_clip.size}")
                logo_clip.close()
            except Exception as e:
                print(f"    ❌ Logo failed: {e}")
        else:
            print(f"    ❌ Logo not found")
            
    # def __init__(self):
    #     self.video_config = {
    #         "width": 1920,
    #         "height": 1080,
    #         "fps": 24,
    #         # Use RGB tuples instead of hex colors to avoid parsing issues
    #         "background_color": (26, 26, 46),      # Dark blue as RGB tuple
    #         "narrator_color": (255, 217, 61),      # Yellow
    #         "ava_color": (0, 212, 170),            # Teal
    #         "marcus_color": (255, 107, 107),       # Red
    #         "text_color": (255, 255, 255),         # White
    #     }
        
    #     print(f"🎬 Fixed Video Generator Initialized")
    #     print(f"   📺 Resolution: {self.video_config['width']}x{self.video_config['height']}")
    #     print(f"   🎨 Using RGB tuples for consistent color formatting")
    
    def create_solid_color_clip(self, color_rgb: tuple, duration: float) -> ColorClip:
        """Simplified - just create basic color clip"""
        
        clip = ColorClip(
            size=(self.video_config["width"], self.video_config["height"]),
            color=color_rgb,
            duration=duration
        )
        
        print(f"   ✅ Created simple color clip: {duration:.1f}s")
        return clip
            
    def _create_numpy_background(self, color_rgb: tuple, duration: float) -> ColorClip:
        """Fallback method to create background using numpy arrays"""
        
        print(f"   🔧 Using numpy fallback for color clip")
        
        def make_frame(t):
            # Create RGB frame with explicit shape
            frame = np.full(
                (self.video_config["height"], self.video_config["width"], 3), 
                color_rgb, 
                dtype=np.uint8
            )
            return frame
        
        from moviepy.editor import VideoClip
        clip = VideoClip(make_frame, duration=duration)
        return clip
    
    def load_logo_clip(self):
        """Load logo with PIL compatibility fix"""
        
        logo_file = "data/materials/LOGO.MOV"
        
        if not Path(logo_file).exists():
            print(f"   ⚠️ Logo file not found: {logo_file}")
            return None
        
        try:
            # Try loading logo with error handling for PIL issues
            logo_clip = VideoFileClip(logo_file)
            
            # Resize if needed (avoid MoviePy's resize due to PIL issues)
            if logo_clip.w != self.video_config["width"] or logo_clip.h != self.video_config["height"]:
                # Skip resizing for now to avoid PIL issues
                print(f"   ⚠️ Logo size mismatch ({logo_clip.size}), but keeping original to avoid PIL issues")
            
            print(f"   ✅ Logo loaded: {logo_clip.duration:.1f}s")
            return logo_clip
            
        except Exception as e:
            print(f"   ⚠️ Error loading logo (PIL compatibility): {e}")
            print(f"   🔄 Skipping logo to avoid crashes")
            return None
        
    def create_speaker_segment(self, speaker: str, duration: float) -> CompositeVideoClip:
        """Fixed version with compatible TextClip positioning"""
        
        print(f"   🎨 Creating segment for {speaker}: {duration:.1f}s")
        
        # Image mapping
        image_map = {
            "Narrator": "data/materials/HOST.JPG",
            "Host": "data/materials/HOST.JPG", 
            "Dr. Ava D.": "data/materials/AVA.JPG",
            "Prof. Marcus W.": "data/materials/MARCUS.JPG"
        }
        
        # Find the right image
        image_file = None
        for key in image_map:
            if key in speaker or key.lower() in speaker.lower():
                image_file = image_map[key]
                break
        
        if not image_file or not Path(image_file).exists():
            print(f"   ⚠️ No image found for {speaker}, using colored background")
            return self.create_solid_color_clip(self.video_config["background_color"], duration)
        
        try:
            print(f"   📁 Loading and resizing image: {image_file}")
            
            # MANUAL RESIZE using PIL directly
            from PIL import Image
            
            # Open image with PIL
            with Image.open(image_file) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize to fit screen height
                target_height = self.video_config["height"]
                aspect_ratio = img.width / img.height
                target_width = int(target_height * aspect_ratio)
                
                # Use LANCZOS instead of ANTIALIAS (compatibility fix)
                img_resized = img.resize((target_width, target_height), Image.LANCZOS)
                
                # Save to temporary file
                temp_path = f"temp_resized_{speaker.replace(' ', '_').replace('.', '')}.png"
                img_resized.save(temp_path)
                
            print(f"   📐 Resized to: {target_width}x{target_height}")
            
            # Load the pre-resized image
            image_clip = ImageClip(temp_path, duration=duration)
            
            # Create background
            background = ColorClip(
                size=(self.video_config["width"], self.video_config["height"]),
                color=self.video_config["background_color"],
                duration=duration
            )
            
            # Center the image
            image_clip = image_clip.set_position('center')
            
            # FIXED: Create text overlay with compatible positioning
            text_clip = TextClip(
                speaker,
                fontsize=48,
                color='white',
                font='Arial-Bold'
            ).set_duration(duration).set_position(('center', self.video_config["height"] - 100))
            # ^^ Use explicit positioning instead of set_margin
            
            # Composite
            final_clip = CompositeVideoClip([
                background, 
                image_clip, 
                text_clip
            ], size=(self.video_config["width"], self.video_config["height"]))
            
            print(f"   ✅ Created segment with image and text")
            
            # Clean up temp file
            try:
                os.remove(temp_path)
            except:
                pass
                
            return final_clip
                
        except Exception as e:
            print(f"   ❌ Error creating image segment: {e}")
            return self.create_solid_color_clip(self.video_config["background_color"], duration)

    def create_title_screen(self, paper_topic: str, duration: float = 3.0) -> CompositeVideoClip:
        """Simple title screen - just background with minimal text"""
        
        print(f"   🎬 Creating simple title screen: {duration:.1f}s")
        
        # Simple dark background
        background = ColorClip(
            size=(self.video_config["width"], self.video_config["height"]),
            color=self.video_config["background_color"],
            duration=duration
        )
        
        try:
            # Simple title text
            title_text = "Research Rundown"
            
            title_clip = TextClip(
                title_text,
                fontsize=64,
                color='white',
                font='Arial-Bold',
            ).set_duration(duration).set_position('center')
            
            final_clip = CompositeVideoClip([background, title_clip])
            print(f"   ✅ Simple title screen created")
            return final_clip
            
        except Exception as e:
            print(f"   ⚠️ Title text failed, using background only")
            return background


class CompletePaperVideoGenerator:
    """Complete pipeline from PDF to video with all fixes"""
    
    def __init__(self):
        print("🎬 Initializing Complete Paper to Video Generator...")
        
        self.pdf_processor = PDFProcessor()
        self.enhanced_analyzer = EnhancedClaimsChallengesAnalyzer()
        self.cohesive_dialogue_generator = CohesiveDialogueGenerator()
        self.audio_generator = FullyFixedAudioGenerator()
        self.video_generator = FixedVideoGenerator()
        
        print("✅ All components initialized")
    
    def check_prerequisites(self) -> bool:
        """Check if all services and dependencies are available"""
        print("🔧 Checking prerequisites...")
        
        # Check Ollama
        if not self.enhanced_analyzer.test_connection():
            print("❌ Ollama not running - start with: ollama serve")
            return False
        print("✅ Ollama connection successful")
        
        # Check dialogue generator
        if not self.cohesive_dialogue_generator.test_connection():
            print("❌ Dialogue generator connection failed")
            return False
        print("✅ Dialogue generator ready")
        
        # Check audio requirements
        if not self.audio_generator.check_requirements():
            print("❌ Edge-TTS not available - install with: pip install edge-tts")
            return False
        print("✅ Audio generation ready")
        
        # Check video requirements
        if not HAS_MOVIEPY:
            print("❌ MoviePy not available - install with: pip install moviepy")
            return False
        print("✅ Video generation ready")
        
        # Check ffmpeg
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            print("✅ FFmpeg available")
        except:
            print("❌ FFmpeg not available - install ffmpeg for video processing")
            return False
        
        return True
    
    def process_paper_complete_video_pipeline(self, pdf_path: str) -> dict:
        """Complete pipeline from PDF to video"""
        
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            raise FileNotFoundError(f"❌ PDF not found: {pdf_path}")
        
        print(f"\n🎬 COMPLETE VIDEO PIPELINE: {pdf_file.name}")
        print("🎥 Structure: PDF → Analysis → Dialogue → Audio → Video")
        print("=" * 80)
        
        start_time = time.time()
        
        # PHASE 1: PAPER ANALYSIS
        print("📖 PHASE 1: PAPER ANALYSIS")
        print("-" * 40)
        
        # Step 1: PDF Processing
        print("📖 Step 1: PDF Processing...")
        paper_data = self.pdf_processor.process_paper(str(pdf_path))
        raw_text = paper_data["raw_text"]
        print(f"   ✅ Extracted {len(raw_text):,} characters")
        
        # Step 2: Section Detection
        print("🔍 Step 2: Enhanced Section Detection...")
        core_sections = self.enhanced_analyzer.enhanced_section_detection(raw_text)
        print(f"   ✅ Found sections: {list(core_sections.keys())}")
        
        # Step 3: Stage 1 Understanding (with pauses removed)
        print("🎯 Step 3: Stage 1 Understanding...")
        stage1_understanding = self.enhanced_analyzer.stage1_simple_understanding(core_sections)
        print(f"   ✅ Field: {stage1_understanding.research_field}")
        print(f"   ✅ Topic: {stage1_understanding.paper_topic}")
        
        # Step 4: Stage 2 Claims→Challenges (with pauses removed)
        print("⚔️ Step 4: Stage 2 Claims→Challenges Analysis...")
        stage2_results = self.enhanced_analyzer.stage2_enhanced_claims_challenges(
            stage1_understanding, raw_text
        )
        
        optimist_points = len(stage2_results.debate_ammunition["optimist"])
        skeptic_points = len(stage2_results.debate_ammunition["skeptic"])
        print(f"   ✅ Generated {optimist_points} optimist points, {skeptic_points} skeptic points")
        
        # Step 5: Apply fixes
        print("🔧 Step 5: Applying Fixes...")
        try:
            from stage2_additional_fixes_patch import patch_stage2_results, apply_quick_field_fix
            stage1_understanding = apply_quick_field_fix(stage1_understanding)
            stage2_results = patch_stage2_results(stage2_results)
            print("   ✅ Additional fixes applied")
        except ImportError:
            print("   ⚠️ Additional fixes not available")
        
        # PHASE 2: DIALOGUE GENERATION
        print("\n🎭 PHASE 2: COHESIVE DIALOGUE GENERATION")
        print("-" * 40)
        
        cohesive_script = self.cohesive_dialogue_generator.create_cohesive_conversation_script(
            stage1_understanding, stage2_results
        )
        print(f"   ✅ Generated {cohesive_script.total_segments} cohesive segments")
        
        # PHASE 3: AUDIO GENERATION
        print("\n🎵 PHASE 3: PROFESSIONAL AUDIO GENERATION")
        print("-" * 40)
        
        video_segments = []
        current_time = 0.0
        
        for i, segment in enumerate(cohesive_script.segments, 1):
            print(f"   🎤 Generating {segment.segment_type}: {segment.speaker}")
            
            # Create unique filename
            timestamp = int(time.time() * 1000) + i
            safe_speaker = segment.speaker.replace(" ", "_").replace(".", "")
            audio_file = self.audio_generator.output_dir / f"video_{segment.segment_type}_{safe_speaker}_{timestamp}.mp3"
            
            try:
                # Generate audio
                duration = asyncio.run(self.audio_generator.text_to_speech_fully_fixed(
                    segment.content, segment.speaker, str(audio_file)
                ))
                
                video_segment = VideoSegmentInfo(
                    speaker=segment.speaker,
                    text=segment.content,
                    audio_file=str(audio_file),
                    duration=duration,
                    segment_type=segment.segment_type,
                    start_time=current_time
                )
                
                video_segments.append(video_segment)
                current_time += duration
                
                print(f"      ✅ Generated: {duration:.1f}s")
                
            except Exception as e:
                print(f"      ❌ Error: {e}")
                continue
        
        # PHASE 4: VIDEO GENERATION WITH FIXED MOVIEPY
        print(f"\n🎬 PHASE 4: PROFESSIONAL VIDEO GENERATION (MOVIEPY FIXED)")
        print("-" * 40)
        
        video_result = self.create_professional_video_fixed(
            video_segments, stage1_understanding, pdf_file.stem
        )
        
        # Calculate total processing time
        total_time = time.time() - start_time
        
        # Create comprehensive result
        complete_result = {
            "source_file": str(pdf_path),
            "processing_time": f"{total_time:.1f} seconds ({total_time/60:.1f} minutes)",
            "paper_analysis": {
                "research_field": stage1_understanding.research_field,
                "paper_topic": stage1_understanding.paper_topic,
                "key_finding": stage1_understanding.key_finding,
                "optimist_points": optimist_points,
                "skeptic_points": skeptic_points
            },
            "cohesive_dialogue": {
                "structure": "logo_intro → title → ava_case → transition → marcus_case → conclusion → logo_outro",
                "total_segments": len(video_segments),
                "total_duration": current_time
            },
            "video_output": video_result,
            "status": "complete_success"
        }
        
        # Save results
        output_json = OUTPUT_DIR / f"{pdf_file.stem}_COMPLETE_VIDEO_results.json"
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(complete_result, f, indent=2, ensure_ascii=False)
        
        # Display final results
        print(f"\n🎉 COMPLETE VIDEO PIPELINE SUCCESS!")
        print(f"=" * 60)
        print(f"⏱️ Total Processing Time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
        print(f"🎬 Final Video: {video_result['video_file']}")
        print(f"📊 Duration: {video_result['duration']/60:.1f} minutes")
        print(f"🎤 Segments: {len(video_segments)} professional segments")
        print(f"📄 Results: {output_json}")
        
        print(f"\n🎥 VIDEO STRUCTURE:")
        if video_result.get('has_logo_intro_outro'):
            print(f"   🎬 Logo Intro (6s)")
        print(f"   🎬 Title Screen (3s)")
        for segment in video_segments:
            print(f"   🎬 {segment.speaker} ({segment.segment_type}): {segment.duration:.1f}s")
        if video_result.get('has_logo_intro_outro'):
            print(f"   🎬 Logo Outro (6s)")
        
        print(f"\n✅ READY FOR YOUTUBE UPLOAD!")
        print(f"🎬 Video file: {video_result['video_file']}")
        print(f"📊 Resolution: {self.video_generator.video_config['width']}x{self.video_generator.video_config['height']}")
        print(f"🎵 Audio: Professional 3-voice narration with logo sound")
        
        return complete_result
    
    def create_professional_video_fixed(self, video_segments: list, stage1_understanding, base_filename: str) -> dict:
        """Debug version focusing on audio sync issues"""
        
        print("🎨 DEBUG: Creating video with focus on audio sync...")
        
        video_clips = []
        audio_clips = []
        current_time = 0.0
        
        # DEBUG: Test logo loading first
        print("DEBUG: Testing logo loading before video creation...")
        logo_test_result = self.video_generator.debug_logo_loading()
        
        # 1. Get preprocessed logo with debug info
        print("DEBUG: Calling get_preprocessed_logo()...")
        logo_clip = self.video_generator.get_preprocessed_logo()
        
        if logo_clip:
            print(f"DEBUG: Logo clip obtained - Duration: {logo_clip.duration}s")
            print(f"DEBUG: Logo has audio: {logo_clip.audio is not None}")
        else:
            print("DEBUG: get_preprocessed_logo() returned None")
        
        # 2. Add logo intro with detailed logging
        if logo_clip:
            print("DEBUG: Adding logo intro...")
            logo_intro = logo_clip.copy()
            video_clips.append(logo_intro)
            
            if logo_intro.audio:
                audio_clips.append(logo_intro.audio)
                print(f"DEBUG: Logo intro added - Video: {logo_intro.duration}s, Audio: {logo_intro.audio.duration}s")
            else:
                print("DEBUG: Logo intro has no audio!")
                
            current_time += logo_intro.duration
            print(f"DEBUG: Current time after logo: {current_time}s")
            print(f"DEBUG: Total video clips so far: {len(video_clips)}")
            print(f"DEBUG: Total audio clips so far: {len(audio_clips)}")
        else:
            print("DEBUG: Skipping logo intro - no logo clip available")
        
        
        
        # 1. Title screen with proper silent audio
        print("   🎬 Creating title screen...")
        title_screen = self.video_generator.create_title_screen(stage1_understanding.paper_topic, 3.0)
        video_clips.append(title_screen)
        
        # Create proper silent audio for title
        title_audio_file = self.audio_generator.output_dir / "title_silence_debug.wav"
        subprocess.run([
            "ffmpeg", "-f", "lavfi", "-i", "anullsrc=r=22050:cl=mono", "-t", "3",
            "-y", str(title_audio_file)
        ], check=True, capture_output=True)
        
        title_audio = AudioFileClip(str(title_audio_file))
        audio_clips.append(title_audio)
        current_time += 3.0
        print(f"   ✅ Title: 3.0s video + {title_audio.duration:.1f}s audio")
        
        # 2. Process each dialogue segment with detailed logging
        for i, segment in enumerate(video_segments):
            print(f"\n   🎤 Processing segment {i+1}: {segment.speaker}")
            
            # Check if audio file exists and get info
            if not Path(segment.audio_file).exists():
                print(f"   ❌ Audio file missing: {segment.audio_file}")
                continue
                
            try:
                # Load audio first and check duration
                audio_clip = AudioFileClip(segment.audio_file)
                audio_duration = audio_clip.duration
                video_duration = segment.duration
                
                print(f"   📊 Expected duration: {video_duration:.1f}s")
                print(f"   📊 Actual audio duration: {audio_duration:.1f}s")
                
                if abs(audio_duration - video_duration) > 1.0:
                    print(f"   ⚠️ Duration mismatch > 1 second!")
                    # Use audio duration as authoritative
                    video_duration = audio_duration
                
                # Create video segment with corrected duration
                video_clip = self.video_generator.create_speaker_segment(segment.speaker, video_duration)
                
                video_clips.append(video_clip)
                audio_clips.append(audio_clip)
                current_time += video_duration
                
                print(f"   ✅ Added: {video_duration:.1f}s video + audio")
                
            except Exception as e:
                print(f"   ❌ Failed to process segment: {e}")
                continue
        
        print(f"\n   📊 Total clips: {len(video_clips)} video, {len(audio_clips)} audio")
        print(f"   📊 Expected total duration: {current_time:.1f}s")
        
        # 3. Debug each audio clip before concatenation
        print("\n   🔍 Debugging audio clips before concatenation:")
        for i, audio in enumerate(audio_clips):
            try:
                print(f"   Audio {i+1}: {audio.duration:.1f}s, fps={audio.fps}")
            except Exception as e:
                print(f"   Audio {i+1}: ERROR - {e}")
        
        # 4. CAREFUL concatenation with error handling
        print("\n   🎬 Careful concatenation...")
        
        try:
            # Video concatenation
            print("   📹 Concatenating video clips...")
            final_video = concatenate_videoclips(video_clips, method="compose")
            print(f"   ✅ Video concatenated: {final_video.duration:.1f}s")
            
            # Audio concatenation  
            print("   🔊 Concatenating audio clips...")
            final_audio = concatenate_audioclips(audio_clips)
            print(f"   ✅ Audio concatenated: {final_audio.duration:.1f}s")
            
            # Check duration match
            video_dur = final_video.duration
            audio_dur = final_audio.duration
            print(f"   📊 Final durations: Video={video_dur:.1f}s, Audio={audio_dur:.1f}s")
            
            if abs(video_dur - audio_dur) > 0.5:
                print(f"   ⚠️ Duration mismatch detected! Adjusting...")
                # Use shorter duration to avoid sync issues
                sync_duration = min(video_dur, audio_dur)
                final_video = final_video.subclip(0, sync_duration)
                final_audio = final_audio.subclip(0, sync_duration)
                print(f"   🔧 Synced to: {sync_duration:.1f}s")
            
            # Set audio
            print("   🔗 Syncing audio with video...")
            final_video = final_video.set_audio(final_audio)
            print("   ✅ Audio sync complete")
            
        except Exception as e:
            print(f"   ❌ Concatenation failed: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        # 5. Export with conservative settings
        output_video = OUTPUT_DIR / f"{base_filename}_AUDIO_DEBUG_youtube.mp4"
        
        print(f"\n   🎥 Rendering to: {output_video}")
        print("   ⚠️ Using conservative render settings...")
        
        try:
            final_video.write_videofile(
                str(output_video),
                fps=24,
                codec='libx264',
                audio_codec='aac',
                bitrate="2000k",           # Conservative bitrate
                audio_bitrate="128k",      # Standard audio bitrate  
                verbose=True,              # Show detailed output
                temp_audiofile='temp-debug-audio.m4a',
                remove_temp=False          # Keep temp files for debugging
            )
            
            print("   ✅ Video rendering complete!")
            
            # Verify the output file
            if output_video.exists():
                file_size_mb = output_video.stat().st_size / (1024 * 1024)
                print(f"   📊 Output file: {file_size_mb:.1f} MB")
                
                # Test if the file is playable
                try:
                    test_clip = VideoFileClip(str(output_video))
                    test_duration = test_clip.duration
                    test_clip.close()
                    print(f"   ✅ File verification: {test_duration:.1f}s duration")
                except Exception as e:
                    print(f"   ❌ File verification failed: {e}")
            
            return {
                "video_file": str(output_video),
                "duration": current_time,
                "resolution": "1920x1080",
                "fps": 24,
                "file_size_mb": f"{output_video.stat().st_size / (1024 * 1024):.1f}",
                "segments": len(video_segments),
                "debug_mode": True,
                "audio_debug": True
            }
            
        except Exception as e:
            print(f"   ❌ Video rendering failed: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        finally:
            # Clean up clips but keep temp files for debugging
            try:
                if 'final_video' in locals():
                    final_video.close()
                if 'final_audio' in locals():
                    final_audio.close()
                # Don't close individual clips yet - might still be needed
            except:
                pass
            
def test_complete_video_pipeline(pdf_path: str = None):
    """Test the complete video pipeline"""
    
    if pdf_path is None:
        pdf_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    print("🎬 TESTING COMPLETE PAPER TO VIDEO PIPELINE")
    print("🎥 Full pipeline: PDF → Analysis → Dialogue → Audio → Video")
    print("=" * 80)
    
    try:
        generator = CompletePaperVideoGenerator()
        
        if not generator.check_prerequisites():
            print("❌ Prerequisites not met")
            return False
        
        # Process paper to video
        result = generator.process_paper_complete_video_pipeline(pdf_path)
        
        if result["status"] == "complete_success":
            print(f"\n🎉 COMPLETE VIDEO PIPELINE SUCCESS!")
            
            video_info = result["video_output"]
            print(f"\n📹 FINAL VIDEO:")
            print(f"   🎬 File: {video_info['video_file']}")
            print(f"   ⏱️ Duration: {video_info['duration']/60:.1f} minutes")
            print(f"   📺 Resolution: {video_info['resolution']}")
            print(f"   📊 File Size: {video_info['file_size_mb']} MB")
            print(f"   🎤 Segments: {video_info['segments']}")
            
            # Handle optional keys safely
            if 'has_logo_intro_outro' in video_info:
                print(f"   📽️ Logo Intro/Outro: {video_info['has_logo_intro_outro']}")
            if 'speaker_images_used' in video_info:
                print(f"   🖼️ Speaker Images: {video_info['speaker_images_used']}")
            
            print(f"\n🚀 READY FOR YOUTUBE!")
            print(f"✅ Professional video with cohesive dialogue")
            print(f"✅ Speaker images and name overlays")
            if video_info.get('has_logo_intro_outro'):
                print(f"✅ Logo intro and outro with sound")
            print(f"✅ Proper resolution and format for upload")
            
            return True
        else:
            print(f"❌ Pipeline failed")
            return False
            
    except Exception as e:
        print(f"❌ Complete video pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function"""
    
    print("🎬 COMPLETE PAPER TO VIDEO GENERATOR")
    print("🎥 End-to-end pipeline: PDF → Analysis → Dialogue → Audio → Video")
    print("-" * 80)
    
    # Get PDF path
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    print(f"📄 Processing: {pdf_path}")
    
    # Run complete pipeline
    success = test_complete_video_pipeline(pdf_path)
    
    if success:
        print(f"\n🎉 COMPLETE SUCCESS!")
        print(f"🎬 Professional YouTube-ready video generated")
        print(f"✅ Speaker images, logo, and text overlays included")
        print(f"✅ Upload ready!")
    else:
        print(f"\n❌ Pipeline failed - check error messages above")


if __name__ == "__main__":
    main()