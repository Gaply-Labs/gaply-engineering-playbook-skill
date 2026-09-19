# GEP Final Checklist Reference

Every `chk`, `init`, and `pchk` run ends with this checklist, and nothing follows it.

The detail lives in the sections above it: tables with evidence, recommendations, open
questions. The checklist exists so a reader who scrolls to the bottom sees the state of
the project in one screen without reconstructing it from prose. Keep it to one line per
item. Move any explanation up into the body.

## Markers

| Marker | Meaning |
| --- | --- |
| `[x]` | Present and correct |
| `[~]` | Present but incomplete, placeholder, or not wired in |
| `[ ]` | Absent |
| `[-]` | Not applicable to this project type, with the reason in the same line |

Use `[~]` for anything that exists but cannot be shipped: a `*-default.*` placeholder, a
favicon set sitting in the repository but never referenced by the application, a document
whose required sections are still `Open`. The difference between `[~]` and `[x]` is what
stops someone from releasing, so do not round `[~]` up.

## Line format

```text
[x] Logo — docs/assets/logo.png
[~] Favicon — set in docs/assets/favicon/, not referenced by the app
[ ] Banner — no file matching a banner pattern
[-] SEO metadata — authenticated-only app, nothing indexable
```

One item, one marker, one short state. No sentences, no evidence paths repeated from the
body unless the path is the whole answer.

## Groups and items

Print the groups in this order. Drop a group only when every item in it is `[-]`, and
then print one line for the group saying why.

### 1. Documentation

- GEP structure (`n/18` required paths present)
- `HANDOFF.md` current
- Product brief
- Architecture
- Feature docs (`n` features, `m` documented)
- Feature status matches the code
- Decisions log
- Open questions (`n` open, `m` blocking)
- Changelog
- Tech stack matches the manifests
- Release readiness gate

### 2. Brand assets

- Logo
- Banner
- Favicon / app icon set
- OG / social image (state the dimensions; anything other than 1200x630 is `[~]`)
- Asset inventory in `docs/assets/README.md` complete
- All assets under `docs/assets/` (list anything still loose elsewhere under `docs/`)

### 3. UI and design

- Design source recorded (`docs/ui/README.md`)
- Screen inventory
- Design package or screenshots archived
- `masterdoc.html` present when the design was built with Claude Design

### 4. Discovery and crawling

- `robots.txt`
- `sitemap.xml`
- `llms.txt`
- Canonical URL
- Structured data / Schema.org

### 5. Metadata and social

- Page title
- Meta description
- Open Graph tags
- Twitter Card tags
- `og:image` resolves to the final 1200x630 asset
- Heading hierarchy (one `h1`, logical `h2`/`h3`)
- Image `alt` text

### 6. Platform and PWA

- Web app manifest (`site.webmanifest` or `manifest.json`)
- Icon sizes the target platforms require
- Theme and background colour
- App store icon set for mobile projects (generate with https://www.digia.tech/tools/app-icon-generator/)

### 7. Engineering (`pchk` only)

- Type check
- Lint
- Unit and integration tests
- E2E for critical flows
- Production build
- Secret scan
- Permissions and security review

### Result

The result is not a numbered group, so that leaving out group 7 outside `pchk` does not
leave a visible gap in the numbering. Repeat the action's overall result string as the
last line, so the checklist and the verdict cannot drift apart:

```text
**Result:** GEP INIT COMPLETE
```

## Applicability by project type

A checklist full of irrelevant rows trains people to skip it. Use the project type
recorded during discovery:

| Project type | Groups 4, 5, 6 |
| --- | --- |
| Public web app | All items apply |
| Authenticated web app | Discovery and social items are `[-]` except `robots.txt`; headings, `alt` text, and the manifest still apply |
| Mobile app | Replace favicon and discovery items with the app icon set and store metadata |
| Backend or API only | Whole groups collapse to one `[-]` line each; documentation and engineering still apply |
| CLI or library | Identity lives in the README and package metadata; discovery and social are `[-]` |

## Status during `chk` and `init`

`chk` and `init` run before the product is finished, so most engineering and metadata
items cannot be verified yet. Mark those `[ ]` when the file or tag is simply absent, and
leave group 7 out entirely outside `pchk`. Never mark an item `[x]` because it is planned.
