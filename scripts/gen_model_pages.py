#!/usr/bin/env python3
"""Generate per-model SEO landing pages from models.json.

Usage:  python3 scripts/gen_model_pages.py
Writes: models/<id>.html, models/index.html; adds missing URLs to
sitemap.xml and a "## Model pages" section to llms.txt. Idempotent —
run it any time models.json changes (the autopilot should run it on
every catalog update).
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.privateslm.dev"
APP_STORE = "https://apps.apple.com/app/id6504996891"
TODAY = date.today().isoformat()

# minRamMb -> which devices that realistically means (device RAM tiers)
RAM_TIERS = {
    2048: "virtually every iPhone, iPad and Mac that can install privateSLM",
    3072: "iPhone 12 and later, recent iPads, and any Apple Silicon Mac",
    4096: "iPhone 13 Pro / iPhone 14 and later, M-series iPads, and any Apple Silicon Mac",
    6144: "iPhone 15 Pro and later, M-series iPads, and any Apple Silicon Mac",
    8192: "iPhone 16 Pro and later, M-series iPad Pro / Air, and any Apple Silicon Mac",
}

CATEGORY_BLURB = {
    "Generalists": "an everyday assistant for chat, writing, summarising and quick questions",
    "Coding & SQL": "a coding assistant for writing code, SQL queries and debugging — entirely on your device, so proprietary code never leaves it",
    "Math & STEM": "step-by-step math and STEM reasoning",
    "Medical": "reading and questioning medical literature (informational only — not a substitute for professional medical advice)",
    "Mental Health": "supportive, judgement-free conversation (informational only — not a substitute for professional care)",
    "Finance": "working through financial concepts and documents (informational only — not financial advice)",
    "Lawyer": "drafting and summarising legal text (informational only — not legal advice)",
    "Translation": "translation between major languages, fully offline",
    "Cybersecurity": "security-focused analysis and content safety checks",
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def gb(size_bytes: int) -> str:
    return f"{size_bytes / 1e9:.2f}"


def quant_of(file_name: str) -> str:
    m = re.search(r"(Q\d+_[A-Z0-9_]+|Q\d+)", file_name, re.I)
    return m.group(1).upper() if m else "GGUF"


def page_shell(title: str, description: str, canonical: str, body: str, ld: list) -> str:
    ld_tags = "\n".join(
        f'  <script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'
        for obj in ld
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="stylesheet" href="../assets/style.css">
  <link rel="icon" href="../assets/favicon.png">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:type" content="article">
{ld_tags}
</head>
<body>
  <nav>
    <a class="logo" href="../">private<span>SLM</span></a>
    <div class="links">
      <a href="./">Models</a>
      <a href="../blog/">Blog</a>
      <a class="nav-btn" href="https://github.com/Mega-Studios/privateslm-site/discussions" target="_blank" rel="noopener">Community</a>
      <a href="{APP_STORE}">App Store</a>
    </div>
  </nav>
  <div class="page">
    <div class="wrap">
{body}
    </div>
  </div>
  <footer>
    <span>© 2026 privateSLM</span>
    <span class="spacer"></span>
    <a href="../">privateSLM</a>
    <a href="./">Models</a>
    <a href="../blog/">Blog</a>
    <a href="../compare/private-llm-vs-privateslm.html">vs Private LLM</a>
  </footer>
</body>
</html>
"""


