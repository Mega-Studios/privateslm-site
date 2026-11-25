"""/status/ (audit #137): "Is ChatGPT / Claude / Gemini down?" explainers.

Static pages. They show no live status, because a static page can't know it: they
link to the makers' official status pages (checked to load on 25 November 2026) and
explain what to try. Omnimo uses the makers' models through APIs, so an outage of a
maker's API can affect that maker's models in Omnimo too; the pages say so.
"""

from .common import UPDATED_TEXT, ul, p, h2, ext, cards

SERVICES = [
    {
        "slug": "is-chatgpt-down", "name": "ChatGPT", "maker": "OpenAI", "family": "GPT-6",
        "status": [("https://status.openai.com", "status.openai.com"),],
        "status_note": "OpenAI's status page shows ChatGPT, the API and OpenAI's other services separately, with current "
                       "incidents and their history.",
        "alt": "Claude, Gemini, Grok or DeepSeek", "model_page": "/models/gpt-6.html",
    },
    {
        "slug": "is-claude-down", "name": "Claude", "maker": "Anthropic", "family": "Claude",
        "status": [("https://status.claude.com", "status.claude.com")],
        "status_note": "Anthropic's status page (status.anthropic.com leads there too) shows claude.ai, the Claude "
                       "API and Claude's other services, with current incidents and their history.",
        "alt": "GPT-6, Gemini, Grok or DeepSeek", "model_page": "/models/claude-sonnet.html",
    },
    {
        "slug": "is-gemini-down", "name": "Gemini", "maker": "Google", "family": "Gemini",
        "status": [("https://www.google.com/appsstatus/dashboard/", "Google Workspace Status Dashboard (the Gemini app)"),
                   ("https://aistudio.google.com/status", "Google AI Studio status (the Gemini API)")],
        "status_note": "Google reports the Gemini app on the Google Workspace Status Dashboard, and the Gemini API "
                       "on Google AI Studio's status page.",
        "alt": "GPT-6, Claude, Grok or DeepSeek", "model_page": "/models/gemini.html",
    },
]


def page(s):
    links = ul([ext(u, label) for u, label in s["status"]])
    body = "\n".join([
        p(f"<strong>This page can't tell you whether {s['name']} is down right now</strong>: it is a static page. "
          f"The answer is on {s['maker']}'s official status page:"),
        links,
        p(s["status_note"]),
        h2("If the status page says everything is fine"),
        p(f"Then the problem is probably closer to you. In order, try:"),
        "    <ol>\n"
        "      <li>Another network: switch between Wi-Fi and mobile data, or turn off a VPN.</li>\n"
        f"      <li>Signing out and in again, or closing and reopening the {s['name']} app.</li>\n"
        f"      <li>Updating the app, or trying {s['name']} on the web from another device.</li>\n"
        "      <li>A shorter message: a very long conversation or file can fail when a short one works.</li>\n"
        f"      <li>Waiting a few minutes: many problems are short and don't reach the status page.</li>\n"
        "    </ol>",
        h2(f"If {s['name']} is down"),
        p(f"An outage usually affects one maker at a time. Another maker's model can carry on in the meantime: in "
          f"Omnimo you can switch from {s['family']} to {s['alt']} in the same chat, and on supported devices Apple "
          "Intelligence answers on the device with no internet at all."),
        p(f"To be clear about what this does and doesn't fix: Omnimo reaches {s['maker']}'s models through an API. When "
          f"{s['maker']}'s API is down, {s['family']} in Omnimo can be down too; the other makers' models are not "
          f"affected. When only the {s['name']} app or website is down, the API often still works. "
          f"<a href=\"{s['model_page']}\">{s['family']} in Omnimo</a>."),
    ])
    return {
        "path": f"status/{s['slug']}.html",
        "title": f"Is {s['name']} down? Where to check, and what to try — Omnimo",
        "description": f"How to check whether {s['name']} is down on {s['maker']}'s official status page, what to try "
                       "when it isn't, and how to keep working with another model when it is.",
        "h1": f"Is {s['name']} down?", "meta": f"Updated {UPDATED_TEXT} · an explainer, not a live status page",
        "body": body, "md": True, "llms": "Status explainers",
        "faq": [(f"How do I know if {s['name']} is down?",
                 f"Check {s['maker']}'s official status page, listed on this page. It shows current incidents for "
                 f"{s['name']} and its API."),
                (f"What can I use while {s['name']} is down?",
                 f"Another maker's model. In Omnimo you can switch to {s['alt']} in the same chat; on a device with "
                 "Apple Intelligence, it answers on the device without the internet.")],
        "crumbs": [("Omnimo", "index.html"), ("Status", "status/index.html"), (f"Is {s['name']} down?", f"status/{s['slug']}.html")],
    }


def hub():
    items = [(f"/status/{s['slug']}.html", "Explainer", f"Is {s['name']} down?",
              f"Where to check {s['maker']}'s official status, and what to try.") for s in SERVICES]
    return {
        "path": "status/index.html", "title": "Is ChatGPT, Claude or Gemini down? Official status pages — Omnimo",
        "description": "Where to find the official status pages of ChatGPT, Claude and Gemini, and what to try when an "
                       "AI service isn't answering.",
        "h1": "Is it down?", "meta": f"Updated {UPDATED_TEXT}", "schema": "CollectionPage",
        "body": p("These pages don't show live status. They point to each maker's official status page and explain "
                  "what to try.") + "\n" + cards(items),
        "crumbs": [("Omnimo", "index.html"), ("Status", "status/index.html")], "llms": "Status explainers",
    }


def pages():
    return [hub()] + [page(s) for s in SERVICES]
