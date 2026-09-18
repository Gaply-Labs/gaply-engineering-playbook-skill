# GEP Documentation Scaffold Reference

Use this reference for `init`.

## 1. Required tree

```text
HANDOFF.md

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
│   └── Fxxx-name.md      (one per supported feature)
├── ui/
│   └── README.md
└── assets/
    └── README.md
```

`docs/ui/README.md` and `docs/assets/README.md` are required so that the folders survive version control even before any design export or final asset exists, and so that their status is written down rather than implied by an empty directory.

## 2. Source coverage: what a brief alone can fill

When the project contains only a brief, `init` still creates the whole tree. This table says how much of each document the brief can fill and what stays open. Never fill a cell the sources do not support; write `Open (see Q-xxx)` and record the question.

| Document | From the brief alone | Needs code, design, or a decision | Opens when |
| --- | --- | --- | --- |
| `HANDOFF.md` | Yes: phase "documentation initialized", next step, read-first list | | |
| `docs/README.md` | Yes | | |
| `docs/docs-manifest.md` | Yes: every artifact with status | | |
| `docs/00-product-brief.md` | Yes: name, summary, problem, users, core flow, scope, constraints | | Ambiguities become questions |
| `docs/01-architecture.md` | Partly: stack, platform, and deployment constraints named in the brief; proposed boundaries | Folder structure, data model, auth details, security boundaries | Code exists |
| `docs/02-ai-context.md` | Yes: standard agent rules plus project constraints stated in the brief | | |
| `docs/03-project-memory.md` | Partly: constraints and product choices stated in the brief | Rationale the brief does not give | The user confirms |
| `docs/04-decisions.md` | Partly: explicit choices in the brief become the first ADRs with reason "specified in brief" | Everything else | Decisions are made |
| `docs/05-open-questions.md` | Yes: every ambiguity found during analysis | | |
| `docs/06-changelog.md` | Yes: first entry "GEP documentation initialized from <source>" | | |
| `docs/07-feature-status.md` | Yes: one `PLANNED` row per in-scope item | | |
| `docs/08-tech-stack.md` | Partly: technologies named in the brief | Versions from manifests | Manifests exist |
| `docs/09-release-readiness.md` | Yes: every row created with status `PENDING` and empty evidence | Evidence | `pchk` |
| `docs/features/Fxxx-name.md` | Partly: Status, Goal, User and User Flow, Business Rules, scope-derived Acceptance Criteria | API contract, UX states, validation, tests, edge cases | Implementation and design |
| `docs/ui/README.md` | Partly: design source (tool, link or "pending"), screen names from the brief with status `pending design` | Screenshots, states | Design export |
| `docs/assets/README.md` | Yes: inventory of the placeholders created | Final assets | Brand delivery |

## 3. Minimum content by file

### `HANDOFF.md`

Must contain: Current Phase, Active Feature or current project state, Current Task, Last Completed, Next Step, Read First, Blockers.

### `docs/README.md`

Explain that `docs/` is the project's living source of truth and give the reading order for a new developer or agent.

### `docs/docs-manifest.md`

Track every required documentation artifact with at least: path, purpose, status, last meaningful update when known.

### `docs/00-product-brief.md`

Derive only from supported requirements. Include: Project Name, product summary, problem or purpose, target users, core flow, in scope, out of scope, known constraints, open questions reference. Do not add unsupported business requirements.

### `docs/01-architecture.md`

Describe the actual or proposed architecture supported by repository evidence and approved project direction: frontend and backend stack, database, authentication, storage, service and repository boundaries, security boundaries, deployment, folder structure, mobile-readiness where applicable. Unknowns must be explicit.

### `docs/02-ai-context.md`

Rules for coding agents: no invented requirements, scope discipline, inspect before editing, impact check for shared dependencies, verification requirements, documentation synchronization, secrets policy, dependency policy. Add project-specific constraints from the brief.

### `docs/03-project-memory.md`

Durable project context not obvious from code: approved constraints, client or product choices, rationale. Do not store secrets.

