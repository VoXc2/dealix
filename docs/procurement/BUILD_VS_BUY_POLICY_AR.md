# سياسة Build vs Buy — Dealix Build vs Buy Policy

> **كل قرار "نُبرمج من الصفر" أو "نشتري" يحتاج تقييم.** هذا الـ doc
> يحدد الإطار.

**الحالة:** مسودة — Phase 3 من Agent #17
**التاريخ:** 2026-06-03

---

## 1. مصفوفة القرار (Decision Matrix)

| العامل | يميل إلى Buy | يميل إلى Build |
| --- | --- | --- |
| Time to value | أسابيع | شهور+ |
| Differentiation | منخفض | مرتفع |
| Customization need | قليل | كثير |
| Data sensitivity | منخفض | مرتفع |
| Volume | متوسط | مرتفع |
| Switching cost | منخفض | مرتفع |
| Long-term cost | $20K/year | $50K+ /year |

## 2. القرارات الحالية (Current Decisions)

### Buy (Commodity)
- **PostHog** — analytics
- **Sentry** — error monitoring
- **SendGrid** — transactional email
- **Calendly** — scheduling
- **Railway** — hosting
- **AWS S3** — backup storage
- **1Password** — secrets vault
- **Moyasar** — payments (لا بديل محلي بنفس الجودة)

### Build (Core Moat)
- **Revenue OS** — commercial chain
- **Governance engine** — approval + audit
- **Proof ledger** — proof of work
- **WhatsApp decision layer** — multi-provider + safety
- **Personal Operator** — daily brief engine
- **Saudi Lead Machine** — sector-specific lead gen

### Hybrid
- **WhatsApp integration** — buy provider (Green/Ultramsg/Fonnte/Meta)
  + build governance
- **CRM sync** — buy HubSpot + build sync layer
- **LLM routing** — buy models + build cost/quality router

## 3. متى نعيد التقييم (When to Re-evaluate)

- **سنوياً** مراجعة شاملة.
- **عند تغيير الحجم** 10x (e.g. > 1000 customers).
- **عند خروج vendor** من السوق.
- **عند تغيير data residency policy.**

## 4. معايير الإيقاف (Stop-Build Criteria)

ابنِ إذا:
- Time to first version < 30 يوم
- Founder-led ممكن
- Long-term cost أقل من $50K/year equivalent

لا تبني إذا:
- Vendor موجود بـ $X/month و X < تكلفة بنائنا السنوية
- لا فرق واضح في الـ moat
- لا bandwidth للفريق

## 5. المالك (Owner)

- **فقط المؤسس** يوافق على قرارات build.
- أي agent يقترح build ⇒ PR + business case + cost estimate.

## 6. المراجع

- `docs/procurement/VENDOR_MANAGEMENT_OS_AR.md`
- `docs/procurement/TOOL_SELECTION_POLICY_AR.md`
- `docs/finance/FOUNDER_UNIT_ECONOMICS_MODEL_AR.md`
- `data/procurement/vendors.jsonl`
