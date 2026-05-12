# Email Triage

Classifies inbound replies into one of 13 buckets (AR + EN) and
drafts a one-line response when appropriate. Mirrors the existing
`auto_client_acquisition/email/reply_classifier` interface.

## Output schema

```yaml
category: interested | scheduling | pricing_q | scope_q | not_now |
          not_decision_maker | wrong_person | hostile | unsubscribe |
          autoreply | out_of_office | spam | other
confidence: 0..1
draft_response: string (≤ 280 chars)
```
