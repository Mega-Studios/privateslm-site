"""The translated pages (audit #134): the home page with its facts table and FAQ, and
five compare pages, in es, de, fr, pt-BR and ja, with hreflang between them and the
English pages. The words are in i18n_<lang>.py; the facts are the same as in English.
"""

import copy

from .common import APP_STORE, LANGS
from .competitors import APPS, store
from . import i18n_es, i18n_de, i18n_fr, i18n_pt, i18n_ja

TEXTS = {"es": i18n_es.T, "de": i18n_de.T, "fr": i18n_fr.T, "pt-BR": i18n_pt.T, "ja": i18n_ja.T}
CODES = ["en", "es", "de", "fr", "pt-BR", "ja"]
COMPARE_KEYS = ["chatgpt", "perplexity", "poe", "chaton", "genie"]
SLUG = {"chatgpt": "omnimo-vs-chatgpt", "perplexity": "omnimo-vs-perplexity", "poe": "omnimo-vs-poe",
        "chaton": "omnimo-vs-chaton", "genie": "omnimo-vs-genie"}


def localized(path_en: str, code: str) -> str:
    return path_en if code == "en" else f"{LANGS[code]['dir']}/{path_en}"


def alternates_for(path_en: str) -> dict:
    return {code: localized(path_en, code) for code in CODES}


