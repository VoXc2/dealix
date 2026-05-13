# Clinics Playbook — Dealix Growth Layer

**Layer:** L6 · Growth Machine
**Owner:** Head of Growth / Compliance Owner
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [clinics_playbook_AR.md](./clinics_playbook_AR.md)

## Context
Clinics and medical centers are a **secondary ICP** for Dealix, opened
only after Trust OS proof on B2B services. This playbook codifies how
we approach the sector under tighter governance constraints — defined
by `docs/ops/PDPL_RETENTION_POLICY.md`, `docs/DPA_DEALIX_FULL.md`, and
the strategic posture in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.
Removes the constraint of "applying B2B playbook to healthcare", which
is unsafe.

## Common Problems

- WhatsApp overload at reception.
- No structured FAQ system; staff answers vary by shift.
- No-shows hurting capacity.
- Appointment friction (manual phone scheduling).
- Patient privacy sensitivity — high.

## Best Offers (in order)

1. **Data Readiness Assessment** — pre-Sprint, scoped to compliance
   posture, anonymization readiness, and consent state.
2. **AI Support Desk Sprint** — governed FAQ + drafted reply pack for
   non-clinical questions only.
3. **AI Quick Win Sprint** — appointment reminders only **with
   documented consent and PDPL-compliant data flow**.

We do **not** sell clinical AI, diagnostic AI, or anything touching a
patient's clinical record.

## Governance Constraints (Non-negotiable)

- **PDPL-aware data handling.** Lawful basis logged for every record.
- **No PII in logs.** Logs are scrubbed.
- **No auto-send to patients** without lawful basis and verifiable
  consent.
- **Human-in-the-loop** for all clinical-adjacent content.
- **Sensitive data never enters public AI tools.** No exceptions.
- Patient records (medical history, diagnosis, lab) are out of scope.

## Data Needed (Intake Checklist)

- Anonymized message samples (no patient identifiers).
- FAQ list provided by the clinic.
- Hours / services / locations.
- Appointment friction map (where do bookings drop off).
- Consent process documentation.
- Designated Data Protection Officer / privacy contact.

## KPIs Per Engagement

- Response time at reception.
- Resolution rate for non-clinical questions.
- Reply consistency across shifts.
- No-show reduction (only when a consented reminder workflow exists).
- Zero PII incidents — hard target.

## Common Objections + Responses

| Objection | Response |
|---|---|
| "Can you answer medical questions?" | No. We do non-clinical FAQ and reception load only. |
| "Do you integrate with our HIS / EMR?" | Not in scope. We avoid clinical records by design. |
| "Why anonymization first?" | Because we operate under PDPL and refuse to handle identifiable patient data without lawful basis. |
| "Can you mass-message patients?" | Only with verifiable, documented consent and a lawful basis — never as bulk automation. |
| "Other vendors do this faster." | They likely accept compliance risk we won't. We trade speed for trust. |

## Delivery Notes

- Begin with the **Data Readiness Assessment**. If the clinic cannot
  meet PDPL posture, we stop here and recommend remediation.
- All sample data must be anonymized before ingestion.
- All outputs reviewed by the clinic's designated reviewer.
- Proof Pack flags any PII incident — even near-miss — explicitly.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Discovery + readiness assessment | Go / No-Go decision | Compliance Owner | Per lead |
| Anonymized samples | Draft FAQ + governed reply pack | Delivery | Per Sprint |
| Proof Pack | Retainer recommendation (if any) | CSM | Per delivery |

## Metrics

- **Go-rate** after readiness assessment.
- **Resolution rate** for non-clinical questions.
- **No-show reduction** (consented workflows only).
- **PII incidents** — target 0.

## Related

- `docs/ops/PDPL_RETENTION_POLICY.md` — operating PDPL baseline.
- `docs/DPA_DEALIX_FULL.md` — data processing agreement template.
- `docs/playbooks/hospitality_events.md` — adjacent consumer-facing ops playbook.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
