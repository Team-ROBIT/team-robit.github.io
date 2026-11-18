"""Phase-2 merges: bring photos / embeds / original wording from _backup/md into the existing pages.

    python scripts/backup/merge_pages.py events broadcast awards srcirc

Local-only additions (2025~2026 data, event names, etc.) are kept; original material is added.
"""
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "_backup" / "md"
OPT = ROOT / "_backup" / "img-opt"
CONTENT = ROOT / "src" / "content" / "archive"
ASSETS = ROOT / "src" / "assets"


def body_of(slug):
    return (MD / f"{slug}.md").read_text(encoding="utf-8").split("---", 2)[2].strip()


def copy_img(name, prefix, adir):
    """img/<slug>-001.png -> src/assets/<adir>/<prefix>-001.webp ; returns md-relative path (content/archive/<sec>/x.md)."""
    stem = Path(name).stem
    num = stem.rsplit("-", 1)[1]
    out = f"{prefix}-{num}.webp"
    (ASSETS / adir).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OPT / f"{stem}.webp", ASSETS / adir / out)
    return f"../../../assets/{adir}/{out}"


def youtube_iframe(vid, title="YouTube video"):
    return (
        f'<iframe class="w-full aspect-video rounded-xl" src="https://www.youtube.com/embed/{vid}" '
        f'title="{title}" loading="lazy" allowfullscreen></iframe>'
    )


def convert_images(text, prefix, adir):
    return re.sub(
        r"!\[([^\]]*)\]\(img/([^)]+)\)",
        lambda m: f"![{m.group(1)}]({copy_img(m.group(2), prefix, adir)})",
        text,
    )


# --------------------------------------------------------------------------- events
def events():
    orig = body_of("events_참여_행사")
    local = (CONTENT / "events/participation.md").read_text(encoding="utf-8")
    names = {}
    for line in local.splitlines():
        m = re.match(r"\|\s*(\d{4}\.\d{2}\.\d{2})\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|", line)
        if m and not m.group(1).startswith(":"):
            names[(m.group(1), re.sub(r"\s+", "", m.group(3)))] = m.group(2)
    entries = []
    for chunk in re.split(r"(?=진행 날짜:)", orig):
        if not chunk.startswith("진행 날짜:"):
            continue
        date = re.search(r"진행 날짜:\s*([\d.]+)", chunk).group(1).strip()
        place = re.search(r"진행 장소:\s*(.*)", chunk).group(1).strip()
        people = re.search(r"참여 인원:\s*(.*)", chunk).group(1).strip()
        imgs = re.findall(r"!\[[^\]]*\]\(img/([^)]+)\)", chunk)
        yts = re.findall(r"youtube\.com/watch\?v=([\w-]+)", chunk)
        rest = [
            l.strip()
            for l in chunk.splitlines()
            if l.strip()
            and not l.startswith(("진행 날짜", "진행 장소", "참여 인원", "!["))
            and "youtube.com" not in l
        ]
        entries.append(dict(date=date, place=place, people=re.sub(r"\s+", " ", people), desc=rest, imgs=imgs, yts=yts))
    entries.sort(key=lambda e: e["date"], reverse=True)
    out = [
        "---",
        'title: "참여 행사"',
        'description: "지역 축제 등 로빛이 참여한 대외 활동 기록"',
        "order: 1",
        "---",
        "",
        "# 🎪 참여 행사",
        "",
        "로빛은 지역 축제와 대학 행사에 로봇을 들고 나가 전시·시연·체험 프로그램을 진행하며 로봇 대중화에 힘써왔습니다.",
        "",
    ]
    for i, e in enumerate(entries, 1):
        key = (e["date"], re.sub(r"\s+", "", e["place"]))
        name = names.get(key, "")
        out.append(f"## {e['date']}" + (f" · {name}" if name else ""))
        out.append("")
        out.append(f"- **진행 장소**: {e['place']}")
        out.append(f"- **참여 인원**: {e['people']}")
        out.append("")
        out.extend(e["desc"])
        out.append("")
        for y in e["yts"]:
            out.append(youtube_iframe(y, f"{e['date']} 행사 영상"))
            out.append("")
        for j, im in enumerate(e["imgs"], 1):
            out.append(f"![{e['date']} 행사 사진 {j}]({copy_img(im, 'event', 'assets_events')})")
            out.append("")
    (CONTENT / "events/participation.md").write_text("\n".join(out), encoding="utf-8")
    print("events:", len(entries), "entries, named:", sum(1 for e in entries if (e["date"], re.sub(r"\s+", "", e["place"])) in names))


# --------------------------------------------------------------------------- broadcast
def broadcast():
    t = body_of("events_출연_방송")
    t = re.sub(
        r"<!-- EMBED: https://www\.youtube\.com/embed/([\w-]+)[^>]*-->",
        lambda m: youtube_iframe(m.group(1), "방송 영상"),
        t,
    )
    t = convert_images(t, "broadcast", "assets_events")
    t = t.replace("## Broadcast\n\n", "", 1)
    head = (
        "---\n"
        'title: "출연 방송"\n'
        'description: "방송 출연 관련 대외 활동과 언론 보도 자료"\n'
        "order: 2\n"
        "---\n\n"
        "# 📺 출연 방송\n\n"
    )
    (CONTENT / "events/broadcast.md").write_text(head + t + "\n", encoding="utf-8")
    print("broadcast written")


