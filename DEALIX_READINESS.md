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

| Field | Value |
|-------|--------|
| **Current Stage** | (مثال: Gate 6 Pass — جاهز للبيع للخدمات الثلاث الأولى) |
| **Officially Sellable Services** | |
| **Services in Beta** | (Score 70–84 أو ناقص demo فقط) |
| **Services Not Ready** | (أقل من 70 أو hard fail) |

---

## Gate Scores (يدوي: نقاط / آلي: راجع مخرجات السكربت)

| Gate | الاسم | قرار (PASS / FIX / BLOCKED) | Score يدوي / ملاحظة |
|------|--------|-----------------------------|---------------------|
| 0 | Founder Clarity | | /100 (Pass ≥ 85) |
| 1 | Offer Readiness | | /100 (Pass ≥ 85 لكل عرض) |
| 2 | Delivery Readiness | | /100 (Pass ≥ 85) |
| 3 | Product Readiness | | /100 (Pass ≥ 80 MVP) |
| 4 | Governance Readiness | | /100 (Pass ≥ 90) |
| 5 | Demo Readiness | | /100 (Pass ≥ 85) |
| 6 | Sales Readiness | | /100 (Pass ≥ 85) |
| 7 | Client Delivery Readiness | | |
| 8 | Retainer Readiness | | /100 (Pass ≥ 85) |
| 9 | Scale Readiness | | /100 (Pass ≥ 85) |
| 10 | World-Class Readiness | | (معيار طموح — انظر [`docs/company/WORLD_CLASS_READINESS_AR.md`](docs/company/WORLD_CLASS_READINESS_AR.md)) |

**قرار ثلاثي:** `PASS` → انتقل | `FIX` → أصلح ثم أعد التقييم | `BLOCKED` → لا بيع ولا توسع حتى تُزال المعرقلات.

---

## Official Services

**Canonical 7-service catalog (Governed Revenue & AI Operations, 2026-05-16):**
انظر [`docs/company/SERVICE_CATALOG_GOVERNED_REVENUE_OPS.md`](docs/company/SERVICE_CATALOG_GOVERNED_REVENUE_OPS.md).

1. **Governed Revenue Ops Diagnostic** — `docs/services/governed_revenue_ops_diagnostic/` — **العرض الأول للسوق**
2. Revenue Intelligence Sprint — flagship
3. Governed Ops Retainer
4. AI Governance for Revenue Teams
5. CRM / Data Readiness for AI
6. Board Decision Memo
7. Trust Pack Lite — on request only

> الخدمات الثلاث القديمة (Lead Intelligence / AI Quick Win / Company Brain Sprint)
> superseded — انظر `SERVICE_REGISTRY.md`.

## Do Not Sell Yet

1.
2.
3.

## Critical Gaps

1.
2.
3.

## Next Build Decisions

1.
2.
3.

---

## قاعدة البيع (تلخيص)

- **بع رسمياً** فقط ما عبر: Gate 0, 1, 2, 4, 5, 6 + Gate 3 كـMVP. راجع `DEALIX_READY_FOR_SALES` من السكربت.
- **Beta** إذا كان score العرض/التسليم بين **70 و 84** وبلا hard fail.
- **ممنوع** إذا كان أقل من 70 أو لا QA / لا scope / لا حوكمة / وعود مبيعات مضمونة / إرسال أو scraping غير محكوم.

## حزم الـDemo

[`demos/lead_intelligence_demo/`](demos/lead_intelligence_demo/) · [`demos/ai_quick_win_demo/`](demos/ai_quick_win_demo/) · [`demos/company_brain_demo/`](demos/company_brain_demo/)
