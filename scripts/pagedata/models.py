"""/models/ (audit #132): the models Omnimo offers, and model-vs-model pages (#148).

The list is gateway/src/catalog.ts in the app repo (main at 67db037, 25 November
2026). CATALOG below is a trimmed copy of catalog.ts: it keeps only what the pages show, the
tier, the longest prompt the gateway accepts (`context`) and whether the model can see
a photo (`vision`). The catalog's other fields are internal and stay out of this
public repo. No benchmark scores: we have not run
any, and the makers' own numbers are theirs to publish.
"""

from .common import UPDATED_TEXT, PRICE_LINE, table, cards, ul, p, h2, ext

# id, name, maker, tier, context (tokens), vision
CATALOG = [
    ("gpt-6-luna", "GPT-6 Luna", "openai", "free", 64000, True),
    ("claude-haiku-5.5", "Claude Haiku 5.5", "anthropic", "free", 64000, True),
    ("gemini-3.1-flash-lite", "Gemini 3.1 Flash-Lite", "google", "free", 64000, True),
    ("deepseek-v4-flash", "DeepSeek V4 Flash", "deepseek", "free", 64000, False),
    ("qwen-3.8-flash", "Qwen 3.8 Flash", "qwen", "free", 64000, True),
    ("deepseek-v4-pro", "DeepSeek V4 Pro", "deepseek", "pro", 64000, False),
    ("glm-5.3", "GLM 5.3", "zhipu", "pro", 64000, False),
    ("minimax-m3", "MiniMax M3", "minimax", "pro", 64000, True),
    ("glm-5.3-flash", "GLM 5.3 Flash", "zhipu", "pro", 64000, True),
    ("deepseek-v4.1-flash", "DeepSeek V4.1 Flash", "deepseek", "pro", 64000, True),
    ("minimax-m3.1-flash", "MiniMax M3.1 Flash", "minimax", "pro", 64000, True),
    ("mistral-small", "Mistral Small", "mistral", "pro", 64000, True),
    ("llama-4-maverick", "Llama 4 Maverick", "meta", "pro", 64000, True),
    ("gemini-3.5-flash-lite", "Gemini 3.5 Flash-Lite", "google", "pro", 64000, True),
    ("qwen-3.7-plus", "Qwen 3.7 Plus", "qwen", "pro", 64000, True),
    ("mimo-v2.6-pro", "MiMo V2.6 Pro", "xiaomi", "pro", 64000, True),
    ("mistral-large-4", "Mistral Large 4", "mistral", "pro", 64000, True),
    ("gpt-6-sol", "GPT-6 Sol", "openai", "premium", 48000, True),
    ("gpt-6.1-sol", "GPT-6.1 Sol", "openai", "premium", 48000, True),
    ("gpt-6.1-terra", "GPT-6.1 Terra", "openai", "premium", 48000, True),
    ("claude-sonnet-5.5", "Claude Sonnet 5.5", "anthropic", "premium", 48000, True),
    ("gemini-3.5-flash", "Gemini 3.5 Flash", "google", "premium", 48000, True),
    ("gemini-3.8-flash", "Gemini 3.8 Flash", "google", "premium", 48000, True),
    ("gemini-3.1-pro", "Gemini 3.1 Pro", "google", "premium", 48000, True),
    ("grok-4.7", "Grok 4.7", "xai", "premium", 48000, True),
    ("grok-4.3", "Grok 4.3", "xai", "premium", 48000, True),
    ("kimi-k3", "Kimi K3", "moonshot", "premium", 48000, True),
    ("kimi-k3.1-pro", "Kimi K3.1 Pro", "moonshot", "premium", 48000, True),
    ("qwen-3.8-max", "Qwen 3.8 Max", "qwen", "premium", 48000, True),
    ("claude-opus-5.5", "Claude Opus 5.5", "anthropic", "premium", 32000, True),
    ("claude-fable-5.1", "Claude Fable 5.1", "anthropic", "premium", 24000, True),
    ("gpt-6-astra", "GPT-6 Astra", "openai", "premium", 24000, True),
]

