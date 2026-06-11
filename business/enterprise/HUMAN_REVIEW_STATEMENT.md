# Human Review Statement (Dealix)

## Rule
No AI output leaves Dealix without a human (founder) approving it.

## What requires review
- Every outreach draft
- Every proposal
- Every client message
- Every external action

## What does NOT require review
- Internal analytics
- Score computation
- Backup / restore
- Internal report generation

## How the gate works
- Every draft has `reviewStatus`
- Founder runs `approve_outreach_draft.py` or `reject_outreach_draft.py`
- Approved ≠ sent: founder sends manually

## Audit
- Every approval and rejection is logged in `reports/audit/audit-YYYY-MM.jsonl`
- Reviewer name + reviewed_at + reason (if reject)
