"""Tidy the five contest pages that were migrated as raw conversions: caption headings -> lists, bullet lists, no duplicate titles.
Text is preserved verbatim (checked by scripts/backup/verify.py)."""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
C = os.path.join(ROOT, 'src', 'content', 'archive', 'contest')


def edit(name, fn):
    p = os.path.join(C, name)
    t = open(p, encoding='utf-8').read()
    _, fm, body = t.split('---', 2)
    body = fn(body)
    body = re.sub(r'\n{3,}', '\n\n', body)
    open(p, 'w', encoding='utf-8').write('---' + fm + '---' + body)
    print('tidied', name)


def defense(b):
    start = b.index('### RMP-1')
    end = b.index('## Technology')
    imgs = re.findall(r'!\[\]\([^)]*defense-robot-00[123]\.webp\)', b)
    block = (
        '- **RMP-1** — 2019 한국지능로봇경진대회 · 국방로봇 부문\n'
        '- **방국 2세** — 2021 국방로봇경진대회\n'
        '- **KUBO** — 2022 국방로봇경진대회\n\n'
        + '\n\n'.join(imgs) + '\n\n'
    )
    return b[:start] + block + b[end:]


def turtlebot(b):
    b = b.replace('<2019 Turtlebot3 Autorace Competition>', '2019 Turtlebot3 Autorace Competition')
    b = b.replace('<2022 Turtlebot3 Autorace Competition>', '2022 Turtlebot3 Autorace Competition')
    b = b.replace('<<2019 Robit Turtlebot3\n2022 Robit Turtlebot3>>', '2019 Robit Turtlebot3 · 2022 Robit Turtlebot3')
    b = re.sub(r'<<2019 Robit Turtlebot3\s*\n?\s*2022 Robit Turtlebot3>>', '2019 Robit Turtlebot3 · 2022 Robit Turtlebot3', b)
    if '## TurtleBot3 AutoRace' not in b:
        b = '\n\n## TurtleBot3 AutoRace\n\n' + b.lstrip('\n')
    # technology section starts at the first image after the two competition photos + robot photo
    idx = b.index('turtlebot-autorace-004')
    start = b.rfind('![', 0, idx)
    b = b[:start] + '## Technology\n\n' + b[start:]
    return b


def battle(b):
    # the first image of the page is the original banner (001); the cover uses 003
    b = b.replace('robotpower-battle-003.webp)\n\n![](../../../assets/assets_contest/robotpower-battle-002', 'robotpower-battle-001.webp)\n\n![](../../../assets/assets_contest/robotpower-battle-002', 1)
    b = b.replace('## EBS 로봇파워 배틀로봇\n\n', '', 1)
    b = b.replace('## EBS 로봇파워 - 배틀로봇', '## 프로그램 소개', 1)
    b = re.sub(r'(?m)^-(?=\S)', '- ', b)
    return b


def humanoid(b):
    b = b.replace('## EBS 로봇파워 - 휴머노이드', '## 프로그램 소개', 1)
    lines = b.split('\n')
    out = []
    for l in lines:
        if re.match(r'^\d{4}년 \d+월 \d+일 ', l) or l.startswith('외 총 17건'):
            out.append('- ' + l)
        else:
            out.append(l)
    b = '\n'.join(out)
    b = b.replace('- 2007년 09월 04일', '## 주요 입상 기록\n\n- 2007년 09월 04일', 1)
    return b


edit('defense-robot.md', defense)
edit('turtlebot-autorace.md', turtlebot)
edit('robotpower-battle.md', battle)
edit('robotpower-humanoid.md', humanoid)
