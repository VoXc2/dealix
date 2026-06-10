# مكتبة أداء الرسائل — Message Performance Library

> **خمسة قوالب رسائل أساسية**، مُعايَرة بالقطاع السعودي، مع إشارات أداء
> (open / reply / positive / meeting) ومعاملات تخصيص لكل قطاع.

**الحالة:** Phase 1 من Agent #31  
**التاريخ:** 2026-06-03  
**الإصدار:** v1.0  
**Schema:** `schemas/message_performance.schema.json`  
**البيانات:** `data/data_products/message_performance.jsonl`

---

## 1. النماذج الخمسة (5 Archetypes)

| # | القالب | الهدف | متى يُستخدم |
| - | --- | --- | --- |
| 1 | **Opener** | أول تواصل بارد | ضمن 0–3 أيام من بحث lead |
| 2 | **Follow-up** | تذكير بعد رد أو فتح | بعد 3–7 أيام |
| 3 | **Reactivation** | إعادة تواصل مع lead بارد | بعد 30+ يوم صمت |
| 4 | **Referral Ask** | طلب إحالة من عميل/شريك | بعد علاقة مُثبتة (week 2+) |
| 5 | **Executive Summary** | ملخص تنفيذي للمدير | بعد warm contact أو referral |

---

## 2. القالب 1 — Opener (الافتتاحية)

- **Subject pattern (AR):** `ملاحظة سريعة بخصوص [وحدة العمل]`
- **Hook:** `لاحظت [إشارة تشغيلية] في [دورتك]، وفكرة بسيطة قلّلت [المشكلة] عند شركات مشابهة.`
- **Body structure (5 أقسام):**
  1. تمهيد شخصي قصير (≤ 12 كلمة).
  2. الإشارة المرصودة (1 جملة).
  3. نتيجة قابلة للقياس (1 جملة).
  4. سؤال صغير (1 جملة).
  5. CTA واحد فقط.
- **CTA options:** `15 دقيقة الأسبوع القادم؟` · `أرسل لك ورقة ROI؟`
- **Length range:** 60–110 كلمة.
- **Tone:** consultative (افتراضي) أو semi_formal لـ D2C.
- **الأداء المرجعي (industrial, observed):** open 42% / reply 18% / positive 7% / meeting 45%.

---

## 3. القالب 2 — Follow-up (المتابعة)

- **Subject pattern (AR):** `متابعة سريعة – [الاسم المستعار]`
- **Hook:** `بدون ما أطوّل، هذي ٣ أفكار قابلة للتطبيق على [السياق] الآن.`
- **Body structure:**
  1. اعتراف بالوقت.
  2. ثلاث نقاط قيمة مختصرة.
  3. CTA خفيف.
- **CTA options:** `تجربة على عميل واحد هذا الشهر؟` · `15 دقيقة لمقارنة؟`
- **Length range:** 80–150 كلمة.
- **الأداء (professional_services, observed):** open 60% / reply 34% / positive 16% / meeting 70%.

---

## 4. القالب 3 — Reactivation (إعادة التفعيل)

- **Subject pattern (AR):** `مرحباً من جديد – [القطاع]`
- **Hook:** `من آخر تواصل، صار عندي [تحديث محدد] يستاهل ٣ دقائق.`
- **Body structure:**
  1. اعتراف بالمسافة الزمنية.
  2. تحديث جديد (ليس نفس pitch).
  3. عرض صغير.
  4. CTA.
- **CTA options:** `أرسل لك المثال في 3 دقايق؟`
- **Length range:** 70–120 كلمة.
- **الشرط:** يعمل فقط إذا كان التحديث حقيقياً، ليس ملفقاً.
- **الأداء (healthcare, assumption):** open 48% / reply 18% / positive 7% / meeting 50%.

---

## 5. القالب 4 — Referral Ask (طلب الإحالة)

- **Subject pattern (AR):** `طلب صغير – [القطاع]`
- **Hook:** `أبحث عن [نوع العميل] يشبه [شركة شبيهة]. عندك اسم واحد في بالك؟`
- **Body structure:**
  1. تمهيد سريع (≤ 10 كلمات).
  2. طلب واضح ومحدد.
  3. مقابل مذكور (هدية، ميزة، شكر).
  4. CTA.
- **CTA options:** `أقدر أرسل لك هدية رمزية مقابل اسم واحد؟`
- **Length range:** 50–100 كلمة.
- **الشرط:** فقط بعد trust مُثبت (أسبوع 2+ من العلاقة).
- **الأداء (professional_services, observed):** open 62% / reply 28% / positive 18% / meeting 65%.

---

## 6. القالب 5 — Executive Summary (الملخص التنفيذي)

- **Subject pattern (AR):** `ملخص تنفيذي – [القطاع]`
- **Hook:** `ملخص 90 ثانية لأربع ملاحظات من قطاع [القطاع] في الربع الأخير.`
- **Body structure:**
  1. تمهيد.
  2. أربع نقاط مع رقم واحد لكل نقطة.
  3. نتيجة.
  4. CTA.
- **CTA options:** `أرسل لك النسخة الكاملة؟` · `اجتماع 20 دقيقة هذا الأسبوع؟`
- **Length range:** 120–220 كلمة.
- **Tone:** formal.
- **الشرط:** لا يُستخدم كـ opener. فقط بعد warm contact أو referral.
- **الأداء (industrial, observed):** open 45% / reply 20% / positive 10% / meeting 55%.

---

## 7. تعديلات حسب القطاع (Sector Adjustments)

| القطاع | Tone | Length cap | CTA مفضّل |
| --- | --- | --- | --- |
| industrial | consultative → formal | 110 | roi_calculator |
| healthcare | consultative | 130 | diagnostic_offer |
| retail | semi_formal | 100 | short_audit_call |
| professional_services | semi_formal | 150 | case_study_link |
| real_estate | formal | 170 | sample_workflow |
| fnb | consultative | 100 | short_audit_call |
| logistics | formal | 130 | roi_calculator |
| education | formal | 130 | executive_summary |

---

## 8. Tone Guide

- **formal**: مخاطبة رسمية، تحية كاملة، توقيع رسمي. مناسب industrial/government.
- **semi_formal**: تحية مختصرة، نبرة ودية. مناسب D2C, agency.
- **consultative**: نبرة استشاري زميل. مناسب healthcare, services.

اللغة الأساسية **AR**، خلط EN مقبول للأسماء العلمية (CRM, AI, ROI).

---

## 9. إشارات الأداء (Performance Signals)

- **Open rate < 25%** → راجع subject line.
- **Reply rate < 8%** → راجع hook أو استهدف قطاع آخر.
- **Positive reply < 4%** → CTA ضعيف أو timing خاطئ.
- **Meeting conversion < 30%** → discovery call ضعيف، ليس الرسالة.
- **Sample size < 30** → أعد الحساب قبل تعميم.

---

## 10. المراجع (References)

- `schemas/message_performance.schema.json`
- `data/data_products/message_performance.jsonl`
- `docs/SECTOR_BENCHMARKS_AR.md`
- `docs/OBJECTION_INTELLIGENCE_AR.md`
- `data/templates/` — قوالب رسائل AR/EN
- `data/analytics/funnel_events.jsonl`
