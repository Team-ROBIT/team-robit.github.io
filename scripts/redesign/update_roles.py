"""Member pages: show 주장(Captain) and 팀장(Team Leader) separately and follow the roles in the Team-ROBIT organization README.
Captain (주장) ranks above Team Leader (팀장)."""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
M = os.path.join(ROOT, 'src', 'content', 'archive', 'members')

# (file, old, new)
EDITS = [
    # 16th
    ('16th.mdx', '{ name: "백인엽", label: "16기(21)" }', '{ name: "백인엽", label: "16기(21)", part: "Software Engineer", github: "INYUP-BAEK", leader: "2023" }'),
    ('16th.mdx', '{ name: "백종욱", label: "16기(21)" }', '{ name: "백종욱", label: "16기(21)", part: "Hardware Design", github: "baekjongwook" }'),
    # 17th
    ('17th.mdx', 'part: "Software Engineer", github: "Leeseunghun03"', 'part: "Software Engineer, Hardware Design", github: "Leeseunghun03", leader: "2024"'),
    ('17th.mdx', 'part: "Software Engineer", github: "minseokle"', 'part: "Software Engineer, Circuit Design", github: "minseokle"'),
    # 18th
    ('18th.mdx', 'part: "Hardware Design", github: "jaewwong"', 'part: "Hardware Design", github: "jaewwong", leader: "2025"'),
    ('18th.mdx', 'part: "Computer Vision", github: "mkdir-sweetiepie"', 'part: "Software Engineer", github: "mkdir-sweetiepie"'),
    # 19th
    ('19th.mdx', 'part: "Computer Vision", github: "beomsuchoi"', 'part: "Software Engineer", github: "beomsuchoi", leader: "2026"'),
    ('19th.mdx', 'part: "Hardware Design", github: "jammay123"', 'part: "Software Engineer", github: "jammay123"'),
    # 20th
    ("20th.mdx", "{ name: '우정윤', part: 'Circuit Design & Hardware Design' }", "{ name: '우정윤', part: 'Circuit Design', github: 'JeongyoonWoo7' }"),
    ("20th.mdx", "{ name: '송수민', part: 'Computer Vision' }", "{ name: '송수민', part: 'Software Engineer', github: 'mikissm' }"),
    ("20th.mdx", "{ name: '김민조', part: 'Software Engineer' }", "{ name: '김민조', part: 'Software Engineer', github: 'kmj060703' }"),
]

for f, old, new in EDITS:
    p = os.path.join(M, f)
    s = open(p, encoding='utf-8').read()
    assert old in s, (f, old)
    open(p, 'w', encoding='utf-8').write(s.replace(old, new, 1))

# chips: add "주장 ..." / "팀장 ..."
CHIPS = {
    '16th.mdx': ['주장 박지훈', '팀장 백인엽'],
    '17th.mdx': ['주장 이명진', '팀장 이승훈'],
    '18th.mdx': ['주장 변정욱', '팀장 소재웅'],
    '19th.mdx': ['주장 하재민', '팀장 최범수'],
}
for f, extra in CHIPS.items():
    p = os.path.join(M, f)
    s = open(p, encoding='utf-8').read()
    m = re.search(r'^chips: (\[.*\])$', s, re.M)
    chips = json.loads(m.group(1))
    for c in extra:
        if c not in chips:
            chips.append(c)
    s = s[: m.start()] + 'chips: ' + json.dumps(chips, ensure_ascii=False) + s[m.end():]
    open(p, 'w', encoding='utf-8').write(s)
print('roles updated')
