# Gaply Engineering Playbook

> **خلاصه کوتاه:** هر پروژه باید طوری ساخته شود که یک انسان جدید یا یک AI جدید بتواند فقط با خواندن Documentation — بدون وابستگی به نفر قبلی — بفهمد محصول چیست، چه چیزی ساخته شده، چرا این تصمیم‌ها گرفته شده و قدم بعدی دقیقاً چیست.

English guide: [Gaply-Engineering-Playbook.md](Gaply-Engineering-Playbook.md)

## این سند برای چیست؟

هدف:

- توسعه سریع محصولات با کمک AI
- جلوگیری از وابستگی پروژه به یک فرد
- تحویل آسان پروژه به Developer جدید
- ایجاد Source of Truth مشترک برای انسان و AI
- معماری قابل رشد از Web به Mobile
- کاهش خطاهای ناشی از تغییر بدون مستندات

**مخاطبان:** Developer، Product Manager، Designer، CTO و AI Coding Agentها (Claude Code، Codex و مشابه).

**دامنه:** تمام پروژه‌های گپلی — Web App، PWA، اپلیکیشن موبایل، Backend و API، پروژه‌های جدید و پروژه‌های قدیمی تحت نگه‌داری گپلی.

این Playbook به‌تنهایی کامل است. Agent Skill با نام `gaply-engineering-playbook` آن را خودکار می‌کند، اما هیچ‌چیز در این سند به آن Skill وابسته نیست: تیمی که فقط همین فایل را بخواند، به همان استاندارد می‌رسد.

---

## شروع سریع — کجای سند را بخوانم؟

| وضعیت شما | مسیر |
| --- | --- |
| Developer جدید هستم و پروژه را تحویل می‌گیرم | بخش 4 + Prompt B |
| پروژه جدید شروع می‌کنم | بخش 5 + Prompt A |
| روی یک Feature کار می‌کنم | بخش 5 و 6 + Prompt C |
| UI پروژه را طراحی می‌کنم | بخش 8 و 9 + Prompt E |
| پروژه قدیمی را استاندارد می‌کنم | بخش 15 + Prompt D |
| برای Release آماده می‌شوم | بخش 10 و 16 |

---

# 1. اصول غیرقابل مذاکره

## 1.1 پروژه به هیچ فردی وابسته نیست

در هر لحظه باید بتوان پروژه را از Developer A به Developer B منتقل کرد، بدون جلسه توضیح چندساعته. نفر بعدی فقط با خواندن مستندات باید بفهمد: محصول چیست، چرا ساخته می‌شود، چه چیزی تمام شده، چه چیزی در جریان است و قدم بعدی چیست.

## 1.2 Documentation بخشی از Development است

یک Feature زمانی **Done** است که:

- کد آن کامل شده باشد
- تست‌های لازم اجرا و پاس شده باشند
- Feature Document به‌روز شده باشد
- Feature Status تغییر کرده باشد
- `HANDOFF.md` آپدیت شده باشد
- تصمیم مهم جدید (اگر بود) در Decision Log ثبت شده باشد

**کدی که Documentation آن قدیمی است، از نظر استاندارد گپلی کامل نیست.**

## 1.3 AI عضو اجرایی تیم است، نه Source of Truth

AI می‌تواند کد بنویسد، معماری پیشنهاد دهد، تست و مستند تولید کند، Refactor کند و پروژه را تحلیل کند. اما:

- Requirement جدید اختراع نمی‌کند
- تصمیم بیزینسی خودسرانه نمی‌گیرد
- خارج از Scope تعریف‌شده تغییری ایجاد نمی‌کند

اگر ابهام وجود داشت:

1. سوال را در `docs/05-open-questions.md` ثبت می‌کند
2. از Developer / Product Owner می‌پرسد
3. پاسخ را در فایل مربوطه ثبت می‌کند و بعد ادامه می‌دهد

## 1.4 معماری Over-engineered نباشد

Clean Architecture اصل راهنماست، نه Ritual. برای یک Prototype دو روزه، ۱۲ لایه و ۴۰ Interface نمی‌سازیم.

معیار:

> کمترین معماری‌ای که تغییر، تست، انتقال مالکیت و رشد محصول را امن نگه دارد.

---

# 2. ساختار استاندارد Documentation

هر پروژه باید این ساختار را داشته باشد:

```text
HANDOFF.md                    ← در ریشه پروژه

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
│   ├── F001-authentication.md
│   └── F002-dashboard.md
├── ui/                       ← خروجی طراحی (بخش 8)
│   ├── README.md
│   ├── masterdoc.html
│   └── pages/  or  desktop/ + mobile/
└── assets/                   ← Assetهای برند (بخش 9)
    ├── README.md
    ├── logo.*
    ├── banner.*
    ├── favicon/
    └── og.png
```

## 2.1 هر فایل چه چیزی دارد؟

