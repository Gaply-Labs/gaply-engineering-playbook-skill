# اسکیل Gaply Engineering Playbook (GEP)

English guide: [README.md](README.md)

GEP یک Agent Skill است که به یک coding agent (Claude Code، Codex، ChatGPT، claude.ai) یک روش ثابت و مبتنی بر شواهد می‌دهد تا مستندات یک پروژهٔ نرم‌افزاری را از اولین `brief.md` تا ممیزی انتشار بسازد و نگه دارد. این skill آنچه در ریپو موجود است را می‌خواند، ساختار استاندارد `docs/` را از روی آن می‌سازد، هیچ نیازمندی‌ای از خودش اختراع نمی‌کند، و هر اجرا را با گزارشی تمام می‌کند که می‌گوید چه چیزی ساخته شد، چه چیزی هنوز کم است، و قدم بعدی چیست.

خودِ استاندارد به‌صورت کامل نوشته شده است، پس می‌توانید بدون استفاده از skill هم از آن پیروی کنید:

- [Gaply-Engineering-Playbook.md](Gaply-Engineering-Playbook.md) — استاندارد، انگلیسی
- [Gaply-Engineering-Playbook.fa.md](Gaply-Engineering-Playbook.fa.md) — استاندارد، فارسی

سه عمل دارد:

| عمل | چه کاری می‌کند | فایل تغییر می‌دهد؟ | کِی استفاده کنید |
| --- | --- | --- | --- |
| `chk` | پروژه را بررسی می‌کند. قبل از init: آیا ورودی‌ها آماده‌اند؟ بعد از init: آیا مستندات کامل و هم‌گام با کد است؟ | نه | فقط گزارش وضعیت می‌خواهید و نباید چیزی دست بخورد. |
| `init` | ساختار مستندات را از brief/PRD و کد می‌سازد یا به‌روز می‌کند، assetهای برند را پیدا و یکپارچه می‌کند، برای آنچه کم است placeholder برچسب‌دار می‌سازد، و هر کاستی را با پیشنهاد مشخص گزارش می‌کند. اجرای دوبارهٔ آن همان sync/update است. | فقط مستندات و assetهای زیر `docs/` | می‌خواهید فایل‌های ناقص ساخته یا کامل شوند. |
| `pchk` | پیاده‌سازی واقعی را قبل از انتشار ممیزی می‌کند: هویت و برند، پرداخت، SEO و کشف‌پذیری، دسترس‌پذیری، تست و build، هم‌گامی مستندات. | نه | نزدیک انتشار هستید. |

چرخهٔ معمول:

1. `brief.md` را می‌نویسید.
2. `chk` می‌گوید آماده‌اید یا نه.
3. `init` مستندات را می‌سازد.
4. محصول را می‌سازید.
5. هر بار مستندات از کد عقب افتاد، `chk` (برای دیدن) یا `init` (برای اصلاح).
6. قبل از انتشار، `pchk`.

هر اجرا با یک Final Checklist تمام می‌شود (بخش 7)، تا وضعیت کل پروژه را در یک صفحه ببینید.

---

## 1. شروع سریع در Claude Code (داخل پروژه‌ای که از قبل دارید)

فرض: داخل پوشهٔ پروژه‌ای هستید که Claude Code در آن کار می‌کند. سه قدم:

**قدم 1. نصب skill داخل پروژه**

```bash
git clone https://github.com/Gaply-Labs/gaply-engineering-playbook-skill.git ~/gaply-engineering-playbook-skill
~/gaply-engineering-playbook-skill/scripts/install.sh claude-project .
```

یا کپی دستی:

```bash
mkdir -p .claude/skills
cp -R ~/gaply-engineering-playbook-skill/gaply-engineering-playbook .claude/skills/
```

نتیجه در هر دو حالت:

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

یک session جدید Claude Code شروع کنید. پوشهٔ skill جدید در شروع session شناسایی می‌شود؛ ویرایش‌های بعدی روی `SKILL.md` موجود خودکار بارگذاری می‌شوند.

**قدم 2. بررسی پروژه بدون هیچ تغییری**

```text
/gaply-engineering-playbook chk
```

**قدم 3. ساخت مستندات**

```text
/gaply-engineering-playbook init
```

با زبان طبیعی هم می‌شود، انگلیسی یا فارسی. وقتی به GEP یا `gep init` اشاره کنید، Claude معمولاً خودش skill را انتخاب می‌کند:

```text
Use the gaply-engineering-playbook skill and run chk on this project.
```

```text
با skill gaply-engineering-playbook این پروژه را بررسی کن. هیچ فایلی را تغییر نده.
```

اگر درخواست را فارسی بنویسید، گزارش هم فارسی برمی‌گردد.

