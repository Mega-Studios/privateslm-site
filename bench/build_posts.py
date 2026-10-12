#!/usr/bin/env python3
"""Builds the three Mac articles and their charts from results.jsonl.

    build_posts.py <results.jsonl> <site dir> <chart html dir> <metal_limit_gb>

Every number in the articles comes from the results file through this script,
so nothing is retyped by hand. Charts are written as HTML (an SVG on a
1200x630 page) for a headless browser to screenshot.
"""
import collections
import html
import json
import os
import re
import sys

RES, SITE, CHARTS, METAL_GB = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
DATE = "October 12, 2026"
BASE = "https://www.privateslm.dev"

# file -> (display name, model page or None, how it is offered in privateSLM)
MODELS = collections.OrderedDict([
    ("LFM2.5-1.2B-Instruct-Q4_K_M.gguf", ("LFM2.5 1.2B", "lfm2.5-1.2b-q4", "free")),
    ("Qwen2.5-1.5B-Instruct-Q4_K_M.gguf", ("Qwen2.5 1.5B", "qwen2.5-1.5b-instruct-q4", "free")),
    ("LiquidAI_LFM2.5-2.6B-Q4_K_M.gguf", ("LFM2.5 2.6B", "lfm2.5-2.6b-q4", "free")),
    ("gemma-2-2b-it-Q4_K_M.gguf", ("Gemma 2 2B", "gemma-2-2b-it-q4", "free")),
    ("ai9stars_G9v3-3B-Q4_K_M.gguf", ("G9v3 3B", "g9v3-3b-q4", "free")),
    ("Llama-3.2-3B-Instruct-Q4_K_M.gguf", ("Llama 3.2 3B", "llama-3.2-3b-instruct-q4", "free")),
    ("Nanbeige_Nanbeige4.2-3B-IQ4_XS.gguf", ("Nanbeige4.2 3B", "nanbeige4.2-3b-q4", "free")),
    ("microsoft_Phi-4-mini-instruct-Q4_K_M.gguf", ("Phi-4 Mini 3.8B", "phi-4-mini-instruct-q4", "free")),
    ("MentaLLaMA-chat-7B.Q4_K_M.gguf", ("MentaLLaMA Chat 7B", "mentallama-chat-7b-q4", "Health Pack")),
    ("qwen2.5-coder-7b-instruct-q4_k_m.gguf", ("Qwen2.5 Coder 7B", "qwen2.5-coder-7b-q4", "Tech Pack")),
    ("Ornith-1.5-9B-Q4_K_M.gguf", ("Ornith 1.5 9B", None, None)),
    ("gpt-oss-20b-Q4_K_M.gguf", ("gpt-oss-20b", None, None)),
])

rows = [json.loads(line) for line in open(RES) if line.strip()]
assert not any(r.get("failed") for r in rows), "a run failed"
runs = collections.defaultdict(dict)
for r in rows:
    runs[r["file"]][r["run"]] = r

S = collections.OrderedDict()  # per-model summary
for file, (name, page, tier) in MODELS.items():
    passes = [runs[file][p] for p in ("passA", "passB", "passC", "passD") if p in runs[file]]
    best = max(passes, key=lambda r: r["gen_tps"])
    ctx = {4096: best["peak_footprint_gb"]}
    for label, r in runs[file].items():
        if label.startswith("ctx"):
            ctx[int(label[3:])] = r["peak_footprint_gb"]
    S[file] = {
        "name": name, "page": page, "tier": tier, "params": best["params_b"], "file_gb": best["weights_gb"],
        "gen": best["gen_tps"], "gen_sd": best["gen_tps_sd"], "pp": best["prompt_tps"],
        "passes": [(p, runs[file][p]["gen_tps"], runs[file][p]["gen_tps_sd"]) for p in ("passA", "passB", "passC", "passD") if p in runs[file]],
        "work4k": best["peak_footprint_gb"], "ctx": dict(sorted(ctx.items())),
        "sustained": runs[file].get("sustained", {}).get("sustained_tps"),
    }

n_models = len(S)
assert all(len(s["passes"]) >= 3 for s in S.values()), "every model needs a rested pass"
total_files_gb = sum(s["file_gb"] for s in S.values())


def n(x, digits=0):
    if digits < 0:
        return f"{round(x, digits):,.0f}"
    return f"{x:.{digits}f}"


def link(s):
    if s["page"]:
        return f'<a href="../models/{s["page"]}.html">{html.escape(s["name"])}</a>'
    return html.escape(s["name"])


def by(name):
    return next(s for s in S.values() if s["name"] == name)


llama3, coder7, mental7, ornith, oss20, lfm12 = (by(x) for x in (
    "Llama 3.2 3B", "Qwen2.5 Coder 7B", "MentaLLaMA Chat 7B", "Ornith 1.5 9B", "gpt-oss-20b", "LFM2.5 1.2B"))
phi4, nanbeige, g9 = by("Phi-4 Mini 3.8B"), by("Nanbeige4.2 3B"), by("G9v3 3B")


def settle(series):
    """First window, and the mean of the last minute (four 15 s windows)."""
    return series[0], sum(series[-4:]) / 4


l_start, l_end = settle(llama3["sustained"])
c_start, c_end = settle(coder7["sustained"])
drop_pct = round(100 * (1 - ((l_end / l_start) + (c_end / c_start)) / 2))

