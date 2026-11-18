"""Point scripts/backup/verify.py at the new content layout (structured data in src/data, contest pages as .md)."""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
p = os.path.join(ROOT, 'scripts', 'backup', 'verify.py')
s = open(p, encoding='utf-8').read()

s = s.replace('["contest/robocup-humanoid.mdx"]', '["contest/robocup-humanoid.md"]')
s = s.replace('["contest/robocup-rescue.mdx"]', '["contest/robocup-rescue.md"]')
s = s.replace('["contest/src-irc-humanoid.mdx"]', '["contest/src-irc-humanoid.md"]')
s = s.replace('"contest_수상내역": ["contest/awards.md"]', '"contest_수상내역": ["contest/awards.md", "../../data/awards.json"]')
s = s.replace('"contest_수상내역_20072014": ["contest/awards.md"]', '"contest_수상내역_20072014": ["contest/awards.md", "../../data/awards.json"]')
s = s.replace('"contest_수상내역_20152024": ["contest/awards.md"]', '"contest_수상내역_20152024": ["contest/awards.md", "../../data/awards.json"]')
s = s.replace('"events_참여_행사": ["events/participation.md"]', '"events_참여_행사": ["events/participation.md", "../../data/events.json"]')
s = s.replace('"robots_로봇_목록": ["robots/list.md"]', '"robots_로봇_목록": ["robots/list.md", "../../data/robots.json"]')
s = s.replace('"main": ["overview/information.md", "overview/welcome.md"]', '"main": ["overview/information.md"]')

# awards rows now come from the JSON data
old_start = s.index('def award_rows():')
old_end = s.index('def main():')
new_fn = '''def award_rows():
    import json

    rows = []
    for y in json.loads((ROOT / "src" / "data" / "awards.json").read_text(encoding="utf-8")):
        for r in y["rows"]:
            rows.append((r["d"], norm(r["n"] + r["r"] + r["o"])))
    return rows


'''
s = s[:old_start] + new_fn + s[old_end:]
open(p, 'w', encoding='utf-8').write(s)
print('patched verify.py')
