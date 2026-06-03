# Market Agent Security Review (Policy)

Security checklist specific to the GTM/market agents. Findings:
`reports/security/MARKET_AGENT_SECURITY_REVIEW.md`.

## Per-agent risks & controls

| Agent | Top risk | Control |
|-------|----------|---------|
| Prospect Research | unsafe scraping / purchased lists / over-collection | public-only; minimization; `is_purchased_list` |
| Draft Factory | guaranteed claims, PII/secret leak | `find_prohibited_claims`, secret detector, draft never sends |
| Personalization Guard | low-quality spam | P1 threshold |
| Compliance Gate | fake subject, missing unsubscribe | `is_fake_reply_subject`, `has_unsubscribe` |
| Deliverability | domain reputation damage | SPF/DKIM/DMARC + ramp + suppression |
| Approval Queue | self-approval | human-only approval; no self-approve |
| Reply Handling | injection via inbound reply | reply = data; safe routing; human handoff |
| WhatsApp Concierge | cold WA, secret leak | post-consent only; secret/key-request detection |

## Standing controls
Untrusted-input doctrine, `send_enabled=false`, suppression append-only, no
purchased lists, no LinkedIn automation.
