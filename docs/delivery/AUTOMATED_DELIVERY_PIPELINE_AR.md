# خط التسليم الآلي (Automated Delivery Pipeline) — دليل تشغيلي

> هذه الوثيقة تشرح كيف يتحوّل البيع إلى تسليم واضح وشبه آلي عبر Delivery Engine.
> المرجع الموحّد للمصطلحات هو `/home/user/dealix/AGENTS.md` (single source of truth). أي تعارض يُحسم لصالحه.
> بيانات التسليم في `data/delivery/pipelines.jsonl` ويحكمها `schemas/delivery_pipeline.schema.json`.
> الحالة المباشرة لكل pipeline تُعرض في `reports/delivery/DELIVERY_PIPELINE_STATUS.md`.

الجمهور: **Delivery Operator**. الهدف أن ينفّذ هذا الدليل دون شرح إضافي.

---

## 1. القاعدة الحاكمة قبل أي شيء (Hard Rule)

```txt
العمل الفعلي على التسليم لا يبدأ قبل استلام required_inputs.
الانتقال إلى delivery_started ممنوع ما لم يكن required_inputs_received = true.
```

- أي delivery task تحمل `depends_on_inputs = true` تبقى `todo` أو `blocked` حتى استلام المدخلات.
- لا يُطلب أي سر أو مفتاح API أو بيانات حساسة داخل واتساب — التسليم الآمن عبر بوابة آمنة فقط.
- لا توجد أي ادعاءات بإيرادات مضمونة في أي مخرج أو رسالة أو تقرير.

---

## 2. حالات الـ Pipeline الثلاث عشرة + شروط الانتقال

الترتيب الكامل (canonical):

```txt
interested
→ qualified
→ mini_proposal_ready
→ proposal_sent
→ payment_handoff
→ won
→ intake_required
→ delivery_started
→ first_output_ready
→ client_review
→ accepted
→ weekly_value_report
→ renewal_candidate
```

حالات نهائية إضافية لإدارة العلاقة: `lost`, `do_not_contact`.

### جدول شروط الانتقال (Transition Gates)

| # | الانتقال إلى | الشرط (Gate) | من يملك القرار |
|---|---|---|---|
| 1 | `interested` | اهتمام مبدئي من العميل | Outreach Operator |
| 2 | `qualified` | ألم واضح + نظام مناسب | Outreach Operator / Founder |
| 3 | `mini_proposal_ready` | system + deliverables + starter_price جاهزة | Dealix AI Agents (تجهيز) |
| 4 | `proposal_sent` | **موافقة founder** | Founder |
| 5 | `payment_handoff` | تسليم رابط/إجراء الدفع بعد موافقة founder | Founder |
| 6 | `won` | اتفاق أو دفع | Founder |
| 7 | `intake_required` | نحتاج required_inputs | Delivery Operator |
| 8 | `delivery_started` | **استلمنا required_inputs** (لا يبدأ العمل قبلها) | Delivery Operator |
| 9 | `first_output_ready` | خرج أول مخرج | Delivery Operator |
| 10 | `client_review` | أُرسل للمراجعة | Delivery Operator |
| 11 | `accepted` | العميل وافق على المخرج | العميل + Delivery Operator |
| 12 | `weekly_value_report` | صدر تقرير قيمة | Delivery Operator |
| 13 | `renewal_candidate` | يوجد دليل قيمة أو توسّع محتمل | Founder |

> ملاحظة: البوابات التفصيلية ومعاييرها موثّقة في `docs/delivery/DELIVERY_ACCEPTANCE_GATES_AR.md` وتُسجَّل وفق `schemas/delivery_acceptance_gate.schema.json`.

---

## 3. ماذا يُنشأ تلقائيًا عند تحوّل الصفقة إلى `won`

بمجرد أن تصبح الحالة `won`، يجهّز النظام (Dealix AI Agents) حزمة التسليم آليًا — **تجهيز فقط، بلا إرسال ولا تسعير ولا تنفيذ**. تُنشأ العناصر التالية:

| # | ما يُنشأ تلقائيًا | الوصف | يعتمد على المدخلات؟ |
|---|---|---|---|
| 1 | Client folder | مجلد خاص بالعميل لحفظ كل المخرجات والبيانات (anonymized) | لا |
| 2 | Delivery checklist | قائمة تسليم النظام المختار (انظر `SYSTEM_DELIVERY_CHECKLISTS_AR.md`) | لا |
| 3 | Required inputs list | قائمة المدخلات المطلوبة قبل بدء العمل (انظر `SYSTEM_REQUIRED_INPUTS_AR.md`) | لا |
| 4 | Delivery tasks | مهام التسليم وفق `schemas/delivery_task.schema.json` (بعضها `depends_on_inputs=true`) | جزئيًا |
| 5 | System-specific templates | قوالب مخرجات النظام المختار | لا (قوالب فارغة) |
| 6 | First output template | قالب أول مخرج يُعرض للعميل | لا (يُعبّأ بعد المدخلات) |
| 7 | Weekly value report template | قالب تقرير القيمة الأسبوعي (انظر `WEEKLY_VALUE_REPORTS_AR.md`) | لا |
| 8 | Acceptance checklist | معايير القبول لكل مخرج (انظر `SYSTEM_ACCEPTANCE_CRITERIA_AR.md`) | لا |
| 9 | Renewal trigger | محفّز يراقب وجود دليل قيمة/توسّع لترشيح التجديد | لا |

بعد الإنشاء تنتقل الحالة إلى `intake_required`، ويبدأ Delivery Operator بمتابعة استلام `required_inputs`.

```txt
won → (auto-create حزمة التسليم) → intake_required → (استلام المدخلات) → delivery_started
```

