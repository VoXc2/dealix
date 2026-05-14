# مصفوفة العروض القابضة — ربط `docs/26`–`docs/44` بعرض وسعر ومدة ومستبعد

**الغرض:** تحويل كثافة الوثائق إلى وحدات أعمال قابلة للبيع. الأرقام **إرشادية** (SAR) — تُثبَّت في العقد و`docs/30_pricing/` حسب السوق.

**رموز:** BU = وحدة أعمال؛ IP = ترخيص/ورشة؛ CR = تغيير نطاق لاحق عبر `delivery_os`.

| المجلد | اسم العرض التجاري | المخرج الملموس | تسعير إرشادي (SAR) | المدة | مستبعد صراحةً | مرساة كود |
|--------|---------------------|----------------|---------------------|--------|----------------|-----------|
| `docs/26_service_catalog` | كتالوج الخدمات + اختيار Sprint | قائمة خدمات + Scope Card | — (مدخل مجاني) | 1 جلسة | لا تنفيذ خارج الكتالوج | [`api/routers/commercial_engagements.py`](../../api/routers/commercial_engagements.py) (`delivery_catalog`) |
| `docs/27_delivery_playbooks` | تسليم Sprint محكوم | Playbook + QA checklist | مضمن في Sprint | ~14 يوماً | لا SLA قانوني لنتائج مبيعات | `delivery_os` |
| `docs/28_change_requests` | سياسة CR / Retainer backlog | تصنيف نطاق + رفض ممنوعات | CR بالساعة/الباقة | لكل طلب | scraping / cold WA / ضمان مبيعات | [`auto_client_acquisition/delivery_os/scope_classifier.py`](../../auto_client_acquisition/delivery_os/scope_classifier.py) |
| `docs/28_operating_finance` | مراجعة هامش العرض | جدول هامش + تكلفة AI | 1,500–4,999 | 3–5 أيام | ليس استشارة ضريبية | `operating_finance_os` |
| `docs/29_sales_os` | حزمة اكتشاف + عرض | ICP + مسودة عرض | 499–2,999 | أسبوع | إرسال خارجي آلي | [`auto_client_acquisition/sales_os/`](../../auto_client_acquisition/sales_os/) |
| `docs/30_pricing` | هيكل تسعير القابضة | شرائح Sprint/Retainer | مرجع داخلي | — | لا التزام عميل | [`docs/30_pricing/`](../30_pricing/) |
| `docs/31_operating_finance` | حوكمة هامش + تكلفة | سياسات Reprice/Cost guard | مضمن Retainer أو 2,999+ | شهر | لا ضمان إيراد | `operating_finance_os` |
| `docs/32_enterprise_readiness` | **BU4 — باقة ثقة مبدئية** | Data Room مصغّر + ملخصات | 9,999–24,999 | 2–4 أسابيع | ليس SOC2 كامل | [`auto_client_acquisition/trust_os/`](../../auto_client_acquisition/trust_os/) + `auditability_os` |
| `docs/33_enterprise_rollout` | خطة Land→Expand | خارطة أقسام + بوابات | 15,000+ | 4–8 أسابيع | لا تشغيل كامل بدون Proof | `enterprise_rollout` وثائق |
| `docs/34_ai_estate` | جرد AI + Shadow risk | سجل استخدامات + مخاطر | 4,999–9,999 | أسبوعين | لا تدريب نماذج | [`auto_client_acquisition/ai_estate_os/`](../../auto_client_acquisition/ai_estate_os/) |
| `docs/35_agent_iam` | سياسة هوية الوكيل | بطاقة وكيل + صلاحيات MVP | مضمن BU4 أو 4,999 | أسبوع | لا SSO مؤسسي كامل | [`auto_client_acquisition/agent_os/`](../../auto_client_acquisition/agent_os/) |
| `docs/36_agent_runtime_security` | أربع حدود تشغيل | سياسات حدود أدوات/سياق | مضمن BU4 | أسبوعين | لا pentest خارجي | [`auto_client_acquisition/secure_agent_runtime_os/`](../../auto_client_acquisition/secure_agent_runtime_os/) |
| `docs/37_saudi_layer` | طبقة سوق سعودية | قطاعات + PDPL لغة | 2,999 مدمج أو منفصل | أسبوع | لا استشارة قانونية ملزمة | [`auto_client_acquisition/saudi_layer/`](../../auto_client_acquisition/saudi_layer/) |
| `docs/38_standards` | حزمة معايير تشغيل | Checklist امتثال داخلي | ترخيص IP (انظر مسار الترخيص) | — | ليس شهادة جهة خارجية | [`docs/23_standards/`](../23_standards/) (مرآة تشغيلية) |
| `docs/39_academy` | مسار شريك/تشغيل | مسارات تدريب مقيدة | شراكة/رسوم أكاديمية | ربع سنوي | لا شهادة حكومية | `docs/39_academy` |
| `docs/40_partners` | برنامج شركاء | Covenant + Enablement | عقد منفصل | سنوي | لا وكالة إرسال جماعي | [`PARTNER_COVENANT`](../40_partners/PARTNER_COVENANT.md) |
| `docs/41_benchmarks` | تقرير مرجعية سوق | Benchmark PDF داخلي | 4,999–12,000 | أسبوعين | لا بيانات حساسة عميل | `benchmark_os` |
| `docs/42_market_power` | لغة فئة + inbound | لوحة إشارات فئة | 4,999+ | شهر | لا إعلان مدفوع | `market_power_os` |
| `docs/43_business_units` | خريطة وحدات القابضة | BU charter داخلي | — | — | لا استثمار خارجي | `docs/43_business_units` |
| `docs/44_ventures` | بوابة Spin-out | معايير + Gate | رسوم استشارية | مشروع | لا التزام تمويل | `docs/44_ventures` |

## ربط سريع بالموجات التجارية

- **BU1 — Sprint ذكاء إيرادات:** `docs/26` + `docs/27` + [`revenue_intelligence`](../../api/routers/revenue_intelligence.py).
- **BU2 — Data Readiness:** `docs/26` (DATA_READINESS) + [`data_os`](../../api/routers/data_os.py).
- **BU3 — Retainer RevOps:** `docs/26` (MONTHLY_*) + [`wave2_client_ops`](../../api/routers/wave2_client_ops.py) + `client_os/monthly_value_report.py`.
- **BU4 — Trust Enterprise:** `docs/32`–`docs/36` كحزمة واحدة قابلة للبيع بعد **بوابة التفعيل** (انظر [BU4_TRUST_ACTIVATION_GATE_AR.md](../enterprise_trust/BU4_TRUST_ACTIVATION_GATE_AR.md)).

## قاعدة القابضة

كل صف في الجدول يجب أن يُرفق في العقد بـ: **مخرج ملموس، حدود، سعر، مدة، مستبعد** — وإلا يُصنَّف كبحث داخلي وليس إيراداً.