# ---------------------------------------------------------------- charts
CHART_CSS = """*{margin:0;padding:0;box-sizing:border-box}html,body{width:1200px;height:630px;overflow:hidden;background:#000}
svg{display:block}text{font-family:"Helvetica Neue",-apple-system,Arial,sans-serif;fill:#f5f5f7}
.t{font-size:34px;font-weight:700}.s{font-size:19px;fill:#9a9aa3}.l{font-size:19px}.v{font-size:19px;font-weight:700}
.a{font-size:16px;fill:#9a9aa3}.brand{font-size:17px;font-weight:700;letter-spacing:.28em;fill:#fff}"""


def chart_page(svg_body):
    return (f'<!DOCTYPE html><html><head><meta charset="UTF-8"><style>{CHART_CSS}</style></head><body>'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">'
            f'<defs><radialGradient id="g" cx="50%" cy="-10%" r="75%"><stop offset="0" stop-color="#7c4dff" stop-opacity=".38"/>'
            f'<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>'
            f'<rect width="1200" height="630" fill="#000"/><rect width="1200" height="630" fill="url(#g)"/>'
            f'{svg_body}<text class="brand" x="1140" y="600" text-anchor="end">PRIVATE<tspan fill="#a78bff">SLM</tspan></text>'
            f'</svg></body></html>')


def speed_chart():
    top = max(s["gen"] for s in S.values())
    out = ['<text class="t" x="60" y="72">Local LLM speed on an M5 MacBook Air, 24 GB</text>',
           '<text class="s" x="60" y="104">Tokens per second while generating · 4-bit models · llama.cpp on Metal</text>']
    y, step, x0, width = 140, 36.5, 300, 720
    for s in S.values():
        w = width * s["gen"] / top
        colour = "#a78bff" if s["name"] == "gpt-oss-20b" else "#5b4bb5"
        out.append(f'<text class="l" x="{x0 - 16}" y="{y + 19}" text-anchor="end">{html.escape(s["name"])}</text>')
        out.append(f'<rect x="{x0}" y="{y}" width="{w:.0f}" height="25" rx="3" fill="{colour}"/>')
        out.append(f'<text class="v" x="{x0 + w + 12:.0f}" y="{y + 19}">{s["gen"]:.0f}</text>')
        y += step
    return chart_page("".join(out))


def line_chart(title, subtitle, series, xs, x_label, y_label, y_max, x_fmt=str, legend=(760, 170)):
    """series: [(name, colour, [y...])] sharing xs."""
    x0, x1, y0, y1 = 110, 1120, 520, 150
    x_min, x_max = min(xs), max(xs)
    px = lambda x: x0 + (x1 - x0) * (x - x_min) / (x_max - x_min)
    py = lambda v: y0 - (y0 - y1) * v / y_max
    out = [f'<text class="t" x="60" y="72">{html.escape(title)}</text>',
           f'<text class="s" x="60" y="104">{html.escape(subtitle)}</text>']
    for i in range(5):
        v = y_max * i / 4
        out.append(f'<line x1="{x0}" y1="{py(v):.0f}" x2="{x1}" y2="{py(v):.0f}" stroke="#fff" stroke-opacity=".12"/>')
        out.append(f'<text class="a" x="{x0 - 12}" y="{py(v) + 5:.0f}" text-anchor="end">{v:g}</text>')
    for x in xs if len(xs) <= 6 else xs[::4]:
        out.append(f'<text class="a" x="{px(x):.0f}" y="{y0 + 28}" text-anchor="middle">{x_fmt(x)}</text>')
    out.append(f'<text class="a" x="{(x0 + x1) / 2:.0f}" y="{y0 + 58}" text-anchor="middle">{html.escape(x_label)}</text>')
    out.append(f'<text class="a" x="{x0}" y="{y1 - 14}">{html.escape(y_label)}</text>')
    for name, colour, ys in series:
        pts = " ".join(f"{px(x):.1f},{py(v):.1f}" for x, v in zip(xs, ys))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="4" stroke-linejoin="round"/>')
        for x, v in zip(xs, ys):
            out.append(f'<circle cx="{px(x):.1f}" cy="{py(v):.1f}" r="4.5" fill="{colour}"/>')
    lx, ly = legend
    for i, (name, colour, _) in enumerate(series):
        out.append(f'<rect x="{lx}" y="{ly + i * 32 - 13}" width="26" height="6" rx="3" fill="{colour}"/>')
        out.append(f'<text class="l" x="{lx + 38}" y="{ly + i * 32 - 4}">{html.escape(name)}</text>')
    return chart_page("".join(out))


def sustained_chart():
    xs = [15 * (i + 1) for i in range(len(llama3["sustained"]))]
    return line_chart("Five minutes of generation without a fan",
                      "Tokens per second in 15-second windows · M5 MacBook Air, 24 GB",
                      [("Llama 3.2 3B", "#a78bff", llama3["sustained"]), ("Qwen2.5 Coder 7B", "#6fd6c4", coder7["sustained"])],
                      xs, "seconds of continuous generation", "tokens / second", 60,
                      x_fmt=lambda x: f"{x}s")


def memory_chart():
    ctxs = [2048, 4096, 8192, 16384, 32768]
    series = [(s["name"], colour, [s["ctx"][c] for c in ctxs])
              for s, colour in ((llama3, "#a78bff"), (coder7, "#6fd6c4"), (oss20, "#f0b86e"), (ornith, "#e77fa0"))]
    return line_chart("Working memory of a local model, by context size",
                      "Memory on top of the model file, GB · measured on an M5 MacBook Air",
                      series, ctxs, "context size, tokens", "GB", 4, x_fmt=lambda x: f"{x // 1024}K", legend=(150, 190))


