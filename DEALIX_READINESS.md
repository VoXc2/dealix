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

## Company Status

_آخر تحقق آلي: 2026-05-15 — `python scripts/verify_dealix_ready.py` →_
**`DEALIX_READY_FOR_SALES=true` · Decision: `SELL_READY_STACK`**

| Field | Value |
|-------|--------|
| **Current Stage** | Gate 8 Pass — جاهز للبيع + جاهزية ريتينر؛ البناء أخضر (0 أخطاء تجميع، التطبيق يقلع) |
| **Officially Sellable Services** | lead_intelligence_sprint (100) · ai_quick_win_sprint (100) · company_brain_sprint (100) · ai_support_desk_sprint (90) · ai_governance_program (100) · client_ai_policy_pack (100) |
| **Services in Beta** | (none) |
| **Services Not Ready** | (none) |

---

## Gate Scores (يدوي: نقاط / آلي: راجع مخرجات السكربت)

| Gate | الاسم | قرار (PASS / FIX / BLOCKED) | Score يدوي / ملاحظة |
|------|--------|-----------------------------|---------------------|
| 0 | Founder Clarity | PASS | تحقق آلي 2026-05-15 |
| 1 | Offer Readiness | PASS | 6/6 عروض ≥ 85 |
| 2 | Delivery Readiness | PASS | |
| 3 | Product Readiness | PASS | البناء أخضر؛ `pytest --co` بلا أخطاء |
| 4 | Governance Readiness | PASS | محرّك eval يثبت بوابات الحوكمة (11/11 probe) |
| 5 | Demo Readiness | PASS | |
| 6 | Sales Readiness | PASS | |
| 7 | Client Delivery Readiness | PASS | اختبار e2e لـ Data Pack ينجح (6/6) |
| 8 | Retainer Readiness | PASS | |
| 9 | Scale Readiness | FIX | تضخّم الوحدات (51 يتيمة) — Phase 4 |
| 10 | World-Class Readiness | FIX | معيار طموح — انظر [`docs/company/WORLD_CLASS_READINESS_AR.md`](docs/company/WORLD_CLASS_READINESS_AR.md) |

**قرار ثلاثي:** `PASS` → انتقل | `FIX` → أصلح ثم أعد التقييم | `BLOCKED` → لا بيع ولا توسع حتى تُزال المعرقلات.

---

## Official Services

1. Lead Intelligence Sprint — `docs/services/lead_intelligence_sprint/`
2. AI Quick Win Sprint — `docs/services/ai_quick_win_sprint/`
3. Company Brain Sprint — `docs/services/company_brain_sprint/`

## Enterprise AI Transformation Programs (catalog-ready)

المصدر الرسمي: `auto_client_acquisition/service_catalog/enterprise_registry.py`
(6 برامج × 3 طبقات Basic/Growth/Enterprise — setup 25K–250K ريال + اشتراك).

| # | البرنامج | نطاق التأسيس | الحالة |
|---|----------|--------------|--------|
| ★ | Enterprise AI Transformation Sprint (45 يومًا) | 25K–150K+ | catalog + proposal + 45-day orchestrator |
| 1 | AI Operating System for Business | 50K–250K | catalog + proposal |
| 2 | AI Revenue Transformation | 25K–100K | catalog + proposal |
| 3 | AI Knowledge & Decision Platform | 30K–150K | catalog + proposal + Knowledge Center UI |
| 4 | AI Operations Automation | 40K–200K | catalog + proposal |
| 5 | AI Governance & Readiness Program | 35K–120K | catalog + proposal |

البنية التحتية الجاهزة: نموذج عروض متدرّج، مولّد عروض أسعار مؤسسية، AI Opportunity
Report، منسّق تحوّل 45 يوم متعدد المسارات، Company Brain (TF-IDF + استشهادات + RBAC)،
موصّلات Drive/Sheets/Slack/Teams، قياس ROI للـengagement.

**قرار `verify_dealix_ready.py`:** `SELL_READY_STACK` — راجع مخرجات السكربت.

## Do Not Sell Yet

1. (none — كل الخدمات الرسمية عبرت ≥ 85)

## Critical Gaps

1. **المدفوعات في وضع الاختبار** — Moyasar مدمج لكن `DEALIX_MOYASAR_MODE` افتراضياً `test`؛ التفعيل الحي قرار مؤسس (بيانات اعتماد + امتثال).
2. **تضخّم الوحدات** — ~51 وحدة OS يتيمة + عائلات مكرّرة؛ Gate 9 Scale = FIX حتى Phase 4.
3. **اختبار التحميل / scale تحت ضغط** — `locustfile.py` موجود لكن لا تقرير حِمل موثّق حديث؛ يلزم قبل وعود SLA مؤسسية. (نماذج `data-pack.html` و`diagnostic.html` مؤكَّد ربطها بـ`/api/v1/data-os` و`/api/v1/public` فعلياً.)

## Next Build Decisions

1. Phase 4 — تجميد التضخّم: تعليم الوحدات اليتيمة `deprecated` + حارس CI ضد وحدات `_vN` جديدة.
2. Phase 5 — تحقق شامل: `pytest` كامل بعتبة تغطية + `verify_dealix_ready.py` بلا `--skip-tests`.
3. قرار المؤسس — تفعيل Moyasar الحي بعد اكتمال بوابة الامتثال.

---

## قاعدة البيع (تلخيص)

- **بع رسمياً** فقط ما عبر: Gate 0, 1, 2, 4, 5, 6 + Gate 3 كـMVP. راجع `DEALIX_READY_FOR_SALES` من السكربت.
- **Beta** إذا كان score العرض/التسليم بين **70 و 84** وبلا hard fail.
- **ممنوع** إذا كان أقل من 70 أو لا QA / لا scope / لا حوكمة / وعود مبيعات مضمونة / إرسال أو scraping غير محكوم.

## حزم الـDemo

[`demos/lead_intelligence_demo/`](demos/lead_intelligence_demo/) · [`demos/ai_quick_win_demo/`](demos/ai_quick_win_demo/) · [`demos/company_brain_demo/`](demos/company_brain_demo/)
