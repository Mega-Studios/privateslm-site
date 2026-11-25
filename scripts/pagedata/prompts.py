"""/prompts/ (audit #135): a prompt library to copy into Omnimo.

No "open in Omnimo" deep links: the app declares a URL scheme (privateslm://, in
project.yml) but only uses it for the widget, and its onOpenURL handles files only,
so a link could not carry a prompt in. The pages copy the prompt and link to the
App Store instead.
"""

from .common import UPDATED_TEXT, APP_STORE, cards, ul, p, h2

CATEGORIES = [
    ("writing", "Writing", "Rewrite, shorten, proofread and draft: prompts for everyday writing."),
    ("email", "Email", "Replies, follow-ups and hard emails, drafted in the right tone."),
    ("study", "Study", "Understand a problem, test yourself and plan your revision."),
    ("documents", "Documents", "Attach a PDF, Word, Excel, PowerPoint or Pages file and get what you need from it."),
    ("photos", "Photos", "Take or choose a photo and ask about it."),
    ("language", "Languages", "Translate, practise and correct, in the tone you need."),
    ("work", "Work and planning", "Plans, decisions, meetings, code and spreadsheets."),
    ("images", "Images", "Descriptions that get good images from the image models."),
]

# (slug, title, why, prompt, tips, needs) — needs: None, "photo", "document" or "image"
PROMPTS = {
    "writing": [
        ("rewrite-clearer", "Rewrite a text so it is clearer", "Keeps your meaning, removes the fog.",
         "Rewrite the text below so it is clear and easy to read. Keep my meaning and my facts, use short sentences "
         "and plain words, and keep it about the same length. Then list the three biggest changes you made.\n\n"
         "Text:\n[paste your text]",
         ["Say who will read it: \"for customers\", \"for my manager\".", "Ask for two versions if you can't decide."], None),
        ("shorten-text", "Cut a text to half its length", "For posts, bios and messages with a limit.",
         "Shorten the text below to about [number] words. Keep the main point and any numbers, dates and names. "
         "Cut repetition and filler first. Don't add anything new.\n\nText:\n[paste your text]",
         ["Give a hard limit in characters for X or SMS.", "Ask which sentence it would cut next."], None),
        ("proofread", "Proofread and explain the fixes", "Catches mistakes and tells you why.",
         "Proofread the text below. Fix spelling, grammar and punctuation, and nothing else. Show the corrected "
         "text, then a list of each change with a short reason.\n\nText:\n[paste your text]",
         ["Say which variety of English: US or UK.", "Add \"keep my style\" if it starts rewriting."], None),
        ("cover-letter", "Write a cover letter for a job", "A first draft that fits the job, not a template.",
         "Write a cover letter for this job. Use only facts from my background, don't invent experience. Keep it "
         "under 300 words, open with why this role, and end with a clear next step.\n\nJob ad:\n[paste the job ad]\n\n"
         "My background:\n[paste your CV or a few lines about you]",
         ["Attach your CV as a PDF instead of pasting it.", "Ask for a version that is more confident."], None),
        ("social-post", "Turn an idea into a social post", "One idea, written for one platform.",
         "Write a [LinkedIn / Instagram / X] post about [your idea]. Audience: [who]. Open with one strong line, "
         "keep it under [number] words, no hashtags in the text, and end with a question to invite replies. Give me "
         "three versions with different openings.",
         ["Paste a post you liked as an example of the tone.", "Ask it to cut the clichés."], None),
        ("blog-outline", "Outline a blog post", "Structure first, so the writing is easy.",
         "Outline a blog post titled \"[title]\" for [audience]. Give me a one-sentence promise for the reader, "
         "five to seven section headings with two bullet points each, and the one fact or example each section "
         "needs. Mark anything I should check.",
         ["Ask for the intro paragraph next.", "A flagship model is worth it for a long piece."], None),
        ("toast-speech", "Write a short toast or speech", "Warm, personal, and the right length.",
         "Write a [two]-minute toast for [occasion] about [person]. Use these details: [three or four true "
         "stories or traits]. Keep it warm and a little funny, nothing embarrassing, and end with a toast line. "
         "Mark where to pause.",
         ["Read it aloud and ask it to cut what sounds stiff.", "Ask for a shorter version as a backup."], None),
        ("product-description", "Write a product description", "Benefits first, facts kept.",
         "Write a product description for [product] for [where it will appear]. Facts: [features, sizes, "
         "materials, price]. Lead with what it does for the buyer, keep every fact exact, and write a 20-word "
         "version too.",
         ["Add a photo of the product for details it can see.", "Ask for SEO keywords to include."], None),
    ],
    "email": [
        ("polite-decline", "Decline politely", "Say no and keep the relationship.",
         "Write a short, polite email declining [the request]. Thank them, give a brief reason [or no reason], "
         "and [suggest an alternative / leave the door open]. Friendly but clear; no apology spiral.\n\n"
         "Their email:\n[paste it]",
         ["Say how well you know them.", "Ask for a more formal version."], None),
        ("follow-up", "Follow up without being pushy", "A nudge that gets an answer.",
         "Write a short follow-up email about [topic]. I wrote on [date] and haven't heard back. Remind them of the "
         "one thing I need, make it easy to answer (a yes/no or a date), and keep it friendly. Under 80 words.",
         ["Paste your first email for context.", "Ask for a second, firmer follow-up for later."], None),
        ("reply-to-complaint", "Reply to a complaint", "Calm, specific, and fair.",
         "Write a reply to this customer complaint. Acknowledge the problem in their words, apologise for what we "
         "got wrong (not for what we didn't), say exactly what we will do and by when: [your fix]. No jargon, no "
         "excuses.\n\nComplaint:\n[paste it]",
         ["Say what you can and can't offer.", "Ask it to check the tone is not defensive."], None),
        ("ask-for-raise", "Ask for a raise or a review", "Confident, with the facts up front.",
         "Help me write an email to my manager asking for a meeting about my pay. Facts: [results, new "
         "responsibilities, market data]. Keep it short and confident, ask for a meeting rather than a number in "
         "the email, and suggest two times.",
         ["Ask it to play your manager and push back.", "Keep the numbers for the meeting."], None),
        ("intro-email", "Introduce two people", "A double opt-in intro that people answer.",
         "Write an email introducing [person A] to [person B]. Why they should talk: [reason]. Two lines about each, "
         "one clear suggestion for what to do next, and make it easy for either to say no.",
         ["Ask for the short message to check first that both are happy."], None),
        ("apology-email", "Apologise for a mistake", "Own it, fix it, move on.",
         "Write an apology email for [what happened]. Say what went wrong in one sentence, take responsibility "
         "without over-explaining, say what I'm doing to fix it and to stop it happening again: [steps]. Under 120 "
         "words.",
         ["Ask it to remove anything that sounds like an excuse."], None),
        ("meeting-request", "Ask for a meeting", "Clear purpose, easy yes.",
         "Write an email asking [person] for a [30]-minute meeting about [topic]. Say why it matters to them, what "
         "I'd like to leave with, and offer [two or three times]. Short and specific.",
         ["Add an agenda of three bullets for a busy reader."], None),
        ("thank-you-note", "Write a thank-you note", "Specific thanks people remember.",
         "Write a short thank-you note to [person] for [what they did]. Mention the specific difference it made: "
         "[detail]. Warm, not gushing, three to five sentences.",
         ["Say whether it is a card, an email or a message."], None),
    ],
    "study": [
        ("explain-step-by-step", "Explain a problem step by step", "Understand it, don't just copy it.",
         "Explain how to solve this problem step by step. Number the steps, say why each one is done, and don't "
         "skip arithmetic. At the end, check the answer a second way.\n\nProblem:\n[type it, or attach a photo]",
         ["Attach a photo of the worksheet.", "Ask a second model to check the answer."], "photo"),
        ("quiz-me", "Quiz me on a topic", "Active recall beats rereading.",
         "Quiz me on [topic] at [level]. Ask one question at a time, wait for my answer, tell me if I'm right and "
         "why, and make the next question harder when I get it right. Ten questions, then a summary of what to "
         "review.",
         ["Attach your notes so the questions match your course."], None),
        ("explain-like-im-12", "Explain something simply", "A plain-language first pass.",
         "Explain [topic] as if I were 12. Use one everyday comparison, no jargon, and under 150 words. Then give me "
         "the same explanation at university level, so I can see what the simple one left out.",
         ["Ask for a drawing idea to remember it."], None),
        ("flashcards", "Make flashcards from notes", "Ready to copy into a flashcard app.",
         "Turn the notes below into [20] flashcards. One fact per card, question on the front, short answer on the "
         "back, as a two-column table. Skip anything that isn't in the notes.\n\nNotes:\n[paste or attach]",
         ["Attach a PDF of the chapter.", "Ask for the cards as \"front;back\" lines."], "document"),
        ("essay-feedback", "Get feedback on an essay", "Feedback like a strict teacher's.",
         "Give feedback on this essay as a strict teacher would. The question was: [question]. Score it on argument, "
         "evidence, structure and style out of 5 each, quote the weakest sentence and suggest a better one, and list "
         "the three changes that would raise the grade most. Don't rewrite it for me.\n\nEssay:\n[paste or attach]",
         ["Paste the marking criteria if you have them."], "document"),
        ("study-plan", "Make a study plan", "From today to the exam, day by day.",
         "Make a study plan for [exam] on [date]. I can study [hours] a day, except [days]. Topics: [list], and I'm "
         "weakest at [topics]. Give a day-by-day table with a review day each week and a practice test before the end.",
         ["Ask it to adjust when you fall behind."], None),
        ("summarize-chapter", "Summarize a chapter", "The key ideas, terms and questions.",
         "Summarize this chapter for revision: the five key ideas in one sentence each, the terms I must know with "
         "definitions, and three exam-style questions with short answers.\n\n[attach the chapter or paste it]",
         ["Attach a scan of the pages: Omnimo reads it on the device."], "document"),
        ("check-my-answer", "Check my answer", "Find the mistake, not just the right answer.",
         "Here is a problem and my answer. Tell me whether my answer is right. If it isn't, find the first step where "
         "I went wrong and explain the mistake, without solving the rest for me.\n\nProblem:\n[problem]\n\nMy "
         "working:\n[your steps, or attach a photo]",
         ["A photo of your handwritten working works well."], "photo"),
    ],
    "documents": [
        ("summarize-document", "Summarize a document", "The point of a long file, fast.",
         "Summarize the attached document in five bullet points, then one sentence on what it asks me to do, if "
         "anything. Quote the page or section for each point.",
         ["Ask follow-up questions in the same chat.", "For long files, a Pro model reads it in one go."], "document"),
        ("contract-red-flags", "Find the red flags in a contract", "What to ask about before you sign.",
         "Read the attached contract and list anything I should question before signing: automatic renewals, "
         "cancellation terms, fees, liability, deadlines and anything unusual. Quote each clause and explain it in "
         "plain words. This is not legal advice; tell me what to ask a lawyer.",
         ["AI can miss things: read the clauses it quotes yourself."], "document"),
        ("extract-dates", "Pull out every date and deadline", "Never miss a deadline buried in a PDF.",
         "List every date, deadline and time period in the attached document as a table: the date, what happens, "
         "and the section it comes from. Put them in date order and flag anything within the next 30 days of [today's date].",
         ["Ask for the table as calendar-ready text."], "document"),
        ("spreadsheet-insights", "Find what a spreadsheet says", "Trends and outliers without a pivot table.",
         "Look at the attached spreadsheet. Tell me what the columns mean, the three most important trends, any "
         "numbers that look wrong or unusual, and one chart that would show the main point. Say which rows you used.",
         ["Ask a follow-up about one column.", "Check the totals it quotes against the sheet."], "document"),
        ("action-items", "Turn notes into action items", "Who does what, by when.",
         "From the attached meeting notes, list every action item as a table: what, who, by when. Then list "
         "decisions made and open questions. Mark anything without an owner.",
         ["Paste notes as text if they're in another app."], "document"),
        ("explain-a-bill", "Explain a bill or statement", "Every line in plain words.",
         "Explain the attached bill line by line in plain words. Tell me what I'm paying for, anything that changed "
         "from what's normal, and any fee I could ask to remove. Don't guess at numbers you can't read.",
         ["Take a photo or scan of a paper bill."], "document"),
        ("plain-language", "Rewrite a document in plain language", "Legal or technical text, made readable.",
         "Rewrite the attached document in plain language for someone with no background in [field]. Keep every "
         "obligation, number and date. Put the most important thing first. Under [number] words.",
         ["Ask for the original wording next to each point you're unsure about."], "document"),
        ("slide-deck-summary", "Get the key points of a slide deck", "The story of a PowerPoint in a minute.",
         "Read the attached presentation. Give me its main message in one sentence, the key point of each slide in "
         "one line, and three questions the audience is likely to ask.",
         ["Works with PowerPoint and Keynote exported to PDF."], "document"),
    ],
    "photos": [
        ("what-is-this", "What is this?", "Identify a thing from a photo.",
         "What is this? Tell me what it is, what it's used for, and how sure you are. If you're not sure, say what "
         "else it could be and what would tell them apart.\n\n[attach a photo]",
         ["Take a second photo from another angle if it's unsure."], "photo"),
        ("fix-it", "How do I fix it?", "From a photo of the problem to steps.",
         "This is [what it is] and it [what's wrong]. Look at the photo and tell me the most likely cause, what I "
         "need, and the steps to fix it safely. Tell me when I should call a professional instead.\n\n[attach a photo]",
         ["Include a photo of any label or model number."], "photo"),
        ("read-label", "Read a label and explain it", "Ingredients, care labels, instructions.",
         "Read the label in this photo and explain it in plain words: what it says, anything I should watch out "
         "for, and [my question, e.g. is it suitable for someone with a nut allergy]. Say if any text is hard to read.\n\n"
         "[attach a photo]",
         ["Check anything health-related with the maker or a pharmacist."], "photo"),
        ("identify-plant", "Identify a plant and how to care for it", "Name, light, water, problems.",
         "What plant is this, and how do I look after it indoors in [climate or room]? Light, watering, soil, and "
         "what the [yellow leaves / spots] in the photo might mean.\n\n[attach a photo]",
         ["A close-up of a leaf helps."], "photo"),
        ("fridge-recipe", "Cook something from what's in the fridge", "A recipe from a photo of your shelves.",
         "Here is what's in my fridge. Suggest three dishes I can make in under [30] minutes with mostly these "
         "ingredients, plus basics like oil, salt and spices. For the first one, give the recipe step by step.\n\n"
         "[attach a photo]",
         ["Say what you don't eat."], "photo"),
        ("explain-chart", "Explain a chart", "What a graph actually shows.",
         "Explain this chart: what it measures, the main trend, anything surprising, and one thing it doesn't tell "
         "us. Quote the numbers you read from it.\n\n[attach a photo or screenshot]",
         ["Ask whether the axes could mislead."], "photo"),
        ("handwriting-to-text", "Turn handwriting into text", "Notes, letters and recipes, typed out.",
         "Type out the handwriting in this photo exactly. Mark any word you can't read as [?]. Then, separately, "
         "tidy it into clean notes.\n\n[attach a photo]",
         ["Good light and a flat page help most."], "photo"),
        ("error-on-screen", "Explain an error on a screen", "A screenshot to a fix.",
         "This error appeared on my [device or app]. What does it mean, what usually causes it, and what should I "
         "try, in order from simplest to most involved?\n\n[attach a screenshot or photo]",
         ["Say what you did just before it appeared."], "photo"),
    ],
    "language": [
        ("translate-keep-tone", "Translate and keep the tone", "Not just the words: the register.",
         "Translate the text below into [language]. Keep the tone [formal / friendly / funny], use natural phrasing "
         "a native speaker would use, and list anything that doesn't translate directly with how you handled it.\n\n"
         "Text:\n[paste it]",
         ["Say the country: Brazilian or European Portuguese, Latin American or Spain Spanish."], None),
        ("translate-photo", "Translate a sign or menu from a photo", "Travel without a phrasebook.",
         "Translate everything in this photo into [language]. For a menu, explain any dish I might not know and "
         "mark what contains [meat / nuts / pork].\n\n[attach a photo]",
         ["Ask how to pronounce what you want to order."], "photo"),
        ("practice-conversation", "Practice a conversation", "A patient partner who corrects you.",
         "Let's practise [language] at [level]. You are [a waiter / a colleague / a shop assistant] in [situation]. "
         "Speak only [language], keep your lines short, and after each of my replies, correct my mistakes in one line "
         "in English before you answer.",
         ["Use voice input to practise speaking.", "Turn on spoken answers to practise listening."], None),
        ("correct-my-grammar", "Correct my grammar and explain", "Learn from your own mistakes.",
         "Correct this text I wrote in [language]. Show the corrected version, then a list of my mistakes grouped by "
         "type, with the rule in one line each.\n\nText:\n[paste it]",
         ["Ask for five exercises on your most common mistake."], None),
        ("explain-idiom", "Explain an idiom or slang", "What it means and when to use it.",
         "What does \"[phrase]\" mean in [language]? Give the meaning, where and with whom it's OK to use it, two "
         "example sentences, and the closest equivalent in [your language].",
         ["Ask whether it sounds dated."], None),
        ("vocabulary-list", "Build a vocabulary list for a topic", "The words you'll actually need.",
         "Give me the 30 most useful [language] words and phrases for [topic, e.g. a doctor's visit], as a table: "
         "word, pronunciation, meaning, example sentence. Most useful first.",
         ["Turn it into flashcards with the study prompt."], None),
        ("formal-informal", "Make a message formal or informal", "The same message, the right register.",
         "Rewrite this [language] message in two versions: one formal, for [someone you don't know], and one "
         "informal, for [a friend]. Explain the main differences.\n\nMessage:\n[paste it]",
         ["Useful for languages with formal \"you\": Sie, usted, vous."], None),
        ("phrasebook-trip", "Make a phrasebook for a trip", "Short, practical, with pronunciation.",
         "Make a one-page phrasebook in [language] for a trip to [place]: greetings, directions, food, shopping, "
         "emergencies. Ten phrases per section, with simple pronunciation for an English speaker.",
         ["Apple Intelligence can translate offline on supported devices once you're there."], None),
    ],
    "work": [
        ("meeting-agenda", "Write a meeting agenda", "Meetings that end on time.",
         "Write an agenda for a [45]-minute meeting about [topic] with [who]. The goal is [decision or outcome]. "
         "Give timed items, who leads each, what to read beforehand, and the decision we need by the end.",
         ["Ask for the invite text too."], None),
        ("project-plan", "Plan a project", "Milestones, risks and a first week.",
         "Help me plan [project] due [date] with [people / budget]. Give milestones with dates, the riskiest part and "
         "how to reduce the risk, and a task list for the first week. Ask me three questions first if something "
         "important is missing.",
         ["A flagship model is worth it for a big plan."], None),
        ("pros-and-cons", "Weigh pros and cons", "A clearer head before a decision.",
         "I'm deciding whether to [decision]. My situation: [details]. List the pros and cons, the questions I should "
         "answer before deciding, and what would make each option clearly better. Don't decide for me.",
         ["Ask a second model for its view in the same chat."], None),
        ("brainstorm-names", "Brainstorm names", "Many options, then a short list.",
         "Brainstorm 30 names for [product / business / project]. It is [description], for [audience], and should "
         "feel [adjectives]. Mix styles: descriptive, invented, short. Then pick your top five and say why.",
         ["Check trademarks and domains yourself before you choose."], None),
        ("decision-matrix", "Compare options in a table", "Score options against what matters.",
         "Compare these options: [A, B, C]. Criteria that matter to me, with weights: [criterion and weight]. Make a "
         "table scoring each option 1–5 per criterion, show the weighted total, and say what would change the result.",
         ["Give it real prices and specs; it will say what it is assuming."], None),
        ("explain-code", "Explain a piece of code", "What it does, line by line.",
         "Explain what this code does, step by step, for someone who knows [language] basics. Then point out any bugs "
         "or edge cases, and suggest one improvement.\n\n```\n[paste the code]\n```",
         ["Attach a screenshot if the code is in a picture."], None),
        ("write-spreadsheet-formula", "Write a spreadsheet formula", "Excel, Numbers or Google Sheets.",
         "Write a [Excel / Numbers / Google Sheets] formula that [what it should do]. My data: column [A] has "
         "[what], column [B] has [what], rows [2 to 100]. Explain how it works and how to adapt it.",
         ["Attach the spreadsheet so it sees your columns."], None),
        ("job-interview-practice", "Practise a job interview", "Questions, then honest feedback.",
         "Interview me for [role] at [company type]. Ask one question at a time, mixing behavioural and role-specific "
         "questions. After each answer, give one strength and one thing to improve, then the next question. Eight "
         "questions in total.",
         ["Use voice input and answer out loud."], None),
    ],
    "images": [
        ("product-photo", "A clean product photo", "A studio-style shot from a description.",
         "A studio product photo of [product], centred on a [white / soft beige] background, soft diffused light from "
         "the left, gentle shadow, sharp focus, no text, no logo.",
         ["Change one thing at a time when you retry.", "Say the shape: square for a shop, tall for a story."], "image"),
        ("illustration-style", "An illustration in a style", "Pick a style, keep it consistent.",
         "An illustration of [scene] in a [watercolor / flat vector / ink sketch / 3D clay] style, [colour palette] "
         "colours, [mood] mood, simple background, no text.",
         ["Reuse the same style words for a series."], "image"),
        ("logo-ideas", "Logo ideas", "Explore directions before a designer.",
         "A simple flat logo for [name], a [business type]. A single [symbol idea] mark, two colours, [colours], on "
         "white, clean geometric shapes, no text.",
         ["Image models are poor at lettering: add the name yourself.", "Treat it as a sketch, not a final logo."], "image"),
        ("birthday-card", "A birthday card picture", "A personal card in a minute.",
         "A cheerful birthday card illustration for [name], who loves [hobby or thing], bright colours, playful "
         "hand-drawn style, space at the top for a message, no text.",
         ["Add the message yourself after."], "image"),
        ("social-banner", "A banner for a social post", "A header image that fits the post.",
         "A wide banner image about [topic] for a [LinkedIn / YouTube] header, modern minimal style, [brand colours], "
         "abstract shapes, plenty of empty space on the [left] for text, no text.",
         ["Ask for the wide format in the app if it offers one."], "image"),
        ("app-icon", "An app icon idea", "A rounded-square icon concept.",
         "An app icon for [app idea]: a single bold [symbol] on a [colour] gradient, rounded square, flat, centred, "
         "high contrast, no text.",
         ["Try three colour gradients and compare."], "image"),
        ("poster", "A poster for an event", "Eye-catching art for a flyer.",
         "Poster art for [event], [style, e.g. retro 70s / bold Swiss / neon], featuring [main image], strong "
         "composition, [colours], leave the bottom third plain for text, no text.",
         ["Add the date and place in a design app; image models misspell."], "image"),
        ("photo-to-style", "Restyle a photo", "Your photo in a new style with photo filters.",
         "Use Photo filters in Explore: choose a photo, then pick a style. If you'd rather describe it, ask in a chat: "
         "\"Make an illustration inspired by this photo, in a [style] style.\"",
         ["The photo you restyle goes to fal.ai, which runs the model."], "image"),
    ],
}

