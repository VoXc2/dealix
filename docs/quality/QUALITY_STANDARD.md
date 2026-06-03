# Quality Standard

Minimum delivery score: 85/100.

## Score weights

- Business impact: 20
- Data quality: 15
- AI output quality: 15
- Arabic/English quality: 10
- Compliance: 15
- Reusability: 15
- Upsell potential: 10

## Hard failures

See also per-deliverable rubric: [`OUTPUT_QA_SCORECARD.md`](OUTPUT_QA_SCORECARD.md).

- PII leaked
- cold WhatsApp or any external send without approval
- unsupported claim or guaranteed sales claims (e.g. «نضمن»)
- fake proof
- source-less knowledge answer when policy requires sources
- unsafe automation (auto-send, scraping without permission)
- no next action in the final report
- no proof pack (inputs / outputs / next)
- hallucinated critical operational answer (per project definition)
