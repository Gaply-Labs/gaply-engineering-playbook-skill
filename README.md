# Gaply Engineering Playbook Skill (GEP)

راهنمای فارسی: [README.fa.md](README.fa.md)

GEP is an Agent Skill that gives a coding agent (Claude Code, Codex, ChatGPT, claude.ai) one fixed, evidence-based way to create and maintain a software project's documentation, from the first `brief.md` to the release audit. It reads what already exists in your repository, builds the standard `docs/` structure from it, never invents requirements, and ends every run with a report that says what was created, what is still missing, and what to create next.

The standard itself is written out in full, so you can follow it without using the skill at all:

- [Gaply-Engineering-Playbook.md](Gaply-Engineering-Playbook.md) — the standard, English
- [Gaply-Engineering-Playbook.fa.md](Gaply-Engineering-Playbook.fa.md) — the standard, Persian

The skill has three actions:

| Action | What it does | Changes files? | Use it when |
| --- | --- | --- | --- |
| `chk` | Checks the project. Before initialization: are the inputs ready? After initialization: is the documentation complete and in sync with the code? | No | You want a status report and nothing touched. |
| `init` | Creates or updates the documentation structure from your brief/PRD and the code, finds and consolidates brand assets, generates clearly labeled placeholders for what is missing, and reports every gap with a recommendation. Running it again is the sync/update. | Documentation and assets under `docs/` only | You want the missing files created or completed. |
| `pchk` | Audits the real implementation before release: identity and brand, payments, SEO and discovery, accessibility, tests and build, documentation sync. | No | You are about to ship. |

Typical lifecycle: `brief.md` → `chk` → `init` → build the product → `chk` or `init` whenever the docs drift → `pchk` before release.

Every run ends with a Final Checklist (section 7), so you can see the whole state of the project in one screen.

---

## 1. Quick start in Claude Code (inside an existing project)

You are in a project folder where Claude Code already runs. Three steps:

**Step 1. Install the skill into the project.**

```bash
git clone https://github.com/Gaply-Labs/gaply-engineering-playbook-skill.git ~/gaply-engineering-playbook-skill
~/gaply-engineering-playbook-skill/scripts/install.sh claude-project .
```

Or copy the skill folder by hand:

```bash
mkdir -p .claude/skills
cp -R ~/gaply-engineering-playbook-skill/gaply-engineering-playbook .claude/skills/
```

Either way the result is:

```text
your-project/
└── .claude/
    └── skills/
        └── gaply-engineering-playbook/
            ├── SKILL.md
            ├── references/
            ├── scripts/
            ├── agents/
            └── extras/
```

Start a new Claude Code session. New skill folders are discovered at session start; later edits to an existing `SKILL.md` reload automatically.

**Step 2. Check the project without changing anything.**

```text
/gaply-engineering-playbook chk
```

**Step 3. Create the documentation.**

```text
/gaply-engineering-playbook init
```

Plain English works too, and Claude usually selects the skill on its own when you mention GEP or `gep init`:

```text
Use the gaply-engineering-playbook skill and run chk on this project.
```

---

## 2. Which command do I need?

| You want to | Run | Notes |
| --- | --- | --- |
| See the current state and change nothing | `chk` | Read-only. Before init it reports readiness; after init it reports documentation health. |
| Create the documentation from a brief | `init` | Needs only a Project Name and a brief. Everything else is scaffolded. |
| Create or complete missing files | `init` | Reads existing docs first and fills only the gaps. It begins with the same checks as `chk`. |
| Find docs that are outdated after code changes | `chk` | Compares the docs with the code and returns `GEP DOCS IN SYNC` or `GEP DOCS OUT OF SYNC`. |
| Update or sync the docs | `init` | There is no separate update command. `sync` and `update` are aliases of `init`. |
| Tidy brand assets into `docs/assets/` | `init` | Finds them by pattern and moves the ones that are safe to move. |
| Know if the product is ready to release | `pchk` | Read-only release gate with evidence. |

