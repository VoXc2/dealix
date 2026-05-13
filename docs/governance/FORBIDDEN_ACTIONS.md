# Forbidden Actions — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Governance Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [FORBIDDEN_ACTIONS_AR.md](./FORBIDDEN_ACTIONS_AR.md)

## Context
This file is the authoritative register of actions that Dealix and its
AI workforce must never perform. It is the concrete, rule-ID-keyed
expression of the non-negotiables in
`docs/company/DEALIX_CONSTITUTION.md` and
`docs/DEALIX_OPERATING_CONSTITUTION.md`. Every entry below maps to a
runtime check enforced by `docs/governance/RUNTIME_GOVERNANCE.md`. If
an action listed here is detected at runtime, the decision is `BLOCK`
or `REDACT` — never `ALLOW`. Any incident that bypasses this register
follows `docs/INCIDENT_RUNBOOK.md`.

## Register
| Rule ID | Forbidden Action | Decision | Severity |
|---|---|---|---|
| FA-01 | Scraping personal data from any source | BLOCK | critical |
| FA-02 | Cold WhatsApp outreach automation | BLOCK | critical |
| FA-03 | Cold LinkedIn outreach automation | BLOCK | critical |
| FA-04 | Guaranteed-outcome sales claims | BLOCK | critical |
| FA-05 | Fake proof or fabricated metrics | BLOCK | critical |
| FA-06 | Storing PII in logs | REDACT | critical |
| FA-07 | Source-less knowledge answers | BLOCK | high |
| FA-08 | External send without explicit approval | BLOCK | critical |
| FA-09 | Autonomous external action (no human in loop) | BLOCK | critical |
| FA-10 | AI agent without owner, scope, and audit | BLOCK | critical |
| FA-11 | Unowned dataset entering an AI workflow | BLOCK | high |
| FA-12 | Sending PII to a non-approved third party | BLOCK | critical |
| FA-13 | Using client data outside declared `allowed_use` | BLOCK | critical |
| FA-14 | Bypassing the LLM Gateway for an external model call | BLOCK | high |
| FA-15 | Disabling audit logging on any AI run | BLOCK | critical |

## Per-Rule Notes
- **FA-01** — covers public-source scraping of personal identifiers
  (email, phone, name). Public business directories without personal
  data are out of scope.
- **FA-02 / FA-03** — "cold" means no prior consent and no existing
  relationship per `relationship_status`. Approved outreach to
  consented or existing contacts is allowed under the Approval Matrix.
- **FA-04** — banned phrasings include "guaranteed sales", "guaranteed
  leads", "guaranteed revenue", and Arabic equivalents.
- **FA-05** — every metric in a proof pack must be traceable to an
  audit event or AI run record.
- **FA-06** — PII must be redacted before any log write. Hashing is
  not a substitute when reversibility is feasible.
- **FA-07** — answers from the Company Brain must cite at least one
  source document, or return "I don't know".
- **FA-08 / FA-09** — every external action (email, message, API
  call) requires a recorded approval per
  `docs/governance/APPROVAL_MATRIX.md`.
- **FA-10** — every AI agent must declare its owner, scope, allowed
  tools, and audit destination. See agent cards under
  `docs/product/agent_cards/`.
- **FA-11** — datasets entering a workflow must have a registered
  owner per `docs/data/DATA_SCHEMA_LIBRARY.md`.
- **FA-12** — third-party processors must be listed in the DPA.
- **FA-13** — `allowed_use` is enforced at the gateway.
- **FA-14** — model calls bypass cost guards, redaction, and audit
  unless they pass through the gateway.
- **FA-15** — disabling audit logging is itself an audit event.

## Detection Pattern
Each rule has a YAML detection pattern in
`docs/governance/RUNTIME_GOVERNANCE.md`. The pattern matches against
the runtime context: channel, recipient, content, dataset metadata,
agent identity, destination.

## Exceptions
There are no exceptions to critical rules. Exceptions to high-severity
rules require:
- Founder written approval recorded in the audit log.
- A time-boxed exception with an expiry date.
- A documented mitigation plan.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Runtime context | Decision (BLOCK / REDACT / ESCALATE) | Governance lead | Per run |
| Incident report | New candidate rule | Governance lead | Per incident |
| Founder approval | Exception record with expiry | Founder | Per exception |

## Metrics
- **Forbidden action attempt rate** — count of attempts blocked by
  this register. Tracked monthly.
- **Critical breach count** — actual forbidden actions that reached
  external systems. Target: 0.
- **Exception expiry compliance** — share of exceptions closed on or
  before their expiry date. Target: 100%.

## Related
- `docs/governance/RUNTIME_GOVERNANCE.md` — runtime checks that enforce
  this register.
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — operating constitution.
- `docs/INCIDENT_RUNBOOK.md` — incident response if a rule is
  bypassed.
- `docs/company/DEALIX_CONSTITUTION.md` — non-negotiables source.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
