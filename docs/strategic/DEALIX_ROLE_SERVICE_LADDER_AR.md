# سلّم الأدوار التشغيلية ↔ خدمات Dealix

**مصدر الحقيقة للعروض والأسعار:** [`auto_client_acquisition/service_catalog/registry.py`](../../auto_client_acquisition/service_catalog/registry.py) (`OFFERINGS` — ترتيب العرض = ترتيب الكتالوج).

**إطار المؤسسات:** طبقات A / B / C في [ENTERPRISE_OFFER_POSITIONING_AR.md](ENTERPRISE_OFFER_POSITIONING_AR.md).

> ⚠️ وُحِّد الكتالوج إلى **سلّم خماسي** بمعرّفات جديدة. أقسام «أدوار المشتري»
> أدناه قد تستخدم معرّفات قديمة — المرجع المعتمد:
> [`../company/SERVICE_CATALOG.md`](../company/SERVICE_CATALOG.md).

## معرّفات السلّم الخماسي + القناة (IDs)

| `service_id` | اسم عربي (مختصر) | السعر (ر.س) | مرحلة الرحلة |
|----------------|-------------------|-------------|----------------|
| `free_diagnostic` | التشخيص المجاني للذكاء الاصطناعي | مجاني | discovery |
| `sprint` | سبرنت إثبات القيمة | 2,500 | first_paid |
| `pilot` | بايلوت التشغيل | 9,500 | pilot |
| `retainer_managed_ops` | التشغيل المُدار الشهري | 6,000–18,000/شهر | retainer |
| `enterprise_custom_ai` | المؤسسات والذكاء الاصطناعي المخصّص | 45,000–120,000 | enterprise |
| `agency_partner_os` | نظام شريك الوكالة (قناة) | بالاتفاق | channel |

## من يشتري ماذا؟ (أدوار المشتري)

### مالك تشغيل المبيعات / RevOps

- **دخول:** `free_mini_diagnostic` → فهم التوافق والمخاطر بلا التزام مالي.
- **أول إثبات مدفوع:** `revenue_proof_sprint_499` — Company Brain، فرص مرتّبة، Decision Passports، مسودات عربية، Proof Pack.
- **تنظيف بيانات وتوسيع قمع:** `data_to_revenue_pack_1500`.
- **إضافة شهرية:** غالباً `growth_ops_monthly_2999` (لوحات، موافقات يومية، مسودات، Proof مستمر).

**طبقات A/B/C:** A أقوى؛ B يتفعّل مع التسليم وProof؛ C عبر `hard_gates` وموافقات على كل قناة.

### مدير النمو / رئيس قسم GTM

- **قلب الرитم:** `growth_ops_monthly_2999` — تدقيقات أسبوعية، Lead Board، طابور موافقات، Proof Events، ملخص تنفيذي شهري، توصية توسعة.
- **تكثيف البيانات:** `data_to_revenue_pack_1500` عند استيراد أو فوضى مصادر.
- **دعم ما بعد البيع (اختياري):** `support_os_addon_1500` — تصنيف تذاكر، ردود مقترحة (مسودة فقط)، صحة عميل.

**ربط تقني:** إشارات وتطبيع عبر `revenue_os` وواجهات `/api/v1/revenue-os/*` كما في [DEALIX_MASTER_OPERATING_MODEL_AR.md](DEALIX_MASTER_OPERATING_MODEL_AR.md).

### الإدارة التنفيذية / لجنة القرار (CEO والمكافئ)

- **`executive_command_center_7500`** — موجز يومي (واتساب حسب التصميم)، تدقيق أسبوعي، board pack شهري، لوحات Radar / Pipeline / Growth / Support / Delivery / Payment / Proof Ledger، سجل مخاطر، خطة ٧ أيام.
- **KPI مذكور في السجل:** توفير وقت قرار تنفيذي (تقديري، مع التزام تعاقدي كما في `registry`).

**لا يُ sold كـ «استبدال CEO»:** الصياغة الصحيحة — **مشغّل إيرادات وقرار معتمد** ضمن حدود المنتج والعقد.

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
