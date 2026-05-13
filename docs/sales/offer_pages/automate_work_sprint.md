# أتمتة عمل في 7 أيام / Automate Work Sprint
## AI Quick Win Sprint — Customer-Facing Offer Page

---

## المشكلة / The Problem

**AR:** عندك عملية واحدة على الأقل تأكل ساعات أسبوعيًا من أهم الناس في فريقك. ربما تقرير CEO الأسبوعي، توزيع leads، فرز tickets، إعداد عروض أسعار، تلخيص واتساب العمل. تحاول AI شات بوت العام، لكن إجاباته غير موثوقة، بدون مراجعة، وبدون audit log. الفِرق ترفض الاعتماد عليه.

**EN:** Your team has at least one recurring process eating hours every week — weekly CEO report, lead routing, ticket triage, proposal drafts, WhatsApp summaries. You tried generic AI chat, but answers were unreliable, unreviewed, and unauditable. Your team won't trust it.

---

## الوعد / The Promise

**AR:** خلال **7 أيام عمل**، نُؤتمت **عملية واحدة** عندك بـ:
- **بوابة موافقة بشرية** قبل كل إرسال أو إجراء.
- **سجل تدقيق كامل** لكل خطوة في `event_store`.
- **توثيق Runbook** يستطيع أي شخص في فريقك تشغيله.
- **قياس ROI الفعلي** بأرقام مُحقَّقة بعد 30 يومًا من التشغيل.

**EN:** In **7 business days**, we automate **one** painful process with:
- **Human approval gate** before every send/action.
- **Full audit log** of every step in `event_store`.
- **Runbook documentation** any team member can operate.
- **Verified ROI** with measured numbers after 30 days of live use.

---

## Use Cases الجاهزة / Curated Use Cases (Pick ONE on Day 1)

| # | العملية المؤتمتة | الوقت قبل | الوقت بعد (متوسط) |
|---|---|---|---|
| 1 | تقرير CEO/المبيعات/العمليات الأسبوعي | 6h/week | 1h/week |
| 2 | توزيع Leads بين المندوبين | 4h/week | 25min/week |
| 3 | فرز Tickets الدعم | 4h/day | 30min/day |
| 4 | مولّد عرض السعر الأولي | 2h/proposal | 15min/proposal |
| 5 | تلخيص Inbox / WhatsApp Business | 5h/week | 40min/week |

> اختر **واحد فقط** في اليوم الأول. (السقف ثابت — نفعّل الأتمتة بعمق، لا بعرض.)

---

## ما تستلمه / What You Receive

| البند | التفاصيل |
|---|---|
| 1. أتمتة حيّة في بيئتك | تعمل من اليوم 7، Cron أو event-triggered |
| 2. بوابة موافقة بشرية | إلزامية على كل خطوة تلمس بيانات حساسة أو خارجية |
| 3. سجل تدقيق كامل | event_store + retention 365 يوم |
| 4. Runbook ≥ 3 صفحات | كيفية التشغيل، المراقبة، الاستعادة عند الفشل |
| 5. جلسة تدريب 60 دقيقة (مسجّلة) | تشمل scenarios للحالات الاستثنائية |
| 6. ROI baseline | قبل/بعد، hours/errors/cycle-time، بأرقام موثَّقة |
| 7. حزمة إثبات | لإعادة استخدامها داخليًا أو مع المجلس |

---

## السعر والشروط / Price & Terms

| البند | القيمة |
|---|---|
| **السعر الثابت / Fixed price** | **SAR 12,000** (ضريبة قيمة مضافة 15% خارج السعر) |
| **المدة / Timeline** | 7 أيام عمل |
| **الدفع / Payment** | Net 14، 100% عند التسليم |
| **عقد / Contract** | SOW جاهز للتوقيع — 5 صفحات |
| **ضمان / Guarantee** | إن لم نحقق **خفض زمن ≥ 50%** على العملية المختارة، نُعيد 50% من الرسوم |

