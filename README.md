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

## Model & compare pages

The `/models/` pages described the GGUF models privateSLM ran on the device. They went
with the rename (Omnimo has no downloadable models), and `vercel.json` sends `/models/`
and every page under it to `blog/privateslm-is-now-omnimo.html` with a 301.
**`models.json` stays:** privateSLM builds from before the rename fetch it from
`https://www.privateslm.dev/models.json`, and `bench/build_posts.py` reads it.

`compare/*.html` are hand-written and still compare privateSLM, the offline app;
`llms.txt` lists them under its archive heading until they are rewritten for Omnimo.

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
