# Proof Pack Template — Master · Operating Blueprint

**Layer:** Master · Operating Blueprint
**Owner:** Delivery Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [PROOF_PACK_TEMPLATE_AR.md](./PROOF_PACK_TEMPLATE_AR.md)

## Context
Every paid Dealix delivery must end with a signed Proof Pack. The Proof
Pack converts the delivery into three reusable assets: a client-facing
artefact, an anonymized case study, and a capital ledger entry. It
operationalizes the closing rule defined in
`docs/company/DEALIX_MASTER_OPERATING_BLUEPRINT.md` and is the input to
`docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` for the next sale. This file is
the canonical template; do not invent a per-client variant — copy this
file, fill it in, and link the result.

## Header (use exactly these fields)

| Field | Example value | Notes |
|---|---|---|
| Client (anonymized) | Client A | Use real name only with written permission. |
| Service | Lead Intelligence Sprint | Must match a Ready service. |
| Sprint duration | 10 working days | Calendar window with dates. |
| Owner | Delivery Lead name | One human, accountable. |
| Date | YYYY-MM-DD | Date the pack was filed. |
| QA score | 0–100 | From `docs/quality/QUALITY_STANDARD_V1.md`. |
| Approval id | `audit_event_id` | Links to governance log. |

## Section 1 — Problem
One paragraph. Quote the original client pain in their own words where
possible. State the business outcome the client paid for in one
sentence. Do not embellish.

## Section 2 — Inputs
List datasets, documents, and processes inspected.
- Dataset: `<name>` — `<row count>` rows, freshness `<date>`, owner `<role>`.
- Document: `<title>` — version, source location, language.
- Process: `<process name>` — observed at `<date>`, interviewed `<role>`.

## Section 3 — Work Completed
Bulleted list. Each item links to an `audit_event_id`.
- `<verb>` `<object>` → `<audit_event_id>`.
- Example: "Scored 1,240 accounts → `evt_2026_05_03_001`".

## Section 4 — AI Outputs
Counts and quality flags only. Never raw PII. Never sample customer
names, phone numbers, or emails.
- Drafts generated: `<n>`; passed claims check: `<n>`; flagged: `<n>`.
- Answers cited with source: `<n>`; "I do not know" responses: `<n>`.
- Blocked by governance: `<n>` with reasons categorized.

## Section 5 — Metrics
Baseline vs result. Cite the source dashboard or query for every number.

| Metric | Baseline | Result | Source |
|---|---|---|---|
| `<name>` | `<value>` | `<value>` | `<dashboard / query ref>` |

If the metric is not directly measurable in the sprint window, mark it
"indicative" and explain the methodology in one sentence.

## Section 6 — Governance
- Policies applied: `<list>`.
- Approvals captured: `<count>` with role and timestamp.
- Incidents (if any): `<incident_id>` + status.
- PDPL / consent notes: `<short summary>`.

## Section 7 — Business Value
Pick one or more value categories and quantify each.
- **Revenue** — booked, qualified pipeline, or expected lift.
- **Time** — hours saved per week / month.
- **Quality** — defect rate, customer satisfaction, accuracy.
- **Risk** — incidents prevented, compliance gaps closed.
- **Knowledge** — capital ledger entries created, playbooks updated.

State the number, the unit, and the time horizon. Do not promise; report.

## Section 8 — Next Step
Recommended upsell + rationale. Reference the upsell path defined in
`docs/company/SERVICE_READINESS_BOARD.md` for this service. The next
step must be concrete (offer name, indicative price, target start date).

## Proof events that must be captured
Use exactly these event names in the audit log so the Reporting OS can
aggregate them:

`rows_imported` · `duplicates_removed` · `accounts_scored` ·
`drafts_generated` · `workflow_created` · `hours_saved` ·
`documents_indexed` · `answers_with_sources` · `blocked_actions` ·
`approvals_logged` · `report_generated`.

Each event must include: `client_id` (anonymized), `service`,
`timestamp`, `count`, `source_run_id`.

## Anonymization rules
- Replace the client name with "Client A / B / C" unless explicit
  written permission is on file.
- Round metrics to the nearest 5% when published externally
  (whitepapers, decks, website).
- Remove all city, sector, and headcount specifics that could
  re-identify the client.
- Never include sample customer names, phone numbers, or emails.
- Remove any chart screenshot that contains raw PII; regenerate from
  aggregated data instead.

## Sign-off process
1. Delivery Lead drafts the Proof Pack at the end of the sprint.
2. QA Lead reviews against `docs/quality/QUALITY_STANDARD_V1.md`.
3. Client signs the client-facing version.
4. CEO countersigns the internal copy.
5. Anonymized version is filed in `docs/case_studies/` (create the
   directory the first time it is needed).
6. A pointer to the anonymized version is linked from the sales deck
   and from `docs/DEALIX_MASTER_EXECUTION_EVIDENCE_TABLE.md`.

A Proof Pack without all five signatures is treated as not filed; the
delivery does not count toward the Definition of Done in
`docs/company/NEXT_90_DAYS_EXECUTION_PLAN.md`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Delivery artefacts + audit log | Filled Proof Pack | Delivery Lead | Per delivery |
| QA score | Pass / hold | QA Lead | Per delivery |
| Anonymized copy | Public case study | Marketing Lead | After sign-off |
| Capital ledger entries | Reusable asset list | CEO | Per delivery |

## Metrics
- **Proof Pack rate** — % of paid deliveries with a filed pack. Target: 100%.
- **Time-to-pack** — calendar days from delivery end to filed pack. Target: ≤ 5 days.
- **Anonymized publish rate** — % of packs that become public case studies. Target: ≥ 50%.
- **Upsell trigger rate** — % of packs whose "Next Step" leads to a booked meeting. Target: ≥ 40%.

## Related
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — playbook the Proof Pack feeds.
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — dashboard spec that aggregates Proof events.
- `docs/DEALIX_MASTER_EXECUTION_EVIDENCE_TABLE.md` — execution evidence table linking back to filed packs.
- `docs/quality/QUALITY_STANDARD_V1.md` — pass gate before sign-off.
- `docs/company/DEALIX_MASTER_OPERATING_BLUEPRINT.md` — closing rule that makes Proof Packs mandatory.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
