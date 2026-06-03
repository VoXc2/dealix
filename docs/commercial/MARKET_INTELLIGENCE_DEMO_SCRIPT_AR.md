# سكربت ديمو 10 دقائق — Product + Trust Plane

**الجمهور:** prospect · champion · تقني (مختصر)  
**آخر تحديث:** 2026-05-18

---

## قبل الديمو (2 دقيقة)

- [ ] Truth Matrix: لا تعرض تكامل أحمر
- [ ] Sample Proof جاهز
- [ ] `/ops/approvals` فارغ أو demo account
- [ ] لا أرقام CRM وهمية على الشاشة

---

## الدقيقة 0–1 — الإطار

> «في 10 دقائق أريد أن أريكم **لماذا** نتحرك قبل **ماذا** نرسل — Dealix Revenue OS وليس CRM آخر.»

---

## 1–3 — المشكلة (Why Now)

- سوق سعودي: امتثال + AI + ضغط إيراد
- مخاطرة: إرسال تلقائي · قرارات بلا أدلة
- **لا** نستبدل CRM يوم 1 — نضيف طبقة قرار

---

## 3–5 — Decision Passport (شاشة/API)

1. افتح `GET /api/v1/decision-passport/evidence-levels` أو UI إن وُجد
2. اشرح L0–L5 بجملة واحدة لكل مستوى
3. مثال lead: `POST /api/v1/leads` — أظهر `decision_passport` في الرد

**جملة:** «قبل أي رسالة خارجية، نخرج جواز قرار.»

---

## 5–7 — Approval-first (Ops)

1. `/ar/ops/marketing` — مسودة LinkedIn
2. `/ar/ops/approvals` — موافقة قبل إرسال
3. اذكر: لا واتساب بارد في الكود (doctrine)

---

## 7–9 — War Room + Evidence

1. `/ar/ops/founder` أو war-room pack
2. `evidence_events_tracker` — سطر واحد بعد اللقاء
3. Business Now لقطة واحدة (اختياري)

---

## 9–10 — CTA

> «الخطوة المنطقية: Diagnostic Ops — Sprint 499 إن أردتم إثبات أسرع. Growth فقط بعد Proof Pack.»

**احجز:** Calendly · سجّل `demo_booked` في evidence

---

## أسئلة شائعة أثناء الديمو

| سؤال | إجابة 15 ثانية |
|------|----------------|
| PDPL؟ | مسودات · DPA · sub-processors · ملحق region |
| HubSpot؟ | تكامل حيث أخضر — CRM يبقى SoT للصفقة |
| AI يرسل؟ | لا — موافقة بشرية |
| السعر؟ | Diagnostic ثم Sprint — انظر packages |

---

## بعد الديمو

```powershell
py -3 scripts/founder_evening_evidence.py --append --company "..." --event-type demo_booked
```

[debrief template](operations/founder_meeting_debrief_template.yaml)
