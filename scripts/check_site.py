#!/usr/bin/env python3
"""Check the static site before a deploy: links, markup, structured data, sitemap.

Usage:  python3 scripts/check_site.py          (all pages)
        python3 scripts/check_site.py --quiet  (problems only)

For every HTML page: internal links and anchors resolve to a file in the repo (after
the redirects in vercel.json), tags are balanced, ids are unique, there is one <h1>,
a <title>, a meta description, a canonical link and a lang attribute, every JSON-LD
block parses, and every FAQPage question is also in the visible text. Then: every
sitemap URL is a page whose canonical is that URL, hreflang links are reciprocal, and
every .md copy linked from a page or llms.txt exists. Exits 1 on any problem.
"""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.privateslm.dev"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SKIP_DIRS = {".git", "node_modules", "bench"}
# privateSLM-era pages kept as an archive; their FAQ markup is not checked against the text.
ARCHIVE = {"compare/offline-ai-chat-iphone.html", "compare/pocketpal-ai-vs-privateslm.html",
           "compare/private-llm-alternatives.html", "compare/private-llm-vs-privateslm.html"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.ids, self.links = [], [], [], []
        self.h1 = 0
        self.title = self.description = self.canonical = None
        self.lang = None
        self.ld, self.in_ld, self.ld_buf = [], False, []
        self.in_script = False
        self.text = []
        self.hreflang = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "meta" and a.get("name") == "description":
            self.description = a.get("content")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.hreflang[a["hreflang"]] = a.get("href")
        if tag == "link" and a.get("rel") == "alternate" and a.get("type") == "text/markdown":
            self.links.append(("href", a.get("href")))
        if tag in ("a", "link") and a.get("href") and a.get("rel") not in ("canonical", "alternate"):
            self.links.append(("href", a["href"]))
        if tag == "a" and a.get("href") and a.get("rel") == "alternate":
            self.links.append(("href", a["href"]))
        if tag in ("img", "script", "source") and a.get("src"):
            self.links.append(("src", a["src"]))
        if tag == "img" and "alt" not in a:
            self.errors.append(f"line {self.getpos()[0]}: <img> without alt")
        if tag == "script":
            self.in_script = True
            if a.get("type") == "application/ld+json":
                self.in_ld, self.ld_buf = True, []

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag == "script":
            self.in_script = False
            if self.in_ld:
                self.ld.append("".join(self.ld_buf))
                self.in_ld = False
        if not self.stack:
            self.errors.append(f"line {self.getpos()[0]}: </{tag}> with nothing open")
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
            return
        # implicitly closed elements (p, li, td...) are legal HTML; report only real mismatches
        names = [t for t, _ in self.stack]
        if tag in names:
            while self.stack and self.stack[-1][0] != tag:
                open_tag, line = self.stack.pop()
                if open_tag not in ("p", "li", "td", "th", "tr", "option", "dt", "dd"):
                    self.errors.append(f"line {line}: <{open_tag}> not closed before </{tag}>")
            self.stack.pop()
        else:
            self.errors.append(f"line {self.getpos()[0]}: </{tag}> without <{tag}>")

    def handle_data(self, data):
        if self.in_ld:
            self.ld_buf.append(data)
        elif self.stack and self.stack[-1][0] == "title":
            self.title = (self.title or "") + data
        elif not self.in_script:
            self.text.append(data)


def redirects():
    data = json.loads((ROOT / "vercel.json").read_text())
    out = []
    for r in data.get("redirects", []):
        src = r["source"]
        pattern = "^" + re.escape(src).replace(re.escape(":path*"), ".*") + "$"
        out.append((re.compile(pattern), r["destination"]))
    return out


REDIRECTS = redirects()


def resolve(url_path: str):
    """A URL path on the site to the file Vercel would serve, or None."""
    for pattern, dest in REDIRECTS:
        if pattern.match(url_path):
            if dest.startswith("http"):
                return "external"
            url_path = dest
            break
    rel = unquote(url_path.lstrip("/"))
    candidates = [rel] if rel and not rel.endswith("/") else []
    candidates.append((rel.rstrip("/") + "/index.html").lstrip("/"))
    for c in candidates:
        f = ROOT / c
        if f.is_file():
            return f
    return None


def page_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{SITE}/"
    if rel.endswith("/index.html"):
        return f"{SITE}/{rel[:-len('index.html')]}"
    return f"{SITE}/{rel}"


def main():
    quiet = "--quiet" in sys.argv
    files = [p for p in sorted(ROOT.rglob("*.html")) if not SKIP_DIRS & set(p.relative_to(ROOT).parts)]
    parsed, problems = {}, []
    for path in files:
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        parsed[path] = page
    ids_of = {path: set(page.ids) for path, page in parsed.items()}
    checked_links = 0
    for path, page in parsed.items():
        rel = path.relative_to(ROOT).as_posix()
        errs = list(page.errors)
        redirect_only = "circuitai/" in rel
        if page.stack:
            errs.append("unclosed at end: " + ", ".join(f"<{t}> (line {l})" for t, l in page.stack
                                                       if t not in ("p", "li", "td", "th", "tr")))
            if errs[-1].endswith(": "):
                errs.pop()
        dupes = {i for i in page.ids if page.ids.count(i) > 1}
        if dupes:
            errs.append(f"duplicate ids: {sorted(dupes)}")
        if not redirect_only:
            if page.h1 != 1:
                errs.append(f"{page.h1} <h1> elements")
            for what, value in (("title", page.title), ("meta description", page.description),
                                ("canonical", page.canonical), ("lang", page.lang)):
                if not value:
                    errs.append(f"no {what}")
            if page.canonical and page.canonical != page_url(path):
                errs.append(f"canonical {page.canonical} is not {page_url(path)}")
        visible = re.sub(r"\s+", " ", "".join(page.text))
        for block in page.ld:
            try:
                data = json.loads(block)
            except ValueError as e:
                errs.append(f"JSON-LD does not parse: {e}")
                continue
            if data.get("@type") == "FAQPage" and rel not in ARCHIVE:
                for q in data["mainEntity"]:
                    for text in (q["name"], q["acceptedAnswer"]["text"]):
                        # sentence by sentence: the visible answer may add a link such as "what changed"
                        for sentence in re.split(r"(?<=[.?!])\s+", text):
                            if sentence.rstrip(".") not in visible:
                                errs.append(f"FAQPage text not visible on the page: {sentence[:60]!r}")
        base = page_url(path)
        for _, href in page.links:
            if href.startswith(("mailto:", "javascript:", "tel:")):
                continue
            url = urlparse(urljoin(base, href))
            if url.netloc and url.netloc != "www.privateslm.dev":
                continue
            checked_links += 1
            target = resolve(url.path) if url.path else path
            if target is None:
                errs.append(f"broken link: {href}")
            elif url.fragment and target != "external":
                target_ids = ids_of.get(target)
                if target_ids is not None and url.fragment not in target_ids:
                    errs.append(f"missing anchor: {href}")
        if errs:
            problems.append((rel, errs))

    # sitemap
    sitemap = (ROOT / "sitemap.xml").read_text()
    locs = re.findall(r"<loc>(.*?)</loc>", sitemap)
    if len(locs) != len(set(locs)):
        problems.append(("sitemap.xml", ["duplicate <loc>"]))
    by_url = {page_url(p): p for p in parsed}
    for loc in locs:
        if loc not in by_url:
            problems.append(("sitemap.xml", [f"no page for {loc}"]))
    generated = [p for p in parsed if "generated by scripts/gen_pages.py" in p.read_text(encoding="utf-8")]
    for p in generated:
        if page_url(p) not in locs:
            problems.append(("sitemap.xml", [f"missing {page_url(p)}"]))

    # hreflang must be reciprocal
    for path, page in parsed.items():
        for code, href in page.hreflang.items():
            other = by_url.get(href)
            if other is None:
                problems.append((path.relative_to(ROOT).as_posix(), [f"hreflang {code} -> missing {href}"]))
            elif page_url(path) not in parsed[other].hreflang.values():
                problems.append((path.relative_to(ROOT).as_posix(), [f"hreflang {code} -> {href} does not link back"]))

    # llms.txt links on this site
    for url in re.findall(r"https://www\.privateslm\.dev[^\s)]*", (ROOT / "llms.txt").read_text()):
        if resolve(urlparse(url).path) is None:
            problems.append(("llms.txt", [f"broken link: {url}"]))

    for rel, errs in problems:
        print(f"{rel}:")
        for e in errs:
            print(f"  {e}")
    if not quiet or problems:
        print(f"{len(parsed)} pages, {checked_links} internal links, {len(locs)} sitemap URLs: "
              f"{sum(len(e) for _, e in problems)} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
