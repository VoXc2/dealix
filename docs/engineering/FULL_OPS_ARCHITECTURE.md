# Full Ops Architecture — Engineering Bridge

**استراتيجياً:** [`../strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md`](../strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md)  
**V12 (حالي):** [`../V12_FULL_OPS_ARCHITECTURE.md`](../V12_FULL_OPS_ARCHITECTURE.md)

## الفكرة

- **V12** يصف **9 أنظمة تشغيل** متعاونة + `full_ops` command center + Knowledge Base للدعم.  
- **Revenue Expansion (12 ماكينة)** في الخطة المركزية هي **عدسة عميل/تشغيل** حول نفس المنتج — لا استبدال لـV12، بل **تراص** مسارات وواجهات وربط أدلة.

## خرائط مقترحة (9 OS → 12 ماكينة)

| ماكينة (استراتيجياً) | أقرب حامل في V12 / الكود |
|------------------------|---------------------------|
| Market Signal | Growth OS + Revenue OS signals (حسب التطبيق) |
| Founder Media | Growth OS (محتوى) — أصول يدوية + جدولة خارجية |
| Lead Magnet | Growth OS + Sales OS (التقاط lead) |
| Sales Autopilot | Sales OS + CRM layers |
| Demo & Proof | Business Now / Cloud UI + Delivery artefacts |
| Closing & Billing | Billing/Moyasar طبقات المنتج + موافقات |
| Delivery Factory | Delivery OS |
| Support Autopilot | Support OS + `docs/knowledge-base` |
| CS & Upsell | Customer Success OS |
| Partner Distribution | Partnership OS |
| Affiliate | Partnership OS + قواعد عمولة (توسعة) |
| Governance & Evidence | Compliance OS + سياسات موافقة + Evidence ledger |

## مجلدات `dealix/` المستهدفة (تدريجي)

`growth/` · `sales/` · `support/` · `partners/` · `affiliates/` · `delivery/` · `governance/` · `evidence/` · `agents/` · `billing/` · `reports/` · `config/`

**ملاحظة:** اليوم تُوزّع القدرات على `auto_client_acquisition/` ووحدات `dealix/*` الحالية — لا تُفترض إعادة تسمية ضخمة دفعة واحدة.

## واجهات API

- **الحالية:** عائلة `/api/v1/*-os` + `full-ops` + `business-now` + `transformation` (راجع `AGENTS.md`).  
- **الهدف الموحّد:** مسارات `public/*` و`ops/*` كما في Master Plan — **تنفيذ تدريجي** مع إبقاء العقود الخلفية مستقرة.

## Config

YAML تحت [`../../dealix/config/`](../../dealix/config/) — مرجع سياسات العرض والأتمتة والتسعير.
