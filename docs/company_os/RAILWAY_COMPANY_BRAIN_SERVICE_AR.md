# Railway Company Brain Service

Create a private Railway service:

- Service name: company-brain
- Config file path: railway.company-brain.toml
- Public networking: OFF

Variables:

AUTO_SEND_ENABLED=false
EXTERNAL_OUTREACH_ENABLED=false
AGENT_APPROVAL_MODE=required
COMPANY_BRAIN_INTERVAL_SECONDS=900

This service generates:
- daily CEO brief
- content drafts
- manual approval queue
- growth scorecard

It does not send messages, scrape platforms, or publish content.
