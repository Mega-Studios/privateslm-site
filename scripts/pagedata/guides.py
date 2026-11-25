"""Guides: the best-apps list (audit #140), Apple Intelligence plus cloud models (#141),
free offline AI on iPhone (#142), and the fact sheet (#149).
"""

import json
import re
from pathlib import Path

from .common import (UPDATED, UPDATED_TEXT, APP_STORE, FREE_MODELS, FAMILIES, PRICE_LINE, CREDITS_LINE,
                     table, ul, p, h2, ext)
from .competitors import APPS, READ, store
from .models import CATALOG, MAKERS

ROOT = Path(__file__).resolve().parent.parent.parent

APPLE_PAGE = "https://support.apple.com/en-us/121115"
APPLE_DEVICES = ("iPhone 15 Pro and iPhone 15 Pro Max, iPhone 16 models or later, iPhone Air and iPhone Duo; iPad "
                 "mini with A17 Pro or A20 Pro and iPads with M1 or later; Macs with M1 or later and MacBook Neo")


# ---------- #140 ----------

BEST = [
    ("chatgpt", "most people, and anyone who wants OpenAI's newest features first",
     "The most used AI app, with a generous free tier, voice conversations, image generation and history on every "
     "device.", "OpenAI's models only."),
    ("claude", "writing, coding and thinking a problem through",
     "Anthropic's own app, with the newest Claude models first, research with citations and connectors to Google apps.",
     "Anthropic's models only; Claude Pro is $20 a month."),
    ("gemini", "people who live in Google's apps",
     "Gemini Live with the camera, Nano Banana image editing, and Gmail, Calendar and Photos in the chat.",
     "Google's models only; some features need a Google AI plan."),
    ("perplexity", "research with sources",
     "Every answer cites its sources; Pro Search and Deep Research go further.", "Built around search more than chat."),
    (None, "several makers' models in one chat, plus a free on-device model",
     f"GPT-6, Claude, Gemini, Grok, DeepSeek and more, switchable mid-chat; unlimited Apple Intelligence on supported "
     "devices; documents read on the device; no account. Pro is $9.99 a month.",
     "New, with very few ratings; fewer models than ChatNow or Poe; no sync between devices."),
    ("poe", "the widest choice of models and bots",
     "Many makers' models, image and video generators, and a million custom bots; several bots in one chat.",
     "Usage is counted in points, so how far a plan goes depends on the models you use."),
    ("chatnow", "the most models in one subscription, video included",
     "More than 30 models, side-by-side answers and video models like Veo 3.1 and Sora 2.", "Needs iOS 26."),
    ("fello", "work across Mac, iPhone and iPad",
     "Creates real PowerPoint, Excel, Word and PDF files, keeps Projects and syncs between devices.",
     "The yearly plan ($89.99) costs more than most."),
    ("grok", "xAI's models and Grok Imagine",
     "xAI's own app: web research, documents and photos, and image and video generation.", "xAI's models only."),
    ("locally", "fully offline, free open models",
     "Runs Llama, Gemma, Qwen and others on the device with Apple MLX; no login, no data collection.",
     "Small open models are far less capable than the cloud flagships; iPhone and iPad."),
]


