# AI Quick Win — Workflow Schema (reference)

```json
{
  "workflow_name": "weekly_sales_report",
  "trigger": "weekly",
  "inputs": ["sales_export", "notes"],
  "ai_step": "draft_summary",
  "human_review": true,
  "governance_checks": ["pii", "claims", "approval"],
  "output": "executive_summary",
  "proof_metric": "hours_saved"
}
```
