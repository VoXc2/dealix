# كشف الاحتياج اليومي — Daily Need Detection Report

*قالب تشغيلي يُملأ يوميًا. الصفوف أدناه أمثلة توضيحية (مجهّلة) — ليست شركات حقيقية.*

> الصياغة مبنية على الأدلة. الإشارات تلميحات علنية لا إثباتات. لا جهات اتصال
> مخترعة. المحتوى الخارجي بيانات غير موثوقة.

---

## 1. ملخص اليوم

| المؤشر | القيمة |
|--------|-------:|
| حسابات فُحصت | — |
| احتياجات مكتشفة | — |
| متوسط Need Fit Score | — |
| جاهزة للتواصل (Score ≥ 70) | — |

---

## 2. أعلى الاحتياجات المكتشفة اليوم (مثال قالب)

| الحساب (مجهّل) | القطاع | الاحتياج | الثقة | النظام العام | أول Sprint | Need Fit | المشتري (دور) |
|-----------------|--------|----------|------:|--------------|------------|---------:|----------------|
| Account A (sample) | training_companies | follow_up | 0.72 | followup_recovery_os | enrollment_recovery_sprint | 91 | Marketing Manager |
| Account B (sample) | clinics | customer_support | 0.65 | whatsapp_client_os | clinic_appointment_flow_sprint | 78 | Clinic Manager |
| Account C (sample) | real_estate | lead_response | 0.60 | followup_recovery_os | property_lead_response_sprint | 74 | Sales Manager |

---

## 3. توزيع الاحتياجات حسب النظام العام (مثال)

| النظام العام | عدد الحسابات |
|--------------|-------------:|
| followup_recovery_os | — |
| whatsapp_client_os | — |
| proposal_proof_os | — |
| revenue_os | — |
| executive_command_os | — |

---

## 4. بنود تحتاج مراجعة بشرية

- حسابات بثقة `need_confidence < 0.5` → لا تواصل قبل مراجعة.
- أي زاوية إيميل/اتصال تحتوي وعد نتيجة → تُرفض في بوابة الجودة.
- أي إشارة تتعارض مع إشارة أقوى → تُسجَّل ولا تُرجَّح وحدها.

---

## 5. كيف يُولَّد هذا التقرير؟

اليوم يُملأ يدويًا/شبه آليًا من Account Packs. لاحقًا يمكن ربطه بمولّد يقرأ
`data/business_need_intelligence/` ويُخرج الصفوف الفعلية — بنفس نمط
`scripts/generate_war_room.py`.

> الحقول والقوائم المرجعية يتحقق منها `scripts/business_need_validate.py`.