---

## 2. کدام دستور را لازم دارم؟

| می‌خواهید | اجرا کنید | توضیح |
| --- | --- | --- |
| فقط وضعیت فعلی را ببینید و چیزی تغییر نکند | `chk` | فقط‌خواندنی. قبل از init آمادگی را گزارش می‌کند؛ بعد از init سلامت مستندات را. |
| مستندات را از روی brief بسازید | `init` | فقط به یک نام پروژه و یک brief نیاز دارد. بقیه ساخته می‌شود. |
| فایل‌های ناقص ساخته یا کامل شوند | `init` | اول مستندات موجود را می‌خواند و فقط جاهای خالی را پر می‌کند. با همان بررسی‌های `chk` شروع می‌شود. |
| بعد از تغییر کد بدانید کدام مستند قدیمی شده | `chk` | مستندات را با کد مقایسه می‌کند و `GEP DOCS IN SYNC` یا `GEP DOCS OUT OF SYNC` برمی‌گرداند. |
| مستندات را update یا sync کنید | `init` | دستور جداگانه‌ای وجود ندارد؛ `sync` و `update` نام‌های دیگر `init` هستند. |
| assetهای برند را در `docs/assets/` مرتب کنید | `init` | آن‌ها را با pattern پیدا می‌کند و آن‌هایی که جابه‌جایی‌شان امن است را منتقل می‌کند. |
| بدانید محصول برای انتشار آماده است | `pchk` | دروازهٔ انتشار فقط‌خواندنی، با شواهد. |

بررسی فقط‌خواندنی هیچ‌وقت چیزی نمی‌نویسد. فقط `init` می‌نویسد، و فقط زیر `docs/` و در `HANDOFF.md`.

---

## 3. فراخوانی skill

### Claude Code

شکل slash، با پارامترهای اختیاری بعد از عمل:

```text
/gaply-engineering-playbook chk
/gaply-engineering-playbook init
/gaply-engineering-playbook init source=brief.md project="Nimbus Notes" lang=fa
/gaply-engineering-playbook pchk
```

زبان طبیعی:

```text
Use the gaply-engineering-playbook skill and initialize this project from brief.md.
```

```text
با skill gaply-engineering-playbook این پروژه را از روی brief.md مقداردهی اولیه کن.
```

دستورهای کوتاه اختیاری: سه فایل داخل `gaply-engineering-playbook/extras/claude-code-commands/` را در `.claude/commands/` کپی کنید تا `/gep-chk`، `/gep-init` و `/gep-pchk` داشته باشید. این‌ها فقط درخواست را به skill می‌فرستند؛ منبع حقیقت خودِ skill است.

### پارامترها

| پارامتر | اثر | مثال |
| --- | --- | --- |
| `lang=` یا `language=` | زبان خروجی. پیش‌فرض انگلیسی، یا زبانی که درخواست را با آن نوشته‌اید. | `lang=fa`، `language=Persian` |
| `project=` (یا `name=`) | نام تأییدشدهٔ پروژه. وقتی brief نام روشنی ندارد. | `project="Nimbus Notes"` |
| `source=` | فایل نیازمندی‌ها که منبع اصلی حقیقت باشد. | `source=docs/prd.md` |

نام‌های جایگزین: `check`، `precheck`، `status` برای `chk`؛ `initialize`، `bootstrap`، `scaffold`، `sync`، `update` برای `init`؛ `postcheck`، `release-check`، `final-check`، `audit` برای `pchk`.

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

نام نمایشی `GEP` است؛ نام واقعی skill همان `gaply-engineering-playbook` می‌ماند.

---

## 4. سناریوهای آماده برای کپی

**سناریو 1. پروژهٔ تازه؛ فقط `brief.md` وجود دارد.**

```text
/gaply-engineering-playbook init source=brief.md
```

یا:

```text
Use the gaply-engineering-playbook skill and initialize this project from brief.md.
```

یا به فارسی:

```text
با skill gaply-engineering-playbook این پروژه را از روی brief.md راه‌اندازی کن و مستندات استاندارد را بساز.
```

انتظار: brief تحلیل می‌شود، درخت کامل `docs/` و `HANDOFF.md` ساخته می‌شود، هر فایلی که از brief قابل استخراج است پر می‌شود، assetهای placeholder برند ساخته می‌شوند، و اجرا با یک گزارش به‌همراه Final Checklist تمام می‌شود.

**سناریو 2. فقط بررسی؛ هیچ تغییری.**

```text
Use gaply-engineering-playbook to check this project. Do not modify any files. Report missing or inconsistent documentation.
```

```text
با gaply-engineering-playbook این پروژه را بررسی کن. هیچ فایلی را تغییر نده. مستندات گمشده یا ناسازگار را گزارش کن.
```

