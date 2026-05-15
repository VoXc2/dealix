# Qualification Engine

**Before** you quote or open a project folder, run this engine. Bad clients steal time and destroy quality; the best CEOs ask **who we do not sell to** ([`CLIENT_SELECTION_DECISION.md`](CLIENT_SELECTION_DECISION.md)).

## Score (100)

| المعيار | النقاط |
|---------|-----:|
| ألم واضح | 20 |
| ميزانية / مسار شراء | 20 |
| صاحب قرار | 15 |
| بيانات أو عملية موجودة | 15 |
| يناسب ICP | 15 |
| يقبل review / approval | 10 |
| لا يطلب ممنوعات | 5 |

## Decision bands

| Score | Action |
|-------|--------|
| **80–100** | Pursue |
| **60–79** | Diagnostic first ([`../services/ai_ops_diagnostic/README.md`](../services/ai_ops_diagnostic/README.md)) |
| **40–59** | Nurture |
| **أقل من 40** | Disqualify |

Disqualifiers: spam, guaranteed sales, no owner, no data path, governance bypass — see [`CLIENT_SELECTION_DECISION.md`](CLIENT_SELECTION_DECISION.md).

## Alignment

Same rubric as [`QUALIFICATION_SCORE.md`](QUALIFICATION_SCORE.md); **update both** if weights change.

**Next step:** always recorded in CRM / [`../operations/REQUEST_INTAKE_SYSTEM.md`](../operations/REQUEST_INTAKE_SYSTEM.md) decision field.
