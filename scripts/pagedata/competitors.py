"""Other AI chat apps, as their own listings describe them.

Read on 2026-11-25 from the US App Store: the iTunes lookup API (rating, number of
ratings, price, the listing's description) and the app's App Store page (its list of
in-app purchases, which Apple shows without the billing period of each). TypingMind
is a web app; its facts are from typingmind.com on the same day. ChatGPT Plus,
Claude Pro and Google AI Pro on the makers' own sites: gateway/src/comparison.ts in
the app repo (read 2026-11-03).

Only what a listing says is used. Where it doesn't say (a free tier's limits, the
period of a plan), the pages say that it isn't stated instead of guessing.
"""

READ = "25 November 2026"

APPS = {
    "chatgpt": {
        "name": "ChatGPT", "maker": "OpenAI", "id": "6448311069", "site": "https://openai.com/chatgpt",
        "rating": "4.8", "ratings": "12.5 million",
        "plans": "ChatGPT Go $8.00, ChatGPT Plus $19.99, ChatGPT Pro from $100 (in-app purchase list); "
                 "Plus is $20 a month on OpenAI's site (3 November 2026)",
        "models": "OpenAI's own models only",
        "listing": "image generation, Advanced Voice Mode, photo upload, history synced across devices",
    },
    "claude": {
        "name": "Claude by Anthropic", "maker": "Anthropic", "id": "6473753684", "site": "https://claude.ai",
        "rating": "4.7", "ratings": "315,000",
        "plans": "Claude Pro $20.00 a month or $214.99 a year, Claude Max $124.99 a month, Claude Ultra "
                 "$249.99 a month (in-app purchase list)",
        "models": "Anthropic's own Claude models only",
        "listing": "writing, coding, research with citations, photo and PDF analysis, voice, Google Drive, Gmail "
                   "and Calendar connectors",
    },
    "gemini": {
        "name": "Google Gemini", "maker": "Google", "id": "6477489729", "site": "https://gemini.google.com/app/download",
        "rating": "4.7", "ratings": "2.46 million",
        "plans": "Google AI Plus $4.99, Google AI Pro $19.99, Google AI Ultra $199.99 (in-app purchase list; "
                 "the plans include Google storage)",
        "models": "Google's own Gemini models only",
        "listing": "Gemini Live with camera and screen sharing, image editing with Nano Banana 2, Google app "
                   "connections (Gmail, Calendar, Photos, YouTube, Search), NotebookLM",
    },
    "perplexity": {
        "name": "Perplexity", "maker": "Perplexity AI", "id": "1668000334", "site": "https://www.perplexity.ai",
        "rating": "4.8", "ratings": "530,000",
        "plans": "Perplexity Pro $20.00 (also listed at $200.00), Perplexity Max $200.00, credit packs from "
                 "$5.00 (in-app purchase list)",
        "models": "\"top AI models from OpenAI, Anthropic, Meta, and more\"",
        "listing": "answers with cited sources, Pro Search and Deep Research, Labs, an assistant that drafts "
                   "emails and books reservations, voice",
    },
    "poe": {
        "name": "Poe", "maker": "Quora", "id": "1640745955", "site": "https://poe.com",
        "rating": "4.7", "ratings": "53,800",
        "plans": "Basic $4.99 a month or $49.99 a year, Plus $19.99 a month or $199.99 a year (in-app purchase "
                 "list); usage is counted in points",
        "models": "models from OpenAI, Anthropic, Google and others, image and video generators, and over a "
                  "million custom bots",
        "listing": "several bots in one chat to compare answers, custom bots you can build and share, web search, "
                   "files, image and video generation",
    },
    "chaton": {
        "name": "ChatOn", "maker": "AIBY", "id": "1661308505", "site": "https://aiby.com",
        "rating": "4.7", "ratings": "289,000",
        "plans": "Premium at $6.99 and $7.99 (weekly) and $29.99 and $39.99 (in-app purchase list)",
        "models": "GPT-5, Gemini 3.5, Claude Sonnet 5 and Sonar, as its listing names them",
        "listing": "100+ ready prompts, image and video generation, text from photos, web search, PDF "
                   "summaries, YouTube summaries, math help",
    },
    "nova": {
        "name": "Nova", "maker": "ScaleUp", "id": "1669007652", "site": "https://chatnova.com",
        "rating": "4.6", "ratings": "128,000",
        "plans": "1 Week Chatbot Pro $4.99 to $7.99, Nova Premium $9.99, 1 Year Chatbot Pro $39.99 and $59.99 "
                 "(in-app purchase list)",
        "models": "GPT-5.6, Gemini 3.6 Flash, Claude Opus 5, Kimi K3, Grok 4.5 and DeepSeek V4 Pro, as its "
                  "listing names them",
        "listing": "image generation, web search, voice mode, Word and Excel files, scan-and-solve, coding help, "
                   "\"140+ languages\"",
    },
    "genie": {
        "name": "Genie (Chatbot AI Assistant)", "short": "Genie", "maker": "AppNation", "id": "1658377526",
        "site": "https://appnation.co",
        "rating": "4.7", "ratings": "204,000",
        "plans": "Weekly Unlimited $7.99, other weekly plans $8.99 to $12.99, yearly $39.99 and $99.99 (in-app "
                 "purchase list); supports Family Sharing",
        "models": "GPT, Gemini, Grok, Claude, DeepSeek, Perplexity Sonar, Kimi and GLM, plus image and video "
                  "models, as its listing names them",
        "listing": "Deep Thinking, image generation and editing, photo analysis, PDF and text files, web search "
                   "and Deep Search, voice chat",
    },
    "chatnow": {
        "name": "ChatNow", "maker": "Tappz", "id": "1667518571", "site": "https://tappz.com/",
        "rating": "4.8", "ratings": "148,000",
        "plans": "AI Plus $6.99, ChatNow Plus $19.99, yearly plans $49.99 to $79.99, credit packs (in-app purchase "
                 "list); supports Family Sharing; needs iOS 26",
        "models": "\"30+ of the top AI models\": GPT-6 Astra, GPT-5.6, Claude Fable 5.1, Claude 4.8 Opus, Gemini "
                  "3.1 Pro, Grok 4.5 and others, plus image and video models such as Veo 3.1 and Sora 2",
        "listing": "ask several models the same question and compare, image and video creation, web search with "
                   "sources, a Playground that builds apps, voice mode",
    },
    "fello": {
        "name": "Fello AI", "maker": "AI Apps Brewery", "id": "6447705369", "site": "https://felloai.com",
        "rating": "4.5", "ratings": "144",
        "plans": "weekly $4.99, monthly $11.99, quarterly $24.99, yearly $89.99 (in-app purchase list); a free "
                 "tier with limited daily messages",
        "models": "GPT-6, Claude 5.5, Gemini 4, Grok 4.7, GLM 5.3, DeepSeek V4.1, Qwen 3.8 Max, MiniMax M3.1, Kimi "
                  "K3.1, Mistral and more, as its listing names them",
        "listing": "Mac, iPhone and iPad with sync, creates real .pptx, .xlsx, .docx and .pdf files, Projects, Deep "
                   "Research, podcasts from documents",
    },
    "allchat": {
        "name": "AllChat", "maker": "IQ Digital", "id": "6756892955", "site": "https://askallchat.com",
        "rating": "4.5", "ratings": "22",
        "plans": "Premium $7.99 weekly or $99.99 yearly, Pro $8.99 a month or $89.99 a year, Max $17.99 a month or "
                 "$179.99 a year (in-app purchase list)",
        "models": "GPT, Claude, Gemini, Grok and more, plus on-device models",
        "listing": "Consensus Mode (several models answer, one combined reply), Smart Routing, alerts, ChatGPT "
                   "memory import, memory, offline on-device models",
    },
    "typingmind": {
        "name": "TypingMind", "maker": "TypingMind", "id": None, "site": "https://www.typingmind.com",
        "rating": None, "ratings": None,
        "plans": "a lifetime license, paid once (price on typingmind.com); you also pay the AI providers for "
                 "what you use, with your own API keys",
        "models": "whichever providers you bring an API key for",
        "listing": "a chat interface in the browser, your own API keys, data stored locally by default, agents, "
                   "prompts, plugins and a knowledge base",
    },
    "private-llm": {
        "name": "Private LLM", "maker": "Numen Technologies", "id": "6448106860", "site": "https://privatellm.app",
        "rating": "4.1", "ratings": "755",
        "plans": "$4.99 once, no subscription",
        "models": "open models run on the device: Llama, Gemma, Qwen, Phi, Mistral, DeepSeek R1 Distill and others",
        "listing": "fully offline, Siri and Shortcuts, Family Sharing",
    },
    "locally": {
        "name": "Locally AI by LM Studio", "short": "Locally AI", "maker": "Element Labs", "id": "6741426692",
        "site": "https://locallyai.app",
        "rating": "4.7", "ratings": "2,047",
        "plans": "free download; no in-app purchases listed",
        "models": "open models run on the device with Apple MLX: Llama 3.2, Gemma 2 and 3, Qwen 3, DeepSeek and more",
        "listing": "offline, no login, no data collection, iPhone and iPad",
    },
    "pocketpal": {
        "name": "PocketPal AI", "maker": "Gooya", "id": "6502579498", "site": "https://apps.apple.com/us/app/id6502579498",
        "rating": "4.1", "ratings": "173",
        "plans": "free download; PocketPal Plus from $3.99 (in-app purchase list)",
        "models": "GGUF models you download from Hugging Face and run on the device",
        "listing": "offline chat, Hugging Face search inside the app",
    },
    "grok": {
        "name": "Grok", "maker": "xAI", "id": "6670324846", "site": "https://x.ai",
        "rating": "4.9", "ratings": "1.63 million",
        "plans": "SuperGrok Lite $10, SuperGrok $30, SuperGrok Plus $100, SuperGrok Heavy $300 (in-app purchase list)",
        "models": "xAI's own Grok models",
        "listing": "deep research on the web, documents and photos in chat, Grok Imagine image and video generation",
    },
}


def store(key):
    app = APPS[key]
    return f"https://apps.apple.com/us/app/id{app['id']}" if app["id"] else app["site"]


def rating(key):
    app = APPS[key]
    if not app["rating"]:
        return "not on the App Store (a web app)"
    return f"{app['rating']} from {app['ratings']} ratings (US App Store, {READ})"
