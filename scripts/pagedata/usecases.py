"""/use-cases/ (audit #133): the jobs people open Omnimo for, matched to the App Store
keywords (summarize, pdf, homework, translate, email) and the audit's jobs J1-J3.
"""

from .common import UPDATED_TEXT, cards, ul, p, h2

APPLE_DEVICES = ("iPhone 15 Pro and Pro Max, iPhone 16 or later, iPhone Air, iPads with M1 or later, iPad mini with "
                 "A17 Pro or later, and Macs with M1 or later")

USE_CASES = [
    {
        "slug": "summarize-pdf", "h1": "Summarize a PDF on iPhone, iPad or Mac",
        "title": "Summarize a PDF with AI on iPhone, iPad and Mac — Omnimo",
        "desc": "Attach a PDF, Word, Excel, PowerPoint or Pages file, or a scan, and ask Omnimo for a summary, the key "
                "dates, a clause or the numbers. The file is read on your device.",
        "intro": "Omnimo reads documents on your device and answers questions about them: a summary, the key dates, "
                 "one clause, the numbers in a table. It works with PDF, Word, Excel, PowerPoint and Pages files and "
                 "with scans.",
        "steps": ["Tap the attachment button in a chat and choose the file, or scan a page with the camera.",
                  "Ask: <em>Summarize this in five bullet points</em>, or something narrower: <em>What does it say "
                  "about cancellation?</em>",
                  "Ask follow-up questions in the same chat. Switch to a flagship model for a long or difficult document."],
        "model": "Any model reads the text. For long documents, Omnimo Pro reads them in one go, and flagships such as "
                 "Claude Sonnet 5.5 or GPT-6 Sol are a good choice for careful reading. If a document is too long to read "
                 "in one go, the app says which pages the answer covers.",
        "privacy": "The document is turned into text on your device. That text goes to the model you picked, through "
                   "Omnimo's server, to get the answer; Omnimo does not keep it. With Apple Intelligence nothing leaves "
                   "the device.",
        "prompts": [("/prompts/documents/summarize-document.html", "Summarize a document"),
                    ("/prompts/documents/contract-red-flags.html", "Find the red flags in a contract"),
                    ("/prompts/documents/extract-dates.html", "Pull out every date and deadline")],
        "faq": [("Can Omnimo summarize a scanned PDF?", "Yes. Scans and photos of pages are read on your device and "
                 "the text goes to the model."),
                ("Is there a page limit?", "The limit is the model's longest prompt in Omnimo: about 64K tokens for the "
                 "free and Pro models, less for some flagships. On Pro a long document is read in one go.")],
    },
    {
        "slug": "homework", "h1": "Homework help with AI: photo of the problem, step-by-step answer",
        "title": "AI homework help on iPhone: snap the problem, get the steps — Omnimo",
        "desc": "Take a photo of a math problem or a worksheet and ask Omnimo to explain it step by step, with GPT-6, "
                "Claude, Gemini and more. Free to start.",
        "intro": "Take a photo of the problem, or type it, and ask for an explanation you can follow. The point is to "
                 "understand it: ask for the steps, a hint, or a similar problem to try yourself.",
        "steps": ["Take or choose a photo of the problem. The photo goes to the model without its location.",
                  "Ask: <em>Explain how to solve this step by step. Don't just give the answer.</em>",
                  "Stuck on one step? Ask about that step. Want practice? <em>Give me a similar problem.</em>"],
        "model": "Photo questions need a model that sees photos: most do, including the free GPT-6 Luna, Claude Haiku "
                 "5.5 and Gemini 3.1 Flash-Lite. For hard math, try a flagship and compare with a second model in the "
                 "same chat: models can make mistakes, and a disagreement is a reason to check.",
        "privacy": "The photo goes to the model answering, without its location, through Omnimo's server, which "
                   "doesn't keep it.",
        "prompts": [("/prompts/study/explain-step-by-step.html", "Explain a problem step by step"),
                    ("/prompts/study/quiz-me.html", "Quiz me on a topic"),
                    ("/prompts/study/explain-like-im-12.html", "Explain it simply")],
        "faq": [("Is Omnimo's homework help free?", "Yes, to start: a few cloud messages a day are free, photo "
                 "questions included. Omnimo Pro has hundreds a day."),
                ("Can I trust the answer?", "Check it. AI can make mistakes, especially in long calculations. Asking a "
                 "second model the same question in the same chat is a quick way to catch one.")],
    },
    {
        "slug": "translate", "h1": "Translate with AI on iPhone, iPad and Mac",
        "title": "AI translator on iPhone and Mac: text, photos and documents — Omnimo",
        "desc": "Translate text, a photo of a sign or menu, or a whole document with GPT-6, Claude, Gemini and more in "
                "Omnimo. Apple Intelligence translates on the device, free and offline.",
        "intro": "Paste text, take a photo of a sign or a menu, or attach a document, and ask for a translation in "
                 "the tone you need: formal, casual, or word for word with notes. Omnimo speaks 46 languages.",
        "steps": ["Paste the text, or attach a photo or file.",
                  "Ask: <em>Translate into Spanish, keep it formal</em>, or <em>Translate and explain any idioms</em>.",
                  "For a quick translation from any app, use the Translate shortcut in Siri and Shortcuts, which runs "
                  "on the device."],
        "model": "Apple Intelligence translates free and offline on supported devices and languages. For long or "
                 "nuanced texts, a cloud model like Claude Sonnet 5.5, GPT-6 Sol or Mistral Large 4 is a good choice.",
        "privacy": "With Apple Intelligence the text stays on the device. With a cloud model it goes through Omnimo's "
                   "server to the model's maker to get the answer, and is not kept.",
        "prompts": [("/prompts/language/translate-keep-tone.html", "Translate and keep the tone"),
                    ("/prompts/language/translate-photo.html", "Translate a sign or menu from a photo"),
                    ("/prompts/language/practice-conversation.html", "Practice a conversation")],
        "faq": [("Does Omnimo translate offline?", "With Apple Intelligence, yes, on supported devices and in the "
                 "languages it supports. Cloud models need the internet."),
                ("Which languages?", "The app is in 46 languages, and the cloud models translate between many more.")],
    },
    {
        "slug": "email", "h1": "Write emails with AI on iPhone and Mac",
        "title": "AI email writer on iPhone and Mac: draft, reply, rewrite — Omnimo",
        "desc": "Draft an email, reply to one, or make yours shorter, warmer or more formal with GPT-6, Claude, Gemini "
                "and more in Omnimo. Rephrase on the device with Siri and Shortcuts.",
        "intro": "Tell Omnimo who the email is for and what it needs to say, or paste the email you got, and get a "
                 "draft to edit. Set the tone of replies in any chat, or make an assistant that always writes the "
                 "way you do.",
        "steps": ["Paste the email you are answering, or describe the one you need.",
                  "Ask: <em>Reply politely, decline the meeting, suggest next week.</em>",
                  "Refine: <em>Shorter</em>, <em>Warmer</em>, <em>More formal</em>. Or select text in any app and use "
                  "Rephrase, which runs on the device."],
        "model": "Any model writes a good short email; the free ones are fine. For a sensitive message, try a flagship "
                 "like Claude Sonnet 5.5 and compare with GPT-6 Sol in the same chat.",
        "privacy": "Pasted text goes to the model you picked through Omnimo's server, and is not kept. Rephrase in "
                   "Siri and Shortcuts uses Apple Intelligence on the device.",
        "prompts": [("/prompts/email/polite-decline.html", "Decline politely"),
                    ("/prompts/email/follow-up.html", "Follow up without being pushy"),
                    ("/prompts/email/reply-to-complaint.html", "Reply to a complaint")],
        "faq": [("Can Omnimo send the email for me?", "No. Omnimo writes the draft; you copy it into your mail app and "
                 "send it."),
                ("Can it write in my style?", "Make an assistant with instructions about your style, or paste an email "
                 "you wrote and ask it to match.")],
    },
    {
        "slug": "photo-questions", "h1": "Ask AI about a photo",
        "title": "Ask AI about a photo on iPhone: what is this, how do I fix it — Omnimo",
        "desc": "Take or choose a photo and ask Omnimo: what is this, what does it say, how do I fix it. GPT-6, Claude, "
                "Gemini and more can see the photo; its location is not sent.",
        "intro": "Show Omnimo what is in front of you and ask about it: a plant, a label, an error on a screen, a "
                 "broken part, a chart, a page of handwriting.",
        "steps": ["Tap the camera or photo button in a chat and take or choose a photo.",
                  "Ask: <em>What is this?</em>, <em>What does it say?</em>, <em>How do I fix it?</em>",
                  "Follow up in the same chat; Omnimo sends the newest photos with your questions."],
        "model": "Most models in Omnimo can see photos, including the free GPT-6 Luna, Claude Haiku 5.5, Gemini 3.1 "
                 "Flash-Lite and Qwen 3.8 Flash. Three can't (DeepSeek V4 Flash, DeepSeek V4 Pro and GLM 5.3); with a "
                 "photo in the chat, Omnimo switches to one that can and says so.",
        "privacy": "The photo goes to the model answering, without its location and other metadata, through Omnimo's "
                   "server, which doesn't keep it.",
        "prompts": [("/prompts/photos/what-is-this.html", "What is this?"),
                    ("/prompts/photos/fix-it.html", "How do I fix it?"),
                    ("/prompts/photos/read-label.html", "Read a label and explain it")],
        "faq": [("Is asking about a photo free?", "Yes, within the free plan's few cloud messages a day."),
                ("Does Apple Intelligence see photos in Omnimo?", "No; photo questions go to a cloud model that can see "
                 "them.")],
    },
    {
        "slug": "image-generator", "h1": "Make images and short videos with AI",
        "title": "AI image and video generator on iPhone and Mac — Omnimo",
        "desc": "Describe an image or a short video and get it right in the chat in Omnimo: an illustration, a "
                "photo-style image or a short clip. One image a day is free; video is part of Pro.",
        "intro": "Describe what you want and get it in the chat: an illustration, a photo-style image, a short video "
                 "clip. Photo filters restyle a photo you choose.",
        "steps": ["Open Explore and pick Generate image or Create video, or Photo filters to restyle a photo.",
                  "Describe it: subject, style, light, framing. <em>A watercolor of a lighthouse at dawn, soft light.</em>",
                  "Not right? Change one thing at a time and try again."],
        "model": "Images and videos are paid in credits, not messages. One image a day is free. Omnimo Pro includes "
                 "credits every period, and credit packs (300 for $4.99, 700 for $9.99, 1600 for $19.99 in the US) "
                 "never expire. Each image or video model costs a set number of credits, shown in the app.",
        "privacy": "The description you write, and a photo you restyle, go to fal.ai, which runs the image and video "
                   "models.",
        "prompts": [("/prompts/images/product-photo.html", "A clean product photo"),
                    ("/prompts/images/illustration-style.html", "An illustration in a style"),
                    ("/prompts/images/logo-ideas.html", "Logo ideas")],
        "faq": [("Is the image generator free?", "One image a day is free. More images, and video, use credits, which "
                 "Pro includes and anyone can buy."),
                ("Can it make videos?", "Yes, short clips, as part of Pro and paid in credits.")],
    },
]