HOW = {
    None: "Open a new chat in Omnimo, paste the prompt, replace the parts in [brackets] and send. The free models "
          "handle this well; for something long or important, switch to a flagship and compare.",
    "photo": "In a chat in Omnimo, tap the camera or photo button and add the photo, then paste the prompt and fill "
             "in the [brackets]. The photo goes to a model that can see it, without its location.",
    "document": "In a chat in Omnimo, attach the file (PDF, Word, Excel, PowerPoint, Pages or a scan), then paste the "
                "prompt. The file is read on your device; its text goes to the model you picked.",
    "image": "In Omnimo, open Explore and pick Generate image, or ask in a chat, and paste the description. Images use "
             "credits: one image a day is free, Pro includes credits every period.",
}

COPY_JS = ("<script>document.querySelectorAll('button.copy').forEach(function(b){b.addEventListener('click',"
           "function(){var t=document.getElementById(b.dataset.for).innerText;navigator.clipboard.writeText(t)"
           ".then(function(){b.textContent='Copied';setTimeout(function(){b.textContent='Copy prompt'},1600)})})})"
           "</script>")


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def prompt_page(cat, label, item, siblings):
    slug, title, why, prompt, tips, needs = item
    related = [f'<a href="/prompts/{cat}/{s[0]}.html">{s[1]}</a>' for s in siblings if s[0] != slug][:5]
    body = "\n".join([
        p(why),
        h2("The prompt"),
        f'    <pre class="prompt"><code id="prompt-text">{esc(prompt)}</code></pre>',
        '    <p><button class="copy" type="button" data-for="prompt-text">Copy prompt</button></p>',
        h2("Tips"),
        ul(tips),
        h2("Use it in Omnimo"),
        p(HOW[needs]),
        h2(f"More {label.lower()} prompts"),
        ul(related + [f'<a href="/prompts/{cat}/">All {label.lower()} prompts</a>']),
        "    " + COPY_JS,
    ])
    return {
        "path": f"prompts/{cat}/{slug}.html", "title": f"{title}: a ready prompt for ChatGPT, Claude or Gemini — Omnimo",
        "description": f"{why} A prompt to copy into Omnimo, or any AI chat: {title.lower()}.",
        "h1": title, "meta": f"Prompt library · {label}", "body": body, "llms": None,
        "crumbs": [("Omnimo", "index.html"), ("Prompts", "prompts/index.html"), (label, f"prompts/{cat}/index.html"),
                   (title, f"prompts/{cat}/{slug}.html")],
    }


