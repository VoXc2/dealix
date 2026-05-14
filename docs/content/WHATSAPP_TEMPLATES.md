# WhatsApp Templates — قوالب واتساب

> Bilingual AR + EN. Voice-note-friendly drafts for the canonical Dealix customer journey. AR primary, EN secondary. No emojis. No model names.
>
> Cross-link: [docs/00_constitution/NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md), [auto_client_acquisition/whatsapp_safe_send.py](../../auto_client_acquisition/whatsapp_safe_send.py), [docs/ops/FIRST_WEEK_DAILY_CHECKLIST.md](../ops/FIRST_WEEK_DAILY_CHECKLIST.md).

---

## How to use this file — كيفية الاستخدام

Each template below is a **founder-approved draft**, never an autonomous send. The founder copies the rendered text into WhatsApp Business and presses send. Placeholders use the scriptable form `{name}`, `{company}`, `{calendly_url}`, `{moyasar_link}`, `{proof_score}`, `{tier}`, `{referral_code}` so they map cleanly onto `scripts/whatsapp_draft.py` output.

All templates respect three rules:

1. Saudi business preference: no emojis, calm tone, one clear ask.
2. PDPL Article 5: every outbound message states the recipient can reply `STOP` at any time.
3. Length: 80–150 words per language, short sentences, voice-note-friendly.

---

## 1. Warm-list intro — تمهيد القائمة الدافئة

> **DRAFT ONLY — founder approval required before send.**
> WhatsApp must have explicit consent (PDPL Article 5) OR a warm intro before any send.

### العربية

السلام عليكم {name}. معك {founder_name} من ديليكس. شركتكم {company} ظهرت في قائمتي القصيرة لشركات الخدمات في السعودية اللي ممكن تستفيد من تشخيص مجاني لعمليات المبيعات.

العرض بسيط: تشخيص مجاني خلال ٧٢ ساعة، وبعده — إذا حبّيت — Sprint مدّته أسبوعان بـ ٤٩٩ ريال يُسلّم Proof Pack من ١٤ قسماً. لا التزام بعد التشخيص.

تحب أرسل لك رابط التشخيص؟ ردّ بكلمة "نعم" أو "STOP" للإيقاف.

---

### English

Peace upon you {name}. This is {founder_name} from Dealix. Your company {company} showed up on my short list of Saudi services firms that may benefit from a free sales-ops diagnostic.

The offer is simple: a free diagnostic within 72 hours, followed by — only if you choose — a 14-day Sprint at 499 SAR that delivers a 14-section Proof Pack. No obligation after the diagnostic.

Want me to send the diagnostic link? Reply "yes" or reply "STOP" to opt out.

---

## 2. Diagnostic intake confirmation reminder — تذكير بنموذج التشخيص

> **DRAFT ONLY — founder approval required before send.**
> WhatsApp must have explicit consent (PDPL Article 5) OR a warm intro before any send.

### العربية

{name}، تحية طيبة. أرسلت أمس رابط التشخيص المجاني لـ {company}. النموذج قصير — أقل من ٧ دقائق — والنتيجة تصلك بريدياً خلال ٧٢ ساعة.

إذا واجهت أي سؤال في النموذج، ردّ هنا وأشرحه شفهياً. وإذا الوقت غير مناسب الآن، أبلغني وأعيد المحاولة الأسبوع القادم.

للإيقاف الكامل: ردّ "STOP".

---

### English

{name}, hope you're well. I sent the free diagnostic link for {company} yesterday. The form is short — under 7 minutes — and you receive the result by email within 72 hours.

If any question in the form is unclear, reply here and I will walk you through it. If the timing is wrong now, let me know and I will follow up next week.

To opt out entirely, reply "STOP".

---

## 3. Discovery call booking — حجز مكالمة استكشاف

> **DRAFT ONLY — founder approval required before send.**
> WhatsApp must have explicit consent (PDPL Article 5) OR a warm intro before any send.

### العربية

{name}، شكراً على إكمال التشخيص. أقترح مكالمة قصيرة ٣٠ دقيقة نراجع فيها النتائج ونرسم خيارات Sprint.

ثلاثة أوقات مقترحة (توقيت الرياض):
- الثلاثاء ١٠:٠٠ صباحاً
- الأربعاء ٢:٠٠ مساءً
- الخميس ١١:٠٠ صباحاً

أو احجز مباشرة عبر: {calendly_url}

ردّ "STOP" للإيقاف.

---

### English

{name}, thanks for completing the diagnostic. I'd like to suggest a 30-minute call to review the results and outline Sprint options.

