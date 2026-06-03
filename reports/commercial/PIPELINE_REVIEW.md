# مراجعة الـ Pipeline — قالب تقرير

> **المصدر:** [`data/commercial/opportunities.jsonl`](../../data/commercial/opportunities.jsonl)
> (schema [`opportunity.schema.json`](../../schemas/opportunity.schema.json)).
> المراحل المرجعية في [`PIPELINE_STAGES_AR.md`](../../docs/commercial/PIPELINE_STAGES_AR.md).
> العملة `ر.س` · القيم **نطاقات** · السعر النهائي بموافقة المؤسّس.

- **تاريخ المراجعة:** <YYYY-MM-DD>
- **الفترة:** <من> – <إلى>
- **المُعِدّ:** <الدور>

## 1) عدّ الفرص وقيمتها حسب المرحلة
| المرحلة | العدد | قيمة النطاق (min–max ر.س) | ملاحظات |
|--------|------|---------------------------|---------|
| `signal_detected` | <n> | <min>–<max> | |
| `researched` | <n> | <min>–<max> | |
| `qualified` | <n> | <min>–<max> | |
| `drafted` | <n> | <min>–<max> | |
| `approved_for_outreach` | <n> | <min>–<max> | |
| `contacted` | <n> | <min>–<max> | |
| `replied` | <n> | <min>–<max> | |
| `discovery_scheduled` | <n> | <min>–<max> | |
| `discovery_completed` | <n> | <min>–<max> | |
| `proposal_needed` | <n> | <min>–<max> | |
| `proposal_sent` | <n> | <min>–<max> | |
| `negotiation` | <n> | <min>–<max> | |
| `payment_handoff` | <n> | <min>–<max> | |
| `won` | <n> | <min>–<max> | |
| `delivery_handoff` | <n> | <min>–<max> | |
| `active_delivery` | <n> | <min>–<max> | |
| `renewal_candidate` | <n> | <min>–<max> | |
| `renewed` | <n> | <min>–<max> | |
| `lost` | <n> | — | سبب الخسارة |
| `nurture` | <n> | — | |
| `do_not_contact` | <n> | — | سبب الإيقاف |
| **الإجمالي النشط** | <n> | <min>–<max> | يستثني lost/nurture/do_not_contact |

## 2) الخطوة التالية لكل فرصة نشطة
> القاعدة: لا فرصة نشطة بلا `next_action` واحدة (انظر `NEXT_STEP_RULES_AR.md`).

| `opp_id` | الشركة | المرحلة | `product_match` | `next_action` | المالك |
|----------|--------|--------|------------------|---------------|--------|
| <OPP-…> | <«مثال توضيحي»> | <stage> | <DLX-L…/null> | <action> | <الدور> |

## 3) فرص جاهزة للعرض (بوّابة التأهيل)
> تظهر هنا فقط الفرص `qualified=true` ومُطابَقة لمنتج ولها success metric ونطاق واضح.
| `opp_id` | `product_match` | `success_metric` | `scope_clarity` | `approval_status` |
|----------|------------------|------------------|------------------|-------------------|
| <OPP-…> | <DLX-L…> | <نص> | true | pending/approved |

## 4) ملاحظات الحوكمة والسلامة
- [ ] لا فرصة نشطة بلا `next_action`.
- [ ] لا فرصة في `proposal_needed`/`proposal_sent` بلا تأهيل + مطابقة + metric + نطاق.
- [ ] أي رقم قيمة نطاق فقط، والسعر النهائي بموافقة المؤسّس.
- [ ] لا أرقام بلا `evidence_level`، لا عبارات محظورة، لا عملاء مختلقون، لا PII.

## 5) قرارات وإجراءات
| القرار | المالك | الموعد |
|-------|--------|--------|
| <…> | <الدور> | <YYYY-MM-DD> |
