# GEP Postcheck / Release Readiness Reference

Use this reference for `pchk`.

The audit must compare documentation claims with the actual repository and available runtime/build evidence.

## 1. Identity & Brand

- Final Project Name is consistent across product brief, application metadata/title, package/config where relevant, and public metadata.
- Final logo exists and is not a bootstrap/default placeholder.
- `docs/assets/README.md` lists every shipped asset as `final`; any `*-default.*` file still referenced by the build, metadata, or UI is a blocking `FAIL`.
- Final favicon exists and is wired into the production application/build.
- App/product icon exists where the platform requires it.
- Final OG/social image exists and is exactly 1200×630 px.
- Public social metadata points to the final asset, not a local-only or placeholder path.

## 2. Payment / Monetization

If the product has no payment/monetization requirement, mark the area `N/A` with evidence from the brief/decisions.

Otherwise verify:

- user-selected provider is documented;
- provider may be RevenueCat, Stripe, MoonPay, or another approved gateway;
- production environment/configuration is separated correctly from test/sandbox;
- success/failure/cancel/retry flows have evidence;
- webhook/callback/idempotency controls are present when required;
- secrets are not committed to client code or documentation;
- relevant critical flow tests exist/run when practical.

Do not infer a working payment integration merely from an installed SDK.

## 3. SEO & Social Metadata

For public/indexable products verify as applicable:

- meaningful page title;
- meta description;
- semantic heading hierarchy (`h1`, then logical `h2`/`h3` structure);
- one primary `h1` per page unless the framework/content structure has a justified alternative;
- meaningful `alt` text on content images;
- decorative images are handled accessibly;
- canonical URL where required;
- sitemap where required;
- robots directives/file where required;
- Open Graph metadata;
- social card metadata where relevant;
- final `og:image` resolves to the final 1200×630 asset;
- structured data is used only when it truthfully matches page content.

For authenticated/internal-only applications, mark non-applicable SEO items `N/A` with reason; accessibility and semantic markup still apply.

## 4. W3C & Accessibility

Target: practical compliance with W3C standards and WCAG 2.2 AA essentials.

Verify or seek evidence for:

- valid/appropriate HTML semantics;
- keyboard navigation through critical flows;
- visible focus indication;
- correct focus management for dialogs/routes/dynamic UI where relevant;
- form labels;
- accessible error association/messages;
- color contrast;
- text scaling/reflow where relevant;
- accessible names for buttons/controls/icons;
- correct landmark/navigation semantics;
- screen-reader smoke test for critical flows;
- no known blocking WCAG 2.2 AA issue.

Automated audits are useful evidence but do not replace manual keyboard/screen-reader checks.

If W3C validation or runtime accessibility testing cannot be executed, mark those checks `UNVERIFIED`, not PASS.

## 5. Final Humanization / AI Artifact Check

Inspect production-facing copy and UI for:

- unnecessary em dashes used as a repetitive generated-writing tic;
- generic AI-generated filler or templated phrasing;
- model names, prompt text, hidden generation notes, or debug explanations exposed to users;
- TODO/FIXME/placeholder copy;
- lorem ipsum/sample data exposed in production unintentionally;
- generic gradient/card/hero patterns used without relation to the project's approved design system;
- bootstrap/default logos, favicons, or social images still in production.

The goal is not to ban punctuation or visual patterns. Flag them only when they are gratuitous, repetitive, placeholder-like, or inconsistent with the approved brand/design.

## 6. Engineering Release Gate

Verify evidence for:

- type check where applicable;
- lint where applicable;
- unit/integration tests appropriate to risk;
- E2E for critical flows such as login, payment, and core product flow;
- production build success;
- permissions/security review relevant to the stack;
- secret exposure check;
- feature status synchronized with actual implementation;
- changelog updated;
- HANDOFF updated;
- `docs/09-release-readiness.md` updated with reviewer/evidence;
- `docs/ui/README.md` screen statuses match the implemented screens.

## 7. Status rules

Use `PASS` only with evidence.

Use `FAIL` when the requirement applies and is demonstrably unsatisfied.

Use `N/A` only when the requirement truly does not apply and the reason is supported.

Use `UNVERIFIED` when the requirement applies or may apply but available evidence is insufficient.

Overall:

- any blocking FAIL => `NOT READY`;
- no blocking FAIL but critical UNVERIFIED items => `NOT VERIFIED`;
- all applicable blocking checks evidenced as PASS => `READY`.
