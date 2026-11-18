"""Download the article scan PDFs that the original site embeds from Google Drive.

    python scripts/backup/pdfs.py download   # -> _backup/pdf/<id>.pdf  (+ _backup/pdf/manifest.json)
    python scripts/backup/pdfs.py publish    # -> public/archive/articles/<period>-NN.pdf and a markdown list

Only files that the public original pages embed (iframe 'drive.google.com/file/d/<id>/preview') are fetched.
"""
import glob
import html
import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
ORIG = ROOT / "_backup" / "original"
PDF = ROOT / "_backup" / "pdf"
PUB = ROOT / "public" / "archive" / "articles"

PERIODS = {
    "articles_기사_목록_2006": "2006",
    "articles_기사_목록_2007": "2007",
    "articles_기사_목록_2008": "2008",
    "articles_기사_목록_2009": "2009",
    "articles_기사_목록_original_20092010": "2009-2010",
    "articles_기사_목록_original_20112012": "2011-2012",
    "articles_기사_목록_original_20132014": "2013-2014",
    "articles_기사_목록_original_20152016": "2015-2016",
    "articles_기사_목록_original_20172018": "2017-2018",
    "articles_기사_목록_original_20192020": "2019-2020",
    "articles_기사_목록_original_20212022": "2021-2022",
    "articles_기사_목록_original_20232024": "2023-2024",
}


def collect():
    items = []  # (period, id, label) in page order
    for slug, period in PERIODS.items():
        s = (ORIG / f"{slug}.html").read_text(encoding="utf-8")
        for tag in re.findall(r"<iframe[^>]*>", s):
            src = re.search(r'data-src="([^"]*)"', tag) or re.search(r' src="([^"]*)"', tag)
            lab = re.search(r'aria-label="([^"]*)"', tag)
            m = src and re.search(r"drive\.google\.com/file/d/([\w-]+)", src.group(1))
            if m:
                label = html.unescape(lab.group(1)) if lab else m.group(1)
                label = re.sub(r"^Drive,\s*", "", label)
                items.append((period, m.group(1), re.sub(r"\.pdf$", "", label, flags=re.I)))
    return items


def fetch(fid):
    out = PDF / f"{fid}.pdf"
    if out.exists() and out.read_bytes()[:4] == b"%PDF":
        return fid, "cached", out.stat().st_size
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                f"https://drive.google.com/uc?export=download&id={fid}", headers={"User-Agent": "Mozilla/5.0"}
            )
            data = urllib.request.urlopen(req, timeout=60).read()
            if data[:4] == b"%PDF":
                out.write_bytes(data)
                return fid, "ok", len(data)
            err = f"not a pdf ({data[:20]!r})"
        except Exception as e:  # noqa: BLE001
            err = str(e)
        time.sleep(1.5)
    return fid, "FAIL " + err, 0


def download():
    PDF.mkdir(parents=True, exist_ok=True)
    items = collect()
    ids = list(dict.fromkeys(i for _, i, _ in items))
    print(len(items), "embeds,", len(ids), "unique files")
    with ThreadPoolExecutor(max_workers=4) as ex:
        res = list(ex.map(fetch, ids))
    bad = [r for r in res if r[1].startswith("FAIL")]
    print("ok", sum(r[1] in ("ok", "cached") for r in res), "fail", len(bad), "total MB", round(sum(r[2] for r in res) / 1048576, 1))
    for b in bad:
        print("  ", b)
    (PDF / "manifest.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")


def publish():
    items = json.loads((PDF / "manifest.json").read_text(encoding="utf-8"))
    PUB.mkdir(parents=True, exist_ok=True)
    placed = {}  # id -> public path
    counters, by_period = {}, {}
    for period, fid, label in items:
        if fid not in placed:
            counters[period] = counters.get(period, 0) + 1
            name = f"{period}-{counters[period]:02d}.pdf"
            (PUB / name).write_bytes((PDF / f"{fid}.pdf").read_bytes())
            placed[fid] = f"/archive/articles/{name}"
        by_period.setdefault(period, []).append((label, placed[fid]))
    lines = []
    for period in PERIODS.values():
        if period not in by_period:
            continue
        lines.append(f"### {period}\n")
        for label, path in by_period[period]:
            safe = label.replace("[", "\[").replace("]", "\]")
            lines.append(f"- [{safe}]({path})")
        lines.append("")
    out = ROOT / "_backup" / "pdf_list.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("published", len(placed), "files; list ->", out)


if __name__ == "__main__":
    {"download": download, "publish": publish}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: print(__doc__))()