A read-only check never writes. Only `init` writes, and only under `docs/` plus `HANDOFF.md`.

---

## 3. Invoking the skill

### Claude Code

Slash form, with optional parameters after the action:

```text
/gaply-engineering-playbook chk
/gaply-engineering-playbook init
/gaply-engineering-playbook init source=brief.md project="Nimbus Notes" lang=fa
/gaply-engineering-playbook pchk
```

Natural language:

```text
Use the gaply-engineering-playbook skill and initialize this project from brief.md.
```

Optional short commands: copy the three files in `gaply-engineering-playbook/extras/claude-code-commands/` into `.claude/commands/` and you get `/gep-chk`, `/gep-init`, and `/gep-pchk`. They only forward to the skill; the skill is the source of truth.

### Parameters

| Parameter | Effect | Example |
| --- | --- | --- |
| `lang=` or `language=` | Output language. Default English, or the language you wrote the request in. | `lang=fa`, `language=Persian` |
| `project=` (alias `name=`) | The confirmed Project Name. Use it when the brief has no clear name. | `project="Nimbus Notes"` |
| `source=` | The requirements file to use as the primary source of truth. | `source=docs/prd.md` |

Aliases: `check`, `precheck`, `status` for `chk`; `initialize`, `bootstrap`, `scaffold`, `sync`, `update` for `init`; `postcheck`, `release-check`, `final-check`, `audit` for `pchk`.

### Codex

```text
$gaply-engineering-playbook chk
$gaply-engineering-playbook init lang=fa
```

### ChatGPT

```text
@GEP chk
@GEP init
```

The display name is `GEP`; the underlying skill name stays `gaply-engineering-playbook`.

---

## 4. Copy-paste scenarios

**Scenario 1. New project, only `brief.md` exists.**

```text
/gaply-engineering-playbook init source=brief.md
```

or

```text
Use the gaply-engineering-playbook skill and initialize this project from brief.md.
```

Expected: the brief is analyzed, the full `docs/` tree plus `HANDOFF.md` is created, every file the brief can fill is filled, placeholder brand assets are generated, and the run ends with a report plus a Final Checklist.

**Scenario 2. Check only. Change nothing.**

```text
Use gaply-engineering-playbook to check this project. Do not modify any files. Report missing or inconsistent documentation.
```

Expected: `chk` runs. On a project without GEP docs it returns `READY FOR GEP INIT` or `NOT READY FOR GEP INIT`; on an initialized project it returns `GEP DOCS IN SYNC` or `GEP DOCS OUT OF SYNC`. No file changes.

**Scenario 3. Create the files that are missing.**

```text
Use gaply-engineering-playbook to check the project and create the missing documentation files where enough information is available.
```

Expected: `init` runs. It starts with the `chk` checks, keeps existing documentation, adds only the missing files and sections, and records anything the sources do not support in `docs/05-open-questions.md` instead of guessing.

**Scenario 4. The code changed. Are the docs still right?**

```text
Run gaply-engineering-playbook check against the current project and report documentation that is outdated, missing, or inconsistent with the codebase.
```

Expected: `chk` in documentation-health mode compares the feature status, tech stack, architecture, `HANDOFF.md`, and changelog against the repository and marks each row `PASS`, `MISSING`, `OUTDATED`, `N/A`, or `UNVERIFIED`. Follow up with `init` to fix.

**Scenario 5. Build the playbook from the brief as the single source of truth.**

```text
Initialize the project documentation using brief.md as the primary source of truth.
```

Add "using the gaply-engineering-playbook skill" if the agent does not select the skill on its own.

**Scenario 6. Output in Persian.**

```text
/gaply-engineering-playbook init lang=fa
```

**Scenario 7. The brief has no project name.**

```text
/gaply-engineering-playbook init project="Nimbus Notes"
```

**Scenario 8. I already have a logo and a favicon folder. Tidy them up.**

