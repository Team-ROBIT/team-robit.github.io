"""One-off conversion: the long Markdown pages (awards, events, robots, roster) -> structured JSON in src/data.

    python -I scripts/redesign/extract_data.py

After running, the Markdown files keep only front matter + a short intro; the views in src/components render the data.
Source text is kept verbatim (verify with scripts/backup/verify.py).
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ARCH = os.path.join(ROOT, 'src', 'content', 'archive')
DATA = os.path.join(ROOT, 'src', 'data')
os.makedirs(DATA, exist_ok=True)


def read(rel):
    return open(os.path.join(ARCH, rel), encoding='utf-8').read()


def dump(name, obj):
    with open(os.path.join(DATA, name), 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    print('wrote', name)


# ---------------------------------------------------------------- awards
def awards():
    text = read('contest/awards.md')
    years = []
    for y, extra, blk in re.findall(r'<summary><b>(\d{4})년 수상 내역([^<]*)</b></summary>(.*?)</details>', text, re.S):
        rows = []
        for line in blk.splitlines():
            m = re.match(r'\|\s*\**(\d\d/\d\d)\**\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$', line)
            if m and not m.group(1).startswith(':'):
                rows.append({'d': m.group(1), 'n': m.group(2), 'r': re.sub(r'[\[\]]', '', m.group(3)), 'o': '' if m.group(4) == '-' else m.group(4)})
        photos = re.findall(r'assets_awards/(awards-\d{4}-\d+)\.webp', blk)
        years.append({'year': int(y), 'note': extra.strip(), 'photo': photos[0] if photos else None, 'rows': rows})
    dump('awards.json', years)
    return text


# ---------------------------------------------------------------- events
def events():
    text = read('events/participation.md')
    out = []
    for chunk in text.split('\n## ')[1:]:
        lines = chunk.splitlines()
        head = lines[0]
        date, _, name = head.partition(' · ')
        place = re.search(r'진행 장소\*\*:\s*(.*)', chunk).group(1).strip()
        people = re.search(r'참여 인원\*\*:\s*(.*)', chunk).group(1).strip()
        desc = [l.strip() for l in lines[1:] if l.strip() and not l.startswith(('-', '!', '<'))]
        images = re.findall(r'assets_events/(event-\d+)\.webp', chunk)
        yt = re.findall(r'youtube\.com/embed/([\w-]+)', chunk)
        out.append({'date': date.strip(), 'name': name.strip(), 'place': place, 'people': people, 'desc': desc, 'images': images, 'youtube': yt})
    dump('events.json', out)
    return text


# ---------------------------------------------------------------- robots
def robots():
    t = read('robots/list.md').split('---', 2)[2]
    pending = []
    cur = None
    rows = []
    for line in t.splitlines():
        m = re.match(r'!\[[^\]]*\]\(.*?(robots-list-\d+)\.webp\)', line)
        if m:
            pending.append(m.group(1))
            continue
        if line.startswith('## '):
            cur = {'name': line[3:].strip(), 'images': pending, 'lines': []}
            pending = []
            rows.append(cur)
        elif cur and line.strip():
            cur['lines'].append(re.sub(r'^#+\s*', '', line.strip()))
    out = []
    for r in rows:
        ls = r['lines']
        facts = {}
        results = []
        desc = []
        for l in ls[1:]:
            m = re.match(r'(Height|Weight|Pilot):\s*(.*)', l)
            if m:
                facts[m.group(1)] = m.group(2)
            elif re.match(r'\d{4}년', l):
                results.append(l)
            else:
                desc.append(l)
        ty = ls[0]
        cat = 'humanoid' if 'Humanoid' in ty else 'battle' if 'Battle' in ty else 'defense' if ('Defense' in ty or 'Rescue' in ty or 'EOD' in ty or 'Disaster' in ty) else 'other'
        if ty.startswith('- '):  # sumo robots have no type line: first line is a feature
            desc.insert(0, ty)
            ty = 'Ssireum Robot'
            cat = 'other'
        out.append({'name': r['name'], 'type': ty, 'cat': cat, 'desc': desc, 'facts': facts, 'results': results, 'images': r['images']})
    dump('robots.json', out)
    return t


# ---------------------------------------------------------------- generations (roster)
def generations():
    text = read('members/roster.md')
    out = []
    for m in re.finditer(r'<a href="/members/(\w+)"[^>]*>\s*<span[^>]*>(현역|은퇴|졸업)</span>\s*<div[^>]*>(\d+)기</div>\s*<div[^>]*>(\d+)명</div>', text):
        out.append({'slug': m.group(1), 'status': m.group(2), 'num': int(m.group(3)), 'count': int(m.group(4))})
    out.sort(key=lambda x: x['num'])
    dump('generations.json', out)
    return text


if __name__ == '__main__':
    awards(); events(); robots(); generations()
