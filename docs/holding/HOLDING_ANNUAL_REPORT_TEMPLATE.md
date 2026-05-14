# Dealix Group — Annual Report Template

> Auto-rendered by `scripts/render_annual_report.py` into
> `landing/assets/downloads/dealix-group-annual-report-<year>.md`.
> Byte-stable for the CI drift gate.

## Sections

The renderer produces every section below. Sections that have no data
are emitted with a "no data this year" line so the structure stays
constant year-over-year.

### 1. Overview
- Year, doctrine version adopted, commit SHA at year-end.
- Operating principles re-stated.

### 2. Business Unit Summary
- For each BU in `data/business_units.json`:
  - Slug, name, status, owner, doctrine version, KPI.
  - Status delta vs prior year (if history available).

### 3. Capital Allocation Actions
- Count of allocation decisions in each bucket (must_fund /
  should_test / hold / kill / spinout / acquire).
- One-line summary per noteworthy decision.

### 4. Verifier State
- Overall PASS / FAIL.
- CEO-complete (top-8) state.
- Per-system score grid (the 19+ systems).
- Year-over-year delta (where prior verifier-report.json snapshots
  exist).

### 5. Market Motion
- `outreach_sent_count` (cumulative).
- `invoice_sent_count` (cumulative).
- Market-feedback summary (counts by signal_type from PR9).

### 6. Capital Assets
- Total count + count by `CapitalAssetType`.
- 5 most-recent safe titles (no PII).

### 7. Doctrine Discipline
- Doctrine version history with summaries.
- Forbidden-feature audit result (PR4 doctrine-gate).
- Marker-honesty audit result (counters match `len(entries)`).

### 8. Risks (qualitative)
- Top risks from `data/group_risk_register.json` (PR15).
- Top mitigations and their status.

### 9. Next Year Theses
- Per-BU thesis (1 line each).
- Group-level theses (1–3 lines).

### 10. Certifications
- Doctrine adoption certificate (group level).
- Partner-kit adoption status.
- Internal audit status (last review date).

## Public Variant

The public-facing version of the annual report is rendered into
`landing/annual-report.html` (PR15). It includes Sections 1, 2 (BU
names + status only, no owner), 4 (verifier state), 6 (capital asset
counts), 7 (doctrine discipline summary), and 10. It NEVER includes
Sections 5 (absolute counts), 8 (raw risk descriptions), or 9
(forward-looking statements that could be misread as guarantees).

## Determinism

The renderer is byte-stable: identical inputs produce identical
output. The CI drift gate fails any change that drifts without an
input change.
