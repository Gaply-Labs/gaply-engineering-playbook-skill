# GEP Documentation Scaffold Reference

Use this reference for `init`.

## Required tree

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
├── ui/
└── assets/
```

## Minimum content by file

### `HANDOFF.md`

Must contain:

- Current Phase
- Active Feature or current project state
- Current Task
- Last Completed
- Next Step
- Read First
- Blockers

### `docs/README.md`

Explain that `docs/` is the project's living source of truth and provide the reading order for a new developer/agent.

### `docs/docs-manifest.md`

Track every required documentation artifact with at least:

- path;
- purpose;
- status;
- last meaningful update when known.

### `docs/00-product-brief.md`

Derive only from supported requirements. Include:

- Project Name
- Product summary
- Problem / purpose
- Target users
- Core flow
- In scope
- Out of scope
- Known constraints
- Open questions reference

Do not add unsupported business requirements.

### `docs/01-architecture.md`

Describe the actual/proposed architecture supported by repository evidence and approved project direction:

- frontend/backend stack;
- database;
- authentication;
- storage;
- service/repository boundaries;
- security boundaries;
- deployment;
- folder structure;
- mobile-readiness where applicable.

Unknowns must be explicit.

### `docs/02-ai-context.md`

Include rules for coding agents:

- no invented requirements;
- scope discipline;
- inspect before editing;
- impact check for shared dependencies;
- verification requirements;
- documentation synchronization;
- secrets policy;
- dependency policy.

### `docs/03-project-memory.md`

Capture durable project context not obvious from code, such as approved constraints, client/product choices, and rationale. Do not store secrets.

### `docs/04-decisions.md`

Append-only ADR log. Minimum ADR fields:

- ID
- Date
- Decision
- Reason
- Impact
- Status

Do not erase superseded decisions; supersede them with a new ADR.

### `docs/05-open-questions.md`

For each unresolved item include:

- ID
- Feature/area
- Question
- Owner when known
- Status
- Blocking: YES/NO

### `docs/06-changelog.md`

Track meaningful product, architecture, and behavior changes. This is not a replacement for Git history.

### `docs/07-feature-status.md`

Maintain a feature table with at least:

- Feature ID
- Name
- Status
- Documentation path
- Notes/blocker when applicable

Recommended statuses:

`PLANNED | READY | IN_PROGRESS | BLOCKED | DONE | DEFERRED | CANCELLED`

### `docs/08-tech-stack.md`

For each key technology include:

- technology/tool;
- version when known;
- purpose;
- reason for selection when known;
- alternatives/notes when relevant.

### `docs/09-release-readiness.md`

Create the release gate with these areas:

1. Identity & Brand
2. Payment / Monetization
3. SEO
4. W3C & Accessibility
5. Final Humanization / AI Artifact Check
6. Engineering Release Gate

Every row should support:

`Status: PASS | FAIL | N/A`

and an `Evidence` field.

Do not pre-mark unverified items as PASS. Before implementation, most final-release checks should remain pending/not evaluated.

### `docs/features/Fxxx-name.md`

Create one per supported feature. Minimum sections:

- Status
- Goal
- User & User Flow
- Business Rules
- Functional Requirements
- UX States
- Validation & Permissions
- API / Service Contract
- Dependencies
- Edge Cases
- Security Considerations
- Acceptance Criteria
- Tests
- Notes

Feature documents represent the current expected behavior. Requirement history belongs in decisions/changelog.

## UI archive

Target location: `docs/ui/`.

If the source is a code prototype, preserve its package structure when practical. If the source is external design, store a reference file plus available key screenshots. If no UI applies, document why.

## Asset archive

Target location: `docs/assets/`.

Bootstrap minimum:

- `logo-default.*` or an equivalent clearly labeled placeholder;
- `og-default.png` exactly 1200×630 px;
- `favicon-default.*` or equivalent clearly labeled placeholder.

Final release must replace placeholders with final brand assets.