```text
Use gaply-engineering-playbook to init this project. My logo and favicon are already in the repo under their own names.
```

Expected: they are found by pattern, moved into `docs/assets/`, and inventoried. Nothing the application serves is moved.

**Scenario 9. Release audit.**

```text
/gaply-engineering-playbook pchk
```

---

## 5. What happens when only `brief.md` exists

This is the most common starting point and `init` is built for it:

1. Read `brief.md` in full.
2. Extract what it supports: project name, summary, problem, users, core flow, in-scope and out-of-scope items, constraints, design source, payment provider, API exposure, explicit decisions.
3. Classify the project type (public web app, authenticated app, mobile, backend/API, CLI or library) because the type decides which checks apply.
4. Create the standard structure (section 8).
5. Fill every document the brief can fill. Each in-scope item becomes a `PLANNED` feature row and a feature document. Explicit choices in the brief become the first decision records. Every ambiguity becomes an open question with an ID.
6. Find existing brand assets by pattern, consolidate them, and create placeholders only for the kinds that have nothing.
7. Compare what the brief mentions with what exists on disk and turn each gap into a recommendation.
8. Re-inspect the repository, print the report, and end with the Final Checklist.

Only two things stop `init`: no Project Name (fix: `project="Name"`) and no usable brief (fix: `source=path`). A missing `docs/` folder, missing designs, or missing brand assets never stop it.

---

## 6. The `init` report

Every `init` ends with a report in this shape. Sections are always present; `none` means nothing was found, not that the check was skipped.

```markdown
# GEP init report: Nimbus Notes

## Detected
- `brief.md`: primary requirements source
- `docs/logo.png`: existing logo, moved to `docs/assets/logo.png`
- preflight: READY FOR GEP INIT, name from brief title

## Created
- `HANDOFF.md`, `docs/00-product-brief.md`, `docs/07-feature-status.md` ...
- `docs/assets/og-default.png`: bootstrap placeholder, 1200x630

## Updated
- `docs/assets/README.md`: inventory rows for the moved assets

## Preserved
- `brief.md`

## Missing or placeholder
- Banner: no file matching a banner pattern (brief, section Design)
- Final logo and favicon: placeholders in place

## Recommended next actions
1. Create `docs/ui/screens.md` from the Figma file; consumed by feature docs (UX States).
2. Replace `docs/assets/og-default.png` with the final 1200x630 image; consumed by social metadata.
3. Generate a favicon set with https://favicon.io/favicon-converter/ into `docs/assets/favicon/`.

## Open questions
- 4 recorded in `docs/05-open-questions.md` (1 blocking)

## Verification
Item | Status | Evidence
docs/docs-manifest.md | PASS | exists
docs/assets/og-default.png | PASS | 1200x630, placeholder

**Result:** GEP INIT COMPLETE
**Next step:** Answer Q-002, then run `chk` after the first feature is implemented.

## Final Checklist
...
```

`GEP INIT COMPLETE` means the required files exist and agree with each other. Placeholders and open questions do not make it `INCOMPLETE` as long as they are recorded.

---

## 7. The Final Checklist

Every action, `chk`, `init`, and `pchk`, ends with a compact checklist and nothing after it. The detail stays in the sections above; the checklist exists so that scrolling to the bottom tells you the state of the project in one screen.

| Marker | Meaning |
| --- | --- |
| `[x]` | Present and correct |
| `[~]` | Present but incomplete, placeholder, or not wired in |
| `[ ]` | Absent |
| `[-]` | Not applicable, with the reason on the same line |

