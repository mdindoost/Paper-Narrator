#!/bin/bash
# github_setup.sh - Clean up project and prepare for GitHub

echo "🧹 Cleaning up AI Paper Narrator project for GitHub..."
echo "📁 Target repo: https://github.com/mdindoost/Paper-Narrator"

cd ~/ai_paper_narrator

# Step 1: Create .gitignore
echo "📝 Creating .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
.venv/

# IDE & Editors
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# Jupyter Notebooks
.ipynb_checkpoints/

# Environment Variables
.env
.env.local
.env.*.local

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Project Specific
# Generated outputs (too large for git)
data/output/
data/input/*.pdf
*.pdf

# Temporary files
temp/
tmp/
*.tmp

# Audio files (Phase 3)
*.mp3
*.wav
*.m4a

# Video files (Phase 4)  
*.mp4
*.avi
*.mov

# Model files (too large)
models/
*.model

# Backup files (cleanup artifacts)
*.backup
*_old.py
*_test.py
debug_*.py
fix_*.py
compare_*.py
upgrade_*.py

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
EOF

# Step 2: Clean up backup and intermediate files
echo "🗑️  Removing backup and intermediate files..."

# Remove backup files
find . -name "*.backup" -delete
find . -name "*_old.py" -delete
find . -name "debug_*.py" -delete
find . -name "fix_*.py" -delete
find . -name "compare_*.py" -delete
find . -name "upgrade_*.py" -delete
find . -name "test_*.py" -delete

# Remove intermediate run scripts (keep only the final ones)
rm -f run_enhanced.py
rm -f run_phase2.py 
rm -f quick_test.py
rm -f test_enhanced.py
rm -f test_fix.py

# Keep only the working files
echo "✅ Keeping only final working files..."

# Step 3: Organize final project structure
echo "📁 Organizing final project structure..."

# Create clean directory structure
mkdir -p docs
mkdir -p examples
mkdir -p tests

# Move test files to tests directory if they exist
[ -f test_phase1.py ] && mv test_phase1.py tests/
[ -f test_phase2.py ] && mv test_phase2.py tests/

# Step 4: Create comprehensive README.md
echo "📖 Creating README.md..."
cat > README.md << 'EOF'
# 🎙️ AI Paper Narrator

Transform research papers into engaging dialogues between AI personalities! 

## 🎯 What It Does

AI Paper Narrator takes any research paper (PDF) and creates a podcast-style conversation between two distinct AI personalities:

- **Dr. Sarah Chen** (The Optimistic Researcher) - Enthusiastic about breakthroughs and applications
- **Prof. Marcus Webb** (The Critical Analyst) - Methodically rigorous and skeptical

## 🚀 Features

✅ **Phase 1: Intelligent Analysis**
- Extracts text from research papers
- Identifies paper sections (abstract, methods, results, etc.)
- Generates comprehensive strengths and weaknesses 
- Creates paper-specific discussion topics

✅ **Phase 2: AI Personality Dialogues**
- Two distinct AI personalities with unique perspectives
- Paper-specific conversations (not generic research talk)
- Natural podcast-style flow with transitions
- Validates content is actually about the specific paper

🔄 **Phase 3: Audio Generation** (Coming Soon)
- Text-to-speech conversion with distinct voices
- Podcast-quality audio output

🔄 **Phase 4: Video Creation** (Coming Soon)
- Visual podcast format
- Animated personalities

## 🛠️ Technology Stack

- **PDF Processing**: PyPDF2 for text extraction
- **AI Engine**: Ollama (local LLM) with Llama 3.1
- **Language**: Python 3.8+
- **Personalities**: Custom prompt engineering
- **TTS**: Bark (free, high-quality)
- **Video**: MoviePy

## 📋 Requirements

- Python 3.8+
- 8GB+ RAM (for Ollama)
- 5GB+ disk space
- Ollama installed locally

## ⚡ Quick Start

### 1. Install Ollama
```bash
# Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Download from https://ollama.ai/download
```

### 2. Setup Project
```bash
git clone https://github.com/mdindoost/Paper-Narrator.git
cd Paper-Narrator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start Ollama & Download Model
```bash
# Start service (keep running)
ollama serve

# Download model (one-time, ~4.7GB)
ollama pull llama3.1:8b
```

### 4. Process Your First Paper
```bash
# Phase 1: Analysis only
python3 run_phase1.py your_paper.pdf

# Phase 2: Analysis + Dialogue
python3 run_phase2_FIXED.py your_paper.pdf
```

## 📖 Usage Examples

### Basic Usage
```bash
# Analyze paper and generate dialogue (2 topics, 2 exchanges each)
python3 run_phase2_FIXED.py research_paper.pdf 2 2

# Longer conversation (3 topics, 4 exchanges each)  
python3 run_phase2_FIXED.py research_paper.pdf 3 4
```

### Sample Output
```
🎙️ Research Rundown: Optimized Parallel Implementations of WCC Algorithms

😊 Dr. Sarah Chen: "I'm excited about these WCC and CM algorithms using Chapel's 
   tasking model! The 23% performance improvement on billion-edge graphs shows 
   real scalability potential..."

🤨 Prof. Marcus Webb: "Hold on, let's examine this more carefully. They only 
   tested on Bitcoin, OpenAlex, and CEN datasets - is that really sufficient 
   for such bold claims about community detection?"
```

## 📁 Project Structure

```
Paper-Narrator/
├── src/                           # Source code
│   ├── config.py                  # Configuration settings
│   ├── pdf_processor.py           # PDF text extraction
│   ├── summarizer_final_fixed_v2.py # Paper analysis with Ollama
│   ├── personalities.py           # AI personality definitions
│   ├── dialogue_generator_fixed.py # Conversation generation
│   └── main_phase2_fixed.py       # Main orchestrator
├── data/                          # Data directory
│   ├── input/                     # Input PDFs (gitignored)
│   └── output/                    # Analysis results (gitignored)
├── tests/                         # Test files
├── docs/                          # Documentation
├── examples/                      # Example outputs
├── run_phase1.py                  # Phase 1 runner
├── run_phase2_FIXED.py           # Phase 2 runner
└── requirements.txt               # Dependencies
```

## 🎯 How It Works

### Phase 1: Paper Analysis
1. **PDF Processing**: Extracts text and identifies sections
2. **AI Analysis**: Uses Ollama to generate:
   - Detailed summary (topic, findings, methods, significance)
   - 5-8 specific strengths 
   - 5-8 specific weaknesses
   - 5 paper-specific discussion topics

### Phase 2: Dialogue Generation  
1. **Personality System**: Two distinct AI researchers with unique traits
2. **Content Integration**: Uses Phase 1 analysis for paper-specific conversations
3. **Dialogue Flow**: Natural exchanges with transitions between topics
4. **Validation**: Ensures conversation mentions actual paper content

## 🎭 AI Personalities

### Dr. Sarah Chen - The Enthusiastic Researcher
- **Role**: Optimistic about research potential
- **Style**: Enthusiastic, explanatory, uses analogies
- **Focus**: Breakthrough possibilities, practical applications
- **Catchphrases**: "This could be game-changing!", "Think about the possibilities..."

### Prof. Marcus Webb - The Critical Analyst  
- **Role**: Methodologically rigorous skeptic
- **Style**: Analytical, precise, asks probing questions
- **Focus**: Limitations, methodology, scientific rigor
- **Catchphrases**: "Hold on, let's examine this more carefully...", "I have serious concerns about..."

## 🔧 Configuration

Edit `src/config.py` to customize:
- Ollama model settings
- Processing parameters  
- Personality traits
- Output directories

## 🧪 Testing

```bash
# Test Phase 1 (analysis only)
python3 tests/test_phase1.py

# Test complete system
python3 run_phase2_FIXED.py examples/sample_paper.pdf 2 2
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for local LLM hosting
- [Llama 3.1](https://ai.meta.com/llama/) for the base language model
- Research community for inspiring this project

## 🚀 Roadmap

- [x] Phase 1: PDF processing and analysis
- [x] Phase 2: AI personality dialogues  
- [ ] Phase 3: Text-to-speech audio generation
- [ ] Phase 4: Video creation with visual elements
- [ ] Web interface for easy access
- [ ] Support for multiple languages
- [ ] Custom personality creation

---

**Transform your research papers into engaging conversations!** 🎙️✨
EOF

# Step 5: Create requirements.txt (final clean version)
echo "📦 Creating clean requirements.txt..."
cat > requirements.txt << 'EOF'
# Core Dependencies
PyPDF2==3.0.1
requests==2.31.0
python-dotenv==1.0.0

# AI/ML Libraries
langchain==0.1.0
langchain-community==0.0.10

# Development & Testing
reportlab==4.0.4
tqdm==4.66.1
colorama==0.4.6

# Future Phases (commented out for now)
# bark==1.0.0           # Phase 3: TTS
# moviepy==1.0.3        # Phase 4: Video
# pydub==0.25.1         # Phase 3: Audio processing
EOF

# Step 6: Create LICENSE file
echo "⚖️  Creating LICENSE..."
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 AI Paper Narrator

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Step 7: Create examples directory with sample output
echo "📁 Creating examples..."
mkdir -p examples

cat > examples/sample_output.md << 'EOF'
# Sample Output: Complex Networks Paper

## Generated Dialogue

```
🎙️ Research Rundown: Optimized Parallel Implementations of WCC Algorithms

🎬 INTRODUCTION:
Welcome to Research Rundown! Today we're discussing groundbreaking work on 
Well-Connected Components and Connectivity Modifier algorithms implemented 
in Chapel programming language for massive network analysis.

😊 Dr. Sarah Chen: I'm thrilled about these optimized WCC and CM algorithms! 
The use of Chapel's tasking model to achieve strong scalability on billion-edge 
graphs is exactly the kind of innovation we need for modern network analysis.

🤨 Prof. Marcus Webb: While I appreciate the technical achievement, I have 
concerns about the evaluation scope. Testing on only Bitcoin, OpenAlex, and 
CEN datasets - can we really claim broad applicability for community detection?

😊 Dr. Sarah Chen: That's a fair point, but consider the scale! These are 
billion-edge networks that break existing methods. The Chapel implementation 
handles what others can't even process.

🤨 Prof. Marcus Webb: Scale is important, but diversity matters too. How do 
we know these algorithms work well on social networks or biological systems? 
The three datasets, while large, represent a narrow slice of network types.

🏁 CONCLUSION:
We've explored the fascinating world of optimized community detection algorithms, 
debating the merits of WCC and CM implementations in Chapel. While the scalability 
achievements are impressive, questions about generalizability remain open for 
future research.
```

## Analysis Metrics
- **Paper-specific terms**: 8 (WCC, CM, Chapel, community detection, etc.)
- **Generic terms**: 0  
- **Validation**: ✅ Paper-specific content
- **Duration**: ~4 minutes
- **Turns**: 6 speaking exchanges
EOF

# Step 8: Create docs directory
echo "📚 Creating documentation..."
mkdir -p docs

cat > docs/INSTALLATION.md << 'EOF'
# Installation Guide

## Prerequisites
- Python 3.8 or higher
- 8GB+ RAM (for Ollama model)
- 5GB+ free disk space

## Step-by-Step Installation

### 1. Install Ollama
```bash
# Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### 2. Clone Repository
```bash
git clone https://github.com/mdindoost/Paper-Narrator.git
cd Paper-Narrator
```

### 3. Setup Python Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Start Ollama and Download Model
```bash
# Terminal 1: Start Ollama service
ollama serve

# Terminal 2: Download model (one-time)
ollama pull llama3.1:8b
```

### 5. Test Installation
```bash
python3 tests/test_phase1.py
```

## Troubleshooting

### "Cannot connect to Ollama"
- Ensure `ollama serve` is running
- Check port 11434 is not blocked
- Verify model is downloaded: `ollama list`

### Memory Issues
- Close other applications
- Use smaller model: `ollama pull llama3.1:7b`
- Increase swap space

### PDF Processing Errors
- Ensure PDF is not password protected
- Check file permissions
- Try different PDF file
EOF

cat > docs/USAGE.md << 'EOF'
# Usage Guide

## Basic Commands

### Phase 1: Analysis Only
```bash
python3 run_phase1.py paper.pdf
```

### Phase 2: Analysis + Dialogue  
```bash
python3 run_phase2_FIXED.py paper.pdf
```

### Custom Parameters
```bash
# Short conversation (2 topics, 2 exchanges each)
python3 run_phase2_FIXED.py paper.pdf 2 2

# Long conversation (4 topics, 3 exchanges each)
python3 run_phase2_FIXED.py paper.pdf 4 3
```

## Output Files

Results are saved in `data/output/`:
- `paper_name_analysis.json` - Phase 1 analysis
- `paper_name_FIXED_phase2.json` - Complete results

## Customization

Edit `src/config.py` to modify:
- Personality traits
- Analysis depth
- Output formatting
- Model parameters

## Best Practices

1. **PDF Quality**: Use text-based PDFs (not scanned images)
2. **Paper Length**: Works best with 10-50 page papers
3. **Topics**: 2-3 topics for concise conversations, 4-5 for detailed
4. **Exchanges**: 2-3 exchanges per topic for natural flow
EOF

# Step 9: Clean up any remaining test/debug files
echo "🧹 Final cleanup..."
rm -f *.py.backup
rm -f test_connection.py
rm -f test_simple.py

# Step 10: Initialize git repository
echo "🔧 Initializing Git repository..."
git init

# Add all files
git add .

echo ""
echo "✅ Project cleaned and ready for GitHub!"
echo ""
echo "📁 Final Project Structure:"
tree -I 'venv|__pycache__|*.pyc|data' -L 3

echo ""
echo "🚀 Next steps:"
echo "1. Review the cleaned project structure"
echo "2. Commit and push to GitHub:"
echo "   git commit -m 'Initial commit - AI Paper Narrator Phase 1 & 2'"
echo "   git remote add origin https://github.com/mdindoost/Paper-Narrator.git" 
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "📖 The README.md explains everything for new users!"
EOF

chmod +x github_setup.sh
echo "Created github_setup.sh - run it to clean up and prepare for GitHub!"
