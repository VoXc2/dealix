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

> آخر تحديث آلي: 2026-05-16 — مُشتقّ من مُحقِّقات `scripts/`. الدرجات
> اليدوية تبقى `FOUNDER_PENDING`. راجع
> [`docs/ops/live/CEO_EXECUTION_REPORT_2026-05-16.md`](docs/ops/live/CEO_EXECUTION_REPORT_2026-05-16.md).

| Field | Value |
|-------|--------|
| **Current Stage** | LAUNCHED تقنياً (`api.dealix.me` حيّ، 25/29 من CEO Top-50 ناجح) — **BLOCKED** على تفعيل Moyasar لـREVENUE VERIFIED |
| **Officially Sellable Services** | FOUNDER_PENDING — درجات البوابات اليدوية لم تُسجَّل بعد |
| **Services in Beta** | FOUNDER_PENDING (Score 70–84 أو ناقص demo فقط) |
| **Services Not Ready** | FOUNDER_PENDING (أقل من 70 أو hard fail) |

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

1. Lead Intelligence Sprint — `docs/services/lead_intelligence_sprint/`
2. AI Quick Win Sprint — `docs/services/ai_quick_win_sprint/`
3. Company Brain Sprint — `docs/services/company_brain_sprint/`

## Do Not Sell Yet

1. FOUNDER_PENDING — يُحدَّد بعد تسجيل درجات البوابات اليدوية.

## Critical Gaps (مُشتقّ آلياً 2026-05-16)

1. تفعيل حساب Moyasar (KYC) — يحبس كل مسار الإيراد (`account_inactive_error`).
2. صفر عملاء مدفوعين — بوابة المادة 13 `NOT_YET (0/3)`؛ بوابات الإطلاق BLOCKED.
3. `SENTRY_DSN` غير مضبوط + UptimeRobot غير مُهيّأ — رصد ناقص قبل أول عميل.

## Next Build Decisions

1. صندوق قرارات المؤسس بالكامل في [`CEO_EXECUTION_REPORT_2026-05-16.md`](docs/ops/live/CEO_EXECUTION_REPORT_2026-05-16.md) §7 (D1–D9، S1–S5).
2. ربط سجل الإثبات (revenue_os `PARTIAL`→`pass`) — مؤجَّل عمداً لما بعد أول عميل دافع (Strategic Master Plan Part V.B).
3. تصريف تراكم 20 PR مفتوح — جلسة دمج/إغلاق/توحيد.

---

## قاعدة البيع (تلخيص)

- **بع رسمياً** فقط ما عبر: Gate 0, 1, 2, 4, 5, 6 + Gate 3 كـMVP. راجع `DEALIX_READY_FOR_SALES` من السكربت.
- **Beta** إذا كان score العرض/التسليم بين **70 و 84** وبلا hard fail.
- **ممنوع** إذا كان أقل من 70 أو لا QA / لا scope / لا حوكمة / وعود مبيعات مضمونة / إرسال أو scraping غير محكوم.

## حزم الـDemo

[`demos/lead_intelligence_demo/`](demos/lead_intelligence_demo/) · [`demos/ai_quick_win_demo/`](demos/ai_quick_win_demo/) · [`demos/company_brain_demo/`](demos/company_brain_demo/)