انتظار: `chk` اجرا می‌شود. روی پروژه‌ای که هنوز مستندات GEP ندارد `READY FOR GEP INIT` یا `NOT READY FOR GEP INIT` برمی‌گرداند؛ روی پروژهٔ مقداردهی‌شده `GEP DOCS IN SYNC` یا `GEP DOCS OUT OF SYNC`. هیچ فایلی تغییر نمی‌کند.

**سناریو 3. فایل‌های ناقص ساخته شوند.**

```text
Use gaply-engineering-playbook to check the project and create the missing documentation files where enough information is available.
```

```text
با gaply-engineering-playbook پروژه را بررسی کن و هر جا اطلاعات کافی هست فایل‌های مستندات گمشده را بساز.
```

انتظار: `init` اجرا می‌شود. با بررسی‌های `chk` شروع می‌کند، مستندات موجود را نگه می‌دارد، فقط فایل‌ها و بخش‌های گمشده را اضافه می‌کند، و هر چیزی که منابع پشتیبانی نمی‌کنند را به‌جای حدس زدن در `docs/05-open-questions.md` ثبت می‌کند.

**سناریو 4. کد تغییر کرده؛ مستندات هنوز درست است؟**

```text
Run gaply-engineering-playbook check against the current project and report documentation that is outdated, missing, or inconsistent with the codebase.
```

```text
با gaply-engineering-playbook پروژهٔ فعلی را بررسی کن و مستنداتی را که قدیمی، گمشده، یا با کد ناسازگارند گزارش کن.
```

انتظار: `chk` در حالت سلامت مستندات، وضعیت Featureها، پشتهٔ فنی، معماری، `HANDOFF.md` و changelog را با ریپو مقایسه می‌کند و هر ردیف را `PASS`، `MISSING`، `OUTDATED`، `N/A` یا `UNVERIFIED` می‌زند. بعد با `init` اصلاح کنید.

**سناریو 5. ساخت playbook پروژه از روی brief به‌عنوان تنها منبع حقیقت.**

```text
Initialize the project documentation using brief.md as the primary source of truth.
```

اگر agent خودش skill را انتخاب نکرد، «using the gaply-engineering-playbook skill» را به جمله اضافه کنید.

**سناریو 6. خروجی فارسی.**

```text
/gaply-engineering-playbook init lang=fa
```

یا کل درخواست را فارسی بنویسید؛ skill به زبان درخواست جواب می‌دهد.

**سناریو 7. brief نام پروژه ندارد.**

```text
/gaply-engineering-playbook init project="Nimbus Notes"
```

**سناریو 8. از قبل logo و پوشهٔ favicon دارم. مرتبشان کن.**

```text
Use gaply-engineering-playbook to init this project. My logo and favicon are already in the repo under their own names.
```

```text
با gaply-engineering-playbook این پروژه را init کن. logo و favicon از قبل با نام‌های خودشان داخل ریپو هستند.
```

انتظار: با pattern پیدا می‌شوند، به `docs/assets/` منتقل و در فهرست assetها ثبت می‌شوند. هیچ فایلی که اپلیکیشن آن را سرو می‌کند جابه‌جا نمی‌شود.

**سناریو 9. ممیزی انتشار.**

```text
/gaply-engineering-playbook pchk
```

---

## 5. وقتی فقط `brief.md` دارید چه می‌شود

این رایج‌ترین نقطهٔ شروع است و `init` دقیقاً برای همین ساخته شده:

1. `brief.md` را کامل می‌خواند.
2. هر چیزی که brief پشتیبانی می‌کند را استخراج می‌کند: نام پروژه، خلاصه، مسئله، کاربران، جریان اصلی، موارد در scope و خارج از scope، محدودیت‌ها، منبع طراحی، ارائه‌دهندهٔ پرداخت، وجود API، تصمیم‌های صریح.
3. نوع پروژه را تشخیص می‌دهد (وب‌اپ عمومی، اپ با ورود، موبایل، backend/API، CLI یا کتابخانه)، چون نوع پروژه تعیین می‌کند کدام بررسی‌ها معنا دارند.
4. ساختار استاندارد را می‌سازد (بخش 8).
5. هر مستندی که از brief قابل پر کردن است را پر می‌کند. هر مورد در scope یک ردیف `PLANNED` در جدول ویژگی‌ها و یک فایل ویژگی می‌شود. تصمیم‌های صریح brief اولین ADRها می‌شوند. هر ابهام یک سؤال باز با شناسه می‌شود.
6. assetهای موجود برند را با pattern پیدا می‌کند، یکپارچه‌شان می‌کند، و فقط برای نوع‌هایی که هیچ فایلی ندارند placeholder می‌سازد.
7. آنچه brief به آن اشاره کرده را با آنچه روی دیسک هست مقایسه می‌کند و هر کاستی را به یک پیشنهاد مشخص تبدیل می‌کند.
8. ریپو را دوباره بازبینی می‌کند، گزارش را چاپ می‌کند، و با Final Checklist تمام می‌کند.