```text
## Final Checklist

Documentation
[x] GEP structure — 18/18 required paths
[~] docs/ui/README.md — 6 screens listed, no design export
[ ] docs/06-changelog.md — no entries since the first release

Brand assets
[x] Logo — docs/assets/logo.png
[~] Favicon — set in docs/assets/favicon/, not referenced by the app
[ ] Banner — no file matching a banner pattern
[~] OG image — og-default.png 1200x630, placeholder
[x] Inventory — docs/assets/README.md complete

UI and design
[~] Design source — Figma named in the brief, no link recorded
[ ] masterdoc.html — no design package

Discovery and crawling
[ ] robots.txt
[ ] sitemap.xml
[ ] llms.txt
[-] Structured data — no public content pages yet

Metadata and social
[ ] Open Graph tags — no application code yet
[ ] Twitter Card tags

Platform and PWA
[~] Web app manifest — site.webmanifest in docs/assets/favicon/, not served

**Result:** GEP INIT COMPLETE
```

`[~]` is never rounded up to `[x]`. The gap between them is what stops a release. Groups that do not apply to the project type collapse to a single `[-]` line.

---

## 8. What gets created

```text
HANDOFF.md                      current phase, current task, next step, blockers

docs/
├── README.md                   what docs/ is and the reading order
├── docs-manifest.md            every artifact with its status (marks the project as GEP-initialized)
├── 00-product-brief.md         the brief, normalized: name, problem, users, core flow, scope
├── 01-architecture.md          stack, boundaries, deployment, folder structure; unknowns explicit
├── 02-ai-context.md            rules for coding agents working in this repo
├── 03-project-memory.md        durable context not obvious from code
├── 04-decisions.md             append-only decision records (ADRs)
├── 05-open-questions.md        every unresolved point, with Blocking: YES/NO
├── 06-changelog.md             meaningful product and architecture changes
├── 07-feature-status.md        feature table: PLANNED, IN_PROGRESS, DONE, ...
├── 08-tech-stack.md            technologies, versions, reasons
├── 09-release-readiness.md     the release gate that pchk fills with evidence
├── features/
│   └── F001-name.md            one per feature supported by the brief or the code
├── ui/
│   ├── README.md               design source and screen inventory with status
│   ├── masterdoc.html          the design system, when the design was built with Claude Design
│   └── pages/ or desktop/ + mobile/
└── assets/
    ├── README.md               inventory: file, kind, purpose, placeholder | final, dimensions
    ├── logo.*                  or logo-default.svg while it is a placeholder
    ├── banner.*
    ├── favicon/                the generated icon set
    └── og.png                  or og-default.png, exactly 1200x630
```

From a brief alone, `init` fully fills the brief, manifest, README, agent rules, open questions, changelog, feature table, and release gate skeleton; it partially fills architecture, tech stack, decisions, project memory, feature documents, and the UI index; and it leaves sections it cannot support marked `Open (see Q-xxx)`. Files named `*-default.*` are placeholders and must be replaced before release.

---

## 9. Brand assets

Four kinds are tracked: **logo, banner, favicon or app icon set, and OG/social image.**

**They are found by name pattern, not by one fixed path.** A project that already has a logo rarely has it where the playbook would have put it, and reporting a file as missing while you are looking at it is worse than saying nothing. A match on the file name or the folder name is enough:

| Kind | File name contains | Folder name |
| --- | --- | --- |
| Logo | `logo`, `logotype`, `logomark`, `wordmark`, `brandmark`, `brand` | `logo/`, `brand/`, `branding/` |
| Banner | `banner`, `hero`, `cover`, `header-image`, `masthead` | `banner/`, `banners/` |
| Favicon / app icon | `favicon`, `apple-touch-icon`, `android-chrome`, `mstile`, `safari-pinned-tab`, `site.webmanifest` | `favicon/`, `icons/`, `app-icon/` |
| OG / social | `og`, `opengraph`, `social`, `share`, `twitter-card`, `preview`, `card` | `og/`, `social/` |

So `company-logo.png`, `logo_dark.svg`, and a seven-file `favicon/` folder from a generator are all detected.

**Consolidation, without breaking the build:**

