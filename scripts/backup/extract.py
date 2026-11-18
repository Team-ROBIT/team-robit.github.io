"""Google Sites (robitarchieve) -> Markdown extractor.

Usage (from repo root):
    python scripts/backup/extract.py fetch            # download every page into _backup/original
    python scripts/backup/extract.py convert [slug..]  # HTML -> _backup/md/<slug>.md (+ images in _backup/img)
    python scripts/backup/extract.py report            # per-page inventory (text lines / images / embeds)

Only the Python standard library is used. Output stays under _backup/ (git-ignored);
pages are then copied into src/content + src/assets by hand / by a second step.
"""
import html as htmlmod
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
ORIG = ROOT / "_backup" / "original"
MD = ROOT / "_backup" / "md"
IMG = ROOT / "_backup" / "img"
BASE = "https://sites.google.com"
SITE = "/view/robitarchieve/"
UA = {"User-Agent": "Mozilla/5.0"}
REUSE = "--reuse" in sys.argv

VOID = {"br", "img", "hr", "input", "meta", "link", "source", "wbr", "area", "col", "base", "embed", "param", "track"}


def http_get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
        return (data, r.headers.get("Content-Type", "")) if binary else data.decode("utf-8", "replace")


def slug_of(path):
    return re.sub(r"[^\w]+", "_", path.replace(SITE, "")).strip("_") or "index"


# --------------------------------------------------------------------------- fetch
def fetch():
    """Crawl every page reachable from /main by following links under /view/robitarchieve/ (BFS)."""
    ORIG.mkdir(parents=True, exist_ok=True)
    queue = [SITE + "main", SITE + "main/information"]
    seen, pmap = set(), {}
    while queue:
        p = queue.pop(0)
        if p in seen:
            continue
        seen.add(p)
        s = http_get(BASE + urllib.parse.quote(p, safe="/"))
        (ORIG / (slug_of(p) + ".html")).write_text(s, encoding="utf-8")
        pmap[slug_of(p)] = p
        print("saved", p)
        for h in re.findall(r'href="((?:https://sites\.google\.com)?/view/robitarchieve/[^"#?]*)"', s):
            h = urllib.parse.unquote(h.replace(BASE, "")).rstrip("/")
            if h not in seen and h not in queue and h != SITE.rstrip("/"):
                queue.append(h)
        time.sleep(0.4)
    (ROOT / "_backup" / "paths.json").write_text(json.dumps(pmap, ensure_ascii=False, indent=1), encoding="utf-8")


# --------------------------------------------------------------------------- tiny DOM
class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.children, self.parent = tag, dict(attrs or {}), [], parent

    @property
    def classes(self):
        return (self.attrs.get("class") or "").split()


class DomBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root")
        self.cur = self.root
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "svg", "noscript", "template"):
            if tag not in VOID:
                self.skip += 1
            return
        if self.skip:
            return
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        if self.skip or tag in ("script", "style", "svg"):
            return
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg", "noscript", "template"):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip or tag in VOID:
            return
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        if self.skip:
            return
        self.cur.children.append(data)


# --------------------------------------------------------------------------- css
def parse_css(s):
    css = "".join(re.findall(r"<style[^>]*>(.*?)</style>", s, flags=re.S))
    rules = []  # (frozenset(classes), {prop: value})
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sel, body = m.group(1).strip(), m.group(2)
        if "font-size" not in body and "font-weight" not in body:
            continue
        for one in sel.split(","):
            one = one.strip()
            if re.fullmatch(r"(\.[\w-]+)+", one):
                cls = frozenset(one.split(".")[1:])
                props = dict(re.findall(r"([\w-]+)\s*:\s*([^;]+)", body))
                rules.append((cls, props))
    return rules


def style_of(node, rules, cache):
    key = tuple(node.classes)
    if key in cache:
        return cache[key]
    cs = set(node.classes)
    out = {}
    for cls, props in rules:
        if cls <= cs:
            out.update(props)
    size = None
    if "font-size" in out:
        m = re.match(r"([\d.]+)pt", out["font-size"].strip())
        if m:
            size = float(m.group(1))
    weight = out.get("font-weight", "400").strip()
    cache[key] = (size, weight)
    return cache[key]


