# Dealix — نظام تنفيذ CEO (أهم 50 إجراء)

هذا الملف يحوّل دور CEO إلى نظام تشغيل فعلي داخل Dealix: **50 إجراء مصنّف** مع أولوية وأثر ومخرج تشغيل وحالة تنفيذ.

## تعريف الحالات

- `DONE_NOW`: نُفّذ داخل المستودع أو له سكربت/مسار جاهز للتشغيل الفوري.
- `NEXT_7`: جاهز للتنفيذ خلال دورة تشغيل أسبوعية (يحتاج بيانات/قرار مؤسس).
- `NEXT_30`: جاهز لكن يعتمد على تراكم إثبات/عملاء/تكاملات لاحقة.

## 1) الإستراتيجية (1–6)

| # | الإجراء التنفيذي | الأثر | الحالة | مخرج التنفيذ | مرجع التنفيذ |
|---|---|---|---|---|---|
| 1 | تشغيل brief تنفيذي يومي قبل أي قرار | 100 | DONE_NOW | توصية يومية واحدة قابلة للتنفيذ | `scripts/dealix_pm_daily.py` |
| 2 | تثبيت لوحة حالة المؤسس اليومية | 99 | DONE_NOW | صورة تشغيل موحدة للوضع الحالي | `scripts/dealix_status.py` |
| 3 | اعتماد scorecard يومي رسمي | 98 | DONE_NOW | قياس يومي موحد بدل الانطباع | `scripts/founder_daily_scorecard.py` |
| 4 | اعتماد بوابة قرار weekly go/no-go | 97 | DONE_NOW | حكم إطلاق أسبوعي موثّق | `scripts/dealix_market_launch_ready_verify.sh` |
| 5 | مراجعة friction كل أسبوع | 95 | DONE_NOW | تقرير اختناقات مع أولوية معالجة | `auto_client_acquisition/friction_log/` |
| 6 | مواءمة 30/60/90 مع مخرجات فعلية | 94 | NEXT_7 | ورقة تنفيذ قصيرة محدثة | `docs/STRATEGIC_MASTER_PLAN_2026.md` |

## 2) المنتج (7–13)

| # | الإجراء التنفيذي | الأثر | الحالة | مخرج التنفيذ | مرجع التنفيذ |
|---|---|---|---|---|---|
| 7 | تثبيت baseline لـ Revenue OS | 98 | DONE_NOW | `DEALIX_REVENUE_OS_VERDICT` | `scripts/revenue_os_master_verify.sh` |
| 8 | تثبيت baseline للقدرات الجوهرية | 97 | DONE_NOW | تقرير جاهزية القدرات | `scripts/dealix_capability_verify.sh` |
| 9 | ضبط حزم الخدمات حسب القطاع | 93 | DONE_NOW | قائمة bundles جاهزة للبيع | `scripts/dealix_diagnostic.py --list-bundles` |
| 10 | توليد Diagnostic فعلي لعينة ICP | 92 | DONE_NOW | brief تسليمي قابل للمراجعة | `scripts/dealix_diagnostic.py` |
| 11 | تثبيت smoke API قبل أي ادعاء جاهزية | 91 | DONE_NOW | نتيجة smoke pass/fail | `scripts/dealix_smoke_test.py` |
| 12 | توحيد backlog الإصلاح التقني الأسبوعي | 89 | NEXT_7 | قائمة P0/P1 مرتبطة بالأثر | `docs/strategic/CEO_ROADMAP_IMPLEMENTATION_INDEX_AR.md` |
| 13 | تفعيل seed آمن لـ Saudi lead machine | 88 | NEXT_7 | seed جاهز + dry-run pass | `scripts/import_seed_leads.py --dry-run` |

## 3) المبيعات (14–21)

