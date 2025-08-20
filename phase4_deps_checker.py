#!/usr/bin/env python3
"""Phase 4 Dependencies Checker - Updated for Video Generation"""

import subprocess
import sys
import json
from pathlib import Path

def check_python_packages():
    """Check required Python packages"""
    print("🐍 Checking Python packages...")
    
    packages = {
        "moviepy": "Video editing and generation",
        "PIL": "Image processing",
        "numpy": "Numerical operations", 
        "edge_tts": "Text-to-speech for audio generation",
        "requests": "HTTP requests for Ollama API",
        "PyPDF2": "PDF text extraction"
    }
    
    missing_packages = []
    
    for package, description in packages.items():
        try:
            if package == "PIL":
                import PIL
                print(f"   ✅ {package}: {description} (Pillow)")
            elif package == "edge_tts":
                import edge_tts
                print(f"   ✅ {package}: {description}")
            elif package == "moviepy":
                import moviepy
                print(f"   ✅ {package}: {description}")
            elif package == "numpy":
                import numpy
                print(f"   ✅ {package}: {description}")
            elif package == "requests":
                import requests
                print(f"   ✅ {package}: {description}")
            elif package == "PyPDF2":
                import PyPDF2
                print(f"   ✅ {package}: {description}")
            else:
                __import__(package)
                print(f"   ✅ {package}: {description}")
        except ImportError:
            print(f"   ❌ {package}: {description}")
            missing_packages.append(package)
    
    # Check optional packages
    optional_packages = {
        "cv2": "OpenCV for video processing (optional)"
    }
    
    for package, description in optional_packages.items():
        try:
            __import__(package)
            print(f"   ✅ {package}: {description}")
        except ImportError:
            print(f"   ⚠️  {package}: {description} (optional)")
    
    return missing_packages

def check_system_tools():
    """Check required system tools"""
    print("\n🛠️  Checking system tools...")
    
    tools = {
        "ffmpeg": "Video encoding/decoding",
        "ollama": "Local LLM server (should be running)"
    }
    
    missing_tools = []
    
    for tool, description in tools.items():
        try:
            result = subprocess.run([tool, "--version"], 
                                 capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"   ✅ {tool}: {description}")
            else:
                print(f"   ❌ {tool}: {description}")
                missing_tools.append(tool)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"   ❌ {tool}: {description}")
            missing_tools.append(tool)
    
    # Check optional tools  
    optional_tools = {
        "sox": "Audio processing (used in Phase 3)"
    }
    
    for tool, description in optional_tools.items():
        try:
            result = subprocess.run([tool, "--version"], 
                                 capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"   ✅ {tool}: {description}")
            else:
                print(f"   ⚠️  {tool}: {description} (already used in Phase 3)")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"   ⚠️  {tool}: {description} (already used in Phase 3)")
    
    return missing_tools

def check_phase3_outputs():
    """Check if any Phase 3 outputs exist (generic for any paper)"""
    print("\\n📁 Checking Phase 3 output files...")
    
    audio_dir = Path("data/output/audio")
    results_dir = Path("data/output")
    
    # Find audio files
    audio_files = list(audio_dir.glob("*_RELIABLE_youtube.wav"))
    metadata_files = list(audio_dir.glob("*_reliable_metadata.json"))
    complete_files = list(results_dir.glob("*_COMPLETE_phase3.json"))
    
    print(f"   🎵 Audio files found: {len(audio_files)}")
    for audio_file in audio_files:
        file_size = audio_file.stat().st_size
        print(f"      ✅ {audio_file.name}: Audio file ({file_size:,} bytes)")
    
    print(f"   📋 Metadata files found: {len(metadata_files)}")
    for metadata_file in metadata_files:
        file_size = metadata_file.stat().st_size
        print(f"      ✅ {metadata_file.name}: Audio metadata ({file_size:,} bytes)")
    
    print(f"   📄 Complete results found: {len(complete_files)}")
    for complete_file in complete_files:
        file_size = complete_file.stat().st_size
        print(f"      ✅ {complete_file.name}: Phase 3 results ({file_size:,} bytes)")
    
    # Check if we have matching sets
    missing_components = []
    
    if not audio_files:
        missing_components.append("No audio files (*_RELIABLE_youtube.wav)")
    if not metadata_files:
        missing_components.append("No metadata files (*_reliable_metadata.json)")
    if not complete_files:
        missing_components.append("No complete results (*_COMPLETE_phase3.json)")
    
    # Try to find matching pairs
    if audio_files and metadata_files:
        matching_pairs = []
        for audio_file in audio_files:
            base_name = audio_file.name.replace("_RELIABLE_youtube.wav", "")
            metadata_name = f"{base_name}_reliable_metadata.json"
            if (audio_dir / metadata_name).exists():
                matching_pairs.append(base_name)
        
        if matching_pairs:
            print(f"   🎯 Complete audio+metadata pairs: {len(matching_pairs)}")
            for pair in matching_pairs:
                print(f"      📝 {pair}: Ready for video generation")
        else:
            missing_components.append("No matching audio+metadata pairs")
    
    return missing_components

