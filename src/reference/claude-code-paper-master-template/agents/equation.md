# Agent: Equation

## Goal
Unified symbols and robust cross-referencing.

## Rules
- Use `templates/equation-template.tex` with `\label{eq:<slug>}`.
- Introduce symbols once with a notation table in Method.
- Keep derivations with clear equivalence/assumption statements.

## Steps
1) Scan `$...$` and `equation` envs in `Paper.md`.
2) Normalize labels; insert a "Notation Table" early in Method.
3) Run `/xref` to refresh references.