| # | الإجراء التنفيذي | الأثر | الحالة | مخرج التنفيذ | مرجع التنفيذ |
|---|---|---|---|---|---|
| 14 | إنشاء warm list من القالب | 97 | DONE_NOW | `data/warm_list.csv` | `data/warm_list.csv.template` |
| 15 | تعبئة أول 20 جهة warm فقط | 96 | NEXT_7 | قائمة فرص مطابقة للسياسة | `data/warm_list.csv` |
| 16 | توليد drafts تواصل ثنائية اللغة | 95 | DONE_NOW | ملف drafts جاهز للموافقة | `scripts/warm_list_outreach.py` |
| 17 | تشغيل لوحة أول 10 فرص | 93 | DONE_NOW | board منظم لأول pipeline | `scripts/dealix_first10_warm_intros.py` |
| 18 | تخصيص 5 رسائل شخصية للبدء | 92 | NEXT_7 | 5 drafts شخصية | `docs/FIRST_10_WARM_MESSAGES_AR_EN.md` |
| 19 | تسجيل كل حركة في pipeline tracker | 91 | DONE_NOW | قياس تحويل حقيقي يومي | `docs/ops/CEO_TOP50_TRACKER.csv` |
| 20 | تطبيق qualification gate على كل فرصة | 89 | NEXT_7 | قرار واضح (قبول/رفض/مؤجل) | `docs/sales-kit/WARM_LIST_WORKFLOW.md` |
| 21 | اعتماد SLA للمتابعة خلال 24 ساعة | 88 | NEXT_7 | التزام متابعة يقلل التسرب | `docs/sales-kit/DAILY_EXECUTION_SCHEDULE_AR.md` |

## 4) التسليم (22–29)

| # | الإجراء التنفيذي | الأثر | الحالة | مخرج التنفيذ | مرجع التنفيذ |
|---|---|---|---|---|---|
| 22 | تجهيز Pilot brief بسعر 499 SAR | 96 | DONE_NOW | عرض Pilot منضبط | `scripts/dealix_pilot_brief.py` |
| 23 | تجهيز فاتورة آمنة (dry-run) | 95 | DONE_NOW | invoice preview بدون شحن حي | `scripts/dealix_invoice.py --dry-run` |
| 24 | توثيق intent/confirmation للدفع | 93 | DONE_NOW | سجل حالة دفع واضح | `scripts/dealix_payment_confirmation_stub.py` |
| 25 | تشغيل kickoff لخدمة sprint | 92 | DONE_NOW | kickoff payload جاهز | `scripts/dealix_delivery_kickoff.py` |
| 26 | بدء سجل proof events يومي | 91 | DONE_NOW | أدلة تنفيذ قابلة للتدقيق | `docs/proof-events/` |
| 27 | توليد Proof Pack حتى لو empty بصدق | 90 | DONE_NOW | pack قابل للمراجعة | `scripts/dealix_proof_pack.py --allow-empty` |
| 28 | التحقق الدوري من قالب proof | 88 | DONE_NOW | فحص جاهزية قوالب الإثبات | `scripts/verify_proof_pack.py` |
| 29 | ربط كل engagement بأصل رأسمالي | 87 | NEXT_30 | asset واحد لكل حالة عميل | `auto_client_acquisition/capital_os/` |

## 5) الحوكمة والامتثال (30–36)

| # | الإجراء التنفيذي | الأثر | الحالة | مخرج التنفيذ | مرجع التنفيذ |
|---|---|---|---|---|---|
| 30 | تشغيل باقة doctrine الأساسية | 100 | DONE_NOW | تأكيد منع المخالفات غير القابلة للتفاوض | `tests/test_no_*.py` |
| 31 | التحقق المركزي من قواعد governance | 98 | DONE_NOW | تقرير قواعد PASS/FAIL | `scripts/verify_governance.py` |
| 32 | إبقاء live actions في وضع آمن افتراضيًا | 97 | DONE_NOW | منع أي إرسال/دفع خارجي تلقائي | `scripts/dealix_status.py` |
| 33 | إغلاق `REVIEW_PENDING` قبل الإطلاق التسويقي | 95 | NEXT_7 | رسائل public خالية من ثغرات claims | `tests/test_landing_forbidden_claims.py` |
| 34 | تثبيت سياسة no-source-no-answer | 94 | DONE_NOW | سلامة المحتوى والقرارات | `tests/test_no_source_no_answer.py` |
| 35 | فرض draft/approval-first لكل قناة خارجية | 93 | DONE_NOW | خط دفاع تشغيلي واضح | `docs/architecture/API_MAP.md` |
| 36 | تفعيل disclaimer القيمة التقديرية | 90 | DONE_NOW | اتساق تجاري قانوني | `dealix/registers/no_overclaim.yaml` |

