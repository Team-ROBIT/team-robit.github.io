"""Parse the converted member pages (_backup/md/members_*_members.md) into JSON.

    python scripts/backup/members.py report     # print parsed data + compare names with src/content/archive/members/*.mdx
    python scripts/backup/members.py json       # write _backup/members.json
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "_backup" / "md"
SLUG_RE = re.compile(r"members_(?:current|graduated)_(\d+)(?:st|nd|rd|th)_members\.md$")
TEAM_RE = re.compile(r"^#*\s*(Humanoid Team|Intelligent Robot Team|Intelligence Robot Team|Battle Robot Team|Intelligent&Battle Robot Team)\s*$")
MEMBER_RE = re.compile(r"^#*\s*\[?\s*(\d+(?:\.\d)?)\s*(?:기|th|st|nd|rd)\s*\((\d{2})\)\s*(.*)$")
CAPTAIN_RE = re.compile(r"^#*\s*RO:BIT\s+\w+\s+Captain\s*$")
IMG_RE = re.compile(r"^!\[[^\]]*\]\(img/([^)]+)\)$")
GH_RE = re.compile(r"\[[▶\s]*View More\]\((https?://[^)]+)\)")
ROLES = {"Hardware Design", "Software Engineer", "Computer Vision", "Circuit Design", "Humanoid Walking"}
NAV_RE = re.compile(r"(←|→|\]\(https://sites\.google\.com/view/robitarchieve/members(?:/(?:current|graduated))?(?:/\d+\w+-members)?\)\s*$|^\[Current Members\])")


def parse(path):
    body = path.read_text(encoding="utf-8").split("---", 2)[2]
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    teams, cur, member = [], None, None
    pending, captain, mode = [], {"name": "", "photos": [], "link": ""}, "roster"
    unknown = []
    for line in lines:
        if "sites.google.com/view/robitarchieve/members" in line and NAV_RE.search(line) and not MEMBER_RE.match(line):
            if "프로필" in line or "이스터에그" in line:
                pass
            else:
                continue
        m = IMG_RE.match(line)
        if m:
            (captain["photos"] if mode == "captain" else pending).append(m.group(1))
            continue
        if CAPTAIN_RE.match(line):
            mode = "captain"
            continue
        if mode == "captain":
            link = re.search(r"\]\((https?://[^)]+)\)", line)
            if link:
                captain["link"] = link.group(1)
            if "이스터에그" in line:
                captain["easter"] = True
                continue
            name = re.sub(r"\[[^\]]*\]\([^)]*\)", "", line)
            name = re.sub(r"^#+\s*|[👑🎓]", "", name).strip()
            if name and not captain["name"]:
                captain["name"] = name
            continue
        t = TEAM_RE.match(line)
        if t:
            cur = {"name": t.group(1), "photos": pending, "members": []}
            pending = []
            teams.append(cur)
            member = None
            continue
        mm = MEMBER_RE.match(line)
        if mm and cur is not None:
            rest = mm.group(3)
            interview = re.search(r"\[인터뷰\]\((https?://[^)]+)\)", rest)
            profile = re.search(r"\]\((https://sites\.google\.com/[^)]+)\)", line)
            name = re.sub(r"\s*-\s*\[인터뷰\]\([^)]*\)", "", rest)
            name = re.sub(r"\]\([^)]*\)", "", name).strip(" []")
            name = re.sub(r"\s+", "", name) if re.fullmatch(r"[가-힣\s]+", name) else name
            member = {"label": f"{mm.group(1)}기({mm.group(2)})", "name": name}
            if interview:
                member["interview"] = interview.group(1)
            if profile:
                member["profile"] = profile.group(1)
            if pending:
                member["_imgs"] = pending
                pending = []
            cur["members"].append(member)
            continue
        if member is not None:
            plain = re.sub(r"^#+\s*", "", line)
            if plain in ROLES:
                member["part"] = plain
                continue
            g = GH_RE.search(line)
            if g:
                member["github"] = g.group(1)
                continue
        unknown.append(line)
    # decide photo semantics: per-member photos when the page has more member-images than teams
    per_member = any("_imgs" in mm for t in teams for mm in t["members"]) and sum(
        1 for t in teams for mm in t["members"] if "_imgs" in mm
    ) >= 3
    for t in teams:
        for mm in t["members"]:
            imgs = mm.pop("_imgs", [])
            if not imgs:
                continue
            if per_member:
                mm["photo"] = imgs[-1]
                t["photos"] += imgs[:-1]
            else:
                t["photos"] += imgs
    return {"teams": teams, "captain": captain, "unknown": unknown}


def all_pages():
    out = {}
    for p in sorted(MD.glob("members_*_members.md")):
        m = SLUG_RE.search(p.name)
        if m:
            out[int(m.group(1))] = parse(p)
    return out


def local_names(n):
    f = ROOT / "src" / "content" / "archive" / "members" / {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th") / ""
    return None


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "report"
    data = all_pages()
    if cmd == "json":
        (ROOT / "_backup" / "members.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print("wrote", len(data))
    else:
        suffix = {1: "1st", 2: "2nd", 3: "3rd"}
        for n, d in data.items():
            f = ROOT / "src" / "content" / "archive" / "members" / f"{suffix.get(n, str(n) + 'th')}.mdx"
            loc = set(re.findall(r"name: '([^']+)'", f.read_text(encoding="utf-8"))) if f.exists() else set()
            orig = {m["name"] for t in d["teams"] for m in t["members"]}
            print(f"{n:>2}기 teams={len(d['teams'])} members={len(orig)} captain={d['captain']['name']!r} cap_photos={len(d['captain']['photos'])}"
                  f" team_photos={[len(t['photos']) for t in d['teams']]} member_photos={sum('photo' in m for t in d['teams'] for m in t['members'])}"
                  f" | only_orig={sorted(orig - loc)} only_local={sorted(loc - orig)} unknown={d['unknown'][:3]}")


# --------------------------------------------------------------------------- emit
OPT = ROOT / "_backup" / "img-opt"
ASSETS = ROOT / "src" / "assets" / "assets_members"
SUFFIX = {1: "1st", 2: "2nd", 3: "3rd"}



def regroup_from_git(n, d):
    """Pages laid out in columns list every team heading first; recover team membership from the earlier hand-made version in git."""
    import subprocess

    if not any(not t["members"] for t in d["teams"]):
        return
    rel = f"src/content/archive/members/{SUFFIX.get(n, str(n) + 'th')}.mdx"
    old = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout
    owner = {}
    for tm in re.finditer(r"team: '([^']+)', members: \[(.*?)\]\}", old, flags=re.S):
        for nm in re.findall(r"name: '([^']+)'", tm.group(2)):
            owner[nm] = tm.group(1)
    members = [m for t in d["teams"] for m in t["members"]]
    for t in d["teams"]:
        t["members"] = []
    by_name = {t["name"]: t for t in d["teams"]}
    for m in members:
        team = by_name.get(owner.get(m["name"])) or d["teams"][-1]
        team["members"].append(m)

def emit():
    import shutil

    ASSETS.mkdir(parents=True, exist_ok=True)
    for n, d in all_pages().items():
        regroup_from_git(n, d)
        f = ROOT / "src" / "content" / "archive" / "members" / f"{SUFFIX.get(n, str(n) + 'th')}.mdx"
        old = f.read_text(encoding="utf-8")
        front = old.split("---", 2)[1]
        imports, counter = [], [0]

        def img(name, kind):
            counter[0] += 1
            var = f"i{counter[0]}"
            out = f"members-{n}-{kind}-{counter[0]}.webp"
            shutil.copyfile(OPT / (Path(name).stem + ".webp"), ASSETS / out)
            imports.append(f"import {var} from '../../../assets/assets_members/{out}';")
            return var

        # keep local-only facts for the (still active) 19th generation: its captain is not on the original page
        keep_captain = None
        if n == 19:
            m = re.search(r"name: ['\"]([^'\"]+)['\"],[^}]*captain: true", old)
            keep_captain = m.group(1) if m else None

        lines = []
        for t in d["teams"]:
            photos = ", ".join(img(p, "team") for p in t["photos"])
            lines.append(f"  {{ team: {json.dumps(t['name'], ensure_ascii=False)}, photos: [{photos}], members: [")
            for m in t["members"]:
                f_ = [f"name: {json.dumps(m['name'], ensure_ascii=False)}", f"label: {json.dumps(m['label'], ensure_ascii=False)}"]
                if m.get("part"):
                    f_.append(f"part: {json.dumps(m['part'], ensure_ascii=False)}")
                gh = re.search(r"github\.com/([^/?#]+)", m.get("github", ""))
                if gh:
                    f_.append(f"github: {json.dumps(gh.group(1))}")
                if m.get("interview"):
                    f_.append(f"interview: {json.dumps(m['interview'])}")
                if m.get("profile"):
                    f_.append("profile: '/members/1st-profile'")
                if m.get("photo"):
                    f_.append(f"photo: {img(m['photo'], 'member')}")
                cap = (m["name"] == d["captain"]["name"]) or (keep_captain and m["name"] == keep_captain)
                if cap:
                    f_.append("captain: true")
                lines.append("    { " + ", ".join(f_) + " },")
            lines.append("  ]},")
        cap = d["captain"]
        cap_js = ""
        if cap["name"]:
            ph = ", ".join(img(p, "captain") for p in cap["photos"])
            link = f", link: {json.dumps(cap['link'])}" if cap.get("link") else ""
            ordinal = f"{n}{'st' if n == 1 else 'nd' if n == 2 else 'rd' if n == 3 else 'th'}"
            cap_js = f"\n  captain={{{{ name: {json.dumps(cap['name'], ensure_ascii=False)}, heading: 'RO:BIT {ordinal} Captain', photos: [{ph}]{link} }}}}"
        body = (
            "import MemberRoster from '../../../components/MemberRoster.astro';\n"
            + "\n".join(imports)
            + "\n\n<MemberRoster"
            + cap_js
            + "\n  teams={[\n"
            + "\n".join(lines)
            + "\n]} />\n"
        )
        f.write_text("---" + front + "---\n" + body, encoding="utf-8")
        print("wrote", f.name, "images", counter[0])


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "emit":
    emit()
