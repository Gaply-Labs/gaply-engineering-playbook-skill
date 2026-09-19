# Gaply Engineering Playbook

> **In one sentence:** every project must be built so that a new person or a new AI can read the documentation alone, without the previous developer, and understand what the product is, what has been built, why the decisions were made, and exactly what comes next.

راهنمای فارسی: [Gaply-Engineering-Playbook.fa.md](Gaply-Engineering-Playbook.fa.md)

## What this document is for

Goals:

- Ship products quickly with AI assistance
- Stop a project from depending on any one person
- Make handover to a new developer cheap
- Give humans and AI a shared source of truth
- Keep architecture able to grow from web to mobile
- Reduce the errors that come from changing code without changing documentation

**Audience:** developers, product managers, designers, CTOs, and AI coding agents (Claude Code, Codex and similar).

**Scope:** every Gaply project. Web apps, PWAs, mobile apps, backends and APIs, new projects, and existing projects under Gaply maintenance.

This playbook is complete on its own. The `gaply-engineering-playbook` Agent Skill automates it, but nothing here requires the skill: a team that reads this file gets the same standard.

---

## Quick start: where should I read?

| Your situation | Path |
| --- | --- |
| I am new and taking over a project | Section 4 + Prompt B |
| I am starting a new project | Section 5 + Prompt A |
| I am working on a feature | Sections 5 and 6 + Prompt C |
| I am designing the UI | Sections 8 and 9 + Prompt E |
| I am standardising a legacy project | Section 15 + Prompt D |
| I am preparing a release | Sections 10 and 16 |

---

# 1. Non-negotiable principles

## 1.1 A project depends on no individual

At any moment the project must be transferable from developer A to developer B without a multi-hour explanation meeting. Reading the documentation alone must answer: what the product is, why it is being built, what is finished, what is in progress, and what comes next.

## 1.2 Documentation is part of development

A feature is **Done** when:

- its code is complete
- the required tests run and pass
- the feature document is up to date
- the feature status has changed
- `HANDOFF.md` is updated
- any significant new decision is recorded in the decision log

**Code whose documentation is stale is not complete by the Gaply standard.**

## 1.3 AI is an executing member of the team, not the source of truth

AI can write code, propose architecture, produce tests and documentation, refactor, and analyse the project. But it:

- does not invent new requirements
- does not make business decisions on its own
- does not change anything outside the defined scope

When something is ambiguous, the AI:

1. records the question in `docs/05-open-questions.md`
2. asks the developer or product owner
3. records the answer in the relevant file, then continues

## 1.4 Architecture is not over-engineered

Clean architecture is a guiding principle, not a ritual. A two-day prototype does not get twelve layers and forty interfaces.

The measure:

> The least architecture that keeps change, testing, ownership transfer, and product growth safe.

---

# 2. Standard documentation structure

Every project has this structure:

```text
HANDOFF.md                    ← at the project root

docs/
├── README.md
├── docs-manifest.md
├── 00-product-brief.md
├── 01-architecture.md
├── 02-ai-context.md
├── 03-project-memory.md
├── 04-decisions.md
├── 05-open-questions.md
├── 06-changelog.md
├── 07-feature-status.md
├── 08-tech-stack.md
├── 09-release-readiness.md
├── features/
│   ├── F001-authentication.md
│   └── F002-dashboard.md
├── ui/                       ← design output (section 8)
│   ├── README.md
│   ├── masterdoc.html
│   └── pages/  or  desktop/ + mobile/
└── assets/                   ← brand assets (section 9)
    ├── README.md
    ├── logo.*
    ├── banner.*
    ├── favicon/
    └── og.png
```

## 2.1 What each file holds

