# Gaply Engineering Playbook Skill (GEP)

راهنمای فارسی: [README.fa.md](README.fa.md)

GEP is an Agent Skill that gives a coding agent (Claude Code, Codex, ChatGPT, claude.ai) one fixed, evidence-based way to create and maintain a software project's documentation, from the first `brief.md` to the release audit. It reads what already exists in your repository, builds the standard `docs/` structure from it, never invents requirements, and ends every run with a report that says what was created, what is still missing, and what to create next.

It has three actions:

| Action | What it does | Changes files? | Use it when |
| --- | --- | --- | --- |
| `chk` | Checks the project. Before initialization: are the inputs ready? After initialization: is the documentation complete and in sync with the code? | No | You want a status report and nothing touched. |
| `init` | Creates or updates the documentation structure from your brief/PRD and the code, generates clearly labeled placeholder brand assets when the final ones do not exist yet, and reports every gap with a recommendation. Running it again is the sync/update. | Documentation and placeholder assets only | You want the missing files created or completed. |
| `pchk` | Audits the real implementation before release: identity and brand, payments, SEO, accessibility, tests and build, documentation sync. | No | You are about to ship. |

Typical lifecycle: `brief.md` -> `chk` -> `init` -> build the product -> `chk` or `init` whenever the docs drift -> `pchk` before release.

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
| Create or complete missing files | `init` | `init` reads existing docs first and fills only the gaps. It begins with the same checks as `chk`. |
| Find docs that are outdated after code changes | `chk` | Compares the docs with the code and returns `GEP DOCS IN SYNC` or `GEP DOCS OUT OF SYNC`. |
| Update or sync the docs | `init` | There is no separate update command. `sync` and `update` are aliases of `init`. |
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

Expected: the brief is analyzed, the full `docs/` tree plus `HANDOFF.md` is created, every file the brief can fill is filled, placeholder brand assets are generated, and the run ends with a report (section 6).

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

Expected: `chk` in documentation-health mode compares `07-feature-status.md`, `08-tech-stack.md`, `01-architecture.md`, `HANDOFF.md`, and the changelog against the repository and marks rows `PASS`, `MISSING`, `OUTDATED`, `N/A`, or `UNVERIFIED`. Follow up with `init` to fix.

**Scenario 5. Build the playbook from the brief as the single source of truth.**

```text
Initialize the project documentation using brief.md as the primary source of truth.
```

Add "using the gaply-engineering-playbook skill" if the agent does not select the skill on its own.

**Scenario 6. Output in Persian.**

```text
/gaply-engineering-playbook init lang=fa
```

Or write the request in Persian; the skill answers in the language of the request.

**Scenario 7. The brief has no project name.**

```text
/gaply-engineering-playbook init project="Nimbus Notes"
```

**Scenario 8. Release audit.**

```text
/gaply-engineering-playbook pchk
```

---

## 5. What happens when only `brief.md` exists

This is the most common starting point and `init` is built for it:

1. Read `brief.md` in full.
2. Extract what it supports: project name, summary, problem, users, core flow, in-scope and out-of-scope items, constraints, design source, payment provider, API exposure, explicit decisions.
3. Classify the project type (public web app, authenticated app, mobile, backend/API, CLI or library) because the type decides which checks apply.
4. Create the standard structure (section 7).
5. Fill every document the brief can fill. Each in-scope item becomes a `PLANNED` feature row and a feature document. Explicit choices in the brief become the first decision records. Every ambiguity becomes an open question with an ID.
6. Create placeholder brand assets under `docs/assets/` when final ones do not exist, and record them as placeholders.
7. Compare what the brief mentions with what exists on disk and turn each gap into a recommendation.
8. Re-inspect the repository and print the report.

Only two things stop `init`: no Project Name (fix: `project="Name"`) and no usable brief (fix: `source=path`). A missing `docs/` folder, missing designs, or missing brand assets never stop it; they are created or reported.

---

## 6. The `init` report

Every `init` ends with a report in this shape. Sections are always present; `none` means nothing was found, not that the check was skipped.

