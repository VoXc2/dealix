# سلّم الأدوار التشغيلية ↔ خدمات Dealix

**مصدر الحقيقة للعروض والأسعار:** [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md) و [`GOVERNED_REVENUE_AI_OPS_STRATEGY.md`](GOVERNED_REVENUE_AI_OPS_STRATEGY.md) — سلم الإيراد المُحوكَم وعمليات الذكاء الاصطناعي.

**إطار المؤسسات:** طبقات A / B / C في [ENTERPRISE_OFFER_POSITIONING_AR.md](ENTERPRISE_OFFER_POSITIONING_AR.md).

## درجات سلّم الإيراد المُحوكَم وعمليات الذكاء الاصطناعي

| الدرجة | الاسم | السعر | مرحلة الرحلة |
|--------|-------|-------|----------------|
| Rung 0 | Governed Revenue & AI Ops Risk Score + Sample Proof Pack | مجاني | discovery |
| العرض العام | 7-Day Governed Revenue & AI Ops Diagnostic | 4,999 / 9,999 / 15,000 / 25,000 SAR (4 شرائح) | first_paid |
| Sprint | Revenue Intelligence Sprint | 25,000 SAR+ | execution |
| Retainer | Governed Ops Retainer | 4,999–35,000 SAR/شهر | monthly |
| مجاور | Board Decision Memo · AI Governance / Trust Pack Lite · CRM/Data Readiness for AI | حسب النطاق | expansion |

## من يشتري ماذا؟ (أدوار المشتري)

### مالك تشغيل المبيعات / RevOps

- **دخول:** Governed Revenue & AI Ops Risk Score المجاني → فهم التوافق والمخاطر بلا التزام مالي.
- **أول إثبات مدفوع:** 7-Day Governed Revenue & AI Ops Diagnostic — خريطة سير العمل، فرص مرتّبة، خريطة حدود الموافقة، مسودات عربية، Proof Pack.
- **تنفيذ مُحوكَم:** Revenue Intelligence Sprint بعد التشخيص.
- **استمرارية شهرية:** Governed Ops Retainer (إيقاع شهري: قرارات مُجهَّزة، موافقات، حزمة إثبات، تقرير KPIs).

**طبقات A/B/C:** A أقوى؛ B يتفعّل مع التسليم وProof؛ C عبر `hard_gates` وموافقات على كل قناة.

### مدير النمو / رئيس قسم GTM

- **قلب الإيقاع:** Governed Ops Retainer — تدقيقات أسبوعية، Lead Board، طابور موافقات، Proof Events، ملخص تنفيذي شهري، توصية توسعة.
- **جاهزية البيانات:** CRM/Data Readiness for AI عند استيراد أو فوضى مصادر.
- **حوكمة وثقة (اختياري):** AI Governance / Trust Pack Lite — بوابات موافقة، مستويات مخاطرة، سجل تدقيق.

**ربط تقني:** إشارات وتطبيع عبر `revenue_os` وواجهات `/api/v1/revenue-os/*` كما في [DEALIX_MASTER_OPERATING_MODEL_AR.md](DEALIX_MASTER_OPERATING_MODEL_AR.md).

### الإدارة التنفيذية / لجنة القرار (CEO والمكافئ)

- **Executive Diagnostic ثم Governed Ops Retainer (الشريحة العليا)** — تشخيص تنفيذي، خريطة حدود الموافقة، مذكرة قرار، board pack شهري، لوحات Radar / Pipeline / Delivery / Proof Ledger، سجل مخاطر، خطة ٧ أيام.
- **عرض مجاور:** Board Decision Memo عند قرار توسّع/استثمار كبير.
- **KPI مذكور في العرض:** توفير وقت قرار تنفيذي (تقديري، لا ضمان).

**لا يُباع كـ «استبدال CEO»:** الصياغة الصحيحة — **مشغّل إيرادات وقرار معتمد** ضمن حدود المنتج والعقد.

### شركاء وكلاء / قنوات

- **`agency_partner_os`** — تسعير مخصص، عمولة متفق عليها، Proof لكل عميل محوّل، بلا نشر Proof بدون موافقة موقّعة.

## قيود دستورية (تنطبق على كل المعرفات أعلاه)

من `hard_gates` و`action_modes` في كل `ServiceOffering`:

- لا إرسال حيّ (`no_live_send`)، لا خصم/تحصيل تلقائي (`no_live_charge`)، لا واتساب بارد (`no_cold_whatsapp`)، لا سكرابينغ، لا إثبات وهمي — إلخ حسب العرض.

## واجهات API للكتالوج

- `GET /api/v1/services/catalog` — قائمة العروض السبعة؛ `GET /api/v1/services/{service_id}` — تفاصيل عرض واحد؛ `GET /api/v1/services/status` — صحة الطبقة (راجع [`api/routers/service_catalog.py`](../../api/routers/service_catalog.py)).

## مراجع

- [DEALIX_MARKET_DIFFERENTIATION_AR.md](DEALIX_MARKET_DIFFERENTIATION_AR.md)
- [WAVE13_LANDING_PORTAL_ALIGNMENT_AR.md](WAVE13_LANDING_PORTAL_ALIGNMENT_AR.md)
- [ENTERPRISE_PILOT_TEMPLATE_AR.md](ENTERPRISE_PILOT_TEMPLATE_AR.md)
