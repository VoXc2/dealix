# كتاب تشغيل GTM — سلّم الخدمات السبع

**الغرض:** مسار مبيعات وتشغيل موحّد لكل `service_id` في [service_catalog/registry.py](../../auto_client_acquisition/service_catalog/registry.py).  
**مرجع الأدوار:** [DEALIX_ROLE_SERVICE_LADDER_AR.md](DEALIX_ROLE_SERVICE_LADDER_AR.md).

## مبادئ

- المصدر الوحيد للأسعار والالتزامات: `GET /api/v1/services/catalog`.
- لا إرسال خارجي بلا موافقة — الحوكمة في المنتج وليس في «وعد البائع».
- كل عميل مدفوع يمر بقالب: [ENTERPRISE_PILOT_TEMPLATE_AR.md](ENTERPRISE_PILOT_TEMPLATE_AR.md).

## مسار لكل عرض (مختصر تشغيلي)

| service_id | لمسة أولى | جلسة اكتشاف | التزام التسليم | مؤشر نجاح أسبوعي |
|------------|-----------|-------------|----------------|------------------|
| `free_mini_diagnostic` | نموذج 24 ساعة | — | صفحة + جواز قرار أولي | اكتمال النموذج |
| `revenue_proof_sprint_499` | دفع + Kickoff | أهداف 7 أيام | 7 مخرجات سبرنت | ≥10 فرص |
| `data_to_revenue_pack_1500` | تدقيق الملف | خريطة مصادر | تنظيف + تقرير مخاطر | ≥20 فرصة معتمدة |
| `growth_ops_monthly_2999` | اجتماع أسبوعي ثابت | لوحة موافقات | مسودات + Proof | تحسين معدل رد (KPI في registry) |
| `support_os_addon_1500` | ربط قناة دعم | تصنيف تذاكر | SLA + مسودات | زمن أول رد |
| `executive_command_center_7500` | موجز يومي | لجنة قرار | board pack + مخاطر | توفير وقت قرار (KPI في registry) |
| `agency_partner_os` | اتفاقية شريك | تدريب Co-brand | عمولة + Proof لكل عميل | إحالة مدفوعة |

## شركاء الوكالة

- عقد موقّع، عمولة 30% سنة أولى (كما في العرض)، **لا نشر Proof** بدون موافقة العميل النهائية.

## مراجع الثقة

- [ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md](ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md)
- [DEALIX_MARKET_DIFFERENTIATION_AR.md](DEALIX_MARKET_DIFFERENTIATION_AR.md)
