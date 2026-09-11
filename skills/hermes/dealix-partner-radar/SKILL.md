---
name: dealix-partner-radar
description: Track partner and referral relationships with real evidence: interactions, quota, referrals, and next safe internal steps. Draft-only for any partner communication.
---

# Dealix Partner Radar

## Scope

- Partners are organizations/people with a real two-way exchange or explicit referral consent.
- Track: interaction evidence, fit, referral potential, quota usage, next safe step.
- No invented partners, quotas, or referrals.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/dealix_partner_referral_tracker.py" --help 2>/dev/null || true
"$PY" "$REPO/scripts/dealix_partner_quota_dashboard.py" --help 2>/dev/null || true
sed -n '1,10p' /opt/dealix/company-os/founder-os/tables/SCOPED_RELATIONSHIPS.tsv
```

## Output contract

- Partner row: entity, evidence type, stage, referral potential, quota status, next internal draft.
- `NO_REPLY_PROVEN` stays a stall, not a loss and not a relationship.
- Any external partner message is a draft pending approval.

## Forbidden

- Sending partner messages, committing discounts, or claiming referrals without consent.
