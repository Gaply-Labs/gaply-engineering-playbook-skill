# اسکیل Gaply Engineering Playbook (GEP)

English guide: [README.md](README.md)

GEP یک Agent Skill است که به یک coding agent (Claude Code، Codex، ChatGPT، claude.ai) یک روش ثابت و مبتنی بر شواهد می‌دهد تا مستندات یک پروژهٔ نرم‌افزاری را از اولین `brief.md` تا ممیزی انتشار بسازد و نگه دارد. این skill آنچه در ریپو موجود است را می‌خواند، ساختار استاندارد `docs/` را از روی آن می‌سازد، هیچ نیازمندی‌ای از خودش اختراع نمی‌کند، و هر اجرا را با گزارشی تمام می‌کند که می‌گوید چه چیزی ساخته شد، چه چیزی هنوز کم است، و قدم بعدی چیست.

سه عمل دارد:

| عمل | چه کاری می‌کند | فایل تغییر می‌دهد؟ | کِی استفاده کنید |
| --- | --- | --- | --- |
| `chk` | پروژه را بررسی می‌کند. قبل از init: آیا ورودی‌ها آماده‌اند؟ بعد از init: آیا مستندات کامل و هم‌گام با کد است؟ | نه | فقط گزارش وضعیت می‌خواهید و نباید چیزی دست بخورد. |
| `init` | ساختار مستندات را از brief/PRD و کد می‌سازد یا به‌روز می‌کند، اگر assetهای نهایی برند وجود نداشته باشند placeholder برچسب‌دار می‌سازد، و هر کاستی را با پیشنهاد مشخص گزارش می‌کند. اجرای دوبارهٔ آن همان sync/update است. | فقط مستندات و placeholderها | می‌خواهید فایل‌های ناقص ساخته یا کامل شوند. |
| `pchk` | پیاده‌سازی واقعی را قبل از انتشار ممیزی می‌کند: هویت و برند، پرداخت، SEO، دسترس‌پذیری، تست و build، هم‌گامی مستندات. | نه | نزدیک انتشار هستید. |

چرخهٔ معمول:

1. `brief.md` را می‌نویسید.
2. `chk` می‌گوید آماده‌اید یا نه.
3. `init` مستندات را می‌سازد.
4. محصول را می‌سازید.
5. هر بار مستندات از کد عقب افتاد، `chk` (برای دیدن) یا `init` (برای اصلاح).
6. قبل از انتشار، `pchk`.

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

انتظار: brief تحلیل می‌شود، درخت کامل `docs/` و `HANDOFF.md` ساخته می‌شود، هر فایلی که از brief قابل استخراج است پر می‌شود، assetهای placeholder برند ساخته می‌شوند، و اجرا با گزارش بخش 6 تمام می‌شود.

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

انتظار: `chk` در حالت سلامت مستندات، فایل‌های `07-feature-status.md`، `08-tech-stack.md`، `01-architecture.md`، `HANDOFF.md` و changelog را با ریپو مقایسه می‌کند و هر ردیف را `PASS`، `MISSING`، `OUTDATED`، `N/A` یا `UNVERIFIED` می‌زند. بعد با `init` اصلاح کنید.

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

**سناریو 8. ممیزی انتشار.**

```text
/gaply-engineering-playbook pchk
```

---

## 5. وقتی فقط `brief.md` دارید چه می‌شود

این رایج‌ترین نقطهٔ شروع است و `init` دقیقاً برای همین ساخته شده:

1. `brief.md` را کامل می‌خواند.
2. هر چیزی که brief پشتیبانی می‌کند را استخراج می‌کند: نام پروژه، خلاصه، مسئله، کاربران، جریان اصلی، موارد در scope و خارج از scope، محدودیت‌ها، منبع طراحی، ارائه‌دهندهٔ پرداخت، وجود API، تصمیم‌های صریح.
3. نوع پروژه را تشخیص می‌دهد (وب‌اپ عمومی، اپ با ورود، موبایل، backend/API، CLI یا کتابخانه)، چون نوع پروژه تعیین می‌کند کدام بررسی‌ها معنا دارند.
4. ساختار استاندارد را می‌سازد (بخش 7).
5. هر مستندی که از brief قابل پر کردن است را پر می‌کند. هر مورد در scope یک ردیف `PLANNED` در جدول ویژگی‌ها و یک فایل ویژگی می‌شود. تصمیم‌های صریح brief اولین ADRها می‌شوند. هر ابهام یک سؤال باز با شناسه می‌شود.
6. اگر assetهای نهایی برند نیستند، زیر `docs/assets/` placeholder می‌سازد و آن‌ها را به‌عنوان placeholder ثبت می‌کند.
7. آنچه brief به آن اشاره کرده را با آنچه روی دیسک هست مقایسه می‌کند و هر کاستی را به یک پیشنهاد مشخص تبدیل می‌کند.
8. ریپو را دوباره بازبینی می‌کند و گزارش را چاپ می‌کند.

فقط دو چیز `init` را متوقف می‌کند: نبودن نام پروژه (راه‌حل: `project="Name"`) و نبودن brief قابل استفاده (راه‌حل: `source=path`). نبودن پوشهٔ `docs/`، نبودن طراحی، یا نبودن assetهای برند هیچ‌وقت آن را متوقف نمی‌کند؛ این‌ها یا ساخته می‌شوند یا گزارش می‌شوند.

---

## 6. گزارش پایانی `init`

هر `init` با گزارشی به این شکل تمام می‌شود. همهٔ بخش‌ها همیشه حاضرند؛ `none` یعنی چیزی پیدا نشد، نه اینکه بررسی نشد. با `lang=fa` همین گزارش به فارسی می‌آید و فقط توکن‌های نتیجه (مثل `GEP INIT COMPLETE`) انگلیسی می‌مانند.

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

`GEP INIT COMPLETE` یعنی فایل‌های لازم وجود دارند و با هم سازگارند. placeholderها و سؤال‌های باز تا وقتی ثبت شده باشند نتیجه را `INCOMPLETE` نمی‌کنند.

---

## 7. چه چیزهایی ساخته می‌شود

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
│   └── F001-name.md
├── ui/
│   ├── README.md
│   ├── screens.md          (recommended)
│   ├── flows.md            (recommended)
│   └── screenshots/        (recommended)
└── assets/
    ├── README.md
    ├── logo-default.svg
    ├── favicon-default.svg
    └── og-default.png      (exactly 1200x630)
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
- `ui/README.md`: منبع طراحی و فهرست صفحه‌ها با وضعیت (`pending design`، `designed`، `implemented`).
- `assets/README.md`: فهرست assetها: فایل، هدف، `placeholder` یا `final`، ابعاد.

از روی brief تنها، `init` این‌ها را کامل پر می‌کند: brief، manifest، README، قواعد agent، سؤال‌های باز، changelog، جدول ویژگی‌ها، و اسکلت دروازهٔ انتشار. این‌ها را تا جایی که brief اجازه دهد پر می‌کند: معماری، پشتهٔ فنی، تصمیم‌ها، حافظهٔ پروژه، فایل‌های ویژگی، و فهرست UI. بخش‌هایی که پشتیبانی نمی‌شوند با `Open (see Q-xxx)` مشخص می‌شوند. فایل‌های با نام `*-default.*` placeholder هستند و باید قبل از انتشار جایگزین شوند.

---

## 8. خروجی `chk`

قبل از مقداردهی (وقتی `docs/docs-manifest.md` وجود ندارد):

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

وضعیت‌ها: `PASS`، `MISSING`، `N/A`، `UNVERIFIED`. نتیجه: `READY FOR GEP INIT` یا `NOT READY FOR GEP INIT`.

بعد از مقداردهی: همان شکل جدول با وضعیت `OUTDATED` اضافه‌شده، مقایسهٔ هر مستند با ریپو، و در پایان `GEP DOCS IN SYNC` یا `GEP DOCS OUT OF SYNC` با قدم بعدی (`init` برای پر کردن کاستی‌ها، `pchk` قبل از انتشار).