def model_page(m: dict, siblings: list) -> str:
    name, mid = m["name"], m["id"]
    size, ram_mb = gb(m["sizeBytes"]), m["minRamMb"]
    ram_gb = ram_mb // 1024
    quant = quant_of(m["fileName"])
    cat = m["category"]
    tier = RAM_TIERS.get(ram_mb, f"devices with at least {ram_gb} GB of RAM")
    blurb = CATEGORY_BLURB.get(cat, "a local AI assistant")
    canonical = f"{SITE}/models/{mid}.html"
    title = f"Run {name} on iPhone, iPad & Mac — Offline | privateSLM"
    description = (
        f"{name}: a {size} GB {quant} GGUF you download once inside privateSLM and run fully "
        f"offline on-device. Needs {ram_gb} GB RAM — {tier}."
    )

    related = "\n".join(
        f'      <li><a href="{s["id"]}.html">{esc(s["name"])}</a> — {gb(s["sizeBytes"])} GB, needs {s["minRamMb"] // 1024} GB RAM</li>'
        for s in siblings
    )

    faq = [
        (
            f"Does {name} run offline on iPhone?",
            f"Yes. After a one-time {size} GB download inside privateSLM, {name} runs entirely "
            "on-device via llama.cpp. Airplane mode works — nothing is ever sent to a server.",
        ),
        (
            f"How much RAM does {name} need?",
            f"A device with at least {ram_gb} GB of RAM — in practice {tier}.",
        ),
        (
            f"Is {name} free to use in privateSLM?",
            f"The model itself is open-weights ({quant} GGUF) and the download is free. privateSLM "
            "is a one-time purchase — no subscription, no per-message fees.",
        ),
    ]
    faq_html = "\n".join(
        f"    <h3>{esc(q)}</h3>\n    <p>{esc(a)}</p>" for q, a in faq
    )

    ld = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Models", "item": f"{SITE}/models/"},
                {"@type": "ListItem", "position": 2, "name": name, "item": canonical},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in faq
            ],
        },
    ]

    body = f"""<article>
    <h1>Run {esc(name)} locally on iPhone, iPad &amp; Mac</h1>
    <div class="meta">{esc(cat)} · {size} GB download · needs {ram_gb} GB RAM · {quant} GGUF</div>

    <p>{esc(m["description"])}</p>
    <p>In <a href="../">privateSLM</a>, {esc(name)} is {blurb}. You download the model once,
    and from then on every conversation runs entirely on your device — no cloud, no account,
    no tracking, and it keeps working with the radio off.</p>

    <h2>At a glance</h2>
    <table>
      <tr><th>Model</th><td>{esc(name)}</td></tr>
      <tr><th>Category</th><td>{esc(cat)}</td></tr>
      <tr><th>Download size</th><td>{size} GB (one time)</td></tr>
      <tr><th>Quantization</th><td>{quant} (GGUF)</td></tr>
      <tr><th>Minimum device RAM</th><td>{ram_gb} GB</td></tr>
      <tr><th>Runs offline</th><td>Yes — fully on-device after download</td></tr>
      <tr><th>Source</th><td><a href="{m["hfRepoUrl"]}" rel="noopener" target="_blank">Hugging Face</a></td></tr>
    </table>

    <h2>Will it run on my device?</h2>
    <p>{esc(name)} needs a device with at least <strong>{ram_gb} GB of RAM</strong> — that means
    {tier}. The privateSLM catalog states the RAM requirement for every model up front, so you
    know before you download.</p>

    <h2>How to run {esc(name)} in privateSLM</h2>
    <ol>
      <li>Get <a href="{APP_STORE}">privateSLM on the App Store</a> — one-time purchase, no subscription.</li>
      <li>Open <strong>Models</strong>, pick {esc(name)}, and tap <strong>Download</strong> ({size} GB, once).</li>
      <li>Select it as your active model and chat — airplane mode included.</li>
    </ol>
    <p>On iPhones, iPads and Macs with Apple Intelligence, privateSLM can also answer instantly
    with the built-in system model — zero downloads. A catalog model like {esc(name)} is for when
    you want this particular specialist, offline, under your control.</p>

    <h2>Related models</h2>
    <ul>
{related}
      <li><a href="./">Browse the full catalog →</a></li>
    </ul>

    <h2>FAQ</h2>
{faq_html}

    <div class="cta"><a class="btn solid" href="{APP_STORE}">Get privateSLM</a></div>
</article>"""
    return page_shell(title, description, canonical, body, ld)


