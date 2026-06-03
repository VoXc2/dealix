# قوائم تسليم الأنظمة (System Delivery Checklists) — حزمة التسليم لكل نظام

> لكل نظام من الأنظمة الخمسة حزمة تسليم (Delivery Pack) ثابتة. هذه الوثيقة تعطي Delivery Operator
> قائمة قابلة للتنفيذ (- [ ]) لكل مخرج، مع **Definition of Done** مختصر لكل عنصر.
> المرجع الموحّد: `/home/user/dealix/AGENTS.md`. لا تبدأ أي عنصر يعتمد على بيانات العميل قبل
> `required_inputs_received = true` (انظر `SYSTEM_REQUIRED_INPUTS_AR.md`).

قواعد ثابتة على كل الحزم:

```txt
- لا ادعاءات بإيرادات مضمونة في أي مخرج.
- بيانات العميل anonymized حيث أمكن (PDPL-aligned).
- لا أسرار / مفاتيح API داخل واتساب — أي بيانات حساسة عبر بوابة آمنة.
- الحالات الحساسة تُحوَّل إلى human handoff.
```

---

## 1. `revenue_os` — نظام تشغيل الإيرادات

| # | المخرج (Deliverable) | Definition of Done |
|---|---|---|
| 1 | Revenue Leakage Map | يبيّن أين تضيع الفرص عبر مراحل البيع، مع أكبر نقاط التسريب |
| 2 | Opportunity Stage Model | نموذج مراحل واضح، كل فرصة تنتمي لمرحلة واحدة محددة |
| 3 | Follow-up Workflow | تدفّق متابعة لكل مرحلة مع وقت ومسؤول |
| 4 | Draft Templates | مسودات رسائل جاهزة لكل خطوة (بلا claim مضمون) |
| 5 | Daily/Weekly Revenue Report | تقرير يومي/أسبوعي يقرأه صاحب القرار بوضوح |
| 6 | Founder Next-Action List | قائمة إجراءات founder التالية، مرتّبة بالأولوية |

- [ ] **Revenue Leakage Map** — DoD: خريطة تسريب واضحة بأكبر نقاط الفقد محدّدة.
- [ ] **Opportunity Stage Model** — DoD: كل فرصة لها status واحد لا لبس فيه.
- [ ] **Follow-up Workflow** — DoD: لكل status توجد خطوة تالية بوقت ومسؤول.
- [ ] **Draft Templates** — DoD: لكل next action draft أو إجراء جاهز.
- [ ] **Daily/Weekly Revenue Report** — DoD: تقرير واضح للإدارة يعطي صورة الإيرادات.
- [ ] **Founder Next-Action List** — DoD: قائمة مرتّبة بالأولوية وقابلة للتنفيذ اليوم.

> ربط القبول: انظر معايير `revenue_os` في `SYSTEM_ACCEPTANCE_CRITERIA_AR.md`.

---

## 2. `executive_command_os` — نظام القيادة التنفيذية

| # | المخرج (Deliverable) | Definition of Done |
|---|---|---|
| 1 | KPI Map | خريطة مؤشرات تربط كل KPI بمصدره وصاحبه |
| 2 | Daily Command Report | تقرير يومي يعطي قرارًا واضحًا لا بيانات خام فقط |
| 3 | Risk/Priority Matrix | مصفوفة ترتّب المخاطر والأولويات |
| 4 | Decision Log | سجل قرارات موثّق بالتاريخ والمسؤول |
| 5 | Executive Action Board | لوحة تنفيذ، لكل بند owner وحالة |
| 6 | Weekly Executive Review Template | قالب مراجعة أسبوعية للإدارة |

- [ ] **KPI Map** — DoD: كل KPI له تعريف ومصدر وصاحب.
- [ ] **Daily Command Report** — DoD: التقرير اليومي يعطي قرارًا واضحًا.
- [ ] **Risk/Priority Matrix** — DoD: المخاطر مرتّبة والفرص مرتّبة.
- [ ] **Decision Log** — DoD: كل قرار مسجَّل بتاريخ وصاحب.
- [ ] **Executive Action Board** — DoD: كل بند تنفيذ له owner واضح.
- [ ] **Weekly Executive Review Template** — DoD: قالب جاهز للمراجعة الأسبوعية.

> ربط القبول: انظر معايير `executive_command_os` في `SYSTEM_ACCEPTANCE_CRITERIA_AR.md`.

---

## 3. `followup_recovery_os` — نظام استرجاع المتابعات

