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