| فایل | محتوا |
| --- | --- |
| **HANDOFF.md** | وضعیت لحظه‌ای پروژه: Feature فعال، Task جاری، آخرین کار، قدم بعدی، Blockerها |
| **docs-manifest.md** | چک‌لیست وجود و وضعیت فایل‌های Documentation |
| **00-product-brief.md** | خلاصه انسانی محصول: چیست، چه مشکلی حل می‌کند، کاربر کیست، Core Flow، Scope و Out of Scope |
| **01-architecture.md** | نقشه معماری: Frontend/Backend Stack، Database، Auth، Storage، Folder Structure، Security Boundary، Deployment، Mobile Readiness |
| **02-ai-context.md** | قوانین کار AI روی این پروژه: قوانین Coding، محدودیت Scope، Dependency Policy، موارد ممنوع |
| **03-project-memory.md** | Contextهایی که در کد دیده نمی‌شوند: محدودیت‌های Client، دلایل انتخاب‌ها، اولویت‌ها |
| **04-decisions.md** | تصمیمات معماری و محصول (ADR) — Append-only |
| **05-open-questions.md** | ابهامات باز: سوال، Feature مرتبط، Owner، وضعیت، Blocking یا نه |
| **06-changelog.md** | تغییرات مهم Product / Architecture / Feature Behavior (جایگزین Git History نیست) |
| **07-feature-status.md** | جدول وضعیت تمام Featureها |
| **08-tech-stack.md** | ابزارها، نسخه‌ها، دلیل انتخاب، جایگزین‌ها |
| **09-release-readiness.md** | دروازه Release: هویت و برند، پرداخت، SEO و کشف‌پذیری، Accessibility، انسانی‌سازی، مهندسی |
| **features/Fxxx-name.md** | مستند کامل هر Feature (بخش 2.3) |
| **ui/** | خروجی طراحی: پکیج Claude Design، یا لینک طراحی به‌همراه اسکرین‌شات‌ها (بخش 8) |
| **assets/** | Assetهای برند: Logo، Banner، Favicon یا ست آیکون اپ، تصویر OG (بخش 9) |

## 2.2 HANDOFF.md — مهم‌ترین فایل عملیاتی

بعد از هر جلسه کاری معنادار آپدیت می‌شود:

```markdown
# HANDOFF

## Current Phase
MVP — Sprint 3

## Active Feature
F003 — Document Analysis (IN_PROGRESS)

## Current Task
Implement upload validation

## Last Completed
Upload UI + storage adapter

## Next Step
Add tests and update feature documentation

## Read First
- docs/features/F003-document-analysis.md
- docs/04-decisions.md (ADR-009)

## Blockers
- Q-014: coverage reference unclear
```

## 2.3 Template مستند Feature

هر Feature یک فایل مستقل دارد: `docs/features/F001-authentication.md`

```markdown
# F001 — Authentication

## Status
PLANNED | READY | IN_PROGRESS | BLOCKED | DONE | DEFERRED | CANCELLED

## Goal
## User & User Flow
## Business Rules
## Functional Requirements
## UX States (Loading / Empty / Success / Error / Offline)
## Validation & Permissions
## API / Service Contract
## Dependencies
## Edge Cases
## Security Considerations
## Acceptance Criteria
- [ ] ...
## Tests (Unit / Integration / E2E)
## Notes
```

**قانون مهم:** Feature Document همیشه **رفتار فعلی مورد انتظار** را نشان می‌دهد. اگر Requirement تغییر کرد، خود متن اصلاح می‌شود، نه اینکه فقط یک Note به انتها اضافه شود. دلیل تغییر در Decision Log و تاریخ آن در Changelog ثبت می‌شود.

Featureای که از روی Brief ساخته شده `PLANNED` است، حتی وقتی سوال‌های باز بخش‌هایی از آن را متوقف کرده باشند؛ در این حالت شناسه سوال‌های Blocking ذکر می‌شود. `BLOCKED` یعنی کار شروع شده و نمی‌تواند ادامه پیدا کند.

## 2.4 Template تصمیم (ADR)

```markdown
## ADR-012 — Authentication
Date: 2026-09-03
Decision: Email OTP is the default authentication method.
Reason: The client does not currently have an SMS gateway.
Impact: Auth UI and Supabase configuration.
Status: Active
```

تصمیمات حذف نمی‌شوند. اگر تصمیم عوض شد، ADR جدید ثبت می‌شود که قبلی را Supersede می‌کند.

## 2.5 Template سوال باز

```markdown
## Q-014
Feature: Insurance Analysis
Question: What is the canonical coverage reference?
Owner: Product
Status: OPEN
Blocking: YES
```

اگر سوال برای رفتار اصلی Feature تعیین‌کننده است (`Blocking: YES`)، توسعه آن Feature متوقف می‌ماند تا پاسخ مشخص شود.

---

# 3. Source of Truth — در تناقض، کدام مرجع است؟

| موضوع | مرجع |
| --- | --- |
| رفتار مورد انتظار محصول | Feature Document |
| خلاصه محصول | Product Brief |
| معماری | Architecture Document |
| دلیل تصمیم‌ها | Decision Log |
| وضعیت توسعه | Feature Status |
| وضعیت واقعی پیاده‌سازی | Code + Tests |

اگر Code با Feature Document فرق دارد، این یک **Gap** است: باید گزارش شود و انسان تصمیم بگیرد کدام طرف اصلاح شود. **AI حق ندارد خودسرانه یکی را انتخاب کند.**

---

# 4. ورود Developer جدید

ترتیب مطالعه:

1. `HANDOFF.md`
2. `docs/00-product-brief.md`
3. `docs/07-feature-status.md`
4. `docs/01-architecture.md`
5. `docs/04-decisions.md`
6. Feature Document فعال (`IN_PROGRESS`)
7. Code و Testهای مرتبط

بعد از مطالعه، با **Prompt B** از AI بخواهد محصول را خلاصه کند، وضعیت فعلی را توضیح دهد و Task بعدی را مشخص کند — بدون تغییر کد.

---

# 5. چرخه توسعه Feature

## Definition of Ready — قبل از شروع

Feature وقتی آماده توسعه است که:

- Goal و User مشخص باشد
- User Flow مشخص باشد
- Requirementهای اصلی مشخص باشند
- Acceptance Criteria داشته باشد
- سوال Blocker باز نداشته باشد
- Dependencyهای اصلی مشخص باشند

## شش مرحله توسعه

### مرحله 1 — Understand

AI (یا Developer) قبل از هر کاری می‌خواند: Product Brief، Architecture، Feature Document، Decisions، Open Questions.

### مرحله 2 — Plan

قبل از کدنویسی ارائه می‌شود:

- چه فایل‌هایی تغییر می‌کنند؟
- چه Dependencyهایی درگیرند؟
- چه Riskهایی وجود دارد؟
- چه تست‌هایی لازم است؟
- چه Documentationهایی باید آپدیت شوند؟

### مرحله 3 — Implement

کدنویسی با رعایت Scope (بخش 6). هر Feature تا جای ممکن داخل پوشه و محدوده خودش می‌ماند.

### مرحله 4 — Verify

اجباری:

- Type Check
- Lint
- Unit Test
- Integration Test در صورت نیاز
- E2E برای Flowهای Critical (Login، Payment، Core Flow)

### مرحله 5 — Sync Documentation

آپدیت: Feature Document، Feature Status، Changelog، `HANDOFF.md`

### مرحله 6 — Git

قبل از Commit: بررسی Diff، اجرای تست، بررسی Sync بودن Documentation.

## Definition of Done — چک‌لیست پایان

- [ ] Implementation کامل است
- [ ] Acceptance Criteria پاس شده
- [ ] Error / Loading / Empty State بررسی شده
- [ ] Permission و Securityهای مرتبط بررسی شده
- [ ] تست‌های مورد نیاز اجرا و پاس شده
- [ ] Regressionهای مهم بررسی شده
- [ ] Build موفق است
- [ ] Documentation به‌روز شده
- [ ] Feature Status = DONE
- [ ] `HANDOFF.md` آپدیت شده

---

# 6. کنترل Scope و قوانین کار با AI

## 6.1 هر Task باید Scope داشته باشد

مثال — Task: «Login OTP»

Allowed:

```text
features/auth/*
services/auth/*
tests/auth/*
docs/features/F001-authentication.md
```

AI اجازه ندارد Payment، Dashboard یا Database را تغییر دهد — مگر با دلیل مشخص و تایید انسان. اگر تغییر خارج از Scope لازم شد: **AI متوقف می‌شود، دلیل ارائه می‌کند و منتظر تایید می‌ماند.**

## 6.2 Dependency Impact Check

قبل از تغییر Shared Logic (مثل Auth، Storage، Types مشترک)، باید مشخص شود چه Featureهایی متاثر می‌شوند. برای تغییرات غیرساده، AI قبل از Coding یک Impact Summary ارائه می‌کند.

## 6.3 انتخاب مدل AI

| نوع Task | مدل |
| --- | --- |
| Architecture، Refactor بزرگ، Security، Migration، Multi-file Change | مدل قوی‌تر با Reasoning بالا |
| Rename، Formatting، تست تکراری، Cleanup مستندات | مدل سریع‌تر |

اصل: هزینه چند بار اجرای اشتباه AI معمولاً بیشتر از یک اجرای دقیق با مدل قوی است.

## 6.4 ساختار Prompt برای Task غیرساده

```text
Context / Goal / Scope / Constraints /
Files to inspect / Expected output /
Verification / Documentation update
```

قاعده کلی برای تغییرات بزرگ:

**Inspect → Plan → Impact → Implement → Verify → Document**

نه: Prompt → Generate Lots of Code → Hope

## 6.5 AI Context Optimization

هدف: کاهش Token مصرفی، افزایش دقت، جلوگیری از خواندن کل Repository.

راهکارها: Documentation دقیق، Feature Isolation، Repository Indexing و ابزارهای Code Intelligence. این ابزارها **مکمل** Documentation هستند، نه جایگزین آن.

---

# 7. استاندارد Frontend

## 7.1 پروژه Web-only

اگر محصول فقط در Browser استفاده می‌شود و Native App در Roadmap ندارد:

**React + TypeScript + Next.js**

دلایل: SSR/SSG، SEO، Routing استاندارد، اکوسیستم بالغ، Deploy ساده.

## 7.2 پروژه‌ای که احتمال Mobile دارد

معماری از روز اول باید Mobile-ready باشد. الزامات:

- Business Logic مستقل از UI
- API Layer مستقل
- Schema و Validation مستقل
- Storage Adapter (نه دسترسی مستقیم به `localStorage`)
- عدم استفاده از Browser API در Domain Logic
- Localization آماده

قانون طلایی:

```text
Bad:   feature logic → window.localStorage / document / router
Good:  feature logic → Storage interface
       Web adapter    → localStorage
       Mobile adapter → SecureStore / AsyncStorage
```

## 7.3 Stack پیشنهادی

- React + TypeScript
- Vite یا Next.js — بر اساس نوع محصول (Next.js برای SEO/SSR، Vite برای App/PWA)
- TanStack Router / TanStack Query
- Zustand
- React Hook Form + Zod
- Tailwind CSS + Motion
- i18next
- Vitest + React Testing Library + Playwright
- Sentry

برای PWA اضافه می‌شود: Dexie + IndexedDB، `vite-plugin-pwa`، Workbox

این Stack **پیش‌فرض** است، نه قانون غیرقابل تغییر. تغییر آن باید در `docs/08-tech-stack.md` و Decision Log ثبت شود.

## 7.4 مالکیت State

| نوع State | ابزار پیشنهادی |
| --- | --- |
| Server State (API/Database) | TanStack Query |
| UI / Client State | React State، Zustand در صورت نیاز |
| Form State | React Hook Form |
| Validation | Zod |

---

# 8. استاندارد طراحی UI و Prototype

## 8.1 جایگاه طراحی در پروسه پروژه

مسیر رسیدن به طراحی همیشه یکی است — فرقی نمی‌کند پروژه از قبل Documentation داشته باشد یا نه:

1. Documentation استاندارد ساخته یا به‌روز می‌شود (پروژه جدید → Prompt A، پروژه موجود → Prompt D)
2. بر اساس همان Documentation، UI طراحی می‌شود (Prompt E)
3. توسعه Featureها طبق بخش 5 شروع می‌شود

قواعد:

- **اول Documentation، بعد Design.** Prototype از روی Product Brief و Feature Documentها ساخته می‌شود، نه از روی حدس.
- اگر پروژه از قبل طراحی معتبر دارد (Figma، Adobe XD یا محصولِ در حال کار)، فاز ساخت Prototype **حذف می‌شود** و فقط قوانین آرشیو (بخش 8.5) اجرا می‌شود.

## 8.2 راه‌اندازی پروژه Claude Design

کار از یک **پروژه خالی و بدون Design System از پیش‌آماده** شروع می‌شود. یک Design System آماده باعث می‌شود صفحه‌ها پیش از آنکه کسی تصمیم گرفته باشد محصول چه شکلی است، تمام‌شده به نظر برسند؛ و بعد هر صفحه جدید همان پیش‌فرض‌های تصادفی را به ارث می‌برد.

فایل **`masterdoc.html` در ریشه پروژه طراحی** ساخته می‌شود و این‌ها را نگه می‌دارد:

- معرفی محصول: چیست، کاربرش کیست، Core Flow چیست
- Design System کامل: رنگ‌ها و توکن‌ها، مقیاس Typography، مقیاس Spacing، Componentها به‌همراه Stateهایشان، قواعد Layout و Grid، Elevation، Radius، Motion، تم Light و Dark، و قواعد RTL/LTR وقتی محصول چندزبانه است
- ورودی Prototype: دکمه‌ای که پیش‌نمایش اپلیکیشن را باز می‌کند، یا دو دکمه وقتی Desktop و Mobile پیش‌نمایش جدا دارند

## 8.3 ساختار فایل‌ها

| دامنه پروژه | ساختار |
| --- | --- |
| فقط Web یا Desktop | `masterdoc.html` + `pages/` |
| Desktop و Mobile | `masterdoc.html` + `desktop/` + `mobile/` |
| فقط Mobile | `masterdoc.html` + `pages/` |

## 8.4 قوانینی که هر صفحه رعایت می‌کند

این جمله باید داخل خودِ هر صفحه نوشته شود، تا اگر صفحه به‌تنهایی باز شد، قانون هم با آن بیاید:

> `masterdoc.html` تنها Source of Truth طراحی و پیاده‌سازی است. از همان Design System تعریف‌شده در آن استفاده کن.

- هیچ صفحه‌ای رنگ، مقیاس Typography، Spacing یا Component مخصوص خودش تعریف نمی‌کند. اگر صفحه‌ای به چیزی نیاز دارد که Design System ندارد، اول آن چیز به `masterdoc.html` اضافه می‌شود.
- هیچ صفحه‌ای استایل ناسازگار با `masterdoc.html` وارد نمی‌کند.
- Dark Mode همیشه هست، مگر پروژه صریحاً خلافش را گفته باشد.
- بدون Backend، Database یا اتصال واقعی به سرویس‌ها. همه‌چیز Mock است.
- صفحه‌ها از **Mock Data واقع‌گرایانه** استفاده می‌کنند، نه Lorem Ipsum و نه `Item 1, Item 2`. اسم‌ها، مبلغ‌ها، تاریخ‌ها و متن‌ها باید شبیه محصول واقعی باشند تا مشکلات Layout در Prototype بیرون بزنند، نه در Production.
- صفحه‌ها **اینتراکتیو** هستند تا کل Flow کلیک‌به‌کلیک قابل تست باشد: Navigation، فرم‌ها با Validation، Modal، Dropdown، Tab و مجموعه کامل UX Stateها یعنی Empty، Loading، Success، Validation Error، Server Error و Permission Error. صفحه‌ای که فقط شبیه یک اسکرین‌شات ثابت است، خروجی قابل قبولی نیست.

## 8.5 آرشیو خروجی طراحی

هر چیزی که فاز طراحی تولید کرده، داخل Repository و در `docs/ui/` می‌ماند.

| ابزار طراحی | چه چیزی در `docs/ui/` قرار می‌گیرد |
| --- | --- |
| Claude Design | پکیج کامل: `masterdoc.html` به‌همراه `pages/`، یا `desktop/` و `mobile/` |
| Figma / Adobe XD | لینک طراحی ثبت‌شده در `docs/ui/README.md` به‌همراه اسکرین‌شات صفحات کلیدی |
| محصول موجود | اسکرین‌شات صفحات کلیدی به‌همراه یادداشتی که می‌گوید خود محصول مرجع است |

برای Figma یا Adobe XD لینک به‌تنهایی کافی نیست: با تغییر دسترسی، Repository نباید کور بماند.

`docs/ui/README.md` همیشه این‌ها را ثبت می‌کند: منبع طراحی و وضعیت آن، فهرست صفحات با یک وضعیت برای هر صفحه (`pending design`، `designed`، `implemented`)، و اشاره‌ای به Flowها. صفحه‌هایی که در Brief آمده‌اند ولی هنوز طراحی نشده‌اند، به‌جای حذف شدن با وضعیت `pending design` فهرست می‌شوند.

## 8.6 Context Pack برای Claude Design

فقط چیزی فرستاده می‌شود که درک محصول و تصمیم‌های UI را تغییر می‌دهد. مستندات فنی‌ای که روی چیزی که کاربر می‌بیند اثر ندارند، Context را مصرف می‌کنند و طراحی را به سمت جزئیات پیاده‌سازی می‌کشند.

پکیج پیش‌فرض:

```text
docs/assets/logo.png          (or the project's actual logo file)
docs/00-product-brief.md
docs/02-ai-context.md
docs/07-feature-status.md
docs/features/
brief.md                      (when it carries brand direction, audience, or positioning)
```

اگر دور قبلی طراحی چیزی تولید کرده که ادامه دادن از رویش ارزش دارد، `docs/ui/` هم اضافه می‌شود.

`docs/01-architecture.md` در پکیج پیش‌فرض **نیست**. فقط وقتی فرستاده می‌شود که معماری برای کاربر قابل مشاهده باشد: ساختار Navigation، Permission و Roleها، جریان داده‌ای که تغییر می‌دهد یک صفحه چه چیزی می‌تواند نشان دهد، یا محدودیت پلتفرمی که طراحی را محدود می‌کند.

---

# 9. استاندارد Assetهای برند

## 9.1 یک محل واحد

`docs/assets/` تمام Assetهای برند پروژه را نگه می‌دارد. چهار نوع Asset ردیابی می‌شوند:

| نوع | کاربرد | شکل نهایی |
| --- | --- | --- |
| Logo | هویت محصول | `logo.svg` یا `logo.png` |
| Banner | سطوح بازاریابی و Repository | `banner.png` یا `banner.jpg` |
| Favicon / آیکون اپ | تب مرورگر، اپ نصب‌شده، Launcher | پوشه `favicon/` شامل ست تولیدشده |
| OG / تصویر شبکه اجتماعی | پیش‌نمایش لینک در شبکه‌های اجتماعی و چت | `og.png`، **دقیقاً 1200x630** |

## 9.2 Asset با الگو پیدا می‌شود، نه با یک مسیر دقیق

پروژه‌ای که از قبل Logo دارد تقریباً هیچ‌وقت آن را در مسیری که این Playbook انتخاب می‌کرد نگه نداشته است. گزارش «Asset وجود ندارد» در حالی که صاحب پروژه دارد به همان فایل نگاه می‌کند، اعتماد به کل گزارش را از بین می‌برد؛ بنابراین تشخیص بر اساس **نام فایل یا نام پوشه** انجام می‌شود:

| نوع | نام فایل شامل | نام پوشه |
| --- | --- | --- |
| Logo | `logo`، `logotype`، `logomark`، `wordmark`، `brandmark`، `brand` | `logo/`، `logos/`، `brand/`، `branding/` |
| Banner | `banner`، `hero`، `cover`، `header-image`، `masthead` | `banner/`، `banners/` |
| Favicon / آیکون اپ | `favicon`، `apple-touch-icon`، `android-chrome`، `mstile`، `safari-pinned-tab`، `site.webmanifest` | `favicon/`، `favicons/`، `icons/`، `app-icon/` |
| OG / شبکه اجتماعی | `og`، `opengraph`، `social`، `share`، `twitter-card`، `preview`، `card` | `og/`، `social/`، `opengraph/` |

جداکننده‌ها هم به حساب می‌آیند: `company-logo.png`، `logo_dark.svg` و `Logo.PNG` هر سه Match می‌شوند. یک پوشه کامل هم Match می‌شود و ست هفت‌فایلی Favicon که از یک Generator بیرون آمده، دقیقاً به همین شکل شناسایی می‌شود.

## 9.3 یکپارچه‌سازی، بدون شکستن Build

| Asset کجاست | چه اتفاقی می‌افتد |
| --- | --- |
| `docs/assets/` | هیچ؛ از قبل درست است |
| هر جای دیگری زیر `docs/` | **به `docs/assets/` منتقل می‌شود** و پوشه‌های ست دست‌نخورده می‌مانند، پس `docs/favicon/` می‌شود `docs/assets/favicon/` |
| `public/`، `static/`، `src/`، `app/`، `assets/`، `www/`، `resources/`، `web/` | **هرگز منتقل نمی‌شود.** Build یا سایتِ سرو‌شده به آن مسیر وابسته است. در Inventory با مسیر واقعی‌اش ارجاع داده می‌شود |

بعد از هر جابه‌جایی، هر لینک مستنداتی که به مسیر قبلی اشاره می‌کرد اصلاح می‌شود.

## 9.4 Placeholderها

وقتی برای یک نوع Asset هیچ فایلی وجود ندارد، یک Placeholder با برچسب روشن ساخته می‌شود تا ساختار کامل بماند و خلأ دیده شود:

- `logo-default.svg`
- `favicon-default.svg`
- `og-default.png` دقیقاً در اندازه 1200x630

پسوند `*-default.*` همان چیزی است که یک فایل را به‌عنوان Placeholder علامت می‌زند. Placeholder برای Banner وجود ندارد: نبودن Banner به‌جای اینکه ساخته شود، به‌عنوان Gap گزارش می‌شود. **هیچ Placeholderای به‌عنوان Asset نهایی برند معرفی نمی‌شود** و Releaseای که هنوز Placeholder در آن وصل است، از Release Gate رد نمی‌شود.

Assetهای نهایی هر نامی که پروژه از قبل استفاده می‌کند را نگه می‌دارند. اجباری برای تغییر نام یک `company-logo.png` سالم وجود ندارد.

## 9.5 Inventory

`docs/assets/README.md` برای هر Asset یک سطر دارد:

```text
File | Kind | Purpose | Status (placeholder | final) | Dimensions | Used in
```

Inventory آن Assetهایی را هم که عمداً داخل پوشه‌های اپلیکیشن باقی مانده‌اند پوشش می‌دهد؛ آن سطرها مسیر واقعی را حمل می‌کنند تا کسی دنبالشان در `docs/assets/` نگردد.

## 9.6 ابزارهای تولید

| Asset | ابزار پیش‌فرض |
| --- | --- |
| ست Favicon از روی یک تصویر منبع | https://favicon.io/favicon-converter/ |
| ست آیکون اپ موبایل | https://www.digia.tech/tools/app-icon-generator/ |

پروژه‌ای که آیکون‌ها را با Build Pipeline خودش تولید می‌کند، به‌جای این‌ها همان انتخاب را در `docs/04-decisions.md` ثبت می‌کند.

---

# 10. SEO، کشف‌پذیری و AI Discoverability

محصولی که پیدا نمی‌شود، Crawl نمی‌شود، پیش‌نمایش ندارد یا نصب نمی‌شود، هر کیفیتی هم که کدش داشته باشد ناتمام است. این موارد بخشی از Release Gate و چک‌لیست نهایی هستند.

## 10.1 فایل‌های ریشه سرو‌شده

این‌ها همان‌جایی بررسی می‌شوند که سایت آن‌ها را سرو می‌کند: ریشه Repository، `public/`، `static/`، `app/`، `src/app/`، `www/` یا خروجی Build. یک `site.webmanifest` که فقط در `docs/assets/favicon/` نشسته، Asset منبع است نه Manifest سرو‌شده؛ و همین تفاوت تعیین می‌کند این بررسی پاس می‌شود یا نه.

| فایل | برای | توضیح |
| --- | --- | --- |
| `robots.txt` | هر سایت سرو‌شده، حتی سایت‌های پشت Auth | محصول Authenticated هم به آن نیاز دارد، برای Disallow کردن |
| `sitemap.xml` | سایت‌های عمومی و Indexable | ممکن است زمان Build ساخته شود؛ خروجی Build یا Config همان Generator مدرک است |
| `llms.txt` | محصولاتی که می‌خواهند برای AI Agentها قابل استفاده باشند | قراردادی تازه‌تر: توصیه‌شده است، نه Blocking، مگر Brief آن را خواسته باشد |
| Web App Manifest | PWA و محصولات قابل نصب | `site.webmanifest`، `manifest.webmanifest` یا `manifest.json`؛ اندازه آیکون‌هایی که اعلام می‌کند باید واقعاً وجود داشته باشند |

## 10.2 Metadata در کد

| مورد | الزام |
| --- | --- |
| Page Title | معنادار و یکتا برای هر صفحه |
| Meta Description | روی صفحات Indexable وجود دارد |
| Canonical URL | هر جا احتمال URL تکراری هست |
| Open Graph | `og:title`، `og:description`، `og:image`، `og:url`، `og:type` |
| Twitter Cards | `twitter:card` و تگ‌هایی که نوع Card انتخاب‌شده لازم دارد |
| `og:image` | روی یک URL عمومی به Asset نهایی 1200x630 برسد، نه یک مسیر Local |
| Structured Data / Schema.org | فقط جایی که واقعاً با محتوای صفحه می‌خواند |
| سلسله‌مراتب Heading | یک `h1` اصلی در هر صفحه و `h2`/`h3` منطقی زیر آن |
| متن `alt` تصاویر | برای تصاویر محتوایی معنادار؛ تصاویر تزئینی به شکل Accessible مدیریت شوند |

## 10.3 بر اساس نوع پروژه

| نوع پروژه | چه چیزی اعمال می‌شود |
| --- | --- |
| Web App عمومی | همه موارد 10.1 و 10.2 |
| Web App پشت Auth | `robots.txt`، Headingها، متن `alt` و Manifest. موارد Indexing و شبکه‌های اجتماعی با ذکر دلیل `N/A` می‌شوند |
| اپلیکیشن موبایل | ست آیکون اپ و Metadata فروشگاه، جای Favicon و Sitemap را می‌گیرند |
| فقط Backend یا API | کل این بخش `N/A` است؛ مستندات API جای آن را می‌گیرد |
| CLI یا Library | هویت در README و Metadata پکیج زندگی می‌کند |

---

# 11. استاندارد Backend

## 11.1 انتخاب اول: Supabase

برای MVP، Prototype و Productionهای سبک تا متوسط:

**Supabase** — به دلایل: PostgreSQL، Auth، Storage، Realtime، RLS، Edge Functions، سرعت توسعه بالا و هزینه کمتر در مراحل اولیه.

اصل: **تا زمانی که نیاز فنی واقعی وجود ندارد، Backend اختصاصی نمی‌سازیم.**

## 11.2 چه زمانی Supabase کافی نیست؟

- پردازش CPU-intensive یا فایل سنگین
- Worker دائمی / Queue پیچیده / Long-running Job
- زیرساخت Blockchain / Custody / Signing
- نیازهای امنیتی یا Network خاص
- Integrationهای Legacy

گزینه‌های مجاز: Node.js، NestJS، Laravel، Django/FastAPI، Go — با دلیل فنی روشن.

**قانون:** قبل از ساخت Backend اختصاصی، این سوال باید در `docs/04-decisions.md` پاسخ داده شود:

> Supabase دقیقاً کدام Requirement را نمی‌تواند با کیفیت، امنیت یا هزینه قابل‌قبول پوشش دهد؟

مدل Hybrid (Supabase برای Auth/DB/Storage + سرویس اختصاصی فقط برای بخش خاص) اغلب از Full Custom Backend بهتر است.

## 11.3 قانون لایه‌بندی

```text
Forbidden:  UI component → supabase.from(...)

Correct:    UI component
              → feature service
              → repository
              → Supabase / API
```

- Business Writeهای حساس: ترجیحاً از طریق RPC / Postgres Function / Edge Function، تا Contract پایدار بماند
- Read ساده: از طریق Repository با رعایت RLS
- Direct Database Call از داخل UI Component: **ممنوع**

---

# 12. قواعد عمومی مهندسی

## 12.1 Feature Isolation

هر Feature پوشه مستقل خودش را دارد (Components، Services، Schemas، Types، Tests) تا Blast Radius تغییرات کوچک بماند:

```text
src/features/
  auth/
  dashboard/
  payment/
```

## 12.2 UX States — هیچ Feature فقط Happy Path نیست

حداقل حالات برای Featureهای User-facing: Loading، Success، Empty، Validation Error، Server Error، Network Error، Permission Error. برای PWA/Mobile: Offline و Retry هم اضافه می‌شود.

## 12.3 تست — متناسب با Risk

| سطح | برای |
| --- | --- |
| Unit | Validation، Domain Logic، Utility، Calculation |
| Integration | API، Database، Auth، Service Integration |
| E2E | Critical Flowها: Login، Checkout، Payment، Core Flow |

اصل: **تغییر بدون Verification تمام نشده است.** AI قبل از نوشتن تست جدید، تست‌های موجود را بررسی می‌کند.

## 12.4 Localization

اگر احتمال چندزبانه بودن هست: Text در Business Logic هاردکد نمی‌شود، Translation Key استفاده می‌شود، Date/Number/Currency باید Locale-aware باشد، و RTL/LTR از ابتدا در Design System دیده شود.

## 12.5 Dependency Policy

قبل از نصب Package جدید:

1. آیا پروژه همین قابلیت را دارد؟
2. آیا Native API کافی است؟
3. Package فعال و Maintain می‌شود؟
4. Bundle / Security Impact چیست؟
5. آیا با Mobile سازگار است (اگر لازم است)؟

Dependencyهای کلیدی در `docs/08-tech-stack.md` ثبت می‌شوند.

## 12.6 Secrets

هیچ Secret نباید: در Git کامیت شود، در Documentation ذخیره شود، داخل Prompt عمومی برود، یا داخل Client Bundle قرار گیرد (مگر Public Key طراحی‌شده برای Client). از Environment Variable و Secret Management استفاده شود.

---

# 13. Mobile Migration

هدف: تبدیل Web به Mobile **بازنویسی کامل نباشد.**

| قابل اشتراک | بازنویسی می‌شود |
| --- | --- |
| TypeScript، Domain Logic، Business Rules | UI |
| API Client، Query Logic | Routing |
| Schema، Validation، Shared Types | Storage Platform |
| Authentication Logic، i18n، Utilities | Native APIs |

پیشنهاد فعلی برای Native: **React Native / Expo**. در پروژه‌های بزرگ‌تر می‌توان Monorepo با Shared Core استفاده کرد.

---

# 14. Git و Review

## 14.1 Commit

Commitها Feature-oriented و کوچک:

```text
feat(auth): add email OTP flow
fix(onboarding): preserve progress after refresh
docs(auth): update Google login requirement
refactor(storage): introduce storage adapter
```

## 14.2 چک‌لیست Pull Request

- Requirement درست پیاده شده؟
- Scope ناخواسته اضافه نشده؟
- Dependency جدید واقعاً لازم بوده؟
- Error Stateها وجود دارند؟
- Tests و Build پاس هستند؟
- Documentation و Feature Status سینک شده؟
- Impact روی Shared Dependencyها بررسی شده؟

## 14.3 Review Triggerها — چه چیزی بدون هماهنگی تغییر نمی‌کند؟

**نیاز به تایید CTO / Technical Lead:** تغییر Backend Stack یا Database، ساخت Backend اختصاصی، Payment/Auth Architecture، Blockchain Custody، Large Refactor، Breaking API Change، هزینه زیرساختی بزرگ.

**نیاز به تایید Product Owner:** تغییر User Flow، حذف/اضافه شدن Step، تغییر Business Rule، Permission، Pricing، Data Retention یا هر رفتار User-visible.

**نیاز به هماهنگی Design:** تغییر Navigation، Onboarding، Checkout، Dashboard Hierarchy، Empty/Error States، Design System.

Developer یا AI نباید صرفاً چون پیاده‌سازی ساده‌تر است، Experience محصول را تغییر دهد.

---

# 15. پروژه‌های قدیمی

مهم‌ترین قانون:

**Big Bang Rewrite ممنوع است.** هدف اول Visibility و Documentation است، نه بازنویسی.

مراحل:

1. **Branch / Backup** — قبل از هر تغییر
2. **AI Inventory** — AI فقط Repository را تحلیل می‌کند (Stack، Features، Auth، Tests، Risks) بدون تغییر کد
3. **Generate `docs/`** — ساخت ساختار استاندارد Documentation از روی کد موجود
4. **Human Review** — Developer حداقل Product Brief، Architecture و Feature Status را بررسی می‌کند
5. **Gap Detection** — گزارش تفاوت بین Code، Docs و رفتار مورد انتظار
6. **No Forced Refactor** — Refactor فقط هنگام تغییر Feature، رفع Risk، Testability، Security یا Mobile-readiness — با دلیل ثبت‌شده

---

# 16. آمادگی Release و چک‌لیست نهایی

## 16.1 Release Gate

`docs/09-release-readiness.md` شش حوزه را نگه می‌دارد: هویت و برند؛ پرداخت و درآمدزایی؛ SEO و کشف‌پذیری؛ W3C و Accessibility؛ انسانی‌سازی نهایی و بررسی آثار AI؛ و دروازه مهندسی.

هر سطر یک Status و یک فیلد Evidence دارد. سطرها با وضعیت `PENDING` و Evidence خالی ساخته می‌شوند و فقط وقتی کسی مدرک واقعی در دست داشته باشد به `PASS`، `FAIL` یا `N/A` می‌روند. **هیچ سطری به این دلیل که کارش برنامه‌ریزی شده `PASS` نمی‌شود.**

بررسی انسانی‌سازی دنبال چیزهایی می‌گردد که لو می‌دهند خروجی تولیدشده بدون بازبینی به Production رفته است: Em Dashهای بی‌مورد که به یک تیک عادتی تبدیل شده‌اند، جمله‌های پرکننده و کلیشه‌ای، متن مدل یا Prompt که به کاربر نشان داده می‌شود، متن TODO و Placeholder، Lorem Ipsum، داده نمونه، و Layoutهای عمومی‌ای که ربطی به Design System تاییدشده ندارند.

## 16.2 چک‌لیست نهایی

هر گزارش پروژه — چه یک Check باشد، چه Initialization، چه Release Audit — با یک چک‌لیست فشرده تمام می‌شود و بعد از آن چیزی نمی‌آید. جزئیات در بخش‌های بالاتر می‌ماند؛ چک‌لیست برای این است که خواننده‌ای که تا انتها Scroll می‌کند، وضعیت پروژه را در یک صفحه ببیند.

نشانه‌ها:

| نشانه | معنا |
| --- | --- |
| `[x]` | هست و درست است |
| `[~]` | هست ولی ناقص، Placeholder یا وصل‌نشده |
| `[ ]` | نیست |
| `[-]` | موضوعیت ندارد، با ذکر دلیل در همان خط |

گروه‌ها، به ترتیب: Documentation؛ Assetهای برند؛ UI و طراحی؛ کشف‌پذیری و Crawling؛ Metadata و شبکه‌های اجتماعی؛ پلتفرم و PWA؛ مهندسی؛ و در آخر نتیجه کلی به‌عنوان آخرین خط.

نمونه:

```text
## Final Checklist

Documentation
[x] GEP structure — 18/18 required paths
[~] docs/ui/README.md — screens listed, no design export
[ ] docs/06-changelog.md — no entries since the first release

Brand assets
[x] Logo — docs/assets/logo.png
[~] Favicon — set in docs/assets/favicon/, not referenced by the app
[ ] Banner — no file matching a banner pattern
[~] OG image — og-default.png 1200x630, placeholder

Discovery and crawling
[ ] robots.txt
[ ] sitemap.xml
[ ] llms.txt
[-] Structured data — no public content pages

**Result:** NOT READY
```

**`[~]` هیچ‌وقت به `[x]` گرد نمی‌شود.** فاصله بین این دو، دقیقاً همان چیزی است که جلوی Release را می‌گیرد.

---

# 17. Promptهای آماده

## Prompt A — شروع پروژه جدید

```text
We are starting this project under the Gaply Engineering Standard.

Before writing application code:
1. Read the client requirements.
2. Identify missing or ambiguous requirements → docs/05-open-questions.md.
3. Create a concise docs/00-product-brief.md.
4. Propose the architecture in docs/01-architecture.md.
5. Break the project into feature documents under docs/features/.
6. Create docs/07-feature-status.md and docs/02-ai-context.md.
7. Create docs/09-release-readiness.md with every row PENDING.
8. Create HANDOFF.md.

Do not invent missing business requirements.

Default technical preferences:
- React + TypeScript. Next.js for SEO/SSR products, Vite for app-like products.
- Mobile-ready architecture if native apps are likely.
- Supabase as the default backend unless there is a documented reason not to.
- No direct Supabase access from UI components.
- Keep business logic independent from UI. Use service/repository boundaries.
- Consider localisation from the start where applicable.
- Add tests appropriate to the risk level.

Before implementation, provide: product summary, open questions,
proposed architecture, feature list, major risks. Then wait for approval.
```

## Prompt B — تحویل گرفتن پروژه موجود

```text
I am taking over this project (Gaply Engineering Standard).

Read in this order:
1. HANDOFF.md
2. docs/00-product-brief.md
3. docs/07-feature-status.md
4. docs/01-architecture.md
5. docs/04-decisions.md
6. the feature document currently marked IN_PROGRESS
7. related code and tests

Then tell me: what the product does, what is complete, what is in
progress, what is blocked, and the next logical task with the files involved.

Do not change code yet. After I approve the plan: implement, run tests,
update documentation, feature status and HANDOFF.md.
```

## Prompt C — توسعه یک Feature

```text
Task: <feature/task name>

Scope (allowed paths):
<list allowed folders/files>

Read first:
- docs/00-product-brief.md
- docs/01-architecture.md
- docs/features/<feature-doc>.md
- docs/04-decisions.md

Before coding, provide: implementation plan, files to change,
dependencies and impacted features, risks, tests needed.

Do not change anything outside the scope. If an out-of-scope change
seems required, stop and explain why.

After approval and implementation:
1. Run type check, lint and tests.
2. Update the feature document.
3. Update changelog and feature status.
4. Update HANDOFF.md.
```

## Prompt D — استانداردسازی پروژه قدیمی

```text
We are adopting the Gaply Engineering Standard for this existing project.
Do not change application code yet.

First inspect the repository and understand: product purpose, architecture,
frontend/backend stack, database, authentication, external services,
existing features, tests, deployment, major technical risks.

Then create or update:

docs/
  00-product-brief.md
  01-architecture.md
  02-ai-context.md
  03-project-memory.md
  04-decisions.md
  05-open-questions.md
  06-changelog.md
  07-feature-status.md
  08-tech-stack.md
  09-release-readiness.md
  features/
  ui/README.md
  assets/README.md
HANDOFF.md

Rules:
- Do not invent product requirements.
- Mark uncertain items clearly and put them in open-questions.
- Build feature documents from the actual code.
- Identify discrepancies between code and documentation.
- Detect existing brand assets by name pattern, not by one exact path,
  and consolidate them into docs/assets/ unless the application serves them.
- Do not refactor during this step.

At the end provide: repository summary, documentation created, unknowns,
risks, recommended next actions, and a final checklist. Wait for human
approval before any refactoring.
```

## Prompt E — طراحی UI با Claude Design

```text
We are designing the UI for this project with Claude Design, under the
Gaply Engineering Standard.

Context pack:
- docs/assets/logo.png (or the project's actual logo)
- docs/00-product-brief.md
- docs/02-ai-context.md
- docs/07-feature-status.md
- docs/features/
- brief.md, if it carries brand direction, audience or positioning
Send docs/01-architecture.md only if the architecture is visible to the
user: navigation, permissions, data flow that changes what a screen shows.

Rules:
- Start from a blank project with no preset design system.
- Create masterdoc.html at the root of the design project. It holds the
  product overview and the complete design system: colours and tokens,
  typography, spacing, components and their states, layout rules,
  light and dark themes.
- masterdoc.html contains a button that opens the application preview.
  If desktop and mobile are separate previews, it contains two buttons.
- File structure: web or desktop only → masterdoc.html + pages/;
  desktop and mobile → masterdoc.html + desktop/ + mobile/;
  mobile only → masterdoc.html + pages/.
- Every page states that masterdoc.html is the only source of truth for
  design and implementation, and uses only the design system defined there.
- No page defines its own colours, spacing, type scale or components, and
  no page introduces a style inconsistent with masterdoc.html.
- Include dark mode for all screens unless explicitly told otherwise.
- Fill every page with realistic mock data, not lorem ipsum.
- Every page is interactive: navigation, forms with validation, modals,
  dropdowns, tabs, and the full UX state set (empty, loading, success,
  validation error, server error, permission error).
- No real backend, database or extra infrastructure.
- Do not invent product requirements. Record anything unclear as an open
  question instead of guessing.

The final package is stored at docs/ui/ in the repository.
```

---

# 18. نگه‌داری این Playbook

استاندارد در چهار فایل زندگی می‌کند، و این چهار فایل یک سند واحدند که بر اساس زبان و مخاطب تقسیم شده است:

```text
Gaply-Engineering-Playbook.md      the standard, English
Gaply-Engineering-Playbook.fa.md   the standard, Persian
README.md                          using the skill, English
README.fa.md                       using the skill, Persian
```

**هیچ تغییری در Skill، قوانین، Workflow یا استانداردهای آن کامل نیست، تا وقتی هر چهار فایل بازبینی و در صورت لزوم به‌روز شده باشند.** قانونی که فقط در یکی از آن‌ها بنشیند، قانونی است که نیمی از تیم هیچ‌وقت نمی‌بیند؛ و فاصله گرفتن دو زبان از هم، همان مسیری است که یک استاندارد را بی‌صدا به دو استاندارد تبدیل می‌کند.

فایل‌های فارسی راهنمای موازی‌اند، نه ترجمه ماشینی: همان قوانین را با زبانی می‌گویند که یک خواننده فارسی‌زبان واقعاً به کار می‌برد.

---

# اصل نهایی گپلی

هدف گپلی بیشترین کد در کمترین زمان نیست.

هدف:

**بیشترین سرعت قابل‌اعتماد، با کمترین وابستگی به فرد، ابزار و تکنولوژی.**

یک پروژه خوب گپلی:

- سریع توسعه پیدا می‌کند
- برای نفر بعدی و برای AI قابل فهم است
- Documentation زنده دارد
- قابل تست و قابل تغییر است
- در صورت نیاز قابل مهاجرت به Mobile است
- بی‌دلیل Over-engineered نیست
- به هیچ فردی وابسته نیست
