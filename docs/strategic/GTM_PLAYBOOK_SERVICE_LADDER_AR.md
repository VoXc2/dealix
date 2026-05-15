# كتاب تشغيل GTM — السلّم الخماسي للخدمات

**الغرض:** مسار مبيعات وتشغيل موحّد لكل `service_id` في [service_catalog/registry.py](../../auto_client_acquisition/service_catalog/registry.py).  
**مرجع الأدوار:** [DEALIX_ROLE_SERVICE_LADDER_AR.md](DEALIX_ROLE_SERVICE_LADDER_AR.md).
**المرجع المعتمد للكتالوج:** [`../company/SERVICE_CATALOG.md`](../company/SERVICE_CATALOG.md).

## مبادئ

- المصدر الوحيد للأسعار والالتزامات: `GET /api/v1/services/catalog`.
- لا إرسال خارجي بلا موافقة — الحوكمة في المنتج وليس في «وعد البائع».
- كل عميل مدفوع يمر بقالب: [ENTERPRISE_PILOT_TEMPLATE_AR.md](ENTERPRISE_PILOT_TEMPLATE_AR.md).

## مسار لكل عرض (مختصر تشغيلي)

| service_id | لمسة أولى | جلسة اكتشاف | التزام التسليم | مؤشر نجاح أسبوعي |
|------------|-----------|-------------|----------------|------------------|
| `free_diagnostic` | نموذج 48 ساعة | — | صفحة + جواز قرار أولي | اكتمال النموذج |
| `sprint` | دفع + Kickoff | أهداف 10 أيام | مخرجات السبرنت + Proof Pack | ≥20 فرصة معتمدة |
| `pilot` | دفع + Kickoff | أهداف 30 يومًا | 4 دورات تشغيل أسبوعية + Proof Pack | اكتمال دورة أسبوعية |
| `retainer_managed_ops` | اجتماع أسبوعي ثابت | لوحة موافقات | إيقاع شهري + مسودات + Proof | تحسين معدل رد (KPI في registry) |
| `enterprise_custom_ai` | جلسة اكتشاف | نطاق SOW | بناء مخصّص + حوكمة + SLA | مرحلة SOW محقّقة |
| `agency_partner_os` | اتفاقية شريك (قناة) | تدريب Co-brand | عمولة + Proof لكل عميل | إحالة مدفوعة |

## شركاء الوكالة

- عقد موقّع، عمولة 30% سنة أولى (كما في العرض)، **لا نشر Proof** بدون موافقة العميل النهائية.

## مراجع الثقة

- [ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md](ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md)
- [DEALIX_MARKET_DIFFERENTIATION_AR.md](DEALIX_MARKET_DIFFERENTIATION_AR.md)
