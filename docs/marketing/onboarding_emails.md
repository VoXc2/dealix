# Onboarding email sequences (Loops)

Source of truth for the email sequences fired from `dealix/marketing/loops_client.py`. Every event below corresponds to one
Loops "email loop" the founder authors in the Loops dashboard. The
variable names map 1:1 to the payload the API sends.

## Sequence A — trial flow

| Order | Trigger event | When | Variables |
| --- | --- | --- | --- |
| 1 | `trial_started` | Immediately after `/api/v1/trial/start` | `tenant_id`, `company`, `name`, `expires_at`, `expires_at_hijri`, `dashboard_url` |
| 2 | `trial_day_3_checkin` | Day 3 since `trial_started` | `tenant_id`, `name`, `leads_count`, `deals_open` |
| 3 | `trial_expiring_3d` | Day 11 since `trial_started` | `tenant_id`, `name`, `days_left=3`, `upgrade_url` |
| 4 | `trial_expired` | Day 14 since `trial_started` | `tenant_id`, `name`, `dashboard_url`, `upgrade_url` |

## Sequence B — billing

| Order | Trigger event | When | Variables |
| --- | --- | --- | --- |
| 1 | `payment_succeeded` | Stripe / Moyasar webhook | `tenant_id`, `amount_sar`, `amount_usd`, `invoice_url`, `issued_at_hijri` |
| 2 | `payment_failed` | Stripe / Moyasar webhook | `tenant_id`, `reason_code`, `retry_url`, `support_url` |
| 3 | `renewal_in_30d` | 30 days before `renewal_at` | `tenant_id`, `plan`, `renewal_at` |

## Sequence C — customer success

| Order | Trigger event | When | Variables |
| --- | --- | --- | --- |
| 1 | `health_at_risk` | Inngest `customer-health-watcher` | `tenant_id`, `risk_score`, `last_active_at` |
| 2 | `feature_adopted` | When tenant first uses a workflow | `tenant_id`, `workflow_name` |
| 3 | `monthly_summary` | 1st business day of month | `tenant_id`, `leads_total`, `deals_won`, `nps_avg` |

## Author guidelines

- Tone: respectful, Saudi-business-appropriate, no superlatives.
- Always render Hijri + Gregorian dates together using the provided
  `*_hijri` and `*_ar` variables.
- Include an unsubscribe link in every footer — RFC 8058 List-Unsubscribe
  header is already wired in `integrations/email.py`.
- The Loops dashboard is the source of design; this file is the source
  of the event contract.

## Wiring

```python
from dealix.marketing.loops_client import get_loops_client

loops = get_loops_client()
await loops.event(
    event_name="trial_started",
    email=user.email,
    properties={
        "tenant_id": tenant.id,
        "company": tenant.name,
        "name": user.name,
        "expires_at": expires_at.isoformat(),
        # ...
    },
)
```

When `LOOPS_API_KEY` is unset, the event is logged + dropped — no
exceptions surface to the caller.