Three proposed slots (Riyadh time):
- Tuesday 10:00 AM
- Wednesday 2:00 PM
- Thursday 11:00 AM

Or book directly: {calendly_url}

Reply "STOP" to opt out.

---

## 4. Proposal sent notification — إشعار إرسال العرض

> **DRAFT ONLY — founder approval required before send.**
> WhatsApp must have explicit consent (PDPL Article 5) OR a warm intro before any send.

### العربية

{name}، أرسلت عرض Sprint لـ {company} على البريد {email}. العرض ثنائي اللغة، ١٤ يوماً، {tier} بـ {price} ريال.

ما أن تؤكد القبول رداً على البريد، أرسل رابط الدفع عبر مُيسّر — ٥٠٪ مقدّماً، ٥٠٪ عند تسليم Proof Pack.

تحب نراجع أي بند شفهياً قبل التوقيع؟

ردّ "STOP" للإيقاف.

---

### English

{name}, I've sent the Sprint proposal for {company} to {email}. The proposal is bilingual, 14 days, {tier} at {price} SAR.

Once you confirm by replying to the email, I'll send the Moyasar payment link — 50% upfront, 50% on Proof Pack delivery.

Would you like to walk through any clause verbally before signing?

Reply "STOP" to opt out.

---

## 5. Payment confirmation receipt — إيصال تأكيد الدفع

> **DRAFT ONLY — founder approval required before send.**
> WhatsApp must have explicit consent (PDPL Article 5) OR a warm intro before any send.

### العربية

{name}، تأكّد استلام الدفعة الأولى لـ {company}. الفاتورة الضريبية في طريقها إلى بريدك.

نبدأ Day 1 من Sprint غداً. أحتاج منك ثلاثة أمور قبل الانطلاق — سأرسلها في رسالة منفصلة الآن.

شكراً على الثقة.

ردّ "STOP" للإيقاف.

---

### English

{name}, first payment for {company} is confirmed. The ZATCA-compliant tax invoice is on its way to your inbox.

We start Sprint Day 1 tomorrow. I need three items from you before we kick off — sending those in a separate message now.

Thank you for the trust.

Reply "STOP" to opt out.

---

## 6. Sprint Day 1 kickoff — انطلاق اليوم الأول

> **DRAFT ONLY — founder approval required before send.**
> WhatsApp must have explicit consent (PDPL Article 5) OR a warm intro before any send.

### العربية

{name}، صباح الخير. اليوم Day 1 من Sprint. ثلاثة أسئلة قصيرة قبل أن أبدأ:

1. هل توافق على Source Passport — أي أنّ كل رقم في Proof Pack مربوط بمصدر بيانات تابع لكم؟
2. هل ملف البيانات (CSV أو Excel) جاهز للرفع؟
3. من جهة الاعتماد لديكم — اسم وبريد — لكل مخرجات اليوم الـ ١٤؟

ردّ صوتي مقبول.

ردّ "STOP" للإيقاف.

---

### English

{name}, good morning. Today is Sprint Day 1. Three quick questions before I start:

1. Do you agree to the Source Passport — meaning every number in Proof Pack is linked to a data source you own?
2. Is the data file (CSV or Excel) ready to upload?
3. Who is the approval contact on your side — name and email — for every Day-14 deliverable?

Voice reply is fine.

Reply "STOP" to opt out.

---

## 7. Sprint daily check-in — تحديث منتصف Sprint

> **DRAFT ONLY — founder approval required before send.**
> WhatsApp must have explicit consent (PDPL Article 5) OR a warm intro before any send.

### العربية

{name}، تحديث Day 3 لـ {company}:

- اكتمل: تدقيق خط الأنابيب + قائمة الـ Source Passports.
- جارٍ: مسوّدات Proof Pack الأقسام ١–٤.

سؤال واحد: هل من عوائق من جهتكم — وصول لبيانات، أو موافقات معلّقة؟

نلتقي يوم Day 7 لمراجعة وسطية مدّتها ٢٠ دقيقة. تحب نثبّت الموعد الآن؟

ردّ "STOP" للإيقاف.

---

### English

{name}, Day 3 update for {company}:

- Done: pipeline audit + Source Passport list.
- In progress: Proof Pack draft sections 1–4.

One question: any blockers on your side — data access, pending approvals?

We have a 20-minute mid-Sprint review on Day 7. Want to lock the time now?

Reply "STOP" to opt out.

---

## 8. Proof Pack delivered — تسليم حزمة الإثبات

> **DRAFT ONLY — founder approval required before send.**
> WhatsApp must have explicit consent (PDPL Article 5) OR a warm intro before any send.

### العربية

