# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is the source package for the **Gaply Engineering Playbook (GEP)** Agent Skill. It is not an application. The deliverable is the skill directory `gaply-engineering-playbook/`, which gets copied into other repositories (Claude Code under `.claude/skills/`, Codex under `.agents/skills/`) or uploaded as a ZIP (claude.ai, ChatGPT, OpenAI Skills API).

Everything else at the root is either the standard in prose or packaging:

- `Gaply-Engineering-Playbook.md` and `Gaply-Engineering-Playbook.fa.md`: the standard itself, written so a team can follow it without the skill. English and Persian.
- `README.md` and `README.fa.md`: how to install and drive the skill. English and Persian.
- `scripts/install.*`, `dist/` (the upload ZIP), `VERSION`.

The skill gives a coding agent three actions to run against a *target* product repository:

| Action | Writes files? | Reference it loads | Overall result strings |
| --- | --- | --- | --- |
| `chk` | No | `references/precheck.md` | Mode A (no `docs/docs-manifest.md`): `READY FOR GEP INIT` / `NOT READY FOR GEP INIT`. Mode B (initialized): `GEP DOCS IN SYNC` / `GEP DOCS OUT OF SYNC` |
| `init` | Docs scaffold + placeholder assets only | `precheck.md` (preflight, gap signals), then `references/docs-scaffold.md` | `GEP INIT COMPLETE` / `GEP INIT INCOMPLETE`, inside a fixed report template (SKILL.md section 6.8) |
| `pchk` | No | `references/postcheck.md` | `READY` / `NOT READY` / `NOT VERIFIED` |

`init` is blocked only when the target has no confirmed Project Name or no usable brief. A brief alone is a valid input: everything else is scaffolded or reported as a gap with a recommendation. `sync` and `update` are aliases of `init`; `project=`, `source=`, and `lang=` are the optional parameters.

Every action ends with the Final Checklist from `references/final-checklist.md`, and nothing follows it.

## Commands

There is no build, lint, or test harness, and no automated tests. Python 3 (stdlib only) is the sole runtime dependency.

Run the deterministic scanner against a target repo (human-readable or JSON):

```bash
python3 gaply-engineering-playbook/scripts/gep_scan.py --root /path/to/project
python3 gaply-engineering-playbook/scripts/gep_scan.py --root /path/to/project --json
```

Move brand assets that sit loose under `docs/` into `docs/assets/`. Prints a plan unless `--apply` is passed, and never touches assets the application serves:

```bash
python3 gaply-engineering-playbook/scripts/organize_assets.py --root /path/to/project
python3 gaply-engineering-playbook/scripts/organize_assets.py --root /path/to/project --apply
```

Generate placeholder assets into `<root>/docs/assets/` (exits 1 rather than overwrite unless `--force`):

```bash
python3 gaply-engineering-playbook/scripts/create_bootstrap_assets.py --root /path/to/project --project-name "Name"
```

Install the skill (destructive: `rm -rf`s an existing skill folder at the destination before copying):

```bash
./scripts/install.sh claude-project|claude-global|codex-project|codex-global [/path/to/project]
```

Smoke-test both scripts in a throwaway directory outside this repo. A brief that mentions Figma screens, a logo, a favicon, a preview card, an API, and Stripe exercises every signal group:

```bash
T=/path/to/scratch/gep-smoke && mkdir -p "$T/docs" && printf '# Brief: Demo\n\nScreens in Figma. Logo and favicon pending. Share links show a preview card. SEO matters. Public REST API. Pro plan via Stripe subscription.\n' > "$T/brief.md"
cp some-image.png "$T/docs/company-logo.png"                                  # an asset under a name the skill never chose
python3 gaply-engineering-playbook/scripts/gep_scan.py --root "$T"            # finds company-logo.png as a logo, flags it to move
python3 gaply-engineering-playbook/scripts/organize_assets.py --root "$T" --apply
python3 gaply-engineering-playbook/scripts/create_bootstrap_assets.py --root "$T" --project-name "Demo"
python3 gaply-engineering-playbook/scripts/gep_scan.py --root "$T" --json     # assets_misplaced empty; og is_1200x630 true
```

