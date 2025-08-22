# Claude Code Paper Master (Template)

A minimal, **Claude Code–ready** repository to write research papers with an agent team.

## Quick Start

### Prereqs
- Node.js >= 18
- Claude Code CLI installed (e.g., `npm i -g @anthropic-ai/claude-code` or official installer)
- Python 3.9+ (for helper scripts)

```bash
# 1) open terminal in repo root
claude

# 2) plan the week
> /plan create a 1-week plan to complete Intro+Method+one main figure and table

# 3) draft intro
> /agent professor1: draft intro based on templates/section-intro.md and our contributions in Paper.md

# 4) search papers (Crossref + arXiv), export bib
make search q="diffusion model for inverse problems" n=10

# 5) validate and dedupe references
make refs

# 6) make a demo figure from data/demo.csv
make plots

# 7) unify equations and cross-references
> /agent equation: normalize symbols and numbering; then /xref

# 8) run Nature-style review, fix P0 issues, then commit
> /agent nature-reviewer: full review; output P0 actions
```

## Structure

- `Paper.md` – the single source of truth (SoT)
- `CLAUDE.md` – routing rules, slash-commands, quality gates
- `agents/` – prompts for each role (supervisor, professor1/2/3, paper-search, plotor, equation, tabler, experiment-summary, nature-reviewer, reference)
- `templates/` – reusable section/figure/table/equation templates
- `scripts/` – helper Python scripts for plots, paper search, and reference validation
- `data/` – datasets (only small CSVs should be checked in)
- `references.bib` – the shared BibTeX library
- `Makefile` – convenient targets

## Notes
- The **paper-search agent** calls `scripts/search_papers.py` (Crossref and arXiv). Results can be saved to `data/papers.csv` and appended to `references.bib` with `--bib`.
- The **reference-guardian** validates DOIs, fills missing metadata, and dedupes. See `scripts/bib_validate.py` and `scripts/dedupe_bib.py`.
