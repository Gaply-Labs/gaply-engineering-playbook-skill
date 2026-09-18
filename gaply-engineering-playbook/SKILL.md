---
name: gaply-engineering-playbook
description: Gaply Engineering Playbook project bootstrap and release-audit skill. Use this skill whenever the user asks to check, initialize, standardize, or perform a final readiness review of a software project under GEP, Gaply Engineering Playbook, or uses commands such as gep chk, gep init, gep pchk, precheck, init, or postcheck. It inspects the repository, validates required project inputs and brand/UI assets, creates the standard documentation scaffold without inventing business requirements, and performs evidence-based final release checks.
---

# GEP - Gaply Engineering Playbook Skill

Use this skill to apply the Gaply Engineering Playbook workflow to a software repository.

The skill has three primary actions:

- `chk` — read-only initial/preflight check.
- `init` — create or synchronize the initial GEP documentation structure, then verify it.
- `pchk` — read-only post-implementation/release-readiness check against the actual repository.

## 1. Command parsing

Recognize these action aliases:

| Canonical action | Accepted aliases |
| --- | --- |
| `chk` | `check`, `precheck`, `pre-check` |
| `init` | `initialize`, `bootstrap` |
| `pchk` | `postcheck`, `post-check`, `release-check`, `final-check` |

Accept commands written in any of these textual forms after the skill has been invoked:

- `gep chk`
- `gep init`
- `gep pchk`
- `gep:chk`
- `gep:init`
- `gep:pchk`

Platform-native invocation can differ. The action token is what matters.

If no action is supplied, do not modify files. Show the three available actions with one-line explanations.

## 2. Language rules

Determine the output language in this order:

1. Explicit language parameter wins: `lang=fa`, `lang=en`, `language=Persian`, etc.
2. Otherwise, if the command includes a natural-language instruction, use that instruction's dominant language.
3. Otherwise, default to English.

For `init`, use the selected language for newly generated prose documentation unless existing project documentation clearly establishes another documentation language. Preserve code identifiers, file names, product names, API names, and technical terms where translation would reduce precision.

The skill instructions themselves are authoritative regardless of output language.

## 3. Non-negotiable behavior

- Never invent missing business requirements.
- Never silently infer that a release requirement is satisfied without evidence.
- Never overwrite substantial existing documentation without first comparing it and preserving valid project-specific information.
- Never change application code during `chk` or `pchk`.
- During `init`, create or update documentation and bootstrap assets only. Do not implement product features unless the user explicitly asks separately.
- If a requirement is not applicable, mark it `N/A` and state why.
- If a fact cannot be verified, report it as `UNVERIFIED`; do not present it as `PASS`.
- Prefer actual repository evidence over claims written in documentation.
- Keep changes scoped to the GEP documentation/bootstrap task.

## 4. Repository discovery

Work from the current repository/project root. Before any action:

1. Inspect the top-level tree.
2. Locate likely brief/product-requirement sources.
3. Locate existing documentation folders (`docs/`, `doc/`, or project-specific equivalents).
4. Locate UI/design sources (`docs/ui/`, `ui/`, `design/`, Figma/XD references, screenshots, or prototype packages).
5. Locate brand assets and public/static asset folders.
6. Detect the technology stack from manifests and configuration files.
7. Do not assume a missing item is absent until reasonable filename/path variants have been checked.

When Python is available, you may run `scripts/gep_scan.py` for deterministic structure and image-dimension checks. Treat its output as evidence, not as a substitute for repository inspection. During `init`, if bootstrap visual assets are missing and a confirmed Project Name exists, prefer `scripts/create_bootstrap_assets.py --project-name "<name>"` to create deterministic placeholders without third-party dependencies.

## 5. Action: `chk` — Initial Check

`chk` is read-only.

Read `references/precheck.md` and evaluate every applicable item.

At minimum verify:

- a confirmed Project Name can be identified;
- a project brief/product requirements source exists;
- the documentation folder status is known;
- the UI/design source status is known, or the project is explicitly non-UI/backend-only;
- a logo exists, or a bootstrap logo is required;
- an OG/social image exists and is exactly 1200×630 px, or a bootstrap image is required;
- a favicon exists, or a bootstrap favicon is required.

Output a checklist table with:

`Item | Status | Evidence | Required action`

Allowed displayed statuses:

- `PASS`
- `MISSING`
- `N/A`
- `UNVERIFIED`

Then output one overall result:

- `READY FOR GEP INIT`
- `NOT READY FOR GEP INIT`

Blocking inputs for `init` are:

- no confirmed Project Name;
- no usable brief/product-requirement source.

Missing `docs/`, `docs/ui/`, or bootstrap visual assets are not blockers if they can be safely scaffolded by `init`. Report that they will be created as bootstrap targets. If the project requires real UI source material for accurate documentation and none exists, mark the affected UI-specific content `UNVERIFIED` and do not invent it.

