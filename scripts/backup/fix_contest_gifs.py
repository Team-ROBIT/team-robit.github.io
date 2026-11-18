"""Replace the down-sampled / truncated GIFs on the RoboCup Rescue / Humanoid pages with the full original animations."""
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OPT = ROOT / "_backup" / "img-opt"
AC = ROOT / "src" / "assets" / "assets_contest"
CT = ROOT / "src" / "content" / "archive" / "contest"


def cp(src_stem, out):
    shutil.copyfile(OPT / f"{src_stem}.webp", AC / out)


# ---- rescue
rescue = CT / "robocup-rescue.mdx"
t = rescue.read_text(encoding="utf-8")
groups = [
    ("4개의 플리퍼를 사용하여 계단 뿐만 아니라 다양한 지형을 돌파할 수 있습니다.", [4, 5, 6, 7, 8]),
    ("이미지 처리 기술을 통해 색상, 패턴, 동작 인식 등을 수행할 수 있습니다.", [9, 10]),
    ("매니퓰레이터를 이용하여 물체를 들고, 옮기고, 작은 구멍에 넣는 등 다양한 미션을 수행할 수 있습니다.", [11, 12, 13, 14, 15]),
    ("IMU와 LiDAR를 이용하여 localization을 진행하고 map을 생성할 수 있습니다.", [16]),
]
imports, blocks = [], []
for text, nums in groups:
    cells = []
    for n in nums:
        cp(f"contest_참여대회_robocup_rescue-{n:03d}", f"rescue-tech-{n:03d}.webp")
        imports.append(f"import rt{n} from '../../../assets/assets_contest/rescue-tech-{n:03d}.webp';")
        cells.append(f'    <img src={{rt{n}.src}} class="rounded-lg shadow-md !m-0 w-full object-cover" alt="Technology" loading="lazy" />')
    blocks.append(f"{text}\n\n<div class=\"grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 my-6\">\n" + "\n".join(cells) + "\n</div>\n")
t = re.sub(r"import techGif\d+ from [^\n]+\n", "", t)
t = t.replace("\n<ContestDetailLayout", "\n" + "\n".join(imports) + "\n\n<ContestDetailLayout", 1)
a = t.index("## 💻 Technology")
b = t.index("</ContestDetailLayout>")
t = t[:a] + "## 💻 Technology\n" + "\n".join(blocks) + "\n" + t[b:]
rescue.write_text(t, encoding="utf-8")

# ---- humanoid soccer walking
cp("contest_참여대회_robocup_humanoid_soccer-003", "robocup-humanoid-walking.webp")
hp = CT / "robocup-humanoid.mdx"
h = hp.read_text(encoding="utf-8")
h = h.replace("assets_contest/contest-robocup-humanoid-walking.gif", "assets_contest/robocup-humanoid-walking.webp")
hp.write_text(h, encoding="utf-8")

# ---- drop the now-unused truncated gifs
for f in list(AC.glob("contest-robocup-rescue-tech-*.gif")) + [AC / "contest-robocup-humanoid-walking.gif"] + list(AC.glob("contest-src-humanoid-mission-*.gif")):
    if f.exists():
        f.unlink()
        print("removed", f.name)
print("done")
