# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose
This is a research configuration repository for using Claude Code to write academic papers. It contains templates, agent configurations, and reference materials for a multi-agent paper writing workflow.

## Key Architecture
- **Reference Templates**: Complete paper writing template located in `Reference/claude-code-paper-master-template/`
- **Multi-Agent System**: Specialized agents for different aspects of paper writing (professor1/2/3, plotor, equation, tabler, etc.)
- **Single Source of Truth**: `Paper.md` serves as the primary document that agents collaborate on
- **Quality Gates**: Built-in review system with Nature-level standards

## Development Commands

### Paper Search and Bibliography
```bash
# Search for papers using the Python script
python Reference/claude-code-paper-master-template/scripts/search_papers.py --q "your query" --n 10 --out data/papers.csv --bib references.bib

# Validate and dedupe references
python Reference/claude-code-paper-master-template/scripts/bib_validate.py
python Reference/claude-code-paper-master-template/scripts/dedupe_bib.py
```

### Plotting and Visualization
```bash
# Generate plots from data
python Reference/claude-code-paper-master-template/scripts/plot.py
```

### Agent System Usage
The repository includes a specialized agent architecture:
- `/agent supervisor`: Top-level narrative and prioritization
- `/agent professor1/2/3`: Writing specialists for different sections
- `/agent paper-search`: Literature search and bibliography management  
- `/agent plotor`: Figure creation and visualization
- `/agent equation`: Mathematical notation and equation management
- `/agent tabler`: Table creation and formatting
- `/agent nature-reviewer`: Final quality review with Nature-level standards
- `/agent reference-guardian`: Bibliography validation and maintenance

## File Structure Conventions
- `Paper.md`: Main paper document (single source of truth)
- `references.bib`: Centralized bibliography file
- `agents/`: Agent specification files for different roles
- `templates/`: Reusable section templates
- `scripts/`: Helper Python scripts for data processing
- `data/`: CSV files and extracted data
- `plots/`: Generated figures and visualizations

## Quality Standards
The system enforces Nature-level quality gates:
1. Narrative coherence (problem → method → results → impact)
2. Consistent mathematical notation and symbols
3. Proper figure formatting with units and confidence intervals
4. Valid cross-references (no dangling refs)
5. Verified citations (DOI/arXiv validation)
6. Statistical rigor and reproducibility

## Working with Templates
When starting a new paper project, copy the template structure from `Reference/claude-code-paper-master-template/` and adapt the agent configurations for your specific research domain. The system supports both English and Chinese language workflows.

## Dependencies
- Python 3.9+
- Node.js >= 18 (for Claude Code CLI)
- requests library for API calls
- Standard Python libraries (csv, json, pathlib, etc.)