```markdown
# GEP init report: Nimbus Notes

## Detected
- `brief.md`: primary requirements source
- stack manifests: none (no code yet)

## Created
- `HANDOFF.md`: current phase and next step
- `docs/00-product-brief.md`: derived from brief.md
- `docs/07-feature-status.md`: 5 PLANNED features
- `docs/features/F001-notes.md` ... `F005-public-api.md`
- `docs/ui/README.md`: 6 screens listed as pending design (Figma link pending)
- `docs/assets/logo-default.svg`: bootstrap placeholder
- `docs/assets/og-default.png`: bootstrap placeholder, 1200x630
- ...

## Updated
- none

## Preserved
- none

## Missing or placeholder
- Figma design export: brief names 6 screens, no design files exist (brief, section Design)
- Final logo and favicon: placeholders in place (brief, section Design)
- Stripe integration details: provider named, no plan or webhook requirements (brief, In scope)

## Recommended next actions
1. Create `docs/ui/screens.md` and `docs/ui/screenshots/` from the Figma file; consumed by feature docs (UX States).
2. Replace `docs/assets/logo-default.svg` and `favicon-default.svg` with the final brand files; consumed by `09-release-readiness.md` section 1.
3. Replace `docs/assets/og-default.png` with the final 1200x630 image; consumed by social metadata.
4. Answer Q-002 (Stripe plan and webhook requirements) and record the decision in `docs/04-decisions.md`; consumed by `F004-pro-plan.md`.

## Open questions
- 4 recorded in `docs/05-open-questions.md` (1 blocking): Q-001 project type (public summary pages), Q-002 Stripe plans, Q-003 free-plan limits, Q-004 API auth

## Verification
Item | Status | Evidence
docs/docs-manifest.md | PASS | exists
docs/assets/og-default.png | PASS | 1200x630 (gep_scan)

**Result:** GEP INIT COMPLETE
**Next step:** Answer Q-002, then run `chk` after the first feature is implemented.
```

`GEP INIT COMPLETE` means the required files exist and agree with each other. Placeholders and open questions do not make it `INCOMPLETE` as long as they are recorded.

---

## 7. What gets created

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
│   ├── screens.md              (recommended) per-screen states
│   ├── flows.md                (recommended) user flows
│   └── screenshots/            (recommended) one PNG per key screen
└── assets/
    ├── README.md               asset inventory: file, purpose, placeholder | final, dimensions
    ├── logo-default.svg        placeholder until the final logo
    ├── favicon-default.svg     placeholder until the final favicon
    └── og-default.png          placeholder, exactly 1200x630, until the final og.png
```

From a brief alone, `init` fully fills the brief, manifest, README, agent rules, open questions, changelog, feature table, and release gate skeleton; it partially fills architecture, tech stack, decisions, project memory, feature documents, and the UI index; and it leaves sections it cannot support marked `Open (see Q-xxx)`. Files named `*-default.*` are placeholders and must be replaced before release.

---

## 8. What `chk` reports

Before initialization (no `docs/docs-manifest.md`):

```text
Item | Status | Evidence | Required action
Project Name | PASS | brief.md title "Nimbus Notes" | -
Brief / requirements | PASS | brief.md, 6 sections | -
docs/ folder | MISSING | none found | will be created by gep init
UI / design source | MISSING | brief mentions Figma, no export | list screens as pending design
Logo | MISSING | none found | bootstrap logo will be created
OG image 1200x630 | MISSING | none found | bootstrap og-default.png will be created
Favicon | MISSING | none found | bootstrap favicon will be created