## 9. خروجی `pchk`

جدول `Area | Check | Status | Evidence | Issue / Required fix` با `PASS`، `FAIL`، `N/A`، `UNVERIFIED`؛ بعد فهرست خطاهای مسدودکننده، یافته‌های غیرمسدودکننده، موارد تأییدنشده، و دقیقاً یک وضعیت کلی: `READY`، `NOT READY` یا `NOT VERIFIED`. `pchk` هیچ‌وقت بدون شاهد `PASS` نمی‌دهد و چیزی را اصلاح نمی‌کند مگر بعداً خودتان بخواهید.

---

## 10. زبان

خروجی پیش‌فرض انگلیسی است. `lang=fa` یا نوشتن درخواست به فارسی، خروجی (و برای `init`، متن مستندات تولیدشده) را فارسی می‌کند. نام فایل‌ها، شناسه‌ها و اصطلاح‌های فنی همان‌طور می‌مانند. فایل‌های خودِ skill انگلیسی می‌مانند.

---

## 11. نصب روی پلتفرم‌های دیگر

**Claude Code، شخصی (برای همهٔ پروژه‌های شما):**

```bash
~/gaply-engineering-playbook-skill/scripts/install.sh claude-global
```

یا در PowerShell ویندوز: `.\scripts\install.ps1 claude-global`. skill در `~/.claude/skills/gaply-engineering-playbook/` قرار می‌گیرد. اگر یک skill هم شخصی و هم داخل پروژه نصب باشد، نسخهٔ شخصی برنده است؛ پس هر دو را روی یک نسخه نگه دارید.

**claude.ai:** فایل `dist/gaply-engineering-playbook.zip` را در بخش Skills سفارشی زیر Settings آپلود کنید. همین ZIP داخلی را آپلود کنید، نه آرشیو کل ریپو.

**Codex، پروژه:** `./scripts/install.sh codex-project /path/to/project` (در `.agents/skills/gaply-engineering-playbook/`). **Codex، شخصی:** `./scripts/install.sh codex-global` (در `~/.agents/skills/`).

**ChatGPT:** مسیر Plugins، بعد Skills، بعد Create، بعد Upload from your computer، و فایل `dist/gaply-engineering-playbook.zip`. بعد `@GEP chk`.

**OpenAI Skills API:**

```bash
curl -X POST 'https://api.openai.com/v1/skills' \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F 'files=@./dist/gaply-engineering-playbook.zip;type=application/zip'
```

ZIP دقیقاً یک پوشهٔ سطح‌بالا دارد که هم API و هم مسیرهای آپلود آن را لازم دارند.

---

## 12. اسکریپت‌های کمکی قطعی

هر دو اسکریپت Python 3 و فقط با کتابخانهٔ استاندارد هستند، پس هر جا agent بتواند Python اجرا کند کار می‌کنند.

```bash
python3 gaply-engineering-playbook/scripts/gep_scan.py --root /path/to/project
python3 gaply-engineering-playbook/scripts/gep_scan.py --root /path/to/project --json
```

اسکنر این‌ها را گزارش می‌کند: کاندیداهای docs، UI، brief، لوگو، favicon و تصویر OG با ابعاد؛ اینکه پروژه با GEP مقداردهی شده یا نه؛ placeholderهایی که هنوز سر جایشان هستند؛ درخت لازم GEP؛ و موضوع‌هایی که brief یا مستندات محصول به آن‌ها اشاره کرده‌اند ولی جای مربوطه وجود ندارد (`referenced_but_missing`). این خروجی شاهد است، نه حکم: اسکنر نمی‌تواند دربارهٔ SEO، دسترس‌پذیری، پرداخت یا نیازمندی‌ها قضاوت کند.

```bash
python3 gaply-engineering-playbook/scripts/create_bootstrap_assets.py --root /path/to/project --project-name "Nimbus Notes"
```

فایل‌های `docs/assets/logo-default.svg`، `favicon-default.svg` و `og-default.png` با ابعاد دقیق 1200x630 را می‌سازد. روی فایل‌های موجود بازنویسی نمی‌کند مگر با `--force`.