def best_page():
    items, ld_items = [], []
    for i, (key, best_for, what, caveat) in enumerate(BEST, start=1):
        if key is None:
            name, url = "Omnimo", APP_STORE
            facts = (f"<em>Free to start; Pro {PRICE_LINE} One rating on the US App Store when we checked. We make "
                     "Omnimo.</em>")
        else:
            a = APPS[key]
            name, url = a["name"], store(key)
            facts = f"<em>{a['plans'][0].upper() + a['plans'][1:]}. Rated {a['rating']} from {a['ratings']} ratings.</em>"
        items.append(f"      <li><h3>{ext(url, name)}: best for {best_for}</h3>\n"
                     f"      <p>{what} <strong>Watch out:</strong> {caveat}</p>\n      <p>{facts}</p></li>")
        ld_items.append({"@type": "ListItem", "position": i, "name": name, "url": url})
    body = "\n".join([
        p("There is no single best AI chat app: the right one depends on which models you want, how you pay, and "
          "whether you need it to work offline. This list says what each app is best for and what to watch out for. "
          "It is written by the team that makes Omnimo, which is on the list, so we have tried to be especially fair "
          "to the others."),
        h2("The list"),
        '    <ol class="best">\n' + "\n".join(items) + "\n    </ol>",
        h2("Also popular"),
        p(f"{ext(store('chaton'), 'ChatOn')}, {ext(store('genie'), 'Genie')} and {ext(store('nova'), 'Nova')} are "
          "all-in-one AI apps with large followings, ready prompts, image tools and weekly plans; their listings name "
          f"models from several makers. {ext(store('private-llm'), 'Private LLM')} ($4.99 once) and "
          f"{ext(store('pocketpal'), 'PocketPal AI')} run open models fully offline. Comparisons: "
          '<a href="/compare/">Omnimo vs other apps</a>.'),
        h2("How we made this list"),
        ul([f"Prices are each app's US App Store list of in-app purchases, and ratings its US App Store rating, read on "
            f"{READ}. Apple lists in-app purchases without the billing period; where a listing doesn't say, neither "
            "do we.",
            "Features are what each app's own listing says, plus our own use of the apps.",
            "We ran no benchmarks, and the order is not a score: each app is placed by what it is best for.",
            "We make Omnimo. Nobody paid to be on this list."]),
        h2("Quick answers"),
        table(["If you want", "Look at"], [
            ["The newest OpenAI features", "ChatGPT"],
            ["GPT, Claude and Gemini for one price", "Omnimo, Poe, ChatNow, Fello AI"],
            ["Answers with sources", "Perplexity"],
            ["Something free that works offline", "Omnimo (Apple Intelligence), Locally AI, PocketPal AI"],
            ["Files made for you on the Mac", "Fello AI"],
        ]),
    ])
    return {
        "path": "best/ai-chat-apps-iphone-2026.html", "title": "The best AI chat apps for iPhone in 2026: an honest list",
        "description": "ChatGPT, Claude, Gemini, Perplexity, Omnimo, Poe, ChatNow, Fello AI, Grok and Locally AI: what "
                       "each AI chat app for iPhone is best for, what it costs in the US App Store, and what to watch out for.",
        "h1": "The best AI chat apps for iPhone in 2026", "meta": f"Updated {UPDATED_TEXT} · prices from the US App Store",
        "body": body, "md": True, "llms": "Guides",
        "extra_ld": [{"@context": "https://schema.org", "@type": "ItemList", "name": "AI chat apps for iPhone, 2026",
                      "itemListOrder": "https://schema.org/ItemListUnordered", "itemListElement": ld_items}],
        "faq": [("What is the best AI chat app for iPhone?",
                 "For most people, ChatGPT. For writing and coding, Claude; for Google's apps, Gemini; for research "
                 "with sources, Perplexity; for several makers' models in one app, Omnimo, Poe, ChatNow or Fello AI; "
                 "for free offline AI, an app that uses Apple Intelligence, or Locally AI."),
                ("Is there a free AI chat app that works offline on iPhone?",
                 "Yes. On iPhones with Apple Intelligence, apps such as Omnimo use Apple's on-device model, free and "
                 "offline. Locally AI and PocketPal AI run open models offline on any recent iPhone.")],
        "crumbs": [("Omnimo", "index.html"), ("Best AI chat apps for iPhone", "best/ai-chat-apps-iphone-2026.html")],
    }


# ---------- #141 ----------