| # | المخرج (Deliverable) | Definition of Done |
|---|---|---|
| 1 | Follow-up Queue | طابور متابعة مرتّب حسب الأولوية والوقت |
| 2 | Lead Status Model | نموذج حالات lead واضح وشامل |
| 3 | Follow-up Message Set | مجموعة رسائل متابعة لكل حالة (بلا claim مضمون) |
| 4 | Reminder Rhythm | إيقاع تذكير محدّد بالأوقات |
| 5 | Recovery Report | تقرير استرجاع أسبوعي |
| 6 | Escalation Rules | قواعد تصعيد، متى وإلى من |

- [ ] **Follow-up Queue** — DoD: طابور مرتّب وكل عنصر له وقت متابعة.
- [ ] **Lead Status Model** — DoD: كل lead يقع في حالة واحدة محددة.
- [ ] **Follow-up Message Set** — DoD: لكل حالة رسالة مناسبة جاهزة.
- [ ] **Reminder Rhythm** — DoD: لكل رسالة وقت متابعة محدّد.
- [ ] **Recovery Report** — DoD: يصدر recovery report كل أسبوع.
- [ ] **Escalation Rules** — DoD: قواعد تصعيد واضحة مع human handoff للحالات الحساسة.

> ربط القبول: انظر معايير `followup_recovery_os` في `SYSTEM_ACCEPTANCE_CRITERIA_AR.md`.

---

## 4. `whatsapp_client_os` — نظام عملاء واتساب

| # | المخرج (Deliverable) | Definition of Done |
|---|---|---|
| 1 | WhatsApp Flow Map | خريطة تدفّقات لكل نوع محادثة |
| 2 | Readiness Scan | فحص جاهزية القناة قبل التشغيل |
| 3 | Action Cards | بطاقات إجراء جاهزة للردود الشائعة |
| 4 | Human Handoff Policy | سياسة تحويل الحالات الحساسة لإنسان |
| 5 | Secure Portal Handoff Guide | دليل استلام أي بيانات حساسة عبر بوابة آمنة |
| 6 | Weekly WhatsApp Review | مراجعة أسبوعية لأداء القناة |

- [ ] **WhatsApp Flow Map** — DoD: كل نوع محادثة له flow محدّد.
- [ ] **Readiness Scan** — DoD: فحص الجاهزية مكتمل قبل التشغيل.
- [ ] **Action Cards** — DoD: بطاقات إجراء لكل ردّ شائع، بلا طلب أسرار.
- [ ] **Human Handoff Policy** — DoD: كل حالة حساسة لها مسار human handoff.
- [ ] **Secure Portal Handoff Guide** — DoD: لا تُطلب بيانات حساسة داخل واتساب إطلاقًا؛ تُستلم عبر بوابة آمنة.
- [ ] **Weekly WhatsApp Review** — DoD: يصدر review كل أسبوع.

> ربط القبول: انظر معايير `whatsapp_client_os` في `SYSTEM_ACCEPTANCE_CRITERIA_AR.md`.

---

## 5. `proposal_proof_os` — نظام العروض والإثبات

| # | المخرج (Deliverable) | Definition of Done |
|---|---|---|
| 1 | Proposal Template | قالب عرض واضح وقابل للتخصيص |
| 2 | Proof Pack Template | قالب حزمة إثبات بأمثلة (anonymized) |
| 3 | Scope/Out-of-scope | تحديد النطاق وما هو خارج النطاق |
| 4 | Risk & Assumption Block | كتلة المخاطر والافتراضات |
| 5 | Next-step Card | بطاقة الخطوة التالية الواضحة |
| 6 | Proposal Review Checklist | قائمة مراجعة العرض قبل الإرسال |

- [ ] **Proposal Template** — DoD: العرض واضح ومكتمل العناصر.
- [ ] **Proof Pack Template** — DoD: الدليل واضح وأمثلته anonymized.
- [ ] **Scope/Out-of-scope** — DoD: النطاق واضح وما خارجه واضح.
- [ ] **Risk & Assumption Block** — DoD: المخاطر والافتراضات واضحة.
- [ ] **Next-step Card** — DoD: الخطوة التالية واضحة وقابلة للتنفيذ.
- [ ] **Proposal Review Checklist** — DoD: قائمة مراجعة مكتملة قبل أي إرسال (بموافقة founder).

> ربط القبول: انظر معايير `proposal_proof_os` في `SYSTEM_ACCEPTANCE_CRITERIA_AR.md`.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