---

## 13. ساختار ریپو و منبع حقیقت

```text
gaply-engineering-playbook-skill/          repository root (this repo)
├── README.md                              English guide
├── README.fa.md                           this guide
├── CLAUDE.md                              guidance for Claude Code when editing this repo
├── VERSION
├── CONTENTS.txt
├── gaply-engineering-playbook/            the skill: this folder is what gets installed
│   ├── SKILL.md                           runtime instructions (source of truth)
│   ├── references/
│   │   ├── precheck.md
│   │   ├── docs-scaffold.md
│   │   └── postcheck.md
│   ├── scripts/
│   │   ├── gep_scan.py
│   │   └── create_bootstrap_assets.py
│   ├── agents/openai.yaml
│   └── extras/claude-code-commands/
├── scripts/
│   ├── install.sh
│   └── install.ps1
└── dist/
    └── gaply-engineering-playbook.zip
```

رفتار معتبر در `gaply-engineering-playbook/SKILL.md` تعریف شده و `references/` پشتیبان آن است. این README فقط نصب و استفاده را توضیح می‌دهد و رفتار را تعریف نمی‌کند.

---

## 14. رفع مشکل

**skill در Claude Code شناسایی نمی‌شود.** مسیر دقیق `.claude/skills/gaply-engineering-playbook/SKILL.md` (یا `~/.claude/skills/...`) را بررسی کنید: `SKILL.md` با حروف بزرگ، و skill داخل پوشهٔ خودش باشد، نه `.claude/skills/SKILL.md`. یک session جدید شروع کنید. بعد صریح بخواهید: «Use the gaply-engineering-playbook skill and run chk.»

**دو نسخه رفتار متفاوت دارند.** نسخهٔ شخصی در `~/.claude/skills/` بر نسخهٔ داخل پروژه با همان نام غلبه می‌کند. یکی را به‌روز یا حذف کنید.

**آپلود ZIP خطا می‌دهد.** فایل `dist/gaply-engineering-playbook.zip` را آپلود کنید که به یک پوشهٔ `gaply-engineering-playbook/` باز می‌شود. آرشیو کل ریپو را آپلود نکنید.

**`chk` فایلی را تغییر داد.** این یک اشکال در آن اجرا است، نه رفتار مورد انتظار. `chk` و `pchk` فقط‌خواندنی‌اند؛ فقط `init` می‌نویسد.

**agent نیازمندی از خودش ساخت.** این هم نادرست است. نیازمندی‌های گمشده یا مبهم باید در `docs/05-open-questions.md` ثبت شوند و agent نباید قاعدهٔ کسب‌وکاری بسازد که brief، کد، یا دستور صریح شما پشتیبانی نمی‌کند.

**`init` متوقف شد.** فقط دو مانع وجود دارد. اگر brief نام ندارد `project="Name"` بدهید؛ اگر brief پیدا نشد `source=path`.

---

## 15. به‌روزرسانی skill

پوشهٔ نصب‌شدهٔ `gaply-engineering-playbook/` را با نسخهٔ جدید جایگزین کنید (`install.sh` همین کار را می‌کند). نیازمندی‌های خاص هر محصول را در مستندات GEP همان محصول نگه دارید، نه با fork کردن skill. نسخهٔ فعلی در `VERSION` است.

---

## نکتهٔ امنیتی

Skillها دستورالعمل دارند و ممکن است اسکریپت اجرایی هم داشته باشند. فقط از ریپوهایی که به آن‌ها اعتماد دارید نصب کنید و قبل از فعال کردن هر Skill شخص ثالث، `SKILL.md` و `scripts/` را مرور کنید.

## مراجع رسمی

- Anthropic, Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Anthropic, Claude Code skills: https://code.claude.com/docs/en/skills
- OpenAI, Skills in ChatGPT: https://help.openai.com/en/articles/20001066
- OpenAI, Building Skills: https://developers.openai.com/docs/build-skills
- OpenAI, Skills API: https://developers.openai.com/api/docs/guides/tools-skills
