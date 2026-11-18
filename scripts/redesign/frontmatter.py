"""Add the new header fields (subtitle / chips / cover ...) to the contest pages that were migrated as plain Markdown."""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
C = os.path.join(ROOT, 'src', 'content', 'archive', 'contest')

PAGES = {
    'defense-robot.md': dict(
        title='국방로봇경진대회', description='국방 무인 로봇 기술을 겨루는 경진대회',
        subtitle='Defense Robot Competition', chips=['2019 — 2026', 'RMP-1', '방국 2세', 'KUBO'],
        highlight='2026 · 1위 · 산업통상부장관상', cover='defense-robot-003', kind='cutout'),
    'ssireum.md': dict(
        title='SEOUL TECH 지능로봇대회 씨름로봇', description='상대 로봇을 경기장 밖으로 밀어내는 지능형 씨름로봇 대회',
        subtitle='SRC·IRC Ssireum Robot', chips=['2011년부터 참가'], highlight='2018 — 2021 4연속 우승',
        cover='ssireum-001', kind='photo'),
    'turtlebot-autorace.md': dict(
        title='STEAM CUP TurtleBot AutoRace', description='TurtleBot3 기반 자율주행 레이스 대회',
        subtitle='TurtleBot3 AutoRace', chips=['자율 주행', '차선 · 장애물 인식'], highlight=None,
        cover='turtlebot-autorace-001', kind='photo'),
    'robotpower-battle.md': dict(
        title='EBS 로봇파워 배틀로봇', description='EBS 로봇파워 배틀로봇 부문 출전 기록',
        subtitle='EBS Robot Power · Battle Robot', chips=['EBS 로봇파워'], highlight=None,
        cover='robotpower-battle-001', kind='photo'),
    'robotpower-humanoid.md': dict(
        title='EBS 로봇파워 휴머노이드', description='EBS 로봇파워 휴머노이드 조종형 미션 경기 출전 기록',
        subtitle='EBS Robot Power · Humanoid', chips=['조종형 휴머노이드', '1 VS 1 미션 경기'], highlight='총 17건 입상',
        cover='robotpower-humanoid-001', kind='photo'),
}

for name, d in PAGES.items():
    path = os.path.join(C, name)
    text = open(path, encoding='utf-8').read()
    body = text.split('---', 2)[2]
    fm = ['---', f'title: {json.dumps(d["title"], ensure_ascii=False)}', f'description: {json.dumps(d["description"], ensure_ascii=False)}',
          f'subtitle: {json.dumps(d["subtitle"], ensure_ascii=False)}', f'chips: {json.dumps(d["chips"], ensure_ascii=False)}']
    if d['highlight']:
        fm.append(f'highlight: {json.dumps(d["highlight"], ensure_ascii=False)}')
    fm += [f'cover: ../../../assets/assets_contest/{d["cover"]}.webp', f'coverKind: {d["kind"]}', 'sidebar: false', '---']
    open(path, 'w', encoding='utf-8').write('\n'.join(fm) + body)
    print('updated', name)

# the participation hub (mdx with cards)
p = os.path.join(C, 'participation.mdx')
t = open(p, encoding='utf-8').read()
body = t.split('---', 2)[2]
fm = '''---
title: "참여 대회"
description: "로빛이 도전해온 국내외 주요 로봇 대회 목록"
order: 1
subtitle: "Participated Competitions"
chips: ["RoboCup", "SRC · IRC", "국방로봇경진대회", "EBS 로봇파워"]
highlight: "8종 + 극한로봇"
cover: ../../../assets/assets_awards/awards-2018-004.webp
coverKind: photo
---'''
open(p, 'w', encoding='utf-8').write(fm + body)
print('updated participation.mdx')