def check_metadata_content():
    """Check Phase 3 metadata content (for any available paper)"""
    print("\\n📊 Phase 3 Metadata Preview:")
    
    audio_dir = Path("data/output/audio")
    metadata_files = list(audio_dir.glob("*_reliable_metadata.json"))
    
    if not metadata_files:
        print(f"   ❌ No metadata files found")
        return False
    
    # Use the most recent metadata file
    latest_metadata = max(metadata_files, key=lambda f: f.stat().st_mtime)
    
    print(f"   📁 Using: {latest_metadata.name}")
    
    try:
        with open(latest_metadata, 'r') as f:
            metadata = json.load(f)
        
        total_duration = metadata.get('total_duration', 0)
        num_segments = metadata.get('num_segments', 0)
        method = metadata.get('method', 'unknown')
        segments = metadata.get('segments', [])
        
        print(f"   🎵 Total duration: {total_duration} seconds")
        print(f"   🎭 Number of segments: {num_segments}")
        print(f"   🔧 Method: {method}")
        
        print(f"\\n   📝 Segment breakdown:")
        for i, segment in enumerate(segments[:5], 1):
            speaker = segment.get('speaker', 'Unknown')
            duration = segment.get('duration', 0)
            seg_type = segment.get('type', 'conversation')
            print(f"      {i}. {speaker} ({seg_type}): {duration}s")
        
        if len(segments) > 5:
            print(f"      ... and {len(segments) - 5} more segments")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Error reading metadata: {e}")
        return False

def check_ollama_connection():
    """Check if Ollama is running"""
    print("\n🤖 Checking Ollama connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [model['name'] for model in models]
            print(f"   ✅ Ollama running with {len(models)} models")
            
            if 'llama3.1:8b' in model_names:
                print(f"   ✅ llama3.1:8b model available")
            else:
                print(f"   ⚠️  llama3.1:8b model not found")
                print(f"      Available models: {', '.join(model_names[:3])}")
            
            return True
        else:
            print(f"   ❌ Ollama not responding (status {response.status_code})")
            return False
    except Exception as e:
        print(f"   ❌ Ollama connection failed: {e}")
        return False

def main():
    """Main dependency checker"""
    print("🎬 Phase 4 Dependencies Checker")
    print("=" * 50)
    
    # Check Python packages
    missing_packages = check_python_packages()
    
    # Check system tools
    missing_tools = check_system_tools()
    
    # Check Phase 3 outputs
    missing_files = check_phase3_outputs()
    
    # Check metadata content
    metadata_ok = check_metadata_content()
    
    # Check Ollama
    ollama_ok = check_ollama_connection()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 DEPENDENCY CHECK SUMMARY")
    print("=" * 50)
    
    if missing_packages:
        print("❌ Missing Python packages:")
        for package in missing_packages:
            print(f"   • {package}")
        print(f"\n📦 Install with:")
        print(f"   pip install {' '.join(missing_packages)}")
    
    if missing_tools:
        print("❌ Missing system tools:")
        for tool in missing_tools:
            print(f"   • {tool}")
        print(f"\n🔧 Installation Commands:")
        if "ffmpeg" in missing_tools:
            print(f"   🛠️  FFmpeg: apt install ffmpeg (Ubuntu) or brew install ffmpeg (Mac)")
        if "ollama" in missing_tools:
            print(f"   🤖 Ollama: curl -fsSL https://ollama.ai/install.sh | sh")
    
    if missing_files:
        print("❌ Missing Phase 3 output files:")
        for file in missing_files:
            print(f"   • {file}")
        print(f"\n🚀 Run Phase 3 first:")
        print(f"   python3 run_phase3_reliable.py path/to/paper.pdf")
    
    # Final verdict
    if not missing_packages and not missing_tools and not missing_files and metadata_ok and ollama_ok:
        print("✅ All dependencies satisfied!")
        print("🚀 Ready for Phase 4 video generation!")
        if metadata_ok:
            print("🎯 Video will be generated from Phase 3 audio")
    else:
        print("❌ Some dependencies missing - install them before proceeding")
        
        if missing_files:
            print("📋 Priority: Run Phase 3 first to generate audio")
        if missing_packages:
            print("📋 Priority: Install missing Python packages")

if __name__ == "__main__":
    main()