فقط دو چیز `init` را متوقف می‌کند: نبودن نام پروژه (راه‌حل: `project="Name"`) و نبودن brief قابل استفاده (راه‌حل: `source=path`). نبودن پوشهٔ `docs/`، نبودن طراحی، یا نبودن assetهای برند هیچ‌وقت آن را متوقف نمی‌کند؛ این‌ها یا ساخته می‌شوند یا گزارش می‌شوند.

---

## 6. گزارش پایانی `init`

هر `init` با گزارشی به این شکل تمام می‌شود. همهٔ بخش‌ها همیشه حاضرند؛ `none` یعنی چیزی پیدا نشد، نه اینکه بررسی نشد. با `lang=fa` همین گزارش به فارسی می‌آید و فقط توکن‌های نتیجه (مثل `GEP INIT COMPLETE`) انگلیسی می‌مانند.

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

`GEP INIT COMPLETE` یعنی فایل‌های لازم وجود دارند و با هم سازگارند. placeholderها و سؤال‌های باز تا وقتی ثبت شده باشند نتیجه را `INCOMPLETE` نمی‌کنند.

---

## 7. Final Checklist

هر سه عمل — `chk`، `init` و `pchk` — با یک checklist فشرده تمام می‌شوند و بعد از آن چیزی نمی‌آید. جزئیات در بخش‌های بالای گزارش می‌ماند؛ این checklist برای این است که با scroll تا انتها، وضعیت پروژه را در یک صفحه ببینید.

| نشانه | معنی |
| --- | --- |
| `[x]` | موجود و درست |
| `[~]` | موجود ولی ناقص، placeholder، یا وصل‌نشده |
| `[ ]` | موجود نیست |
| `[-]` | موضوعیت ندارد، با ذکر دلیل در همان خط |

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

`[~]` هیچ‌وقت به `[x]` گرد نمی‌شود. همین فاصله است که جلوی انتشار را می‌گیرد. گروه‌هایی که به نوع پروژه ربطی ندارند به یک خط `[-]` جمع می‌شوند.

---

## 8. چه چیزهایی ساخته می‌شود

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

نقش هر فایل:

- `HANDOFF.md`: فاز فعلی، کار فعلی، قدم بعدی، موانع.
- `docs/README.md`: `docs/` چیست و ترتیب خواندن.
- `docs/docs-manifest.md`: فهرست همهٔ artifactها با وضعیت؛ وجود این فایل یعنی پروژه با GEP مقداردهی شده است.
- `00-product-brief.md`: brief نرمال‌شده: نام، مسئله، کاربران، جریان اصلی، scope.
- `01-architecture.md`: پشته، مرزها، deployment، ساختار پوشه‌ها؛ نامعلوم‌ها صریح.
- `02-ai-context.md`: قواعد کار coding agentها در این ریپو.
- `03-project-memory.md`: زمینهٔ پایدار پروژه که از کد پیدا نیست.
- `04-decisions.md`: تصمیم‌ها (ADR)، فقط اضافه‌شدنی.
- `05-open-questions.md`: هر نکتهٔ حل‌نشده با `Blocking: YES/NO`.
- `06-changelog.md`: تغییرهای معنادار محصول و معماری.
- `07-feature-status.md`: جدول ویژگی‌ها با وضعیت `PLANNED`، `IN_PROGRESS`، `DONE` و غیره.
- `08-tech-stack.md`: فناوری‌ها، نسخه‌ها، دلیل انتخاب.
- `09-release-readiness.md`: دروازهٔ انتشار که `pchk` با شواهد پر می‌کند.
- `features/F001-name.md`: یک فایل برای هر ویژگی‌ای که brief یا کد پشتیبانی می‌کند.
- `ui/README.md`: منبع طراحی و فهرست صفحه‌ها با وضعیت.
- `ui/masterdoc.html`: design system، وقتی طراحی با Claude Design ساخته شده باشد.
- `assets/README.md`: فهرست assetها: فایل، نوع، هدف، `placeholder` یا `final`، ابعاد.
- `assets/logo.*`، `banner.*`، `favicon/`، `og.png`: assetهای برند؛ تا وقتی placeholder باشند با نام `*-default.*`.

