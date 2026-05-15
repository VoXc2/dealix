# العربية

Owner: قائد نجاح العميل (Customer Success Lead)

## درجة الطبقة

طبقة تسليم العميل (Layer 10): **78 من 100 — نطاق تجربة عميل**.

## قائمة التحقق المكوّنة من ثمانية أجزاء

| الجزء | الحالة | الدليل (كود حقيقي) |
|---|---|---|
| معمارية | متوفر | `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`، `clients/_TEMPLATE/`، `clients/_PROJECT_WORKBENCH/` |
| جاهزية | متوفر | هذه الوثيقة |
| اختبارات | متوفر | `readiness/delivery/tests.md` |
| مراقبة | متوفر | `clients/_TEMPLATE/VALUE_DASHBOARD.md`، `clients/_TEMPLATE/CAPABILITY_SCORECARD.md` |
| حوكمة | متوفر | `clients/_TEMPLATE/delivery_approval.md`، `clients/_TEMPLATE/governance_events.md` |
| تراجع | متوفر | `clients/_TEMPLATE/04_qa_review.md` (بوابة مراجعة الجودة قبل التسليم) |
| مقاييس | متوفر | `readiness/delivery/scorecard.yaml` |
| مالك | متوفر | قائد نجاح العميل |

## الفجوات المحددة

- **حزم الإثبات المتحقَّقة:** قوالب حزم الإثبات قائمة في `clients/_TEMPLATE/06_proof_pack.md`، لكن كل قيمة فيها يجب أن تُوسَم تقديرية حتى التحقق — لا أرقام مضمونة ولا عملاء وهميين.
- **تمرين تسليم من البداية للنهاية:** انتقال كامل من الاستلام إلى التسليم عبر `clients/_PROJECT_WORKBENCH/` يحتاج تمريناً مُسجَّلاً على وتيرة دورية.

## روابط ذات صلة

- `readiness/delivery/tests.md`
- `readiness/delivery/scorecard.yaml`
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Customer Success Lead

## Layer score

Client Delivery layer (Layer 10): **78 out of 100 — client pilot band**.

## The 8-part checklist

| Part | Status | Evidence (real code) |
|---|---|---|
| architecture | present | `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`, `clients/_TEMPLATE/`, `clients/_PROJECT_WORKBENCH/` |
| readiness | present | this document |
| tests | present | `readiness/delivery/tests.md` |
| observability | present | `clients/_TEMPLATE/VALUE_DASHBOARD.md`, `clients/_TEMPLATE/CAPABILITY_SCORECARD.md` |
| governance | present | `clients/_TEMPLATE/delivery_approval.md`, `clients/_TEMPLATE/governance_events.md` |
| rollback | present | `clients/_TEMPLATE/04_qa_review.md` (a QA review gate before delivery) |
| metrics | present | `readiness/delivery/scorecard.yaml` |
| owner | present | Customer Success Lead |

## Specific gaps

- **Verified proof packs:** proof-pack templates exist in `clients/_TEMPLATE/06_proof_pack.md`, but every value in them must be labeled estimated until verified — no guaranteed numbers and no fake customers.
- **End-to-end delivery drill:** a full transition from intake to handoff through `clients/_PROJECT_WORKBENCH/` needs a documented drill on a periodic cadence.

## Related links

- `readiness/delivery/tests.md`
- `readiness/delivery/scorecard.yaml`
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`

Estimated value is not Verified value.
