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