### `docs/04-decisions.md`

Append-only ADR log with at least: ID, Date, Decision, Reason, Impact, Status. Do not erase superseded decisions; supersede them with a new ADR.

### `docs/05-open-questions.md`

For each unresolved item: ID (`Q-001`), feature or area, question, owner when known, status, `Blocking: YES/NO`.

### `docs/06-changelog.md`

Meaningful product, architecture, and behavior changes. Not a replacement for Git history.

### `docs/07-feature-status.md`

A feature table with at least: Feature ID, Name, Status, Documentation path, Notes or blocker. Statuses: `PLANNED | READY | IN_PROGRESS | BLOCKED | DONE | DEFERRED | CANCELLED`. A feature scaffolded from the brief is `PLANNED` even when open questions block parts of it; note the blocking question IDs in the Notes column. `BLOCKED` means work has started and cannot continue, which `init` alone never establishes.

### `docs/08-tech-stack.md`

For each key technology: technology or tool, version when known, purpose, reason for selection when known, alternatives or notes when relevant.

### `docs/09-release-readiness.md`

The release gate with these areas: 1 Identity & Brand, 2 Payment / Monetization, 3 SEO, 4 W3C & Accessibility, 5 Final Humanization / AI Artifact Check, 6 Engineering Release Gate. Every row supports `Status: PENDING | PASS | FAIL | N/A` and an `Evidence` field. `init` creates every row as `PENDING` with empty evidence; only `pchk` (or a human reviewer with evidence) moves a row to `PASS`, `FAIL`, or `N/A`.

### `docs/features/Fxxx-name.md`

One per supported feature, named `F001-kebab-name.md` with IDs matching `docs/07-feature-status.md`. Minimum sections: Status, Goal, User & User Flow, Business Rules, Functional Requirements, UX States, Validation & Permissions, API / Service Contract, Dependencies, Edge Cases, Security Considerations, Acceptance Criteria, Tests, Notes. Feature documents describe current expected behavior; requirement history belongs in decisions and changelog.

### `docs/ui/README.md`

Must contain:

- Design source: tool and link, or `pending` with the owner when known.
- Screen inventory: name, purpose, status (`pending design | designed | implemented`), reference (screenshot or design frame).
- Flow references, or a pointer to `flows.md`.
- For a project without a UI: `N/A` with the reason from the brief.

Recommended files next to it. Create one as soon as the sources name its subject, even when only names are known, and mark the unknown parts `pending design`; an empty heading with a status is more useful to the next reader than a missing file. Skip a file entirely when the sources say nothing about its subject:

- `screens.md`: one section per screen with its states (empty, loading, error, success) and responsive notes.
- `flows.md`: user flows step by step, cross-referenced to feature IDs.
- `screenshots/`: one PNG per key screen, named `screen-<slug>.png`.
- `design-tokens.md`: when a design system or token set exists.

### `docs/assets/README.md`

An inventory table: `File | Purpose | Status (placeholder | final) | Dimensions | Used in`.

Naming: `logo-default.svg`, `favicon-default.svg`, and `og-default.png` are placeholders. Final assets are `logo.svg` (or `.png`), a favicon set (`favicon.svg`, `favicon.ico`, PNG sizes as the platform requires), and `og.png` at exactly 1200x630. Release replaces every placeholder row with a final row.

## 4. UI archive

Target location: `docs/ui/`.

If the source is a code prototype, preserve its package structure when practical. If the source is an external design, store a reference file plus available key screenshots. If the brief names screens but no design exists yet, list them in `docs/ui/README.md` as `pending design`. If no UI applies, document why.

## 5. Asset archive

Target location: `docs/assets/`.

Bootstrap minimum: `logo-default.svg` (or an equivalent clearly labeled placeholder), `og-default.png` at exactly 1200x630, `favicon-default.svg` (or equivalent), and an inventory row for each in `docs/assets/README.md`.

Final release must replace placeholders with final brand assets.
