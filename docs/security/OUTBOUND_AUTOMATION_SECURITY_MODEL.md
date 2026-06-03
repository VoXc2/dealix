# Outbound Automation Security Model — Dealix

Covers email + WhatsApp outbound. The system is **draft-and-approve**; there is
no autonomous sender, and any future sender must pass through these gates.

## The send pipeline (every gate is a hard stop)

```
draft → [P1 personalization] → [no prohibited claims] → [no fake subject]
      → [unsubscribe present (cold email)] → [not purchased list]
      → [recipient not suppressed] → [consent (WhatsApp)] → [no secrets]
      → ENQUEUE → [HUMAN APPROVAL] → [deliverability verdict ∈ {LIMITED_SEND_READY, RAMP_READY}]
      → send (human/external, send_enabled flag) → log
```

## Hard stops (no send if any are true)
- no approval · no unsubscribe (cold email) · suppressed recipient ·
  domain unhealthy · bounce spike · spam warning · risk high · no evidence level ·
  cold WhatsApp · prohibited claim · secret in message.

## Defaults
`dry_run=true · approval_required=true · send_enabled=false`.

## Enforcement
`core/safety/outreach.py`, `core/safety/draft.py`, `core/safety/whatsapp.py`,
`core/safety/suppression.py`; deliverability verdicts in `docs/outreach/`.

## Anti-abuse
- No LinkedIn automation. No scraping. No purchased lists.
- Volume ramp + domain/subdomain separation (see `docs/outreach/SENDING_RAMP_PLAN_AR.md`).
- Reply-driven suppression (angry/unsubscribe/bounce) is automatic and append-only.
