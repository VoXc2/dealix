# 🚀 خطة الإطلاق الشاملة — Dealix (من الألف إلى الياء)

> **يوم الإطلاق:** الخميس 2026-06-05 · **أُعدّت:** 2026-06-04
> **النوع:** Soft Launch تجاري محكوم — صفحة بيع عامة + Funnel + آلة يومية موحّدة.
> **ليست:** إعلان مدفوعات Moyasar Live ولا حملة باردة — تلك بوابة لاحقة منفصلة.

هذه الوثيقة هي **المرجع الوحيد ليوم الإطلاق**. كل شيء آخر «ارجع له عند الحاجة».

---

## 0) ملخّص تنفيذي + حالة الجاهزية (حقيقية، مُتحقَّقة اليوم)

شُغّلت بوابات التحقق فعلياً بتاريخ 2026-06-04 والنتائج:

| البوابة | الأمر | النتيجة |
|---|---|---|
| جاهزية الشركة | `verify_dealix_commercial_go_live.sh` → `COMPANY_READY_VERDICT` | ✅ PASS |
| go-live تجاري | `verify_dealix_commercial_go_live.sh` → `DEALIX_COMMERCIAL_GO_LIVE_VERDICT` | ✅ PASS |
| الإطلاق الرسمي | `… → DEALIX_OFFICIAL_LAUNCH_VERDICT` | ✅ PASS |
| جاهزية Soft Launch | `verify_commercial_launch_ready.py` | ✅ PASS |
| القنوات العامة GTM | `verify_gtm_public_surfaces.py` | ✅ PASS |
| حُرّاس الدكترين (11 لا-تفاوض) | `pytest tests/test_no_*` + doctrine | ✅ 38/38 أخضر |
| بوابات الإنتاج | `run_founder_production_gates.py` | ⚠️ WARN (خطوات يدوية: Moyasar Live + DNS + DPA) |
| خط الأنابيب (عملاء مدفوعون) | `FIRST_PAID_VERDICT` | `PIPELINE_OPEN` (لا يوجد عميل مدفوع بعد — صادق) |

**الخلاصة:** المنصّة والقنوات والآلة اليومية **جاهزة للإطلاق الناعم**. المتبقّي خطوات يدوية بشرية (تسجيلات دخول شخصية) موضّحة في القسم 2. **لا توجد أرقام عملاء مختلقة — `PIPELINE_OPEN` يعني أننا نبدأ من صفر بصدق.**

---

## 1) ما الذي نُطلقه؟ — سلّم العروض الخمسة (مُسعّر وموصول)

Dealix تبيع **عمليات AI محوكمة للسوق السعودي B2B** — قدرة تشغيلية + دليل قابل للتدقيق، **لا أدوات AI ولا سبام**.

| الدرجة | العرض | السعر (ر.س) | الهدف |
|---|---|---|---|
| 0 | تشخيص AI Ops مجاني | 0 | فتح الباب + توليد ثقة |
| 1 | Sprint ذكاء الإيراد (7 أيام) | 499 | أول قيمة مدفوعة سريعة |
| 2 | حزمة Data-to-Revenue | 1,500 | تحويل بيانات → فرص |
| 3 | عمليات إيراد مُدارة (ريتينر) | 2,999–4,999/شهر | إيراد متكرّر |
| 4 | إعداد خدمة AI مخصّصة | 5,000–25,000 + 1,000/شهر | مشاريع كبيرة |
| Enterprise (مسار بطيء) | مراجعة حوكمة AI | 25,000–50,000 | مؤسسات |

**باقات الاشتراك المعروضة في الواجهة:** Starter 999 · Growth 2,999 · Scale 7,999 ر.س/شهر.
**هدف 90 يوماً:** ‎8–15K ر.س MRR + 30–40K ر.س مرة واحدة ≈ 40–55K ر.س تراكمي.

---

## 2) قبل الإطلاق — الليلة (خطوات يدوية للمؤسس فقط · ~30 دقيقة)

هذه هي الأشياء التي **لا يمكن للأتمتة تنفيذها** (تحتاج تسجيل دخولك الشخصي). راجع التفاصيل في
[`docs/go-to-market/launch_runbook.md`](../go-to-market/launch_runbook.md) و
[`docs/ops/PHASE_C_PRODUCTION_LAUNCH_AR.md`](../ops/PHASE_C_PRODUCTION_LAUNCH_AR.md).

