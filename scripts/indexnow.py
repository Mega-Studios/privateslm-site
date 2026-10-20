#!/usr/bin/env python3
"""Tell Bing (and the other IndexNow engines) which pages changed.

ChatGPT's web search reads Bing's index, so this is the quickest way for a new
or corrected page to reach it — days instead of weeks.

    python3 scripts/indexnow.py                     # every URL in the live sitemap
    python3 scripts/indexnow.py /llms.txt /compare/private-llm-alternatives.html
    python3 scripts/indexnow.py --dry-run           # print what would be sent

Run it after a deploy, never before: the engines fetch the key file from the
live site to check the request, and the pages have to be there to be crawled.
The key is public by design — it is served at /<key>.txt.
"""
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

HOST = "www.privateslm.dev"
KEY = "b554a11595e2c5a99c976126fb9e55bb"
ORIGIN = f"https://{HOST}"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "privateslm-indexnow"})
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read().decode("utf-8")


def main() -> int:
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    paths = [a for a in args if not a.startswith("--")]

    try:
        live_key = fetch(f"{ORIGIN}/{KEY}.txt").strip()
    except urllib.error.URLError:
        live_key = ""
    if live_key != KEY:
        print(f"{ORIGIN}/{KEY}.txt does not serve the key yet — deploy first.", file=sys.stderr)
        return 1

    if paths:
        urls = [urllib.parse.urljoin(ORIGIN + "/", p.lstrip("/")) for p in paths]
    else:
        urls = re.findall(r"<loc>([^<]+)</loc>", fetch(f"{ORIGIN}/sitemap.xml"))
    body = {"host": HOST, "key": KEY, "keyLocation": f"{ORIGIN}/{KEY}.txt", "urlList": urls}

    if dry_run:
        print(json.dumps(body, indent=2))
        return 0

    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            status = res.status
    except urllib.error.HTTPError as e:
        print(f"IndexNow: HTTP {e.code} — {e.read().decode('utf-8', 'replace')}", file=sys.stderr)
        return 1
    # 200 and 202 both mean accepted; 202 is "key not validated yet", which
    # clears on its own once the engine has fetched the key file.
    print(f"IndexNow: HTTP {status} for {len(urls)} URLs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
