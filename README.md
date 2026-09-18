# Gaply Engineering Playbook Skill (GEP)

Reusable Agent Skill for applying the **Gaply Engineering Playbook** to software repositories.

The skill supports three core workflows:

- `chk` — read-only initial project check.
- `init` — create/synchronize the initial GEP documentation structure and bootstrap assets, then verify the result.
- `pchk` — read-only final implementation and release-readiness audit.

The same `SKILL.md` package is designed to work with **ChatGPT/OpenAI**, **Codex**, **Claude Code**, and **claude.ai** where custom Agent Skills are supported.

---

## 1. What the skill checks

### `chk` — Initial check

Checks the project before GEP initialization, including:

- confirmed project name;
- brief / PRD / requirements source;
- documentation folder;
- UI/design source;
- logo;
- favicon;
- OG/social image;
- OG image dimensions (`1200x630`).

It returns an evidence-based checklist and one of:

- `READY FOR GEP INIT`
- `NOT READY FOR GEP INIT`

`chk` never modifies the project.

### `init` — Documentation initialization

Creates or synchronizes the standard GEP structure:

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

If final brand assets do not exist yet, the skill can create clearly labeled bootstrap assets:

- `logo-default.svg`
- `favicon-default.svg`
- `og-default.png` at exactly `1200x630`

Bootstrap assets are placeholders and must not be treated as final release assets.

After initialization the skill re-checks the repository and returns:

- `GEP INIT COMPLETE`
- `GEP INIT INCOMPLETE`

### `pchk` — Final check

Audits the actual implementation before release, including:

- final project name consistency;
- final logo and favicon;
- final `og:image` at `1200x630`;
- social metadata;
- payment integration when applicable (RevenueCat, Stripe, MoonPay, or another approved provider);
- SEO metadata;
- semantic `h1` / `h2` / `h3` hierarchy;
- image `alt` text;
- canonical / sitemap / robots where applicable;
- W3C/HTML validity evidence where applicable;
- WCAG 2.2 AA essentials;
- keyboard navigation and visible focus;
- form labels and accessible errors;
- screen-reader smoke-test evidence for critical flows;
- removal of placeholder/debug/model/prompt text;
- unnecessary generated-writing artifacts such as gratuitous em dashes;
- tests, build, security, permissions, and secret checks;
- documentation synchronization.

Final result:

- `READY`
- `NOT READY`
- `NOT VERIFIED`

`pchk` is read-only unless you separately ask the agent to fix findings.

---

## 2. Language behavior

Default output language is **English**.

You can explicitly set another language:

```text
gep chk lang=fa
gep init lang=fa
gep pchk lang=fa
```

You can also use:

```text
language=Persian
language=English
```

Resolution order:

1. Explicit `lang=` / `language=` parameter.
2. Otherwise, the dominant language of the instruction after the command.
3. Otherwise, English.

The skill itself remains written in English.

---

## 3. Repository package structure

```text
gaply-engineering-playbook-skill-v1.0.0/
├── README.md
├── gaply-engineering-playbook/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── references/
│   │   ├── precheck.md
│   │   ├── docs-scaffold.md
│   │   └── postcheck.md
│   ├── scripts/
│   │   ├── gep_scan.py
│   │   └── create_bootstrap_assets.py
│   └── extras/
│       └── claude-code-commands/
│           ├── gep-chk.md
│           ├── gep-init.md
│           └── gep-pchk.md
├── scripts/
│   ├── install.sh
│   └── install.ps1
└── dist/
    └── gaply-engineering-playbook.zip
```

`gaply-engineering-playbook/` is the canonical skill directory.

`dist/gaply-engineering-playbook.zip` contains exactly one top-level skill folder and is intended for platforms that accept direct ZIP uploads.

---

# Installation

## 4. Claude Code — project-level installation

Claude Code discovers project Skills from:

```text
.claude/skills/<skill-name>/SKILL.md
```

From your project root, copy the canonical skill folder:

### macOS / Linux

```bash
mkdir -p .claude/skills
cp -R /path/to/gaply-engineering-playbook .claude/skills/
```

Or use the included installer from this repository:

```bash
./scripts/install.sh claude-project /path/to/your-project
```

Expected result:

```text
your-project/
└── .claude/
    └── skills/
        └── gaply-engineering-playbook/
            ├── SKILL.md
            ├── references/
            ├── scripts/
            └── agents/
```

Start a new Claude Code session after installation if the skill is not immediately discovered.

### Suggested usage in Claude Code

Claude can select the Skill automatically when the request matches its description. You can also invoke it explicitly using the Skill name and action, for example:

```text
/gaply-engineering-playbook chk
/gaply-engineering-playbook init lang=fa
/gaply-engineering-playbook pchk
```

If your Claude Code version does not expose the Skill as a slash command, ask explicitly:

```text
Use the gaply-engineering-playbook skill and run chk.
```

The package also includes optional wrapper examples under:

```text
gaply-engineering-playbook/extras/claude-code-commands/
```

These wrappers are optional. The Skill itself is the source of truth.

---

## 5. Claude Code — global/personal installation

To make the Skill available across your local Claude Code projects, install it under:

```text
~/.claude/skills/gaply-engineering-playbook/
```

### macOS / Linux

```bash
mkdir -p ~/.claude/skills
cp -R ./gaply-engineering-playbook ~/.claude/skills/
```

Or:

```bash
./scripts/install.sh claude-global
```

### Windows PowerShell

```powershell
.\scripts\install.ps1 claude-global
```

---

## 6. claude.ai — ZIP upload

Custom Skills can be uploaded as ZIP files in supported claude.ai plans/configurations.

Use this file from the repository package:

```text
dist/gaply-engineering-playbook.zip
```

In claude.ai, open the custom Skills area under Settings/Features (exact UI wording can vary), then upload the ZIP.

Important:

- Upload the **inner** `dist/gaply-engineering-playbook.zip`, not the complete GitHub repository ZIP.
- Each user may need to upload the Skill separately depending on workspace configuration.
- Custom Skill availability depends on the current Claude plan and Code Execution settings.

Official Anthropic Skill format requires a directory containing `SKILL.md` with `name` and `description` frontmatter. This package follows that format.

---

## 7. Codex — project-level installation

Codex discovers repository Skills from:

```text
.agents/skills/<skill-name>/SKILL.md
```

From your project root:

### macOS / Linux

```bash
mkdir -p .agents/skills
cp -R /path/to/gaply-engineering-playbook .agents/skills/
```

Or use:

```bash
./scripts/install.sh codex-project /path/to/your-project
```

Expected result:

```text
your-project/
└── .agents/
    └── skills/
        └── gaply-engineering-playbook/
            ├── SKILL.md
            ├── references/
            ├── scripts/
            └── agents/
```

Codex may automatically select the Skill based on its description, or you can invoke it explicitly.

Suggested explicit usage:

```text
$gaply-engineering-playbook chk
$gaply-engineering-playbook init lang=fa
$gaply-engineering-playbook pchk
```

If you use a shortened UI display name such as `GEP`, the visible picker label may differ from the underlying Skill `name`.

---

## 8. Codex — global/personal installation

For a personal Skill available across repositories, install it under:

```text
~/.agents/skills/gaply-engineering-playbook/
```

### macOS / Linux

```bash
mkdir -p ~/.agents/skills
cp -R ./gaply-engineering-playbook ~/.agents/skills/
```

Or:

```bash
./scripts/install.sh codex-global
```

### Windows PowerShell

```powershell
.\scripts\install.ps1 codex-global
```

If a newly installed Skill does not appear, restart Codex and start a new session.

---

## 9. ChatGPT — upload/install

ChatGPT Skills can be uploaded where Skills are enabled for your account/workspace.

Use:

```text
dist/gaply-engineering-playbook.zip
```

