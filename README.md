# privateslm.dev — site

Static site: privateSLM landing, circuitAI landing, and the on-device AI blog.

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

## Model & compare pages (SEO)

`models/*.html` are **generated** — never edit by hand. Regenerate whenever
`models.json` changes:

```
python3 scripts/gen_model_pages.py
```

The script also appends any missing `/models/` and `/compare/` URLs to
`sitemap.xml` and refreshes the "## Model pages" section of `llms.txt`.
`compare/*.html` are hand-written; keep every competitor claim verifiable and
update the "Updated <date>" line when facts change.
