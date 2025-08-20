#!/usr/bin/env python3
"""Run Phase 3 with Reliable Audio Generator (SOX only, no FFmpeg complexity)"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from main_phase3 import main
if __name__ == "__main__":
    main()