def category_page(cat, label, blurb):
    items = [(f"/prompts/{cat}/{s[0]}.html", label, s[1], s[2]) for s in PROMPTS[cat]]
    return {
        "path": f"prompts/{cat}/index.html", "title": f"{label} prompts for AI chat — Omnimo prompt library",
        "description": f"{blurb} Ready prompts to copy into Omnimo or any AI chat.",
        "h1": f"{label} prompts", "meta": f"Prompt library · {len(items)} prompts", "schema": "CollectionPage",
        "body": p(blurb + " Copy one, fill in the [brackets] and send.") + "\n" + cards(items),
        "crumbs": [("Omnimo", "index.html"), ("Prompts", "prompts/index.html"), (label, f"prompts/{cat}/index.html")],
        "extra_ld": [{"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i, "name": s[1], "url": f"https://www.privateslm.dev/prompts/{cat}/{s[0]}.html"}
            for i, s in enumerate(PROMPTS[cat], start=1)]}],
    }


def index_page():
    total = sum(len(v) for v in PROMPTS.values())
    items = [(f"/prompts/{c}/", f"{len(PROMPTS[c])} prompts", label, blurb) for c, label, blurb in CATEGORIES]
    body = "\n".join([
        p(f"{total} ready prompts for everyday jobs: writing, email, study, documents, photos, languages, work and "
          "images. Copy one, paste it into a chat in Omnimo, fill in the parts in [brackets] and send. They work in "
          "any AI chat app too."),
        cards(items),
        h2("How to write a good prompt"),
        ul(["Say who it is for and what it is for.", "Give the facts it must use, and tell it not to invent others.",
            "Ask for a format: bullet points, a table, a word limit.",
            "Refine in the same chat: \"shorter\", \"more formal\", \"another option\".",
            "Not sure about an answer? Ask a second model in the same chat."]),
        p(f'Omnimo is free on the <a href="{APP_STORE}">App Store</a> for iPhone, iPad and Mac.'),
    ])
    return {
        "path": "prompts/index.html", "title": f"AI prompt library: {total} ready prompts — Omnimo",
        "description": f"{total} ready prompts for writing, email, study, documents, photos, languages, work and images, "
                       "to copy into Omnimo or any AI chat app.",
        "h1": "Prompt library", "meta": f"Updated {UPDATED_TEXT} · {total} prompts", "schema": "CollectionPage",
        "body": body, "llms": "Prompt library", "md": True,
        "crumbs": [("Omnimo", "index.html"), ("Prompts", "prompts/index.html")],
    }


def pages():
    out = [index_page()]
    for cat, label, blurb in CATEGORIES:
        out.append(category_page(cat, label, blurb))
        for item in PROMPTS[cat]:
            out.append(prompt_page(cat, label, item, PROMPTS[cat]))
    return out
