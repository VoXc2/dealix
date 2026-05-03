# Dealix — خطة التدشين الشاملة (مرجع واحد)

هذا الملف **يوحّد** مسار التدشين ويربط الوثائق الموجودة في الريبو. نفّذ المراحل بالترتيب؛ كل مرحلة لها **DoD** (معيار انتهاء) و**دليل** (screenshot، مخرجات terminal، رقم صف، إلخ).

**النجم الشمالي (ماذا نفوز وكيف نقيسه):** [strategic/NORTH_STAR_AR.md](strategic/NORTH_STAR_AR.md)

**قاعدة الإطلاق العام:** راجع [LAUNCH_GATES.md](LAUNCH_GATES.md) — لا تُعلن «إطلاقاً كاملاً» حتى تُستوفى القاعدة المذكورة هناك (≥24/30 بوابات + عناصر P0). قائمة عامة إضافية: [PUBLIC_LAUNCH_CHECKLIST.md](PUBLIC_LAUNCH_CHECKLIST.md).

---

## 1) ما هو جاهز في الريبو (جرد سريع)

| المحور | الملفات / المسارات |
|--------|---------------------|
| API | [`api/main.py`](../api/main.py) — فحص: `/health`؛ إن وُجد: `/health/deep` (انظر نشر الإنتاج) |
| CI | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) — `compileall` + `pytest` |
| Smoke / جاهزية | [`scripts/smoke_staging.py`](../scripts/smoke_staging.py)، [`scripts/launch_readiness_check.py`](../scripts/launch_readiness_check.py)، [`scripts/smoke_inprocess.py`](../scripts/smoke_inprocess.py)، [`scripts/print_routes.py`](../scripts/print_routes.py) |
| نشر Railway | [`RAILWAY_DEPLOY_GUIDE_AR.md`](RAILWAY_DEPLOY_GUIDE_AR.md)، [`DEPLOYMENT.md`](../DEPLOYMENT.md)، [`railway_deploy.yml`](../.github/workflows/railway_deploy.yml) |
| نشر VPS / systemd | [`DEPLOY_CHECKLIST.md`](DEPLOY_CHECKLIST.md) |
| بوابات الجاهزية | [`LAUNCH_GATES.md`](LAUNCH_GATES.md) |
| قائمة الإطلاق العام | [`PUBLIC_LAUNCH_CHECKLIST.md`](PUBLIC_LAUNCH_CHECKLIST.md) |
| Level 1 Full Ops | [`ops/full_ops_pack/DEALIX_FULL_OPS_SETUP.md`](ops/full_ops_pack/DEALIX_FULL_OPS_SETUP.md)، [`ops/TURN_ON_FULL_OPS_AR.md`](ops/TURN_ON_FULL_OPS_AR.md)، [`ops/EXECUTE_NOW_AR.md`](ops/EXECUTE_NOW_AR.md)، [`ops/full_ops_pack/LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md`](ops/full_ops_pack/LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md)، [`ops/full_ops_pack/dealix_google_apps_script.gs`](ops/full_ops_pack/dealix_google_apps_script.gs) |
| استراتيجية الفئة | [`strategic/CATEGORY_DESIGN_AND_MASTER_OPERATING_SYSTEM_AR.md`](strategic/CATEGORY_DESIGN_AND_MASTER_OPERATING_SYSTEM_AR.md)، [`strategic/SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md`](strategic/SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md)، [`strategic/NORTH_STAR_AR.md`](strategic/NORTH_STAR_AR.md)، [`strategic/DEALIX_CATEGORY_EXECUTIVE_SUMMARY_EN.md`](strategic/DEALIX_CATEGORY_EXECUTIVE_SUMMARY_EN.md) |
| v3 / Revenue Graph | [`DEALIX_V3_AUTONOMOUS_REVENUE_OS.md`](DEALIX_V3_AUTONOMOUS_REVENUE_OS.md)، [`../auto_client_acquisition/revenue_graph/`](../auto_client_acquisition/revenue_graph/)، [`../api/routers/command_center.py`](../api/routers/command_center.py) |
| GTM | [`GTM_PLAYBOOK.md`](GTM_PLAYBOOK.md)، [`ops/LAUNCH_DAY_ONE_KIT.md`](ops/LAUNCH_DAY_ONE_KIT.md)، [`OFFER_LADDER.md`](OFFER_LADDER.md)، [`COMPETITIVE_POSITIONING.md`](COMPETITIVE_POSITIONING.md) |
| فوترة يدوية | [`ops/MANUAL_PAYMENT_SOP.md`](ops/MANUAL_PAYMENT_SOP.md)، [`BILLING_MOYASAR_RUNBOOK.md`](BILLING_MOYASAR_RUNBOOK.md) |
| ما بعد الإطلاق (لا تُبنى قبل الإثبات) | [`ops/POST_LAUNCH_BACKLOG.md`](ops/POST_LAUNCH_BACKLOG.md) |

