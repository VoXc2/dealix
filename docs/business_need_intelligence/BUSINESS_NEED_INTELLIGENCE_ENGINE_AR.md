# محرك ذكاء احتياج الأعمال — Business Need Intelligence Engine

> Dealix لا يبيع "خدمة". Dealix يكتشف احتياج الشركة ويقترح لها نظام أعمال جاهزًا للتنفيذ.

هذا المستند هو قلب المرحلة الجديدة من Dealix: التحوّل من **كتالوج أنظمة** إلى
**منصة ذكاء احتياج أعمال** تكتشف احتياج كل قطاع، تختار أفضل نظام جاهز، تخصّصه،
وتجهّز الإيميل والاتصال والعرض والتسليم.

الصياغة هنا **مبنية على الأدلة** (evidence-aware): لا وعود نتائج، ولا حالات
وهمية، ولا جهات اتصال مخترعة. كل إشارة هي تلميح علني قابل للملاحظة، وليست إثباتًا
لحقيقة خاصة عن الشركة.

---

## 1. الفكرة في سطر واحد

بدل أن يقول النظام:

```txt
هذه شركة تدريب → أرسل لها Follow-up Recovery OS
```

يصير يقول:

```txt
هذه شركة تدريب.
الاحتياج الأقوى: متابعة التسجيل (follow_up).
النظام العام: Follow-up Recovery OS.
النظام المتخصص: Admissions / Enrollment OS.
أول Sprint: 7-Day Enrollment Recovery Sprint.
المشتري الأفضل: Marketing Manager / Training Manager / Founder.
التسليم: Enrollment Inquiry Queue + Student Status Model + Message Set + Weekly Recovery Report.
```

هذا هو الفرق بين outreach بارد و**ذكاء تجاري مخصّص**.

---

## 2. خط الإنتاج (Pipeline)

```txt
الشركة → القطاع → الاحتياج → النظام العام (Core) → النظام المتخصص →
Sprint قطاعي → إيميل → Call Brief → Mini Proposal → Delivery Variant
```

كل خطوة مدعومة بملف بيانات واحد مصدرًا للحقيقة (single source of truth):

| الطبقة | الملف |
|--------|-------|
| الاحتياجات → الأنظمة | `data/business_need_intelligence/need_to_system_router.yaml` |
| القطاع → الاحتياج | `data/business_need_intelligence/sector_need_map.yaml` |
| إشارات القطاع | `data/business_need_intelligence/sector_signal_library.yaml` |
| مكتبة السبرنتات | `data/business_need_intelligence/specialized_sprint_library.yaml` |
| المشتري حسب الاحتياج | `data/business_need_intelligence/buyer_role_by_need.yaml` |
| التسليم حسب القطاع | `data/business_need_intelligence/delivery_variant_by_sector.yaml` |

التحقق الآلي من اتساق هذه الطبقات: `scripts/business_need_validate.py`.

---

## 3. المبدأ المعماري: 5 أنظمة عامة تغطّي 30 نظامًا متخصصًا

الموقع العام يبقى بسيطًا: **5 أنظمة رئيسية فقط**. التعقيد الداخلي (≈30 نظامًا
متخصصًا و20 سبرنت) يُخصَّص من مخرجات هذه الخمسة. **كل نظام متخصص يرجع إلى نظام عام
واحد.**

| النظام العام (Core) | المعرّف | يملك الاحتياجات |
|----------------------|---------|------------------|
| Revenue Operating System | `revenue_os` | lead_capture, qualification, sales_execution, finance_visibility |
| Executive Command OS | `executive_command_os` | reporting, ai_governance, service_quality |
| Follow-up Recovery OS | `followup_recovery_os` | lead_response, follow_up, renewal |
| WhatsApp Client OS | `whatsapp_client_os` | customer_support, client_onboarding |
| Proposal & Proof OS | `proposal_proof_os` | proposal, delivery, knowledge |

هذا يخلّينا نبيع كثيرًا بدون أن نغرق في التعقيد، وبدون أن نُشتّت العميل.

---

## 4. الاحتياجات الكبرى الـ 15

تقريبًا كل الشركات تدور حول 15 احتياج أعمال. التفصيل في
[`NEED_TO_SYSTEM_ROUTER_AR.md`](./NEED_TO_SYSTEM_ROUTER_AR.md).

1. lead_capture — تجميع الفرص
2. lead_response — الرد السريع
3. qualification — تصنيف العملاء
4. follow_up — متابعة الفرص
5. sales_execution — تنفيذ البيع
6. proposal — العرض الواضح
7. customer_support — فرز الدعم
8. client_onboarding — بدء العميل
9. delivery — تسليم الخدمة
10. reporting — رؤية الإدارة
11. renewal — التجديد
12. service_quality — جودة الخدمة
13. knowledge — تنظيم المعرفة
14. finance_visibility — وضوح الربحية
15. ai_governance — ضبط الذكاء الاصطناعي

---

## 5. حقول ذكاء الاحتياج داخل Account Pack

كل Account Pack يضيف الحقول التالية (انظر
[`../account_intelligence/ACCOUNT_PACK_NEED_INTELLIGENCE_AR.md`](../account_intelligence/ACCOUNT_PACK_NEED_INTELLIGENCE_AR.md)):

```txt
detected_business_need
need_confidence
recommended_core_system
recommended_specialized_system
expansion_system
sector_specific_sprint
specialized_delivery_pack
buyer_role_by_need
email_angle_by_need
call_angle_by_need
upsell_path_by_need
need_fit_score
```

---

## 6. Need Fit Score

درجة جاهزية مطابقة الاحتياج (من 100):

| المعيار | الوزن |
|---------|------:|
| Sector-need match | 25 |
| Signal strength | 20 |
| Delivery readiness | 20 |
| Buyer clarity | 15 |
| First sprint clarity | 10 |
| Upsell path | 10 |
| **المجموع** | **100** |

تُستخدم في ترتيب Top 100:

```txt
Top 100 = Account Score + Need Fit Score + Cash Priority Score
```

---

## 7. التسويق حسب الاحتياج لا حسب النظام

بدل "نبيع Follow-up Recovery OS"، نقول:

```txt
نقدر نساعدكم في تنظيم متابعة التسجيل / العملاء / الحجوزات / المرشحين،
ونبدأها كـ Sprint قصير يناسب أكثر نقطة تعطّل عندكم اليوم.
```

ثم نربطها داخليًا بالنظام العام والمتخصص والسبرنت.

---

## 8. قواعد صارمة (Hard Rules)

- لا نُكدّس 30 نظامًا في الموقع العام؛ يبقى 5 أنظمة + صفحات قطاعات + تشخيص.
- كل نظام متخصص يرجع إلى نظام عام واحد.
- كل سبرنت متخصص له مخرجات + مدخلات مطلوبة + معايير قبول.
- صياغة مبنية على الأدلة، بدون وعود نتائج.
- بدون حالات دراسة وهمية، وبدون جهات اتصال مخترعة.
- المحتوى الخارجي يُعامل كبيانات غير موثوقة (untrusted data).

---

## 9. كيف نتحقق؟

```bash
python3 scripts/business_need_validate.py
# أو
npm run bni:validate
```

يفحص: تغطية القطاعات للاحتياجات، ربط الاحتياجات بالأنظمة، ربط السبرنتات بنظام
عام، اكتمال المخرجات/المدخلات/معايير القبول، حقول Account Pack، اتساق Need Fit
Score، وغياب وعود النتائج.