---

## 4. مخطط البوابة قبل بدء التنفيذ (Required Inputs Gate)

```txt
[won]
   │  auto-create: folder + checklist + required inputs + tasks + templates + reports
   ▼
[intake_required]
   │
   ├─ required_inputs_received = false  → ابقَ هنا. المهام depends_on_inputs تبقى blocked.
   │
   └─ required_inputs_received = true   → اسمح بالانتقال
   ▼
[delivery_started]   ← يبدأ العمل الفعلي الآن فقط
```

تحقّق إلزامي قبل `delivery_started`:

- [ ] كل عناصر `required_inputs` للنظام مُستلمة.
- [ ] البيانات الحساسة وصلت عبر بوابة آمنة وليس واتساب.
- [ ] البيانات anonymized حيث أمكن (PDPL-aligned).
- [ ] `required_inputs_received = true` في سجل الـ pipeline.

> إن لم تتحقق الشروط، تبقى الحالة `intake_required` وتُسجَّل الأسباب في `blockers[]`.

---

## 5. جولتان كاملتان لإنشاء حزمة التسليم آليًا (Walkthroughs)

### 5.1 النظام: `followup_recovery_os` (نظام استرجاع المتابعات)

عند `won` يُنشئ النظام بالترتيب:

```txt
1) Required Inputs list
2) Lead Status Model
3) Follow-up Queue Template
4) Message Set Template
5) Weekly Recovery Report
6) Acceptance Checklist
```

| الخطوة | المخرج المُنشأ | متى يُعبَّأ |
|---|---|---|
| 1 | **Required Inputs list** | فورًا عند `won` — يحدّد ما ننتظره من العميل |
| 2 | **Lead Status Model** | قالب فورًا؛ يُضبط بعد استلام المدخلات |
| 3 | **Follow-up Queue Template** | قالب فورًا؛ يُعبَّأ بعد `delivery_started` |
| 4 | **Message Set Template** | قالب فورًا؛ يُصاغ بعد عينة المحادثات (anonymized) |
| 5 | **Weekly Recovery Report** | قالب فورًا؛ أول إصدار بعد أول أسبوع تشغيل |
| 6 | **Acceptance Checklist** | فورًا — معايير قبول المخرج |

البوابة: لا يبدأ ضبط Lead Status Model ولا تعبئة Follow-up Queue قبل `required_inputs_received = true`.

### 5.2 النظام: `proposal_proof_os` (نظام العروض والإثبات)

عند `won` يُنشئ النظام بالترتيب:

```txt
1) Proposal Template
2) Proof Pack Template
3) Scope/Out-of-scope Block
4) Risk Block
5) Next-step Card
6) Review Checklist
```

| الخطوة | المخرج المُنشأ | متى يُعبَّأ |
|---|---|---|
| 1 | **Proposal Template** | قالب فورًا؛ يُخصّص بعد قائمة الخدمات والأسعار |
| 2 | **Proof Pack Template** | قالب فورًا؛ يُعبَّأ بأمثلة proof المتاحة (anonymized) |
| 3 | **Scope/Out-of-scope Block** | فورًا — يُحدَّد بعد فهم الخدمة المطلوبة |
| 4 | **Risk Block** | فورًا — كتلة المخاطر والافتراضات |
| 5 | **Next-step Card** | فورًا — بطاقة الخطوة التالية الواضحة |
| 6 | **Review Checklist** | فورًا — قائمة مراجعة العرض قبل الإرسال |

البوابة: لا يُملأ Proposal Template أو Proof Pack بمحتوى العميل قبل `required_inputs_received = true`.

---

## 6. سجل الحالة (State History) والتقارير

- كل انتقال حالة يُسجَّل في `state_history[]` داخل `data/delivery/pipelines.jsonl` (مع `state` و`at`).
- البنية يحكمها `schemas/delivery_pipeline.schema.json` (الحقول الإلزامية: `id`, `company`, `recommended_system`, `current_state`, `required_inputs`, `required_inputs_received`, `owner`, `updated_at`).
- الحالة المجمّعة لكل العملاء تُعرض في `reports/delivery/DELIVERY_PIPELINE_STATUS.md`.

### مفهوم سجل pipeline (مثال توضيحي)

```txt
id:                       DP-001
company:                  شركة أفق التدريب (synthetic)
recommended_system:       followup_recovery_os
current_state:            intake_required
required_inputs:          [مصادر الاستفسارات, عينة محادثات (anonymized), حالات العميل الحالية, من يتابع ومتى]
required_inputs_received: false
blockers:                 [بانتظار عينة المحادثات anonymized]
owner:                    Delivery Operator
```

> ملاحظة: الأسماء أعلاه تركيبية (synthetic) بنمط سعودي، بلا PII ولا أرقام جوال ولا أسرار.

---

## 7. قائمة تحقق سريعة لـ Delivery Operator

- [ ] الصفقة `won`؟ تأكّد أن حزمة التسليم التسع أُنشئت آليًا.
- [ ] أرسلت `required_inputs list` للعميل عبر القناة المناسبة (لا أسرار في واتساب).
- [ ] استلمت كل المدخلات وتم anonymize حيث أمكن.
- [ ] ضبطت `required_inputs_received = true` فقط بعد التحقق الفعلي.
- [ ] انتقلت إلى `delivery_started` ثم شغّلت المهام.
- [ ] أول مخرج جاهز → `first_output_ready` → `client_review`.
- [ ] قبول العميل → `accepted` → أصدرت تقرير القيمة → `weekly_value_report`.
- [ ] دليل قيمة/توسّع → `renewal_candidate`.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