Typical flow:

1. Open ChatGPT.
2. Open **Plugins**.
3. Open the **Skills** section/tab.
4. Select **Create**.
5. Choose **Upload from your computer**.
6. Upload `dist/gaply-engineering-playbook.zip`.
7. Review the Skill contents and install it.

After installation, ChatGPT can select the Skill automatically or you can explicitly select/@-mention it.

Suggested usage:

```text
@GEP chk
@GEP init lang=fa
@GEP pchk
```

Depending on the surface, the display name may appear as **GEP** while the underlying Skill name remains `gaply-engineering-playbook`.

Workspace owners/admins may control whether members can create, install, upload, or share Skills.

---

## 10. OpenAI Skills API — optional

For API-based Skill registration, upload the standalone ZIP:

```text
dist/gaply-engineering-playbook.zip
```

Example:

```bash
curl -X POST 'https://api.openai.com/v1/skills' \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F 'files=@./dist/gaply-engineering-playbook.zip;type=application/zip'
```

The ZIP intentionally contains exactly one top-level folder, which matches the OpenAI Skills API packaging requirement.

---

# Usage

## 11. `chk` examples

English:

```text
gep chk
```

Persian:

```text
gep chk lang=fa
```

Expected output format:

```text
Item | Status | Evidence | Required action
```

Statuses:

- `PASS`
- `MISSING`
- `N/A`
- `UNVERIFIED`

No project files should be changed.

---

## 12. `init` examples

```text
gep init
```

or:

```text
gep init lang=fa
```

Before modifying files, `init` performs the same initial checks as `chk`.

Blocking conditions:

- no confirmed Project Name;
- no usable brief / PRD / requirements source.

If either blocker exists, initialization must stop instead of inventing product information.

After creation/synchronization, the Skill verifies the result and reports every created/updated file.

---

## 13. `pchk` examples

```text
gep pchk
```

or:

```text
gep pchk lang=fa
```

Expected table:

```text
Area | Check | Status | Evidence | Issue / Required fix
```

Statuses:

- `PASS`
- `FAIL`
- `N/A`
- `UNVERIFIED`

The Skill must not claim `PASS` without evidence.

---

# Deterministic helper scripts

## 14. Repository scanner

The Skill includes a dependency-free scanner:

```bash
python3 gaply-engineering-playbook/scripts/gep_scan.py --root /path/to/project
```

JSON output:

```bash
python3 gaply-engineering-playbook/scripts/gep_scan.py --root /path/to/project --json
```

It checks deterministic items such as:

- docs paths;
- UI/design paths;
- likely brief files;
- logo candidates;
- favicon candidates;
- OG image candidates;
- PNG/JPEG dimensions;
- expected GEP documentation structure.

It does **not** replace semantic review of SEO, accessibility, payments, security, or product requirements.

---

## 15. Bootstrap asset generator

When a confirmed Project Name exists and bootstrap assets are missing:

```bash
python3 gaply-engineering-playbook/scripts/create_bootstrap_assets.py \
  --root /path/to/project \
  --project-name "Example Project"
```

Creates:

```text
docs/assets/logo-default.svg
docs/assets/favicon-default.svg
docs/assets/og-default.png
```

The OG image is exactly `1200x630`.

These are intentionally obvious placeholders and must be replaced by final brand assets before public release.

---

# Team / GitHub workflow

## 16. Recommended team setup

Keep this repository as the source repository for the GEP Skill.

For a product repository, choose one of these approaches:

### Option A — Install directly into each product repository

Claude Code:

```text
.claude/skills/gaply-engineering-playbook/
```

Codex:

```text
.agents/skills/gaply-engineering-playbook/
```

This makes the Skill version explicit in that repository.

### Option B — Personal/global installation

Claude Code:

```text
~/.claude/skills/gaply-engineering-playbook/
```

Codex:

```text
~/.agents/skills/gaply-engineering-playbook/
```

