"""Configuration settings for the AI Paper Narrator"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
TEST_PAPERS_DIR = PROJECT_ROOT / "data" / "input"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"

# Create directories if they don't exist
TEST_PAPERS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Ollama settings
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "llama3.1:8b"

# Processing settings
MAX_CHUNK_SIZE = 4000  # Characters per chunk
OVERLAP_SIZE = 200     # Overlap between chunks

# Personality settings
PERSONALITIES = {
    "optimist": {
        "name": "Dr. Sarah Chen",
        "role": "The Enthusiastic Researcher",
        "traits": "optimistic, explanatory, focuses on potential and applications"
    },
    "skeptic": {
        "name": "Prof. Marcus Webb", 
        "role": "The Critical Analyst",
        "traits": "skeptical, methodical, focuses on limitations and flaws"
    }
}