READY FOR GEP INIT
Next step: gep init
```

Statuses: `PASS`, `MISSING`, `N/A`, `UNVERIFIED`. Result: `READY FOR GEP INIT` or `NOT READY FOR GEP INIT`.

After initialization: the same table shape with `OUTDATED` added, comparing each document with the repository, then `GEP DOCS IN SYNC` or `GEP DOCS OUT OF SYNC` and a next step (`init` to fill gaps, `pchk` before release).

## 9. What `pchk` reports

A table `Area | Check | Status | Evidence | Issue / Required fix` with `PASS`, `FAIL`, `N/A`, `UNVERIFIED`, followed by blocking failures, non-blocking findings, unverified items, and exactly one overall status: `READY`, `NOT READY`, or `NOT VERIFIED`. `pchk` never claims `PASS` without evidence and never fixes anything unless you ask afterwards.

---

## 10. Language

Default output is English. `lang=fa` or a request written in Persian switches the output (and, for `init`, the generated prose) to Persian. File names, identifiers, and technical terms stay as they are. The skill files themselves remain in English.

---

## 11. Installing on other platforms

**Claude Code, personal (all your projects):**

```bash
~/gaply-engineering-playbook-skill/scripts/install.sh claude-global
```

or on Windows PowerShell: `.\scripts\install.ps1 claude-global`. The skill lands in `~/.claude/skills/gaply-engineering-playbook/`. If the same skill is installed both personally and in a project, the personal copy wins, so keep them at the same version.

**claude.ai:** upload `dist/gaply-engineering-playbook.zip` in the custom Skills area under Settings. Upload that inner ZIP, not an archive of this whole repository.

**Codex, project:** `./scripts/install.sh codex-project /path/to/project` (lands in `.agents/skills/gaply-engineering-playbook/`). **Codex, personal:** `./scripts/install.sh codex-global` (lands in `~/.agents/skills/`).

**ChatGPT:** Plugins -> Skills -> Create -> Upload from your computer -> `dist/gaply-engineering-playbook.zip`. Then `@GEP chk`.

**OpenAI Skills API:**

```bash
curl -X POST 'https://api.openai.com/v1/skills' \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F 'files=@./dist/gaply-engineering-playbook.zip;type=application/zip'
```

The ZIP contains exactly one top-level folder, which both the API and the upload flows require.

---

## 12. Deterministic helper scripts

Both scripts are Python 3, standard library only, so they run anywhere the agent can execute Python.

```bash
python3 gaply-engineering-playbook/scripts/gep_scan.py --root /path/to/project
python3 gaply-engineering-playbook/scripts/gep_scan.py --root /path/to/project --json
```

The scanner reports docs, UI, brief, logo, favicon, and OG candidates with image dimensions; whether the project is GEP-initialized; placeholder assets still in place; the required GEP tree; and topics the brief or product docs mention without a matching location (`referenced_but_missing`). It is evidence for the agent, not a verdict: it cannot judge SEO, accessibility, payments, or requirements.

```bash
python3 gaply-engineering-playbook/scripts/create_bootstrap_assets.py --root /path/to/project --project-name "Nimbus Notes"
```

Creates `docs/assets/logo-default.svg`, `favicon-default.svg`, and `og-default.png` at exactly 1200x630. It refuses to overwrite existing files unless `--force` is given.

---

## 13. Repository layout and source of truth

```text
gaply-engineering-playbook-skill/          repository root (this repo)
├── README.md                              this guide
├── README.fa.md                           Persian guide
├── CLAUDE.md                              guidance for Claude Code when editing this repo
├── VERSION
├── CONTENTS.txt
├── gaply-engineering-playbook/            the skill: this folder is what gets installed
│   ├── SKILL.md                           runtime instructions (source of truth)
│   ├── references/
│   │   ├── precheck.md                    chk rules, name resolution, gap signals
│   │   ├── docs-scaffold.md               required tree, minimum contents, brief coverage
│   │   └── postcheck.md                   release checklist
│   ├── scripts/
│   │   ├── gep_scan.py
│   │   └── create_bootstrap_assets.py
│   ├── agents/openai.yaml                 display metadata for OpenAI surfaces
│   └── extras/claude-code-commands/       optional /gep-chk, /gep-init, /gep-pchk wrappers
├── scripts/
│   ├── install.sh
│   └── install.ps1
└── dist/
    └── gaply-engineering-playbook.zip     upload package (one top-level folder)
```

`gaply-engineering-playbook/SKILL.md` is the authoritative behavior. `references/` support it. This README explains installation and usage; it does not define behavior.

---

## 14. Troubleshooting

**The skill is not discovered in Claude Code.** Confirm the exact path `.claude/skills/gaply-engineering-playbook/SKILL.md` (or `~/.claude/skills/...`), with `SKILL.md` in uppercase and the skill in its own folder, not `.claude/skills/SKILL.md`. Start a new session. Then ask explicitly: "Use the gaply-engineering-playbook skill and run chk."

**Two copies behave differently.** A personal copy in `~/.claude/skills/` overrides a project copy with the same name. Update or remove one of them.

**ZIP upload fails.** Upload `dist/gaply-engineering-playbook.zip`, which unpacks to a single `gaply-engineering-playbook/` folder. Do not upload an archive of the whole repository.

**`chk` changed files.** That is a bug in the run, not intended behavior. `chk` and `pchk` are read-only; only `init` writes.

**The agent invented requirements.** Also incorrect. Missing or ambiguous requirements belong in `docs/05-open-questions.md`, and the agent must not create business rules unsupported by the brief, the code, or your explicit instruction.

**`init` stopped.** Only two blockers exist. Pass `project="Name"` if the brief has no name, or `source=path` if the brief was not found.

---

## 15. Updating the skill

Replace the installed `gaply-engineering-playbook/` folder with the new one (`install.sh` does this). Keep project-specific requirements in the product's own GEP documentation rather than forking the skill. The current version is in `VERSION`.

---

## Security note

Skills contain instructions and may include executable scripts. Install Skills only from repositories you trust, and review `SKILL.md` and `scripts/` before enabling a third-party Skill.

## Official references

- Anthropic, Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Anthropic, Claude Code skills: https://code.claude.com/docs/en/skills
- OpenAI, Skills in ChatGPT: https://help.openai.com/en/articles/20001066
- OpenAI, Building Skills: https://developers.openai.com/docs/build-skills
- OpenAI, Skills API: https://developers.openai.com/api/docs/guides/tools-skills