| Where the asset is | What `init` does |
| --- | --- |
| `docs/assets/` | Nothing; already correct |
| Anywhere else under `docs/` | Moves it into `docs/assets/`, keeping set folders, so `docs/favicon/` becomes `docs/assets/favicon/` |
| `public/`, `static/`, `src/`, `app/`, `assets/`, `www/`, `resources/`, `web/` | Never moves it. The site depends on that path. It is referenced in the inventory at its real path |

After the move, `init` lists every document that mentions a moved file so the links can be corrected.

**Placeholders** are created only for a kind with nothing at all: `logo-default.svg`, `favicon-default.svg`, `og-default.png` at exactly 1200x630. There is no placeholder banner; a missing banner is reported as a gap. The `*-default.*` suffix is what marks a placeholder, and shipping one fails `pchk`.

**Generation tools**, recommended rather than faked:

| Asset | Tool |
| --- | --- |
| Favicon set | https://favicon.io/favicon-converter/ |
| Mobile app icon set | https://www.digia.tech/tools/app-icon-generator/ |

---

## 10. SEO, discovery and AI discoverability

`chk` and `pchk` check whether the product can be found, crawled, previewed, and installed. These appear in the Final Checklist.

Files, looked for where the site actually serves them (repository root, `public/`, `static/`, `app/`, `src/app/`, `www/`, build output) rather than in `docs/`:

| File | Applies to |
| --- | --- |
| `robots.txt` | Any served site, including authenticated ones, which still need one to disallow |
| `sitemap.xml` | Public indexable sites; a build-time sitemap counts when the config is evidence |
| `llms.txt` | Products that want to be usable by AI agents; recommended, not blocking |
| Web app manifest (`site.webmanifest`, `manifest.json`) | PWA and installable products, including the icon sizes it declares |

A manifest or favicon that exists only under `docs/assets/` is a source asset. It passes only when the application actually serves or references it.

Metadata checked in the code: page title, meta description, canonical URL, Open Graph tags, Twitter Card tags, `og:image` resolving to the final 1200x630 asset over a public URL, Schema.org structured data where it truthfully matches the page, heading hierarchy, and image `alt` text.

Applicability follows the project type. An authenticated app keeps `robots.txt`, headings, `alt` text, and the manifest, and marks indexing and social items `N/A` with the reason. A backend-only project collapses the whole group.

---

## 11. Designing the UI with Claude Design

When you ask the skill to design the UI, it follows a fixed workflow:

- Start a **blank Claude Design project with no preset design system**, so no screen inherits accidental defaults.
- Create **`masterdoc.html` at the root** holding the product overview and the complete design system: colours and tokens, typography, spacing, components and their states, layout rules, light and dark themes.
- `masterdoc.html` carries the button that opens the application preview, or two buttons when desktop and mobile are separate previews.

File structure:

| Project scope | Structure |
| --- | --- |
| Web or desktop only | `masterdoc.html` + `pages/` |
| Desktop and mobile | `masterdoc.html` + `desktop/` + `mobile/` |
| Mobile only | `masterdoc.html` + `pages/` |

Every page states that `masterdoc.html` is the only source of truth for design and implementation, and no page defines its own colours, spacing, type scale, or components. Pages are filled with realistic mock data, not lorem ipsum, and are interactive: navigation, forms with validation, modals, dropdowns, tabs, and the full UX state set (empty, loading, success, validation error, server error, permission error).

**Context pack** to send Claude Design, which is deliberately small:

```text
docs/assets/logo.png
docs/00-product-brief.md
docs/02-ai-context.md
docs/07-feature-status.md
docs/features/
brief.md                  (when it carries brand direction, audience, or positioning)
```

`docs/01-architecture.md` is not in the default pack. Send it only when the architecture is visible to the user: navigation, permissions and roles, or data flow that changes what a screen can show.

The finished package is archived at `docs/ui/`. For Figma or Adobe XD, a link alone is not enough: screenshots of the key screens are required so the repository does not go blind when access changes.