MAKERS = {
    "openai": "OpenAI", "anthropic": "Anthropic", "google": "Google", "xai": "xAI", "deepseek": "DeepSeek",
    "qwen": "Alibaba (Qwen)", "moonshot": "Moonshot AI", "minimax": "MiniMax", "zhipu": "Zhipu (Z.ai)",
    "mistral": "Mistral AI", "meta": "Meta", "xiaomi": "Xiaomi",
}
# gateway/src/catalog.ts RESTRICTED_VENDORS: hidden in some countries.
RESTRICTED = {"openai", "anthropic", "google", "mistral", "meta"}

TIER = {"free": "Free and Pro", "pro": "Pro", "premium": "Pro flagship"}


def rows(models):
    out = []
    for m in models:
        out.append([f"<strong>{m[1]}</strong>", MAKERS[m[2]], TIER[m[3]],
                    f"~{m[4] // 1000}K tokens", "Yes" if m[5] else "No"])
    return out


HEAD = ["Model", "Maker", "Plan", "Longest prompt", "Photos"]

HOW = ("<strong>How the allowance works.</strong> Free users get a few cloud messages a day with the free models, "
       "and unlimited Apple Intelligence on supported devices. Omnimo Pro has hundreds of messages a day for the free "
       "and Pro models, and a smaller daily allowance for the flagships. The exact numbers are set on Omnimo's server "
       "and the app shows how many are left.")

SOURCE = ("    <p class=\"cite\">Source: Omnimo's model catalog (the gateway that serves the app), 25 November 2026. "
          "Models, limits and the longest prompt can change with a server update, without an app update. "
          "Which models are offered can depend on your country.</p>")


