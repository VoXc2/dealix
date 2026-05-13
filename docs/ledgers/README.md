# Dealix Ledgers — Templates and Conventions

> Markdown-table MVP for the 8 ledgers defined in
> `docs/company/OPERATING_LEDGER.md`. Phase 2 migrates to the event store
> for queryable, immutable storage.

## Conventions

- One file per ledger (below).
- Every row has an ID (e.g., `R-001`, `D-001`, …) — never reused.
- Every row has a date and an owner.
- **No retroactive editing**. Corrections are new dated rows.
- Sort: newest at top.

---

## 1. `REQUEST_LEDGER.md`

```markdown
# Request Ledger

| ID | Date | Source | Request | Type | Fit | Risk | Decision | Owner | Next Action |
|----|------|--------|---------|------|----:|------|----------|-------|-------------|
| R-001 | YYYY-MM-DD | LinkedIn | Wants lead scoring | Sales | 85 | Medium | Discovery | __ | Schedule call |
```

Type ∈ {Sales / Client Change / Feature / Governance / Support / Partner / Enterprise}.
Decision ∈ {Accept / Qualify / Diagnostic / Redirect / Backlog / Reject / Block}.

## 2. `DECISION_LEDGER.md`

```markdown
# Decision Ledger

| ID | Date | Decision | Context | Evidence | Risk | Owner | Outcome | Review Date |
|----|------|----------|---------|----------|------|-------|---------|-------------|
| D-001 | YYYY-MM-DD | Sell Lead Intelligence Sprint | Service Readiness 92 | demo + QA + proof | Low | CEO | Official | Q+1 |
```

## 3. `CLIENT_LEDGER.md`

```markdown
# Client Ledger

| Codename | Sector | Service | Status | Revenue (SAR) | QA | Proof | Health | Next Step |
|----------|--------|---------|--------|--------------:|---:|-------|-------:|-----------|
| BFSI-A1 | bfsi | Lead Intelligence | Delivered | 9,500 | 91 | Yes | 85 | Retainer offer |
```

Status ∈ {Lead / Qualified / Proposal / Paid / In Delivery / Delivered / Proof Delivered / Retainer Offered / Retainer / Dormant}.
Health ∈ {0–100; expand ≥ 80; nurture 60–79; risk 40–59; churn likely < 40}.

## 4. `DELIVERY_LEDGER.md`

```markdown
# Delivery Ledger

| ID | Client | Service | Output | Date | QA Score | Governance | Delivered | Proof Ref |
|----|--------|---------|--------|------|---------:|------------|:---------:|-----------|
| O-001 | BFSI-A1 | Lead Intelligence | Executive Report | YYYY-MM-DD | 91 | Pass | YES | P-001 |
```

Rule: every customer-facing output must be QA-scored, Governance-checked, and tied to a Proof Pack.

## 5. `GOVERNANCE_LEDGER.md`

```markdown
# Governance Ledger

| ID | Date | Client | Issue | Risk | Decision | Control | Owner |
|----|------|--------|-------|------|----------|---------|-------|
| G-001 | YYYY-MM-DD | BFSI-A1 | Missing data source 8% | Medium | Flag research-only | Source-required gate | HoLegal |
| G-002 | YYYY-MM-DD | HEALTH-C3 | Cold WhatsApp request | High | Block | Forbidden Actions | CRO |
```

Decision ∈ {Allow / Allow-with-approval / Redact / Research-only / Rewrite / Block / Escalate}.

## 6. `PROOF_LEDGER.md`

```markdown
# Proof Ledger

| ID | Client | Service | Proof Type | Metric | Before | After | Anonymized Asset |
|----|--------|---------|------------|--------|--------|-------|------------------|
| P-001 | BFSI-A1 | Lead Intelligence | Data Quality | valid rows % | 65% | 88% | `docs/assets/proof_packs/proof_bfsi_lis_001.md` |
| P-002 | BFSI-A1 | Lead Intelligence | Revenue Proof | top accounts | 0 ranked | 50 ranked | same |
```

Proof Type ∈ {Revenue / Time / Quality / Risk / Knowledge}.

## 7. `LEARNING_LEDGER.md`

```markdown
# Learning Ledger

| ID | Date | Source Project | Insight | Category | Action | Owner |
|----|------|----------------|---------|----------|--------|-------|
| L-001 | YYYY-MM-DD | BFSI-A1 | B2B clients struggle with source attribution at first | Data | Add source-required checklist Day 1 | HoData |
| L-002 | YYYY-MM-DD | HEALTH-C3 | Arabic outreach needs sector-specific tone | Arabic QA | Build tone library | HoP |
```

Category ∈ {Sales / Delivery / Data / Governance / Arabic QA / Product / Pricing / Sector Playbook}.

Rule: every project closes a Learning Ledger entry (per `COMPOUNDING_SYSTEM.md`).

## 8. `PRODUCT_LEDGER.md`

```markdown
# Product Ledger

| ID | Feature | Source projects | Repeated? | Value | Risk Reduction | Build score | Decision |
|----|---------|-----------------|----------:|-------|----------------|------------:|----------|
| F-001 | Import Preview | BFSI-A1, RETAIL-B2 | Yes (2) | High | Medium | 90 | Build now |
| F-002 | WhatsApp auto-send | (Customer request) | No | Medium | LOW (high risk) | 25 | Block (Decision Rule 3) |
```

Decision ∈ {Build now / Backlog / Template-first / Manual-first / Block}.

---

## How to keep these alive

- **Daily**: 15 min — log new Request rows + any Governance events.
- **Weekly**: walk every ledger; ensure each open Request has a decision, each delivered Output has QA + Proof, each closed project has a Learning entry.
- **Monthly**: count rows per ledger. A ledger with 0 new rows is a signal: either nothing is happening in that domain (OK), or operating habit broke (NOT OK).

## Cross-links

- `docs/company/OPERATING_LEDGER.md` — master concept
- `docs/company/CONTROL_PLANE.md` — reads from these ledgers
- `docs/company/CLOSED_LOOP_EXECUTION.md` — the 11 stations
- `docs/company/COMPOUNDING_SYSTEM.md` — the 6 assets per project that produce ledger rows