def index_page(models: list) -> str:
    cats: dict[str, list] = {}
    for m in models:
        cats.setdefault(m["category"], []).append(m)
    # Generalists first, then alphabetical
    order = sorted(cats, key=lambda c: (c != "Generalists", c))

    sections = []
    for cat in order:
        cards = "\n".join(
            f"""      <a class="post-card" href="{m["id"]}.html">
        <div class="meta">{gb(m["sizeBytes"])} GB · needs {m["minRamMb"] // 1024} GB RAM</div>
        <h3>{esc(m["name"])}</h3>
        <p>{esc(m["description"][:160])}{"…" if len(m["description"]) > 160 else ""}</p>
      </a>"""
            for m in cats[cat]
        )
        sections.append(
            f"""    <h2 style="margin:56px 0 6px;text-transform:uppercase;font-size:20px">{esc(cat)}</h2>
    <div class="post-list" style="margin-top:18px">
{cards}
    </div>"""
        )

    canonical = f"{SITE}/models/"
    title = "Local AI Models for iPhone, iPad & Mac — privateSLM catalog"
    description = (
        f"All {len(models)} open models in the privateSLM catalog — coding, math, medical, legal, "
        "finance, translation and general chat. Every one runs fully offline on your device."
    )
    ld = [
        {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": "privateSLM model catalog",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "name": m["name"],
                    "url": f"{SITE}/models/{m['id']}.html",
                }
                for i, m in enumerate(models)
            ],
        }
    ]
    body = f"""<h1 class="page-title">Model catalog</h1>
    <p class="lead">Every model below downloads once and runs fully offline on your iPhone, iPad
    or Mac — checked daily, with the RAM it needs stated up front. Comparing apps?
    See <a href="../compare/private-llm-vs-privateslm.html">privateSLM vs Private LLM</a> and
    <a href="../compare/pocketpal-ai-vs-privateslm.html">privateSLM vs PocketPal AI</a>.</p>
{chr(10).join(sections)}"""
    return page_shell(title, description, canonical, body, ld)


def update_sitemap(urls: list):
    sm = ROOT / "sitemap.xml"
    text = sm.read_text()
    existing = set(re.findall(r"<loc>(.*?)</loc>", text))
    additions = "".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>\n"
        for u in urls
        if u not in existing
    )
    if additions:
        text = text.replace("</urlset>", additions + "</urlset>")
        sm.write_text(text)
    return bool(additions)


def update_llms_txt(models: list, compare_urls: list):
    p = ROOT / "llms.txt"
    text = p.read_text()
    lines = [f"## Model pages (run these on iPhone/iPad/Mac, offline)"]
    lines.append(f"- Full catalog: {SITE}/models/")
    for m in models:
        lines.append(f"- {m['name']} ({m['category']}): {SITE}/models/{m['id']}.html")
    for label, u in compare_urls:
        lines.append(f"- {label}: {u}")
    block = "\n".join(lines) + "\n"
    if "## Model pages" in text:
        text = re.sub(r"## Model pages.*?(?=\n## |\Z)", block, text, flags=re.S)
    elif "## Blog" in text:
        text = text.replace("## Blog", block + "\n## Blog", 1)
    else:
        text = text.rstrip() + "\n\n" + block
    p.write_text(text)


def main():
    models = json.loads((ROOT / "models.json").read_text())["models"]
    out = ROOT / "models"
    out.mkdir(exist_ok=True)

    for m in models:
        sibs = [s for s in models if s["category"] == m["category"] and s["id"] != m["id"]]
        if len(sibs) < 4:
            sibs += [
                s
                for s in models
                if s["category"] != m["category"] and s["minRamMb"] == m["minRamMb"] and s["id"] != m["id"]
            ]
        (out / f"{m['id']}.html").write_text(model_page(m, sibs[:4]))

    (out / "index.html").write_text(index_page(models))

    compare_dir = ROOT / "compare"
    compare_pages = sorted(compare_dir.glob("*.html")) if compare_dir.exists() else []
    compare_urls = [
        (
            f"Comparison: {f.stem.replace('-', ' ')}",
            f"{SITE}/compare/{f.name}",
        )
        for f in compare_pages
    ]

    urls = [f"{SITE}/models/"] + [f"{SITE}/models/{m['id']}.html" for m in models]
    urls += [u for _, u in compare_urls]
    update_sitemap(urls)
    update_llms_txt(models, compare_urls)

    print(f"generated {len(models)} model pages + index; sitemap/llms.txt updated")


if __name__ == "__main__":
    sys.exit(main())
