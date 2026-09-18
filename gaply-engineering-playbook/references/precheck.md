# GEP Precheck Reference

Use this reference for `chk` and the preflight stage of `init`.

## Required inventory

### 1. Project identity

Check for a confirmed project/product name in this order:

1. explicit user instruction/current task context;
2. project brief/product brief;
3. package/app metadata;
4. repository documentation.

Do not treat generic repository names such as `new-app`, `test`, `frontend`, or temporary branch names as confirmed product names.

Status:

- `PASS` if a specific project name is supported by project evidence.
- `MISSING` if no credible project name exists.
- `UNVERIFIED` if names conflict.

### 2. Brief / requirements source

Look for likely sources including:

- `brief.md`, `BRIEF.md`, `product-brief.md`;
- `docs/00-product-brief.md`;
- PRD/requirements/specification files in Markdown, text, PDF, DOCX, or other readable formats;
- explicit project requirements supplied in the current workspace/context.

A brief must provide enough information to understand product purpose and at least the primary scope/core flow. If it exists but is materially incomplete, mark `UNVERIFIED` rather than inventing missing requirements.

### 3. Documentation folder

Check:

- `docs/` first;
- `doc/` and other obvious documentation folders second.

If `docs/` does not exist, report `MISSING — will be created by gep init`.

### 4. UI / design source

Look for:

- `docs/ui/`;
- `ui/`;
- `design/`;
- prototype/source packages;
- Figma or Adobe XD references;
- screenshots of key screens.

For a backend/API-only project, this item may be `N/A` if that scope is supported by the brief.

Do not claim a UI package is complete only because an empty folder exists.

### 5. Logo

Search likely asset locations and names, including:

- `docs/assets/logo*`;
- `public/logo*`, `static/logo*`, `assets/logo*`;
- brand/design source folders.

For initial readiness, either final or clearly labeled bootstrap/default logo is acceptable.

### 6. OG / social image

Search likely asset locations/names:

- `docs/assets/og*`;
- `public/og*`, `public/social*`, `assets/og*`, `assets/social*`.

Initial requirement:

- image exists or can be scaffolded;
- target resolution is exactly 1200×630 px.

If an image exists but dimensions cannot be verified, mark `UNVERIFIED`.

### 7. Favicon

Search likely locations/names:

- `docs/assets/favicon*`;
- `public/favicon*`;
- `app/favicon*`;
- framework-specific icon metadata.

For initial readiness, final or clearly labeled bootstrap/default favicon is acceptable.

## Readiness logic

Block `init` only when:

- Project Name is missing/conflicting without a safe resolution; or
- no usable brief/requirements source exists.

Other missing structure/assets should be reported and can be scaffolded during `init`, provided doing so does not require invented product requirements.
