# Dealix Quality Gates — كل بوابات الجودة

> *آخر تحديث: 2026-06-03*
> الملف الأب: `DEALIX_MAXIMUM_REVENUE_FACTORY_AR.md`

لا مخرج يعبر طبقة دون أن يمرّ على بوابته. هذا الملف يجمع كل البوابات:
Contact، Email، Call، Mini Proposal، Delivery، وFinance Scoring.

---

## 1. Contact Confidence Gate (اكتشاف التواصل)

كل شركة تأخذ مستوى ثقة لقناة التواصل:

| المستوى | المعنى |
|:-------:|--------|
| **C0** | لا توجد قناة تواصل |
| **C1** | قناة عامة غير مؤكدة |
| **C2** | صفحة تواصل رسمية |
| **C3** | إيميل/هاتف منشور رسميًا |
| **C4** | مؤكد من المؤسس/العميل |

**القاعدة:**
```txt
إذا C0/C1:
  لا ترسل ولا تتصل مباشرة.
  أعد البحث، أو استخدم نموذج تواصل رسمي فقط.
إذا C2+:
  مؤهّل للإرسال بعد بقية البوابات.
```

**لماذا؟** الإرسال لمن لم يشترك أو لقوائم غير مؤكدة يرفع احتمال تصنيف الرسائل
كـ spam ويضرّ سمعة الدومين. (راجع `docs/privacy/DO_NOT_CONTACT_AND_SUPPRESSION_POLICY_AR.md`.)

> **ممنوع اختلاق جهات اتصال.** المصدر يجب أن يكون عامًا ومشروعًا ومُسجَّلًا في
> حقل `source`. أي رقم/إيميل بلا مصدر = C0.

---

## 2. Email Production — 6 بوابات

كل إيميل يمرّ على ست بوابات بالترتيب:

```txt
1. Evidence Gate          — هل كل ادعاء مدعوم بإشارة عامة حقيقية؟
2. Personalization Gate   — هل الرسالة مخصّصة لهذه الشركة تحديدًا؟
3. System Fit Gate        — هل النظام المقترح يناسب ألمها فعلًا؟
4. Claim Safety Gate      — لا ضمانات، لا مبالغة، لا ادعاء غير مدعوم.
5. Deliverability Gate    — صياغة لا تُصنَّف spam؛ سطر واحد لإلغاء الاشتراك للتسويق.
6. Founder Approval Gate  — موافقة المؤسس قبل الإرسال.
```

### Email Quality Score

| المعيار | الوزن |
|---------|------:|
| Company context | 20 |
| Pain clarity | 20 |
| System fit | 20 |
| Offer clarity | 15 |
| Tone quality | 10 |
| Evidence correctness | 10 |
| Risk safety | 5 |
| **المجموع** | **100** |

### حالات النتيجة

```txt
90–100 = exceptional
80–89  = send candidate
70–79  = rewrite candidate
<70    = reject
```

### ممنوع نهائيًا في الإيميل

```txt
❌ نضمن زيادة الإيرادات
❌ نضاعف مبيعاتكم
❌ واضح أنكم تخسرون
❌ Re: مزيفة
❌ Fwd: مزيفة
❌ إيميل عام بلا سياق
❌ بيع الأنظمة الخمسة في رسالة واحدة
```

> هذه القائمة أمثلة **محظورة**. أي ظهور لها في نسخة موجّهة للعميل = رفض فوري.
> متطلبات المرسلين (SPF/DKIM، DMARC للمرسلين الكبار، إلغاء اشتراك بنقرة واحدة
> للرسائل التسويقية) تُراجَع في `docs/security/`.

---

## 3. Call System Gate

### بنية Call Brief (قابل لتسليم شخص ثانٍ)

```txt
company · phone_if_public · best_contact_role
recommended_system · why_this_system
email_sent_summary · call_objective
opening_line · three_questions
expected_objection · best_response
next_step · mini_proposal_offer
```

**البوابة:** لا اتصال إلا برقم عام (C3+) و Brief مكتمل وموافقة المؤسس.
**لا اتصال آلي** — الاتصال بيد إنسان.

### Call Outcome Model → Next Action

| النتيجة | الإجراء التالي |
|---------|----------------|
| not_reached | متابعة لاحقًا |
| wrong_person | اطلب تحويلًا (referral) |
| gatekeeper | اطلب تحويلًا |
| interested | Mini Proposal |
| send_more_info | Mini Proposal |
| price_question | ردّ سعر مبدئي (starter) |
| booked_call | تحضير Discovery |
| not_now | Nurture |
| not_interested | إغلاق مهذّب |
| do_not_contact | **Suppression فورًا** |

