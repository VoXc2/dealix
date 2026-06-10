# Security and Incident System

## Purpose
Prepare Dealix to detect, respond, document, and learn from operational, security, data, and AI incidents.

## Incident levels

| Level | Meaning | Example | Response time | Owner |
|---|---|---|---|---|
| P0 | Company or customer critical | Major outage or severe data exposure | Immediate | Founder + Engineering |
| P1 | High impact | Production failure, security concern, critical customer issue | Same day | Engineering/Security |
| P2 | Medium impact | Broken workflow or degraded service | 1-2 days | Workstream owner |
| P3 | Low impact | Minor bug or documentation issue | Planned | Team owner |

## Incident record

| Field | Detail |
|---|---|
| Incident ID | INC-YYYY-MM-DD-001 |
| Level | P0/P1/P2/P3 |
| Start time | TBD |
| Detected by | TBD |
| Owner | TBD |
| Systems affected | TBD |
| Customers affected | TBD |
| Current status | Investigating/Contained/Resolved |
| Next update | TBD |

## Response steps

1. Confirm incident.
2. Assign single incident owner.
3. Stop or contain impact.
4. Preserve evidence and logs.
5. Communicate internally.
6. Communicate externally if needed.
7. Fix root cause.
8. Verify recovery.
9. Document postmortem.
10. Create follow-up issues.

## AI incident examples

- Unsupported claim used externally.
- Sensitive data appears in output.
- AI workflow acts without required review.
- Scoring or recommendation cannot be explained.
- Customer challenges AI output accuracy.

## Postmortem template

| Question | Answer |
|---|---|
| What happened? | TBD |
| Why did it happen? | TBD |
| What was the impact? | TBD |
| How was it detected? | TBD |
| What fixed it? | TBD |
| What will prevent recurrence? | TBD |
| Follow-up issues | TBD |

## Security review checklist

- Secrets and keys reviewed.
- Access reviewed.
- Logs reviewed.
- Customer data exposure assessed.
- Vendor involvement assessed.
- Legal/customer communication need assessed.
- Follow-up actions created.