FAMILIES = [
    {
        "slug": "gpt-6", "name": "GPT-6", "maker": "openai", "ids": ["gpt-6-luna", "gpt-6-sol", "gpt-6.1-sol", "gpt-6.1-terra", "gpt-6-astra"],
        "title": "GPT-6 in Omnimo: Luna free, Sol, Terra and Astra on Pro",
        "desc": "OpenAI's GPT-6 models in the Omnimo app for iPhone, iPad and Mac: GPT-6 Luna is free; GPT-6 Sol, "
                "GPT-6.1 Sol, GPT-6.1 Terra and GPT-6 Astra are part of Omnimo Pro.",
        "about": "GPT-6 is OpenAI's model family. Omnimo offers five of them. <strong>GPT-6 Luna</strong> is the "
                 "default model for new users and one of the free ones. <strong>GPT-6 Sol</strong>, "
                 "<strong>GPT-6.1 Sol</strong> and <strong>GPT-6.1 Terra</strong> are flagships on Pro. "
                 "<strong>GPT-6 Astra</strong> is a Pro flagship too, and takes the shortest prompts of the five.",
        "use": ["Luna for everyday questions, quick drafts, translations and photo questions, free.",
                "Sol or Terra when an answer needs more care: a long email, a tricky explanation, planning.",
                "Astra for the hardest questions, when it is worth spending more of the day's flagship allowance."],
        "faq": [("Is GPT-6 free in Omnimo?", "GPT-6 Luna is free, with a few messages a day. The other GPT-6 models "
                 "are part of Omnimo Pro."),
                ("Is this ChatGPT?", "No. Omnimo uses OpenAI's GPT-6 models through a pay-per-token API. ChatGPT is "
                 "OpenAI's own app, with its own features. Omnimo is not affiliated with OpenAI.")],
    },
    {
        "slug": "claude-haiku", "name": "Claude Haiku", "maker": "anthropic", "ids": ["claude-haiku-5.5"],
        "title": "Claude Haiku 5.5 in Omnimo: Anthropic's fast model, free",
        "desc": "Claude Haiku 5.5, Anthropic's fastest Claude model, is one of Omnimo's free cloud models on iPhone, "
                "iPad and Mac: a few messages a day free, hundreds on Pro.",
        "about": "Haiku is the fastest and least expensive model in Anthropic's Claude line. In Omnimo, "
                 "<strong>Claude Haiku 5.5</strong> is one of the five free cloud models, and it can see photos.",
        "use": ["Quick questions and short answers in Claude's style.",
                "Rewriting and summarizing short texts.",
                "Trying Claude before deciding on Pro."],
        "faq": [("Is Claude free in Omnimo?", "Claude Haiku 5.5 is free, with a few messages a day. Claude Sonnet, "
                 "Opus and Fable are part of Omnimo Pro.")],
    },
    {
        "slug": "claude-sonnet", "name": "Claude Sonnet", "maker": "anthropic", "ids": ["claude-sonnet-5.5"],
        "title": "Claude Sonnet 5.5 in Omnimo (Pro)",
        "desc": "Claude Sonnet 5.5, Anthropic's balanced Claude model, in the Omnimo app for iPhone, iPad and Mac. "
                "Part of Omnimo Pro, next to GPT-6, Gemini and Grok.",
        "about": "Sonnet sits in the middle of Anthropic's Claude line, between the fast Haiku and the larger Opus. "
                 "In Omnimo, <strong>Claude Sonnet 5.5</strong> is a flagship on Pro.",
        "use": ["Writing that needs care: a cover letter, a difficult email, an essay outline.",
                "Reading a long document and answering questions about it.",
                "Code: explaining, reviewing and fixing short programs."],
        "faq": [("How many Claude Sonnet messages do I get on Pro?", "Sonnet uses the daily flagship allowance; "
                 "the app shows how many messages are left."),
                ("Is it the same Claude as in the Claude app?", "It is Anthropic's Claude Sonnet 5.5 model, through "
                 "Anthropic's API. Features of the Claude app itself, such as projects and connectors, are not in "
                 "Omnimo.")],
    },
    {
        "slug": "claude-opus", "name": "Claude Opus", "maker": "anthropic", "ids": ["claude-opus-5.5"],
        "title": "Claude Opus 5.5 in Omnimo (Pro)",
        "desc": "Claude Opus 5.5, one of Anthropic's largest Claude models, in the Omnimo app for iPhone, iPad and "
                "Mac. Part of Omnimo Pro.",
        "about": "Opus is the larger model in Anthropic's Claude line. In Omnimo, <strong>Claude Opus 5.5</strong> "
                 "is a Pro flagship.",
        "use": ["Hard reasoning: a plan with many constraints, a careful argument, a long analysis.",
                "A second opinion on an answer from another model in the same chat."],
        "faq": [("Is Claude Opus in the free plan?", "No, Claude Opus 5.5 is part of Omnimo Pro and uses the daily "
                 "flagship allowance. The free plan has Claude Haiku 5.5.")],
    },
    {
        "slug": "claude-fable", "name": "Claude Fable", "maker": "anthropic", "ids": ["claude-fable-5.1"],
        "title": "Claude Fable 5.1 in Omnimo (Pro)",
        "desc": "Claude Fable 5.1 from Anthropic in the Omnimo app for iPhone, iPad and Mac. The most expensive Claude "
                "model in Omnimo, part of Pro.",
        "about": "<strong>Claude Fable 5.1</strong> is the most expensive Claude model Omnimo offers. It is part of Pro, and "
                 "Omnimo accepts shorter prompts for it than for the other Claude models.",
        "use": ["The questions where you want Anthropic's most capable model in the app and a few answers a day are "
                "enough.",
                "Comparing its answer with Opus or GPT-6 Astra in the same chat."],
        "faq": [("How many Fable messages can I send?", "Fable uses the daily flagship allowance of Omnimo Pro, and "
                 "as the most expensive Claude model it uses it up faster than Sonnet. The app shows what is left.")],
    },
    {
        "slug": "gemini", "name": "Gemini", "maker": "google",
        "ids": ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3.8-flash", "gemini-3.1-pro"],
        "title": "Gemini in Omnimo: Flash-Lite free, Flash and Pro on Pro",
        "desc": "Google's Gemini models in the Omnimo app for iPhone, iPad and Mac: Gemini 3.1 Flash-Lite is free; "
                "Gemini 3.5 Flash-Lite, 3.5 Flash, 3.8 Flash and 3.1 Pro are part of Omnimo Pro.",
        "about": "Gemini is Google's model family. In Google's naming, Flash-Lite is the lightest, Flash the fast "
                 "general model and Pro the larger one. Omnimo offers <strong>Gemini 3.1 Flash-Lite</strong> free, "
                 "<strong>Gemini 3.5 Flash-Lite</strong> on Pro, and <strong>Gemini 3.5 Flash</strong>, "
                 "<strong>3.8 Flash</strong> and <strong>3.1 Pro</strong> as Pro flagships. All of them can see photos.",
        "use": ["Flash-Lite for quick free answers and photo questions.",
                "Flash or Pro for longer answers, explanations and planning."],
        "faq": [("Is this the Gemini app?", "No. Omnimo uses Google's Gemini models through an API. The Gemini app's "
                 "own features, such as Gemini Live and Google app connections, are not in Omnimo. Omnimo is not "
                 "affiliated with Google.")],
    },
    {
        "slug": "grok", "name": "Grok", "maker": "xai", "ids": ["grok-4.7", "grok-4.3"],
        "title": "Grok in Omnimo: Grok 4.7 and Grok 4.3 (Pro)",
        "desc": "xAI's Grok 4.7 and Grok 4.3 in the Omnimo app for iPhone, iPad and Mac, next to GPT-6, Claude and "
                "Gemini. Part of Omnimo Pro.",
        "about": "Grok is xAI's model family. Omnimo offers <strong>Grok 4.7</strong> and <strong>Grok 4.3</strong> "
                 "as Pro flagships; both can see photos.",
        "use": ["Another maker's take on a question you have asked GPT or Claude.",
                "Everyday questions and writing in Grok's style, without a separate subscription."],
        "faq": [("Can I use Grok without an X subscription?", "In Omnimo, yes: Grok 4.7 and 4.3 are part of Omnimo "
                 "Pro. xAI's own Grok app and X subscription have features Omnimo doesn't, such as Grok Imagine.")],
    },
    {
        "slug": "deepseek", "name": "DeepSeek", "maker": "deepseek", "ids": ["deepseek-v4-flash", "deepseek-v4-pro", "deepseek-v4.1-flash"],
        "title": "DeepSeek in Omnimo: V4 Flash free, V4 Pro and V4.1 Flash on Pro",
        "desc": "DeepSeek's models in the Omnimo app for iPhone, iPad and Mac: DeepSeek V4 Flash is free, DeepSeek V4 "
                "Pro and V4.1 Flash are part of Omnimo Pro.",
        "about": "DeepSeek makes open-weight models. Omnimo offers <strong>DeepSeek V4 Flash</strong> free, and "
                 "<strong>DeepSeek V4 Pro</strong> and <strong>V4.1 Flash</strong> on Pro, from the large daily "
                 "allowance. DeepSeek V4 Flash and V4 Pro can't see photos; when a photo is in the chat, Omnimo "
                 "switches to a model that can and says so.",
        "use": ["Text questions, math and code explanations.",
                "In countries where some makers' models are not offered, DeepSeek V4 Flash is Omnimo's default free model."],
        "faq": [("Can DeepSeek read my photos in Omnimo?", "DeepSeek V4.1 Flash can. DeepSeek V4 Flash and V4 Pro "
                 "can't; with a photo in the chat Omnimo uses a model that can see it.")],
    },
    {
        "slug": "kimi", "name": "Kimi", "maker": "moonshot", "ids": ["kimi-k3", "kimi-k3.1-pro"],
        "title": "Kimi K3 and K3.1 Pro in Omnimo (Pro)",
        "desc": "Moonshot AI's Kimi K3 and Kimi K3.1 Pro in the Omnimo app for iPhone, iPad and Mac. Part of Omnimo Pro.",
        "about": "Kimi is Moonshot AI's model family. Omnimo offers <strong>Kimi K3</strong> and <strong>Kimi K3.1 "
                 "Pro</strong> as Pro flagships.",
        "use": ["Long, structured answers and a different maker's view on a problem."],
        "faq": [("Is Kimi free in Omnimo?", "No, Kimi K3 and K3.1 Pro are part of Omnimo Pro.")],
    },
    {
        "slug": "qwen", "name": "Qwen", "maker": "qwen", "ids": ["qwen-3.8-flash", "qwen-3.7-plus", "qwen-3.8-max"],
        "title": "Qwen in Omnimo: 3.8 Flash free, 3.7 Plus and 3.8 Max on Pro",
        "desc": "Alibaba's Qwen models in the Omnimo app for iPhone, iPad and Mac: Qwen 3.8 Flash is free, Qwen 3.7 "
                "Plus and Qwen 3.8 Max are part of Omnimo Pro.",
        "about": "Qwen is Alibaba's model family. Omnimo offers <strong>Qwen 3.8 Flash</strong> free, <strong>Qwen "
                 "3.7 Plus</strong> on Pro and <strong>Qwen 3.8 Max</strong> as a Pro flagship.",
        "use": ["Quick free answers with Flash.", "Translation and multilingual questions."],
        "faq": [("Which Qwen is free?", "Qwen 3.8 Flash, with a few messages a day.")],
    },
    {
        "slug": "glm", "name": "GLM", "maker": "zhipu", "ids": ["glm-5.3", "glm-5.3-flash"],
        "title": "GLM 5.3 and GLM 5.3 Flash in Omnimo (Pro)",
        "desc": "Zhipu's GLM 5.3 and GLM 5.3 Flash in the Omnimo app for iPhone, iPad and Mac, part of Omnimo Pro.",
        "about": "GLM is the model family of Zhipu (Z.ai). Omnimo offers <strong>GLM 5.3</strong> and <strong>GLM "
                 "5.3 Flash</strong> on Pro, from the large daily allowance. GLM 5.3 can't see photos; GLM 5.3 Flash can.",
        "use": ["Text tasks and code on Pro without touching the flagship allowance."],
        "faq": [("Does GLM count against the flagship allowance?", "No. GLM 5.3 and GLM 5.3 Flash use the larger "
                 "daily allowance of Pro messages.")],
    },
    {
        "slug": "minimax", "name": "MiniMax", "maker": "minimax", "ids": ["minimax-m3", "minimax-m3.1-flash"],
        "title": "MiniMax M3 and M3.1 Flash in Omnimo (Pro)",
        "desc": "MiniMax M3 and MiniMax M3.1 Flash in the Omnimo app for iPhone, iPad and Mac, part of Omnimo Pro.",
        "about": "Omnimo offers <strong>MiniMax M3</strong> and <strong>MiniMax M3.1 Flash</strong> on Pro, from the "
                 "large daily allowance. Both can see photos.",
        "use": ["Everyday questions on Pro without touching the flagship allowance."],
        "faq": [("Is MiniMax free?", "No, the MiniMax models are part of Omnimo Pro.")],
    },
    {
        "slug": "mistral", "name": "Mistral", "maker": "mistral", "ids": ["mistral-small", "mistral-large-4"],
        "title": "Mistral Small and Mistral Large 4 in Omnimo (Pro)",
        "desc": "Mistral AI's Mistral Small and Mistral Large 4 in the Omnimo app for iPhone, iPad and Mac, part of "
                "Omnimo Pro.",
        "about": "Mistral AI is a French model maker. Omnimo offers <strong>Mistral Small</strong> and "
                 "<strong>Mistral Large 4</strong> on Pro, from the large daily allowance. Both can see photos.",
        "use": ["Writing and questions in French and other European languages.", "Fast answers on Pro."],
        "faq": [("Is Mistral in the free plan?", "No, Mistral Small and Mistral Large 4 are part of Omnimo Pro.")],
    },
    {
        "slug": "llama", "name": "Llama", "maker": "meta", "ids": ["llama-4-maverick"],
        "title": "Llama 4 Maverick in Omnimo (Pro)",
        "desc": "Meta's Llama 4 Maverick in the Omnimo app for iPhone, iPad and Mac, part of Omnimo Pro.",
        "about": "Llama is Meta's open-weight model family. Omnimo offers <strong>Llama 4 Maverick</strong> on Pro, "
                 "from the large daily allowance; it can see photos.",
        "use": ["Everyday questions and another maker's view, on Pro."],
        "faq": [("Does Omnimo run Llama on my iPhone?", "No. Llama 4 Maverick runs in the cloud. The only model "
                 "that runs on your device in Omnimo is Apple Intelligence.")],
    },
    {
        "slug": "mimo", "name": "MiMo", "maker": "xiaomi", "ids": ["mimo-v2.6-pro"],
        "title": "MiMo V2.6 Pro in Omnimo (Pro)",
        "desc": "Xiaomi's MiMo V2.6 Pro in the Omnimo app for iPhone, iPad and Mac, part of Omnimo Pro.",
        "about": "MiMo is Xiaomi's model family. Omnimo offers <strong>MiMo V2.6 Pro</strong> on Pro, from the large "
                 "daily allowance; it can see photos.",
        "use": ["Everyday questions and another maker's view, on Pro."],
        "faq": [("Is MiMo free?", "No, MiMo V2.6 Pro is part of Omnimo Pro.")],
    },
]

