# Dealix — مركز الاستراتيجية التجارية

**كتاب تشغيل تجاري يومي للمؤسس** — تموضع، سلم قيمة، GTM، توسيع، قطاعات، North Star.

- **واجهة:** `/ar/business-now` (قسم الاستراتيجية)
- **API:** `GET /api/v1/business-now/commercial-strategy` · `POST /api/v1/business-now/commercial-strategy/simulate`
- **تحديث:** `bash scripts/run_business_now.sh` (يشمل توليد هذا الملف)
- **تعديل تركيز يدوي:** `dealix/transformation/commercial_focus_override.yaml`

### أدوات المؤسس في الواجهة

في `/ar/business-now#strategy`: توصية قطاع، توصية خطة، محاكاة، GTM أول 10، سكربت مبيعات، Proof demo، anti-waste.

**حزمة Ops Client:** [ops_client_pack/](../commercial/ops_client_pack/) — Runbook + `dealix_ops_sales_kit_ar.pptx`

---

## 1) تموضع وتمييز

Dealix **Revenue OS محكوم** — ليس CRM عاماً:

- مسودات + موافقة قبل أي إرسال خارجي
- Decision Passport و Proof Pack قبل التوسع
- ذاكرة إيرادات وامتثال PDPL مدمجان

مرجع: [DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) · [COMPETITIVE_POSITIONING.md](../COMPETITIVE_POSITIONING.md)

---

## 2) سلم القيمة (10 طبقات → 7 عروض Dealix)

| طبقة | عروض Dealix |
| --- | --- |
| تعليم / تشخيص | `free_mini_diagnostic` |
| Sprint / حزمة بيانات | `revenue_proof_sprint_499` · `data_to_revenue_pack_1500` |
| Retainer | `growth_ops_monthly_2999` · `support_os_addon_1500` |
| قيادة / شريك | `executive_command_center_7500` · `agency_partner_os` |

تفصيل: [VALUE_CAPTURE_LADDER.md](../value_capture/VALUE_CAPTURE_LADDER.md)

---

## 3) تركيز الأسبوع

يُحدَّد حتمياً من حالة المنصة وKPIs — انظر اللقطة الآلية أدناه.

---

## 4) GTM — أول 10 ثم 100

- **أول 10:** قائمة دافئة، إحالات، demo بـ Command Center — [GTM_PLAYBOOK.md](../GTM_PLAYBOOK.md)
- **أول 100:** محتوى مؤسس، شركاء، إحالات — نفس الكتاب
- **سلّم خدمات:** [GTM_PLAYBOOK_SERVICE_LADDER_AR.md](../strategic/GTM_PLAYBOOK_SERVICE_LADDER_AR.md)

---

## 5) قنوات وشركاء

- **أساسي:** مبيعات بقيادة المؤسس + شركاء
- **ثانوي:** مجتمع واتساب opt-in فقط
- **تجنّب:** واتساب بارد، قوائم مكشوفة بدون امتثال

---

## 6) توسيع و Upsell (من Proof)

إشارة Proof → عرض مقترح (قراءة فقط في API — لا تنفيذ تلقائي).

---

## 7) قطاعات سعودية أولوية

عيادات · عقار · لوجستيات · تدريب · وكالات · B2B SaaS — زوايا رسالة في API `/commercial-strategy`.

---

## 8) North Star

مرجع جدول: [NORTH_STAR_METRICS_AR.md](../commercial/NORTH_STAR_METRICS_AR.md)

---

## 9) اقتصاديات الوحدة

أرقام demo في API موسومة `is_estimate` — ليست إيراداً فعلياً من CRM.

---

## 10) حواجز Dealix (لا تفاوض)

- لا واتساب بارد · لا LinkedIn تلقائي
- لا إرسال Gmail خارجي بدون موافقة
- لا أرقام CRM مختلقة في الأتمتة
- Moyasar live — بوابة وثائقية فقط

---

<!-- AUTO_GENERATED_START -->
# Commercial strategy snapshot — 2026-08-31

## Focus
- stage: pilot_execution
- primary_offer_id: revenue_command_pilot_30d
- rationale: بايلوتات جاهزة للقالب — ركّز على Revenue Command Pilot لمدة 30 يوماً + PILOT_EXECUTION_RUNBOOK