os.makedirs(CHARTS, exist_ok=True)
for fname, page in (("m5-air-llm-speed", speed_chart()), ("m5-air-sustained-generation", sustained_chart()),
                    ("llm-working-memory-by-context", memory_chart())):
    open(os.path.join(CHARTS, fname + ".html"), "w", encoding="utf-8").write(page)

# ---------------------------------------------------------------- page shell
IMG = 'style="width:100%;height:auto;border-radius:8px;margin:8px 0 24px;"'
SLUG_SPEED, SLUG_RAM, SLUG_MINI = "local-llm-speed-m5-macbook-air", "how-much-ram-local-llm-mac", "mac-mini-local-ai"


def shell(slug, title, description, body):
    # wide tables scroll inside themselves on a phone instead of widening the page
    body = body.replace("<table>", '<div style="overflow-x:auto;"><table>').replace("</table>", "</table></div>")
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    minutes = max(3, round(words / 220))
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} — privateSLM blog</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <link rel="stylesheet" href="../assets/style.css">
  <link rel="icon" href="../assets/favicon.png">
  <link rel="canonical" href="{BASE}/blog/{slug}.html">
</head>
<body>
  <nav>
    <a class="logo" href="../">private<span>SLM</span></a>
    <div class="links">
      <a href="./">Blog</a>
      <a class="nav-btn" href="https://github.com/Mega-Studios/privateslm-site/discussions" target="_blank" rel="noopener">Community</a>
      <a href="../circuitai/">circuitAI</a>
      <a href="https://apps.apple.com/app/id6504996891">App Store</a>
    </div>
  </nav>
  <div class="page">
    <div class="wrap">
<article>
    <h1>{html.escape(title)}</h1>
    <div class="meta">{DATE} · {minutes} min read</div>

{body}
</article>
    </div>
  </div>
  <footer>
    <span>© 2026 privateSLM</span>
    <span class="spacer"></span>
    <a href="../">privateSLM</a>
    <a href="./">Blog</a>
    <a href="../circuitai/">circuitAI</a>
  </footer>
