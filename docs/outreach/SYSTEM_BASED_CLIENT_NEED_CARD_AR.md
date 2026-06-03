# Dealix — بطاقة احتياج العميل (System-Based Client Need Card)

> أهم شيء في الإيميل المخصص: لكل شركة بطاقة احتياج تربطها بالنظام المناسب من الأنظمة
> الخمسة، وتحدد زاوية الإثبات وزاوية الرسالة وجاهزية الإرسال.
>
> **مصدر الحقيقة للحقول:** `CLIENT_NEED_CARD_FIELDS` في `src/data/draftFactory.ts`.

---

## 1. المخطط (Schema)

```yaml
company:            # اسم الشركة
sector:             # القطاع
country:            # الدولة
city:               # المدينة
website:            # الموقع/الحضور الرقمي
signal:             # الإشارة التي لاحظناها (قنوات، نشاط، توسّع...)
likely_pain:        # الألم المرجّح
recommended_system: # أحد الأنظمة الخمسة فقط
why_this_system:    # لماذا هذا النظام تحديدًا
first_mission:      # أول Sprint مقترح
proof_angle:        # زاوية الإثبات (قبل/بعد، تقرير...)
email_angle:        # زاوية الرسالة (الجملة المفتاحية)
cta:                # الدعوة للإجراء
risk_level:         # low | medium | high
evidence_level:     # weak | moderate | strong
approval_status:    # pending | approved | rejected
send_readiness:     # not_ready | ready_after_gates | ready
```

### قواعد الحقول

- `recommended_system` لازم يكون **واحدًا** من: `revenue-operating-system`,
  `executive-command-os`, `follow-up-recovery-os`, `whatsapp-client-os`,
  `proposal-proof-os`.
- `approval_status` يبدأ دائمًا بـ `pending` (لا إرسال بدون اعتماد).
- `send_readiness` لا يصبح `ready` إلا بعد اجتياز بوابات الأمان (انظر مصنع المسودات).
- ممنوع وضع أي بيانات شخصية حساسة (PII) أو أسرار في البطاقة أو السجلات.

---

## 2. مثال مكتمل

```yaml
company:            شركة تدريب في الرياض
sector:             Training
country:            SA
city:               الرياض
website:            example-training.sa
signal:             برامج متعددة + واتساب للتواصل
likely_pain:        استفسارات التسجيل تضيع أو لا تُتابع بنفس الجودة
recommended_system: follow-up-recovery-os
why_this_system:    أول قيمة تظهر بسرعة في ترتيب المتابعة والرسائل
first_mission:      7-day Follow-up Recovery Sprint
proof_angle:        قبل/بعد follow-up queue + تقرير أسبوعي
email_angle:        "المشكلة ليست في عدد الاستفسارات، بل في آخر متابعة لم تحدث"
cta:                أرسل لك تصورًا مختصرًا لأول workflow؟
risk_level:         low
evidence_level:     moderate
approval_status:    pending
send_readiness:     not_ready
```

---

## 3. كيف تُختار توصية النظام؟

| إشارة من الشركة | النظام المرجّح |
| --- | --- |
| فرص واستفسارات بلا next action واضح | Revenue Operating System |
| إدارة تريد قرارًا يوميًا لا تقارير كثيرة | Executive Command OS |
| متابعة تضيع بعد أول رسالة | Follow-up Recovery OS |
| واتساب قناة رئيسية وفوضوية | WhatsApp Client OS |
| عروض بطيئة أو غير مقنعة | Proposal & Proof OS |

---

## 4. العلاقة بمخطط الإخراج الحالي

النظام الحالي ينتج `outreach_queue.json` و `approval_queue.json` بحقول مختصرة
(`company`, `pain`, `draft_subject`, `draft_body`, `status`, `priority`). بطاقة احتياج
العميل هنا هي **توسعة متوافقة** (superset) تضيف حقول التخصيص والحوكمة المطلوبة للأنظمة
الخمسة، مع الإبقاء على التوافق مع الحقول القديمة.
