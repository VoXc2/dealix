# Dealix Tool Notes

## Canonical systems
- GitHub: code, PRs, CI, implementation history.
- Railway: Production Core/API/PostgreSQL and intended frontend runtime.
- Hostinger VPS: Command & AI Node only.
- Dealix Company Brain / Opportunity Graph / Strategy Execution / Approval / Proof / Learning: canonical business state.
- n8n: deterministic connectors/workflows, not business source of truth.
- Ollama: loopback-only local inference.
- Hermes: internal specialist runtime.
- OpenClaw: founder command/Telegram gateway.

## Safety
The Telegram-facing agent must not receive unrestricted shell, file mutation, production, payment, secret, or merge tools.

Use sub-agents only for bounded research and synthesis. Sub-agents do not receive L5 authority.

Use the private GitHub Issue/VPS command bridge and Company Autopilot as governed operational surfaces instead of inventing raw shell access.

## Expected founder intents
/status — current company/infrastructure posture
/today — Daily Command
/production — Production Trust and blockers
/revenue — money-now priorities and pipeline proof
/opportunities — highest verified opportunities
/approvals — exact waiting L5 decisions
/prs — Draft PRs and CI readiness
/security — security posture
/proof — recent evidence and proof gaps
/costs — infrastructure/tool cost posture
/learn — latest learning and improvement proposals
/help — command catalog

Never state that an intent executed an external action unless a proof event verifies it.
