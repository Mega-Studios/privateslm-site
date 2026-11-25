"""Shared facts and layout bits for the generated pages.

Omnimo's facts here match the home page's "at a glance" table, its FAQ and JSON-LD,
and llms.txt. Sources in the app repo (Mega-Studios/omnimo, main at 67db037):
appstore/metadata/en-US/, docs/monetization.md, gateway/src/catalog.ts and
gateway/src/comparison.ts. Message counts are not given as numbers ("a few a day",
"hundreds a day"), as in the App Store listing: they change with a gateway deploy.
"""

SITE = "https://www.privateslm.dev"
UPDATED = "2026-11-25"
UPDATED_TEXT = "November 25, 2026"
APP_STORE = "https://apps.apple.com/app/id6504996891"

# What the free tier's cloud models are called on the site (gateway/src/catalog.ts, tier "free").
FREE_MODELS = "GPT-6 Luna, Claude Haiku 5.5, Gemini 3.1 Flash-Lite, DeepSeek V4 Flash and Qwen 3.8 Flash"
FAMILIES = "GPT-6, Claude, Gemini, Grok, DeepSeek, Kimi, Qwen, GLM and MiniMax"

PRICE_LINE = ("$6.99 a week (3-day free trial), $9.99 a month or $39.99 a year (1-week free trial). "
              "US prices; the app shows the price for your country.")
CREDITS_LINE = "300 for $4.99, 700 for $9.99, 1600 for $19.99; bought credits never expire."

FINE_EN = ("Model and app names belong to their owners. Omnimo is an independent app and is not affiliated "
           "with OpenAI, Anthropic, Google, xAI, DeepSeek, Moonshot, Alibaba, Zhipu, MiniMax, Mistral AI, Meta "
           "or Xiaomi, or with the other apps named on this site. AI can make mistakes; check important answers.")

EN_NAV = [("Models", "/models/"), ("Compare", "/compare/"), ("Prompts", "/prompts/"),
          ("Blog", "/blog/"), ("App Store", APP_STORE)]
EN_FOOTER = [("Home", "/"), ("Facts", "/facts.html"), ("Models", "/models/"), ("Compare", "/compare/"),
             ("Alternatives", "/alternatives/"), ("Use cases", "/use-cases/"), ("Prompts", "/prompts/"),
             ("Status", "/status/"), ("Blog", "/blog/"), ("Support", "/support.html"),
             ("Privacy", "/privacy.html"), ("App Store", APP_STORE)]


def _intl(code, name, og, directory, compare, support, cta, faq, fine, home_label, english):
    return {
        "code": code, "name": name, "og": og, "dir": directory, "home": f"/{directory}/",
        "nav": [(compare, f"/{directory}/#compare"), (support, "/support.html"), ("App Store", APP_STORE)],
        "footer": [(home_label, f"/{directory}/"), (english, "/"), (support, "/support.html"),
                   ("Privacy", "/privacy.html"), ("App Store", APP_STORE)],
        "cta": cta, "faq": faq, "fine": fine,
    }


