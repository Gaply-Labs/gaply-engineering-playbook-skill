# GEP Precheck Reference

Use this reference for `chk` (both modes) and for the preflight, analysis, and gap-detection stages of `init`.

## 1. Discovery inventory

### 1.1 Project identity

Resolve the Project Name in this order and stop at the first credible hit:

1. the `project=` or `name=` parameter on the command;
2. an explicit user instruction or the current task context;
3. the title or first heading of the brief (`# Brief: Nimbus Notes` yields `Nimbus Notes`) or a `Project Name:` line inside it;
4. package or app metadata: `package.json` name, `pyproject.toml`, `app.json`, Android or iOS display names;
5. repository documentation.

Do not treat generic names such as `new-app`, `test`, `frontend`, `my-project`, or temporary branch names as confirmed product names.

Status:

- `PASS`: a specific name is supported by evidence.
- `MISSING`: no credible name exists. Name the parameter that resolves it: `gep init project="Name"`.
- `UNVERIFIED`: names conflict, for example brief title versus package name. Report both. Use the brief's name for `init` only after the user confirms it.

### 1.2 Requirements source

Resolve in this order:

1. the `source=` parameter;
2. `brief.md`, `BRIEF.md`, `product-brief.md`, `docs/00-product-brief.md`;
3. PRD, requirements, or specification files (`*brief*`, `*prd*`, `*requirement*`, `*spec*`) in Markdown, text, PDF, DOCX, or another readable format, at the root or under `docs/`;
4. requirements supplied directly in the current conversation.

A usable brief explains the product's purpose and at least the primary scope or core flow. A brief that exists but is materially incomplete is `UNVERIFIED`, not `PASS`. `init` still proceeds with it and records what is missing as open questions: scaffolding around an incomplete brief is safe, inventing requirements is not.

### 1.3 Documentation folder

Check `docs/` first, then `doc/` and other obvious documentation folders.

`docs/docs-manifest.md` marks a GEP-initialized project and decides the `chk` mode.

If `docs/` does not exist, report `MISSING - will be created by gep init`.

### 1.4 UI / design source

Look for `docs/ui/`, `ui/`, `design/`, prototype or source packages, Figma or Adobe XD references, and screenshots of key screens.

For a backend or API-only project this item is `N/A` when the brief supports that scope.

Do not claim a UI package is complete because an empty folder exists. A brief that names screens without a design export means `docs/ui/README.md` will list those screens as `pending design`.

Status:

- `PASS`: design files, exports, screenshots, or a prototype package exist in the repository.
- `UNVERIFIED`: only a reference exists (a Figma or XD link) and it cannot be opened from here.
- `MISSING`: nothing on disk and no link; the brief may still name the tool. A `docs/ui/README.md` that lists screens as `pending design` documents this gap; it is not a design source and does not change the status.
- `N/A`: the brief supports a project without a UI.

### 1.5 Brand assets

Four asset kinds are tracked: logo, banner, favicon or app icon set, and OG/social image.

Detect them **by name pattern, not by one exact path**. A project that already has a logo almost never has it at the path the playbook would have chosen, and reporting `MISSING` next to a file the user is looking at destroys trust in the whole report. Recognise an asset when either the file name or the folder name matches:

| Kind | File name contains | Folder name | Extensions |
| --- | --- | --- | --- |
| Logo | `logo`, `logotype`, `logomark`, `wordmark`, `brandmark`, `brand` | `logo/`, `logos/`, `brand/`, `branding/` | png, jpg, svg, webp, avif, gif |
| Banner | `banner`, `hero`, `cover`, `header-image`, `masthead` | `banner/`, `banners/` | same |
| Favicon / app icon | `favicon`, `apple-touch-icon`, `android-chrome`, `mstile`, `safari-pinned-tab`, `site.webmanifest` | `favicon/`, `favicons/`, `icons/`, `app-icon/` | same, plus `.ico` and `.webmanifest` |
| OG / social | `og`, `opengraph`, `social`, `share`, `twitter-card`, `preview`, `card` | `og/`, `social/`, `opengraph/` | same |

Separators count: `company-logo.png`, `logo_dark.svg`, and `Logo.PNG` all match. A whole folder matches too, which is how a seven-file favicon set from a generator is found.

`scripts/gep_scan.py --json` reports this under `assets`, one list per kind, each entry carrying `path`, `placement`, `dimensions`, and `is_placeholder`.

#### Placement decides what `init` may do

| `placement` | Where | What `init` does |
| --- | --- | --- |
| `assets` | `docs/assets/` | Nothing; already correct |
| `docs` | Anywhere else under `docs/` | **Move it into `docs/assets/`**, preserving set folders |
| `app` | `public/`, `static/`, `src/`, `app/`, `assets/`, `www/`, `resources/`, `web/` | Reference only. Moving it would break the build or the served site |
| `other` | Anywhere else | Reference only |

