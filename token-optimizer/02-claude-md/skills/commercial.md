# Dealix — Commercial Chain Context (On-Demand Skill)

## Overview
الماكينة التجارية الكاملة: تشخيص → واتساب → Pilot → إثبات → دفع → Upsell

## Modules — `dealix/commercial/`

| الملف | الوظيفة | الفئة |
|-------|---------|-------|
| `diagnostic_engine.py` | تشخيص 10 أقسام AR/EN عبر Claude | Free Diagnostic |
| `warm_intro_generator.py` | 5 مسودات واتساب + 3 إيميل | Outreach |
| `pilot_delivery.py` | برنامج 7 أيام 499 SAR | Sprint |
| `proof_builder.py` | أطقم إثبات L0-L5 | Proof Pack |
| `upsell_engine.py` | عروض Managed Ops 2,999-15,000 SAR | Upsell |
| `case_study_generator.py` | قصص نجاح LinkedIn-ready | Content |
| `zatca_invoice.py` | ZATCA-compliant invoices | Billing |

## Payments — `dealix/payments/`

| الملف | الوظيفة |
|-------|---------|
| `moyasar.py` | MoyasarClient wrapper |
| `payment_link.py` | Payment links for all 5 service tiers |

**Sandbox by default.** Set `MOYASAR_LIVE_MODE=1` for live payments.

## Commercial API Endpoints — `api/routers/commercial.py`

```
POST /api/v1/commercial/diagnostic/generate          → DiagnosticReport
POST /api/v1/commercial/diagnostic/generate/markdown → str (AR/EN markdown)
POST /api/v1/commercial/warm-intro/draft             → WarmIntroBundle (NO_LIVE_SEND)
POST /api/v1/commercial/pilot/start                  → PilotDeliveryKit
GET  /api/v1/commercial/pilot/{id}/report            → PilotReport
POST /api/v1/commercial/proof/build                  → ProofPack (L0-L5)
POST /api/v1/commercial/proof/build/markdown         → str (proof markdown)
POST /api/v1/commercial/payment/link                 → MoyasarPaymentLink
GET  /api/v1/commercial/payment/tiers                → list[ServiceTier]
GET  /api/v1/commercial/upsell/check/{account_id}    → UpsellOffer | None
POST /api/v1/commercial/case-study/generate          → CaseStudy
POST /api/v1/commercial/case-study/generate/markdown → str
GET  /api/v1/commercial/daily-brief                  → FounderDailyBrief
```

All endpoints require `X-API-Key` header and return `approval_status: "approval_required"`.

## Constitutional Guardrails (hard-coded)

```python
_NO_LIVE_SEND = True               # warm_intro_generator.py — never sends messages
SANDBOX_MODE = True (default)      # payment_link.py — no real charges
assert metric_after is not None    # proof_builder.py — no fake metrics
assert customer_consent            # case_study_generator.py — no unnapproved quotes
```

## Templates — `data/templates/`

| الملف | الاستخدام |
|-------|----------|
| `warm_intro_whatsapp_ar.md` | 5 قوالب واتساب + قواعد الاستخدام |
| `proposal_499_sar_ar.md` | عرض الأسبوع المكثف |
| `proof_pack_ar.md` | تنسيق طقم الإثبات L1-L3 |
| `founder_daily_checklist.md` | قائمة تحقق يومية 45 دقيقة |

## Service Tiers

```python
ServiceTier.FREE_DIAGNOSTIC   = "free_diagnostic"    # 0 SAR
ServiceTier.SPRINT_499        = "sprint_499"          # 499 SAR
ServiceTier.DATA_PACK_1500    = "data_pack_1500"      # 1,500 SAR
ServiceTier.MANAGED_OPS       = "managed_ops"         # 2,999-4,999 SAR/mo
ServiceTier.CUSTOM_AI         = "custom_ai"           # 5,000-25,000 SAR
```

## Usage Pattern

```python
from dealix.commercial.diagnostic_engine import DiagnosticEngine, DiagnosticRequest

engine = DiagnosticEngine()
report = await engine.generate(DiagnosticRequest(
    company_name="شركة الاختبار",
    sector="b2b_services"
))
# report.sections → list[10 DiagnosticSection]
# report.score → int (0-100)
```