# --------------------------------------------------------------------------- convert
def unwrap_link(href):
    if not href:
        return None
    href = htmlmod.unescape(href)
    if "google.com/url?" in href:
        q = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get("q")
        if q:
            return q[0]
    if href.startswith("/"):
        return BASE + href
    return href


class Converter:
    def __init__(self, page_html, slug, download=True):
        self.slug = slug
        self.rules = parse_css(page_html)
        self.cache = {}
        b = DomBuilder()
        b.feed(page_html)
        self.root = b.root
        self.raw = page_html
        self.images = []  # (url, local relpath)
        self.embeds = []
        self.download = download
        self.title = ""

    # --- helpers
    def find(self, node, pred):
        for c in node.children:
            if isinstance(c, Node):
                if pred(c):
                    return c
                r = self.find(c, pred)
                if r:
                    return r
        return None

    def inline(self, node):
        out = []
        for c in node.children:
            if isinstance(c, str):
                out.append(c.replace("\xa0", " "))
            elif c.tag == "br":
                out.append("  \n")
            elif c.tag == "a":
                href = unwrap_link(c.attrs.get("href"))
                txt = self.inline(c).strip()
                if href and txt and not href.startswith("#"):
                    out.append(f"[{txt}]({href})")
                else:
                    out.append(txt)
            elif c.tag == "img":
                out.append(self.image(c))
            else:
                out.append(self.inline(c))
        return "".join(out)

    def para_size(self, p):
        sizes = []
        stack = [p]
        while stack:
            n = stack.pop()
            for c in n.children:
                if isinstance(c, Node):
                    if c.tag == "span" and any(isinstance(x, str) and x.strip() for x in c.children):
                        sz, _ = style_of(c, self.rules, self.cache)
                        if sz:
                            sizes.append(sz)
                    stack.append(c)
        return max(sizes) if sizes else None

    def image(self, img):
        src = img.attrs.get("src") or ""
        alt = (img.attrs.get("alt") or "").strip()
        if not src:
            return ""
        full = re.sub(r"=w\d+(-h\d+)?[^/]*$", "=w16383", src)
        self.images.append(full)
        return f"![{alt}]({{{{IMG:{len(self.images) - 1}}}}})"

    def download_all(self, page_path):
        """Download this page's images right away (signed URLs expire fast); retry with a fresh page on failure."""
        from concurrent.futures import ThreadPoolExecutor

        IMG.mkdir(parents=True, exist_ok=True)
        idx_file = IMG / "_index.json"
        index = json.loads(idx_file.read_text(encoding="utf-8")) if idx_file.exists() else {}
        names = {}
        for i, u in enumerate(self.images):  # already downloaded earlier -> reuse
            if index.get(u) and index[u] != "FAILED" and (IMG / index[u]).exists():
                names[i] = index[u]
        for attempt in range(4):
            todo = [i for i in range(len(self.images)) if i not in names]
            if not todo:
                break
            if attempt:  # refresh signed URLs
                time.sleep(1.5)
                fresh = Converter(http_get(BASE + urllib.parse.quote(page_path, safe="/")), self.slug)
                fresh.convert()
                if len(fresh.images) == len(self.images):
                    self.images = fresh.images

            def one(i):
                try:
                    data, _ = http_get(self.images[i], binary=True)
                except Exception:  # noqa: BLE001
                    return i, None
                ext = ".png"
                if data[:3] == bytes([0xFF, 0xD8, 0xFF]):
                    ext = ".jpg"
                elif data[:4] == b"GIF8":
                    ext = ".gif"
                elif data[:4] == b"RIFF" and data[8:12] == b"WEBP":
                    ext = ".webp"
                name = f"{self.slug}-n{i + 1:03d}{ext}"
                (IMG / name).write_bytes(data)
                return i, name

            with ThreadPoolExecutor(max_workers=8) as ex:
                for i, name in ex.map(one, todo):
                    if name:
                        names[i] = name
        failed = [i for i in range(len(self.images)) if i not in names]
        for i in range(len(self.images)):
            index[self.images[i]] = names.get(i, "FAILED")
        idx_file.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
        return names, failed

    # --- block walk
    def blocks(self, node, out, depth=0):
        for c in node.children:
            if isinstance(c, str):
                continue
            t = c.tag
            if t == "p":
                text = self.inline(c).strip()
                if not text:
                    continue
                size = self.para_size(c)
                if size and size >= 24:
                    out.append(("h2", text))
                elif size and size >= 17:
                    out.append(("h3", text))
                else:
                    out.append(("p", text))
            elif t in ("ul", "ol"):
                out.append(("list", self.list_items(c, 0, t == "ol")))
            elif t == "img":
                out.append(("p", self.image(c)))
            elif t == "iframe" or "data-embed-url" in c.attrs:
                url = c.attrs.get("src") or c.attrs.get("data-embed-url") or ""
                self.embeds.append(url)
                out.append(("p", f"<!-- EMBED: {url} -->"))
            elif t == "a" and not any(isinstance(x, Node) and x.tag == "p" for x in c.children):
                txt = self.inline(c).strip()
                if txt:
                    out.append(("p", txt))
            elif t == "section":
                out.append(("hr", ""))
                self.blocks(c, out, depth)
            else:
                self.blocks(c, out, depth)

    def list_items(self, ul, level, ordered):
        items = []
        for li in ul.children:
            if not isinstance(li, Node) or li.tag != "li":
                continue
            parts, subs = [], []
            for c in li.children:
                if isinstance(c, Node) and c.tag in ("ul", "ol"):
                    subs.append(self.list_items(c, level + 1, c.tag == "ol"))
                elif isinstance(c, Node):
                    parts.append(self.inline(c).strip())
                elif c.strip():
                    parts.append(c.strip())
            items.append((" ".join(p for p in parts if p), subs, ordered))
        return items

    def render_list(self, items, level=0):
        lines = []
        for i, (text, subs, ordered) in enumerate(items, 1):
            mark = f"{i}." if ordered else "-"
            lines.append("  " * level + f"{mark} {text}")
            for sub in subs:
                lines.extend(self.render_list(sub, level + 1))
        return lines

    def convert(self):
        main = self.find(self.root, lambda n: n.attrs.get("role") == "main")
        m = re.search(r'<meta property="og:title" content="([^"]*)"', self.raw)
        self.title = htmlmod.unescape(m.group(1)).strip() if m else ""
        start = main
        while start and start.tag != "section":
            start = start.parent
        body = start.parent if start else self.root
        out = []
        seen_start = False
        for c in body.children:
            if not isinstance(c, Node):
                continue
            if c is start:
                seen_start = True
            if seen_start:
                self.blocks(c, out)
        # the banner's own title paragraph repeats the page title -> drop it
        norm = lambda t: re.sub(r"\W+", "", t).lower()
        for i, (kind, val) in enumerate(out):
            if kind not in ("hr", "list") and norm(val) == norm(self.title):
                del out[i]
                break
        lines = []
        for kind, val in out:
            if kind == "hr":
                continue
            if kind == "h2":
                lines.append(f"## {val}")
            elif kind == "h3":
                lines.append(f"### {val}")
            elif kind == "h4":
                lines.append(f"#### {val}")
            elif kind == "list":
                lines.append("\n".join(self.render_list(val)))
            else:
                lines.append(val)
        text = "\n\n".join(lines)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text