BY_ID = {m[0]: m for m in CATALOG}


def family_page(f):
    models = [BY_ID[i] for i in f["ids"]]
    restricted = f["maker"] in RESTRICTED
    body = "\n".join([
        p(f["about"]),
        h2(f"{f['name']} in Omnimo"),
        table(HEAD, rows(models)),
        SOURCE,
        h2("Good for"),
        ul(f["use"]),
        p(HOW),
        p("Not offered in some countries: the maker's terms don't allow it there, and Omnimo hides these models."
          if restricted else
          "In countries where some makers' models are not offered, these models are still available."),
        h2("Try it"),
        p("Open Omnimo, tap the model name at the top of the chat and pick it. You can switch in the middle of a "
          "chat; each answer shows which model wrote it. Ready prompts: the <a href=\"/prompts/\">prompt library</a>."),
    ])
    return {
        "path": f"models/{f['slug']}.html", "title": f["title"], "description": f["desc"],
        "h1": f"{f['name']} in Omnimo", "meta": f"Updated {UPDATED_TEXT} · from Omnimo's model catalog",
        "body": body, "faq": f["faq"], "md": True, "llms": "Models",
        "crumbs": [("Omnimo", "index.html"), ("Models", "models/index.html"), (f["name"], f"models/{f['slug']}.html")],
    }


