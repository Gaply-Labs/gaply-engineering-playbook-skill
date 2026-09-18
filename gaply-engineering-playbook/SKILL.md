---
name: gaply-engineering-playbook
description: Gaply Engineering Playbook (GEP) project bootstrap, documentation sync, and release-audit skill. Use it whenever the user wants to check, initialize, scaffold, synchronize, or audit a software project's documentation under GEP or the Gaply Engineering Playbook, wants project documentation created from a brief or PRD (for example "initialize this project from brief.md"), asks what documentation is missing, outdated, or inconsistent with the code, or uses commands such as gep chk, gep init, gep pchk, precheck, init, sync, postcheck. It inspects the repository, validates project inputs and brand/UI assets, creates the standard documentation scaffold without inventing business requirements, reports every gap with a concrete recommendation, and performs evidence-based release checks.
---

# GEP - Gaply Engineering Playbook Skill

Apply the Gaply Engineering Playbook workflow to a software repository. GEP keeps a project's documentation (`docs/` plus `HANDOFF.md`) as the living source of truth for humans and coding agents, from the first brief to release.

The skill has three actions:

- `chk`: read-only check. Before initialization it answers "can GEP be initialized here?". After initialization it answers "is the documentation complete and in sync with the codebase?".
- `init`: create or synchronize the GEP documentation structure from the sources that exist, then verify the result and report every gap with a recommendation. Running `init` again on an initialized project is the sync/update operation.
- `pchk`: read-only post-implementation and release-readiness audit against the actual repository.

Typical lifecycle: brief -> `chk` -> `init` -> build -> `chk` or `init` whenever docs drift -> `pchk` before release.

## 1. Command parsing

Recognize these action aliases:

| Canonical action | Accepted aliases |
| --- | --- |
| `chk` | `check`, `precheck`, `pre-check`, `status` |
| `init` | `initialize`, `bootstrap`, `scaffold`, `sync`, `update` |
| `pchk` | `postcheck`, `post-check`, `release-check`, `final-check`, `audit` |

Accept the action in any of these textual forms once the skill is active: `gep chk`, `gep:chk`, `/gaply-engineering-playbook chk`, or a natural-language request. Platform-native invocation differs; the action token and the user's intent are what matter.

Map natural-language requests to actions with this table:

| The user asks for | Action |
| --- | --- |
| "check this project", "what is missing", "status", "do not modify anything" | `chk` |
| "initialize", "set up GEP", "create the documentation from brief.md", "scaffold the docs" | `init` |
| "sync", "update the docs", "fill the gaps", "create the missing documentation files" | `init` (sync run on existing docs) |
| "check the project and create what is missing" | `init`; say in the report that `init` began with the same checks as `chk` |
| "release check", "are we ready to ship", "final audit" | `pchk` |

Optional parameters may appear anywhere after the action as `key=value`:

| Parameter | Effect |
| --- | --- |
| `lang=fa`, `language=Persian` | Output language (see section 2). |
| `project="Name"` (alias `name=`) | Confirmed Project Name. Overrides discovery. |
| `source=path/to/brief.md` | Primary requirements source. Overrides discovery. |

If no action is supplied, do not modify files. List the three actions with one-line explanations and say which one fits the current repository state: not initialized (no `docs/docs-manifest.md`) suggests `chk` then `init`; initialized suggests `chk`.

## 2. Language rules

Determine the output language in this order:

1. Explicit language parameter wins: `lang=fa`, `lang=en`, `language=Persian`, etc.
2. Otherwise, if the command includes a natural-language instruction, use that instruction's dominant language.
3. Otherwise, default to English.

For `init`, use the selected language for newly generated prose documentation unless existing project documentation clearly establishes another documentation language. Preserve code identifiers, file names, product names, API names, and technical terms where translation would reduce precision.

The skill instructions themselves are authoritative regardless of output language.

## 3. Non-negotiable behavior

