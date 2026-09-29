# English edition build (`/en`)

The English site under `en/` is **generated** from the Korean pages. Never edit `en/*.html`
by hand — the next build overwrites it. Edit the Korean page, then rebuild.

## How it works

Each Korean page is scanned for translatable pieces, and each piece is recorded with its exact
character offsets in the original file. The build splices English text back into those exact
ranges, so markup, scripts, styles and whitespace are preserved byte-for-byte — only the words
change. Translations live in `tm.json`, keyed by the original Korean string, so identical text
(the nav, the footer, repeated buttons) is translated once and reused across all pages.

What gets translated: text inside elements, `alt` / `title` / `placeholder` / `aria-label` /
`content` attributes, Korean string literals in inline `<script>`, and JSON-LD values.
Korean in HTML/JS comments is left alone — it never renders.

## Rebuilding

```bash
python3 tools/en-edition/batch.py extract   # rescan the Korean pages
python3 tools/en-edition/batch.py status    # report anything not yet translated
python3 tools/en-edition/batch.py packets   # write packets/pNN.json for the untranslated text
#   ... translate each packets/pNN.json into packets/pNN.out.json (same keys, English values),
#       following GLOSSARY.md, then check each one:
python3 tools/en-edition/validate.py tools/en-edition/packets/p00.json tools/en-edition/packets/p00.out.json
python3 tools/en-edition/batch.py merge     # fold the finished packets into tm.json
python3 tools/en-edition/batch.py apply     # write the en/ tree
```

`extract` must be re-run after **any** edit to a Korean page — the offsets are position-based,
and a stale offset makes `apply` stop with a "segment drift" error rather than corrupt a file.

### Verifying

`render_check.mjs` loads built pages in a real browser and reports Korean that a visitor would
actually see (it reads rendered text, so commented-out markup is excluded by construction):

```bash
python3 -m http.server 8777          # from the site root
cd /path/to/process-gpt/services/frontend   # any checkout with Playwright installed
node render_check.mjs en/index.html en/contents/processgpt.html   # SITE_URL overrides the host
```

## What the build does besides translating

- `html lang`, `og:locale` and JSON-LD `inLanguage` switch to English.
- `canonical`, `og:url` and breadcrumb URLs point at the `/en/` address, and every page gets
  `hreflang` alternates for `ko`, `en` and `x-default`.
- Relative asset paths gain one `../`, because `en/` sits one level deeper.
- **English screenshots**: if `images/en/<same path>` exists, the English page uses it instead of
  the Korean screenshot — including the absolute `og:image` / `twitter:image` URLs. Dropping a
  file into `images/en/...` is all that's needed; no page edit.
- **English videos**: `VIDEO_OVERRIDES` in `apply.py` maps a YouTube id to a locally hosted
  English recording, which replaces that embed on the English side only.
- A KO/EN language switch is inserted into the nav on both sides.
- Links written as `en/contents/x.html` on Korean pages are rewritten to stay inside `en/`.

## Pages deliberately excluded

`contents/consultingMSAcopy.html`, `contents/vibeCodingRental.html`, `contents/openingSoon.html`
and the two `supplychain-risk-before-edit.html` copies. They are orphans, stubs or `noindex`
pre-edit snapshots. They carry no language switch, so nothing links to a page that isn't built.

## Watch out: sitemap.xml and the SEO skill

`sitemap.xml` now lists both trees, each entry carrying `hreflang` alternates. It was produced by
extending the existing file. **`.claude/skills/seo-optimize/apply_seo.py` regenerates
`sitemap.xml` from `seo-meta.json` and does not know about `/en/`** — re-running that skill will
drop every English URL and the alternates. Either teach that script about the English tree or
re-apply the English entries afterwards.

The per-page SEO block in each Korean page is still owned by the SEO skill; the English pages
inherit it through the build, so run the SEO skill first and rebuild `en/` afterwards.