# --------------------------------------------------------------------------- awards
def awards():
    path = CONTENT / "contest/awards.md"
    text = path.read_text(encoding="utf-8")
    year_imgs = {}
    for slug, years in (("contest_수상내역_20072014", range(2007, 2015)), ("contest_수상내역_20152024", range(2015, 2025))):
        lines = body_of(slug).splitlines()
        heads = [i for i, l in enumerate(lines) if re.match(r"## 수상\s?횟수", l)]
        end = next((i for i, l in enumerate(lines) if l.startswith("## [←]")), len(lines))
        for k, y in enumerate(years):
            seg = lines[heads[k] : (heads[k + 1] if k + 1 < len(heads) else end)]
            # the photo sits at the end of the *previous* heading's segment boundary: collect images up to next heading
            imgs = [re.search(r"img/([^)]+)", l).group(1) for l in seg if l.startswith("![")]
            year_imgs[y] = imgs
    # the original puts each year's photo just before the next "수상 횟수" heading -> already inside the segment above
    for y, imgs in year_imgs.items():
        if not imgs:
            continue
        block = re.search(rf"(<summary><b>{y}년 수상 내역[^\n]*</summary>.*?)(</details>)", text, flags=re.S)
        if not block:
            print("no block for", y)
            continue
        gallery = "\n".join(f"![{y}년 수상 사진]({copy_img(im, f'awards-{y}', 'assets_awards')})\n" for im in imgs)
        text = text.replace(block.group(0), block.group(1) + gallery + "\n" + block.group(2), 1)
    if "전체 수상 횟수" not in text:
        text = text.replace(
            "## 🗓 2015년 ~ 현재", "**전체 수상 횟수: 295회(2025년 기준)**\n\n## 🗓 2015년 ~ 현재", 1
        )
    path.write_text(text, encoding="utf-8")
    print("awards photos:", {y: len(v) for y, v in year_imgs.items()})


# --------------------------------------------------------------------------- srcirc
def srcirc():
    path = CONTENT / "contest/src-irc-humanoid.mdx"
    t = path.read_text(encoding="utf-8")
    t = re.sub(r"## Introduction\n.*?\n\n(?=## )", "", t, count=1, flags=re.S)
    orig_para = (
        "SRCIRC 휴머노이드 로봇 스포츠 지능형 하이테크는 휴머노이드 플랫폼을 활용해 육상, 농구, 컬링, 하노이 등 다양한 스포츠 종목을 수행하는 대회입니다. "
        "매년 종목이 무작위로 선정되거나 새로운 경기가 추가되기 때문에, 로보컵과 달리 기본적인 비전 및 보행 기술을 기반으로 매번 새로운 하드웨어와 소프트웨어를 개발해 대회를 준비합니다."
    )
    t = re.sub(r"(<p class=\"text-sm leading-relaxed\">\s*).*?(\s*</p>)", lambda m: m.group(1) + orig_para + m.group(2), t, count=1, flags=re.S)
    t = re.sub(r"<li>2024년 SRCIRC 예선 1위</li>", "<li>2024년 SRCIRC 휴머노이드 로봇 스포츠 지능형 하이테크 부문 예선 1위</li>", t)
    t = re.sub(r"<li>2024년 SRCIRC 하이테크 부문 1위</li>", "<li>2024년 SRCIRC 휴머노이드 로봇 스포츠 지능형 하이테크 부문 1위</li>", t)
    t = re.sub(r"<li>2024년 SRCIRC 하이테크 부문 2위</li>", "<li>2024년 SRCIRC 휴머노이드 로봇 스포츠 지능형 하이테크 부문 2위</li>", t)
    # Playing: use all five original animations
    caps = ["육상", "컬링", "하노이", "농구", "농구"]
    cells = []
    for i, c in enumerate(caps):
        p = copy_img(f"contest_참여대회_srcirc_휴머노이드-{i + 2:03d}.webp", "srcirc-play", "assets_contest")
        cells.append(
            '    <div class="flex flex-col items-center">\n'
            f'        <img src={{play{i + 1}.src}} class="rounded-lg shadow-md !m-0 aspect-square object-cover" alt="{c}" />\n'
            f'        <p class="text-xs font-bold mt-2 text-zinc-600">〈{c}〉</p>\n'
            "    </div>"
        )
    t = re.sub(r"import play\d from [^\n]+\n", "", t)
    imports = "".join(
        f"import play{i + 1} from '../../../assets/assets_contest/srcirc-play-{i + 2:03d}.webp';\n" for i in range(5)
    )
    t = t.replace("\n<ContestDetailLayout", "\n" + imports + "\n<ContestDetailLayout", 1)
    t = re.sub(
        r'(<div class="grid grid-cols-2 md:grid-cols-3 gap-6">\n).*?(\n</div>\n\n</ContestDetailLayout>)',
        lambda m: m.group(1) + "\n".join(cells) + m.group(2),
        t,
        flags=re.S,
    )
    path.write_text(t, encoding="utf-8")
    print("srcirc updated")


if __name__ == "__main__":
    for a in sys.argv[1:]:
        globals()[a]()