---

## 2) المراحل 0–4 (تنفيذ)

لكل مرحلة عيّن **مالكاً** واحداً ووثّق **الأداة** و**الدليل** في مجلد أدلة داخلي أو Drive حسب سياسة الشركة.

### المرحلة 0 — إغلاق المسار في GitHub

| البند | الوصف |
|--------|--------|
| الإجراء | دمج PR إلى `main` بعد CI أخضر؛ لا أسرار في الـ commit |
| الأداة | GitHub Actions + سياسة الفرع |
| DoD | `main` أخضر؛ working tree نظيف للإصدار المطلوب نشره |

### المرحلة 1 — التقني حيّ وجاهز للقياس

| البند | الوصف |
|--------|--------|
| الإجراء | `curl` على `/health` (و`/health/deep` إن وُجد على البيئة المستهدفة)؛ `python scripts/launch_readiness_check.py --base-url "$STAGING_BASE_URL"`؛ أو نشر VPS حسب [DEPLOY_CHECKLIST.md](DEPLOY_CHECKLIST.md) |
| الأداة | Terminal + متغيرات البيئة |
| DoD | مخرجات تحتوي `STAGING_HEALTH_OK` و `SMOKE_STAGING_OK` (أو ما يعادلهما على الإنتاج) **محفوظة كنص**؛ تحديث أدلة في [LAUNCH_GATES.md](LAUNCH_GATES.md) عند إغلاق أي بوابة تقنية |

### المرحلة 2 — تدشين التشغيل التجاري Level 1

| البند | الوصف |
|--------|--------|
| الإجراء | اتبع [ops/TURN_ON_FULL_OPS_AR.md](ops/TURN_ON_FULL_OPS_AR.md)؛ تحقق من [LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md](ops/full_ops_pack/LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md) |
| الأداة | Google Sheet + Form + Apps Script |
| DoD | Form مربوط · Trigger يعمل · `testInsertRow` ناجح · صف تجريبي كامل الحقول الحرجة · أدلة القائمة مكتملة |

### المرحلة 3 — أول إيراد مثبت (Paid beta path)

| البند | الوصف |
|--------|--------|
| الإجراء | مسار عرض حسب [OFFER_LADDER.md](OFFER_LADDER.md) (مثلاً Diagnostic ثم Pilot 499)؛ فاتورة يدوية عبر Moyasar إن لزم: [MANUAL_PAYMENT_SOP.md](ops/MANUAL_PAYMENT_SOP.md) |
| الأداة | Sheet + Moyasar + تواصل يدوي |
| DoD | `pilot_status` / التزام أو دفع موثّق · Proof Pack مملوء · تحديث [LAUNCH_GATES.md](LAUNCH_GATES.md) لبنود G4/G5 عند تحققها |

### المرحلة 4 — الإطلاق العام (عند الجاهزية)