def page(u):
    body = "\n".join([
        p(u["intro"]),
        h2("How to do it in Omnimo"),
        "    <ol>\n" + "\n".join(f"      <li>{s}</li>" for s in u["steps"]) + "\n    </ol>",
        h2("Which model"),
        p(u["model"]),
        h2("Where your data goes"),
        p(u["privacy"] + ' <a href="/privacy.html">Privacy policy</a>.'),
        h2("Prompts to start with"),
        ul([f'<a href="{href}">{label}</a>' for href, label in u["prompts"]]),
    ])
    return {
        "path": f"use-cases/{u['slug']}.html", "title": u["title"], "description": u["desc"], "h1": u["h1"],
        "meta": f"Updated {UPDATED_TEXT}", "body": body, "faq": u["faq"], "md": True, "llms": "Use cases",
        "crumbs": [("Omnimo", "index.html"), ("Use cases", "use-cases/index.html"), (u["h1"], f"use-cases/{u['slug']}.html")],
    }


def hub():
    items = [(f"/use-cases/{u['slug']}.html", "Use case", u["h1"], u["desc"]) for u in USE_CASES]
    return {
        "path": "use-cases/index.html", "title": "What you can do with Omnimo: AI use cases on iPhone, iPad and Mac",
        "description": "Summarize a PDF, get homework help from a photo, translate, write emails, ask about a photo and "
                       "make images with Omnimo, the AI chat app with GPT-6, Claude, Gemini and more.",
        "h1": "Use cases", "meta": f"Updated {UPDATED_TEXT}", "schema": "CollectionPage",
        "body": p("The things people most often open Omnimo for, and how to do each one.") + "\n" + cards(items),
        "crumbs": [("Omnimo", "index.html"), ("Use cases", "use-cases/index.html")], "llms": "Use cases",
    }


def pages():
    return [hub()] + [page(u) for u in USE_CASES]
