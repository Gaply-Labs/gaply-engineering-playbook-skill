# GEP UI Design Reference

Use this reference when a project needs a UI designed or when `init` records the design
source. It covers where design sits in the process, how a Claude Design package is built,
what to send Claude Design as context, and how design output is archived.

## 1. Order of work

Documentation first, design second, implementation third. The prototype is built from the
product brief and the feature documents, not from a guess about what the product is.

1. Documentation is created or updated (`init`).
2. The UI is designed from that documentation.
3. Feature development starts.

If the project already has a valid design, a Figma or Adobe XD file or a working product,
skip the prototype phase and apply the archive rules in section 5.

## 2. Claude Design project setup

Start from a **blank project with no preset design system**. A starter design system
produces screens that look finished before anyone has decided what the product looks like,
and every later screen inherits those accidental defaults.

Create `masterdoc.html` at the root of the design project. It holds two things:

- the product overview: what the product is, who uses it, the core flow;
- the complete design system: colours and tokens, typography scale, spacing scale,
  components with their states, layout and grid rules, elevation, radii, motion,
  light and dark themes, and the RTL or LTR rules when the product is localised.

`masterdoc.html` also carries the entry point to the prototype: a button that opens the
application preview. When desktop and mobile are separate previews, it carries two
buttons, one for each.

## 3. File structure

| Project scope | Structure |
| --- | --- |
| Web or desktop only | `masterdoc.html` + `pages/` |
| Desktop and mobile | `masterdoc.html` + `desktop/` + `mobile/` |
| Mobile only | `masterdoc.html` + `pages/` |

## 4. Rules every page follows

State this on every page, in the page itself, so the rule survives being opened alone:

> `masterdoc.html` is the only source of truth for design and implementation. Use the
> design system defined there.

The rules it enforces:

- No page defines its own colours, type scale, spacing, or components. A page that needs
  something the design system does not have gets it added to `masterdoc.html` first.
- No page introduces a style inconsistent with `masterdoc.html`.
- Dark mode is included unless the project explicitly says otherwise.
- No real backend, database, or service connection. Everything is mocked.

Pages are filled with **realistic mock data**, not lorem ipsum and not `Item 1, Item 2`.
Names, amounts, dates, and text should look like the real product so that layout problems
show up in the prototype rather than in production.

Pages are **interactive** so the whole flow can be tested click by click: navigation
between screens, forms with validation, modals, dropdowns, tabs, and the full set of UX
states, meaning empty, loading, success, validation error, server error, and permission
error. A static screenshot-like page is not acceptable output.

## 5. Context pack for Claude Design

Send only what changes product understanding and UI decisions. Technical documentation
that does not affect what the user sees costs context and pulls the design toward
implementation detail.

Default pack:

```text
docs/assets/logo.png          (or the project's actual logo file)
docs/00-product-brief.md
docs/02-ai-context.md
docs/07-feature-status.md
docs/features/
brief.md                      (when it carries brand direction, audience, or positioning)
```

Add `docs/ui/` when a previous design round produced anything worth continuing from.

`docs/01-architecture.md` is **not** part of the default pack. Send it only when the
architecture is visible to the user: navigation structure, permissions and roles, data
flow that changes what a screen can show, or a platform constraint that limits the design.

## 6. Archiving design output

Everything the design phase produced lives in the repository under `docs/ui/`, so the
project does not go blind if access to an external tool is lost.

| Design tool | What goes into `docs/ui/` |
| --- | --- |
| Claude Design | The full package: `masterdoc.html` plus `pages/`, or `desktop/` and `mobile/` |
| Figma or Adobe XD | The design link recorded in `docs/ui/README.md` plus screenshots of the key screens |
| Existing product | Screenshots of the key screens plus a note that the product itself is the reference |

For Figma or Adobe XD a link alone is not enough. Screenshots of the key screens are
required, because a link stops working the moment access changes.

`docs/ui/README.md` always records: the design source and its status, the screen
inventory with one status per screen (`pending design`, `designed`, `implemented`), and a
pointer to the flows. Screens named in the brief but not yet designed are listed as
`pending design` rather than omitted.

## 7. Asset generation tools

| Asset | Tool |
| --- | --- |
| Favicon set from a source image | https://favicon.io/favicon-converter/ |
| Mobile app icon set | https://www.digia.tech/tools/app-icon-generator/ |

These are the default recommendations. A project that generates icons through its own
build pipeline records that choice in `docs/04-decisions.md` instead.
