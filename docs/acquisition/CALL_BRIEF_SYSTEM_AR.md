# Call Brief System — دليل التشغيل (AR)

> الـ Call Brief هو ملف اتصال جاهز **لمتصل بشري**. لا اتصال آلي إطلاقًا. كل إيميل مُرسل يُنتج Call Brief.
> مرجع الحقول: `schemas/call_brief.schema.json`. مرجع المصطلحات: `AGENTS.md`.

---

## 1. الغرض والقاعدة الصارمة

بعد إرسال الإيميل، الفرصة تضيع غالبًا في الفجوة بين الإيميل والمكالمة. الـ Call Brief يسدّ هذه الفجوة: ورقة واحدة يفتحها المتصل البشري ويتصل مباشرة دون تحضير إضافي.

```txt
HARD RULE: No automated calling.
الـ Call Brief مادة لمتصل بشري (Caller / Sales Follow-up) فقط.
الذكاء يجهّز الـ brief — الإنسان يتصل، يسجّل الرد، يطلب diagnostic.
```

---

## 2. القالب (Template) — الحقول الـ 11

| # | الحقل | الشرح |
|---|---|---|
| 1 | `company` | اسم الشركة. |
| 2 | `contact_role` | الدور الذي نتصل به (ضمن أدوار النظام المسموحة). |
| 3 | `recommended_system` | النظام المناسب. |
| 4 | `likely_pain` | الألم المحتمل (يُصاغ كاحتمال عند L0/L1). |
| 5 | `email_sent_summary` | ملخص الإيميل الذي أُرسل فعلًا (حتى يربط المتصل المكالمة بالرسالة). |
| 6 | `call_objective` | هدف المكالمة الواحد (عادة: تأكيد الألم + اقتراح Sprint صغير). |
| 7 | `opening_line` | جملة الافتتاح. |
| 8 | `discovery_questions` | أسئلة الاكتشاف (≥ 1). |
| 9 | `expected_objection` | الاعتراض الأرجح. |
| 10 | `best_response` | الرد الآمن المناسب (بلا وعود مضمونة). |
| 11 | `next_step` | الخطوة التالية الواضحة (عادة: إرسال Mini Proposal بعد موافقة founder، أو مكالمة diagnostic). |

> حقول إضافية: `id` (نمط `CB-###`)، `owner`، `status` (`ready` / `called` / `no_answer` / `interested` / `not_interested` / `callback_scheduled`)، `created_at`.

```txt
=== CALL BRIEF ===
Company:            [اسم الشركة]
Contact role:       [دور من أدوار النظام]
System:             [recommended_system]
Likely pain:        [ألم محتمل — صياغة احتمالية]
Email sent summary: [ملخص الإيميل المرسل]
Call objective:     [هدف واحد]
Opening line:       [جملة افتتاح]
Discovery questions:
  - [...]
  - [...]
Expected objection: [الاعتراض الأرجح]
Best response:      [رد آمن بلا ضمان]
Next step:          [خطوة واضحة]
==================
```

---

## 3. كيف يُولَّد الـ Brief من إيميل مُرسل

الـ Call Brief **لا يُجهَّز إلا لإيميل أُرسل فعلًا** (حالة الشركة `sent` ثم `follow_up_due`). مصادر الحقول:

| حقل الـ Call Brief | مصدره |
|---|---|
| `company`, `recommended_system`, `likely_pain` | الـ Company Intelligence Pack / Need Card. |
| `contact_role` | `best_contact_role` من Contact Target. |
| `email_sent_summary` | الإيميل المُرسل فعليًا (subject + جوهر الرسالة). |
| `opening_line`, `discovery_questions`, `expected_objection` | `call_opener` / `call_questions` / `expected_objections` من الـ pack. |
| `best_response` | بنك الاعتراضات (`OBJECTION_HANDLING_LIBRARY_AR.md`). |
| `next_step` | `next_action` من الـ pack. |

تسلسل الحالات:

```txt
approved_to_send → sent → follow_up_due → call_brief_ready → called → interested
```

---

## 4. المالك والتسليم (Owner / Handoff)

| الدور | المسؤولية في مرحلة الاتصال |
|---|---|
| Outreach Operator | يرسل المعتمد، يحدّث الحالة إلى `sent` ثم `follow_up_due`، يطلب تجهيز الـ Call Brief. |
| Caller / Sales Follow-up | **يملك المكالمة**: يفتح الـ brief، يتصل، يسجّل الرد، يحدّث `status`، يطلب diagnostic. |
| Founder | يوافق على Mini Proposal بعد المكالمة قبل أي إرسال. |

> كل Call Brief له `owner` صريح حتى لا يضيع بين فريق الإرسال وفريق الاتصال. راجع `EMAIL_TO_CALL_HANDOFF_AR.md`.

---

## 5. مثال عملي كامل — `followup_recovery_os`

```txt
=== CALL BRIEF ===
id:                 CB-101
Company:            شركة تدريب في الرياض
Contact role:       Marketing Manager
System:             followup_recovery_os
Likely pain:        استفسارات التسجيل غالبًا تضيع أو لا تُتابع بنفس الجودة عبر القنوات
Email sent summary: أرسلنا رسالة مختصرة بعنوان "آخر متابعة لم تحدث قد تكون أغلى فرصة"،
                    اقترحنا فيها Sprint صغير (followup_recovery_os) لبناء follow-up queue
                    ورسائل متابعة حسب حالة المسجّل، مع نموذج من صفحة واحدة.
Call objective:     تأكيد أن المتابعة بعد أول تواصل غير منظمة، واقتراح 7-day Follow-up Recovery Sprint.
Opening line:       السلام عليكم، معك [الاسم] من Dealix. أرسلنا لكم رسالة مختصرة بخصوص
                    نظام استرجاع المتابعات. تواصلنا لأن شركات التدريب غالبًا تخسر جزءًا من
                    التسجيل بسبب متابعة غير منظمة.
Discovery questions:
  - هل عندكم متابعة موحّدة بعد أول تواصل مع المسجّل المحتمل؟
  - هل الرسائل جاهزة حسب حالة العميل (استفسر / سجّل مبدئيًا / لم يكمل)؟
  - من يتابع الاستفسارات حاليًا، وعبر أي قناة؟
Expected objection: "عندنا فريق يتابع"
Best response:      هذا أفضل. Dealix لا يستبدل الفريق؛ يجهّز لهم queue ورسائل وتقارير
                    تخلي المتابعة أوضح.
Next step:          مكالمة 20 دقيقة لفهم مصادر الاستفسارات، ثم تجهيز Mini Proposal
                    (يتطلب موافقة founder قبل الإرسال).
owner:              Caller / Sales Follow-up
status:             ready
==================
```

**ملاحظات الأمان في المثال:** الافتتاح يربط المكالمة بإيميل حقيقي (لا `Re:` مزيّف). الألم صيغ بـ "غالبًا". الرد على الاعتراض بلا أي ضمان. الخطوة التالية تحترم بوابة موافقة founder قبل إرسال الـ Mini Proposal.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
