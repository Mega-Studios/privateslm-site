"""/compare/omnimo-vs-*.html (audit #130), the /compare/ hub and /alternatives/ (#131).

Fair to the other apps: every page says where the other app is the better choice,
and its facts come from its own listing (competitors.py), with the date.
"""

from .common import (UPDATED_TEXT, FREE_MODELS, FAMILIES, PRICE_LINE, table, cards, ul, p, h2, ext)
from .competitors import APPS, READ, store, rating

OMNIMO_PLANS = "Free; Omnimo Pro $6.99 a week (3-day trial), $9.99 a month, $39.99 a year (1-week trial)"
OMNIMO_MODELS = (f"{FAMILIES}: from several makers, switchable mid-chat, plus Apple Intelligence on the device")
OMNIMO_FREE = f"Unlimited Apple Intelligence on the device; a few messages a day with {FREE_MODELS}; one image a day"
OMNIMO_ONDEVICE = "Apple Intelligence, free, unlimited and offline (iOS, iPadOS or macOS 26 on a supported device)"
OMNIMO_RATING = "New: one rating on the US App Store when we checked"
OMNIMO_LISTING = ("photos the model can see, documents read on the device, Ask Web with sources, image and video "
                  "generation, your own assistants, voice, Siri and Shortcuts, a widget, 46 languages, no account")


def name(key):
    return APPS[key].get("short", APPS[key]["name"])


def compare_table(key, extra=()):
    them = APPS[key]
    rows = [
        ["Made by", "An independent developer", f"{them['maker']}"],
        ["Models", OMNIMO_MODELS, them["models"]],
        ["Price (US)", OMNIMO_PLANS, them["plans"]],
        ["Free to start", OMNIMO_FREE, "Free download" if them["id"] else "No free app; a paid license"],
        ["On-device model", OMNIMO_ONDEVICE, them.get("ondevice", "Not in its listing")],
        ["What the listing highlights", OMNIMO_LISTING, them["listing"]],
        ["App Store rating", OMNIMO_RATING, rating(key)],
        *extra,
    ]
    return table(["", "Omnimo", name(key)], rows)