def apple_page():
    body = "\n".join([
        p("Apple Intelligence includes a language model that runs on your iPhone, iPad or Mac. Apple lets apps use "
          "it through its Foundation Models framework, and Omnimo does: chats with Apple Intelligence are free, "
          "unlimited, work offline and never leave the device."),
        table(["", "Apple Intelligence in Omnimo"], [
            ["Plan", "Free, unlimited, on every plan"],
            ["Runs", "On your device. Nothing is sent anywhere."],
            ["Needs", "iOS, iPadOS or macOS 26 on a device that supports Apple Intelligence, with Apple Intelligence "
                      "turned on, in a language it supports"],
            ["Internet", "Not needed"],
            ["When it is used", "Pick it in the model menu. A new user on a supported device starts with it. When the "
                                "free cloud messages run out, or the internet is gone, the chat can carry on with it."],
        ]),
        h2("What to expect"),
        p("Apple's on-device model is much smaller than the cloud flagships. It is good at short, everyday tasks: "
          "rewriting a message, a summary, a quick answer, a translation. For long documents, hard reasoning or "
          "photos, switch to a cloud model in the same chat."),
        p("Siri and Shortcuts in Omnimo, Ask, Summarize, Rephrase and Translate, run on the device with Apple "
          "Intelligence too."),
        h2("Which devices"),
        p(f"Apple keeps the list of devices that support Apple Intelligence: "
          f"{ext('https://support.apple.com/en-us/121115', 'Apple Intelligence requirements')}. On other devices Omnimo "
          "works with the cloud models only. More: <a href=\"/guides/free-offline-ai-iphone.html\">free offline AI on "
          "iPhone</a>."),
    ])
    return {
        "path": "models/apple-intelligence.html", "title": "Apple Intelligence in Omnimo: free, unlimited, on your device",
        "description": "Omnimo uses Apple Intelligence's on-device model: free, unlimited, offline, nothing leaves your "
                       "iPhone, iPad or Mac. What it needs and what to expect.",
        "h1": "Apple Intelligence in Omnimo", "meta": f"Updated {UPDATED_TEXT}", "body": body, "md": True,
        "llms": "Models",
        "faq": [("Is Apple Intelligence in Omnimo really unlimited?", "Yes. It runs on your device, so it costs "
                 "nothing to run and has no daily limit."),
                ("Does Apple Intelligence in Omnimo work offline?", "Yes, on supported devices and languages. The cloud "
                 "models need the internet.")],
        "crumbs": [("Omnimo", "index.html"), ("Models", "models/index.html"), ("Apple Intelligence", "models/apple-intelligence.html")],
    }


