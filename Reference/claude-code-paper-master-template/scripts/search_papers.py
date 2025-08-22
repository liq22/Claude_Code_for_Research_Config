"""
search_papers.py — Query Crossref & arXiv, export CSV and optionally BibTeX.

Examples:
  python scripts/search_papers.py --q "graph diffusion denoising" --n 10 --out data/papers.csv --bib references.bib
"""
import argparse, csv, json, re, time, pathlib, html
from urllib.parse import urlencode
import requests

CR_API = "https://api.crossref.org/works"
ARXIV_API = "http://export.arxiv.org/api/query"

def crossref(q, rows=10):
    params = {"query": q, "rows": rows, "sort": "published", "order": "desc"}
    r = requests.get(CR_API, params=params, timeout=20)
    r.raise_for_status()
    items = r.json()["message"]["items"]
    out = []
    for it in items:
        title = (it.get("title") or [""])[0]
        authors = []
        for a in it.get("author", []) or []:
            name = " ".join([a.get("given",""), a.get("family","")]).strip()
            if name:
                authors.append(name)
        year = (it.get("issued", {}).get("date-parts") or [[None]])[0][0]
        doi = it.get("DOI")
        url = it.get("URL")
        venue = it.get("container-title", [""])[0]
        out.append({"source":"crossref","title":title,"authors":"; ".join(authors),"venue":venue,"year":year,"doi":doi,"arxiv_id":"","url":url})
    return out

def arxiv(q, rows=10):
    params = {"search_query": f"all:{q}", "start": 0, "max_results": rows, "sortBy": "submittedDate", "sortOrder":"descending"}
    r = requests.get(ARXIV_API, params=params, timeout=20)
    r.raise_for_status()
    # Poor man's Atom parser
    entries = r.text.split("<entry>")[1:]
    out = []
    for e in entries:
        def g(tag):
            try:
                return e.split(f"<{tag}>")[1].split(f"</{tag}>")[0]
            except Exception:
                return ""
        title = html.unescape(g("title")).strip().replace("\n"," ")
        authors = "; ".join([html.unescape(a.split("</name>")[0]) for a in e.split("<name>")[1:]])
        year = g("published")[:4]
        arxiv_id = g("id").split("/")[-1]
        url = f"https://arxiv.org/abs/{arxiv_id}"
        out.append({"source":"arxiv","title":title,"authors":authors,"venue":"arXiv","year":year,"doi":"","arxiv_id":arxiv_id,"url":url})
    return out

def to_bib_entries(rows):
    bibs = []
    for r in rows:
        key = None
        if r.get("doi"):
            key = r["doi"].split("/")[-1].replace(".","_").replace("-","_")
        else:
            # arXiv key fallback
            key = r.get("arxiv_id","").replace(".","_").replace("-","_") or re.sub(r"[^A-Za-z0-9]+","", (r["title"][:40]))
        if r["source"]=="crossref":
            bibs.append(f"@article{{{key},\n  title={{ {r['title']} }},\n  author={{ {r['authors']} }},\n  journal={{ {r['venue']} }},\n  year={{ {r['year']} }},\n  doi={{ {r['doi']} }},\n  url={{ {r['url']} }}\n}}\n")
        else:
            bibs.append(f"@article{{{key},\n  title={{ {r['title']} }},\n  author={{ {r['authors']} }},\n  journal={{ arXiv preprint }},\n  year={{ {r['year']} }},\n  eprint={{ {r['arxiv_id']} }},\n  archivePrefix={{ arXiv }},\n  url={{ {r['url']} }}\n}}\n")
    return bibs

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", required=True, help="query string")
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--out", default="data/papers.csv")
    ap.add_argument("--bib", default="")
    args = ap.parse_args()

    results = crossref(args.q, rows=args.n) + arxiv(args.q, rows=max(0, args.n//2))
    # sort by year desc if available
    results.sort(key=lambda r: str(r.get("year") or ""), reverse=True)

    pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=["source","title","authors","venue","year","doi","arxiv_id","url"])
        wr.writeheader()
        wr.writerows(results)

    if args.bib:
        with open(args.bib, "a", encoding="utf-8") as f:
            for b in to_bib_entries(results):
                f.write(b)

    print(f"[search] wrote {len(results)} rows to {args.out}")
    if args.bib:
        print(f"[search] appended BibTeX entries to {args.bib}")