def table(head, rows):
    out = ["    <table>"]
    if head:
        out.append("      <tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr>")
    for r in rows:
        out.append("      <tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    out.append("    </table>")
    return "\n".join(out)


def nav(code):
    items = "\n".join(f'      <a href="{h}">{l}</a>' for l, h in LANGS[code]["nav"])
    return (f'  <nav>\n    <a class="logo" href="/{LANGS[code]["dir"]}/">Omni<span>mo</span></a>\n'
            f'    <div class="links">\n{items}\n    </div>\n  </nav>')


def footer(code, alternates):
    links = "\n".join(f'    <a href="{h}">{l}</a>' for l, h in LANGS[code]["footer"])
    langs = " · ".join(
        f'<a href="/{p.replace("index.html", "")}" hreflang="{c}" lang="{c}">{LANGS[c]["name"]}</a>'
        for c, p in alternates.items() if c != code)
    return (f'  <footer>\n    <span>© 2026 Omnimo</span>\n    <span class="langs">{langs}</span>\n'
            f'    <span class="spacer"></span>\n{links}\n  </footer>')


def software_ld(code, home_ld, text):
    data = copy.deepcopy(home_ld)
    data["description"] = text
    data["inLanguage"] = LANGS[code]["code"]
    data["url"] = f"https://www.privateslm.dev/{LANGS[code]['dir']}/"
    data.pop("featureList", None)
    for offer in data.get("offers", []):
        offer.pop("description", None)
    return data


def home_page(code, home_ld):
    t = TEXTS[code]["home"]
    alts = alternates_for("index.html")
    stats = "\n".join(f'        <div class="stat"><div class="num">{n}</div><div class="label">{l}</div></div>'
                      for n, l in t["stats"])
    panels = []
    for kicker, h2, sub, button in t["panels"]:
        cta = f'\n      <div class="cta"><a class="btn" href="{button[1]}">{button[0]}</a></div>' if button else ""
        panels.append(f'  <section class="panel">\n    <div class="inner">\n      <div class="kicker">{kicker}</div>\n'
                      f'      <h2>{h2}</h2>\n      <p class="sub">{sub}</p>{cta}\n    </div>\n  </section>')
    faq = "\n".join(f"      <h3>{q}</h3>\n      <p>{a}</p>" for q, a in t["faq"])
    compares = "\n".join(
        f'        <li><a href="/{LANGS[code]["dir"]}/compare/{SLUG[k]}.html">'
        f'{TEXTS[code]["cmp"]["h1"].format(name=TEXTS[code]["cmp"]["apps"][k]["name"])}</a></li>' for k in COMPARE_KEYS)
    facts = "\n".join(f"        <tr><th>{a}</th><td>{b}</td></tr>" for a, b in t["facts"])
    raw = f"""{nav(code)}

  <section class="panel hero">
    <div class="inner">
      <a class="rename-note" href="/blog/privateslm-is-now-omnimo.html"><strong>{t['rename'][0]}</strong> <span>{t['rename'][1]}</span></a>
      <div class="kicker">{t['kicker']}</div>
      <h1>{t['h1']}</h1>
      <p class="sub">{t['sub']}</p>
      <div class="cta">
        <a class="btn solid" href="{APP_STORE}">{t['download']}</a>
        <a class="btn" href="#models">{t['see_models']}</a>
      </div>
      <div class="stats">
{stats}
      </div>
    </div>
  </section>

{panels[0].replace('<section class="panel">', '<section class="panel" id="models">', 1)}

{chr(10).join(panels[1:])}

  <section class="facts" id="facts">
    <div class="wrap">
    <article>
      <h2>{t['facts_h2']}</h2>
      <table>
{facts}
      </table>

      <h2>{LANGS[code]['faq']}</h2>
{faq}

      <h2 id="compare">{t['compare_h2']}</h2>
      <p>{t['compare_intro']}</p>
      <ul>
{compares}
      </ul>
      <p>{t['more']}</p>
      <div class="cta"><a class="btn solid" href="{APP_STORE}">{LANGS[code]['cta']}</a></div>
      <p class="fine">{LANGS[code]['fine']}</p>
    </article>
    </div>
  </section>

{footer(code, alts)}"""
    return {
        "path": f"{LANGS[code]['dir']}/index.html", "lang": code, "title": t["title"], "description": t["description"],
        "og_title": t["og_title"], "og_type": "website", "h1": t["og_title"], "schema": "WebPage", "raw": raw,
        "faq": t["faq"], "alternates": alts, "extra_ld": [software_ld(code, home_ld, t["ld_description"])],
    }


def compare_page(code, key):
    tt = TEXTS[code]
    c, a = tt["cmp"], tt["cmp"]["apps"][key]
    name = a["name"]
    path_en = f"compare/{SLUG[key]}.html"
    them_values = [a["maker"], a["models"], a["plans"], c["free_download"], c["not_listed"], a["listing"],
                   c["rating"].format(r=a["r"], n=a["n"], date=tt["date"])]
    rows = [[f"<strong>{label}</strong>", ours, theirs] for label, ours, theirs in zip(c["rows"], c["omnimo"], them_values)]
    link = f'<a href="{store(key)}" rel="noopener" target="_blank">{c["on_store"].format(name=name)}</a>'
    body = "\n".join([
        f"    <p>{a['intro']}</p>",
        f"\n    <h2>{c['side']}</h2>",
        table(["", "Omnimo", name], rows),
        f'    <p class="cite">{c["cite"].format(name=APPS[key]["name"], date=tt["date"])}</p>',
        f"\n    <h2>{c['them_better'].format(name=name)}</h2>",
        f"    <p>{a['them']}</p>",
        f"\n    <h2>{c['us_better']}</h2>",
        f"    <p>{a['us']}</p>",
        f"\n    <h2>{c['verdict']}</h2>",
        f"    <p>{c['choose'].format(name=name, why=a['pick_them'])}</p>",
        f"    <p>{c['choose'].format(name='Omnimo', why=a['pick_us'])}</p>",
        f"    <p>{c['try'].format(them=link, name=name)}</p>",
    ])
    home = f"{LANGS[code]['dir']}/index.html"
    return {
        "path": localized(path_en, code), "lang": code, "title": a["title"], "description": a["desc"],
        "h1": c["h1"].format(name=name), "meta": c["meta"].format(date=tt["date"]), "body": body, "faq": a["faq"],
        "alternates": alternates_for(path_en),
        "crumbs": [("Omnimo", home), (c["h1"].format(name=name), localized(path_en, code))],
    }


def pages(home_ld):
    out = []
    for code in TEXTS:
        out.append(home_page(code, home_ld))
        out.extend(compare_page(code, k) for k in COMPARE_KEYS)
    return out
