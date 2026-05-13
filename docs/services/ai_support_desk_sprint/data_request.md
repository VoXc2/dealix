# Data Request — AI Support Desk Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Delivery Analyst
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [data_request_AR.md](./data_request_AR.md)

## Context
Client-facing checklist of everything Dealix needs before Day 1. Support data is highly sensitive — this document enforces the DPA in `docs/DPA_DEALIX_FULL.md`, the PDPL retention in `docs/ops/PDPL_RETENTION_POLICY.md`, and the human-in-the-loop posture in `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`.

## Summary
Client provides:
1. **Anonymized message samples** — last 30 days, up to 5,000 messages.
2. **Current FAQ document.**
3. **Hours of operation and service-list reference.**
4. **Escalation contact list.**
5. **Signed data handling acknowledgement.**

Time budget: **≤ 2 business days**.

## Item 1 — Anonymized Message Samples

### Format
- CSV, XLSX, or JSON.
- One row/object per message.
- Required columns: `message_id`, `channel`, `received_at`, `language`, `body_redacted`.
- Optional columns: `current_category`, `agent_response_redacted`, `resolution_time_hours`.

### Anonymization Required
- Customer names → replaced with `<customer_N>`.
- Phone numbers → masked except last 2 digits.
- Email → masked username.
- National IDs / medical record numbers → fully removed.
- Any URLs to private resources → masked.
- Any quoted PII inside message body → removed.

### Volume
- Last 30 days (or last 5,000 messages if higher volume).
- More history acceptable if anonymization is solid.

### What We'll Do
- Profile, cluster, categorize.
- Build the classification rubric.
- Draft suggested-reply candidates per category.

### What We Will NOT Do
- Train any public AI model on it.
- Share with any third party.
- Retain beyond `DATA_RETENTION_POLICY`.
- Process outside the agreed jurisdiction.

## Item 2 — Current FAQ Document

### Minimum Content
- Top 20 FAQ entries with current answers.
- 1–2 pages OK.
- PDF, DOCX, Notion page link.

### If Missing
Dealix drafts an FAQ from the message clusters; the client reviews and approves.

## Item 3 — Hours of Operation & Service List

- Days and hours support is staffed.
- After-hours behavior (auto-acknowledge / silent / partial coverage).
- The services / products being supported (list with brief descriptions).
- Sectors / regions served.

## Item 4 — Escalation Contact List

For each sensitive case type:
- The named human to escalate to (name + role + phone + email).
- Working hours of that human.
- Backup if primary unreachable.

For clinics/healthcare clients, the escalation list MUST include:
- A clinician (doctor or licensed practitioner) for any medical-relevant case.
- A clinic operations lead for non-medical issues.
- A complaints officer.

## Item 5 — Signed Data Handling Acknowledgement
Auto-generated from intake. Sponsor signs electronically. Confirms:
- Lawful basis for processing the message samples.
- Agreement to `docs/DPA_DEALIX_FULL.md`.
- Cross-border posture per `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.
- Retention per `docs/ops/PDPL_RETENTION_POLICY.md`.

## Sensitive Data Handling
If intake flagged sensitivity OR client is a clinic/healthcare:
- All transfers encrypted; vault encrypted at rest.
- Two-person delivery team only.
- Sensitive sample subset isolated to its own index partition.
- Proof pack auto-anonymizes any flagged field.
- Retention reduced to project + 30 days.

## Delivery Method
- Preferred: encrypted shared folder with named access.
- SFTP available on request.
- Not acceptable: WhatsApp file send, public link, personal email attachment unencrypted.

## SLA
- Upload expected within **2 business days** of kickoff.
- Per business day of delay, Sprint slips by 1 day.
- After 4 business days of delay, restart fee SAR 1,500.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Welcome email | Drop folder ready | Dealix Ops | T-1 |
| Client upload | Receipt + integrity check | Dealix Analyst | Day 1 |
| Sensitive flag | Vault placement | Dealix QA + Analyst | Day 1 |
| Missing items | Chase email | Sales Engineer | Daily |

## Metrics
- **On-time data provision** — Target ≥ 80%.
- **Anonymization quality** — `% rows passing PII sweep`. Target ≥ 99%.
- **Lawful-basis acknowledgement** — Target = 100%.

## Related
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/DATA_RETENTION_POLICY.md` — retention
- `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` — cross-border
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md` — HITL rules
- `docs/capabilities/customer_capability.md` — capability blueprint
- `docs/playbooks/clinics_playbook.md` — clinics premium
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