---

## 12. What `chk` reports

Before initialization (no `docs/docs-manifest.md`), a table `Item | Status | Evidence | Required action` with `PASS`, `MISSING`, `N/A`, `UNVERIFIED`, then `READY FOR GEP INIT` or `NOT READY FOR GEP INIT`, a next step, and the Final Checklist.

After initialization, the same shape with `OUTDATED` added, comparing each document against the repository, then `GEP DOCS IN SYNC` or `GEP DOCS OUT OF SYNC`.

## 13. What `pchk` reports

A table `Area | Check | Status | Evidence | Issue / Required fix` with `PASS`, `FAIL`, `N/A`, `UNVERIFIED`, followed by blocking failures, non-blocking findings, unverified items, exactly one overall status (`READY`, `NOT READY`, `NOT VERIFIED`), and the Final Checklist including its engineering group. `pchk` never claims `PASS` without evidence and never fixes anything unless you ask afterwards.

---

## 14. Language

Default output is English. `lang=fa` or a request written in Persian switches the output (and, for `init`, the generated prose) to Persian. File names, identifiers, status tokens, and technical terms stay as they are. The skill files themselves remain in English.

---

## 15. Installing on other platforms

**Claude Code, personal (all your projects):**

```bash
~/gaply-engineering-playbook-skill/scripts/install.sh claude-global
```

or on Windows PowerShell: `.\scripts\install.ps1 claude-global`. The skill lands in `~/.claude/skills/gaply-engineering-playbook/`. If the same skill is installed both personally and in a project, the personal copy wins, so keep them at the same version.

**claude.ai:** upload `dist/gaply-engineering-playbook.zip` in the custom Skills area under Settings. Upload that inner ZIP, not an archive of this whole repository.

**Codex, project:** `./scripts/install.sh codex-project /path/to/project` (lands in `.agents/skills/gaply-engineering-playbook/`). **Codex, personal:** `./scripts/install.sh codex-global`.

**ChatGPT:** Plugins → Skills → Create → Upload from your computer → `dist/gaply-engineering-playbook.zip`. Then `@GEP chk`.

**OpenAI Skills API:**

```bash
curl -X POST 'https://api.openai.com/v1/skills' \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F 'files=@./dist/gaply-engineering-playbook.zip;type=application/zip'
```

---

## 16. Deterministic helper scripts

All three are Python 3, standard library only, so they run anywhere the agent can execute Python.

```bash
python3 gaply-engineering-playbook/scripts/gep_scan.py --root /path/to/project
python3 gaply-engineering-playbook/scripts/gep_scan.py --root /path/to/project --json
```

The scanner reports docs, UI, and brief candidates; brand assets by pattern with their placement, dimensions, and placeholder status; discovery files; whether the project is GEP-initialized; the required GEP tree; and topics the brief mentions without a matching location. It is evidence for the agent, not a verdict: it cannot judge SEO semantics, accessibility, payments, or requirements.

```bash
python3 gaply-engineering-playbook/scripts/organize_assets.py --root /path/to/project
python3 gaply-engineering-playbook/scripts/organize_assets.py --root /path/to/project --apply
```

Moves brand assets that sit loose under `docs/` into `docs/assets/`, keeping set folders intact, and lists every document that mentions a moved file. Without `--apply` it only prints the plan. It never touches assets the application serves.

```bash
python3 gaply-engineering-playbook/scripts/create_bootstrap_assets.py --root /path/to/project --project-name "Nimbus Notes"
```

Creates `docs/assets/logo-default.svg`, `favicon-default.svg`, and `og-default.png` at exactly 1200x630. It refuses to overwrite existing files unless `--force` is given.

---

## 17. Repository layout and source of truth