COMPARES = [
    {
        "key": "chatgpt", "slug": "omnimo-vs-chatgpt",
        "title": "Omnimo vs ChatGPT (2026): one maker or several, honestly compared",
        "desc": "ChatGPT is OpenAI's own app; Omnimo puts GPT-6, Claude, Gemini, Grok and more in one chat, with free "
                "Apple Intelligence on the device. Prices, models and where each one is the better choice.",
        "intro": "ChatGPT is OpenAI's own app, and with 12.5 million ratings on the US App Store it is the one most "
                 "people start with. Omnimo is a smaller, independent app that puts models from several makers in "
                 "one chat, OpenAI's GPT-6 among them. They answer different questions: \"the best of OpenAI\" or "
                 "\"the right model for each question\".",
        "them": "OpenAI's newest models and features usually reach ChatGPT first, and Omnimo does not have all of "
                "them: Advanced Voice Mode, memory across chats, history synced between your phone, computer and the "
                "web. Its free tier is generous, its image generator is built in, and it has a far bigger track "
                "record. If you only ever use GPT, ChatGPT is the better app.",
        "us": "You are not limited to one maker: ask GPT-6, then Claude or Gemini the same question in the same chat. "
              "On a device with Apple Intelligence, Omnimo also has a free, unlimited model that works offline and "
              "sends nothing anywhere. There is no account, and Pro is $9.99 a month against $19.99 for ChatGPT Plus "
              "in the App Store, for models from several makers.",
        "pick_them": "you want OpenAI's latest features first, voice conversations, memory and your chats on every "
                     "device and the web.",
        "pick_us": "you want GPT, Claude and Gemini side by side for one subscription, a free on-device model, and "
                   "no account.",
        "faq": [
            ("Is Omnimo the same as ChatGPT?",
             "No. ChatGPT is OpenAI's own app. Omnimo is an independent app that offers OpenAI's GPT-6 models next to "
             "Claude, Gemini, Grok, DeepSeek and others. It is not affiliated with OpenAI."),
            ("Is Omnimo cheaper than ChatGPT Plus?",
             "Omnimo Pro is $9.99 a month in the US. ChatGPT Plus is $19.99 in the App Store's list of in-app "
             f"purchases ({READ}) and $20 a month on OpenAI's site (3 November 2026); ChatGPT Go is $8.00. "
             "The plans are not the same thing: Plus gives more of OpenAI's models and features, Omnimo Pro gives "
             "several makers' models with a daily allowance."),
            ("Can I use GPT-6 for free in Omnimo?",
             "GPT-6 Luna is one of Omnimo's free cloud models, with a few messages a day. GPT-6 Sol, Terra and Astra "
             "are part of Omnimo Pro."),
        ],
    },
    {
        "key": "perplexity", "slug": "omnimo-vs-perplexity",
        "title": "Omnimo vs Perplexity (2026): answer engine or model picker",
        "desc": "Perplexity answers with cited sources; Omnimo is a chat app with GPT-6, Claude, Gemini and Grok in "
                "one place and Apple Intelligence free on the device. An honest comparison with prices.",
        "intro": "Perplexity, like Omnimo, puts models from several makers behind one app. But Perplexity is built "
                 "around search: every answer comes with sources. Omnimo is built around choosing the model, with "
                 "web answers as one tool among several.",
        "them": "For research, Perplexity is the stronger app: cited sources on every answer, Pro Search and Deep "
                "Research, Labs for reports, and an assistant that can act for you. It has half a million ratings and "
                "apps on many platforms. Omnimo's Ask Web also answers with sources, but it is one tool with a daily "
                "limit, not the core of the app.",
        "us": "In Omnimo you choose the model, by name, and can switch in the middle of a chat. It reads your "
              "documents on the device, and it has Apple Intelligence free and offline on supported devices. Pro is "
              "$9.99 a month or $39.99 a year, against $20 a month for Perplexity Pro.",
        "pick_them": "most of your questions are research and you want sources on every answer.",
        "pick_us": "you mostly chat, write and ask about photos and documents, and want to pick the model yourself.",
        "faq": [
            ("Does Omnimo search the web like Perplexity?",
             "Omnimo has Ask Web, which answers with numbered sources. It has a daily limit, higher on Pro. "
             "Perplexity is built around search and has deeper research tools."),
            ("Which is cheaper, Omnimo Pro or Perplexity Pro?",
             f"In the US, Omnimo Pro is $9.99 a month or $39.99 a year. Perplexity Pro is $20.00 in the App Store's "
             f"list of in-app purchases ({READ}), which also lists it at $200.00."),
            ("Can I choose Claude or GPT in Omnimo?",
             "Yes. Omnimo lists every model by name, GPT-6, Claude, Gemini, Grok, DeepSeek and more, and you can "
             "switch at any time, even mid-chat."),
        ],
    },
    {
        "key": "poe", "slug": "omnimo-vs-poe",
        "title": "Omnimo vs Poe (2026): two multi-model apps, honestly compared",
        "desc": "Poe and Omnimo both put many AI models in one app. Poe has more models and custom bots; Omnimo has "
                "Apple Intelligence free on the device and a simpler plan. Prices and where each wins.",
        "intro": "Poe, from Quora, was one of the first apps to put many AI models in one place, and Omnimo does "
                 "the same thing on a smaller scale. The difference is mostly breadth against simplicity.",
        "them": "Poe has far more: models from many makers, image and video generators, and over a million custom "
                "bots, including ones you can build and share. You can bring several bots into one chat to compare "
                "answers. Its Basic plan starts at $4.99 a month, cheaper than Omnimo Pro.",
        "us": "Omnimo is simpler: one list of models, a daily allowance instead of points, and Apple Intelligence "
              "free and offline on supported devices. Documents are read on your device, there is no account, and "
              "Siri and Shortcuts work on the device. Pro at $9.99 a month includes every model in the app.",
        "pick_them": "you want the widest choice of models and bots, or to build your own bots.",
        "pick_us": "you want a short list of leading models, a free on-device model and no account.",
        "faq": [
            ("Does Omnimo use points like Poe?",
             "No. Omnimo gives a number of messages a day: a few on the free plan, hundreds on Pro. Flagship models "
             "count against a smaller daily allowance, and the most expensive ones count as more than one request."),
            ("Is Poe cheaper than Omnimo?",
             f"Poe Basic is $4.99 a month and Poe Plus $19.99 a month in the App Store's list ({READ}). Omnimo Pro is "
             "$9.99 a month, $6.99 a week or $39.99 a year in the US."),
            ("Can I make my own bot in Omnimo?",
             "You can make your own assistants, with a name, a purpose, an icon and instructions, and pick the tone of "
             "replies. They stay on your device; Omnimo has no public bot store like Poe."),
        ],
    },
    {
        "key": "chaton", "slug": "omnimo-vs-chaton",
        "title": "Omnimo vs ChatOn (2026): an honest comparison",
        "desc": "ChatOn and Omnimo are both AI chat apps for iPhone with several models. Prices from the App Store, "
                "the models each one names, and where each one is the better choice.",
        "intro": "ChatOn, from AIBY, is one of the most popular AI chat apps on the App Store, with 289,000 ratings. "
                 "Omnimo is much newer. Both offer more than one model; they differ in what they are built around.",
        "them": "ChatOn has a large library of ready prompts (100+), YouTube video summaries, an AI keyboard, and "
                "image and video generation from photos. It has years of reviews behind it and is rated 4.7.",
        "us": "Omnimo names every model and lets you pick: GPT-6, Claude, Gemini, Grok, DeepSeek and more, switchable "
              "mid-chat. Apple Intelligence on the device is free and unlimited, and documents are read on the "
              "device. Pro has a monthly plan at $9.99 besides the weekly and yearly ones.",
        "pick_them": "you want ready prompts, YouTube summaries and an AI keyboard.",
        "pick_us": "you want to choose the model yourself, a free on-device model and a monthly plan.",
        "faq": [
            ("Which models does ChatOn use?",
             "Its App Store listing says it is built on GPT-5, Gemini 3.5, Claude Sonnet 5 and Sonar. Omnimo lists "
             "GPT-6, Claude (Haiku, Sonnet, Opus, Fable), Gemini, Grok, DeepSeek, Kimi, Qwen, GLM and MiniMax."),
            ("How much is ChatOn compared with Omnimo?",
             f"ChatOn's in-app purchases include Premium at $6.99 and $7.99 a week and at $29.99 and $39.99 ({READ}). "
             "Omnimo Pro is $6.99 a week, $9.99 a month or $39.99 a year in the US."),
            ("Does Omnimo have a prompt library?",
             "Yes, on this site: the <a href=\"/prompts/\">prompt library</a> has ready prompts to copy into Omnimo."),
        ],
    },
    {
        "key": "genie", "slug": "omnimo-vs-genie",
        "title": "Omnimo vs Genie AI Chatbot (2026): an honest comparison",
        "desc": "Genie (Chatbot AI Assistant by AppNation) and Omnimo both offer several AI models on iPhone. Prices "
                "from the App Store, models, and where each one is the better choice.",
        "intro": "Genie, listed as \"Chatbot AI Assistant – Genie\" by AppNation, has 204,000 ratings on the US App "
                 "Store. Like Omnimo it brings models from several makers together; it puts more weight on "
                 "research and image tools.",
        "them": "Genie has Deep Thinking for hard problems, Deep Search reports, image generation and editing, and "
                "voice chat, plus a long track record and Family Sharing. Its listing names more image and video "
                "models than Omnimo has.",
        "us": "Omnimo has Apple Intelligence free and offline on the device, reads your documents on the device, "
              "needs no account. It names each model so you know which one is answering. Pro "
              "has a $9.99 monthly plan as well as $6.99 a week and $39.99 a year.",
        "pick_them": "you want deep-search reports and an image editor built around chat.",
        "pick_us": "you want to pick each model by name and a free on-device model.",
        "faq": [
            ("Which models does Genie use?",
             "Its listing names GPT, Gemini, Grok, Claude, DeepSeek, Perplexity Sonar, Kimi and GLM, plus image and "
             "video models. Omnimo offers GPT-6, Claude, Gemini, Grok, DeepSeek, Kimi, Qwen, GLM and MiniMax."),
            ("How much does Genie cost?",
             f"Its in-app purchases include Weekly Unlimited at $7.99, other weekly plans from $8.99 to $12.99 and "
             f"yearly plans at $39.99 and $99.99 ({READ}). Omnimo Pro is $6.99 a week, $9.99 a month or $39.99 a year "
             "in the US."),
            ("Does Omnimo work offline?",
             "Apple Intelligence does, on supported devices and languages. The cloud models need the internet."),
        ],
    },
    {
        "key": "nova", "slug": "omnimo-vs-nova",
        "title": "Omnimo vs Nova AI Chatbot (2026): an honest comparison",
        "desc": "Nova (AI Chatbot by ScaleUp) and Omnimo both offer several AI models on iPhone. Prices from the App "
                "Store, the models each one names, and where each one is the better choice.",
        "intro": "Nova, by ScaleUp, has 128,000 ratings on the US App Store and names six model families in its "
                 "listing. Omnimo names nine, plus Apple Intelligence on the device.",
        "them": "Nova has a polished onboarding, scan-and-solve for homework, Word and Excel files, voice mode and a "
                "long track record. Its listing says it supports more than 140 languages.",
        "us": "Omnimo lets you choose the model by name and switch mid-chat, has Apple Intelligence free and offline "
              "on supported devices, reads documents on the device, needs no account and has a Mac app.",
        "pick_them": "you like a guided app with scan-and-solve and don't mind not choosing the model.",
        "pick_us": "you want to pick the model yourself and have a free on-device model.",
        "faq": [
            ("Which models does Nova use?",
             "Its listing names GPT-5.6, Gemini 3.6 Flash, Claude Opus 5, Kimi K3, Grok 4.5 and DeepSeek V4 Pro."),
            ("How much is Nova?",
             f"Its in-app purchases include weekly plans from $4.99 to $7.99, Nova Premium at $9.99 and yearly plans at "
             f"$39.99 and $59.99 ({READ}). Omnimo Pro is $6.99 a week, $9.99 a month or $39.99 a year in the US."),
            ("Can Omnimo solve homework from a photo?",
             "Yes: take or choose a photo and ask. The photo goes to the model answering, without its location. See "
             "<a href=\"/use-cases/homework.html\">homework help</a>."),
        ],
    },
    {
        "key": "chatnow", "slug": "omnimo-vs-chatnow",
        "title": "Omnimo vs ChatNow (2026): an honest comparison",
        "desc": "ChatNow offers 30+ models including video; Omnimo offers GPT-6, Claude, Gemini, Grok and more with "
                "Apple Intelligence free on the device. Prices, models and where each one wins.",
        "intro": "ChatNow, by Tappz, is the closest app to Omnimo in idea: many named models in one subscription. "
                 "It is rated 4.8 from 148,000 ratings and offers more models than Omnimo does.",
        "them": "ChatNow has more: over 30 models, video models like Veo 3.1 and Sora 2, a mode that asks several "
                "models the same question side by side, and a Playground that builds small apps. It supports Family "
                "Sharing and has a large base of reviews.",
        "us": "Omnimo runs on older systems (iOS 17 and macOS 14; ChatNow needs iOS 26), has Apple Intelligence free "
              "and offline on supported devices, reads documents on the device and needs no account. Its monthly Pro "
              "plan is $9.99.",
        "pick_them": "you want the most models, video generation and side-by-side answers.",
        "pick_us": "you want a free on-device model, an app that runs on iOS 17, and a cheaper monthly plan.",
        "faq": [
            ("Does ChatNow have more models than Omnimo?",
             "Yes. ChatNow lists more than 30 models for chat, images and video. Omnimo has nine chat model families "
             "plus Apple Intelligence, and a smaller set of image and video models."),
            ("How much does ChatNow cost?",
             f"Its in-app purchases include AI Plus at $6.99, ChatNow Plus at $19.99 and yearly plans from $49.99 to "
             f"$79.99 ({READ}). Omnimo Pro is $6.99 a week, $9.99 a month or $39.99 a year in the US."),
            ("Can I compare two models in Omnimo?",
             "Switch models in the same chat and ask again: each answer shows which model wrote it. Omnimo does not "
             "show several answers side by side."),
        ],
    },
    {
        "key": "fello", "slug": "omnimo-vs-fello-ai",
        "title": "Omnimo vs Fello AI (2026): an honest comparison",
        "desc": "Fello AI and Omnimo both bring the leading AI models to iPhone, iPad and Mac. Fello creates Office "
                "files and syncs; Omnimo has Apple Intelligence free on the device. Prices and where each wins.",
        "intro": "Fello AI is a native app for Mac, iPhone and iPad with the leading models in one subscription. "
                 "Omnimo is too. Fello leans toward work: it makes documents for you.",
        "them": "Fello AI creates real PowerPoint, Excel, Word and PDF files from a chat, keeps work in Projects, "
                "syncs everything across Mac, iPhone and iPad, and has Deep Research and podcasts from documents. "
                "Its listing names more models, Gemini 4 among them.",
        "us": "Omnimo has Apple Intelligence free, unlimited and offline on supported devices, reads documents on "
              "the device and needs no account. Pro is cheaper: $9.99 a month and $39.99 a year, against $11.99 and "
              "$89.99 in Fello's list of in-app purchases.",
        "pick_them": "you want files made for you, Projects and sync between Mac and iPhone.",
        "pick_us": "you want a free on-device model and a cheaper yearly plan, and don't need sync.",
        "faq": [
            ("Does Omnimo sync chats between iPhone and Mac?",
             "No. Omnimo keeps chat history on each device. Fello AI syncs across Mac, iPhone and iPad."),
            ("How much is Fello AI?",
             f"Its in-app purchases are $4.99 a week, $11.99 a month, $24.99 a quarter and $89.99 a year ({READ}), "
             "with a free tier of limited daily messages. Omnimo Pro is $6.99 a week, $9.99 a month or $39.99 a year "
             "in the US."),
            ("Can Omnimo create a PowerPoint or Excel file?",
             "No. Omnimo reads PDF, Word, Excel, PowerPoint and Pages files and answers questions about them, but it "
             "does not create Office files."),
        ],
    },
    {
        "key": "allchat", "slug": "omnimo-vs-allchat",
        "title": "Omnimo vs AllChat (2026): an honest comparison",
        "desc": "AllChat combines several models' answers into one; Omnimo lets you pick the model and has Apple "
                "Intelligence free on the device. Prices, features and where each one wins.",
        "intro": "AllChat, by IQ Digital, takes a different approach to many models: by default it asks several at "
                 "once and combines their answers. Omnimo asks the one you pick.",
        "them": "AllChat's Consensus Mode, which sends your question to several models and builds one answer, shows "
                "where they agreed and differed. It also has Smart Routing, alerts, memory, a ChatGPT memory import "
                "and its own on-device models for offline use.",
        "us": "Omnimo speaks 46 languages (AllChat's listing has "
              "English only), and its on-device model is Apple Intelligence, which needs no download. Pro is $9.99 "
              "a month or $39.99 a year.",
        "pick_them": "you want several models to check each other's answers.",
        "pick_us": "you want an app in your language and to pick the model yourself.",
        "faq": [
            ("Does Omnimo combine answers from several models?",
             "No. Omnimo answers with the model you choose; you can switch and ask again in the same chat."),
            ("Do both apps work offline?",
             "Both have an on-device option. Omnimo uses Apple Intelligence on supported devices and languages; "
             "AllChat's listing says it offers on-device models for offline use."),
            ("How much is AllChat?",
             f"Its in-app purchases include Premium at $7.99 a week, Pro at $8.99 a month or $89.99 a year, and Max at "
             f"$17.99 a month or $179.99 a year ({READ}). Omnimo Pro is $6.99 a week, $9.99 a month or $39.99 a year "
             "in the US."),
        ],
    },
    {
        "key": "typingmind", "slug": "omnimo-vs-typingmind",
        "title": "Omnimo vs TypingMind (2026): app subscription or your own API keys",
        "desc": "TypingMind is a web chat interface for your own API keys, paid once; Omnimo is an iPhone, iPad and "
                "Mac app with the models included. Which fits whom.",
        "intro": "TypingMind and Omnimo solve the same problem, many models in one place, in opposite ways. "
                 "TypingMind is software you buy once and connect to the AI providers with your own API keys. "
                 "Omnimo includes the models: no keys, one subscription.",
        "them": "With TypingMind you pay once for the interface and then only for what you use, at the providers' "
                "own prices, with any model your keys reach. It stores data locally by default and has agents, "
                "plugins, prompts and a knowledge base. For a heavy or technical user it can be much more flexible.",
        "us": "Omnimo needs no API keys, accounts with providers or setup: install it and ask. It is a native iPhone, "
              "iPad and Mac app with a camera for photo questions, Siri and Shortcuts, a widget and Apple "
              "Intelligence free on the device. The price is fixed, with a free tier to start.",
        "pick_them": "you already have API keys, use AI heavily, and want to pay providers directly.",
        "pick_us": "you want a phone app that works without keys or setup.",
        "faq": [
            ("Do I need an API key for Omnimo?",
             "No. The models are included. A free plan gives a few cloud messages a day and unlimited Apple "
             "Intelligence; Omnimo Pro gives every model."),
            ("Is TypingMind an iPhone app?",
             "TypingMind is a web app that runs in the browser; it is not on the App Store."),
            ("Which is cheaper?",
             "It depends on use. TypingMind is a one-time license plus what the providers charge for your usage. "
             "Omnimo Pro is $6.99 a week, $9.99 a month or $39.99 a year in the US, models included."),
        ],
    },
]

