# العربية

# اجتماع الانطلاق — Layer 10 / مرحلة التهيئة

**المالك:** قائد التسليم (Delivery Lead)
**الجمهور:** عضو الفريق الذي يدير اجتماع Kick-off مع عميل دفع للتو
**المراجع:** `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` (القسم 1) · `docs/PILOT_DELIVERY_SOP.md` · `docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md` · `clients/_TEMPLATE/01_intake.md`

> الغرض: اجتماع موحّد مدته 30 دقيقة يضع توقعات واضحة ويجمع كل ما يلزم لبدء التسليم. أي عضو في الفريق يستطيع تنفيذه من هذا الدليل.

## 1. متى يُستخدم هذا الدليل

في اليوم 1 من أي ارتباط مدفوع — Revenue Intelligence Sprint بسعر 499 ريال أو ما فوقه على سُلَّم الخدمات.

## 2. قبل الاجتماع

- تأكّد من استلام الدفع وتأكيده.
- أرسل رسالة ترحيب عربية خلال ساعتين من الدفع.
- أرسل اتفاقية معالجة البيانات (DPA) للتوقيع.
- جهّز رمز مرجعي للعميل بصيغة `DLX-XXXX`.
- شارك جدول أعمال الاجتماع مسبقاً.

## 3. جدول الاجتماع (30 دقيقة)

1. **الترحيب (3 دقائق):** تعريف بقائد التسليم ونقطة التواصل.
2. **شرح الرحلة (7 دقائق):** ماذا يحدث كل يوم خلال الـ Sprint، والمخرجات المتوقعة.
3. **سياسة المسودة فقط (3 دقائق):** «لا يُرسَل أي شيء بدون موافقتك المباشرة».
4. **جمع المدخلات (10 دقائق):** وصف خط الأنابيب، العميل المثالي، 3 صفقات حالية.
5. **الاتفاق على الإيقاع (4 دقائق):** موعد تواصل يومي 15 دقيقة، قناة التواصل.
6. **الخطوة التالية (3 دقائق):** تأكيد مواعيد التسليم ومن يقدّم البيانات.

## 4. القواعد الحاكمة (Non-negotiables)

- لا وعود بأرقام إيراد أو نسب تحويل في الاجتماع.
- كل مخرَج لاحق بحالة `draft_only` حتى موافقة العميل.
- لا طلب بيانات شخصية تتجاوز ما يلزم للتسليم.
- لا إرسال نيابة عن العميل دون موافقة صريحة لكل رسالة.
- لا ذكر للكشط أو الرسائل الباردة كجزء من الخدمة.

## 5. معايير القبول (قائمة الجاهزية)

- [ ] DPA موقّعة قبل بدء التسليم.
- [ ] الرمز المرجعي `DLX-XXXX` أُعطي للعميل.
- [ ] المدخلات الثلاث جُمعت (خط أنابيب، عميل مثالي، 3 صفقات).
- [ ] نقطة التواصل وإيقاع الاجتماعات متّفق عليهما.
- [ ] ملخص الاجتماع أُرسل خلال ساعة.

## 6. المقاييس

- زمن الانطلاق: من الدفع إلى اكتمال Kick-off (الهدف ≤ 24 ساعة).
- اكتمال المدخلات: نسبة العناصر الثلاثة المُجمَّعة في الاجتماع.
- نسبة الاجتماعات التي انتهت بملخص خلال ساعة.

## 7. خطافات المراقبة (Observability)

- سجّل اكتمال Kick-off في ملف العميل تحت `clients/<client>/01_intake.md`.
- علّم الحالة: `kickoff_done` / `inputs_pending`.
- راجعة أسبوعية لزمن الانطلاق لكل عميل.

## 8. إجراء التراجع (Rollback)

إذا انتهى الاجتماع دون مدخلات كافية:
1. أعِد جدولة 15 دقيقة لاستكمال المدخلات الناقصة.
2. لا تبدأ اليوم 1 من التسليم قبل اكتمال المدخلات وتوقيع DPA.
3. سجّل سبب النقص لتحسين قالب الاجتماع.

# English

# Kick-off Meeting — Layer 10 / Onboarding Stage

**Owner:** Delivery Lead
**Audience:** Team member running the Kick-off meeting with a client who has just paid
**References:** `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` (Section 1) · `docs/PILOT_DELIVERY_SOP.md` · `docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md` · `clients/_TEMPLATE/01_intake.md`

> Purpose: a standard 30-minute meeting that sets clear expectations and collects everything needed to start delivery. Any team member can run it from this playbook.

## 1. When to use this playbook

On Day 1 of any paid engagement — the 499 SAR Revenue Intelligence Sprint or any rung above it on the service ladder.

## 2. Before the meeting

- Confirm payment has been received.
- Send an Arabic welcome message within two hours of payment.
- Send the Data Processing Agreement (DPA) for signature.
- Prepare a client reference code in the form `DLX-XXXX`.
- Share the meeting agenda in advance.

## 3. Meeting agenda (30 minutes)

1. **Welcome (3 min):** introduce the Delivery Lead and point of contact.
2. **Journey walkthrough (7 min):** what happens each day of the Sprint, and expected deliverables.
3. **Draft-only policy (3 min):** "Nothing is sent without your direct approval."
4. **Input collection (10 min):** pipeline description, ideal client, 3 current deals.
5. **Cadence agreement (4 min):** daily 15-minute touchpoint, communication channel.
6. **Next step (3 min):** confirm delivery dates and who supplies the data.

## 4. Governance rules (non-negotiables)

- No promises of revenue figures or conversion rates in the meeting.
- Every later deliverable is `draft_only` until client approval.
- Do not request PII beyond what delivery requires.
- No sending on the client's behalf without explicit per-message approval.
- No scraping or cold messaging mentioned as part of the service.

## 5. Acceptance criteria (readiness checklist)

- [ ] DPA signed before delivery starts.
- [ ] Reference code `DLX-XXXX` issued to the client.
- [ ] All three inputs collected (pipeline, ideal client, 3 deals).
- [ ] Point of contact and meeting cadence agreed.
- [ ] Meeting summary sent within one hour.

## 6. Metrics

- Onboarding time: payment to Kick-off completion (target ≤ 24 hours).
- Input completeness: share of the three items collected in the meeting.
- Share of meetings that ended with a summary within one hour.

## 7. Observability hooks

- Log Kick-off completion in the client folder under `clients/<client>/01_intake.md`.
- Tag the state: `kickoff_done` / `inputs_pending`.
- Weekly review of onboarding time per client.

## 8. Rollback procedure

If the meeting ended without sufficient inputs:
1. Reschedule 15 minutes to complete the missing inputs.
2. Do not start Day 1 of delivery before inputs are complete and the DPA is signed.
3. Record the cause of the gap to improve the meeting template.