از روی brief تنها، `init` این‌ها را کامل پر می‌کند: brief، manifest، README، قواعد agent، سؤال‌های باز، changelog، جدول ویژگی‌ها، و اسکلت دروازهٔ انتشار. این‌ها را تا جایی که brief اجازه دهد پر می‌کند: معماری، پشتهٔ فنی، تصمیم‌ها، حافظهٔ پروژه، فایل‌های ویژگی، و فهرست UI. بخش‌هایی که پشتیبانی نمی‌شوند با `Open (see Q-xxx)` مشخص می‌شوند. فایل‌های با نام `*-default.*` placeholder هستند و باید قبل از انتشار جایگزین شوند.

---

## 9. assetهای برند

چهار نوع دنبال می‌شود: **logo، banner، favicon یا مجموعهٔ آیکون اپ، و تصویر OG/شبکه‌های اجتماعی.**

**این‌ها با pattern نام پیدا می‌شوند، نه با یک مسیر ثابت.** پروژه‌ای که از قبل logo دارد به‌ندرت آن را دقیقاً جایی گذاشته که playbook می‌گذاشت، و گزارش کردن فایلی به‌عنوان گمشده در حالی که جلوی چشمتان است بدتر از سکوت است. تطبیق نام فایل یا نام پوشه کافی است:

| نوع | نام فایل شامل | نام پوشه |
| --- | --- | --- |
| Logo | `logo`, `logotype`, `logomark`, `wordmark`, `brandmark`, `brand` | `logo/`, `brand/`, `branding/` |
| Banner | `banner`, `hero`, `cover`, `header-image`, `masthead` | `banner/`, `banners/` |
| Favicon / آیکون اپ | `favicon`, `apple-touch-icon`, `android-chrome`, `mstile`, `safari-pinned-tab`, `site.webmanifest` | `favicon/`, `icons/`, `app-icon/` |
| OG / شبکه‌های اجتماعی | `og`, `opengraph`, `social`, `share`, `twitter-card`, `preview`, `card` | `og/`, `social/` |

پس `company-logo.png`، `logo_dark.svg`، و یک پوشهٔ هفت‌فایلی `favicon/` که یک generator ساخته، همه شناسایی می‌شوند.

**یکپارچه‌سازی، بدون شکستن build:**

| asset کجاست | `init` چه می‌کند |
| --- | --- |
| `docs/assets/` | هیچ کاری؛ از قبل درست است |
| هر جای دیگری زیر `docs/` | آن را به `docs/assets/` منتقل می‌کند و پوشه‌های مجموعه را حفظ می‌کند، پس `docs/favicon/` می‌شود `docs/assets/favicon/` |
| `public/`، `static/`، `src/`، `app/`، `assets/`، `www/`، `resources/`، `web/` | هیچ‌وقت منتقل نمی‌کند. سایت به آن مسیر وابسته است. در فهرست assetها با مسیر واقعی‌اش ثبت می‌شود |

بعد از جابه‌جایی، `init` هر مستندی که به فایل منتقل‌شده اشاره کرده را فهرست می‌کند تا لینک‌ها اصلاح شوند.

**Placeholder** فقط برای نوعی ساخته می‌شود که اصلاً چیزی ندارد: `logo-default.svg`، `favicon-default.svg`، و `og-default.png` با ابعاد دقیق 1200x630. برای banner هیچ placeholder ساخته نمی‌شود؛ نبودن banner به‌عنوان کاستی گزارش می‌شود. پسوند `*-default.*` همان چیزی است که یک فایل را placeholder علامت می‌زند، و انتشار با آن در `pchk` رد می‌شود.

**ابزارهای تولید**، که پیشنهاد می‌شوند به‌جای اینکه جعل شوند:

| asset | ابزار |
| --- | --- |
| مجموعهٔ favicon | https://favicon.io/favicon-converter/ |
| مجموعهٔ آیکون اپ موبایل | https://www.digia.tech/tools/app-icon-generator/ |

---

## 10. SEO، کشف‌پذیری و دیده‌شدن توسط AI

`chk` و `pchk` بررسی می‌کنند که آیا محصول پیدا می‌شود، crawl می‌شود، preview دارد و نصب‌شدنی است. این‌ها در Final Checklist می‌آیند.

فایل‌ها آن‌جایی جست‌وجو می‌شوند که سایت واقعاً آن‌ها را سرو می‌کند (ریشهٔ ریپو، `public/`، `static/`، `app/`، `src/app/`، `www/`، خروجی build)، نه زیر `docs/`:

| فایل | برای چه پروژه‌هایی |
| --- | --- |
| `robots.txt` | هر سایت سرو‌شده، از جمله سایت‌های پشت ورود که باز هم برای disallow به آن نیاز دارند |
| `sitemap.xml` | سایت‌های عمومی و قابل ایندکس؛ sitemap ساخته‌شده در زمان build وقتی config شاهد باشد قبول است |
| `llms.txt` | محصولاتی که می‌خواهند برای AI agentها قابل استفاده باشند؛ پیشنهادی، نه مسدودکننده |
| Web app manifest (`site.webmanifest`، `manifest.json`) | محصولات PWA و نصب‌شدنی، به‌همراه اندازه‌های آیکونی که اعلام می‌کند |

manifest یا favicon که فقط زیر `docs/assets/` باشد یک asset منبع است. تنها وقتی `PASS` می‌گیرد که اپلیکیشن واقعاً آن را سرو کند یا به آن ارجاع دهد.

متادیتایی که در کد بررسی می‌شود: عنوان صفحه، meta description، canonical URL، تگ‌های Open Graph، تگ‌های Twitter Card، `og:image` که روی یک URL عمومی به asset نهایی 1200x630 برسد، دادهٔ ساختاریافتهٔ Schema.org هر جا واقعاً با صفحه بخواند، سلسله‌مراتب headingها، و متن `alt` تصویرها.

اینکه کدام مورد موضوعیت دارد به نوع پروژه بستگی دارد. یک اپ پشت ورود، `robots.txt`، headingها، `alt` و manifest را نگه می‌دارد و موارد ایندکس و شبکه‌های اجتماعی را با ذکر دلیل `N/A` می‌زند. یک پروژهٔ فقط‌backend کل این گروه را جمع می‌کند.

---

## 11. طراحی UI با Claude Design

وقتی از skill بخواهید UI را طراحی کند، این جریان ثابت را دنبال می‌کند:

- با یک **پروژهٔ خالی Claude Design بدون هیچ design system از پیش‌آماده** شروع می‌کند، تا هیچ صفحه‌ای پیش‌فرض‌های اتفاقی را به ارث نبرد.
- در ریشه **`masterdoc.html`** می‌سازد که مرور محصول و کل design system را نگه می‌دارد: رنگ‌ها و tokenها، تایپوگرافی، فاصله‌گذاری، کامپوننت‌ها و حالت‌هایشان، قواعد چیدمان، و تم روشن و تیره.
- `masterdoc.html` دکمهٔ باز کردن preview اپلیکیشن را دارد، یا دو دکمه وقتی desktop و mobile دو preview جدا هستند.

ساختار فایل‌ها:

| دامنهٔ پروژه | ساختار |
| --- | --- |
| فقط وب یا desktop | `masterdoc.html` + `pages/` |
| desktop و mobile | `masterdoc.html` + `desktop/` + `mobile/` |
| فقط mobile | `masterdoc.html` + `pages/` |

هر صفحه اعلام می‌کند که `masterdoc.html` تنها منبع حقیقت برای طراحی و پیاده‌سازی است، و هیچ صفحه‌ای رنگ، فاصله، مقیاس تایپ یا کامپوننت خودش را تعریف نمی‌کند. صفحه‌ها با دادهٔ نمونهٔ واقع‌گرایانه پر می‌شوند، نه lorem ipsum، و تعاملی‌اند: navigation، فرم‌ها با validation، modal، dropdown، tab، و مجموعهٔ کامل حالت‌های UX (خالی، در حال بارگذاری، موفق، خطای validation، خطای سرور، خطای دسترسی).

**بستهٔ زمینه (context pack)** که به Claude Design داده می‌شود و عمداً کوچک است:

```text
docs/assets/logo.png
docs/00-product-brief.md
docs/02-ai-context.md
docs/07-feature-status.md
docs/features/
brief.md                  (when it carries brand direction, audience, or positioning)
```

`docs/01-architecture.md` در بستهٔ پیش‌فرض نیست. فقط وقتی بفرستید که معماری برای کاربر دیده می‌شود: navigation، دسترسی‌ها و نقش‌ها، یا جریان داده‌ای که تعیین می‌کند یک صفحه چه چیزی می‌تواند نشان دهد.

بستهٔ نهایی در `docs/ui/` بایگانی می‌شود. برای Figma یا Adobe XD، فقط لینک کافی نیست: از صفحه‌های کلیدی screenshot لازم است تا با تغییر دسترسی‌ها، ریپو کور نشود.

---

## 12. خروجی `chk`

قبل از مقداردهی (وقتی `docs/docs-manifest.md` وجود ندارد): جدولی با ستون‌های `Item | Status | Evidence | Required action` و وضعیت‌های `PASS`، `MISSING`، `N/A`، `UNVERIFIED`؛ بعد `READY FOR GEP INIT` یا `NOT READY FOR GEP INIT`، یک قدم بعدی، و Final Checklist.