## Offers
- free_mini_diagnostic: None SAR — اكتمال النموذج خلال 24 ساعة + جواز قرار أولي
- revenue_command_pilot_30d: None SAR — خط أساس موثق + هدف تشغيلي مقاس + Proof Pack خلال 30 يوماً
- data_to_revenue_pack_1500: None SAR — ≥20 فرصة معتمدة + تقرير مخاطر بيانات
- growth_ops_monthly_2999: None SAR — موجز أسبوعي + تحسين معدل رد على المسودات
- support_os_addon_1500: None SAR — SLA أول رد + تصنيف تذاكر
- executive_command_center_7500: None SAR — موجز يومي + board pack شهري
- agency_partner_os: None SAR — إحالة مدفوعة واحدة على الأقل / ربع
- ai_command_center_os: None SAR — نلتزم بإطلاق رؤية يومية موحّدة للإدارة خلال مدة الإعداد. الأسعار نطاقات تقديرية تُحدَّد بعد جلسة تشخيص مدفوعة.
- whatsapp_revenue_os: None SAR — نلتزم بتحويل واتساب إلى pipeline قابل للقياس خلال مدة الإعداد. كل رسالة خارجية مسودة تتطلب موافقة — لا إرسال بارد ولا أتمتة.
- brand_intelligence_os: None SAR — نلتزم بتسليم نظام هوية موحّد قابل لإعادة الاستخدام خلال مدة الإعداد. الأسعار نطاقات تقديرية.
- ai_agent_workforce_os: None SAR — نلتزم بنشر وكلاء بأدوار وحدود وصلاحيات واضحة ومراجعة بشرية للإجراءات الحساسة. لا تنفيذ خارجي تلقائي. الأسعار نطاقات تقديرية.
- client_experience_os: None SAR — نلتزم بتوحيد رحلة العميل من أول تواصل إلى إعادة الشراء خلال مدة الإعداد. الأسعار نطاقات تقديرية.
- operations_automation_os: None SAR — نلتزم بأتمتة العمليات المتكررة بحوكمة وتنبيهات ولوحات خلال مدة الإعداد. نُخرِّط أولاً ثم نؤتمت — لا نؤتمت الفوضى. الأسعار نطاقات تقديرية.
- executive_reporting_os: None SAR — نلتزم بتحويل بيانات التشغيل إلى تقارير تنفيذية أسبوعية وشهرية تربط بالقرار خلال مدة الإعداد. الأسعار نطاقات تقديرية.
- trust_governance_os: None SAR — نلتزم ببناء حوكمة عملية للذكاء الاصطناعي والبيانات متوائمة مع PDPL وإدارة المخاطر، قابلة للتطبيق التشغيلي. الأسعار نطاقات تقديرية.
- growth_engine_os: None SAR — نلتزم ببناء آلة نمو قابلة للتكرار عبر مسودات معتمدة فقط. لا واتساب بارد ولا أتمتة LinkedIn ولا إرسال جماعي ولا scraping. الأسعار نطاقات تقديرية.
- custom_enterprise_system: None SAR — نلتزم ببناء نظام تشغيل مخصص حول عمليات الشركة وبياناتها وفريقها، يبدأ بجلسة تشخيص مدفوعة. النطاق ٠٠٠ر١٠٠–٠٠٠ر٥٠٠+ تقديري يُحدَّد بالعقد.

## Weekly motions
- sun: راجع لقطة Business NOW + KPIs التجارية المعلّقة
- mon: حدّث قائمة دافئة (~30) — مسودات فقط
- tue: POST /api/v1/leads لاختبار مسار intake
- wed: anti-waste قبل أي رسالة خارجية
- thu: راجع موافقات اليوم — لا إرسال بدون جواز
- fri: Proof / تقرير أسبوعي للعميل النشط
- sat: شغّل run_business_now.sh + حدّث cache

## Guardrails
- لا واتساب بارد ولا LinkedIn تلقائي
- لا إرسال خارجي بدون موافقة صريحة
- شغّل anti-waste قبل أي حملة أو رسالة خارجية
- لا upsell بدون Proof Pack أو دليل L3+
- لا أرقام CRM في الأتمتة — عبّئ kpi_founder_commercial_import.yaml يدوياً

<!-- AUTO_GENERATED_END -->