`scripts/organize_assets.py --root . --apply` performs the `docs` moves deterministically and lists every document that mentions a moved file by name so links can be corrected. Run it during `init`, never during `chk` or `pchk`.

#### Status

- `PASS`: a final asset exists, whatever it is called and wherever it legitimately lives.
- `PASS` with `placeholder` in the evidence: a `*-default.*` file stands in for it. Still list it under the report's missing-or-placeholder section.
- `UNVERIFIED`: the file exists but its dimensions or wiring cannot be checked, for example an SVG where a pixel size is required, or an icon set with no application to reference it from.
- `MISSING`: no file matches any pattern.
- `N/A`: the project type does not need it, with the reason. A CLI tool needs no OG image.

The OG image must be exactly 1200x630. Any other size is a finding, not a pass. If dimensions cannot be read, `UNVERIFIED`.

Generate a missing favicon set with https://favicon.io/favicon-converter/ and a missing mobile app icon set with https://www.digia.tech/tools/app-icon-generator/. Recommend the tool rather than producing a fake final asset.

### 1.6 Discovery and platform files

These decide whether the product can be found, crawled, previewed, and installed. They are looked for in served roots only: the repository root, `public/`, `static/`, `app/`, `src/app/`, `www/`, `dist/`, and `docs/`. A `site.webmanifest` sitting in `docs/assets/favicon/` is a source asset, not a served manifest, and the difference matters.

| File | Applies to | Note |
| --- | --- | --- |
| `robots.txt` | Any served site, including authenticated ones | An authenticated app still needs one, to disallow |
| `sitemap.xml` | Public, indexable sites | May be generated at build time; check the build output or config |
| `llms.txt` | Sites that want to be usable by AI agents | Newer convention; recommend, do not treat as blocking unless the brief asks |
| Web app manifest | PWA and installable products | `site.webmanifest`, `manifest.webmanifest`, or `manifest.json` |

`scripts/gep_scan.py --json` reports these under `discovery_files`.

Metadata that lives in code rather than in a file, meaning page title, meta description, canonical URL, Open Graph tags, Twitter Card tags, and Schema.org structured data, is not something the scanner can judge. Read the application's head or metadata configuration and report what is there. Before any application code exists, these are `MISSING`, not `UNVERIFIED`.

## 2. Project type signals

Classify the project before deciding which checks apply. Record the evidence.

| Type | Signals in the brief or repository | Consequences |
| --- | --- | --- |
| Public web app | landing or marketing pages, SEO, public share links, indexable content | SEO, OG/social, W3C, and accessibility checks all apply |
| Authenticated web app | dashboard, sign in, workspace, admin, no public content | SEO items `N/A` with reason; accessibility applies; OG applies only to public pages |
| Mobile app | iOS, Android, React Native, Flutter, app stores | app icon and store metadata replace favicon and SEO |
| Backend or API only | service, API, worker, SDK, no screens | UI archive `N/A`; logo and favicon only if a public surface exists |
| CLI or library | commands, packages, publishing to npm or PyPI | UI `N/A`; identity lives in README and package metadata |
| Hybrid | combinations of the above | apply each part's rules; record the split in `docs/01-architecture.md` |

When signals conflict or are absent, record an open question for the project type and apply the stricter rules until it is resolved.

## 3. Referenced-but-missing signals

Use this table in `chk` Mode B and in `init` step 6.7. A row fires when the brief or product docs mention the signal and the expected location is absent or empty. Product docs means the brief, `docs/00-product-brief.md`, `docs/01-architecture.md`, `docs/features/`, `docs/ui/`, and the root `README.md`; release checklists and agent rules are excluded because they mention every topic by design.

`scripts/gep_scan.py --json` reports the deterministic part as `referenced_but_missing`. Confirm each hit against the brief: a sentence such as "no payments in v1" contains the word without creating a requirement.