بعد از مقداردهی: همان شکل با وضعیت `OUTDATED` اضافه‌شده و مقایسهٔ هر مستند با ریپو؛ بعد `GEP DOCS IN SYNC` یا `GEP DOCS OUT OF SYNC`.

## 13. خروجی `pchk`

جدول `Area | Check | Status | Evidence | Issue / Required fix` با `PASS`، `FAIL`، `N/A`، `UNVERIFIED`؛ بعد فهرست خطاهای مسدودکننده، یافته‌های غیرمسدودکننده، موارد تأییدنشده، دقیقاً یک وضعیت کلی (`READY`، `NOT READY` یا `NOT VERIFIED`)، و Final Checklist به‌همراه گروه مهندسی آن. `pchk` هیچ‌وقت بدون شاهد `PASS` نمی‌دهد و چیزی را اصلاح نمی‌کند مگر بعداً خودتان بخواهید.

---

## 14. زبان

خروجی پیش‌فرض انگلیسی است. `lang=fa` یا نوشتن درخواست به فارسی، خروجی (و برای `init`، متن مستندات تولیدشده) را فارسی می‌کند. نام فایل‌ها، شناسه‌ها، توکن‌های وضعیت و اصطلاح‌های فنی همان‌طور می‌مانند. فایل‌های خودِ skill انگلیسی می‌مانند.

---

## 15. نصب روی پلتفرم‌های دیگر

**Claude Code، شخصی (برای همهٔ پروژه‌های شما):**

```bash
~/gaply-engineering-playbook-skill/scripts/install.sh claude-global
```

یا در PowerShell ویندوز: `.\scripts\install.ps1 claude-global`. skill در `~/.claude/skills/gaply-engineering-playbook/` قرار می‌گیرد. اگر یک skill هم شخصی و هم داخل پروژه نصب باشد، نسخهٔ شخصی برنده است؛ پس هر دو را روی یک نسخه نگه دارید.

**claude.ai:** فایل `dist/gaply-engineering-playbook.zip` را در بخش Skills سفارشی زیر Settings آپلود کنید. همین ZIP داخلی را آپلود کنید، نه آرشیو کل ریپو.

**Codex، پروژه:** `./scripts/install.sh codex-project /path/to/project` (در `.agents/skills/gaply-engineering-playbook/`). **Codex، شخصی:** `./scripts/install.sh codex-global`.

**ChatGPT:** مسیر Plugins، بعد Skills، بعد Create، بعد Upload from your computer، و فایل `dist/gaply-engineering-playbook.zip`. بعد `@GEP chk`.

**OpenAI Skills API:**

```bash
curl -X POST 'https://api.openai.com/v1/skills' \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F 'files=@./dist/gaply-engineering-playbook.zip;type=application/zip'
```

---

## 16. اسکریپت‌های کمکی قطعی

هر سه اسکریپت Python 3 و فقط با کتابخانهٔ استاندارد هستند، پس هر جا agent بتواند Python اجرا کند کار می‌کنند.

```bash
python3 gaply-engineering-playbook/scripts/gep_scan.py --root /path/to/project
python3 gaply-engineering-playbook/scripts/gep_scan.py --root /path/to/project --json
```

اسکنر این‌ها را گزارش می‌کند: کاندیداهای docs، UI و brief؛ assetهای برند بر اساس pattern، با جایگاه، ابعاد و وضعیت placeholder بودنشان؛ فایل‌های کشف‌پذیری؛ اینکه پروژه با GEP مقداردهی شده یا نه؛ درخت لازم GEP؛ و موضوع‌هایی که brief به آن‌ها اشاره کرده ولی جای مربوطه وجود ندارد. این خروجی شاهد است برای agent، نه حکم: اسکنر نمی‌تواند دربارهٔ معنای SEO، دسترس‌پذیری، پرداخت یا نیازمندی‌ها قضاوت کند.

```bash
python3 gaply-engineering-playbook/scripts/organize_assets.py --root /path/to/project
python3 gaply-engineering-playbook/scripts/organize_assets.py --root /path/to/project --apply
```

assetهای برند را که بی‌نظم زیر `docs/` افتاده‌اند به `docs/assets/` منتقل می‌کند، پوشه‌های مجموعه را دست‌نخورده نگه می‌دارد، و هر مستندی که به فایل منتقل‌شده اشاره کرده را فهرست می‌کند. بدون `--apply` فقط نقشهٔ کار را چاپ می‌کند. هیچ‌وقت به assetهایی که اپلیکیشن سرو می‌کند دست نمی‌زند.

```bash
python3 gaply-engineering-playbook/scripts/create_bootstrap_assets.py --root /path/to/project --project-name "Nimbus Notes"
```

