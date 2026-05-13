# QA Checklist — Lead Intelligence Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** QA Reviewer (independent)
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [qa_checklist_AR.md](./qa_checklist_AR.md)

## Context
Quality gates the Sprint must clear **twice** — once on Day 7 (round 1) and once on Day 10 (round 2). The QA Reviewer must be a Dealix team member who did **not** produce the deliverables. This protocol exists to enforce `docs/quality/QUALITY_STANDARD_V1.md` and to guarantee that every proof pack delivered to a buyer is defensible. It connects to the strategic plan in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and the trust posture documented in `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`.

## How To Use
1. Open the sprint's Notion record.
2. Click "QA Round N" and walk through every gate.
3. For each gate, mark Pass / Fail / N/A and add a one-line evidence pointer (file path or screenshot id).
4. Failures create a fix ticket assigned to the responsible role. SLA = same day.
5. A round is "passed" only when all gates are Pass or N/A.

## Gate 1 — Data Provenance
- [ ] Every account row has a `source` value or a `source_missing` flag.
- [ ] No row contains scraped data from a disallowed source (LinkedIn Sales Nav scrape, etc.).
- [ ] The sensitive-data flag from intake is reflected in column-level masking where required.

## Gate 2 — Scoring Integrity
- [ ] Every score has a one-line explanation in the same row.
- [ ] No score is generated from a model run without the rubric being version-tagged.
- [ ] Distribution is sane (no collapsing to a single value, no unexplained bimodal cliffs).
- [ ] Top 50 list matches the cleaned set, not the raw set.

## Gate 3 — Draft Pack Hygiene
- [ ] Every draft carries `draft_only` in its filename and first line.
- [ ] No draft makes a guaranteed claim ("we will get you 10 meetings", "guaranteed reply", etc.).
- [ ] No cold WhatsApp drafts. Period.
- [ ] No drafts impersonate a third party (e.g., pretending to be a referral from someone real).
- [ ] Arabic drafts in Saudi/Gulf register; English drafts in business register.
- [ ] Drafts respect client's previous tone sample.
- [ ] Drafts include a "remove me / opt-out" line where the channel requires it.

## Gate 4 — Top 10 Action Plan
- [ ] Each top-10 entry has a named human owner.
- [ ] Each entry has a recommended channel.
- [ ] Each entry has a suggested first touch.
- [ ] Each entry has at least one fallback path.
- [ ] No "TBD" owners, channels, or actions.

## Gate 5 — PII & Logging
- [ ] No personally identifiable information (names, emails, phones) in any system log.
- [ ] Sensitive fields (national ID, financial detail, health data) never leave the encrypted vault.
- [ ] Logs use IDs, not raw values.
- [ ] Test/sample exports do not include real client PII.

## Gate 6 — Proof Report
- [ ] Proof report includes baseline state (before sprint) AND result state (after sprint).
- [ ] Every quantitative claim in the report is traceable to a proof pack event.
- [ ] Anonymization rules from intake are applied if the proof will be reused for marketing.
- [ ] Report is signed off by the Delivery Lead before client preview.

## Gate 7 — Proof Pack
- [ ] All required events are present: `intake_completed`, `rows_imported`, `duplicates_removed`, `accounts_scored`, `drafts_generated`, `qa_round_1_complete`, `sprint_delivered`.
- [ ] Each event has a timestamp.
- [ ] Each event has an actor (which role produced it).
- [ ] Each event has a numeric or boolean value where applicable.

## Gate 8 — Mini CRM Board
- [ ] All stages are defined.
- [ ] All top-50 entries are imported.
- [ ] Top-10 entries are visually highlighted.
- [ ] Up to 5 named client users have access.
- [ ] No broader sharing or public link.

## Gate 9 — Lawful Basis & DPA
- [ ] Signed data handling acknowledgement is on file.
- [ ] Cross-border posture matches `CROSS_BORDER_TRANSFER_ADDENDUM`.
- [ ] Retention policy matches `DATA_RETENTION_POLICY`.
- [ ] No data sent to any unapproved third party.

## Gate 10 — Communication & Handoff
- [ ] Daily standup notes exist for every business day of the sprint.
- [ ] Client revision log is complete.
- [ ] Final deliverables package is one coherent zip or shared folder.
- [ ] Client sponsor handoff note is sent.
- [ ] Upsell motion is triggered (per `upsell.md`).

## QA Round 1 vs. Round 2
- **Round 1 (Day 7)**: Gates 1–7 must pass. Gates 8–10 may be in progress.
- **Round 2 (Day 10)**: All 10 gates must pass.

## Escalation
- 3 or more gate failures on Round 1 → escalate to the capability owner.
- Any failure on Gate 5 (PII) → immediate escalation to the Data Protection Officer.
- Any failure on Gate 9 (Lawful Basis) → engagement is paused until resolved.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Day 7 deliverable set | Round 1 result | QA Reviewer | Day 7 |
| Day 10 deliverable set | Round 2 result | QA Reviewer | Day 10 |
| Fix tickets | Resolutions | DL + responsible role | Same-day SLA |
| Proof pack | Final signoff | QA Reviewer | Day 10 |

## Metrics
- **First-time pass rate** — `% sprints clearing Round 1 without rework`. Target ≥ 70%.
- **Gate-failure count** — `average failures per sprint`. Target ≤ 2.
- **PII incidents** — `count`. Target = 0.

## Related
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack scaffold
- `docs/capabilities/revenue_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/DATA_RETENTION_POLICY.md` — retention
- `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` — cross-border
- `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md` — trust pack
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability hooks
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