The asset patterns are the part most likely to regress. Any change to them must be tested against a project whose assets use the user's own names, not the playbook's defaults.

Syntax checks. Use `ast` rather than `py_compile`: a `__pycache__/` written into the skill dir would travel into the upload ZIP and into every project the skill is copied to. `organize_assets.py` imports `gep_scan`, so it sets `sys.dont_write_bytecode = True` before the import for the same reason; keep that line if you touch its imports. `.gitignore` covers the rest.

```bash
python3 -c "import ast,sys; [ast.parse(open(f).read(), f) for f in sys.argv[1:]]" gaply-engineering-playbook/scripts/*.py
bash -n scripts/install.sh
```

Rebuild the upload ZIP from the repo root after any change under `gaply-engineering-playbook/`. There is no build script and the ZIP is committed. It must unpack to exactly one top-level folder.

```bash
rm -f dist/gaply-engineering-playbook.zip
zip -r dist/gaply-engineering-playbook.zip gaply-engineering-playbook -x '*/__pycache__/*' '*.pyc'
unzip -Z1 dist/gaply-engineering-playbook.zip | cut -d/ -f1 | sort -u   # must print only: gaply-engineering-playbook
```

Behavior changes to SKILL.md or the references have no unit tests. Validate them the way the skill is used: copy a brief-only fixture into a scratch project, have a subagent follow the skill to run `init` and then `chk`, and check that the output matches the report template and result strings above.

## Source-of-truth hierarchy

1. `gaply-engineering-playbook/SKILL.md` is the runtime instruction set and the only file every platform reads. Its frontmatter `name` must stay `gaply-engineering-playbook` and must equal the directory name: installers copy the folder under that name and Claude Code discovers `.claude/skills/<name>/SKILL.md`. `GEP` is only a display name (`agents/openai.yaml`, OpenAI surfaces), and `gep` is only the action prefix parsed in SKILL.md section 1. The frontmatter must stay under 1024 characters.
2. `references/*.md` are loaded on demand per action (table above). SKILL.md tells the agent to load only what the action needs, so checklist detail belongs in the references and SKILL.md stays a router plus the non-negotiable rules and output templates. `precheck.md` owns Project Name resolution, project-type signals, the referenced-but-missing signal table, and both `chk` modes; `docs-scaffold.md` owns the required tree, minimum contents, and the brief-to-document coverage table.
3. `scripts/*.py` produce evidence only. They deliberately decide nothing about business requirements, SEO, payments, or accessibility; that judgment stays in the markdown. The scanner's `referenced_but_missing` output is labeled advisory for the same reason.
4. `extras/claude-code-commands/` are optional slash-command wrappers that forward `$ARGUMENTS` to the skill by its full name. Explicitly non-authoritative.
5. `README.md` and `README.fa.md` cover installation and usage only. They are not runtime behavior, and the Persian file is a parallel guide, not a translation to be regenerated mechanically.

## Cross-file coupling to keep in sync

The same facts are repeated in prose and code, and nothing detects drift. When changing one copy, update all of them:

- **Required doc tree** (`HANDOFF.md`, thirteen `docs/*.md` files, `docs/features/`, `docs/ui/README.md`, `docs/assets/README.md`): SKILL.md section 6.4, `references/docs-scaffold.md` section 1, README.md section 8, README.fa.md section 8, and `REQUIRED_DOCS` in `scripts/gep_scan.py`.
- **Referenced-but-missing signals** (topic words, expected location, default files, consumer): the table in `references/precheck.md` section 3 and the `SIGNALS` list plus `location_present()` in `gep_scan.py`. The scanner reads only product-facing docs (brief, `00-product-brief.md`, `01-architecture.md`, `features/`, `ui/`, root README) on purpose; scanning `09-release-readiness.md` or `02-ai-context.md` would flag every topic.
- **Placeholder asset names and the exact 1200x630 OG size**: `create_bootstrap_assets.py`, `docs-scaffold.md`, SKILL.md section 6.5, both READMEs. The `*-default.*` naming is what the scanner's `placeholder_assets` and `pchk` rely on to tell placeholders from finals.
- **Status vocabularies and result strings** (`PASS/MISSING/N/A/UNVERIFIED` for `chk` Mode A, plus `OUTDATED` in Mode B; `PASS/FAIL/N/A/UNVERIFIED` for `pchk`; the overall results in the table above; the `init` report section headings): SKILL.md, `precheck.md`, `postcheck.md`, README.md, README.fa.md. Agents and users match on these exact strings.
- **Aliases and parameters** (`status`, `sync`, `update`, `audit`; `project=`, `source=`, `lang=`): SKILL.md section 1, README.md section 3, README.fa.md section 3, `agents/openai.yaml` default prompt.
- **Initialization marker** `docs/docs-manifest.md`: SKILL.md sections 1 and 5, `precheck.md` section 1.3, `gep_initialized` in `gep_scan.py`, README section 12.
- **Brand asset patterns and placement** (four kinds, the name and folder patterns, and which locations `init` may move from): `references/precheck.md` section 1.5, SKILL.md section 6.5, `ASSET_KINDS` plus `APP_ASSET_ROOTS` and `placement_of()` in `gep_scan.py`, `organize_assets.py` (which imports them), README.md section 9, README.fa.md section 9, and section 9 of both playbooks.
- **Discovery files** (`robots.txt`, `sitemap.xml`, `llms.txt`, web app manifest): `references/precheck.md` section 1.6, `references/postcheck.md` section 3, `DISCOVERY_FILES` and `DISCOVERY_ROOTS` in `gep_scan.py`, `references/final-checklist.md` group 4, README section 10, and section 10 of both playbooks.
- **Final Checklist** (markers, group order, applicability): `references/final-checklist.md`, SKILL.md section 8, README section 7, and section 16 of both playbooks.
- **Claude Design workflow** (`masterdoc.html`, file structure per scope, page rules, context pack): `references/ui-design.md`, SKILL.md section 6.6, README section 11, and section 8 of both playbooks, including Prompt E.
- **Asset generation tools** (favicon.io, digia.tech): `references/precheck.md`, `references/ui-design.md`, SKILL.md section 6.5, README section 9, and section 9 of both playbooks.
- **Version**: `VERSION`.
- **`dist/gaply-engineering-playbook.zip`**: rebuild after any skill change (command above).

## Constraints that shape the code

- Scripts must stay **stdlib-only** so they run wherever a bare `python3` exists, including platform code-execution sandboxes without `pip`. That is why PNG and JPEG headers are parsed by hand and the OG PNG is emitted with `struct` + `zlib` instead of Pillow.
- Skill prose stays in **English**. Output language (for example `lang=fa`) is resolved at runtime by SKILL.md section 2, never by translating the skill files.
- The skill's core promise is **no invented requirements and no `PASS` without evidence**. Edits to SKILL.md or the references must preserve the read-only guarantee of `chk` and `pchk`, the "docs and placeholder assets only" scope of `init`, and the rule that `init` never stops for anything other than a missing name or missing brief.
- Every gap in a report must carry a recommendation pointing at a standard GEP location (`docs/ui/`, `docs/assets/`, `docs/features/`), never an ad hoc folder. Adding a new standard location means touching the tree coupling above.
- `.remember/` at the repo root belongs to a local Claude Code plugin and is self-ignored via its own `.gitignore`. It is not part of the package.

## The four-document rule

The standard lives in four files and they are one document split by language and audience:

```text
Gaply-Engineering-Playbook.md      the standard, English
Gaply-Engineering-Playbook.fa.md   the standard, Persian
README.md                          using the skill, English
README.fa.md                       using the skill, Persian
```

**No change to the skill, its rules, its workflow, or its standards is complete until all four have been reviewed and, where relevant, updated.** This is a user instruction, not a style preference. Before reporting a skill change as done, check each of the four and say in the report which ones changed and which needed no change.

The Persian files are parallel guides, not machine translations. When updating them, reuse the existing Persian wording for unchanged sections rather than re-translating from English, and keep technical terms in Latin script inside Persian sentences, which is the style both Persian files already use.