| Signal words | Expected location | Default files | Consumed by |
| --- | --- | --- | --- |
| UI, UX, screens, wireframes, mockups, prototype, Figma, Adobe XD, design system | `docs/ui/` | `README.md` (design source, screen inventory, status); the Claude Design package (`masterdoc.html` plus `pages/`, or `desktop/` and `mobile/`) or screenshots, per `references/ui-design.md` | feature docs (UX States), `docs/01-architecture.md` (frontend) |
| logo, brand, branding, identity | `docs/assets/` | `logo-default.svg` until the final logo; an inventory row in `docs/assets/README.md` | `docs/09-release-readiness.md` section 1, public metadata |
| banner, hero image, cover image, masthead | `docs/assets/` | `banner.*`; an inventory row in `docs/assets/README.md` | repository README, marketing surfaces |
| favicon, app icon, launcher icon, touch icon | `docs/assets/` | `favicon-default.svg` until the final set from https://favicon.io/favicon-converter/ | `docs/09-release-readiness.md` section 1, app or build configuration |
| OG image, Open Graph, social preview, share card, link preview | `docs/assets/` | `og-default.png` at exactly 1200x630 until the final `og.png` | `docs/09-release-readiness.md` sections 1 and 3, social metadata |
| API, REST, GraphQL, endpoints, webhooks, SDK, OpenAPI | service boundaries in `docs/01-architecture.md` and the `API / Service Contract` section of each feature doc; `docs/api/` only for spec files | `docs/api/openapi.yaml` when a machine-readable spec exists | `docs/01-architecture.md`, `docs/09-release-readiness.md` section 6 |
| payment, subscription, billing, checkout, Stripe, RevenueCat, MoonPay, in-app purchase | an ADR in `docs/04-decisions.md` naming the provider and a feature doc such as `docs/features/F00x-billing.md` | | `docs/09-release-readiness.md` section 2 |
| auth, login, sign in, sign up, magic link, OAuth, SSO | a feature doc and the authentication part of `docs/01-architecture.md` | | `docs/09-release-readiness.md` sections 4 and 6 |
| mobile, responsive, phone, tablet | mobile-readiness in `docs/01-architecture.md`; responsive states in the design package | app icon set from https://www.digia.tech/tools/app-icon-generator/ | `docs/09-release-readiness.md` section 4 |
| SEO, search engine, indexable, crawler, sitemap, robots.txt, llms.txt | the served root | `robots.txt`, `sitemap.xml`, `llms.txt` | `docs/09-release-readiness.md` section 3 |
| PWA, progressive web app, installable, service worker, offline, add to home screen | the served root | `site.webmanifest` or `manifest.json`, plus the icon sizes it declares | `docs/09-release-readiness.md` sections 1 and 3 |

Write one recommendation per gap in one of these two shapes:

- `Create <path> containing <default files>; consumed by <document or check>.`
- `Replace <placeholder> with <final asset> (<constraints>); consumed by <document or check>.`

Recommendations point at the standard GEP locations above, not at ad hoc folders, so that every project initialized with GEP has the same shape.

## 4. Mode A readiness logic

Block `init` only when:

- the Project Name is missing or conflicting without a safe resolution; or
- no usable brief or requirements source exists.

Every other missing structure or asset is reported as a target that `init` will create, provided creating it needs no invented product requirement.

## 5. Mode B documentation health

Statuses:

- `MISSING`: a required path is absent, or a referenced item has no location.
- `OUTDATED`: a document contradicts repository evidence.
- `UNVERIFIED`: the comparison could not be made (no history, unreadable source).
- `N/A`: the item does not apply to this project type, with the reason.
- `PASS`: present and consistent, with evidence.

Two cases the vocabulary does not cover on its own:

- A placeholder asset that is present and correctly labeled is `PASS`, with `placeholder` in its Evidence cell and "replace with the final asset before release" as its required action. A placeholder is a recorded gap, not a broken document, so it does not by itself make the documentation out of sync.
- When a comparison has no counterpart yet, say the docs describe a stack but no code or manifests exist, the row is `PASS` with `nothing to contradict` in Evidence. Reserve `UNVERIFIED` for a comparison that should have been possible but could not be made, such as missing history for the `HANDOFF.md` and changelog rows.

Compare each document against the repository:

| Document | Compare against | `OUTDATED` when |
| --- | --- | --- |
| `docs/07-feature-status.md` | routes, modules, feature folders, feature docs | implemented features are missing from the table, or `DONE` rows have no code |
| `docs/08-tech-stack.md` | manifests such as `package.json`, `pyproject.toml`, `go.mod`, lock files | a dependency or version is missing or differs |
| `docs/01-architecture.md` | the actual folder tree, configuration, deployment files | the described structure does not match |
| `HANDOFF.md` | recent commits and the changelog | `Last Completed` or `Next Step` predate the latest meaningful change |
| `docs/06-changelog.md` | recent commits | meaningful changes have no entry |
| `docs/05-open-questions.md` | code and decisions | `Blocking: YES` items the code has already answered |
| `docs/09-release-readiness.md` | actual evidence | rows marked `PASS` without evidence |
| `docs/assets/README.md` | files under `docs/assets/` and public asset folders | inventory rows missing, or a placeholder listed as final |
| asset placement | the `assets_misplaced` list from the scanner | any brand asset still loose under `docs/` outside `docs/assets/` |
| discovery files | the served roots | the brief implies a public site but `robots.txt` or `sitemap.xml` is absent |
| `docs/ui/README.md` | implemented screens | screen statuses no longer match the implementation |

Overall: `GEP DOCS IN SYNC` when nothing is `MISSING` or `OUTDATED` and no required-structure item is `UNVERIFIED`; otherwise `GEP DOCS OUT OF SYNC`.