- Never invent missing business requirements. Unknowns go to `docs/05-open-questions.md`.
- Never present a release requirement as satisfied without evidence.
- Never overwrite substantial existing documentation without first reading it and preserving valid project-specific information.
- Never change application code during `chk` or `pchk`.
- During `init`, create or update documentation and bootstrap assets only. Do not implement product features unless the user explicitly asks separately.
- `init` never stops because folders or assets other than the requirements source are missing. A brief alone is enough input: scaffold what the brief supports, create clearly labeled placeholders where the standard requires an asset, and report the rest as gaps.
- Every missing item in a report comes with a concrete recommendation: the path to create, the default file names, and which documentation or check will consume it. A list of what is absent, on its own, is not a finished report.
- If a requirement is not applicable, mark it `N/A` and state why.
- If a fact cannot be verified, report it as `UNVERIFIED`; do not present it as `PASS`.
- Prefer actual repository evidence over claims written in documentation.
- Keep changes scoped to the GEP documentation and bootstrap task.

## 4. Repository discovery

Work from the current repository/project root. Before any action:

1. Inspect the top-level tree.
2. Locate the requirements source: the `source=` parameter first, then likely brief/PRD files (see `references/precheck.md`).
3. Locate existing documentation folders (`docs/`, `doc/`, or project-specific equivalents). `docs/docs-manifest.md` marks a GEP-initialized project.
4. Locate UI/design sources (`docs/ui/`, `ui/`, `design/`, Figma/XD references, screenshots, prototype packages).
5. Locate brand assets and public/static asset folders.
6. Detect the technology stack from manifests and configuration files.
7. Read the requirements source and classify the project type (public web app, authenticated web app, mobile app, backend/API only, CLI or library, hybrid). The type decides which checks apply: UI archive, SEO, payments, public assets. Record the classification and its evidence; when the brief does not settle it, record an open question instead of guessing.
8. Do not assume a missing item is absent until reasonable filename/path variants have been checked.

When Python is available, run `scripts/gep_scan.py --root . --json` for deterministic structure, asset, image-dimension, and referenced-but-missing checks. Treat its output as evidence, not as a substitute for reading the repository. During `init`, if bootstrap visual assets are missing and a confirmed Project Name exists, prefer `scripts/create_bootstrap_assets.py --project-name "<name>"` to create deterministic placeholders without third-party dependencies.

## 5. Action: `chk` - Check

`chk` is read-only. Do not create or edit files.

Read `references/precheck.md`. Pick the mode from repository state:

- `docs/docs-manifest.md` absent: Mode A, initialization readiness.
- `docs/docs-manifest.md` present: Mode B, documentation health.

Say which mode ran in the first line of the output.

### 5.1 Mode A: initialization readiness

Verify at minimum:

- a confirmed Project Name can be identified;
- a project brief or product requirements source exists and is usable;
- the documentation folder status is known;
- the UI/design source status is known, or the project is explicitly non-UI/backend-only;
- a logo exists, or a bootstrap logo will be required;
- an OG/social image exists and is exactly 1200x630 px, or a bootstrap image will be required;
- a favicon exists, or a bootstrap favicon will be required.

Output a checklist table:

`Item | Status | Evidence | Required action`

Allowed statuses: `PASS`, `MISSING`, `N/A`, `UNVERIFIED`.

Then output exactly one overall result:

- `READY FOR GEP INIT`
- `NOT READY FOR GEP INIT`

Only two conditions block `init`: no confirmed Project Name, or no usable brief/requirements source. Missing `docs/`, `docs/ui/`, or bootstrap visual assets are not blockers; report them as targets `init` will create. If the project needs real UI source material for accurate documentation and none exists, mark UI-specific content `UNVERIFIED` and do not invent it.

End with a `Next step:` line, normally `gep init` (or `gep init project="<name>"` when the name is the only blocker).

### 5.2 Mode B: documentation health

Evaluate, with evidence:

- required GEP structure: every path in the standard tree exists;
- referenced-but-missing items: anything the brief or product docs mention (UI screens, wireframes, brand assets, favicon, OG image, API, payments) that has no corresponding folder, file, or documented decision; use the signal table in `references/precheck.md`;
- placeholders still in place: bootstrap `*-default.*` assets, template text, empty required sections;
- sync with the codebase: features present in code but absent from `docs/07-feature-status.md` and vice versa; `docs/08-tech-stack.md` versus manifests; `docs/01-architecture.md` folder structure versus the actual tree; `HANDOFF.md` and `docs/06-changelog.md` versus recent history where available;
- open questions marked `Blocking: YES` that the code has since answered.

Output a checklist table:

`Item | Status | Evidence | Required action`

Allowed statuses: `PASS`, `MISSING`, `OUTDATED`, `N/A`, `UNVERIFIED`.

Then output exactly one overall result:

- `GEP DOCS IN SYNC`: no `MISSING` or `OUTDATED` item, and no `UNVERIFIED` item on the required structure.
- `GEP DOCS OUT OF SYNC`: otherwise.

List `Unverified items` separately, then end with a `Next step:` line: `gep init` to fill gaps while preserving existing content, or `gep pchk` when the project is heading to release. Mode B never replaces `pchk`.

## 6. Action: `init` - Initialize or synchronize GEP documentation

`init` may create and update GEP documentation and bootstrap files. It runs the same way on an empty project, a brief-only project, and an already initialized project; only the amount of new content differs.

### 6.1 Preflight

Run the Mode A checks from section 5.1 first.

Stop only when the Project Name is missing (after applying the resolution order in `references/precheck.md`) or when no usable requirements source exists. In that case return the blockers and the exact parameter that resolves each one, for example `gep init project="Name"` or `gep init source=docs/prd.md`.

Everything else, including a project that contains nothing but `brief.md`, proceeds. Record the preflight outcome as one line in the report's `Detected` section (for example `preflight: READY FOR GEP INIT, name from brief title`); the full `chk` table appears only when a blocker stops the run.

### 6.2 Analyze the requirements source

Read the brief (or PRD) in full before writing. Extract, with the brief section as evidence:

- Project Name, one-paragraph summary, problem or purpose;
- target users;
- core flow;
- in-scope items and steps of the core flow that the in-scope list does not already cover (sign-in is the usual example); each becomes a feature candidate that cites its brief section. Out-of-scope items are recorded as such;
- constraints: stack, platforms, deployment, compliance, performance;
- project type (section 4, step 7);
- UI presence and design source;
- monetization and payment provider, if any;
- public/indexable surface versus authenticated-only;
- API exposure;
- explicit decisions already made (these become the first ADRs, with "specified in brief" as the reason).

Anything the brief leaves ambiguous becomes an entry in `docs/05-open-questions.md`, not an assumption in another file. Use the source-coverage table in `references/docs-scaffold.md` to decide which documents the brief can fill and which parts stay open.

### 6.3 Preserve existing material

If `docs/` or any target file already exists:

1. Read it first.
2. Preserve valid project-specific content.
3. Fill structural gaps.
4. Do not replace project facts with generic boilerplate.
5. Put unresolved facts in `docs/05-open-questions.md`.

### 6.4 Create or synchronize the standard structure

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
│   └── Fxxx-name.md      (one per supported feature)
├── ui/
│   └── README.md
└── assets/
    └── README.md