Use this when developers want the Skill available across many repositories.

### Option C — Upload the standalone Skill ZIP

Use:

```text
dist/gaply-engineering-playbook.zip
```

for supported ChatGPT / claude.ai / API upload flows.

---

## 17. Recommended first test

Create a temporary repository with only a simple brief, for example:

```text
test-project/
└── brief.md
```

Then run:

```text
gep chk
```

Expected:

- Project Name may be missing unless present in the brief.
- `docs/` may be reported as missing.
- UI/assets may be missing.
- No files should be created.

Then add a confirmed project name to the brief and run:

```text
gep init
```

Expected:

- documentation scaffold created;
- missing bootstrap assets handled;
- post-init verification returned.

Finally, after implementing a sample application:

```text
gep pchk
```

Expected:

- evidence-based final readiness report;
- no automatic fixes unless explicitly requested.

---

# Troubleshooting

## 18. Skill is not discovered in Claude Code

Check the exact path:

```text
.claude/skills/gaply-engineering-playbook/SKILL.md
```

or:

```text
~/.claude/skills/gaply-engineering-playbook/SKILL.md
```

Then:

- confirm `SKILL.md` is uppercase exactly as shown;
- confirm the Skill folder is directly under `skills/`;
- start a new Claude Code session;
- explicitly ask Claude to use `gaply-engineering-playbook`.

Do not place the file like this:

```text
.claude/skills/SKILL.md
```

The Skill must have its own directory.

---

## 19. Skill is not discovered in Codex

Check:

```text
.agents/skills/gaply-engineering-playbook/SKILL.md
```

or:

```text
~/.agents/skills/gaply-engineering-playbook/SKILL.md
```

Then restart Codex/start a new session if necessary.

---

## 20. ZIP upload fails

For direct Skill upload, use:

```text
dist/gaply-engineering-playbook.zip
```

Do **not** upload the complete GitHub repository ZIP unless the product explicitly expects a repository archive.

The standalone ZIP should unpack to:

```text
gaply-engineering-playbook/
├── SKILL.md
├── agents/
├── references/
├── scripts/
└── extras/
```

There should not be an extra repository folder above `gaply-engineering-playbook/` inside the standalone ZIP.

---

## 21. `chk` changes files

That is incorrect behavior.

`chk` and `pchk` must be read-only.

Only `init` may create/update GEP documentation and bootstrap assets.

---

## 22. Agent invents missing requirements

That is also incorrect behavior.

Missing/ambiguous requirements must be recorded in:

```text
docs/05-open-questions.md
```

The agent must not silently create business rules that are not supported by the brief, code, or explicit user instruction.

---

# Updating the Skill

## 23. Updating a project installation

Replace the existing Skill directory with the new canonical folder:

```text
gaply-engineering-playbook/
```

Do not manually merge old generic instructions into the new Skill unless you intentionally customized them.

For product-specific requirements, prefer storing those requirements in the product's own GEP documentation instead of forking the general Skill.

---

# Source of truth

The authoritative Skill instructions are:

```text
gaply-engineering-playbook/SKILL.md
```

Supporting references:

```text
gaply-engineering-playbook/references/
```

Helper scripts:

```text
gaply-engineering-playbook/scripts/
```

`README.md` explains installation and usage. It is not the runtime source of truth for Skill behavior.

---

# Official references

OpenAI:

- Skills in ChatGPT: https://help.openai.com/en/articles/20001066
- Building Skills: https://developers.openai.com/docs/build-skills
- OpenAI Skills API: https://developers.openai.com/api/docs/guides/tools-skills
- OpenAI Academy — Using Skills: https://openai.com/academy/skills/

Anthropic:

- Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Repository/managed agent Skills: https://platform.claude.com/docs/en/managed-agents/skills

---

## Security note

Skills contain instructions and may include executable scripts. Only install Skills from repositories you trust. Review `SKILL.md` and scripts before enabling a third-party Skill in a development environment.