</body>
</html>
"""
    open(os.path.join(SITE, "blog", slug + ".html"), "w", encoding="utf-8").write(page)
    return minutes


MACHINE = "MacBook Air with an M5 chip and 24 GB of memory"
METHOD_LINKS = (f'<a href="../bench/bench.c">bench.c</a>, <a href="../bench/run_all.sh">run_all.sh</a> and the raw '
                f'<a href="../bench/results.jsonl">results.jsonl</a> ({len(rows)} runs)')

# ---------------------------------------------------------------- article 1: speed
speed_rows = "\n".join(
    f'      <tr><td>{link(s)}</td><td>{n(s["params"], 1)}B</td><td>{n(s["file_gb"], 2)} GB</td>'
    f'<td><strong>{n(s["gen"])}</strong> ± {n(s["gen_sd"], 1)}</td><td>{n(s["pp"], -1) if s["pp"] >= 1000 else n(s["pp"])}</td></tr>'
    for s in S.values())
def pass_cells(s):
    got = {p: g for p, g, _ in s["passes"]}
    return "".join(f'<td>{n(got[p], 1) if p in got else "—"}</td>' for p in ("passA", "passB", "passC", "passD"))


pass_rows = "\n".join(f'      <tr><td>{html.escape(s["name"])}</td>{pass_cells(s)}</tr>' for s in S.values())
doc_tokens = 3000
speed_body = f"""    <p>How fast is a local model on an ordinary Mac — not a Mac Studio with 128 GB, the laptop people actually buy? We took a {MACHINE}, the fanless one, and measured {n_models} models on it: from a 1.2-billion-parameter model that fits in {n(lfm12["file_gb"], 1)} GB to a 20-billion-parameter one that needs {n(oss20["file_gb"], 1)} GB. Same engine, same settings, every model measured in at least three separate passes.</p>

    <p>The short version: the small models write far faster than anyone reads, the 7–9B models write {n(ornith["gen"])}–{n(mental7["gen"])} tokens a second, and the biggest model in the test is faster than the 7B ones. The less pleasant finding is at the end: without a fan, a long generation loses about {drop_pct}% of its speed after two minutes.</p>

    <img src="../assets/blogimg/m5-air-llm-speed.png" alt="Bar chart: tokens per second for {n_models} local models on an M5 MacBook Air with 24 GB, from {n(lfm12["gen"])} for LFM2.5 1.2B to {n(ornith["gen"])} for Ornith 1.5 9B" width="1200" height="630" {IMG}>

    <h2>The numbers</h2>
    <table>
      <tr><th>Model</th><th>Parameters</th><th>File</th><th>Generation, tokens/s</th><th>Prompt, tokens/s</th></tr>
{speed_rows}
    </table>
    <p class="cite">MacBook Air (M5, 10-core GPU, 24 GB), macOS 26.5, on mains power. 4-bit files: Q4_K_M, except Nanbeige4.2 (IQ4_XS). Generation is 256 tokens after a 512-token prompt in a 4,096-token context; each figure is the mean of five repetitions in the fastest pass, ± the standard deviation within it. Prompt speed is rounded to the nearest ten above 1,000.</p>

    <h2>What those speeds feel like</h2>
    <p>A token is roughly three quarters of an English word, and an attentive reader gets through four or five words a second — six or seven tokens. So everything in this table generates faster than you read it. The gap between {n(llama3["gen"])} and {n(lfm12["gen"])} tokens a second only matters when you are <em>not</em> reading along: a summary you will skim, a page being rewritten, a batch of files.</p>
    <p>The prompt column is the wait before the first word. A {doc_tokens:,}-token document — four or five pages — takes about {n(doc_tokens / mental7["pp"])} seconds to read at {n(mental7["pp"])} tokens a second ({html.escape(mental7["name"])}) and under {n(doc_tokens / llama3["pp"] + 0.5)} seconds at {n(llama3["pp"], -1)} ({html.escape(llama3["name"])}).</p>

    <h2>The 20B model that outruns the 7B ones</h2>
    <p>gpt-oss-20b has {n(oss20["params"], 1)} billion parameters and generated {n(oss20["gen"])} tokens a second. The two 7B models managed {n(coder7["gen"])} and {n(mental7["gen"])}. That is not a measurement error: gpt-oss-20b is a mixture-of-experts model, and its file says how — 32 experts in each layer, 4 of them used for any one token (the <code>expert_count</code> and <code>expert_used_count</code> fields in the GGUF header). All {n(oss20["params"], 1)} billion parameters have to sit in memory, {n(oss20["file_gb"], 1)} GB of it, but only a fraction is read for each token.</p>
    <p>Speed follows the parameters a model touches; memory follows the parameters it stores. This is the class of model a 24 GB Mac buys you over a 16 GB one — <a href="{SLUG_RAM}.html">the memory arithmetic is here</a>.</p>

    <h2>Below 4B, size does not predict speed</h2>
    <p>{html.escape(llama3["name"])} ({n(llama3["params"], 1)}B) ran at {n(llama3["gen"])} tokens a second, {html.escape(g9["name"])} at {n(g9["gen"])}, {html.escape(phi4["name"])} at {n(phi4["gen"])}. {html.escape(nanbeige["name"])} — {n(nanbeige["params"], 1)}B parameters despite the name — ran at {n(nanbeige["gen"])}, close to the speed of a 7B. If you choose a small model for its speed, the parameter count on the label is a poor guide; measure the one you mean to use.</p>

    <h2>Two minutes without a fan</h2>
    <p>Everything above is a short burst — the length of a chat reply. The MacBook Air has no fan, so we also let two models generate continuously for five minutes.</p>
    <img src="../assets/blogimg/m5-air-sustained-generation.png" alt="Line chart: generation speed over five minutes on a fanless MacBook Air. Llama 3.2 3B falls from {n(l_start)} to about {n(l_end)} tokens per second, Qwen2.5 Coder 7B from {n(c_start)} to about {n(c_end)}" width="1200" height="630" {IMG}>
    <table>
      <tr><th>Model</th><th>First 15 s</th><th>Slowest 15 s</th><th>Last minute</th><th>Kept</th></tr>
      <tr><td>{html.escape(llama3["name"])}</td><td>{n(l_start, 1)}</td><td>{n(min(llama3["sustained"]), 1)}</td><td>{n(l_end, 1)}</td><td>{n(100 * l_end / l_start)}%</td></tr>
      <tr><td>{html.escape(coder7["name"])}</td><td>{n(c_start, 1)}</td><td>{n(min(coder7["sustained"]), 1)}</td><td>{n(c_end, 1)}</td><td>{n(100 * c_end / c_start)}%</td></tr>
    </table>
    <p class="cite">Tokens per second in 15-second windows. The context is emptied each time it fills (4,096 tokens); the time that takes is not counted.</p>
    <p>Both models hold their speed for about a minute and a half and then slide to roughly {100 - drop_pct}% of where they started. Part of the early decline is the context filling up, which makes every token a little more expensive; the part that does not come back when the context is emptied is heat.</p>
    <p>In practice: a chat reply is over long before this matters. Long jobs — summarising a book chapter by chapter, translating a folder of files — run at the lower rate. A Mac with a fan should hold its speed, but we have not measured one and will not put a number on it. Phones behave the same way: a sustained-load study <a href="2026-08-13-thermal-cliff.html">we covered earlier</a> found an iPhone 16 Pro losing 44% of its throughput.</p>

    <h2>How we measured</h2>
    <ul>
      <li><strong>Machine.</strong> MacBook Air, Apple M5 (10-core CPU, 10-core GPU), 24 GB, macOS 26.5, plugged in, Low Power Mode off. An ordinary desktop session with other apps open, not a clean boot.</li>
      <li><strong>Engine.</strong> llama.cpp build b10488 — the build privateSLM 2.3 ships — with every layer on Metal.</li>
      <li><strong>One run.</strong> Load the model, warm it up, then five times: empty the context, read a 512-token English prompt in one batch, generate 256 tokens one at a time. Context of 4,096 tokens, the app's default.</li>
      <li><strong>Passes.</strong> Every model was measured at least three times: in a pass from the smallest model to the largest with 75 seconds between models, in a second pass in the reverse order, and once more after three minutes of rest. We report the fastest pass, because everything that disturbs a run — a background process, a warm chassis — makes it slower. All passes are below and in the raw data.</li>
      <li><strong>What the passes show.</strong> Rest matters even for short bursts on a fanless machine: the smallest model generated {n(dict((p, g) for p, g, _ in lfm12["passes"])["passB"])} tokens a second 75 seconds after the previous model and {n(dict((p, g) for p, g, _ in lfm12["passes"])["passC"])} after three minutes of rest. Ornith's third pass ran while we were using the laptop ourselves, so it got a fourth.</li>
      <li><strong>Discarded.</strong> Runs made after the laptop was unplugged and had gone to sleep. On battery this Mac switches to Low Power Mode, and those numbers are not comparable with the rest.</li>
      <li><strong>Not measured.</strong> Answer quality. A 1.2B model that writes {n(lfm12["gen"])} tokens a second writes worse text than a 9B at {n(ornith["gen"])}; this page is about speed only. Nor other quantizations, other Macs, or battery power.</li>
    </ul>
    <table>
      <tr><th>Generation, tokens/s</th><th>Pass 1</th><th>Pass 2</th><th>Pass 3, rested</th><th>Pass 4, rested</th></tr>
{pass_rows}
    </table>
    <p>The code and data are public: {METHOD_LINKS}.</p>

    <h2>Run them yourself</h2>
    <p>Eight of these models are free in <a href="../">privateSLM</a>, which is itself free: open <strong>Models</strong>, pick one, and it downloads once and runs offline from then on. Two more are in the expert packs; Ornith 1.5 9B and gpt-oss-20b are not in the catalog. The <a href="../models/">catalog</a> states the memory each one needs before you download it. On Macs and iPhones with Apple Intelligence there is also the built-in model, with nothing to download at all.</p>
    <p>Related: <a href="{SLUG_RAM}.html">how much RAM a local model needs on a Mac</a>, and <a href="{SLUG_MINI}.html">which Mac mini to buy for local AI</a>.</p>
    <div class="cta"><a class="btn solid" href="https://apps.apple.com/app/id6504996891">Get privateSLM</a></div>"""

speed_title = f"Local LLM speed on an M5 MacBook Air: {n_models} models measured"
speed_desc = (f"Tokens per second for {n_models} local models, 1.2B to 20B, on a fanless M5 MacBook Air with 24 GB. "
              f"Measured with llama.cpp; code and raw data included.")

# ---------------------------------------------------------------- article 2: RAM
ratios = [s["file_gb"] / s["params"] for s in S.values()]
file_rows = "\n".join(
    f'      <tr><td>{link(s)}</td><td>{n(s["params"], 2)}B</td><td>{n(s["file_gb"], 2)} GB</td><td>{n(s["file_gb"] / s["params"], 2)}</td>'
    f'<td>{n(s["work4k"], 2)} GB</td><td><strong>{n(s["file_gb"] + s["work4k"], 1)} GB</strong></td></tr>'
    for s in S.values())
CTXS = [2048, 4096, 8192, 16384, 32768]


def per_k(s):
    return (s["ctx"][32768] - s["ctx"][4096]) / ((32768 - 4096) / 1000)


ctx_rows = "\n".join(
    f'      <tr><td>{html.escape(s["name"])}</td>' + "".join(f'<td>{n(s["ctx"][c], 2)}</td>' for c in CTXS)
    + f'<td>{n(1000 * per_k(s))} MB</td></tr>'
    for s in (llama3, coder7, ornith, oss20))
mental_per_k = mental7["work4k"] / 4.096
ram_body = f"""    <p>Most answers to this question are rules of thumb. We measured it instead, on a {MACHINE}, for {n_models} models from 1.2 to 20 billion parameters. The memory a local model needs has two parts, and the second one is easy to overestimate.</p>

    <h2>The short answer</h2>
    <ul>
      <li><strong>The file.</strong> A 4-bit model takes about 0.6 GB per billion parameters, and all of it has to be in memory.</li>
      <li><strong>The working area.</strong> On top of the file the model needs room for its context. For current models that is small — {n(1000 * per_k(ornith))} to {n(1000 * per_k(llama3))} MB per 1,000 tokens of context in our measurements. For models built on older designs it is not: one 7B in the test needs {n(mental7["work4k"], 1)} GB for a 4,096-token context.</li>
      <li><strong>So:</strong> a 3B model is a {n(llama3["file_gb"] + llama3["work4k"], 1)} GB job, a current 7B about {n(coder7["file_gb"] + coder7["work4k"], 0)} GB, and a 20B model {n(oss20["file_gb"] + oss20["ctx"][32768], 1)} GB even with a 32,000-token context — it ran on our 24 GB Mac without trouble.</li>
    </ul>

    <h2>Part one: the file</h2>
    <table>
      <tr><th>Model</th><th>Parameters</th><th>File</th><th>GB per B</th><th>Working area, 4K context</th><th>Total</th></tr>
{file_rows}
    </table>
    <p class="cite">4-bit GGUF files (Q4_K_M; Nanbeige4.2 is IQ4_XS). Working area measured after generating with a 4,096-token context.</p>
    <p>Across the {n_models} files the ratio runs from {n(min(ratios), 2)} to {n(max(ratios), 2)} GB per billion parameters. Use 0.6 and you will be within a tenth. The file is memory-mapped rather than copied, but it still has to be in RAM for the model to run at full speed — count all of it. (How mapped files are counted differs between operating systems; <a href="2026-08-01-mmap-ram-gap.html">we wrote about that separately</a>.)</p>

    <h2>Part two: the working area</h2>
    <p>This is where the model keeps what it has already read: every token of the conversation leaves an entry in every layer. It grows in a straight line with the size of the context — and note that it is the context you <em>allocate</em> that costs memory, not the part you have filled.</p>
    <img src="../assets/blogimg/llm-working-memory-by-context.png" alt="Line chart: working memory in GB against context size from 2K to 32K tokens for four models. Llama 3.2 3B reaches {n(llama3["ctx"][32768], 1)} GB at 32K; Qwen2.5 Coder 7B, gpt-oss-20b and Ornith 1.5 9B stay at or under {n(max(coder7["ctx"][32768], oss20["ctx"][32768], ornith["ctx"][32768]), 1)} GB" width="1200" height="630" {IMG}>
    <table>
      <tr><th>Working area, GB</th><th>2K</th><th>4K</th><th>8K</th><th>16K</th><th>32K</th><th>Per 1,000 tokens</th></tr>
{ctx_rows}
    </table>
    <p class="cite">Memory the process uses on top of the model file, by context size in tokens. The last column is the slope between 4K and 32K.</p>
    <p>Two things stand out. First, the working area has little to do with the size of the model: the 3B model here needs more per token than the 20B one. Second, for all four it is modest — a 32,000-token context costs between {n(min(s["ctx"][32768] for s in (llama3, coder7, ornith, oss20)), 1)} and {n(llama3["ctx"][32768], 1)} GB.</p>

    <h2>Why an older 7B needs gigabytes more</h2>
    <p>{link(mental7)} is a fine-tune of an earlier generation of 7B model, and its working area for a 4,096-token context is {n(mental7["work4k"], 1)} GB — about {n(1000 * mental_per_k)} MB per 1,000 tokens, against {n(1000 * per_k(coder7))} MB for {link(coder7)}, a model of the same size.</p>
    <p>The difference is one design decision, and it is written in the files. Each layer stores a "key" and a "value" for every token, for every attention head. The older model has 32 heads and stores 32 sets. Qwen2.5 Coder 7B has 28 heads that share 4 sets; Llama 3.2 3B has 24 heads sharing 8. Multiply layers by stored sets by head size and you get the numbers we measured, to within a few percent:</p>
    <table>
      <tr><th>Model</th><th>Layers</th><th>Heads</th><th>Stored sets</th><th>Arithmetic, per 1,000 tokens</th><th>Measured</th></tr>
      <tr><td>{html.escape(mental7["name"])}</td><td>32</td><td>32</td><td>32</td><td>{n(32 * 32 * 128 * 4 * 1000 / 1e6)} MB</td><td>{n(1000 * mental_per_k)} MB</td></tr>
      <tr><td>{html.escape(llama3["name"])}</td><td>28</td><td>24</td><td>8</td><td>{n(28 * 8 * 128 * 4 * 1000 / 1e6)} MB</td><td>{n(1000 * per_k(llama3))} MB</td></tr>
      <tr><td>{html.escape(coder7["name"])}</td><td>28</td><td>28</td><td>4</td><td>{n(28 * 4 * 128 * 4 * 1000 / 1e6)} MB</td><td>{n(1000 * per_k(coder7))} MB</td></tr>
    </table>
    <p class="cite">Layer and head counts from each file's GGUF header; 128 values per head, a key and a value, 2 bytes each. The measured figure for MentaLLaMA is its working area divided by its 4,096-token context, which also includes fixed buffers.</p>
    <p>The practical point: "a 7B model needs 8 GB" was a fair rule for the older designs with a few thousand tokens of context. It overstates what a current 7B needs by about three gigabytes.</p>

    <h2>What fits which Mac</h2>
    <p>We have one Mac, so only one row of this table is measured. The rest is arithmetic from the numbers above, with one rule of thumb we are stating rather than proving: keep the model — file plus working area — to about half of the machine's memory, and macOS and your other apps keep theirs.</p>
    <table>
      <tr><th>Mac memory</th><th>Comfortable budget</th><th>What that runs</th><th>Basis</th></tr>
      <tr><td>8 GB</td><td>about 4 GB</td><td>Models up to 4B with room to spare ({html.escape(phi4["name"])} needs {n(phi4["file_gb"] + phi4["work4k"], 1)} GB). A 7B is {n(coder7["file_gb"] + coder7["work4k"], 0)}–{n(mental7["file_gb"] + mental7["work4k"], 0)} GB: over budget.</td><td>Arithmetic</td></tr>
      <tr><td>16 GB</td><td>about 8 GB</td><td>7B and 9B models ({n(ornith["file_gb"] + ornith["work4k"], 1)} GB for the 9B here), with long contexts. A 20B model at {n(oss20["file_gb"] + oss20["work4k"], 0)} GB is not a comfortable fit.</td><td>Arithmetic</td></tr>
      <tr><td>24 GB</td><td>about 12 GB</td><td>Everything in this test, including the 20B model with a 32K context ({n(oss20["file_gb"] + oss20["ctx"][32768], 1)} GB).</td><td><strong>Measured</strong></td></tr>
      <tr><td>32 GB</td><td>about 16 GB</td><td>Models around 27B, by the 0.6 GB rule.</td><td>Arithmetic</td></tr>
      <tr><td>64 GB</td><td>about 32 GB</td><td>Models around 50B; a 70B at about 42 GB takes two thirds of the machine.</td><td>Arithmetic</td></tr>
    </table>
    <p>Half the machine is a comfortable target, not the ceiling: on the 24 GB test machine, the amount of GPU memory macOS recommends one app stay within is {n(METAL_GB, 1)} GB.</p>

    <h2>Speed is a separate question</h2>
    <p>Fitting in memory says nothing about how fast a model runs. On the same Mac the 20B model generated {n(oss20["gen"])} tokens a second and the 9B one {n(ornith["gen"])}. The speed measurements, including what happens on a fanless Mac after two minutes, are in <a href="{SLUG_SPEED}.html">Local LLM speed on an M5 MacBook Air</a>.</p>

    <h2>How we measured</h2>
    <ul>
      <li><strong>Machine and engine.</strong> MacBook Air (M5, 24 GB), macOS 26.5; llama.cpp build b10488 with every layer on Metal — the build privateSLM 2.3 ships.</li>
      <li><strong>Working area.</strong> The process's own peak memory footprint after loading the model and generating — the same measure Activity Monitor reports as Memory. It leaves out the mapped model file, which is why we add the file size back.</li>
      <li><strong>Context sizes.</strong> Four models were run again at 2,048, 8,192, 16,384 and 32,768 tokens, one process per size.</li>
      <li><strong>Not measured.</strong> What happens when a model does not fit; other quantizations (an 8-bit file is nearly twice the size); image input.</li>
    </ul>
    <p>The code and data are public: {METHOD_LINKS}.</p>

    <h2>On iPhone and iPad</h2>
    <p>The same arithmetic applies with less room to spare, which is why <a href="../">privateSLM</a> states the memory every model needs before you download it and hides the ones your device cannot run. The <a href="../models/">catalog</a> has a page per model. In the app the context is 4,096 tokens by default, adjustable from 2,048 to 8,192 under Settings.</p>
    <p>Buying a Mac for this? See <a href="{SLUG_MINI}.html">which Mac mini to buy for local AI</a>.</p>
    <div class="cta"><a class="btn solid" href="https://apps.apple.com/app/id6504996891">Get privateSLM</a></div>"""

ram_title = "How much RAM do you need to run an LLM on a Mac? Measured"
ram_desc = (f"A local model needs its file plus a working area that grows with context. We measured both for "
            f"{n_models} models, 1.2B to 20B, on a 24 GB Mac.")

# ---------------------------------------------------------------- article 3: Mac mini
catalog = json.load(open(os.path.join(SITE, "models.json")))["models"]
largest = max(catalog, key=lambda m: m["sizeBytes"])
mini_speed_rows = "\n".join(
    f'      <tr><td>{link(s)}</td><td>{n(s["file_gb"] + s["work4k"], 1)} GB</td><td>{n(s["gen"])}</td></tr>'
    for s in (lfm12, llama3, phi4, coder7, ornith, oss20))
mini_body = f"""    <p>A Mac mini is the usual suggestion for a private AI machine on a desk: a small box with Apple silicon's unified memory, and a fan. The question is which one. Memory decides what you can run at all; the chip decides how fast. Here is what each configuration can hold, based on model sizes and speeds we measured — and, clearly marked, what we could not measure.</p>

    <h2>The current line-up</h2>
    <table>
      <tr><th>Chip</th><th>CPU / GPU</th><th>Memory</th><th>Memory bandwidth</th></tr>
      <tr><td>M6</td><td>12-core / 12-core</td><td>16 GB</td><td>153 GB/s</td></tr>
      <tr><td>M6</td><td>12-core / 12-core</td><td>24 GB or 32 GB</td><td>170 GB/s</td></tr>
      <tr><td>M5 Pro</td><td>15-core / 16-core, or 18-core / 20-core</td><td>24, 48 or 64 GB</td><td>307 GB/s</td></tr>
    </table>
    <p class="cite">From <a href="https://www.apple.com/mac-mini/specs/" target="_blank" rel="noopener">Apple's Mac mini specifications</a>, checked on {DATE}. Storage starts at 256 GB on the 16 GB model and 512 GB on the others. Prices vary by country and change; see Apple's store for yours.</p>
    <p>Memory cannot be added later, so this is the decision to get right.</p>

    <h2>What we measured, and on what</h2>
    <p>Not on a Mac mini. Our numbers come from a MacBook Air with an M5 chip — 10-core GPU, 24 GB, 153 GB/s by Apple's figure — which is one chip generation behind the mini's M6 and has no fan. Read them as a likely floor for the M6 mini, not as its score.</p>
    <table>
      <tr><th>Model</th><th>Memory needed</th><th>Generation, tokens/s (M5 Air)</th></tr>
{mini_speed_rows}
    </table>
    <p class="cite">Memory is the model file plus its working area for a 4,096-token context. Full tables: <a href="{SLUG_SPEED}.html">speed</a>, <a href="{SLUG_RAM}.html">memory</a>.</p>
    <p>Two differences should favour the mini, and we have measured neither. The M6 has two more GPU cores, and in its 24 and 32 GB configurations more memory bandwidth than our test machine. And it has a fan: the Air lost about {drop_pct}% of its generation speed after two minutes of continuous work, which is a cooling limit, not a chip limit.</p>

    <h2>16 GB: every small and mid-size model</h2>
    <p>A model needs its file plus a working area in memory, and half of the machine is a comfortable budget for it. Half of 16 GB is 8 GB, which covers everything up to 9B in our test — the largest, {html.escape(ornith["name"])}, needs {n(ornith["file_gb"] + ornith["work4k"], 1)} GB. It also covers all {len(catalog)} models in the <a href="../models/">privateSLM catalog</a>; the largest file there is {largest["sizeBytes"] / 1e9:.1f} GB.</p>
    <p>What it does not hold comfortably is the 20B class: gpt-oss-20b needs {n(oss20["file_gb"] + oss20["work4k"], 0)} GB before you open anything else. Note too that the 16 GB model starts at 256 GB of storage; the {n_models} model files in our test add up to {n(total_files_gb)} GB.</p>

    <h2>24 GB: the 20B class</h2>
    <p>This is the configuration we can speak for, because our test machine has the same amount. A 20-billion-parameter model with a 32,000-token context took {n(oss20["file_gb"] + oss20["ctx"][32768], 1)} GB and ran at {n(oss20["gen"])} tokens a second — faster than the 7B models, because it is a mixture-of-experts design that reads only part of itself for each token. If you are buying a mini mainly to run local models, this is the one we would start from: it is the smallest configuration that runs that class comfortably, and it is also where the M6's faster memory begins.</p>

    <h2>32 GB: headroom, by arithmetic</h2>
    <p>We have not run anything that needs it. By the 0.6 GB-per-billion-parameters rule our files follow, a 27B model is about 16 GB — half of this machine. Buy it if you already know you want models of that size, or if the mini will be doing other memory-hungry work at the same time.</p>

    <h2>M5 Pro, 48 or 64 GB: larger models, and faster ones</h2>
    <p>Again arithmetic: a 70B model at 4 bits is around 42 GB, which is workable in 64 GB and too tight for 48. The other reason to look at the M5 Pro is the last column of the table above. Generating text is mostly a matter of reading the model's weights from memory over and over, so memory bandwidth is the specification most often tied to speed on large models, and the M5 Pro has nearly twice the M6's. We have not measured by how much that helps, and would not guess.</p>

    <h2>What we would buy</h2>
    <ul>
      <li><strong>To try local AI and keep the option open:</strong> M6 with 24 GB.</li>
      <li><strong>Only small and mid-size models, and the budget is tight:</strong> M6 with 16 GB — with more than 256 GB of storage if you can.</li>
      <li><strong>You already know you want 27B-class models:</strong> M6 with 32 GB.</li>
      <li><strong>Larger than that, or speed on big models matters:</strong> M5 Pro with 48 or 64 GB.</li>
    </ul>

    <h2>What this page does not know</h2>
    <ul>
      <li>How fast any Mac mini actually is. Every speed here was measured on an M5 MacBook Air.</li>
      <li>How models larger than 20B behave. Everything above that line is arithmetic from file sizes.</li>
      <li>Prices. They differ by country and by the week.</li>
      <li>Answer quality. A bigger model is not automatically the better one for your work.</li>
    </ul>
    <p>The measurements behind the numbers, with code and raw data: {METHOD_LINKS}.</p>

    <h2>Once it is on your desk</h2>
    <p><a href="../">privateSLM</a> is free on the Mac App Store and runs on the mini as it does on a MacBook or an iPhone: on a Mac with Apple Intelligence it answers straight away with the built-in model, and the <a href="../models/">catalog</a> adds open models that download once and then work offline. Nothing you type leaves the machine.</p>
    <div class="cta"><a class="btn solid" href="https://apps.apple.com/app/id6504996891">Get privateSLM</a></div>"""

mini_title = "Mac mini for local AI: which configuration to buy"
mini_desc = ("The 2026 Mac mini has 16 to 32 GB on M6 and up to 64 GB on M5 Pro. What each can run, from measured "
             "model sizes and speeds — and what we could not measure.")

posts = [
    (SLUG_SPEED, speed_title, speed_desc, speed_body),
    (SLUG_RAM, ram_title, ram_desc, ram_body),
    (SLUG_MINI, mini_title, mini_desc, mini_body),
]
cards = []
for slug, title, desc, body in posts:
    minutes = shell(slug, title, desc, body)
    cards.append((slug, title, desc, minutes))
    print(f"wrote blog/{slug}.html  ({minutes} min read)")

# blog index: newest first
index_path = os.path.join(SITE, "blog", "index.html")
index = open(index_path, encoding="utf-8").read()
block = "".join(
    f'        <a class="post-card" href="{slug}.html">\n          <div class="meta">{DATE} · {minutes} min read</div>\n'
    f'          <h3>{html.escape(title)}</h3>\n          <p>{html.escape(desc)}</p>\n        </a>\n'
    for slug, title, desc, minutes in cards)
for slug, *_ in cards:
    index = re.sub(r'        <a class="post-card" href="%s\.html">.*?</a>\n' % re.escape(slug), "", index, flags=re.S)
marker = '      <div class="post-list">\n'
assert index.count(marker) == 1
open(index_path, "w", encoding="utf-8").write(index.replace(marker, marker + block))

# llms.txt: same three at the top of the Blog section
llms_path = os.path.join(SITE, "llms.txt")
llms = open(llms_path, encoding="utf-8").read()
for slug, *_ in cards:
    llms = re.sub(r"^- .*%s\.html\n" % re.escape(slug), "", llms, flags=re.M)
lines = "".join(f"- {title}: {BASE}/blog/{slug}.html\n" for slug, title, _, _ in cards)
assert llms.count("## Blog\n") == 1
open(llms_path, "w", encoding="utf-8").write(llms.replace("## Blog\n", "## Blog\n" + lines))

print(json.dumps({"n_models": n_models, "drop_pct": drop_pct,
                  "gen": {s["name"]: round(s["gen"], 1) for s in S.values()}}, indent=1))
