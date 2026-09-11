---
name: dealix-tender-radar
description: Track Saudi B2G tender and procurement readiness lanes from canonical artifacts. Tender research is not a relationship; bid submission is L5 and requires explicit approval.
---

# Dealix Tender Radar

## Scope

- Read canonical B2G artifacts and founder-provided tender notes only.
- Track: entity, readiness gap, documents, partner requirements, deadline, bid/no-bid rationale.
- Submission, bidding, and contract actions are L5.

## Commands

```bash
sed -n '1,40p' /opt/dealix/company-os/founder-os/current/B2G_NELC_LANE.json 2>/dev/null || echo "B2G_LANE=MISSING"
sed -n '1,40p' /opt/dealix/company-os/founder-os/current/B2G_RADAR_SECONDARY.md 2>/dev/null || echo "B2G_RADAR=MISSING"
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
"$REPO/.venv/bin/python" "$REPO/scripts/commercial/generate_daily_targeting_plan.py" 2>/dev/null || true
```

## Output contract

- Lane row: entity, readiness state, required evidence, partner need, deadline, next safe step.
- Expiring deadlines escalate in priority (`P2`) but never auto-submit.
- Public tender research is explicitly labelled `NOT_A_RELATIONSHIP`.

## Forbidden

- Submitting bids, signing, paying fees, or contacting procurement before approval.