Do not create or edit files in `chk`.

## 6. Action: `init` — Initialize GEP Documentation

`init` may create and update GEP documentation/bootstrap files.

### 6.1 Preflight

First run the same checks as `chk`.

If Project Name or the brief/product-requirement source is missing, stop before creating substantive documentation and return the missing blockers.

### 6.2 Preserve existing material

If `docs/` or any target file already exists:

1. Read it first.
2. Preserve valid project-specific content.
3. Fill structural gaps.
4. Do not replace project facts with generic boilerplate.
5. Put unresolved facts in `docs/05-open-questions.md`.

### 6.3 Create/synchronize the standard structure

Read `references/docs-scaffold.md` and ensure this structure exists:

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

Create feature documents only for features supported by the brief, existing code, or explicit requirements. Do not invent a feature list.

### 6.4 Bootstrap identity/assets

Use the confirmed Project Name.

If final brand assets are unavailable, ensure bootstrap assets exist under `docs/assets/`:

- a clearly labeled default/placeholder logo;
- `og-default.png` at exactly 1200×630 px;
- a clearly labeled default/placeholder favicon.

If Python execution is available, use `scripts/create_bootstrap_assets.py` to create simple non-branded placeholders. Otherwise create equivalent placeholders only if the environment safely supports it; if not, create the target paths/manifest entries and report asset generation as pending. Never claim a placeholder is a final brand asset.

If final assets already exist, preserve and reference them rather than creating unnecessary placeholders.

### 6.5 UI archive

If a valid UI/design source exists, archive or reference it under `docs/ui/` according to the project source:

- code/prototype package: retain the package structure;
- Figma/XD/external design: record the design reference and keep screenshots of key screens when available;
- backend/API-only project: document UI as `N/A` with reason.

Do not fabricate screenshots or design states.

### 6.6 Post-init verification

After writing files, immediately re-inspect the repository.

Return a verification table:

`Item | Status | Evidence`

Then state exactly one result:

- `GEP INIT COMPLETE`
- `GEP INIT INCOMPLETE`

`COMPLETE` requires the required GEP files/folders to exist and the generated documentation to be internally consistent. Open product questions may remain, but they must be explicitly recorded and must not be silently resolved.

Summarize every file created and every existing file updated.

## 7. Action: `pchk` — Final/Post-Implementation Check

`pchk` is read-only unless the user separately asks for fixes.

Read `references/postcheck.md` and inspect the actual implementation, configuration, build output where available, and documentation.

Do not rely only on `docs/09-release-readiness.md`; verify claims against repository evidence.

At minimum evaluate:

- final Project Name consistency;
- final logo;
- final favicon;
- final OG/social image exactly 1200×630 px;
- public social/OG metadata;
- payment/monetization integration when applicable, including the user-selected provider such as RevenueCat, Stripe, MoonPay, or another provider;
- SEO metadata;
- semantic heading hierarchy (`h1`, `h2`, `h3`, ...);
- meaningful image `alt` text;
- canonical/sitemap/robots where applicable;
- W3C/HTML validity evidence where applicable;
- WCAG 2.2 AA essentials;
- keyboard navigation and focus behavior for critical flows;
- form labels and accessible error associations;
- screen-reader smoke-test evidence for critical flows;
- absence of bootstrap/placeholder/debug/TODO/prompt/model text in production UI;
- removal of unnecessary generated-copy artifacts such as gratuitous em dashes;
- tests, build, security/permission/secret checks;
- synchronization of feature status, changelog, HANDOFF, and release-readiness documentation.

For payment, SEO, accessibility, W3C, and runtime behavior, distinguish static-code evidence from executed test evidence.

Output a checklist table:

`Area | Check | Status | Evidence | Issue / Required fix`

Use:

- `PASS`
- `FAIL`
- `N/A`
- `UNVERIFIED`

Then provide:

- `Blocking failures`
- `Non-blocking findings`
- `Unverified items`
- `Overall release status`

Overall release status must be exactly one of:

- `READY`
- `NOT READY`
- `NOT VERIFIED`

Rules:

- Any blocking `FAIL` => `NOT READY`.
- No blocking failures but critical checks remain `UNVERIFIED` => `NOT VERIFIED`.
- `READY` requires evidence for all applicable blocking checks.

Do not fix issues during `pchk` unless the user explicitly asks for remediation after seeing the report.

## 8. Evidence quality

Prefer evidence in this order:

1. Executed test/build/audit output.
2. Actual implementation/configuration.
3. Generated artifact inspection.
4. Documentation claims.
5. Inference.

Label inference as inference.

For each failed or unverified item, include the exact file/path when available.

## 9. Supporting references

Use these files as needed:

- `references/precheck.md` — initial inspection checklist and discovery rules.
- `references/docs-scaffold.md` — required documentation structure and minimum contents.
- `references/postcheck.md` — final release-readiness checklist.

Do not load every reference when it is not relevant to the requested action.
