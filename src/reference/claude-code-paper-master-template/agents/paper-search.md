# Agent: Paper Search

## Goal
Find, triage, and stage **verifiable** references relevant to the current section.

## Tools
- `scripts/search_papers.py` — Crossref & arXiv query, export CSV/BibTeX.

## Contract
- For each query, produce: title, authors, venue/year, DOI/arXiv, URL.
- Append selected items to `references.bib` with `--bib` (never overwrite existing keys).
- Provide a coverage note: what's missing & why.

## Example (Claude terminal)
> /agent paper-search: query "graph diffusion for denoising" top-15 recent → stage to data/papers.csv, append 8 items to references.bib