def apple_plus_cloud_page():
    body = "\n".join([
        p("Apple Intelligence has a model that runs on your iPhone, iPad or Mac. It is free, private and works "
          "offline, but it is small. GPT, Claude and Gemini are much larger and run in the cloud. Omnimo puts both "
          "in one chat: start with Apple Intelligence, switch to GPT-6, Claude or Gemini when a question needs more, "
          "and switch back."),
        h2("How it works in Omnimo"),
        table(["", "Apple Intelligence", "GPT-6, Claude, Gemini and the rest"], [
            ["Where it runs", "On your device", "In the cloud, through Omnimo's server to the model's maker"],
            ["Price", "Free, unlimited", f"A few messages a day free ({FREE_MODELS}); every model on Omnimo Pro"],
            ["Internet", "Not needed", "Needed"],
            ["Your messages", "Never leave the device", "Sent to the model's maker to get the answer; Omnimo doesn't keep them"],
            ["Good for", "Short everyday tasks: rewriting, summaries, quick answers, translation",
             "Long documents, photos, hard questions, careful writing"],
        ]),
        p("In the same chat: when the free cloud messages run out, or the internet goes, the conversation can carry "
          "on with Apple Intelligence. Siri and Shortcuts (Ask, Summarize, Rephrase, Translate) use Apple "
          "Intelligence on the device."),
        h2("What you need"),
        p(f"Apple Intelligence in Omnimo needs iOS, iPadOS or macOS 26 on a device that supports it. Apple's list "
          f"({ext(APPLE_PAGE, 'Apple Intelligence requirements')}, read {UPDATED_TEXT}): {APPLE_DEVICES}. It also has "
          "to be turned on in Settings, and works in the languages Apple supports. On other devices, Omnimo works with "
          "the cloud models only."),
        h2("Other ways to get both"),
        ul(["<strong>Apple's own ChatGPT extension.</strong> On supported devices, Siri and Writing Tools can hand a "
            "request to ChatGPT, if you turn it on in Settings. It is built into the system, but it is ChatGPT only, "
            "and not a chat app.",
            f"<strong>{ext(store('allchat'), 'AllChat')}</strong>: its listing offers its own on-device models next "
            "to cloud models.",
            "<strong>Two apps.</strong> An offline app such as Locally AI next to ChatGPT, Claude or Gemini."]),
        p('More: <a href="/models/apple-intelligence.html">Apple Intelligence in Omnimo</a> · '
          '<a href="/models/">all the models</a>.'),
    ])
    return {
        "path": "guides/apple-intelligence-with-gpt-claude-gemini.html",
        "title": "An AI chat app with Apple Intelligence and GPT, Claude and Gemini — Omnimo",
        "description": "Omnimo puts Apple Intelligence, free and on your device, in the same chat as GPT-6, Claude, "
                       "Gemini and Grok. How it works, what you need, and the other ways to get both.",
        "h1": "Apple Intelligence and GPT, Claude and Gemini in one chat", "meta": f"Updated {UPDATED_TEXT}",
        "body": body, "md": True, "llms": "Guides",
        "faq": [("Is there an app that uses Apple Intelligence and ChatGPT, Claude and Gemini?",
                 "Yes. Omnimo has Apple Intelligence on the device and the GPT-6, Claude and Gemini models in the "
                 "cloud, in one chat. (It uses OpenAI's GPT models, not the ChatGPT app.)"),
                ("Can I switch from Apple Intelligence to Claude in the middle of a chat?",
                 "Yes. Pick another model from the menu at the top of the chat and ask again.")],
        "crumbs": [("Omnimo", "index.html"), ("Apple Intelligence with GPT, Claude and Gemini",
                                               "guides/apple-intelligence-with-gpt-claude-gemini.html")],
    }


# ---------- #142 ----------

