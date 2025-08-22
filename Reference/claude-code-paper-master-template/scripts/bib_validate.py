"""
bib_validate.py — Validate and enrich references.bib using Crossref & arXiv.

Examples:
  python scripts/bib_validate.py --bib references.bib --report data/bib_report.csv --write
"""
import argparse, csv, re, json, pathlib, requests, time

CR_API = "https://api.crossref.org/works/"
ARXIV_API = "http://export.arxiv.org/api/query"


def parse_bib(path):
    text = pathlib.Path(path).read_text(encoding="utf-8", errors="ignore")
    entries = []
    current = None
    for line in text.splitlines():
        if line.strip().startswith("@"):
            if current:
                entries.append(current)
            key = re.findall(r"@\\w+{([^,]+),", line)
            current = {"raw": [line], "key": key[0] if key else ""}
        elif current is not None:
            current["raw"].append(line)
    if current:
        entries.append(current)
    return entries


def find_field(raw_lines, field):
    pat = re.compile(rf"\\b{field}\\s*=\\s*{{([^}}]+)}}", re.IGNORECASE)
    text = "\n".join(raw_lines)
    m = pat.search(text)
    return m.group(1).strip() if m else ""


def replace_field(raw_lines, field, value):
    pat = re.compile(rf"(\\b{field}\\s*=\\s*){{[^}}]+}}", re.IGNORECASE)
    text = "\n".join(raw_lines)
    if pat.search(text):
        text = pat.sub(rf"\\1{{{value}}}", text)
    else:
        # add before closing brace
        if text.strip().endswith("}"):
            text = text.rstrip().rstrip("}") + f",\n  {field}={{ {value} }}\n}}\n"
    return text


def validate_entry(entry):
    raw = "\n".join(entry["raw"])
    doi = find_field(entry["raw"], "doi")
    eprint = find_field(entry["raw"], "eprint")
    report = {"key": entry["key"], "doi": doi, "eprint": eprint, "status": "unknown", "title": "", "year": "", "url": ""}

    if doi:
        r = requests.get(CR_API + doi, timeout=20)
        if r.status_code == 200:
            j = r.json()["message"]
            report["status"] = "ok"
            report["title"] = (j.get("title") or [""])[0]
            report["year"] = (j.get("issued", {}).get("date-parts") or [[None]])[0][0]
            report["url"] = j.get("URL","")
        else:
            report["status"] = f"doi_{r.status_code}"
    elif eprint:
        # quick arXiv existence check
        params = {"search_query": f"id:{eprint}", "max_results": 1}
        r = requests.get(ARXIV_API, params=params, timeout=20)
        if r.status_code == 200 and "<entry>" in r.text:
            report["status"] = "ok_arxiv"
            report["title"] = (r.text.split("<title>")[1].split("</title>")[0]).strip()
        else:
            report["status"] = "arxiv_not_found"
    else:
        report["status"] = "missing_ids"

    return report


def write_report(reports, path):
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=["key","doi","eprint","status","title","year","url"])
        wr.writeheader()
        wr.writerows(reports)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bib", default="references.bib")
    ap.add_argument("--report", default="data/bib_report.csv")
    ap.add_argument("--write", action="store_true", help="enrich titles/year/url back into the .bib")
    args = ap.parse_args()

    entries = parse_bib(args.bib)
    reports = []
    changed = []
    for e in entries:
        rep = validate_entry(e)
        reports.append(rep)
        if args.write and rep["status"].startswith("ok"):
            raw = "\n".join(e["raw"])
            if rep.get("title"):
                raw = replace_field(e["raw"], "title", rep["title"])
            if rep.get("year"):
                raw = replace_field(raw.splitlines(), "year", rep["year"])
            if rep.get("url"):
                raw = replace_field(raw.splitlines(), "url", rep["url"])
            changed.append(raw)

    write_report(reports, args.report)

    if args.write and changed:
        with open(args.bib, "w", encoding="utf-8") as f:
            for ch in changed:
                f.write(ch if ch.endswith("\n") else ch + "\n")

    print(f"[refs] validated {len(entries)} entries → {args.report}")
    if args.write:
        print(f"[refs] wrote enriched metadata back to {args.bib}")