---

## 4. Mini Proposal Gate

### بنية Mini Proposal (صفحة واحدة)

```txt
Title · Company · Recommended System
Observed Public Signal · Likely Pain
First Sprint · Deliverables · Timeline
Starter Price · Required Inputs
Expected First Proof · Risks / Assumptions
Next Step · Approval Required
```

### Proposal Approval Gate — يفشل إذا

```txt
❌ لا يوجد starter_price
❌ لا يوجد deliverables
❌ لا يوجد timeline
❌ لا يوجد required_inputs
❌ لا يوجد approval_required
❌ يوجد claim مضمون
❌ يوجد scope مفتوح
```

> السعر المعروض "starter from" مرجعيّ، والسعر النهائي **قرار المؤسس**.
> قوالب الأسعار المرجعية في `company_os/revenue/proposals.json`.

---

## 5. Delivery Gates (التسليم لكل نظام)

عند الحالة `won`، يُنشأ تلقائيًا لكل عميل:

```txt
client_workspace · required_inputs_checklist · delivery_task_list
first_output_template · acceptance_gate · weekly_value_report · renewal_trigger
```

**Delivery Start Gate:** لا يبدأ التسليم قبل اكتمال `required_inputs_checklist`.
**Acceptance Gate:** كل مخرج يُراجَع من المؤسس قبل تسليمه للعميل.

### مدخلات/مخرجات كل نظام

**Revenue OS** — *Inputs:* lead sources, pipeline stages, sample leads, follow-up process.
*Outputs:* Revenue Leakage Map, Opportunity Stage Model, Follow-up Workflow, Draft Templates, Revenue Report.

**Executive Command OS** — *Inputs:* goals, KPIs, reports, risks, owners.
*Outputs:* KPI Map, Daily Command Report, Risk Matrix, Decision Log, Executive Board.

**Follow-up Recovery OS** — *Inputs:* leads, last contact, statuses, message samples.
*Outputs:* Follow-up Queue, Lead Status Model, Message Set, Recovery Report.

**WhatsApp Client OS** — *Inputs:* conversation types, FAQs, handoff cases, forms/links.
*Outputs:* Flow Map, Readiness Scan, Action Cards, Handoff Policy, Weekly WhatsApp Review.

**Proposal & Proof OS** — *Inputs:* service description, old proposal, objections, proof/examples, pricing range.
*Outputs:* Proposal Template, Proof Pack, Scope Block, Risk Block, Next-step Card.

> التسليم يحترم حوكمة البيانات: مدخلات العميل تُجهَّل قبل تحليل الـ AI، ولا
> تُلصَق في أدوات عامة. (راجع `company_os/governance/data_handling_checklist.md`.)

---

## 6. Finance Scoring — Cash Priority Score

كل فرصة تأخذ Score مالية لترتيب الأولوية:

| المعيار | الوزن |
|---------|------:|
| Ability to pay | 25 |
| Urgency | 25 |
| Ease of delivery | 20 |
| Upsell potential | 15 |
| Contact availability | 15 |
| **المجموع** | **100** |

### قرار الأولوية

```txt
80+    = high priority
65–79  = good
50–64  = maybe
<50    = nurture
```

> Finance Agent **يحسب ويرتّب فقط** (Observe/Advise). قرار البيع/التسعير للمؤسس.

---

## 7. بوابة عرضية: لا أسماء داخلية في نسخة العميل

أي نسخة موجّهة للعميل (موقع، إيميل، Proposal) **يجب ألا** تحتوي على مصطلحات
داخلية مثل:

```txt
Account Pack · Cash Priority Score · Quality Gate · C0/C1/C2/C3/C4
contact_confidence · operating_factory · ai_action_ledger · suppression_list
```

تُستخدم بدلًا منها الأسماء الخمسة للعملاء (Revenue OS … Proposal & Proof OS)
ولغة فائدة واضحة. هذه البوابة يفحصها `scripts/operating_factory_check.py`.

---

## ملخّص البوابات

```txt
Contact ≥ C2  →  Email 6 Gates (Score ≥ 80)  →  Founder Approval
→ Human Send/Call  →  Mini Proposal Gate  →  Founder Approval
→ Delivery Start Gate  →  Acceptance Gate  →  Renewal Trigger
```

---

*Dealix Quality Gates | Version 1.0 | 2026-06-03*
