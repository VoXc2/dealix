---
name: dealix-discovery-prep
description: Prepare an internal discovery agenda from diagnostic evidence and evidence gaps, with qualification questions and a customer-specific scope checklist. No external send or booking.
---

# Dealix Discovery Prep

## Scope

- Discovery happens only after a qualified diagnostic with evidence.
- Deliverable: agenda, evidence gaps, decision criteria, attendees, and the exact questions that change scope or price.
- Prices remain `quote_required_after_qualified_discovery`; never invented.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/founder_meeting_debrief_init.py" --help 2>/dev/null || true
sed -n '1,12p' /opt/dealix/company-os/founder-os/tables/EVENT_INTERACTIONS.tsv
sed -n '1,12p' /opt/dealix/company-os/founder-os/queues/APPROVAL_QUEUE.tsv
```

## Output contract

- Agenda items tied to diagnostic family ids and open evidence gaps.
- Success criteria: baseline, intervention, result, evidence source, acceptance criteria.
- Any customer-facing artifact is a draft for founder approval.

## Forbidden

- Scheduling externally, sending invitations, or committing scope without approval.
