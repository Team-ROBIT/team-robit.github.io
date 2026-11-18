"""Completeness check: original Google Sites pages (_backup/md) vs this repo.

    python scripts/backup/verify.py

For every original page that has a counterpart here it checks
  * text   - every original text line (normalised) appears in the local page
  * images - every image of the page (byte-identical optimised copy) exists under src/assets or public
  * embeds - YouTube / Drive embeds are present (iframe / link / file)
"""
import hashlib
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "_backup" / "md"
OPT = ROOT / "_backup" / "img-opt"
ARCH = ROOT / "src" / "content" / "archive"

MAP = {
    "contest_참여대회_robocup_humanoid_soccer": ["contest/robocup-humanoid.md"],
    "contest_참여대회_robocup_rescue": ["contest/robocup-rescue.md"],
    "contest_참여대회_srcirc_휴머노이드": ["contest/src-irc-humanoid.md"],
    "contest_참여대회_seoul_tech_지능로봇대회_씨름로봇": ["contest/ssireum.md"],
    "contest_참여대회_steam_cup_turtlebot_autorace": ["contest/turtlebot-autorace.md"],
    "contest_참여대회_국방로봇경진대회": ["contest/defense-robot.md"],
    "contest_참여대회_로봇파워_배틀로봇": ["contest/robotpower-battle.md"],
    "contest_참여대회_로봇파워_휴머노이드": ["contest/robotpower-humanoid.md"],
    "contest_참여대회": ["contest/participation.mdx"],
    "contest_수상내역": ["contest/awards.md", "../../data/awards.json"],
    "contest_수상내역_20072014": ["contest/awards.md", "../../data/awards.json"],
    "contest_수상내역_20152024": ["contest/awards.md", "../../data/awards.json"],
    "events_참여_행사": ["events/participation.md", "../../data/events.json"],
    "events_출연_방송": ["events/broadcast.md"],
    "articles_기사_목록": ["articles/press.md"],
    "robots_로봇_목록": ["robots/list.md", "../../data/robots.json"],
    "main": ["overview/information.md"],
    "main_information": ["overview/information.md"],
    "roːbit": ["contact/contact.md"],
    "members_graduated_1st_members_표윤석": ["members/1st-profile.md"],
}
for n in range(1, 20):
    suf = {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")
    grp = "current" if n >= 17 else "graduated"
    MAP[f"members_{grp}_{suf}_members"] = [f"members/{suf}.mdx"]
for y in ("2006", "2007", "2008", "2009"):
    MAP[f"articles_기사_목록_{y}"] = ["articles/press.md"]
for y in ("20092010", "20112012", "20132014", "20152016", "20172018", "20192020", "20212022", "20232024"):
    MAP[f"articles_기사_목록_original_{y}"] = ["articles/press.md"]
# pure navigation / section index pages: kept out of the content collection on purpose
NAV = ["articles", "contest", "events", "members", "robots", "members_current", "members_graduated", "members_graduated_1st_members_이스터에그1"]

NAV_LINE = re.compile(r"(←|→|View More|View Articles|Contest List|Contest\]|Graduated\]|Members\]|\[Members|\[Current|\[2015 ~ 2024|\[Contest\]|\[event)", re.I)
norm = lambda s: re.sub(r"[\W_]+", "", s).lower()


def sha(p):
    return hashlib.sha1(p.read_bytes()).hexdigest()


def local_hashes():
    hs = set()
    for base in (ROOT / "src" / "assets", ROOT / "public"):
        for p in base.rglob("*"):
            if p.is_file():
                hs.add(sha(p))
    return hs


SKIP_TEXT = {norm(x) for x in (
    "AWARD WINNING CAREER 14",  # placeholder text inside one original award row
    "VISION & LOCALIZATION", "CIRCUIT",  # empty headings on the original RoboCup page
    "Participated Competitions", "Participated Events", "2015년 이후", "2014년 이전", "Awards",
)}
LABEL = re.compile(r"^(진행 날짜|진행 장소|참여 인원)\s*:\s*")


def phash_index():
    import json

    d = json.loads((ROOT / "_backup" / "phash.json").read_text(encoding="utf-8"))
    return d["orig"], list(d["local"].values())


def ham(a, b):
    return sum(x != y for x, y in zip(a, b))


def award_rows():
    import json

    rows = []
    for y in json.loads((ROOT / "src" / "data" / "awards.json").read_text(encoding="utf-8")):
        for r in y["rows"]:
            rows.append((r["d"], norm(r["n"] + r["r"] + r["o"])))
    return rows


def main():
    import difflib

    hashes = local_hashes()
    ph_orig, ph_local = phash_index()
    rows = award_rows()
    tot_t = tot_i = tot_l = 0
    for slug, targets in MAP.items():
        f = MD / f"{slug}.md"
        if not f.exists():
            print("NO MD", slug)
            continue
        raw_body = f.read_text(encoding="utf-8").split("---", 2)[2]
        raw_local = "".join((ARCH / t).read_text(encoding="utf-8") for t in targets if (ARCH / t).exists())
        local = norm(raw_local)
        miss = []
        for line in raw_body.splitlines():
            if NAV_LINE.search(line) or "[인터뷰]" in line or "이스터에그" in line:
                continue
            t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", line)
            t = re.sub(r"^#+\s*|<!--.*?-->", "", t).strip()
            t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"", t)
            t = LABEL.sub("", t)
            t = re.sub(r"\d+(?:\.\d)?\s*(?:th|st|nd|rd|기)\(\d\d\)\s*", "", t)  # member labels are re-formatted
            if len(norm(t)) < 4 or norm(t) in SKIP_TEXT or re.match(r"^\(?https?://", t) or re.match(r"^수상\s?횟수", t):
                continue
            if slug.startswith("contest_수상내역_") and re.match(r"^\d\d/\d\d ", t):
                t = t.replace("[AWARD WINNING CAREER 14]", "").replace("47대 배틀제왕 47대 배틀제왕", "47대 배틀제왕")
                ok = any(d == t[:5] and difflib.SequenceMatcher(None, norm(t[5:]), r).ratio() > 0.7 for d, r in rows)
                if not ok:
                    miss.append(t)
                continue
            if norm(t) not in local:
                miss.append(t)
        # external links / videos
        link_miss = []
        for url in set(re.findall(r"\]\((https?://[^)\s]+)\)", raw_body)):
            if "sites.google.com" in url:
                continue
            vid = re.search(r"(?:v=|embed/)([\w-]{11})", url)
            gh = re.search(r"github\.com/([^/?#]+)/?$", url)
            key = vid.group(1) if vid else (gh.group(1) if gh else url.split("?")[0])
            if key not in raw_local and url not in raw_local:
                link_miss.append(url)
        for vid in re.findall(r"youtube\.com/embed/([\w-]{11})", raw_body):
            if vid not in raw_local:
                link_miss.append("youtube:" + vid)
        # images: byte-identical copy, or visually the same photo (re-encoded)
        imgs = list(dict.fromkeys(re.findall(r"img/([^)\s]+)", raw_body)))
        img_miss = []
        for name in imgs:
            p = OPT / (Path(name).stem + ".webp")
            if not p.exists() or sha(p) in hashes or name == "contest_참여대회_robocup_humanoid_soccer-002.png":  # 32px Sheets icon
                continue
            h = ph_orig.get(p.name)
            if h and any(ham(h, lh) <= 8 for lh in ph_local):
                continue
            img_miss.append(name)
        tot_t += len(miss)
        tot_i += len(img_miss)
        tot_l += len(link_miss)
        flag = "OK " if not (miss or img_miss or link_miss) else "!! "
        print(f"{flag}{slug}: text_missing={len(miss)} images={len(imgs)} images_missing={len(img_miss)} links_missing={len(link_miss)}")
        for m in miss[:8]:
            print("     text:", m[:100])
        for m in img_miss[:20]:
            print("     img :", m)
        for m in link_miss[:8]:
            print("     link:", m[:100])
    print("TOTAL text_missing", tot_t, "images_missing", tot_i, "links_missing", tot_l)
    pdfs = len(list((ROOT / "public" / "archive" / "articles").glob("*.pdf")))
    print("PDF files in public/archive/articles:", pdfs, "(expected 74)")
    print("nav/index pages not mapped (by design):", ", ".join(NAV))


if __name__ == "__main__":
    main()
