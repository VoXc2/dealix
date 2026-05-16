# Dealix Readiness Control Center

**لا تثق بالإحساس. ثق بنظام التحقق.**  
**نظام التشغيل اليومي:** [`docs/company/DEALIX_OPERATING_KERNEL.md`](docs/company/DEALIX_OPERATING_KERNEL.md) — [`docs/company/DECISION_RULES.md`](docs/company/DECISION_RULES.md) — مراجعة أسبوعية [`docs/company/WEEKLY_OPERATING_REVIEW.md`](docs/company/WEEKLY_OPERATING_REVIEW.md) — [`docs/company/SERVICE_REGISTRY.md`](docs/company/SERVICE_REGISTRY.md).  
سياق السوق: [McKinsey — The State of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai/) — [Gartner — AI-ready data](https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk).

المرجع: [`docs/company/DEALIX_STAGE_GATES_AR.md`](docs/company/DEALIX_STAGE_GATES_AR.md).

التحقق الآلي:

```bash
python scripts/verify_dealix_ready.py
python scripts/verify_dealix_ready.py --skip-tests
```

---

> **آخر تحديث صادق:** 2026-05-16. الحالة أدناه واقعية وليست طموحة — راجع `قاعدة البيع`.

## Company Status

| Field | Value |
|-------|--------|
| **Current Stage** | ما قبل الإيرادات — منشور تقنياً (`api.dealix.me`)، صفر عملاء، صفر إيراد. |
| **Officially Sellable Services** | Rung 0 — Free AI Ops Diagnostic. |
| **Services in Beta** | Rung 1 — 7-Day Revenue Intelligence Sprint (499 SAR): مسار التسليم أُصلح ويعمل end-to-end؛ ينتظر أول عميل حقيقي + تفعيل Moyasar. |
| **Services Not Ready** | Rung 2 (Data Pack)، Rung 3 (Managed Ops)، Rung 4 (Custom AI) — مقفلة ببوابات السُلّم حتى تُسلَّم pilots. |

---

## Gate Scores (يدوي: نقاط / آلي: راجع مخرجات السكربت)

| Gate | الاسم | قرار | ملاحظة |
|------|--------|------|---------|
| 0 | Founder Clarity | PASS | العقيدة والسُلّم الخماسي محسومان. |
| 1 | Offer Readiness | FIX | السُلّم الخماسي مُعتمد؛ يلزم مواءمة README/landing عليه (مصدر حقيقة واحد). |
| 2 | Delivery Readiness | FIX | منسّق الـ7-Day Sprint أُصلح ويعمل؛ يلزم تشغيله على بيانات عميل حقيقي مرة واحدة. |
| 3 | Product Readiness | FIX | الـAPI يقلع (750 مسار)؛ المجموعة الكاملة فيها ~57 فشل سابق (انجراف اختبار↔كود). |
| 4 | Governance Readiness | PASS | الـ11 غير-قابل-للتفاوض مُنفَّذة في `doctrine.py` ومُختبرة. |
| 5 | Demo Readiness | FIX | حزم demo موجودة؛ تحتاج تحقق على المنسّق المُصلَّح. |
| 6 | Sales Readiness | BLOCKED | لا بيع رسمي قبل تفعيل Moyasar (لا قدرة تحصيل حالياً). |
| 7 | Client Delivery Readiness | FIX | السجلات (Proof/Capital/Value/Governance) موجودة؛ صفر Proof Pack مُسلَّم. |
| 8 | Retainer Readiness | BLOCKED | يعتمد على ≥3 pilots. |
| 9 | Scale Readiness | BLOCKED | يعتمد على إيراد متكرر. |
| 10 | World-Class Readiness | BLOCKED | معيار طموح — بعيد. |

**قرار ثلاثي:** `PASS` → انتقل | `FIX` → أصلح ثم أعد التقييم | `BLOCKED` → لا بيع ولا توسع حتى تُزال المعرقلات.

---

## Official Services (السُلّم الخماسي — مصدر الحقيقة الوحيد)

راجع [`docs/COMPANY_SERVICE_LADDER.md`](docs/COMPANY_SERVICE_LADDER.md).

1. **Rung 0** — Free AI Ops Diagnostic (0 SAR) — قابل للبيع الآن.
2. **Rung 1** — 7-Day Revenue Intelligence Sprint (499 SAR) — Beta، ينتظر Moyasar + أول عميل.
3. **Rung 2–4** — Data Pack / Managed Ops / Custom AI — مقفلة ببوابات الفتح.

## Do Not Sell Yet

1. Rung 2 (Data Pack) — يُفتح بعد 3 pilots بنفس القطاع.
2. Rung 3 (Managed Ops) — يُفتح بعد 3 أشهر retainer.
3. Rung 4 (Custom AI) — يُفتح بعد 3 pilots + إذن موقّع.

## Critical Gaps

1. **Moyasar غير مُفعّل** — لا قدرة تحصيل (`account_inactive_error`). إجراء KYC على المؤسس. يحجب كل إيراد.
2. **صفر Proof Pack مُسلَّم وصفر case study** — لا دليل أثر؛ يحجب الترقّي في السُلّم.
3. **~57 فشل اختبار سابق** في المجموعة الكاملة — انجراف اختبار↔كود من موجات البناء السابقة (مثل LLM router `route` مفقود، enum `ACTIVE` مفقود) — دَيْن جودة يجب سداده.

## Next Build Decisions

1. مواءمة README/landing/COMMERCIAL_WIRING على السُلّم الخماسي (مصدر حقيقة واحد).
2. تشغيل الـ7-Day Sprint المُصلَّح على بيانات تجريبية كاملة وإصدار أول Proof Pack داخلي.
3. سداد دَيْن الاختبارات الـ57 (إصلاح انجراف اختبار↔كود) قبل ادعاء "جاهز للإنتاج".

---

## قاعدة البيع (تلخيص)

- **بع رسمياً** فقط ما عبر: Gate 0, 1, 2, 4, 5, 6 + Gate 3 كـMVP. راجع `DEALIX_READY_FOR_SALES` من السكربت.
- **Beta** إذا كان score العرض/التسليم بين **70 و 84** وبلا hard fail.
- **ممنوع** إذا كان أقل من 70 أو لا QA / لا scope / لا حوكمة / وعود مبيعات مضمونة / إرسال أو scraping غير محكوم.

## حزم الـDemo

[`demos/lead_intelligence_demo/`](demos/lead_intelligence_demo/) · [`demos/ai_quick_win_demo/`](demos/ai_quick_win_demo/) · [`demos/company_brain_demo/`](demos/company_brain_demo/)
