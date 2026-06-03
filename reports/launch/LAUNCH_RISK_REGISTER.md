# Launch Risk Register

Operational risk register for launch. Reviewed before every mode transition.
Arabic companion: `docs/launch/LAUNCH_RISK_REGISTER_AR.md`.

---

| # | Risk | Level | Trigger | Mitigation | Owner |
|---|------|:-----:|---------|-----------|-------|
| R1 | Email domain reputation | High | Bulk/cold sends, low warm-up | Manual send + SPF/DKIM/DMARC + low volume + warm-up | Founder |
| R2 | Invented contacts | High | Discovery without source | Required public source + confidence + checker scan | Founder |
| R3 | Weak delivery | High | Start without inputs | Delivery Gate + required inputs + acceptance criteria | Delivery |
| R4 | Prompt injection / tool poisoning | High | Untrusted web/email/CI content | External content = untrusted data; least-privilege CI | Founder |
| R5 | Too many systems public | Medium | Marketing all systems | Public site = core systems only | Founder |
| R6 | Founder overload | Medium | Too many daily decisions | Daily Super Command → one critical decision | Founder |
| R7 | Bad-fit prospects | Medium | Loose targeting | Final account score + suppression | Revenue |
| R8 | Scope creep | Medium | Vague proposals | Proposal Gate + explicit out-of-scope | Founder |
| R9 | Secrets leakage | High | Secrets in prompts/logs/reports | No secrets in prompts/logs/reports + review | Founder |
| R10 | Spam complaints / no unsubscribe | High | Marketing mail w/o opt-out | One-click unsubscribe + spam-rate monitoring | Founder |

---

## Highest-priority mitigations (High risks)

- **R1 / R10 (deliverability):** authenticate the domain (SPF, DKIM, DMARC),
  include one-click unsubscribe on marketing mail, keep volume low and warm up
  gradually, and monitor spam rate. Gate sends — never auto-send.
- **R2 (invented contacts):** every contact route needs a verifiable public
  source and a confidence score; the checker fails CI if personal emails/phones
  appear in prospect data without a source column.
- **R4 / R9 (security):** treat all external content as untrusted data (never
  instructions), keep secrets out of prompts/logs/reports, and run GitHub Actions
  with least-privilege permissions (`contents: read` by default).

## Current exposure

At **Internal Dry Run** (no external sending), R1/R2/R10 are dormant by design.
They become live only when Soft Launch enables manual sending — which is gated on
Score ≥ 75 and founder sign-off.