```text
gaply-engineering-playbook-skill/
├── README.md                              using the skill, English
├── README.fa.md                           using the skill, Persian
├── Gaply-Engineering-Playbook.md          the standard itself, English
├── Gaply-Engineering-Playbook.fa.md       the standard itself, Persian
├── CLAUDE.md                              guidance for Claude Code when editing this repo
├── VERSION
├── gaply-engineering-playbook/            the skill: this folder is what gets installed
│   ├── SKILL.md                           runtime instructions (source of truth)
│   ├── references/
│   │   ├── precheck.md                    chk rules, name resolution, asset patterns, gap signals
│   │   ├── docs-scaffold.md               required tree, minimum contents, brief coverage
│   │   ├── postcheck.md                   release checklist
│   │   ├── final-checklist.md             the closing checklist every action ends with
│   │   └── ui-design.md                   Claude Design workflow, masterdoc.html, context pack
│   ├── scripts/
│   │   ├── gep_scan.py
│   │   ├── organize_assets.py
│   │   └── create_bootstrap_assets.py
│   ├── agents/openai.yaml
│   └── extras/claude-code-commands/
├── scripts/
│   ├── install.sh
│   └── install.ps1
└── dist/
    └── gaply-engineering-playbook.zip     upload package (one top-level folder)
```

`gaply-engineering-playbook/SKILL.md` is the authoritative runtime behavior and `references/` support it. The two playbook files are the human-readable standard: same rules, no agent required. The two READMEs explain how to install and drive the skill.

---

## 18. Troubleshooting

**The skill is not discovered in Claude Code.** Confirm the exact path `.claude/skills/gaply-engineering-playbook/SKILL.md` (or `~/.claude/skills/...`), with `SKILL.md` in uppercase and the skill in its own folder. Start a new session, then ask explicitly: "Use the gaply-engineering-playbook skill and run chk."

**Two copies behave differently.** A personal copy in `~/.claude/skills/` overrides a project copy with the same name.

**An asset I already have was reported as missing.** That is a bug, not intended behavior. Assets are matched by the patterns in section 9; if yours uses a name none of them cover, open an issue with the file name so the pattern can be extended.

**An asset the site serves was moved.** Also a bug. Only assets under `docs/` are moved; `public/`, `static/`, `src/`, `app/`, `assets/`, `www/`, `resources/`, and `web/` are never touched.

**ZIP upload fails.** Upload `dist/gaply-engineering-playbook.zip`, which unpacks to a single `gaply-engineering-playbook/` folder.

**`chk` changed files.** `chk` and `pchk` are read-only; only `init` writes.

**The agent invented requirements.** Missing or ambiguous requirements belong in `docs/05-open-questions.md`.

**`init` stopped.** Only two blockers exist: pass `project="Name"` if the brief has no name, or `source=path` if the brief was not found.

---

## 19. Updating the skill, and keeping four documents in sync

Replace the installed `gaply-engineering-playbook/` folder with the new one (`install.sh` does this). Keep project-specific requirements in the product's own GEP documentation rather than forking the skill. The current version is in `VERSION`.

The standard lives in four files, and they are one document split by language and audience:

```text
Gaply-Engineering-Playbook.md      the standard, English
Gaply-Engineering-Playbook.fa.md   the standard, Persian
README.md                          using the skill, English
README.fa.md                       using the skill, Persian
```

**No change to the skill, its rules, its workflow, or its standards is complete until all four have been reviewed and, where relevant, updated.** A rule that lives in only one of them is a rule half the team will never see, and two languages drifting apart is how one standard quietly becomes two.

---

## Security note

Skills contain instructions and may include executable scripts. Install Skills only from repositories you trust, and review `SKILL.md` and `scripts/` before enabling a third-party Skill.

## Official references

- Anthropic, Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Anthropic, Claude Code skills: https://code.claude.com/docs/en/skills
- OpenAI, Skills in ChatGPT: https://help.openai.com/en/articles/20001066
- OpenAI, Building Skills: https://developers.openai.com/docs/build-skills
- OpenAI, Skills API: https://developers.openai.com/api/docs/guides/tools-skills
