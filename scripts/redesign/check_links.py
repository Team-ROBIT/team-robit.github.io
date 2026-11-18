"""Check that every internal link / image in dist/ resolves (run after `npm run build`)."""
import os
import re
import sys
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DIST = os.path.join(ROOT, 'dist')
bad = {}
google = set()
pages = 0
for base, _, files in os.walk(DIST):
    for f in files:
        if not f.endswith('.html'):
            continue
        pages += 1
        html = open(os.path.join(base, f), encoding='utf-8').read()
        page = '/' + os.path.relpath(os.path.join(base, f), DIST).replace(os.sep, '/')
        for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
            u = m.group(1)
            if 'sites.google.com/view/robitarchieve' in u:
                google.add((page, u))
            if not u.startswith('/') or u.startswith('//'):
                continue
            path = urllib.parse.unquote(u.split('#')[0].split('?')[0])
            if not path:
                continue
            target = os.path.join(DIST, path.lstrip('/'))
            if not (os.path.isfile(target) or os.path.isfile(os.path.join(target, 'index.html'))):
                bad.setdefault(u, set()).add(page)
print('pages', pages)
print('broken internal refs:', len(bad))
for u, ps in list(bad.items())[:20]:
    print('  ', u, '<-', sorted(ps)[:2])
print('links to the old Google Site:', len(google))
for p, u in sorted(google)[:15]:
    print('  ', p, u)