TRANSLATED = {"omnimo-vs-chatgpt", "omnimo-vs-perplexity", "omnimo-vs-poe", "omnimo-vs-chaton", "omnimo-vs-genie"}


def compare_page(c, alternates=None):
    key = c["key"]
    them = name(key)
    body = "\n".join([
        p(c["intro"]),
        h2("Side by side"),
        compare_table(key),
        f'    <p class="cite">Omnimo: the app\'s App Store listing and its pricing (US). {APPS[key]["name"]}: '
        f'{"its App Store listing and list of in-app purchases, US storefront" if APPS[key]["id"] else "its website"}, '
        f'read {READ}. Prices in other countries differ.</p>',
        h2(f"Where {them} is better"),
        p(c["them"]),
        h2("Where Omnimo is better"),
        p(c["us"]),
        h2("The honest verdict"),
        p(f"<strong>Choose {them}</strong> if {c['pick_them']}",
          f"<strong>Choose Omnimo</strong> if {c['pick_us']}",
          f"Both are free to try: {ext(store(key), them + ' on the App Store' if APPS[key]['id'] else them)} and "
          f"<a href=\"https://apps.apple.com/app/id6504996891\">Omnimo on the App Store</a>. Omnimo is made by the "
          f"team that writes this site, so weigh this page accordingly; we have tried to say where {them} wins."),
    ])
    page = {
        "path": f"compare/{c['slug']}.html", "title": c["title"], "description": c["desc"],
        "h1": f"Omnimo vs {them}", "meta": f"Updated {UPDATED_TEXT} · prices from the US App Store",
        "body": body, "faq": c["faq"], "md": True, "llms": "Compare",
        "crumbs": [("Omnimo", "index.html"), ("Compare", "compare/index.html"), (f"Omnimo vs {them}", f"compare/{c['slug']}.html")],
    }
    if alternates:
        page["alternates"] = alternates
    return page


