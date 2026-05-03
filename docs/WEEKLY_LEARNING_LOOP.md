# Dealix Weekly Learning Loop

> Live source: deploy-branch `/api/v1/self-growth/{today,experiments,weekly-learning}`.

## Weekly question set (must answer)

Every Sunday morning, the loop must answer:

| Question | Source |
| --- | --- |
| Best segment | aggregate `LeadRecord.tier` × `industry` |
| Best channel | `outreach_queue` → reply rate by channel |
| Best message | `EmailSendLog` reply_received_at by template |
| Best objection response | `objections/bank` × win rate |
| Worst bottleneck | `revops` role brief → weakest funnel stage |
| Risks blocked | count `compliance/check-outreach` blocks |
| Proof delivered | count `customers/{id}/proof-pack` calls |
| Next experiment | `self-growth/experiments` (deploy branch) |
| Service improvement | weekly review + objection-bank diff |

## Output contract

Single JSON document per company per week:

```
{
  "company_id": "...",
  "iso_week": "2026-W19",
  "best_segment": "...",
  "best_channel": "...",
  "best_message_id": "...",
  "best_objection_response_id": "...",
  "worst_bottleneck": "...",
  "risks_blocked_count": <int>,
  "proof_packs_delivered": <int>,
  "next_experiment": {"id":"...", "hypothesis_ar":"..."},
  "service_improvement_ar": "...",
  "generated_at": "<iso>"
}
```

## Status today

- Endpoints exist on the deploy branch (`self-growth/today` + `weekly-learning`) — CODE_EXISTS_NOT_PROVEN.
- No automated weekly cron yet. Manual call works.
- BACKLOG: schedule via Railway cron service or daily-ops pipeline.
