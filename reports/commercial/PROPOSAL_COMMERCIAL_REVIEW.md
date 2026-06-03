# مراجعة العروض التجارية — قالب تقرير

> **المصدر:** [`schemas/commercial_proposal.schema.json`](../../schemas/commercial_proposal.schema.json) ·
> الفرص [`opportunities.jsonl`](../../data/commercial/opportunities.jsonl).
> القاعدة المُلزِمة: لا عرض بدون فرصة مؤهّلة + فئة ألم + مطابقة `DLX-L*` + success metric
> + وضوح نطاق + موافقة المؤسّس (انظر [`PROPOSAL_APPROVAL_POLICY_AR.md`](../../docs/commercial/PROPOSAL_APPROVAL_POLICY_AR.md)
> واختبار `tests/test_proposal_requires_qualified_opportunity.py`).

- **تاريخ المراجعة:** <YYYY-MM-DD>
- **المُعِدّ:** <الدور>

## 1) اكتمال العروض (البوّابات الست)
| `proposal_id` | `opp_id` | الشركة | `qualified` | `pain_category` | `product_match` | `success_metric` | `scope_clarity` | `includes_out_of_scope` | موافقة المؤسّس |
|----------------|----------|--------|-------------|------------------|------------------|------------------|------------------|--------------------------|----------------|
| <PRP-…> | <OPP-…> | <«مثال توضيحي»> | true/false | <فئة> | <DLX-L…> | <نص> | true/false | true/false | approved/pending |

> أي صف فيه `qualified=false` أو `product_match` فارغ أو `scope_clarity=false` =
> **عرض غير مكتمل، يُمنع إرساله**.

## 2) حالة الاعتماد والإرسال
| `proposal_id` | `price_range` (ر.س) | `final_price` | `approval_status` | `send_status` |
|----------------|----------------------|----------------|--------------------|----------------|
| <PRP-…> | <min>–<max> | null/<رقم> | pending/approved/needs_revision/rejected | not_sent/queued_plan/approved_for_send/sent |

> `final_price` يبقى `null` حتى موافقة المؤسّس. `send_status` لا يتجاوز
> `approved_for_send` إلا بقرار بشري ووفق سياسة قابلية التسليم.

## 3) فحص البوّابات (ملخّص)
| البوّابة | عدد العروض المستوفية | عدد المُخالِف | إجراء |
|---------|----------------------|---------------|------|
| 1. تأهيل (`qualified=true`) | <n> | <n> | <…> |
| 2. فئة ألم | <n> | <n> | <…> |
| 3. مطابقة `^DLX-L[0-6]$` | <n> | <n> | <…> |
| 4. success metric | <n> | <n> | <…> |
| 5. نطاق + خارج نطاق | <n> | <n> | <…> |
| 6. موافقة المؤسّس | <n> | <n> | <…> |

## 4) فحص السلامة
- [ ] لا عبارة محظورة (نضمن/نضاعف/نتائج مضمونة/بدون مخاطرة/10x/"guaranteed revenue"/"no risk").
- [ ] لا عميل/دراسة حالة/رقم مختلق.
- [ ] كل رقم كمّي يحمل `evidence_level`.
- [ ] لا PII (أدوار فقط)، لا `Re:`/`Fwd:` مزيّفة.
- [ ] لا سعر نهائي قبل الموافقة، لا إرسال تلقائي.

## 5) قرارات
| العرض | القرار | المالك | الموعد |
|------|-------|--------|--------|
| <PRP-…> | approve/revise/reject | المؤسّس | <YYYY-MM-DD> |

> «مثال توضيحي»: عرض لـ Digital Rise Agency (`DLX-L1`) مستوفٍ للبوّابات → جاهز لاعتماد المؤسّس.