def offline_page():
    body = "\n".join([
        p("Most AI apps need the internet: the model runs on a server. Two kinds of AI run on the iPhone itself, "
          "for free, and keep working in airplane mode: Apple Intelligence, already on supported iPhones, and small "
          "open models you download. Here is what each needs, and the honest catch."),
        h2("1. Apple Intelligence: nothing to download"),
        p(f"On a supported iPhone, Apple's on-device model is already there. Apps can use it through Apple's "
          "Foundation Models framework; Omnimo does, free and unlimited, and the chat never leaves the phone."),
        p(f"<strong>The catch: not every iPhone has it.</strong> Apple's list ({ext(APPLE_PAGE, 'Apple Intelligence requirements')}, "
          f"read {UPDATED_TEXT}): {APPLE_DEVICES}. Omnimo needs iOS 26 for it, Apple Intelligence has to be turned "
          "on in Settings, and it works only in the languages Apple supports. On other iPhones Omnimo still works, "
          "but only with its cloud models, which need the internet."),
        h2("2. Open models you download"),
        p(f"Apps like {ext(store('locally'), 'Locally AI')} (free), {ext(store('pocketpal'), 'PocketPal AI')} (free) "
          f"and {ext(store('private-llm'), 'Private LLM')} ($4.99 once) download an open model, such as Llama, Gemma "
          "or Qwen, and run it on the phone. They work on more iPhones than Apple Intelligence does."),
        p("<strong>The catch:</strong> a model is a download of hundreds of megabytes to several gigabytes, larger "
          "models need more memory than many phones have, and long answers warm the phone and use battery."),
        h2("What offline AI is good for, and what it isn't"),
        table(["Good for", "Not so good for"], [
            ["Rewriting, shortening and fixing a message", "Facts it might not know, or recent news"],
            ["Quick summaries and translations", "Long documents and hard reasoning"],
            ["Private notes you don't want to send anywhere", "Photos (Omnimo sends photo questions to a cloud model)"],
            ["Planes, trains and bad signal", "Anything where a mistake is costly: check it"],
        ]),
        p("A practical setup is both: offline for the everyday, a cloud model for the hard questions. In Omnimo they "
          "are in the same chat, and when the free cloud messages run out or the signal drops, the chat carries on "
          "with Apple Intelligence."),
        p('Omnimo used to be privateSLM, an app of the second kind. It changed in October 2026: '
          '<a href="/blog/privateslm-is-now-omnimo.html">what changed</a>.'),
    ])
    return {
        "path": "guides/free-offline-ai-iphone.html",
        "title": "Free offline AI on iPhone: Apple Intelligence and open models (2026)",
        "description": "Two ways to run AI on your iPhone for free, with no internet: Apple Intelligence, in apps like "
                       "Omnimo, and downloaded open models. Which iPhones support each, and the honest catch.",
        "h1": "Free offline AI on iPhone", "meta": f"Updated {UPDATED_TEXT}", "body": body, "md": True, "llms": "Guides",
        "faq": [("Can I use AI on my iPhone without the internet?",
                 "Yes, in two ways: Apple Intelligence on supported iPhones, in apps such as Omnimo, and apps that "
                 "download an open model, such as Locally AI or PocketPal AI."),
                ("Which iPhones can run Apple Intelligence?",
                 f"According to Apple ({UPDATED_TEXT}): iPhone 15 Pro and Pro Max, iPhone 16 models or later, iPhone "
                 "Air and iPhone Duo. In Omnimo it also needs iOS 26.")],
        "crumbs": [("Omnimo", "index.html"), ("Free offline AI on iPhone", "guides/free-offline-ai-iphone.html")],
    }


# ---------- #149 ----------

def home_software_ld():
    """The SoftwareApplication JSON-LD of the home page, so the two never disagree."""
    text = (ROOT / "index.html").read_text(encoding="utf-8")
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        data = json.loads(block)
        if data.get("@type") == "SoftwareApplication":
            return data
    raise SystemExit("index.html: no SoftwareApplication JSON-LD")


