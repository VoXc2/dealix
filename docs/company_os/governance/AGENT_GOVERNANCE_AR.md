# Dealix Agent Governance

## Hard Controls

- AUTO_SEND_ENABLED=false
- EXTERNAL_OUTREACH_ENABLED=false
- AGENT_APPROVAL_MODE=required

## Why

Agents can draft, summarize, prioritize, score, and report.
Agents must not send, scrape, impersonate, or publish without approval.

## Audit Trail

Every action should leave one of:
- JSON report
- markdown report
- CSV queue
- Git commit
- Railway/GitHub workflow log

## Escalation

If a task touches client data, payment, public outreach, or legal/compliance: founder approval required.
