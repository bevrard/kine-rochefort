#!/usr/bin/env python3
import os
import re
import sys
import mimetypes
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

START_URL = "https://kine-rochefort.be/"
ALLOWED_HOSTS = {"kine-rochefort.be", "www.kine-rochefort.be"}
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
MIRROR_DIR = os.path.join(ROOT_DIR, "site")
USER_AGENT = "Mozilla/5.0 (compatible; OpenClawMirror/1.0)"

visited = set()
queued = []
assets = set()

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.assets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("href", "src"):
            if key in attrs:
                val = attrs[key].strip()
                if not val or val.startswith("data:") or val.startswith("mailto:") or val.startswith("tel:") or val.startswith("javascript:"):
                    continue
                if tag == "a" and key == "href":
                    self.links.append(val)
                else:
                    self.assets.append(val)
        if tag == "link" and attrs.get("rel"):
            href = attrs.get("href")
            if href:
                self.assets.append(href.strip())


def normalize(url):
    url, _frag = urldefrag(url)
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return None
    host = parsed.netloc.lower()
    if host not in ALLOWED_HOSTS:
        return None
    path = parsed.path or "/"
    norm = f"https://{host}{path}"
    if parsed.query:
        norm += f"?{parsed.query}"
    return norm


def local_path_for(url, content_type=None):
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path or "/"
    if path.endswith("/") or path == "":
        path = path + "index.html"
    base = os.path.join(MIRROR_DIR, host, path.lstrip("/"))
    root, ext = os.path.splitext(base)
    if not ext:
        guessed = mimetypes.guess_extension((content_type or "").split(";")[0].strip())
        if guessed and guessed not in (".ksh",):
            base = base + guessed
        else:
            base = base + ".html"
    if parsed.query:
        safe_q = re.sub(r"[^A-Za-z0-9._-]+", "_", parsed.query)[:80]
        root, ext = os.path.splitext(base)
        base = f"{root}__q_{safe_q}{ext}"
    return base


def fetch(url):
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=30) as resp:
        content = resp.read()
        ctype = resp.headers.get("Content-Type", "")
        return content, ctype


def save(url, content, content_type):
    path = local_path_for(url, content_type)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(content)
    return path


def should_crawl(url):
    parsed = urlparse(url)
    path = parsed.path.lower()
    if any(path.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".css", ".js", ".woff", ".woff2", ".ttf", ".eot", ".ico", ".pdf", ".mp4"]):
        return False
    return True


def rewrite_html(file_path, base_url, html):
    def repl(match):
        attr = match.group(1)
        quote = match.group(2)
        raw = match.group(3)
        absolute = normalize(urljoin(base_url, raw))
        if not absolute:
            return match.group(0)
        local = local_path_for(absolute)
        rel = os.path.relpath(local, os.path.dirname(file_path)).replace(os.sep, "/")
        return f'{attr}={quote}{rel}{quote}'

    pattern = re.compile(r'(href|src)=("|\')(.*?)(\2)', re.IGNORECASE)
    return pattern.sub(repl, html)


def process_page(url):
    try:
        content, ctype = fetch(url)
    except (URLError, HTTPError, TimeoutError) as e:
        print(f"WARN page {url}: {e}")
        return
    path = save(url, content, ctype)
    if "html" not in ctype and not path.endswith(".html"):
        return
    text = content.decode("utf-8", errors="ignore")
    parser = LinkParser()
    parser.feed(text)
    for href in parser.links:
        absu = normalize(urljoin(url, href))
        if absu and absu not in visited and absu not in queued and should_crawl(absu):
            queued.append(absu)
    for src in parser.assets:
        absu = normalize(urljoin(url, src))
        if absu:
            assets.add(absu)
    rewritten = rewrite_html(path, url, text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(rewritten)
    print(f"PAGE {url} -> {path}")


def process_asset(url):
    try:
        content, ctype = fetch(url)
    except (URLError, HTTPError, TimeoutError) as e:
        print(f"WARN asset {url}: {e}")
        return
    path = save(url, content, ctype)
    print(f"ASSET {url} -> {path}")


def main():
    os.makedirs(MIRROR_DIR, exist_ok=True)
    queued.append(normalize(START_URL))
    while queued:
        url = queued.pop(0)
        if not url or url in visited:
            continue
        visited.add(url)
        process_page(url)
    for asset in sorted(assets):
        process_asset(asset)
    print(f"Done. Pages: {len(visited)}, Assets: {len(assets)}")

if __name__ == "__main__":
    main()