def facts_page():
    free = [m[1] for m in CATALOG if m[3] == "free"]
    pro = [m[1] for m in CATALOG if m[3] == "pro"]
    flag = [m[1] for m in CATALOG if m[3] == "premium"]
    body = "\n".join([
        p(f"One page with the facts about Omnimo, for journalists, reviewers and AI assistants. Checked against the app "
          f"(version 2.7.4) and its App Store listing on {UPDATED_TEXT}. If anything elsewhere disagrees with this "
          'page, this page is the newer one. A plain-text copy is at <a href="/facts.md">/facts.md</a>.'),
        h2("The app"),
        table(["", ""], [
            ["Name", "Omnimo: AI Chat &amp; Assistant"],
            ["App Store", f'<a href="{APP_STORE}">apps.apple.com/app/id6504996891</a> (id 6504996891), one app for '
                          "iPhone, iPad and Mac"],
            ["Formerly", "privateSLM, an offline chat app with downloadable open models. Renamed Omnimo in October "
                         "2026 (version 2.4); the downloadable models and the one-time model packs were retired then."],
            ["Not to be confused with", "Omni AI, Omnia, OMNI AI or the OMNI AI Keyboard"],
            ["Category", "AI chat (App Store: Utilities)"],
            ["Devices", "iPhone and iPad with iOS or iPadOS 17 or later, Mac with macOS 14 or later"],
            ["Languages", "46"],
            ["Website", "www.privateslm.dev (the domain keeps the old name)"],
            ["Contact", '<a href="/support.html">Support</a> · team@getmegabrain.com'],
        ]),
        h2("Models"),
        p(f"{len(CATALOG)} cloud models from {len(MAKERS)} makers, plus Apple Intelligence on the device. Families: "
          f"{FAMILIES}, plus Mistral, Llama and MiMo. Switch at any time, even mid-chat. Which models are offered can "
          'depend on the country. Details: <a href="/models/">the models in Omnimo</a>.'),
        table(["Plan", "Models"], [
            ["Free", ", ".join(free) + "; Apple Intelligence on the device"],
            ["Pro", ", ".join(pro)],
            ["Pro flagships", ", ".join(flag)],
        ]),
        h2("Prices and limits"),
        table(["", ""], [
            ["Free", "Unlimited Apple Intelligence on the device (supported devices and languages); a few cloud "
                     "messages a day with the free models; one image a day; web searches with a daily limit"],
            ["Omnimo Pro", f"Every model; hundreds of messages a day, with a smaller daily allowance for the flagships; "
                           f"long documents read in one go; image and video generation with credits included. {PRICE_LINE}"],
            ["Credits", f"For images and videos. {CREDITS_LINE}"],
            ["Trials", "3 days on the weekly plan, 1 week on the yearly plan"],
            ["Customers from before Omnimo", "People who bought privateSLM as a paid app, or a model pack, get Omnimo "
                                             "Pro at no charge until 31 October 2027."],
        ]),
        p("Exact daily numbers are set on Omnimo's server and can change without an app update; the app shows what is "
          "left. Prices in other countries differ, and the app shows the local price."),
        h2("Privacy"),
        ul(["No account, no ads, no tracking.",
            "Chat history is kept on the device. Chats with Apple Intelligence never leave it.",
            "A message to a cloud model goes through Omnimo's server to the company that makes the model, to get the "
            "answer. Omnimo does not keep chats.",
            "A photo goes to the model answering, without its location. Documents are read on the device; their text "
            "goes to the model picked.",
            "The description of an image or video goes to fal.ai, which runs the model.",
            "Usage statistics help improve the app and can be turned off in Settings.",
            'Policy: <a href="/privacy.html">privacy policy</a>.']),
        h2("Features"),
        ul(["Photos the model can see", "Documents: PDF, Word, Excel, PowerPoint, Pages and scans, read on the device",
            "Ask Web: answers with sources", "Image and video generation, photo filters",
            "Your own assistants and the tone of replies", "Voice input and spoken answers", "Chat history",
            "Siri and Shortcuts: Ask, Summarize, Rephrase, Translate, on the device", "A Home Screen widget"]),
        h2("Not affiliated"),
        p("Omnimo is an independent app. It is not affiliated with OpenAI, Anthropic, Google, xAI, DeepSeek, Moonshot, "
          "Alibaba, Zhipu, MiniMax, Mistral AI, Meta or Xiaomi; model names belong to their owners."),
        h2("Changes"),
        table(["Date", "What changed"], [
            ["2026-11-25", "This fact sheet published."],
            ["2026-11-18", "Lower prices in 115 storefronts, by purchasing power (the US price is unchanged)."],
            ["2026-11", "Version 2.7: photos in chat, Ask Web, image and video generation, photo filters, credit packs."],
            ["2026-10", "privateSLM renamed Omnimo (2.4): cloud models, Omnimo Pro."],
        ]),
    ])
    return {
        "path": "facts.html", "title": "Omnimo fact sheet: models, prices, limits and privacy",
        "description": "The facts about Omnimo (formerly privateSLM) in one place: the app, every model, free and Pro, "
                       "US prices, credits, devices and privacy. Checked " + UPDATED_TEXT + ".",
        "h1": "Omnimo fact sheet", "meta": f"Checked {UPDATED_TEXT} · Omnimo 2.7.4", "schema": "WebPage",
        "body": body, "md": True, "llms": "Facts", "updated": UPDATED,
        "extra_ld": [home_software_ld()],
        "crumbs": [("Omnimo", "index.html"), ("Fact sheet", "facts.html")],
    }


def pages():
    return [facts_page(), best_page(), apple_plus_cloud_page(), offline_page()]