ARCHIVE = [
    ("/compare/private-llm-vs-privateslm.html", "Private LLM vs privateSLM"),
    ("/compare/pocketpal-ai-vs-privateslm.html", "PocketPal AI vs privateSLM"),
    ("/compare/private-llm-alternatives.html", "Private LLM alternatives (privateSLM era)"),
    ("/compare/offline-ai-chat-iphone.html", "Offline AI chat on iPhone (privateSLM era)"),
]


def hub():
    items = [(f"/compare/{c['slug']}.html", "Compare", f"Omnimo vs {name(c['key'])}", c["desc"]) for c in COMPARES]
    body = "\n".join([
        p("Side-by-side comparisons of Omnimo with other AI chat apps: what each costs in the US App Store, which "
          "models it names, and where each one is the better choice. Every page says where the other app wins."),
        cards(items),
        h2("More"),
        ul(['<a href="/alternatives/">Alternatives to ChatGPT Plus, Poe, ChatOn, Claude and Private LLM</a>',
            '<a href="/best/ai-chat-apps-iphone-2026.html">Best AI chat apps for iPhone in 2026</a>',
            '<a href="/models/">The models in Omnimo</a>']),
        h2("Archive: privateSLM"),
        p("These pages compare privateSLM, the offline app Omnimo used to be, and describe it as it was then: "
          "downloadable on-device models, no cloud. They are not a description of Omnimo."),
        ul([f'<a href="{h}">{t}</a>' for h, t in ARCHIVE]),
    ])
    return {
        "path": "compare/index.html", "title": "Compare Omnimo with other AI chat apps (2026)",
        "description": "Omnimo compared with ChatGPT, Perplexity, Poe, ChatOn, Genie, Nova, ChatNow, Fello AI, AllChat "
                       "and TypingMind: prices, models and where each app is the better choice.",
        "h1": "Compare Omnimo", "meta": f"Updated {UPDATED_TEXT}", "body": body, "schema": "CollectionPage",
        "crumbs": [("Omnimo", "index.html"), ("Compare", "compare/index.html")], "llms": "Compare",
    }