def convert(slugs):
    MD.mkdir(parents=True, exist_ok=True)
    files = sorted(ORIG.glob("*.html"))
    if slugs:
        files = [f for f in files if f.stem in slugs]
    pmap = json.loads((ROOT / "_backup" / "paths.json").read_text(encoding="utf-8"))
    for f in files:
        # image URLs are short-lived signed URLs: re-fetch the page right before downloading its images
        live = f.read_text(encoding="utf-8") if REUSE else http_get(BASE + urllib.parse.quote(pmap[f.stem], safe="/"))
        if not REUSE:
            f.write_text(live, encoding="utf-8")
        cv = Converter(live, f.stem)
        body = cv.convert()
        names, failed = cv.download_all(pmap[f.stem])
        body = re.sub(r"\{\{IMG:(\d+)\}\}", lambda m: ("img/" + names[int(m.group(1))]) if int(m.group(1)) in names else "FAILED", body)
        fm = f'---\ntitle: "{cv.title}"\n---\n\n'
        (MD / (f.stem + ".md")).write_text(fm + body + "\n", encoding="utf-8")
        print(f"{f.stem}: title={cv.title!r} chars={len(body)} images={len(cv.images)} failed={len(failed)} embeds={len(cv.embeds)}")


# --------------------------------------------------------------------------- publish
# slug -> (destination md under src/content/archive, ascii asset prefix, asset dir, frontmatter extras)
PUBLISH = {
    "robots_로봇_목록": ("robots/list.md", "robots-list", "assets_robots", {"title": "로봇 목록", "description": "로빛이 개발한 역대 로봇 목록", "order": 1}),
    "contest_참여대회_seoul_tech_지능로봇대회_씨름로봇": ("contest/ssireum.md", "ssireum", "assets_contest", {"title": "SEOUL TECH 지능로봇대회 씨름로봇", "sidebar": False}),
    "contest_참여대회_steam_cup_turtlebot_autorace": ("contest/turtlebot-autorace.md", "turtlebot-autorace", "assets_contest", {"title": "STEAM CUP TurtleBot AutoRace", "sidebar": False}),
    "contest_참여대회_국방로봇경진대회": ("contest/defense-robot.md", "defense-robot", "assets_contest", {"title": "국방로봇경진대회", "sidebar": False}),
    "contest_참여대회_로봇파워_배틀로봇": ("contest/robotpower-battle.md", "robotpower-battle", "assets_contest", {"title": "EBS 로봇파워 배틀로봇", "sidebar": False}),
    "contest_참여대회_로봇파워_휴머노이드": ("contest/robotpower-humanoid.md", "robotpower-humanoid", "assets_contest", {"title": "EBS 로봇파워 휴머노이드", "sidebar": False}),
    "main_information": ("overview/information.md", "information", "assets_overview", {"title": "로빛 소개", "description": "원본 아카이브의 Information 페이지", "order": 4}),
    "roːbit": ("contact/contact.md", "contact", "assets_overview", {"title": "Contact", "description": "로빛 공식 SNS 및 연락처", "order": 1}),
}
LINK_MAP = {
    BASE + SITE + "contest": "/contest/participation",
    BASE + SITE + "events": "/events/participation",
}
OPT = ROOT / "_backup" / "img-opt"
CONTENT = ROOT / "src" / "content" / "archive"
ASSETS = ROOT / "src" / "assets"


