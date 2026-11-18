"""Docs clean-up for the redesign: new header fields for member pages, no emoji headings, no duplicated H1,
remove the two marketing-style overview pages (their facts live on the Information page and the home page)."""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
A = os.path.join(ROOT, 'src', 'content', 'archive')

EMOJI = re.compile('[\U0001F300-\U0001FAFF☀-➿⬀-⯿️‍]+\\s*')


def read(rel):
    return open(os.path.join(A, rel), encoding='utf-8').read()


def write(rel, text):
    open(os.path.join(A, rel), 'w', encoding='utf-8').write(text)


def split(text):
    _, fm, body = text.split('---', 2)
    return fm.strip('\n'), body


def clean_headings(body):
    out = []
    for line in body.split('\n'):
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            title = EMOJI.sub('', m.group(2)).strip()
            if len(m.group(1)) == 1:  # page title is shown by the page header
                continue
            line = f'{m.group(1)} {title}'
        out.append(line)
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).lstrip('\n')


def add_fields(fm, extra):
    for k, v in extra.items():
        if re.search(rf'^{k}:', fm, re.M):
            continue
        fm += f'\n{k}: {json.dumps(v, ensure_ascii=False)}'
    return fm


# ---- member pages
ORD = {1: '1st', 2: '2nd', 3: '3rd'}
for f in sorted(os.listdir(os.path.join(A, 'members'))):
    m = re.match(r'(\d+)(?:st|nd|rd|th)\.mdx$', f)
    if not m:
        continue
    n = int(m.group(1))
    text = read(f'members/{f}')
    fm, body = split(text)
    teams = re.findall(r'team: ["\']([^"\']+)["\']', body)
    names = re.findall(r'\bname: ["\']', body)
    members_total = len(names) - (1 if re.search(r'captain=\{\{ name:', body) else 0)
    per_team = []
    for t in re.split(r'\{ team: ', body)[1:]:
        tn = re.match(r'["\']([^"\']+)', t).group(1)
        per_team.append(f'{tn} {len(re.findall(r"name: ", t.split("]}")[0]))}')
    fm = add_fields(fm, {'subtitle': f'RO:BIT {ORD.get(n, str(n) + "th")} Members', 'highlight': f'{members_total}명', 'chips': per_team})
    write(f'members/{f}', f'---\n{fm}\n---\n{body}')
print('members updated')

# ---- 1st captain profile
fm, body = split(read('members/1st-profile.md'))
write('members/1st-profile.md', f'---\n{add_fields(fm, {"subtitle": "RO:BIT 1st Captain"})}\n---\n' + clean_headings(body))

# ---- docs: strip emoji + H1
for rel, extra in {
    'overview/history.md': {'subtitle': 'History & Archive', 'highlight': '2006 —'},
    'articles/press.md': {'subtitle': 'Press · 2006 — 2026', 'highlight': '기사 스캔 74건'},
    'events/broadcast.md': {'subtitle': 'Broadcast Appearances', 'highlight': '방송 출연'},
    'contact/contact.md': {'subtitle': 'Contact'},
}.items():
    fm, body = split(read(rel))
    write(rel, f'---\n{add_fields(fm, extra)}\n---\n\n' + clean_headings(body))
print('docs cleaned')

# ---- information (original page): header fields, drop the Google-Sites label banners
fm, body = split(read('overview/information.md'))
labels = {'information-001', 'information-002', 'information-004', 'information-006'}
body = '\n'.join(l for l in body.split('\n') if not any(f'{s}.webp' in l for s in labels))
body = re.sub(r'\n{3,}', '\n\n', body)
write('overview/information.md', f'---\n{add_fields(fm, {"subtitle": "About ROːBIT", "highlight": "2006.11.01 창단", "chips": ["국내 최초 로봇 스포츠 게임단", "광운대학교"]})}\n---\n' + body)

# ---- remove the marketing-style pages
for rel in ('overview/welcome.md', 'overview/about.md'):
    p = os.path.join(A, rel)
    if os.path.exists(p):
        os.remove(p)
        print('removed', rel)