- [ ] **Railway — النشر والمتغيّرات (3 د):** خدمة `dealix` → Settings → Deploy: امسح Start Command (يستخدم Dockerfile CMD `/app/start.sh`). Variables → Raw Editor → الصق من `docs/go-to-market/railway_vars_template.txt`. احفظ → سيعيد النشر. تحقّق: آخر Deploy = **Active** (أخضر).
- [ ] **DNS (إن لم يكن مفعّلاً):** ربط الدومين العام بالـ Railway domain. تحقّق أن `/ar` يفتح.
- [ ] **Moyasar Webhook (دقيقتان):** dashboard.moyasar.com/webhooks → Add Webhook → URL `https://<domain>/api/v1/webhooks/moyasar` · Events: `payment_paid, payment_failed, payment_refunded` · Secret = قيمة `MOYASAR_WEBHOOK_SECRET`. **أبقِ الوضع `test` ما لم تكتمل KYC** — التحويل للـ Live بأمرك أنت فقط: `python scripts/moyasar_live_cutover.py`.
- [ ] **DPA / اتفاقية معالجة البيانات (PDPL):** جاهزة للتوقيع قبل أي بيانات عميل حقيقية. راجع [`docs/commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md`](../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md).
- [ ] **القائمة الدافئة `data/warm_list.csv`:** عبّئها بأسماء من شبكتك (يدوي). بعد التعبئة فقط تعمل مولّدات المسودّات.
- [ ] **Calendly:** ضع `CALENDLY_URL` في متغيّرات Railway (يُستخدم في نموذج الحجز + الـ outreach).
- [ ] **Gmail/OAuth (اختياري لليوم 1):** للتأكيدات المعاملاتية فقط. الإرسال الخارجي يمرّ عبر approval_center.

> ⚠️ **لا تطلق Moyasar Live قبل اكتمال KYC.** الوضع `test` كافٍ تماماً لليوم 1 (Soft Launch). البديل الآمن للدفع: تحويل بنكي يدوي + فاتورة ZATCA.

---

## 3) يوم الإطلاق — Runbook ساعة بساعة (≤45 دقيقة تنفيذ فعلي)

### 🌅 الصباح (≤10 دقائق)

```bash
# 1) بوابة جاهزية اليوم (دقيقة)
bash scripts/verify_dealix_commercial_go_live.sh        # توقّع PASS

# 2) آلة المؤسس اليومية — كل شيء في أمر واحد (الأمر الأساسي الصباحي)
bash scripts/run_founder_commercial_day.sh
#   يشمل: brief · KPI · war_room_sync · import CSV · مسودّات لمسة · digest+index · social(12w) · AEO
```

ثم افتح لوحة القيادة: **`/ar/ops/founder`** (90-min cockpit) — راجع الـ10 مهام P0.

### ☀️ خلال النهار (≤30 دقيقة موزّعة)

- **3–5 لمسات دافئة** (واتساب شخصي فقط — لكل رسالة اسم + سياق مشترك + سؤال واحد). انسخ من [`docs/FIRST_10_WARM_MESSAGES_AR_EN.md`](../FIRST_10_WARM_MESSAGES_AR_EN.md). **السقف 5/يوم. لا blast. لا أتمتة.**
- **راجع الردود** على `/ar/ops/war-room` وخطّط متابعات اليوم.
- **وافق على المسودّات** الآمنة على `/ar/ops/approvals` (كل إرسال خارجي يمرّ من هنا).

### 🌙 المساء (≤5 دقائق)

- سجّل كل حدث في عمود الأدلة: `python3 scripts/founder_evening_evidence.py` (أو عبر الـUI على `/ar/ops/evidence`). أنواع الأحداث: message_sent_manual · reply_received · demo_booked · scope_requested · invoice_sent · payment_received · proof_pack_delivered.
- اقرأ تذكير الـ digest.

---

## 4) القنوات العامة (GTM Funnel) — تحقّق يدوي سريع

كل هذه شُغّلت في بوابة `verify_gtm_public_surfaces.py` = **PASS**. تأكّد بصرياً يوم الإطلاق:

| # | الصفحة | المسار |
|---|---|---|
| 1 | الصفحة الرئيسية (5 أقسام + CTAs) | `/ar` |
| 2 | Risk Score | `/ar/risk-score` |
| 3 | Proof Pack | `/ar/proof-pack` |
| 4 | التشخيص المجاني | `/ar/dealix-diagnostic` |
| 5 | الشركاء | `/ar/partners` |
| 6 | محتوى Learn (AEO) | `/ar/learn` (فهرس + مقالات) |
| 7 | التسعير | `/ar/pricing` |

**نقاط API العامة:** `POST /api/v1/public/leads` · `GET /api/v1/public/knowledge/answer` · `POST /api/v1/public/demo-request` (→ Calendly).