VERSUS = [
    {
        "slug": "claude-vs-gpt-6", "a": "Claude", "b": "GPT-6",
        "title": "Claude vs GPT-6 in Omnimo: which to pick, and how to compare them yourself",
        "desc": "Claude (Anthropic) and GPT-6 (OpenAI) side by side as Omnimo offers them: which is free, which is "
                "Pro, and a simple way to compare their answers to your own questions.",
        "ids": ["claude-haiku-5.5", "gpt-6-luna", "claude-sonnet-5.5", "gpt-6-sol", "gpt-6.1-sol", "gpt-6.1-terra",
                "claude-opus-5.5", "claude-fable-5.1", "gpt-6-astra"],
        "body": [
            "Both families come in tiers, and the fair comparison is tier against tier: <strong>Claude Haiku 5.5 vs "
            "GPT-6 Luna</strong> (both free), <strong>Claude Sonnet 5.5 vs GPT-6 Sol or GPT-6.1 Terra</strong> (Pro "
            "flagships), and <strong>Claude Fable 5.1 vs GPT-6 Astra</strong> (the top of each family in the app, "
            "also Pro flagships). Claude Opus 5.5 sits between.",
            "We don't publish a winner. The makers publish their own benchmark scores, and which model writes the "
            "answer you prefer depends on the question. What we can say from the catalog: all of these models see "
            "photos; the free pair take the longest prompts; the top pair the shortest.",
        ],
    },
    {
        "slug": "gemini-vs-claude", "a": "Gemini", "b": "Claude",
        "title": "Gemini vs Claude in Omnimo: tiers, limits and how to compare",
        "desc": "Google's Gemini and Anthropic's Claude as Omnimo offers them: free and Pro models, prompt limits, "
                "and how to compare their answers in one chat.",
        "ids": ["gemini-3.1-flash-lite", "claude-haiku-5.5", "gemini-3.5-flash-lite", "gemini-3.5-flash",
                "gemini-3.8-flash", "gemini-3.1-pro", "claude-sonnet-5.5", "claude-opus-5.5", "claude-fable-5.1"],
        "body": [
            "The free pair is <strong>Gemini 3.1 Flash-Lite vs Claude Haiku 5.5</strong>. On Pro, Gemini 3.5 Flash-Lite "
            "comes from the large daily allowance, while <strong>Gemini 3.5 Flash, 3.8 Flash and 3.1 Pro</strong> "
            "and <strong>Claude Sonnet 5.5, Opus 5.5 and Fable 5.1</strong> are Pro flagships, from the daily flagship "
            "allowance.",
            "Which writes the better answer to your question is something to try, not something we can promise.",
        ],
    },
    {
        "slug": "gpt-6-sol-vs-luna", "a": "GPT-6 Sol", "b": "GPT-6 Luna",
        "title": "GPT-6 Sol vs GPT-6 Luna: what Pro adds",
        "desc": "GPT-6 Luna is free in Omnimo; GPT-6 Sol is a Pro flagship. What the difference means in the app, and "
                "when it is worth switching.",
        "ids": ["gpt-6-luna", "gpt-6-sol", "gpt-6.1-sol"],
        "body": [
            "<strong>GPT-6 Luna</strong> is OpenAI's fast model and Omnimo's default free model: a few messages a day "
            "free, and on Pro it comes from the large daily allowance. <strong>GPT-6 Sol</strong> (and the newer "
            "<strong>GPT-6.1 Sol</strong>) are flagships: Pro only, counted against the smaller flagship allowance, "
            "with a shorter longest prompt (about 48K tokens against Luna's 64K).",
            "In practice: start with Luna. If an answer is too shallow, switch to Sol in the same chat and ask again; "
            "you keep the conversation and see both answers.",
        ],
    },
]