def publish(slugs):
    for slug, (dest, prefix, adir, fm) in PUBLISH.items():
        if slugs and slug not in slugs:
            continue
        md = (MD / (slug + ".md")).read_text(encoding="utf-8")
        body = md.split("---\n", 2)[2].lstrip("\n")
        (ASSETS / adir).mkdir(parents=True, exist_ok=True)

        def img(m):
            alt, name = m.group(1), m.group(2)
            src = OPT / (Path(name).stem + ".webp")
            new = f"{prefix}-{Path(name).stem.rsplit('-', 1)[1]}.webp"
            (ASSETS / adir / new).write_bytes(src.read_bytes())
            return f"![{alt}](../../../assets/{adir}/{new})"

        body = re.sub(r"!\[([^\]]*)\]\(img/([^)]+)\)", img, body)
        for old, new in LINK_MAP.items():
            body = body.replace(old, new)
        lines = ["---"]
        for k, v in fm.items():
            lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}" if not isinstance(v, bool) else f"{k}: {str(v).lower()}")
        lines.append("---\n")
        target = CONTENT / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(lines) + "\n" + body, encoding="utf-8")
        print("published", slug, "->", dest)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "fetch":
        fetch()
    elif cmd == "publish":
        publish(set(a for a in sys.argv[2:] if not a.startswith("--")))
    elif cmd == "convert":
        convert(set(a for a in sys.argv[2:] if not a.startswith("--")))
    else:
        print(__doc__)
