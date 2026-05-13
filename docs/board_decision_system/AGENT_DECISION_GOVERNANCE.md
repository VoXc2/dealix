# Agent Decision Governance

## Gate

No new production agent without:

- Clear **purpose**
- Clear **owner**
- **Allowed tools** enumerated
- **Forbidden actions** enumerated (must include: no cold WhatsApp, no scraping, no unapproved external send)
- **Autonomy level** ≤ 3 in MVP
- **Audit** required on all tool calls affecting customer data
- **Decommission rule** (when to retire the agent)

## Research context

Multi-agent systems increase the need for identity, verification, and accountability standards for non-human actors (see [arXiv:2604.23280](https://arxiv.org/abs/2604.23280) — informational).

## Example decision record

```json
{
  "decision": "APPROVE_AGENT",
  "agent": "RevenueAgent",
  "autonomy_level": 2,
  "allowed_actions": ["score_accounts", "generate_drafts", "summarize"],
  "forbidden_actions": ["send_messages", "scrape_web", "cold_whatsapp"],
  "required_controls": ["audit_log", "approval_gate", "pii_redaction"]
}
```

## API

`POST /api/v1/board-decision-os/agent-gate/evaluate`