---

## غير مشمول (Not Included)

- **لا نُرسل أي شيء بدون موافقة بشرية صريحة.** هذه قاعدة منتجة (product rule).
- لا تكامل CRM مخصص مع نظام لم نختبره من قبل (نقدر نستكشف، لكن خارج Sprint).
- لا نضمن "زيادة مبيعات" أو "تخفيض موظفين" — نضمن خفض زمن العملية بأرقام موثقة فقط.
- لا نؤتمت أكثر من use case واحد ضمن 7 أيام (تكتفي بعمل واحد متقن).
- لا نتعامل مع بيانات صحية مرضية (PDPL Art. 27) ضمن هذا Sprint — متاحة في Company Brain Sprint.

---

## مناسب لـ / Best For

- مديري عمليات (COO/Head of Ops) محبَطون من مهام أسبوعية متكررة.
- فرق المالية/المبيعات يفقدون ساعات بسبب تقارير دورية.
- شركات مرَّبة عبر AI شات عام لكنها فقدت الثقة بسبب غياب المراجعة.
- مَن يريد **يبدأ صغيرًا** قبل التزام بمشروع AI كبير.

---

## كيف تبدو النتيجة / What the Output Looks Like

> "تقرير CEO الأسبوعي الآن يأخذ ساعة بدلًا من 6 ساعات، بتغطية audit log كاملة 100%."

شاهد نموذج تقرير تنفيذي (بيانات اصطناعية لعميل لوجستيات): `docs/services/ai_quick_win_sprint/sample_output.md`

---

## ضمانات الحوكمة / Governance Guarantees

| البند | القيمة |
|---|---|
| موافقة بشرية قبل أي إرسال خارجي | 100% (بدون استثناء) |
| تغطية event_store | 100% من الأحداث مُسجَّلة |
| Pydantic schema validation | على كل output |
| Forbidden claims auto-check | يمر بـ `forbidden_claims.py` |
| PII auto-redaction | 100% (`pii_detector.py`) |
| PDPL Art. 13/14 footers | على outputs خارجية |
| Rollback في 5 دقائق | عند أي خطأ تشغيلي |

---

## مسار الترقية / Upgrade Path

بعد Sprint، تختار:

1. **Workflow Automation Sprint** — use case ثاني بسعر SAR 12,000 آخر.
2. **Monthly AI Ops Retainer** بسعر **SAR 9,500/شهريًا** — صيانة + 1 use case جديد/ربع + 4 ساعات استشارة شهريًا.
3. **Both (الأفضل قيمةً)** — خصم 5%.

---

## خطوة البدء / Call to Action

**AR:** جلسة 30 دقيقة لاختيار الـ use case الأنسب لك من القائمة الخمس. لا التزام. رد بكلمة **"ابدأ"** على أي بريد من Dealix، أو احجز موعد مباشر.

**EN:** A 30-minute call to pick the right use case from the curated five. No commitment. Reply **"start"** to any Dealix email, or book directly.

> **احجز جلستك / Book your slot:** [calendly.com/dealix/automate-work-sprint](#)
> **أو راسلنا / Or email:** sales@dealix.me

---

## روابط ذات صلة / Related links

- [نموذج تقرير تنفيذي / Sample executive report](../../services/ai_quick_win_sprint/sample_output.md)
- [نطاق الخدمة / Scope](../../services/ai_quick_win_sprint/scope.md)
- [قائمة التحقق التشغيلي / QA checklist](../../services/ai_quick_win_sprint/qa_checklist.md)
- [حزمة الإثبات / Proof pack template](../../services/ai_quick_win_sprint/proof_pack_template.md)
- [سيناريو المبيعات / Sales script](../sales_script.md)
- [إجابات الاعتراضات / Objection handling](../objection_handling.md)

---

*Dealix · sales@dealix.me · `service_id: ai_quick_win_sprint` · SAR 12,000 · 7 أيام عمل*
