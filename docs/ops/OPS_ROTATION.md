# On-call rotation

Until the team grows past two engineers we run a "primary + deputy"
rotation, weekly. The primary is the IC for any SEV-1 / SEV-2; the
deputy is paged if the primary is unreachable for 15 min.

## Coverage

- **Business hours** (Sun–Thu 09:00–18:00 Asia/Riyadh): primary on
  Slack within 5 min.
- **Out-of-hours**: primary paged via PagerDuty SMS within 15 min.
  Deputy paged after 15 more min if no ack.

## Current week (template)

| Week of | Primary | Deputy |
| --- | --- | --- |
| YYYY-MM-DD | name | name |

Update this table in the same PR that swaps the rotation. Yes — it's
intentionally manual so the change has a code review.

## Hand-off ritual

Every Sunday 09:00 Riyadh the outgoing primary writes a 5-line summary
in #incidents Slack:

1. Anything still investigating / unresolved.
2. Customers in active contact about incidents.
3. Open postmortem action items due this week.
4. Known-fragile parts of the system right now.
5. "Pager works" confirmation (test page sent + acked by deputy).

## PagerDuty wiring

The Python stub at `dealix/integrations/pagerduty_client.py` posts
events to PagerDuty's Events API v2 when `PAGERDUTY_INTEGRATION_KEY` is
set. Wire alerts from Grafana → PagerDuty → on-call rotation. Until the
account exists this is a no-op.

## What "being on-call" means

- Phone reachable + on charge.
- Laptop reachable in <15 min.
- VPN configured + Railway CLI signed-in.
- Coffee.
