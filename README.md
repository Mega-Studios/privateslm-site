# privateslm.dev — site

Static site for **Omnimo** (the iOS/Mac AI chat app, App Store id 6504996891, called
privateSLM until October 2026): the landing page, support, privacy policy and the blog.
The domain keeps the old name.

Domain `privateslm.dev` is purchased through Vercel Domains. Hosting is migrating
from GitHub Pages to Vercel to avoid manual DNS config (Vercel domains attach to
Vercel projects with zero DNS records) and to avoid two live copies of the same
site (duplicate content is bad for SEO):

1. Import this repo as a Vercel project (Framework Preset: Other — no build step,
   it's plain static HTML).
2. Project Settings → Domains → add `privateslm.dev`. Since the domain is owned by
   the same Vercel account, it attaches without copying any DNS records.
3. Once the Vercel deployment is confirmed working, disable the GitHub Pages
   deployment for this repo so `privateslm.dev` is the single canonical origin.

## MegaBrain promotion

Every page carries an orange bar across the top ("For business · MegaBrain — Private AI
for your business") that stays in view while the page scrolls, and every blog post ends
with a banner in the same colour. Both come from `scripts/promo.py`:

```
python3 scripts/promo.py
```

The same script puts Safari's Smart App Banner for Omnimo
(`<meta name="apple-itunes-app" content="app-id=6504996891">`) in the `<head>` of every
page. It is idempotent, and `gen_blog_meta.py` calls it when it finishes, so new pages
get all of it without a separate step. `privacy.html` and `support.html` get the Smart
App Banner but no MegaBrain bar. The wording and
the link are in that script; the colours are in `assets/style.css` under "MegaBrain
promotion". A hand-written page needs nothing but `<body>` on its own line.

## Blog posts (SEO)

Every post needs a `<title>`, a meta description, a canonical link and a date in
`<div class="meta">` ("July 20, 2026 · 8 min read"). The rest is generated — run this
after adding or editing a post:

```
python3 scripts/gen_blog_meta.py
```

It writes the Open Graph tags, the Twitter card and the `BlogPosting` structured data
into the post's `<head>` (between the `seo:start` / `seo:end` comments — do not edit
by hand) and adds the post to `sitemap.xml`. The preview image is the first image in
the article, or `assets/og-default.png`. To mark a revision, write
"Updated October 11, 2026" in the meta line.

## Generated pages: compare, models, prompts, guides, translations

```
python3 scripts/gen_pages.py     # write the pages, their .md copies, sitemap and llms.txt
python3 scripts/check_site.py    # links, anchors, markup, JSON-LD, sitemap, hreflang
```

`gen_pages.py` writes these pages from the data in `scripts/pagedata/` (the words live
there; the script only lays them out — do not edit the generated HTML by hand):

| Path | What | Data |
|---|---|---|
| `/facts.html` | the fact sheet: models, prices, limits, privacy, changes | `guides.py` |
| `/compare/` | Omnimo vs ChatGPT, Perplexity, Poe, ChatOn, Genie, Nova, ChatNow, Fello AI, AllChat, TypingMind | `compare.py`, `competitors.py` |
| `/alternatives/` | alternatives to ChatGPT Plus, Poe, ChatOn, the Claude app, Private LLM | `compare.py` |
| `/models/` | every cloud model Omnimo offers, by family, and model-vs-model pages | `models.py` |
| `/use-cases/` | summarize a PDF, homework, translate, email, photo questions, images | `usecases.py` |
| `/prompts/` | the prompt library: 8 categories, 64 prompts | `prompts.py` |
| `/status/` | "Is ChatGPT / Claude / Gemini down?": links to the official status pages, no live status | `status.py` |
| `/best/`, `/guides/` | the best AI chat apps for iPhone; Apple Intelligence with GPT, Claude and Gemini; free offline AI | `guides.py` |
| `/es/ /de/ /fr/ /pt-br/ /ja/` | the home page with its FAQ and five compare pages, with hreflang | `i18n*.py` |

Facts about Omnimo come from the app repo (`appstore/metadata/en-US/`,
`docs/monetization.md`, `gateway/src/catalog.ts`); `models.py` copies the catalog, so
**when the gateway's catalog changes, change `CATALOG` there**. Facts about other apps
are in `competitors.py`, read from their US App Store listings and in-app purchase lists
with the date; re-read them before changing a price. Message counts are never given as
numbers ("a few a day", "hundreds a day"): they change with a gateway deploy. The fact
sheet's JSON-LD is copied from the home page's, so the two can't disagree.

Pages marked `md` also get a Markdown copy next to them (`/facts.md`,
`/compare/omnimo-vs-chatgpt.md`...), as do the home page (`/index.md`) and the rename
post; `llms.txt` lists them in a generated block between `pages:start` and `pages:end`.
`vercel.json` serves `.md` as `text/markdown`.

The prompt pages copy the prompt and link to the App Store. They do not deep-link into
the app: Omnimo declares a `privateslm://` scheme, but only the widget uses it and the
app's `onOpenURL` handles files only, so a link could not carry a prompt.

## The old model pages

The GGUF model pages privateSLM had under `/models/` went with the rename; `vercel.json`
sends each of the 22 old addresses (`/models/*-q4.html`) to
`blog/privateslm-is-now-omnimo.html` with a 301, and `/models/` is now Omnimo's model
list. **`models.json` stays:** privateSLM builds from before the rename fetch it from
`https://www.privateslm.dev/models.json`, and `bench/build_posts.py` reads it.

The four hand-written privateSLM-era compare pages (`compare/*-vs-privateslm.html`,
`offline-ai-chat-iphone.html`, `private-llm-alternatives.html`) compare privateSLM, the
offline app; each carries an archive note, and `llms.txt` lists them under its archive
heading.

## Search engines and assistants

ChatGPT's web search reads Bing's index, so a page Bing has not crawled does not
exist for it.

- `llms.txt` is the site in one text file for assistants, written by hand. Its
  summary, "Facts" and "Questions" must match the app and the App Store (the app
  repo's `appstore/metadata/en-US/` and `docs/monetization.md`): when a price, a
  model family or a minimum OS changes, change it there, in the home page's facts
  table and FAQ, and in the home page's JSON-LD (`SoftwareApplication` and
  `FAQPage`), all four together.
- IndexNow: the key is served at `/b554a11595e2c5a99c976126fb9e55bb.txt`. After a
  deploy, `python3 scripts/indexnow.py` sends the whole sitemap to Bing and the
  other IndexNow engines; `python3 scripts/indexnow.py /compare/x.html` sends one
  page.
- `vercel.json` sends `/circuitai/` to circuitapp.app: CircuitAI became Circuit, an
  app blocker, in September 2026. `circuitai/index.html` does the same for hosts
  without that rule (GitHub Pages).
- `privateslm.app` is not ours. It was registered at GoDaddy on 2026-02-23 by
  someone else and shows a parking page; every domain we own is in Vercel. Never
  link to it — the site is `www.privateslm.dev`.