def versus_page(v):
    models = [BY_ID[i] for i in v["ids"]]
    body = "\n".join([
        p(*v["body"]),
        h2("Side by side in Omnimo"),
        table(HEAD, rows(models)),
        SOURCE,
        h2("Compare them on your own question"),
        "    <ol>\n      <li>Ask your question with the first model.</li>\n"
        "      <li>Tap the model name at the top, pick the other one, and ask again in the same chat.</li>\n"
        "      <li>Each answer shows which model wrote it. Keep the one you prefer and carry on.</li>\n    </ol>",
        p(HOW),
    ])
    return {
        "path": f"models/{v['slug']}.html", "title": v["title"], "description": v["desc"],
        "h1": f"{v['a']} vs {v['b']}", "meta": f"Updated {UPDATED_TEXT} · from Omnimo's model catalog",
        "body": body, "md": True, "llms": "Models",
        "faq": [(f"Which is better, {v['a']} or {v['b']}?", "It depends on the question, and we have not run "
                 "benchmarks of our own. In Omnimo you can ask both in the same chat and keep the answer you prefer.")],
        "crumbs": [("Omnimo", "index.html"), ("Models", "models/index.html"), (f"{v['a']} vs {v['b']}", f"models/{v['slug']}.html")],
    }


def index_page():
    by_tier = {t: [m for m in CATALOG if m[3] == t] for t in ("free", "pro", "premium")}
    fam = [(f"/models/{f['slug']}.html", MAKERS[f["maker"]], f["name"], f["desc"]) for f in FAMILIES]
    fam.insert(0, ("/models/apple-intelligence.html", "Apple", "Apple Intelligence",
                   "On your device: free, unlimited, offline. Needs a supported device on iOS, iPadOS or macOS 26."))
    body = "\n".join([
        p(f"Omnimo has {len(CATALOG)} cloud models from {len(MAKERS)} makers, plus Apple Intelligence on the device. "
          "Pick any of them from the menu at the top of a chat, and switch at any time, even in the middle of a chat."),
        h2(f"Free: {len(by_tier['free'])} models"),
        table(HEAD, rows(by_tier["free"])),
        h2(f"Pro: {len(by_tier['pro'])} models"),
        table(HEAD, rows(by_tier["pro"])),
        h2(f"Pro flagships: {len(by_tier['premium'])} models"),
        table(HEAD, rows(by_tier["premium"])),
        SOURCE,
        p(HOW),
        p(f"<strong>Omnimo Pro</strong>: {PRICE_LINE}"),
        h2("By family"),
        cards(fam),
        h2("Model vs model"),
        ul([f'<a href="/models/{v["slug"]}.html">{v["a"]} vs {v["b"]}</a>' for v in VERSUS]),
        h2("Images and video"),
        p("Image and video generation is paid in credits, not messages: one image a day is free, Pro includes "
          "credits every period, and credit packs can be bought. The description you write goes to fal.ai, which "
          "runs the image and video models."),
    ])
    return {
        "path": "models/index.html", "title": "The AI models in Omnimo: GPT-6, Claude, Gemini, Grok, DeepSeek and more",
        "description": f"Every model in the Omnimo app: {len(CATALOG)} cloud models from {len(MAKERS)} makers plus Apple "
                       "Intelligence on the device. Which are free, which are Pro, and the longest prompt each takes.",
        "h1": "The models in Omnimo", "meta": f"Updated {UPDATED_TEXT} · from Omnimo's model catalog",
        "body": body, "schema": "CollectionPage", "md": True, "llms": "Models",
        "faq": [("Which models are free in Omnimo?", "Apple Intelligence on the device (unlimited, on supported "
                 "devices), and a few messages a day with GPT-6 Luna, Claude Haiku 5.5, Gemini 3.1 Flash-Lite, "
                 "DeepSeek V4 Flash and Qwen 3.8 Flash."),
                ("Can I switch models in the middle of a chat?", "Yes. Pick another model from the menu and ask "
                 "again; the conversation carries on.")],
        "crumbs": [("Omnimo", "index.html"), ("Models", "models/index.html")],
    }


def pages():
    return [index_page(), apple_page()] + [family_page(f) for f in FAMILIES] + [versus_page(v) for v in VERSUS]