# ---------- /alternatives/ ----------

def option(key, best_for, note):
    a = APPS[key]
    link = ext(store(key), a["name"])
    return (f"<strong>{link}</strong> ({a['maker']}): best for {best_for}. {note} "
            f"<em>Price (US): {a['plans']}.</em>")


OMNIMO_OPTION = ("<strong><a href=\"https://apps.apple.com/app/id6504996891\">Omnimo</a></strong> (made by the team "
                 "behind this site): best for several makers' models in one chat. GPT-6, Claude, Gemini, Grok, DeepSeek "
                 "and more, switchable mid-chat, with Apple Intelligence free on the device and no account. "
                 f"<em>Price (US): free to start; {PRICE_LINE}</em>")

ALTERNATIVES = [
    {
        "slug": "chatgpt-plus", "of": "ChatGPT Plus",
        "title": "ChatGPT Plus alternatives (2026): six options and when each one fits",
        "desc": "Alternatives to ChatGPT Plus on iPhone: Claude Pro, Google AI Pro, Perplexity Pro, Poe, ChatGPT Go "
                "and Omnimo, with US prices and what each one is best for.",
        "intro": "ChatGPT Plus is $19.99 a month in the App Store ($20 on OpenAI's site). Most people looking for an "
                 "alternative want one of three things: a cheaper plan, a different maker's model, or several "
                 "makers' models for one price. Here are the honest options.",
        "options": [
            option("chatgpt", "staying with OpenAI for less", "ChatGPT Go, at $8.00 in the App Store's list, is "
                   "OpenAI's own cheaper plan: the simplest switch if you like ChatGPT and want to pay less."),
            option("claude", "writing, coding and long thinking", "Anthropic's own app, with Claude's newest models "
                   "first and connectors to Google Drive, Gmail and Calendar."),
            option("gemini", "people who live in Google's apps", "Gemini connects to Gmail, Calendar, Photos and "
                   "YouTube, and Google AI Pro includes Google storage."),
            option("perplexity", "research with sources", "Every answer comes with citations, and Pro adds deeper "
                   "research tools."),
            option("poe", "the widest choice", "Many models and a million custom bots, from $4.99 a month."),
            OMNIMO_OPTION,
        ],
        "faq": [
            ("What is the cheapest alternative to ChatGPT Plus?",
             f"Among the options here, Poe Basic is $4.99 a month and ChatGPT Go $8.00 in the US App Store ({READ}). "
             "Omnimo is free to start, with unlimited Apple Intelligence on supported devices, and Omnimo Pro is "
             "$9.99 a month."),
            ("Is there an app with ChatGPT, Claude and Gemini in one subscription?",
             "Yes, several: Omnimo, Poe, ChatNow and Fello AI among them. Omnimo offers OpenAI's GPT-6, Anthropic's "
             "Claude and Google's Gemini: the makers' models, used through pay-per-token APIs, not the ChatGPT app."),
        ],
    },
    {
        "slug": "poe", "of": "Poe",
        "title": "Poe alternatives (2026): apps with many AI models in one place",
        "desc": "Alternatives to Poe on iPhone and Mac: ChatNow, Fello AI, Omnimo, Perplexity and TypingMind, with "
                "US prices and what each is best for.",
        "intro": "Poe's appeal is choice: many models and bots in one app. If you want that with a different "
                 "pricing model, a native Mac app or an on-device model, these are the alternatives worth a look.",
        "options": [
            option("chatnow", "the most models, including video", "More than 30 models and side-by-side answers; "
                   "needs iOS 26."),
            option("fello", "work on Mac and iPhone", "Creates Office files, keeps Projects and syncs between devices."),
            OMNIMO_OPTION,
            option("perplexity", "research", "Answers with sources, with models from several makers behind it."),
            option("typingmind", "your own API keys", "A web interface you buy once; you pay the providers directly."),
        ],
        "faq": [
            ("Is there a Poe alternative without points?",
             "Omnimo counts messages a day instead of points: a few on the free plan, hundreds on Pro. TypingMind has "
             "no usage limits of its own: you pay the providers for what you use."),
            ("Which Poe alternative works offline?",
             "Omnimo's Apple Intelligence works offline on supported devices. AllChat's listing also offers on-device "
             "models. Apps such as Locally AI and PocketPal run open models fully offline."),
        ],
    },
    {
        "slug": "chaton", "of": "ChatOn",
        "title": "ChatOn alternatives (2026): AI chat apps for iPhone compared",
        "desc": "Alternatives to ChatOn: ChatGPT, Genie, Nova, ChatNow and Omnimo, with US App Store prices and what "
                "each one is best for.",
        "intro": "ChatOn is a popular all-in-one AI app. If you want a different set of models, a monthly plan or "
                 "an on-device model, here are the alternatives, with what their own listings say.",
        "options": [
            option("chatgpt", "OpenAI's own app", "The original, with a generous free tier and OpenAI's newest features."),
            option("genie", "research and images", "Deep Search reports, image editing and voice chat."),
            option("nova", "a guided app", "Scan-and-solve, Word and Excel files, voice mode."),
            option("chatnow", "the most models", "More than 30 models including video."),
            OMNIMO_OPTION,
        ],
        "faq": [
            ("Is there a ChatOn alternative with a monthly plan?",
             "Yes. Omnimo Pro has a monthly plan at $9.99 in the US, besides $6.99 a week and $39.99 a year. ChatGPT, "
             "Claude and Perplexity also sell monthly plans."),
            ("Which ChatOn alternative lets me choose the model?",
             "Omnimo, ChatNow, Poe and Fello AI all let you pick the model by name."),
        ],
    },
    {
        "slug": "claude-app", "of": "the Claude app",
        "title": "Claude app alternatives (2026): where else to use Claude, and other options",
        "desc": "Alternatives to the Claude app on iPhone: apps that also offer Claude, like Omnimo and Poe, and other "
                "assistants like ChatGPT, Gemini and Perplexity. US prices and honest notes.",
        "intro": "Anthropic's Claude app is the most direct way to use Claude, and Claude Pro is $20 a month. Some "
                 "people want Claude next to other models, a lower price, or Claude without an account. These are "
                 "the options.",
        "options": [
            ("<strong><a href=\"https://apps.apple.com/app/id6504996891\">Omnimo</a></strong> (made by the team "
             "behind this site): Claude next to other makers' models. Claude Haiku 5.5 is free (a few messages a day); "
             "Claude Sonnet 5.5, Opus 5.5 and Fable 5.1 are in Omnimo Pro, next to GPT-6, Gemini and Grok. No account. "
             f"<em>Price (US): free to start; {PRICE_LINE}</em> See <a href=\"/models/claude-sonnet.html\">Claude in "
             "Omnimo</a>."),
            option("poe", "Claude among many bots", "Poe offers Anthropic's models among many others."),
            option("chatgpt", "OpenAI's models", "The most used assistant, with voice and memory."),
            option("gemini", "Google's apps", "Gemini with Gmail, Calendar and Photos."),
            option("perplexity", "research with sources", "Citations on every answer."),
        ],
        "faq": [
            ("Can I use Claude without the Claude app?",
             "Yes. Apps such as Omnimo and Poe offer Anthropic's Claude models; Omnimo uses Anthropic's API. Features of "
             "Anthropic's own app, such as projects and connectors, are only in the Claude app."),
            ("Is Claude free in Omnimo?",
             "Claude Haiku 5.5 is one of Omnimo's free cloud models, with a few messages a day. Sonnet, Opus and Fable "
             "are part of Omnimo Pro."),
        ],
    },
    {
        "slug": "private-llm", "of": "Private LLM",
        "title": "Private LLM alternatives (2026): on-device AI for iPhone and Mac",
        "desc": "Alternatives to Private LLM for on-device AI: Locally AI, PocketPal AI, Apple Intelligence in "
                "Omnimo, and AllChat. What runs offline, what it costs, and honest caveats.",
        "intro": "Private LLM runs open models entirely on your iPhone, iPad or Mac for $4.99, once. If you want "
                 "the same thing, offline and private, or something lighter, here are the options. One note first: "
                 "Omnimo was privateSLM, an offline app like Private LLM, until October 2026. It is now a cloud AI "
                 "app with Apple Intelligence on the device, so it is an alternative only if Apple's on-device model "
                 "is enough for you.",
        "options": [
            option("locally", "free open models on iPhone and iPad", "Runs Llama, Gemma, Qwen and others with Apple "
                   "MLX; no login."),
            option("pocketpal", "choosing any GGUF model", "Search Hugging Face from the app and run what you "
                   "download."),
            ("<strong><a href=\"https://apps.apple.com/app/id6504996891\">Omnimo</a></strong> (made by the team "
             "behind this site): Apple Intelligence free, unlimited and offline, with nothing to download, on iOS, "
             "iPadOS or macOS 26 on a supported device. Everything else in Omnimo is cloud models, which need the "
             "internet. <em>Price (US): free; Pro for the cloud models from $6.99 a week.</em>"),
            option("allchat", "cloud and on-device in one app", "Its listing offers on-device models for offline use "
                   "next to cloud models."),
        ],
        "faq": [
            ("Is Omnimo still an offline app?",
             "Only partly. Apple Intelligence runs on your device and works offline, on devices and languages that "
             "support it. The downloadable open models of privateSLM were retired in October 2026; the other models "
             "in Omnimo are cloud models."),
            ("What is the best free offline AI app for iPhone?",
             "If your iPhone has Apple Intelligence, Apple's model is already on it, and apps like Omnimo use it with "
             "nothing to download. For open models, Locally AI and PocketPal AI are free downloads. See "
             "<a href=\"/guides/free-offline-ai-iphone.html\">free offline AI on iPhone</a>."),
        ],
    },
]


