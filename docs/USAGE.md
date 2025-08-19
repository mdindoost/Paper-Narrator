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
