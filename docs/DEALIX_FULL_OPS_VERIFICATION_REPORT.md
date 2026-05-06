# Dealix — تقرير التحقق Full-Ops ↔ خدمة الشركات

هذا المستند يربط **التحقق من خمس طبقات** (تقني، Full-Ops، تجربة شركة، قيمة، أثر طويل) بما هو **قابل للقياس في الريبو** اليوم. لا يفترض سكربتات خارجية (`v11_*`, `v12_*`, `company_service_verify.sh`) إلا إذا وُجدت فعلياً — انظر [`docs/V13_NOT_ALLOWED_REVENUE_FIRST_REALITY.md`](V13_NOT_ALLOWED_REVENUE_FIRST_REALITY.md).

---

## 1) هل الكود والإنتاج شغالين؟

| فحص | أمر / مسار |
|-----|------------|
| إنتاج | `curl -s https://api.dealix.me/health` — قارن `git_sha` مع `origin/main` |
| Smoke | `STAGING_BASE_URL=https://api.dealix.me python scripts/launch_readiness_check.py` |
| حزمة التحقق | `bash scripts/revenue_execution_verify.sh` |
| اختبارات كاملة (اختياري) | `python3 -m pytest -q --no-cov` — انسخ الملخص إلى قسم «الحقيقة» أدناه |

**نجاح:** `health` 200 + smoke يمر + `DEALIX_REVENUE_EXECUTION=PASS` من السكربت أعلاه.

---

## 2) هل Full-Ops يغطي النمو، المبيعات، الدعم، التسليم، الإثبات، الامتثال؟

| OS (مفهوم) | مخرج شركة/مشغّل | API أو وثيقة |
|-------------|-----------------|---------------|
| Growth | خطط/مسودات، لا نشر تلقائي | `GET /api/v1/growth-os/status` → `growth_v10` |
| Sales | مسودات + CRM scoring | `GET /api/v1/sales-os/status`, `POST /api/v1/crm-v10/score-lead` |
| Support | تصنيف + تصعيد | `POST /api/v1/support-os/classify` |
| Delivery | خطة خدمة | `GET /api/v1/delivery-os/status`, `GET /api/v1/delivery-os/session/{id}` |
| Customer success | حالة + at-risk | `GET /api/v1/customer-success/customer-success-os/status`, `GET /api/v1/customer-success/at-risk` |
| Partnership | مسودات شراكة | `GET /api/v1/partnership-os/status` |
| Compliance | allow/block | `POST /api/v1/compliance-os/action-check` |
| Executive | تقرير أسبوعي | `GET /api/v1/executive-os/weekly-pack` |
| Self-improvement | تعلم عند وجود بيانات | `GET /api/v1/self-improvement-os/weekly-learning` |
| Proof | أحداث | `GET /api/v1/proof-ledger/events` |

**نجاح جزئي:** كل endpoint أعلاه يرجع 200 مع guardrails واضحة في JSON حيث ينطبق.

---

## 3) هل تجربة الشركة سهلة؟

| معيار | كيف تتحقق |
|--------|-----------|
| 6 مدخلات | [`docs/revenue/05_MINI_DIAGNOSTIC_QUESTIONS_AR_EN.md`](revenue/05_MINI_DIAGNOSTIC_QUESTIONS_AR_EN.md) |
| واجهة واحدة للشركة | `GET /api/v1/company-service/command-center` — بدون أسماء OS داخلية |
| بدون مفاتيح للبدء | التشخيص CLI يعمل محلياً بدون LLM — [`scripts/dealix_diagnostic.py`](../scripts/dealix_diagnostic.py) |

---

## 4) هل القيمة الاستراتيجية والتكتيكية واضحة؟

| معيار | مرجع |
|--------|------|
| مسار إيراد | [`docs/REVENUE_EXECUTION_OS.md`](REVENUE_EXECUTION_OS.md) |
| North Star تشغيلي | حقل `north_star_hint_ar` في `company-service/command-center` |
| تموضع السوق | [`docs/COMPETITIVE_POSITIONING.md`](COMPETITIVE_POSITIONING.md) + استراتيجية [`docs/strategic/`](strategic/) |

---

## 5) هل النظام ينتج أثراً طويل المدى (وليس أداة فقط)؟

| معيار | كيف |
|--------|-----|
| Proof حقيقي | Proof Pack فارغ صادق أفضل من ادعاء — [`scripts/dealix_proof_pack.py`](../scripts/dealix_proof_pack.py) |
| تعلم من أحداث | `self-improvement-os/weekly-learning` يعيد `insufficient_data` إن لا snapshot |
| V12.1 فقط بعد عميل | [`docs/V12_1_TRIGGER_RULES.md`](V12_1_TRIGGER_RULES.md) |

---

## لوحة النتيجة (املأ بعد التشغيل)

| المقياس | القيمة |
|---------|--------|
| PRODUCTION_MATCHES_LOCAL | yes / no / unknown |
| PROD_GIT_SHA | |
| LOCAL_MAIN_SHA | |
| FULL_PYTEST | pass / fail / not_run |
| DEALIX_REVENUE_EXECUTION | PASS / FAIL |
| FIRST_3_DIAGNOSTICS_READY | yes / no |
| FIRST_PAID_PILOT_READY | yes / no / manual_only |

**DEALIX_FULL_OPS_COMPANY_SERVICE_VERDICT:** PASS | PARTIAL | FAIL

**BLOCKERS:**

**NEXT_3_FOUNDER_ACTIONS:**

1.  
2.  
3.  