| File | Contents |
| --- | --- |
| **HANDOFF.md** | Live project state: active feature, current task, last completed work, next step, blockers |
| **docs-manifest.md** | Inventory and status of every documentation artifact |
| **00-product-brief.md** | The human summary: what it is, what problem it solves, who uses it, core flow, scope and out of scope |
| **01-architecture.md** | Frontend and backend stack, database, auth, storage, folder structure, security boundaries, deployment, mobile readiness |
| **02-ai-context.md** | Rules for AI working on this project: coding rules, scope limits, dependency policy, what is forbidden |
| **03-project-memory.md** | Context invisible in the code: client constraints, why choices were made, priorities |
| **04-decisions.md** | Architecture and product decisions (ADRs), append-only |
| **05-open-questions.md** | Open ambiguities: question, related feature, owner, status, blocking or not |
| **06-changelog.md** | Significant product, architecture, and behaviour changes. Not a replacement for git history |
| **07-feature-status.md** | Status table for every feature |
| **08-tech-stack.md** | Tools, versions, reasons, alternatives |
| **09-release-readiness.md** | The release gate: identity and brand, payment, SEO and discovery, accessibility, humanisation, engineering |
| **features/Fxxx-name.md** | The full document for each feature (section 2.3) |
| **ui/** | Design output: the Claude Design package, or a design link plus screenshots (section 8) |
| **assets/** | Brand assets: logo, banner, favicon or app icon set, OG image (section 9) |

## 2.2 HANDOFF.md, the most operational file

Updated after every meaningful working session:

```markdown
# HANDOFF

## Current Phase
MVP — Sprint 3

## Active Feature
F003 — Document Analysis (IN_PROGRESS)

## Current Task
Implement upload validation

## Last Completed
Upload UI + storage adapter

## Next Step
Add tests and update feature documentation

## Read First
- docs/features/F003-document-analysis.md
- docs/04-decisions.md (ADR-009)

## Blockers
- Q-014: coverage reference unclear
```

## 2.3 Feature document template

Each feature gets its own file, `docs/features/F001-authentication.md`:

```markdown
# F001 — Authentication

## Status
PLANNED | READY | IN_PROGRESS | BLOCKED | DONE | DEFERRED | CANCELLED

## Goal
## User & User Flow
## Business Rules
## Functional Requirements
## UX States (Loading / Empty / Success / Error / Offline)
## Validation & Permissions
## API / Service Contract
## Dependencies
## Edge Cases
## Security Considerations
## Acceptance Criteria
- [ ] ...
## Tests (Unit / Integration / E2E)
## Notes
```

**Important rule:** a feature document always describes the **currently expected behaviour**. When a requirement changes, the text itself is corrected rather than having a note appended to the end. The reason for the change goes in the decision log and the date goes in the changelog.

A feature scaffolded from a brief is `PLANNED` even when open questions block parts of it; note the blocking question IDs. `BLOCKED` means work has started and cannot continue.

## 2.4 Decision template (ADR)

```markdown
## ADR-012 — Authentication
Date: 2026-09-03
Decision: Email OTP is the default authentication method.
Reason: The client does not currently have an SMS gateway.
Impact: Auth UI and Supabase configuration.
Status: Active
```

Decisions are never deleted. When a decision changes, a new ADR supersedes the old one.

## 2.5 Open question template

```markdown
## Q-014
Feature: Insurance Analysis
Question: What is the canonical coverage reference?
Owner: Product
Status: OPEN
Blocking: YES
```

When a question determines the core behaviour of a feature (`Blocking: YES`), development of that feature stops until it is answered.

---

# 3. Source of truth: which reference wins?

| Subject | Reference |
| --- | --- |
| Expected product behaviour | Feature document |
| Product summary | Product brief |
| Architecture | Architecture document |
| Why a decision was made | Decision log |
| Development status | Feature status |
| What is actually implemented | Code + tests |

When the code differs from the feature document, that is a **gap**: report it and let a human decide which side is corrected. **AI does not get to pick a side on its own.**

---

# 4. Onboarding a new developer

Reading order:

1. `HANDOFF.md`
2. `docs/00-product-brief.md`
3. `docs/07-feature-status.md`
4. `docs/01-architecture.md`
5. `docs/04-decisions.md`
6. the feature document currently `IN_PROGRESS`
7. the related code and tests

After reading, use **Prompt B** to have the AI summarise the product, explain the current state, and identify the next task, without changing code.

---

# 5. Feature development cycle

## Definition of Ready

A feature is ready to build when:

- the goal and the user are clear
- the user flow is clear
- the main requirements are clear
- it has acceptance criteria
- it has no open blocking question
- its main dependencies are known

## The six steps

### Step 1 — Understand

Before anything else, read: product brief, architecture, feature document, decisions, open questions.

### Step 2 — Plan

Before writing code, state:

- which files change
- which dependencies are involved
- what the risks are
- which tests are needed
- which documents must be updated

### Step 3 — Implement

Write code within scope (section 6). Each feature stays inside its own folder and boundary as far as possible.

### Step 4 — Verify

Mandatory: type check, lint, unit tests, integration tests where needed, and E2E for critical flows (login, payment, core flow).

### Step 5 — Sync documentation

Update the feature document, feature status, changelog, and `HANDOFF.md`.

### Step 6 — Git

Before committing: review the diff, run the tests, confirm the documentation is in sync.

## Definition of Done

- [ ] Implementation complete
- [ ] Acceptance criteria met
- [ ] Error, loading, and empty states handled
- [ ] Permissions and related security checked
- [ ] Required tests run and pass
- [ ] Important regressions checked
- [ ] Build succeeds
- [ ] Documentation updated
- [ ] Feature status = DONE
- [ ] `HANDOFF.md` updated

---

# 6. Scope control and working with AI

## 6.1 Every task has a scope

Example task: "Login OTP"

Allowed:

```text
features/auth/*
services/auth/*
tests/auth/*
docs/features/F001-authentication.md
```

The AI may not change payment, dashboard, or database code without a clear reason and human approval. When an out-of-scope change turns out to be necessary: **the AI stops, explains why, and waits for approval.**

## 6.2 Dependency impact check

Before changing shared logic (auth, storage, shared types), identify which features are affected. For anything non-trivial, the AI produces an impact summary before coding.

## 6.3 Choosing an AI model

| Task type | Model |
| --- | --- |
| Architecture, large refactor, security, migration, multi-file change | Stronger model with high reasoning |
| Rename, formatting, repetitive tests, documentation cleanup | Faster model |

Principle: running a weak model several times usually costs more than running a strong model once.

## 6.4 Prompt structure for non-trivial tasks

```text
Context / Goal / Scope / Constraints /
Files to inspect / Expected output /
Verification / Documentation update
```

The general rule for large changes:

**Inspect → Plan → Impact → Implement → Verify → Document**

Not: prompt → generate lots of code → hope.

## 6.5 AI context optimisation

The goal is fewer tokens, higher accuracy, and no need to read the whole repository. The means: precise documentation, feature isolation, repository indexing, and code-intelligence tooling. These **complement** documentation; they do not replace it.

---

# 7. Frontend standard

## 7.1 Web-only projects

If the product only runs in a browser and no native app is on the roadmap:

**React + TypeScript + Next.js**

Reasons: SSR/SSG, SEO, standard routing, mature ecosystem, simple deployment.

## 7.2 Projects that may go mobile

The architecture must be mobile-ready from day one:

- business logic independent of UI
- an independent API layer
- independent schema and validation
- a storage adapter, never direct `localStorage` access
- no browser APIs in domain logic
- localisation ready

The golden rule:

```text
Bad:   feature logic → window.localStorage / document / router
Good:  feature logic → Storage interface
       Web adapter    → localStorage
       Mobile adapter → SecureStore / AsyncStorage
```

## 7.3 Suggested stack

React + TypeScript; Vite or Next.js depending on the product (Next.js for SEO/SSR, Vite for app-like products); TanStack Router and TanStack Query; Zustand; React Hook Form + Zod; Tailwind CSS + Motion; i18next; Vitest + React Testing Library + Playwright; Sentry.

For PWAs add: Dexie + IndexedDB, `vite-plugin-pwa`, Workbox.

This stack is a **default**, not an unchangeable law. Changing it is recorded in `docs/08-tech-stack.md` and the decision log.

## 7.4 State ownership

| State type | Suggested tool |
| --- | --- |
| Server state (API/database) | TanStack Query |
| UI / client state | React state, Zustand when needed |
| Form state | React Hook Form |
| Validation | Zod |

---

# 8. UI design and prototype standard

## 8.1 Where design sits in the process

The path to design is always the same, whether or not the project already had documentation:

1. Standard documentation is created or updated (new project → Prompt A, existing project → Prompt D)
2. The UI is designed from that documentation (Prompt E)
3. Feature development starts (section 5)

Rules:

- **Documentation first, design second.** The prototype is built from the product brief and the feature documents, not from a guess.
- If the project already has a valid design (Figma, Adobe XD, or a working product), the prototype phase is **skipped** and only the archive rules in 8.5 apply.

## 8.2 Claude Design project setup

Start from a **blank project with no preset design system**. A starter design system produces screens that look finished before anyone has decided what the product looks like, and every later screen inherits those accidental defaults.

Create **`masterdoc.html` at the root of the design project**. It holds:

- the product overview: what it is, who uses it, the core flow
- the complete design system: colours and tokens, typography scale, spacing scale, components with their states, layout and grid rules, elevation, radii, motion, light and dark themes, and RTL/LTR rules when the product is localised
- the entry point to the prototype: a button that opens the application preview, or two buttons when desktop and mobile are separate previews

## 8.3 File structure

| Project scope | Structure |
| --- | --- |
| Web or desktop only | `masterdoc.html` + `pages/` |
| Desktop and mobile | `masterdoc.html` + `desktop/` + `mobile/` |
| Mobile only | `masterdoc.html` + `pages/` |

## 8.4 Rules every page follows

State this on every page, in the page itself, so the rule survives being opened alone:

> `masterdoc.html` is the only source of truth for design and implementation. Use the design system defined there.

- No page defines its own colours, type scale, spacing, or components. A page that needs something the design system lacks gets it added to `masterdoc.html` first.
- No page introduces a style inconsistent with `masterdoc.html`.
- Dark mode is included unless the project explicitly says otherwise.
- No real backend, database, or service connection. Everything is mocked.
- Pages use **realistic mock data**, not lorem ipsum and not `Item 1, Item 2`. Names, amounts, dates, and text should look like the real product so layout problems appear in the prototype rather than in production.
- Pages are **interactive** so the whole flow can be tested click by click: navigation, forms with validation, modals, dropdowns, tabs, and the full set of UX states, meaning empty, loading, success, validation error, server error, and permission error. A static screenshot-like page is not acceptable output.

## 8.5 Archiving design output

Everything the design phase produced lives in the repository under `docs/ui/`.

| Design tool | What goes into `docs/ui/` |
| --- | --- |
| Claude Design | The full package: `masterdoc.html` plus `pages/`, or `desktop/` and `mobile/` |
| Figma / Adobe XD | The design link recorded in `docs/ui/README.md` plus screenshots of the key screens |
| Existing product | Screenshots of the key screens plus a note that the product is the reference |

For Figma or Adobe XD a link alone is not enough: the repository must not go blind when access changes.

`docs/ui/README.md` always records the design source and its status, the screen inventory with one status per screen (`pending design`, `designed`, `implemented`), and a pointer to the flows. Screens named in the brief but not yet designed are listed as `pending design` rather than omitted.

## 8.6 Context pack for Claude Design

Send only what changes product understanding and UI decisions. Technical documentation that does not affect what the user sees costs context and pulls the design toward implementation detail.

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

`docs/01-architecture.md` is **not** in the default pack. Send it only when the architecture is visible to the user: navigation structure, permissions and roles, data flow that changes what a screen can show, or a platform constraint that limits the design.

---

# 9. Brand assets standard

## 9.1 One location

`docs/assets/` holds every brand asset the project owns. Four kinds are tracked:

| Kind | Purpose | Final form |
| --- | --- | --- |
| Logo | Product identity | `logo.svg` or `logo.png` |
| Banner | Marketing and repository surfaces | `banner.png` or `banner.jpg` |
| Favicon / app icon | Browser tab, installed app, launcher | a `favicon/` folder holding the generated set |
| OG / social image | Link previews on social platforms and chat | `og.png`, **exactly 1200x630** |

## 9.2 Assets are found by pattern, not by one exact path

A project that already has a logo almost never has it at the path this playbook would have chosen. Reporting an asset as missing while the owner is looking at the file destroys trust in the whole report, so detection matches the **file name or the folder name**:

| Kind | File name contains | Folder name |
| --- | --- | --- |
| Logo | `logo`, `logotype`, `logomark`, `wordmark`, `brandmark`, `brand` | `logo/`, `logos/`, `brand/`, `branding/` |
| Banner | `banner`, `hero`, `cover`, `header-image`, `masthead` | `banner/`, `banners/` |
| Favicon / app icon | `favicon`, `apple-touch-icon`, `android-chrome`, `mstile`, `safari-pinned-tab`, `site.webmanifest` | `favicon/`, `favicons/`, `icons/`, `app-icon/` |
| OG / social | `og`, `opengraph`, `social`, `share`, `twitter-card`, `preview`, `card` | `og/`, `social/`, `opengraph/` |

Separators count: `company-logo.png`, `logo_dark.svg`, and `Logo.PNG` all match. A whole folder matches too, which is how a seven-file favicon set from a generator is recognised.

## 9.3 Consolidate, but never break the build

| Where the asset is | What happens |
| --- | --- |
| `docs/assets/` | Nothing; already correct |
| Anywhere else under `docs/` | **Moved into `docs/assets/`**, keeping set folders intact, so `docs/favicon/` becomes `docs/assets/favicon/` |
| `public/`, `static/`, `src/`, `app/`, `assets/`, `www/`, `resources/`, `web/` | **Never moved.** The build or the served site depends on the path. Reference it in the inventory at its real path |

After a move, correct any documentation link that pointed at the old path.

## 9.4 Placeholders

When a kind has no asset at all, a clearly labelled placeholder is created so the structure is complete and the gap is visible:

- `logo-default.svg`
- `favicon-default.svg`
- `og-default.png` at exactly 1200x630

The `*-default.*` suffix is what marks a file as a placeholder. There is no placeholder banner: an absent banner is reported as a gap rather than invented. **A placeholder is never described as a final brand asset,** and a release with a placeholder still wired in fails the release gate.

Final assets keep whatever name the project already uses. There is no requirement to rename a working `company-logo.png`.

## 9.5 Inventory

`docs/assets/README.md` carries one row per asset:

```text
File | Kind | Purpose | Status (placeholder | final) | Dimensions | Used in
```

The inventory covers assets that were deliberately left in application folders; those rows carry the real path, so nobody goes looking in `docs/assets/` for them.

## 9.6 Generation tools

| Asset | Default tool |
| --- | --- |
| Favicon set from a source image | https://favicon.io/favicon-converter/ |
| Mobile app icon set | https://www.digia.tech/tools/app-icon-generator/ |

A project that generates icons through its own build pipeline records that choice in `docs/04-decisions.md` instead.

---

# 10. SEO, discovery and AI discoverability

A product that cannot be found, crawled, previewed, or installed is unfinished, whatever its code quality. These items belong to the release gate and to the final checklist.

## 10.1 Files in the served root

These are checked where the site serves them: the repository root, `public/`, `static/`, `app/`, `src/app/`, `www/`, or the build output. A `site.webmanifest` sitting only in `docs/assets/favicon/` is a source asset, not a served manifest, and the difference decides whether the check passes.

| File | Applies to | Note |
| --- | --- | --- |
| `robots.txt` | Any served site, including authenticated ones | An authenticated product still needs one, to disallow |
| `sitemap.xml` | Public, indexable sites | May be generated at build time; the build output or generator config is the evidence |
| `llms.txt` | Products that want to be usable by AI agents | A newer convention: recommended, not blocking unless the brief asks for it |
| Web app manifest | PWA and installable products | `site.webmanifest`, `manifest.webmanifest`, or `manifest.json`; the icon sizes it declares must exist |

## 10.2 Metadata in the code

| Item | Requirement |
| --- | --- |
| Page title | Meaningful and unique per page |
| Meta description | Present on indexable pages |
| Canonical URL | Present wherever duplicate URLs are possible |
| Open Graph | `og:title`, `og:description`, `og:image`, `og:url`, `og:type` |
| Twitter Cards | `twitter:card` and the tags the chosen card type requires |
| `og:image` | Resolves to the final 1200x630 asset over a public URL, not a local path |
| Structured data / Schema.org | Only where it truthfully matches the page content |
| Heading hierarchy | One primary `h1` per page, logical `h2`/`h3` beneath it |
| Image `alt` text | Meaningful for content images; decorative images handled accessibly |

## 10.3 By project type

| Project type | What applies |
| --- | --- |
| Public web app | Everything in 10.1 and 10.2 |
| Authenticated web app | `robots.txt`, headings, `alt` text, and the manifest. Indexing and social items are `N/A` with the reason |
| Mobile app | App icon set and store metadata replace favicon and sitemap items |
| Backend or API only | The whole section is `N/A`; API documentation takes its place |
| CLI or library | Identity lives in the README and package metadata |

---

# 11. Backend standard

## 11.1 First choice: Supabase

For MVPs, prototypes, and light to medium production workloads: **Supabase**. Reasons: PostgreSQL, auth, storage, realtime, RLS, edge functions, fast development, and lower early cost.

Principle: **we do not build a custom backend until there is a real technical need.**

## 11.2 When Supabase is not enough

- CPU-intensive processing or heavy file work
- Long-running workers, complex queues, long-running jobs
- Blockchain, custody, or signing infrastructure
- Particular security or network requirements
- Legacy integrations

Allowed alternatives: Node.js, NestJS, Laravel, Django/FastAPI, Go, each with a clear technical reason.

**Rule:** before building a custom backend, `docs/04-decisions.md` must answer:

> Which requirement, specifically, can Supabase not cover at acceptable quality, security, or cost?

A hybrid model (Supabase for auth, database, and storage plus a dedicated service for one part) is usually better than a full custom backend.

## 11.3 Layering rule

```text
Forbidden:  UI component → supabase.from(...)

Correct:    UI component
              → feature service
              → repository
              → Supabase / API
```

- Sensitive business writes go through RPC, Postgres functions, or edge functions, so the contract stays stable.
- Simple reads go through a repository, respecting RLS.
- Direct database calls from a UI component are **forbidden**.

---

# 12. General engineering rules

## 12.1 Feature isolation

Each feature owns its folder (components, services, schemas, types, tests) so the blast radius of a change stays small:

```text
src/features/
  auth/
  dashboard/
  payment/
```

## 12.2 UX states: no feature is only the happy path

Minimum states for user-facing features: loading, success, empty, validation error, server error, network error, permission error. PWA and mobile add offline and retry.

## 12.3 Testing proportional to risk

| Level | For |
| --- | --- |
| Unit | Validation, domain logic, utilities, calculations |
| Integration | API, database, auth, service integration |
| E2E | Critical flows: login, checkout, payment, core flow |

Principle: **a change without verification is not finished.** Before writing new tests, the AI reviews the existing ones.

## 12.4 Localisation

Where multiple languages are possible: no hard-coded text in business logic, translation keys instead, locale-aware dates, numbers, and currency, and RTL/LTR considered in the design system from the start.

## 12.5 Dependency policy

Before installing a new package:

1. Does the project already do this?
2. Is a native API enough?
3. Is the package actively maintained?
4. What is the bundle and security impact?
5. Is it mobile-compatible, if that matters?

Key dependencies are recorded in `docs/08-tech-stack.md`.

## 12.6 Secrets

No secret is ever committed to git, written into documentation, pasted into a shared prompt, or shipped in a client bundle (except a public key designed for the client). Use environment variables and a secret manager.

---

# 13. Mobile migration

The goal: turning web into mobile must not be a full rewrite.

| Shareable | Rewritten |
| --- | --- |
| TypeScript, domain logic, business rules | UI |
| API client, query logic | Routing |
| Schema, validation, shared types | Platform storage |
| Auth logic, i18n, utilities | Native APIs |

Current suggestion for native: **React Native / Expo**. Larger projects can use a monorepo with a shared core.

---

# 14. Git and review

## 14.1 Commits

Feature-oriented and small:

```text
feat(auth): add email OTP flow
fix(onboarding): preserve progress after refresh
docs(auth): update Google login requirement
refactor(storage): introduce storage adapter
```

## 14.2 Pull request checklist

- Is the requirement implemented correctly?
- Was unintended scope added?
- Was the new dependency really necessary?
- Do error states exist?
- Do tests and build pass?
- Are documentation and feature status in sync?
- Was the impact on shared dependencies checked?

## 14.3 Review triggers: what never changes unilaterally

**Needs CTO or technical lead approval:** changing the backend stack or database, building a custom backend, payment or auth architecture, blockchain custody, large refactors, breaking API changes, significant infrastructure cost.

**Needs product owner approval:** changing a user flow, adding or removing a step, changing a business rule, permissions, pricing, data retention, or any user-visible behaviour.

**Needs design coordination:** navigation, onboarding, checkout, dashboard hierarchy, empty and error states, the design system.

A developer or an AI does not change the product experience simply because another implementation is easier.

---

# 15. Legacy projects

The most important rule:

**No big-bang rewrite.** The first goal is visibility and documentation, not rewriting.

Steps:

1. **Branch or back up** before any change
2. **AI inventory:** the AI only analyses the repository (stack, features, auth, tests, risks) without changing code
3. **Generate `docs/`:** build the standard documentation structure from the existing code
4. **Human review:** a developer checks at least the product brief, architecture, and feature status
5. **Gap detection:** report the differences between code, documentation, and expected behaviour
6. **No forced refactor:** refactor only when changing a feature, removing a risk, improving testability or security, or preparing for mobile, always with a recorded reason

---

# 16. Release readiness and the final checklist

## 16.1 The release gate

`docs/09-release-readiness.md` holds six areas: identity and brand; payment and monetisation; SEO and discovery; W3C and accessibility; final humanisation and AI-artifact check; the engineering gate.

Every row carries a status and an evidence field. Rows are created `PENDING` with empty evidence and only move to `PASS`, `FAIL`, or `N/A` when someone has actual evidence. **A row is never marked `PASS` because the work is planned.**

The humanisation check looks for what reveals unreviewed generated output in production: gratuitous em dashes used as a tic, generic filler phrasing, model or prompt text exposed to users, TODO and placeholder copy, lorem ipsum, sample data, and generic layout patterns unrelated to the approved design system.

## 16.2 The final checklist

Every project report, whether it is a check, an initialisation, or a release audit, ends with a compact checklist and nothing after it. The detail stays in the sections above; the checklist exists so a reader who scrolls to the bottom sees the state of the project in one screen.

Markers:

| Marker | Meaning |
| --- | --- |
| `[x]` | Present and correct |
| `[~]` | Present but incomplete, placeholder, or not wired in |
| `[ ]` | Absent |
| `[-]` | Not applicable, with the reason on the same line |

Groups, in order: documentation; brand assets; UI and design; discovery and crawling; metadata and social; platform and PWA; engineering; then the overall result as the final line.

Example:

```text
## Final Checklist

Documentation
[x] GEP structure — 18/18 required paths
[~] docs/ui/README.md — screens listed, no design export
[ ] docs/06-changelog.md — no entries since the first release

Brand assets
[x] Logo — docs/assets/logo.png
[~] Favicon — set in docs/assets/favicon/, not referenced by the app
[ ] Banner — no file matching a banner pattern
[~] OG image — og-default.png 1200x630, placeholder

Discovery and crawling
[ ] robots.txt
[ ] sitemap.xml
[ ] llms.txt
[-] Structured data — no public content pages

**Result:** NOT READY
```

**`[~]` is never rounded up to `[x]`.** The gap between them is exactly what stops a release.

---

# 17. Ready-made prompts

## Prompt A — starting a new project

```text
We are starting this project under the Gaply Engineering Standard.

Before writing application code:
1. Read the client requirements.
2. Identify missing or ambiguous requirements → docs/05-open-questions.md.
3. Create a concise docs/00-product-brief.md.
4. Propose the architecture in docs/01-architecture.md.
5. Break the project into feature documents under docs/features/.
6. Create docs/07-feature-status.md and docs/02-ai-context.md.
7. Create docs/09-release-readiness.md with every row PENDING.
8. Create HANDOFF.md.

Do not invent missing business requirements.

Default technical preferences:
- React + TypeScript. Next.js for SEO/SSR products, Vite for app-like products.
- Mobile-ready architecture if native apps are likely.
- Supabase as the default backend unless there is a documented reason not to.
- No direct Supabase access from UI components.
- Keep business logic independent from UI. Use service/repository boundaries.
- Consider localisation from the start where applicable.
- Add tests appropriate to the risk level.

Before implementation, provide: product summary, open questions,
proposed architecture, feature list, major risks. Then wait for approval.
```

## Prompt B — taking over an existing project

```text
I am taking over this project (Gaply Engineering Standard).

Read in this order:
1. HANDOFF.md
2. docs/00-product-brief.md
3. docs/07-feature-status.md
4. docs/01-architecture.md
5. docs/04-decisions.md
6. the feature document currently marked IN_PROGRESS
7. related code and tests

Then tell me: what the product does, what is complete, what is in
progress, what is blocked, and the next logical task with the files involved.

Do not change code yet. After I approve the plan: implement, run tests,
update documentation, feature status and HANDOFF.md.
```

## Prompt C — developing a feature

```text
Task: <feature/task name>

Scope (allowed paths):
<list allowed folders/files>

Read first:
- docs/00-product-brief.md
- docs/01-architecture.md
- docs/features/<feature-doc>.md
- docs/04-decisions.md

Before coding, provide: implementation plan, files to change,
dependencies and impacted features, risks, tests needed.

Do not change anything outside the scope. If an out-of-scope change
seems required, stop and explain why.

After approval and implementation:
1. Run type check, lint and tests.
2. Update the feature document.
3. Update changelog and feature status.
4. Update HANDOFF.md.
```

## Prompt D — standardising a legacy project

```text
We are adopting the Gaply Engineering Standard for this existing project.
Do not change application code yet.

First inspect the repository and understand: product purpose, architecture,
frontend/backend stack, database, authentication, external services,
existing features, tests, deployment, major technical risks.

Then create or update:

docs/
  00-product-brief.md
  01-architecture.md
  02-ai-context.md
  03-project-memory.md
  04-decisions.md
  05-open-questions.md
  06-changelog.md
  07-feature-status.md
  08-tech-stack.md
  09-release-readiness.md
  features/
  ui/README.md
  assets/README.md
HANDOFF.md

Rules:
- Do not invent product requirements.
- Mark uncertain items clearly and put them in open-questions.
- Build feature documents from the actual code.
- Identify discrepancies between code and documentation.
- Detect existing brand assets by name pattern, not by one exact path,
  and consolidate them into docs/assets/ unless the application serves them.
- Do not refactor during this step.

At the end provide: repository summary, documentation created, unknowns,
risks, recommended next actions, and a final checklist. Wait for human
approval before any refactoring.
```

## Prompt E — designing the UI with Claude Design

```text
We are designing the UI for this project with Claude Design, under the
Gaply Engineering Standard.

Context pack:
- docs/assets/logo.png (or the project's actual logo)
- docs/00-product-brief.md
- docs/02-ai-context.md
- docs/07-feature-status.md
- docs/features/
- brief.md, if it carries brand direction, audience or positioning
Send docs/01-architecture.md only if the architecture is visible to the
user: navigation, permissions, data flow that changes what a screen shows.

Rules:
- Start from a blank project with no preset design system.
- Create masterdoc.html at the root of the design project. It holds the
  product overview and the complete design system: colours and tokens,
  typography, spacing, components and their states, layout rules,
  light and dark themes.
- masterdoc.html contains a button that opens the application preview.
  If desktop and mobile are separate previews, it contains two buttons.
- File structure: web or desktop only → masterdoc.html + pages/;
  desktop and mobile → masterdoc.html + desktop/ + mobile/;
  mobile only → masterdoc.html + pages/.
- Every page states that masterdoc.html is the only source of truth for
  design and implementation, and uses only the design system defined there.
- No page defines its own colours, spacing, type scale or components, and
  no page introduces a style inconsistent with masterdoc.html.
- Include dark mode for all screens unless explicitly told otherwise.
- Fill every page with realistic mock data, not lorem ipsum.
- Every page is interactive: navigation, forms with validation, modals,
  dropdowns, tabs, and the full UX state set (empty, loading, success,
  validation error, server error, permission error).
- No real backend, database or extra infrastructure.
- Do not invent product requirements. Record anything unclear as an open
  question instead of guessing.

The final package is stored at docs/ui/ in the repository.
```

---

# 18. Maintaining this playbook

The standard exists in four files, and they are one document split by language and by audience:

```text
Gaply-Engineering-Playbook.md      the standard, English
Gaply-Engineering-Playbook.fa.md   the standard, Persian
README.md                          using the skill, English
README.fa.md                       using the skill, Persian
```

**No change to the skill, its rules, its workflow, or its standards is complete until all four files have been reviewed and, where relevant, updated.** A rule that lives in only one of them is a rule half the team will never see, and the two languages drifting apart is how a standard quietly becomes two standards.

The Persian files are parallel guides, not machine translations: they carry the same rules in language a Persian-speaking reader would actually use.

---

# The final Gaply principle

The goal is not the most code in the least time.

The goal is:

**the most reliable speed, with the least dependence on any individual, tool, or technology.**

A good Gaply project:

- develops quickly
- is understandable to the next person and to an AI
- has living documentation
- is testable and changeable
- can migrate to mobile when needed
- is not over-engineered without reason
- depends on no individual
