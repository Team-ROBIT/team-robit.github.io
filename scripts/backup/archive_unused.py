"""Keep every original image that is not (visibly) used anywhere in the repo, e.g. Google Sites banners and
navigation cards, so nothing is lost before the redesign.  -> src/assets/assets_original/<page>-<n>.webp"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OPT = ROOT / "_backup" / "img-opt"
OUT = ROOT / "src" / "assets" / "assets_original"
ph = json.loads((ROOT / "_backup" / "phash.json").read_text(encoding="utf-8"))
sha = lambda p: hashlib.sha1(p.read_bytes()).hexdigest()
have = set()
for base in (ROOT / "src" / "assets", ROOT / "public"):
    for p in base.rglob("*"):
        if p.is_file() and p.suffix.lower() in (".webp", ".png", ".jpg", ".jpeg", ".gif"):
            have.add(sha(p))
ham = lambda a, b: sum(x != y for x, y in zip(a, b))
local = list(ph["local"].values())
OUT.mkdir(parents=True, exist_ok=True)
n = 0
for name, h in sorted(ph["orig"].items()):
    p = OPT / name
    if sha(p) in have or any(ham(h, lh) <= 8 for lh in local):
        continue
    if name.startswith("contest_참여대회_robocup_humanoid_soccer-002"):  # 32px Google Sheets icon
        continue
    stem = name[:-5].replace("contest_", "").replace("_", "-")
    shutil.copyfile(p, OUT / f"{stem}.webp")
    n += 1
print("archived", n, "unused original images ->", OUT)
