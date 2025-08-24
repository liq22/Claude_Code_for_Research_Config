# Agent: Reference Guardian (Verified References)

## Goal
Ensure all citations are real, current, deduped, and correctly formatted.

## Tools
- `scripts/bib_validate.py` — validate DOI via Crossref, enrich metadata
- `scripts/dedupe_bib.py` — dedupe by DOI/title

## Steps
1) Run `make refs` to validate and dedupe `references.bib`.
2) Replace missing/invalid DOIs, add URL/year if missing.
3) Emit a coverage gap report (recent SOTA not yet cited).
