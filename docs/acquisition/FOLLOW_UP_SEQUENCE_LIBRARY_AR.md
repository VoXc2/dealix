# Follow-up Sequence Library — مكتبة تسلسل المتابعة (AR)

> تسلسلات متابعة مرتبطة بإيميل مُرسل. **كل الخطوات مسودات (drafts) تنتظر موافقة founder.** تتوقف فورًا عند رد/إلغاء/تحويل.
> مرجع الحقول: `schemas/follow_up_sequence.schema.json`. مرجع المصطلحات: `AGENTS.md`.

---

## 1. القواعد (Cadence & Stop Conditions)

```txt
follow_up_sequence: [3, 7, 14]   (أيام من الإيميل الأصلي)
max_followups:      3
stop_conditions:    replied | unsubscribed | converted
channel:            email فقط
```

| المعلمة | القيمة | المعنى |
|---|---|---|
| Cadence | `[3, 7, 14]` | المتابعة الأولى بعد 3 أيام، الثانية بعد 7، الإغلاق بعد 14. |
| Max follow-ups | `3` | لا تتجاوز 3 متابعات. |
| Stop conditions | `replied`, `unsubscribed`, `converted` | يتوقف التسلسل فور تحقق أي شرط. |

> كل خطوة draft. لا fake `Re:/Fwd:`. لا وعود مضمونة. opt-out متاح حيث يلزم. التسلسل لا يبدأ قبل أن يكون الإيميل الأصلي `sent` (بعد موافقة founder).

---

## 2. القوالب الثلاثة (حرفيًا)

استبدل [الاقواس] حسب الشركة والنظام. الحقول المتغيّرة: [الاسم]، [النظام]، [Recommended System]، [الألم]، [Delivery Output]، [الشركة]، والقطاع بين الأقواس.

### Follow-up 1 (day_offset = 3)

```txt
Subject: متابعة على فكرة [النظام]

السلام عليكم [الاسم]، أتابع فقط على الرسالة السابقة بخصوص [Recommended System]. الفكرة باختصار: نبدأ Sprint صغير يوضح أين يتعطل [الألم] عندكم، ونطلع بمخرج عملي مثل [Delivery Output]. هل يناسب أرسل لكم نموذج مختصر؟
```

### Follow-up 2 (day_offset = 7)

```txt
Subject: هل [الألم] أولوية عندكم حاليًا؟

السلام عليكم [الاسم]، إذا كان [الألم] ليس أولوية الآن، أتفهم ذلك. لكن إذا كان عندكم اهتمام بتحسين [المتابعة/الإيراد/واتساب/العروض/القرار التنفيذي]، أقدر أرسل تصور من صفحة واحدة يوضح أول Sprint مناسب لـ [الشركة]. هل أرسله؟
```

### Close-loop (day_offset = 14)

```txt
Subject: أختم المتابعة؟

السلام عليكم [الاسم]، أختم المتابعة من طرفي حتى لا أزعجكم. إذا أصبح [الألم] أولوية لاحقًا، Dealix يقدر يبدأ Sprint صغير وواضح بدون مشروع كبير من البداية. بالتوفيق لكم.
```

---

## 3. تعبئة الحقول المتغيّرة لكل نظام

| النظام | [الألم] | [Delivery Output] | الجزء في Follow-up 2 |
|---|---|---|---|
| `revenue_os` | الفرص بلا next action واضح | Weekly Opportunity Report | الإيراد |
| `executive_command_os` | القرار اليومي غير الواضح | Daily Command View | القرار التنفيذي |
| `followup_recovery_os` | المتابعة غير المنظمة بعد أول تواصل | Weekly Recovery Report | المتابعة |
| `whatsapp_client_os` | طلبات واتساب غير المصنّفة | WhatsApp Flow + Action Cards | واتساب |
| `proposal_proof_os` | العروض بلا scope وproof كافيين | Proposal Template + Proof Block | العروض |

### مثال معبّأ — `followup_recovery_os`، Follow-up 1

```txt
Subject: متابعة على فكرة نظام استرجاع المتابعات

السلام عليكم [الاسم]، أتابع فقط على الرسالة السابقة بخصوص followup_recovery_os. الفكرة باختصار: نبدأ Sprint صغير يوضح أين يتعطل المتابعة غير المنظمة بعد أول تواصل عندكم، ونطلع بمخرج عملي مثل Weekly Recovery Report. هل يناسب أرسل لكم نموذج مختصر؟
```

---

## 4. الزاوية لكل نظام (Per-System Angle)

| النظام | زاوية المتابعة |
|---|---|
| `revenue_os` | أين تضيع الفرص؟ من يحتاج متابعة؟ ما الخطوة التالية؟ |
| `executive_command_os` | التقارير كثيرة، لكن القرار اليومي غير واضح. |
| `followup_recovery_os` | آخر متابعة لم تحدث قد تكون أغلى فرصة. |
| `whatsapp_client_os` | واتساب ليس فقط محادثات؛ يحتاج flows وaction cards وhandoff آمن. |
| `proposal_proof_os` | العرض المقنع يحتاج Proof وليس كلامًا أكثر. |

---

## 5. مثال على بنية التسلسل (Sequence Object)

```txt
id:                    FUS-101
company:               شركة تدريب في الرياض
recommended_system:    followup_recovery_os
related_email_subject: آخر متابعة لم تحدث قد تكون أغلى فرصة
status:                scheduled
steps:
  - sequence: 1, day_offset: 3,  channel: email, subject: "متابعة على فكرة نظام استرجاع المتابعات"
  - sequence: 2, day_offset: 7,  channel: email, subject: "هل المتابعة غير المنظمة أولوية عندكم حاليًا؟"
  - sequence: 3, day_offset: 14, channel: email, subject: "أختم المتابعة؟"
rules:
  follow_up_sequence: [3, 7, 14]
  max_followups:      3
  stop_conditions:    [replied, unsubscribed, converted]
```

---

## 6. قواعد الأمان

```txt
- كل خطوة draft — لا إرسال قبل موافقة founder.
- لا fake Re:/Fwd:.
- لا وعود مضمونة.
- يتوقف التسلسل فورًا عند: replied | unsubscribed | converted.
- لا يبدأ التسلسل إلا لإيميل sent فعلًا.
- يحترم do_not_contact والـ suppression list.
```

- التحقق: `schemas/follow_up_sequence.schema.json`.
- الفاحص: `scripts/acquisition_delivery_check.py` (`npm run os:check`).

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
