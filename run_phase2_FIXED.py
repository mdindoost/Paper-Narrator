#!/usr/bin/env python3
"""Run FIXED Phase 2 that uses Phase 1 results"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from main_phase2_fixed import main
if __name__ == "__main__":
    main()
