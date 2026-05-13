# Executive Report — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Delivery Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [executive_report_AR.md](./executive_report_AR.md)

## Context
This is the executive report template used inside the proof pack at
end of engagement. It is the document the client's executive team
reads. It is paired with the Quality Standard
(`docs/quality/QUALITY_STANDARD_V1.md`), the Executive Decision Pack
(`docs/EXECUTIVE_DECISION_PACK.md`), and the Handoff Process
(`docs/delivery/HANDOFF_PROCESS.md`). Every claim must be traceable
to an `AuditEvent` or `ProofEvent`.

## Cover
- Client name: `<text>`
- Engagement title: `<text>`
- Reporting period: `<text>`
- Author (Dealix delivery lead): `<text>`
- Date: `<date>`

## Section 1 — Hero Metric
One number, one sentence, one source.

- Metric: `<text>`
- Value: `<text>`
- Baseline: `<text>`
- Change: `<text>`
- Source: `<audit_event_id>`

## Section 2 — What We Did
A 3-5 bullet summary of the work performed. Each bullet ties to a
deliverable in the Scope of Work.

- `<text>`
- `<text>`
- `<text>`

## Section 3 — Before / After
A short table or paragraph showing the measured change. Use the same
units in both columns.

| Dimension | Before | After |
|---|---|---|
| `<text>` | `<text>` | `<text>` |
| `<text>` | `<text>` | `<text>` |

## Section 4 — Top Risks
List the top three risks observed during the engagement, with a
proposed mitigation for each.

1. `<risk> → mitigation: <text>`
2. `<risk> → mitigation: <text>`
3. `<risk> → mitigation: <text>`

## Section 5 — Next 3 Actions
List the three highest-leverage next actions, with an owner and a
date.

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | `<text>` | `<text>` | `<date>` |
| 2 | `<text>` | `<text>` | `<date>` |
| 3 | `<text>` | `<text>` | `<date>` |

## Section 6 — Sources And Evidence
List the `AuditEvent`, `AIRun`, and `ProofEvent` IDs that support
the metrics in Section 1 and the before/after in Section 3.

- `AUD-<id>` — `<one line>`
- `AIR-<id>` — `<one line>`
- `PEV-<id>` — `<one line>`

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Delivered work | Hero metric | Delivery lead | Per engagement |
| Audit ledger | Source IDs | Backend lead | Per engagement |
| QA record | Quality attestation | QA reviewer | Per engagement |
| Sponsor | Sign-off | Sponsor | Per engagement |

## Metrics
- **Source traceability** — share of claims tied to a ledger ID.
  Target: 100%.
- **Executive read time** — target reading time ≤ 5 minutes.
- **Decision conversion** — share of reports producing a recorded
  next-step decision. Target: ≥ 90%.

## Related
- `docs/quality/QUALITY_STANDARD_V1.md` — quality bar.
- `docs/EXECUTIVE_DECISION_PACK.md` — executive decision pack.
- `docs/delivery/HANDOFF_PROCESS.md` — handoff process.
- `docs/templates/renewal_proposal.md` — renewal proposal sibling.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