```

Create feature documents only for features supported by the brief, existing code, or explicit requirements. Do not invent a feature list. Fill each file with what the sources support and mark the remaining sections `Open` with a pointer to the relevant open question, so a reader can tell "not yet known" from "not applicable".

### 6.5 Identity and bootstrap assets

Use the confirmed Project Name.

If final brand assets are unavailable, ensure bootstrap assets exist under `docs/assets/`:

- `logo-default.svg`, a clearly labeled placeholder logo;
- `og-default.png` at exactly 1200x630 px;
- `favicon-default.svg`, a clearly labeled placeholder favicon.

If Python execution is available, use `scripts/create_bootstrap_assets.py` to create simple non-branded placeholders. Otherwise create equivalent placeholders only if the environment safely supports it; if not, create the target paths and manifest entries and report asset generation as pending. Record every asset in `docs/assets/README.md` with its status (`placeholder` or `final`) and dimensions. Never describe a placeholder as a final brand asset.

If final assets already exist, preserve and reference them rather than creating placeholders.

### 6.6 UI archive

If a valid UI/design source exists, archive or reference it under `docs/ui/` according to the project source:

- code/prototype package: retain the package structure;
- Figma/XD/external design: record the design reference in `docs/ui/README.md` and keep screenshots of key screens when available;
- backend/API-only project: document UI as `N/A` in `docs/ui/README.md` with the reason.

When the brief names screens but no design export exists, list the screens in `docs/ui/README.md` with status `pending design`. Do not fabricate screenshots or design states.

### 6.7 Detect gaps

After writing, compare what the sources reference with what exists on disk, using the signal table in `references/precheck.md` and the scanner's `referenced_but_missing` output as evidence. A gap is any of:

- a folder or file the standard tree requires that could not be created;
- something the brief or docs mention (screens, wireframes, brand, logo, favicon, OG image, API, payments, auth) with no corresponding folder, file, or documented decision;
- a placeholder standing in for a final asset;
- a required document section left `Open`.

Each gap gets a recommendation with the target path, the default file names, and the document or check that will consume it. Recommendations follow the GEP standard locations (`docs/ui/`, `docs/assets/`, `docs/features/`), not ad hoc folders.

### 6.8 Verify and report

Re-inspect the repository after writing and produce the report in exactly this shape. Keep every section, writing `none` where a section has no entries, so the reader can trust that an empty section means "nothing here" rather than "not checked".

```markdown
# GEP init report: <Project Name>

## Detected
- `<path>`: role (primary requirements source, stack manifest, existing docs, UI source, asset)

## Created
- `<path>`: one-line purpose (say "bootstrap placeholder" where it applies)

## Updated
- `<path>`: what changed, what was preserved

## Preserved
- `<path>`: existing project-specific content left unchanged

## Missing or placeholder
- <item>: why it matters, where it is referenced (file and section)

## Recommended next actions
1. Create `<path>` containing `<default files>`; consumed by `<document or check>`.
2. Replace `<placeholder>` with `<final asset and required dimensions>`; consumed by `<document or check>`.

## Open questions
- <count> recorded in `docs/05-open-questions.md` (<count> blocking): <IDs and one-line topics>

## Verification
Item | Status | Evidence

**Result:** GEP INIT COMPLETE | GEP INIT INCOMPLETE
**Next step:** <one sentence: what the user should do now>
```

Verification statuses are `PASS`, `MISSING`, and `UNVERIFIED`. A placeholder asset that exists with the right dimensions is `PASS` with `placeholder` stated in its Evidence cell, and it is also listed under `Missing or placeholder` so nobody mistakes it for a final asset.

`GEP INIT COMPLETE` requires the required files and folders to exist and the generated documentation to be internally consistent. Open product questions and placeholder assets may remain as long as they are recorded; they do not make the result `INCOMPLETE`. `INCOMPLETE` means a required path could not be created or the documents contradict each other.

## 7. Action: `pchk` - Final / post-implementation check

`pchk` is read-only unless the user separately asks for fixes.

Read `references/postcheck.md` and inspect the actual implementation, configuration, build output where available, and documentation.

Do not rely only on `docs/09-release-readiness.md`; verify claims against repository evidence.

At minimum evaluate:

- final Project Name consistency;
- final logo;
- final favicon;
- final OG/social image exactly 1200x630 px;
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

Use: `PASS`, `FAIL`, `N/A`, `UNVERIFIED`.

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

For each failed, missing, outdated, or unverified item, include the exact file/path when available.

## 9. Supporting references

Use these files as needed:

- `references/precheck.md`: discovery rules, Project Name resolution, project-type signals, the referenced-but-missing signal table, and both `chk` modes.
- `references/docs-scaffold.md`: required documentation structure, minimum contents, recommended files for `docs/ui/` and `docs/assets/`, and the brief-to-document source-coverage table.
- `references/postcheck.md`: final release-readiness checklist.

Load only the references the requested action needs. `extras/` holds optional installer conveniences (Claude Code slash-command wrappers) and is not a runtime reference.
