# Intake Form — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Delivery Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [intake_form_AR.md](./intake_form_AR.md)

## Context
This is the canonical intake form for any Dealix engagement. It is
filled during the Discover stage of the Delivery Standard
(`docs/delivery/DELIVERY_STANDARD.md`). It feeds the Diagnose stage,
the governance plan, and the QA checklist. Templates siblings live in
`docs/templates/` and the quality bar is defined in
`docs/quality/QUALITY_STANDARD_V1.md`.

## How To Use
Copy this file into the project workspace and fill in the placeholders
in the order below. Every required field must be filled before the
Discover gate passes. Mark unknown fields as `unknown` rather than
leaving them blank.

## Section 1 — Business
- Client legal name: `<text>`
- Trading name: `<text>`
- Sector: `<text>`
- City / region: `<text>`
- Headcount band: `<1-10 | 11-50 | 51-200 | 201-1000 | 1000+>`
- Languages used in business: `<text>`
- Primary business problem (one sentence): `<text>`
- What success looks like (one sentence): `<text>`

## Section 2 — Sponsor And Owners
- Sponsor name and role: `<text>`
- Business owner name and role: `<text>`
- Technical contact name and role: `<text>`
- Data owner name and role: `<text>`
- Approver for external communication: `<text>`

## Section 3 — Service Selection
- Service package: `<text>`
- Capability target (Revenue / Customer / Operations / Knowledge /
  Data / Governance / Reporting): `<text>`
- Current capability level: `<0-5>`
- Target capability level: `<0-5>`
- Engagement type: `<Sprint | Pilot | Retainer>`
- Engagement length: `<text>`

## Section 4 — Data
- Data sources available (list): `<text>`
- Record counts (approximate): `<text>`
- Data formats: `<text>`
- Refresh frequency: `<text>`
- Known data issues: `<text>`
- PII present (yes/no): `<text>`
- Lawful basis for any PII: `<text>`
- Cross-border data transfer needed: `<text>`

## Section 5 — Sales / Ops Context
- Current pipeline volume: `<text>`
- Current win rate: `<text>`
- Current support ticket volume: `<text>`
- Current automation in place: `<text>`
- Channels in scope: `<text>`
- Out-of-scope channels: `<text>`

## Section 6 — Governance
- Action class anticipated: `<A | B | C | D>`
- Approval routing agreed: `<text>`
- Known forbidden-action exposure: `<text>`
- Retention preference: `<text>`
- Audit log access required by client: `<yes/no>`

## Section 7 — Success Metrics
- Hero metric: `<text>`
- Baseline value: `<text>`
- Target value: `<text>`
- Measurement source: `<text>`
- Date of baseline measurement: `<text>`
- Reporting cadence: `<text>`

## Section 8 — Risks And Constraints
- Top business risk: `<text>`
- Top data risk: `<text>`
- Top governance risk: `<text>`
- Hard deadlines: `<text>`
- Budget cap: `<text>`
- Resource constraints: `<text>`

## Section 9 — Sign-Off
- Sponsor signature: `<text>`
- Date: `<date>`
- Dealix delivery lead signature: `<text>`
- Date: `<date>`

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Signed scope | Completed intake form | Delivery lead | Per engagement |
| Intake form | Governance plan | Governance lead | Per engagement |
| Intake form | Data request | Data lead | Per engagement |

## Metrics
- **Intake completion rate** — share of engagements with all required
  fields filled. Target: 100%.
- **Unknown-field rate** — share of fields marked `unknown` at end of
  Discover. Target: ≤ 10%.

## Related
- `docs/delivery/DELIVERY_STANDARD.md` — delivery standard.
- `docs/delivery/CLIENT_ONBOARDING.md` — kickoff session template.
- `docs/templates/data_request.md` — data request sibling.
- `docs/quality/QUALITY_STANDARD_V1.md` — quality bar.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