def alternative_page(a):
    body = "\n".join([
        p(a["intro"]),
        h2("The options"),
        "    <ol>\n" + "\n".join(f"      <li>{o}</li>" for o in a["options"]) + "\n    </ol>",
        f'    <p class="cite">Ratings, prices and features: each app\'s US App Store listing and list of in-app '
        f'purchases, read {READ}. The App Store lists in-app purchases without their billing period; where a '
        f'listing doesn\'t say, neither do we.</p>',
        h2("How we chose"),
        p("We list apps we have looked at closely, with what their own listings say. We make Omnimo, so it is on "
          "every list; we have tried to say plainly when another app is the better choice."),
    ])
    return {
        "path": f"alternatives/{a['slug']}.html", "title": a["title"], "description": a["desc"],
        "h1": f"Alternatives to {a['of']}", "meta": f"Updated {UPDATED_TEXT} · prices from the US App Store",
        "body": body, "faq": a["faq"], "md": True, "llms": "Alternatives",
        "crumbs": [("Omnimo", "index.html"), ("Alternatives", "alternatives/index.html"),
                   (f"Alternatives to {a['of']}", f"alternatives/{a['slug']}.html")],
    }


def alternatives_hub():
    items = [(f"/alternatives/{a['slug']}.html", "Alternatives", f"Alternatives to {a['of']}", a["desc"])
             for a in ALTERNATIVES]
    return {
        "path": "alternatives/index.html", "title": "Alternatives to popular AI chat apps (2026)",
        "description": "Honest alternatives to ChatGPT Plus, Poe, ChatOn, the Claude app and Private LLM, with US "
                       "prices and what each option is best for.",
        "h1": "Alternatives", "meta": f"Updated {UPDATED_TEXT}", "schema": "CollectionPage",
        "body": p("Looking for something other than the app you use now? Each page lists the realistic options, "
                  "what they cost in the US App Store and what each one is best for.") + "\n" + cards(items),
        "crumbs": [("Omnimo", "index.html"), ("Alternatives", "alternatives/index.html")], "llms": "Alternatives",
    }


def pages(alternates_for):
    out = [hub(), alternatives_hub()]
    for c in COMPARES:
        out.append(compare_page(c, alternates_for(f"compare/{c['slug']}.html") if c["slug"] in TRANSLATED else None))
    out.extend(alternative_page(a) for a in ALTERNATIVES)
    return out
