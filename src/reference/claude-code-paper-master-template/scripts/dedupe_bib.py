"""
dedupe_bib.py — Remove duplicate BibTeX entries by DOI or normalized title.

Usage:
  python scripts/dedupe_bib.py --in references.bib --out references.bib
"""
import argparse, re, pathlib, hashlib

def parse_entries(text):
    blocks = []
    cur = []
    for line in text.splitlines():
        if line.strip().startswith("@"):
            if cur:
                blocks.append("\n".join(cur))
            cur = [line]
        elif cur:
            cur.append(line)
    if cur:
        blocks.append("\n".join(cur))
    return blocks

def get_field(block, field):
    m = re.search(rf"\\b{field}\\s*=\\s*{{([^}}]+)}}", block, flags=re.I)
    return (m.group(1).strip() if m else "")

def norm_title(t):
    return re.sub(r"[^a-z0-9]+","", t.lower())

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="references.bib")
    ap.add_argument("--out", dest="out", default="references.bib")
    args = ap.parse_args()

    text = pathlib.Path(args.inp).read_text(encoding="utf-8", errors="ignore")
    entries = parse_entries(text)
    seen = set()
    out = []
    for e in entries:
        doi = get_field(e, "doi")
        title = get_field(e, "title")
        key = doi.lower() or norm_title(title)
        if key and key not in seen:
            seen.add(key)
            out.append(e)
    pathlib.Path(args.out).write_text("\n\n".join(out) + "\n", encoding="utf-8")
    print(f"[dedupe] {len(entries)} → {len(out)} entries")