---

## 5) محرك المبيعات (Founder-led · محكوم)

- **الحركة:** قائمة دافئة فقط — معارف، إحالات، شركاء. **ممنوع:** scraping · واتساب بارد · أتمتة LinkedIn (حُرّاس كود يمنعونها).
- **التأهيل والعروض:** وكيل `dealix-sales` يولّد مسودّات outreach + تسجيل تأهيل + عروض من السلّم الخماسي — **كلها مسودّات تنتظر موافقتك**، لا إرسال مباشر.
- **مسار التحويل:** تشخيص مجاني → Sprint 499 → ريتينر. لكل صفقة Proof Pack (درجة ≥70) + Capital Asset.
- **War Room:** `docs/commercial/operations/targeting/agency_accounts_seed.csv` (هدف ≥80 صف) · تدوير: `python scripts/rotate_agency_targets.py`.

---

## 6) المحتوى والتسويق

- **طابور سوشال 12 أسبوعاً:** `python3 scripts/expand_social_queue_12w.py` · مسودّات اليوم: `GET /api/v1/ops-autopilot/marketing/social-today` (لا إرسال LinkedIn/واتساب حيّ — مسودّات للموافقة).
- **AEO / Learn:** مقالات الإجابة-أولاً تُحقّق بـ verdict في الآلة اليومية.
- **وكيل المحتوى** `dealix-content` ينتج: دراسات حالة (case-safe فقط) · قوالب عروض · منشورات LinkedIn (مسودّة) · تقارير قطاعية — ثنائية اللغة، وتنتهي كلها بإخلاء المسؤولية الإلزامي.

---

## 7) التسليم (Delivery SOP — Sprint 7 أيام)

وكيل `dealix-delivery` يشغّل لكل عميل:

`Source Passport` → `DQ Score` (جودة البيانات) → `Account Scoring` → `Draft Pack` → `Governance Review` → `Proof Pack` → `Capital Asset` → فحص أهلية الريتينر.

**قواعد صارمة:** لا مشروع بلا Proof Pack (≥70) · لا مشروع بلا Capital Asset · كل مخرج يحمل `governance_decision`. مرجع: [`operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md`](../commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md).

---

## 8) الامتثال والثقة (السياق السعودي)

- **PDPL:** DPA جاهز للتوقيع · لا PII في السجلّات (حارس كود) · مراجعة قانونية في [`MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md`](../commercial/MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md).
- **ZATCA:** فوترة متوافقة عبر `dealix/commercial/zatca_invoice`.
- **استضافة/إقامة البيانات:** راجع [`INFRA_HOSTING_REGION_RUBRIC_AR.md`](../commercial/INFRA_HOSTING_REGION_RUBRIC_AR.md).
- **الثقة:** كل إجابة معرفية مع `source_id` · رفض «insufficient_evidence» عند نقص الدليل · 0 حوادث PII هدف صارم.

---

## 9) المدفوعات (Moyasar)

- **الوضع الافتراضي:** `test` (sandbox). يولّد فاتورة قابلة للدفع للتجربة دون تحصيل حقيقي.
- **التحصيل الحقيقي:** `MOYASAR_LIVE_MODE=1` — **بأمر المؤسس فقط** بعد KYC: `python scripts/moyasar_live_cutover.py`.
- **النقاط:** `POST /api/v1/checkout` (فاتورة) · `POST /api/v1/webhooks/moyasar` (تأكيد الدفع → PostHog events).
- **حارس:** `test_finance_os_no_live_charge_invariant` يمنع التحصيل الحيّ غير المقصود.
- **البديل:** تحويل بنكي يدوي + فاتورة ZATCA لليوم 1.

---

## 10) البنية والنشر (Railway)

- **النشر الرسمي:** `bash scripts/railway_prod_bootstrap.sh` (legacy HOLD-only; no DDL/seed/API mutation) ثم `bash scripts/official_launch_verify.sh` → `OFFICIAL_LAUNCH_VERDICT=PASS`.
- **مصفوفة المتغيّرات:** `python3 scripts/railway_launch_env_check.py`.
- **Alembic:** CI يفرض head واحد — شغّل `alembic heads` قبل `upgrade head`.
- **smoke إنتاج:** `bash scripts/founder_production_smoke.sh` (مرّر `DEALIX_API_BASE`).
- **الخدمات:** FastAPI:8000 · Postgres:5432 · Redis:6379 · Next.js:3000.

---

## 11) المقاييس و North Star

المرجع الكامل: [`docs/commercial/NORTH_STAR_METRICS_AR.md`](../commercial/NORTH_STAR_METRICS_AR.md). أهم 5 يومياً:

1. **لمسات دافئة مُرسَلة** (يدوي، ≤5/يوم)
2. **ردود/اجتماعات محجوزة**
3. **scope_requested → فواتير**
4. **Proof Packs مُسلّمة (≥70)**
5. **حوادث PII = 0 · موافقات مسجّلة = 100% من انتقالات active**

```bash
python scripts/founder_daily_five_metrics.py      # المقاييس الخمسة
python scripts/founder_weekly_scorecard.py        # بطاقة أسبوعية
```

> ⚠️ كل الأرقام أهداف داخلية قابلة للمعايرة — **ليست وعوداً للعميل، ولا تُعلَن نتائج عميل قبل دفع مؤكّد.**

---

## 12) الإيقاع (يومي/أسبوعي)

| الإيقاع | الأمر |
|---|---|
| صباح كل يوم | `bash scripts/run_founder_commercial_day.sh` + `/ar/ops/founder` |
| مساء كل يوم | سطر في عمود الأدلة + قراءة digest |
| الأحد (بوابات أسبوعية) | `bash scripts/founder_weekly_loop.sh` + `/ar/ops/approvals` |
| المؤسس CEO | `python scripts/run_ceo_master_plan_status.py` |

---

## 13) المخاطر والتراجع (Rollback)

| الخطر | الإشارة | الإجراء |
|---|---|---|
| Railway deploy فشل | healthcheck أحمر | راجع deploy log → `bash scripts/ci_watch.sh` |
| Moyasar يبقى `test` بعد اليوم 1 | launch-status | تذكير: `moyasar_live_cutover.py` (بعد KYC فقط) |
| القائمة الدافئة فارغة | لا مسودّات | عبّئ `data/warm_list.csv` يدوياً |
| إيراد < 25K بيوم 60 | تتبّع KPI | أوقف بناء عروض جديدة → ضاعِف المبيعات |
| وقت المؤسس/Sprint > 5س بعد العميل 5 | تتبّع | أوقف بيع Sprint جديد → أتمتة Sprint أولوية P0 |
| انتهاك أي لا-تفاوض | حارس كود يفشل | ارفض العمل + اقترح بديلاً آمناً |

---

## 14) بوابات القرار (Decision Gates)

- **أخضر للموجة التالية (Enterprise Trust):** إيراد ≥40K تراكمي + 3 ريتينرات نشطة بيوم 90.
- **green-light اليوم التالي يتطلّب:** ≥1 فاتورة مدفوعة في Moyasar · ≥1 Proof Pack (≥70) · ≥1 ملخّص case-safe منشور · 0 انتهاكات دكترين في سجل التدقيق.

---

## 15) الـ11 لا-تفاوض (مفروضة بالكود — لا تُكسَر أبداً)

1. لا أنظمة scraping · 2. لا واتساب بارد آلي · 3. لا أتمتة LinkedIn · 4. لا ادعاءات بلا مصدر · 5. لا ضمان نتائج بيع · 6. لا PII في السجلّات · 7. لا إجابة معرفية بلا مصدر · 8. لا فعل خارجي بلا موافقة · 9. لا وكيل بلا هوية · 10. لا مشروع بلا Proof Pack · 11. لا مشروع بلا Capital Asset.

أي طلب يخالف واحدة منها → **يُرفَض ويُقترَح بديل آمن**.

---

## 16) ملحق — مرجع الأوامر السريع

```bash
# بوابات الجاهزية
bash scripts/verify_dealix_commercial_go_live.sh        # PASS متوقّع
python3 scripts/verify_commercial_launch_ready.py       # PASS متوقّع
python3 scripts/verify_gtm_public_surfaces.py           # PASS متوقّع

# الآلة اليومية + المقاييس
bash scripts/run_founder_commercial_day.sh
python scripts/founder_daily_five_metrics.py
python scripts/founder_weekly_scorecard.py

# الإطلاق الإنتاجي الرسمي (عند جاهزية Railway)
bash scripts/railway_prod_bootstrap.sh
bash scripts/official_launch_verify.sh                  # OFFICIAL_LAUNCH_VERDICT=PASS

# حُرّاس الدكترين
python3 -m pytest tests/test_no_*.py tests/test_commercial_doctrine.py -q
```

**لوحات التشغيل:** `/ar/ops/founder` · `/ar/ops/war-room` · `/ar/ops/marketing` · `/ar/ops/sales` · `/ar/ops/partners` · `/ar/ops/approvals` · `/ar/ops/evidence`.

---

*القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.*