## 6) العمليات والتشغيل (37–42)

| # | الإجراء التنفيذي | الأثر | الحالة | مخرج التنفيذ | مرجع التنفيذ |
|---|---|---|---|---|---|
| 37 | إقلاع Postgres/Redis محليًا | 94 | DONE_NOW | بيئة تشغيل back-end جاهزة | `docker compose up -d postgres redis` |
| 38 | تشغيل API في وضع development | 93 | DONE_NOW | endpoints متاحة للاختبار | `uvicorn api.main:app` |
| 39 | تنفيذ hello-world lead pipeline | 92 | DONE_NOW | استجابة تتضمن decision passport | `POST /api/v1/leads` |
| 40 | فحص Alembic single-head قبل الترقية | 90 | DONE_NOW | انضباط ترحيلات DB | `scripts/check_alembic_single_head.py` |
| 41 | تشغيل readiness gate صباحيًا | 89 | DONE_NOW | تقرير تشغيل يومي | `scripts/dealix_market_launch_ready_verify.sh` |
| 42 | مراقبة CI blockers قبل أي deploy | 87 | NEXT_7 | خفض مفاجآت الإصدار | `scripts/ci_watch.sh` |

## 7) المالية (43–46)

| # | الإجراء التنفيذي | الأثر | الحالة | مخرج التنفيذ | مرجع التنفيذ |
|---|---|---|---|---|---|
| 43 | تثبيت انضباط الأسعار عبر الأصول البيعية | 94 | DONE_NOW | عرض سعر متسق عبر كل المواد | `docs/V7_CUSTOMER_PITCH_AR_EN.md` |
| 44 | تجهيز cutover checklist للدفع الحي | 91 | NEXT_7 | خطة انتقال محكومة بدون مفاجآت | `docs/integrations/PAYMENT_MOYASAR_LIVE.md` |
| 45 | تفعيل reconciliation يومي للدفع | 89 | NEXT_7 | مطابقة تحصيل يومية | `scripts/reconcile_moyasar.py` |
| 46 | مراجعة شهرية لـ refund/payment governance | 87 | NEXT_30 | مذكرة انضباط مالي شهرية | `docs/REFUND_SOP.md` |

## 8) الفريق والقيادة (47–50)

| # | الإجراء التنفيذي | الأثر | الحالة | مخرج التنفيذ | مرجع التنفيذ |
|---|---|---|---|---|---|
| 47 | تطبيق قاعدة 5 مهام تنفيذية يوميًا | 92 | DONE_NOW | تركيز تنفيذي يومي ثابت | `docs/sales-kit/DAILY_EXECUTION_SCHEDULE_AR.md` |
| 48 | تشغيل Weekly Executive Pack كل أسبوع | 90 | DONE_NOW | تقرير تنفيذي أسبوعي موحّد | `scripts/dealix_weekly_executive_pack.py` |
| 49 | Retro أسبوعي (friction/proof/capital) | 89 | DONE_NOW | قرار تحسين واحد أسبوعيًا | `scripts/dealix_pm_daily.py` + `capital_os` |
| 50 | إغلاق queue القرارات مع owner/date | 88 | DONE_NOW | traceability كاملة للقرارات | `docs/EXECUTIVE_DECISION_PACK.md` |

## تنفيذ اليوم (حزمة CEO الفورية)

1. `python3 scripts/dealix_pm_daily.py --json`
2. `python3 scripts/dealix_status.py --json`
3. `python3 scripts/founder_daily_scorecard.py --json`
4. `bash scripts/revenue_os_master_verify.sh`
5. `bash scripts/dealix_capability_verify.sh`
6. `bash scripts/dealix_market_launch_ready_verify.sh`
7. `pytest tests/test_no_cold_whatsapp.py tests/test_no_linkedin_automation.py tests/test_no_scraping_engine.py tests/test_no_guaranteed_claims.py tests/test_no_source_no_answer.py -q`
8. `cp data/warm_list.csv.template data/warm_list.csv`
9. `python3 scripts/warm_list_outreach.py`
10. `python3 scripts/dealix_first10_warm_intros.py`

هذا هو تعريف “CEO execution”: **كل بند له قرار + مخرج + أداة تشغيل + حالة متابعة**.