LANGS = {
    "en": {"code": "en", "name": "English", "og": "en_US", "dir": "", "home": "/", "nav": EN_NAV,
           "footer": EN_FOOTER, "cta": "Get Omnimo — free", "faq": "Questions", "fine": FINE_EN},
    "es": _intl("es", "Español", "es_ES", "es", "Comparativas", "Soporte", "Descarga Omnimo gratis",
                "Preguntas",
                "Los nombres de modelos y apps pertenecen a sus dueños. Omnimo es una app independiente y no está "
                "afiliada a OpenAI, Anthropic, Google, xAI, DeepSeek, Moonshot, Alibaba, Zhipu ni MiniMax, ni a las "
                "demás apps que se mencionan. La IA puede equivocarse; comprueba las respuestas importantes.",
                "Inicio", "English"),
    "de": _intl("de", "Deutsch", "de_DE", "de", "Vergleiche", "Support", "Omnimo kostenlos laden",
                "Fragen",
                "Modell- und App-Namen gehören ihren Inhabern. Omnimo ist eine unabhängige App und nicht mit OpenAI, "
                "Anthropic, Google, xAI, DeepSeek, Moonshot, Alibaba, Zhipu oder MiniMax verbunden, auch nicht mit "
                "den anderen hier genannten Apps. KI kann Fehler machen; prüfe wichtige Antworten.",
                "Start", "English"),
    "fr": _intl("fr", "Français", "fr_FR", "fr", "Comparatifs", "Assistance", "Télécharger Omnimo gratuitement",
                "Questions",
                "Les noms des modèles et des apps appartiennent à leurs propriétaires. Omnimo est une app "
                "indépendante, sans lien avec OpenAI, Anthropic, Google, xAI, DeepSeek, Moonshot, Alibaba, Zhipu "
                "ou MiniMax, ni avec les autres apps citées. L’IA peut se tromper ; vérifiez les réponses importantes.",
                "Accueil", "English"),
    "pt-BR": _intl("pt-BR", "Português (Brasil)", "pt_BR", "pt-br", "Comparações", "Suporte",
                   "Baixe o Omnimo grátis", "Perguntas",
                   "Os nomes de modelos e apps pertencem aos seus donos. O Omnimo é um app independente, sem vínculo "
                   "com OpenAI, Anthropic, Google, xAI, DeepSeek, Moonshot, Alibaba, Zhipu ou MiniMax, nem com os "
                   "outros apps citados. A IA pode errar; confira as respostas importantes.",
                   "Início", "English"),
    "ja": _intl("ja", "日本語", "ja_JP", "ja", "比較", "サポート", "Omnimoを無料で入手", "よくある質問",
                "モデル名とアプリ名は各所有者に帰属します。OmnimoはOpenAI、Anthropic、Google、xAI、DeepSeek、Moonshot、"
                "Alibaba、Zhipu、MiniMax、およびここで挙げた他のアプリとは提携していない独立したアプリです。"
                "AIは間違えることがあります。重要な回答は確認してください。",
                "ホーム", "English"),
}


def table(head, rows, wide=False) -> str:
    """A table; head is a list of header cells, rows a list of lists (HTML allowed)."""
    lines = ["    <table>", "      <tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr>"]
    for row in rows:
        lines.append("      <tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>")
    lines.append("    </table>")
    out = "\n".join(lines)
    if wide:
        out = '    <div class="table-scroll">\n' + out + "\n    </div>"
    return out


def cards(items) -> str:
    """A list of linked cards: items are (href, kicker, title, text)."""
    out = ['    <div class="post-list">']
    for href, kicker, title, text in items:
        out.append(f'      <a class="post-card" href="{href}"><div class="meta">{kicker}</div>'
                   f"<h3>{title}</h3><p>{text}</p></a>")
    out.append("    </div>")
    return "\n".join(out)


def ul(items) -> str:
    return "    <ul>\n" + "\n".join(f"      <li>{i}</li>" for i in items) + "\n    </ul>"


def p(*paras) -> str:
    return "\n".join(f"    <p>{x}</p>" for x in paras)


def h2(text) -> str:
    return f"\n    <h2>{text}</h2>"


def ext(url, label) -> str:
    return f'<a href="{url}" rel="noopener" target="_blank">{label}</a>'


# The block every Omnimo-facing page can reuse: what Omnimo is, in one table.
def omnimo_facts_rows():
    return [
        ["Models", f"{FAMILIES}, plus Apple Intelligence on the device. Switch at any time, even mid-chat. "
                   "Which models are offered can depend on your country. <a href=\"/models/\">All models</a>"],
        ["Free", "Apple Intelligence on the device: unlimited, offline, nothing leaves the device (supported "
                 f"devices and languages). A few messages a day with {FREE_MODELS}. One image a day."],
        ["Omnimo Pro", "Every model, flagships included; hundreds of messages a day; long documents read in one go; "
                       f"image and video generation with credits included. {PRICE_LINE}"],
        ["Privacy", "No account, no ads, no tracking. Chat history stays on the device. A message to a cloud model "
                    "goes through Omnimo's server to the model's maker and is not kept. "
                    "<a href=\"/privacy.html\">Privacy policy</a>"],
        ["Devices", "iPhone and iPad with iOS 17 or later, Mac with macOS 14 or later. Apple Intelligence needs "
                    "iOS, iPadOS or macOS 26 on a supported device."],
    ]
