# Market Agent Security Review — Findings (2026-06-03)

Per-agent controls verified against `docs/security/MARKET_AGENT_SECURITY_REVIEW.md`.

| Agent | Risk | Control verified | Status |
|-------|------|------------------|--------|
| Prospect Research | scraping/purchased/over-collection | minimization + `is_purchased_list` | ✅ |
| Draft Factory | claims/PII/secret | claim + secret detectors; draft-only | ✅ |
| Personalization Guard | spam | P1 threshold | ✅ |
| Compliance Gate | fake subject/unsubscribe | detectors | ✅ |
| Deliverability | reputation | ramp/suppression policy | 🟡 infra pending |
| Approval Queue | self-approval | human-only | ✅ |
| Reply Handling | inbound injection | data-only + safe routing | ✅ |
| WhatsApp Concierge | cold/secret | consent + secret detectors | ✅ |

## Residual
- 🟡 Deliverability infra provisioning (founder).
- 🟡 Sending remains external/manual by design.

**Verdict:** Market agents are safe to run as draft-and-review. No autonomous
send path is enabled.