| البند | الوصف |
|--------|--------|
| الإجراء | نفّذ [PUBLIC_LAUNCH_CHECKLIST.md](PUBLIC_LAUNCH_CHECKLIST.md)؛ راقب [LAUNCH_GATES.md](LAUNCH_GATES.md) |
| الأداة | قانوني + منتج + فوترة + تشغيل + GTM |
| DoD | لا إعلان «إطلاق كامل» إلا وفق قاعدة البوابات في الملف؛ سياسة خصوصية وشروط ومسارات PDPL حسب القائمة |

---

## 3) أول 48 ساعة (مسار عملي مختصر)

مزامنة مع [strategic/CATEGORY_DESIGN_AND_MASTER_OPERATING_SYSTEM_AR.md](strategic/CATEGORY_DESIGN_AND_MASTER_OPERATING_SYSTEM_AR.md) (قسم المسار القوي) و [ops/EXECUTE_NOW_AR.md](ops/EXECUTE_NOW_AR.md):

1. تأكد أن الواجهة العامة و`api` يستجيبان (حسب بيئتك: staging أو إنتاج).
2. شغّل Full Ops Board (Form + Sheet + Script + Trigger).
3. اختر الوكالات كشريحة أولى ([FIRST_10_AGENCIES_OUTREACH_AR.md](ops/full_ops_pack/FIRST_10_AGENCIES_OUTREACH_AR.md) + [LAUNCH_DAY_ONE_KIT.md](ops/LAUNCH_DAY_ONE_KIT.md)).
4. أرسل 10 لمسات يدوية آمنة.
5. اجلب 1–2 Diagnostic مكتملاً في الصف.
6. اعرض Pilot 499 حيث ينطبق.
7. جهّز أول Proof Pack في التبويب المخصص.
8. سجّل learning في Scorecard يومي ([DAILY_SCORECARD_TEMPLATE_AR.md](ops/full_ops_pack/DAILY_SCORECARD_TEMPLATE_AR.md)).

---

## 4) ما لا تفعله في هذه الجولة (لتجنب فشل التدشين)

لا تبدأ بناء: `repo_architecture_audit` ضخم، Safe Tool Gateway كامل، Role-Based Cards كاملة، أو billing automation **قبل** إغلاق المرحلة 2–3 ووجود Proof حقيقي. ضع ذلك في [POST_LAUNCH_BACKLOG.md](ops/POST_LAUNCH_BACKLOG.md) أو PRs لاحقة.

---

## 5) إغلاق أسبوع التشغيل (مشغّل)

استخدم: [prompts/PROMPT_5_LAUNCH_CLOSURE_OPERATOR.md](prompts/PROMPT_5_LAUNCH_CLOSURE_OPERATOR.md) مع جدول الأدلة في قائمة القبول.

---

## 6) فهرس سريع

| السؤال | اذهب إلى |
|--------|----------|
| من أين أبدأ اليوم؟ | [ops/EXECUTE_NOW_AR.md](ops/EXECUTE_NOW_AR.md) |
| كيف أشغّل Sheet + Form؟ | [ops/TURN_ON_FULL_OPS_AR.md](ops/TURN_ON_FULL_OPS_AR.md) |
| لماذا نفوز في الفئة؟ | [strategic/CATEGORY_DESIGN_AND_MASTER_OPERATING_SYSTEM_AR.md](strategic/CATEGORY_DESIGN_AND_MASTER_OPERATING_SYSTEM_AR.md) |
| النجم الشمالي والقياس؟ | [strategic/NORTH_STAR_AR.md](strategic/NORTH_STAR_AR.md) |
| هل نحن جاهزون تقنياً للإعلان؟ | [LAUNCH_GATES.md](LAUNCH_GATES.md) |
| قائمة الإطلاق العام؟ | [PUBLIC_LAUNCH_CHECKLIST.md](PUBLIC_LAUNCH_CHECKLIST.md) |