فایل‌های `docs/assets/logo-default.svg`، `favicon-default.svg` و `og-default.png` با ابعاد دقیق 1200x630 را می‌سازد. روی فایل‌های موجود بازنویسی نمی‌کند مگر با `--force`.

---

## 17. ساختار ریپو و منبع حقیقت

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

رفتار معتبر زمان اجرا در `gaply-engineering-playbook/SKILL.md` تعریف شده و `references/` پشتیبان آن است. دو فایل playbook همان استانداردِ قابل‌خواندن برای انسان‌اند: همان قواعد، بدون نیاز به agent. دو README توضیح می‌دهند که چطور skill را نصب و هدایت کنید.

---

## 18. رفع مشکل

**skill در Claude Code شناسایی نمی‌شود.** مسیر دقیق `.claude/skills/gaply-engineering-playbook/SKILL.md` (یا `~/.claude/skills/...`) را بررسی کنید: `SKILL.md` با حروف بزرگ، و skill داخل پوشهٔ خودش. یک session جدید شروع کنید. بعد صریح بخواهید: «Use the gaply-engineering-playbook skill and run chk.»

**دو نسخه رفتار متفاوت دارند.** نسخهٔ شخصی در `~/.claude/skills/` بر نسخهٔ داخل پروژه با همان نام غلبه می‌کند.

**assetی که از قبل داشتم گمشده گزارش شد.** این یک باگ است، نه رفتار مورد انتظار. assetها با patternهای بخش 9 تطبیق داده می‌شوند؛ اگر نام فایل شما با هیچ‌کدام نمی‌خواند، یک issue با نام آن فایل باز کنید تا pattern گسترده شود.

**assetی که سایت آن را سرو می‌کند جابه‌جا شد.** این هم باگ است. فقط assetهای زیر `docs/` جابه‌جا می‌شوند؛ `public/`، `static/`، `src/`، `app/`، `assets/`، `www/`، `resources/` و `web/` هیچ‌وقت دست نمی‌خورند.

**آپلود ZIP خطا می‌دهد.** فایل `dist/gaply-engineering-playbook.zip` را آپلود کنید که به یک پوشهٔ `gaply-engineering-playbook/` باز می‌شود.

**`chk` فایلی را تغییر داد.** `chk` و `pchk` فقط‌خواندنی‌اند؛ فقط `init` می‌نویسد.

**agent نیازمندی از خودش ساخت.** نیازمندی‌های گمشده یا مبهم باید در `docs/05-open-questions.md` ثبت شوند.

**`init` متوقف شد.** فقط دو مانع وجود دارد: اگر brief نام ندارد `project="Name"` بدهید؛ اگر brief پیدا نشد `source=path`.

---

## 19. به‌روزرسانی skill و هم‌گام نگه داشتن چهار مستند

پوشهٔ نصب‌شدهٔ `gaply-engineering-playbook/` را با نسخهٔ جدید جایگزین کنید (`install.sh` همین کار را می‌کند). نیازمندی‌های خاص هر محصول را در مستندات GEP همان محصول نگه دارید، نه با fork کردن skill. نسخهٔ فعلی در `VERSION` است.

استاندارد در چهار فایل زندگی می‌کند، و این چهار فایل یک مستند واحدند که بر اساس زبان و مخاطب تقسیم شده:

```text
Gaply-Engineering-Playbook.md      the standard, English
Gaply-Engineering-Playbook.fa.md   the standard, Persian
README.md                          using the skill, English
README.fa.md                       using the skill, Persian
```

**هیچ تغییری در skill، قواعد، جریان کار یا استانداردهای آن کامل نیست تا وقتی هر چهار فایل بازبینی و در صورت لزوم به‌روز شوند.** قاعده‌ای که فقط در یکی از آن‌ها باشد، قاعده‌ای است که نیمی از تیم هرگز نمی‌بیند، و دو زبانی که از هم فاصله بگیرند، همان مسیری است که یک استاندارد بی‌سروصدا تبدیل به دو استاندارد می‌شود.

---

## نکتهٔ امنیتی

Skillها دستورالعمل دارند و ممکن است اسکریپت اجرایی هم داشته باشند. فقط از ریپوهایی که به آن‌ها اعتماد دارید نصب کنید و قبل از فعال کردن هر Skill شخص ثالث، `SKILL.md` و `scripts/` را مرور کنید.

## مراجع رسمی

- Anthropic, Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Anthropic, Claude Code skills: https://code.claude.com/docs/en/skills
- OpenAI, Skills in ChatGPT: https://help.openai.com/en/articles/20001066
- OpenAI, Building Skills: https://developers.openai.com/docs/build-skills
- OpenAI, Skills API: https://developers.openai.com/api/docs/guides/tools-skills