{name}، Proof Pack لـ {company} جاهز. ١٤ قسماً، درجة منهجية {proof_score}/100، ملحقات JSON و PDF.

أقترح مكالمة تسليم ٣٠ دقيقة نراجع فيها كل قسم ونتفق على خطوات ما بعد Sprint. ثلاثة أوقات مقترحة على {calendly_url}.

الدفعة الثانية (٥٠٪) مستحقة بعد التسليم. أرسل رابط مُيسّر بعد المكالمة.

ردّ "STOP" للإيقاف.

---

### English

{name}, Proof Pack for {company} is ready. 14 sections, methodology score {proof_score}/100, JSON and PDF attachments.

I propose a 30-minute handoff call to walk through each section and agree on post-Sprint next steps. Three time slots at {calendly_url}.

The second payment (50%) is due after delivery. I'll send the Moyasar link after the call.

Reply "STOP" to opt out.

---

## 9. Retainer offer — عرض الاحتفاظ

> **DRAFT ONLY — founder approval required before send.**
> WhatsApp must have explicit consent (PDPL Article 5) OR a warm intro before any send.

### العربية

{name}، بعد Proof Pack لـ {company} وجدنا ثلاث فرص تستحق متابعة شهرية:

١. مراجعة خطّ الأنابيب أسبوعياً.
٢. حوكمة بيانات المصدر.
٣. مسوّدات تواصل بريدية بموافقة المؤسّس.

نوفّر هذا عبر باقة Managed Revenue Ops بـ ٢٩٩٩ ريال شهرياً، إلغاء بأي وقت بإشعار ٣٠ يوم.

لا التزام الآن — فقط تأكّدوا إذا أحببتم نُرسل ورقة الباقة ثنائية اللغة.

ردّ "STOP" للإيقاف.

---

### English

{name}, after the Proof Pack for {company} we identified three opportunities worth monthly follow-through:

1. Weekly pipeline review.
2. Source-data governance.
3. Email outreach drafts with founder approval.

We offer this through a Managed Revenue Ops retainer at 2,999 SAR/month, cancel any time on 30-day notice.

No obligation now — just confirm if you'd like us to send the bilingual retainer brief.

Reply "STOP" to opt out.

---

## 10. Referral ask (5K SAR credit) — طلب إحالة

> **DRAFT ONLY — founder approval required before send.**
> WhatsApp must have explicit consent (PDPL Article 5) OR a warm intro before any send.

### العربية

{name}، شكراً مرة أخرى على ثقة {company} في Dealix. لدينا برنامج إحالة بسيط: كل عميل جديد توصّيه ويوقّع Sprint، نخصم ٥٠٠٠ ريال من فاتورتك القادمة.

كود الإحالة الخاص بك: {referral_code}

إذا خطر ببالك زميل في قطاع الخدمات يستفيد من تشخيص مجاني، شارك معه الكود.

لا ضغط — فقط فرصة.

ردّ "STOP" للإيقاف.

---

### English

{name}, thanks again for {company}'s trust in Dealix. We have a simple referral program: for each new customer you recommend who signs a Sprint, we credit 5,000 SAR off your next invoice.

Your referral code: {referral_code}

If a peer in services comes to mind who'd benefit from a free diagnostic, share the code with them.

No pressure — just an option.

Reply "STOP" to opt out.

---

## Channel rules — قواعد القناة

WhatsApp inside Dealix is **never autonomous**. The system never presses send on the founder's behalf. Every message above is rendered by `scripts/whatsapp_draft.py`, queued for review, and only the founder pushes the final send through WhatsApp Business on their own device.

Hard rules:

- **Founder approval** is required for every WhatsApp send — no exceptions, no bulk runs.
- **Consent or warm intro** is required before the first send. Cold WhatsApp is blocked at the `safe_send_gateway` layer.
- **Quiet hours** 21:00–08:00 KSA — no sends, no drafts queued for delivery in the window.
- **STOP honored within 24 hours.** Any `STOP` reply moves the contact into the suppression list and removes them from future drafts.
- **PDPL Article 5** — every first-contact message states the opt-out instruction in the same language as the body.

---

## Compliance reminder — تذكير الامتثال

These templates exist inside the perimeter defined by:

- [docs/00_constitution/NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md) — Rule 2 (No cold WhatsApp automation), Rule 6 (No PII in logs), Rule 8 (PDPL alignment).
- [auto_client_acquisition/whatsapp_safe_send.py](../../auto_client_acquisition/whatsapp_safe_send.py) — the safe-send gateway that the founder pipes drafts through.

If a draft fails one of these rules, the founder discards it and reports the failure via `data/daily_brief/<date>.md` so the rule can be re-enforced.

---

Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
