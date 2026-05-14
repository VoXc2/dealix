# Dealix Group — Investment Memo

> Doctrine version: `v1.0.0` ·
> [`/api/v1/doctrine?version=v1.0.0`](https://dealix.example.com/api/v1/doctrine?version=v1.0.0)
>
> This memo is investor-grade in **structure** and doctrine-locked in
> **content**. It does NOT contain forward-looking financial figures
> that would conflict with the eleventh non-negotiable
> ("verifiable, not merely trusted").

## 1. One-Line Thesis

Dealix Group is the holding parent of operating BUs that deliver
**governed AI operations** to Saudi and GCC companies — starting with
B2B services and expanding through partner-led pilots.

## 2. Market

- **Beachhead:** Saudi B2B services (40–500 headcount,
  ≥ 20 M SAR / year), regulated-adjacent buyers.
- **Expansion:** UAE → Qatar / Bahrain → Kuwait / Oman, partner-led
  (see `docs/gcc-expansion/GCC_COUNTRY_PRIORITY_MAP.md`).
- **Category:** Governed AI Operations (a category created by
  Dealix's doctrine, not a generic "AI services" claim).

## 3. Doctrine Moat

Every claim is locked by a test that fails the build if violated.
Eleven non-negotiables, each with a control mapping
(`open-doctrine/CONTROL_MAPPING.md`). Public verification:

- `GET /api/v1/dealix-promise` — the 11 commitments.
- `GET /api/v1/doctrine?version=v1.0.0` — pinned doctrine snapshot.
- `GET /api/v1/holding/charter` — Group operating Charter.
- `GET /api/v1/capital-assets/public` — safe capital-asset projection.
- `GET /api/v1/trust/status` — Shields.io-style trust payload.

## 4. BU Portfolio

Current registered BUs: see `data/business_units.json` (live).
Initial:

- `Dealix Core OS` — status `BUILD`. Owner: founder.
- Reserved future BUs: `Sprint Delivery`, `Trust Services`, `Labs`,
  `Academy`. Names reserved by Brand Architecture (PR13). Not active
  until registered.

## 5. Financial Model (qualitative)

This memo does not disclose absolute SAR / USD figures. Discipline
references:

- **Margin discipline:** `operating_finance_os/margin_by_offer.py` +
  `margin_protection.py`. Offers below floor → protection action.
- **Retainer economics:** `operating_finance_os/retainer_economics.py`.
- **Capital allocation:** 6 buckets in
  `docs/holding/CAPITAL_ALLOCATION_POLICY.md` (must_fund /
  should_test / hold / kill / spinout / acquire). Allocation cycle
  monthly.
- **Hiring discipline:** `operating_finance_os/hiring_triggers.py` +
  `docs/funding/FIRST_3_HIRES.md`. Sequential triggers; no parallel
  hires.

## 6. Use of Funds

See `docs/funding/USE_OF_FUNDS.md`. The principle: capital does not
skip proof. Capital accelerates revenue, trust, delivery
repeatability, evidence infrastructure, partner distribution. Capital
does **not** fund: premature SaaS, marketplace, autonomous external
agents, broad GCC launch before Saudi proof, vanity hiring.

## 7. Hiring Plan

See `docs/funding/HIRING_SCORECARDS.md` + `docs/funding/FIRST_3_HIRES.md`.
Three roles, in order:

1. AI Ops Engineer (after 1 paid Sprint + 2 paying Retainers).
2. Delivery / RevOps Operator (after 3 sprints + scope frozen 30 days).
3. Partnerships / GCC Growth Operator (after 1 partner co-sold a
   paying client + 1 published case study).

## 8. Traction

Honest counters (the verifier refuses to inflate these):

- `outreach_sent_count`: see `data/partner_outreach_log.json`.
- `invoice_sent_count`: see `data/first_invoice_log.json`.
- Capital Assets registered: see `data/capital_asset_index.json`.
- Verifier state: `landing/assets/data/verifier-report.json`.

The current counters reflect pre-Invoice-#1 state. Investors interested
in traction should re-check these counters at the time of diligence
rather than rely on any number quoted in this memo.

## 9. Risks

See `docs/holding/GROUP_RISK_REGISTER.md` for the top-12 risks,
categorized (commercial / operational / regulatory / agentic-AI).
Each has owner, likelihood, impact, mitigation, status.

## 10. Governance

- Board: see `docs/holding/BOARD_OF_DIRECTORS.md` +
  `docs/holding/BOARD_CHARTER.md`.
- Doctrine versioning: `open-doctrine/VERSIONS.md` +
  `scripts/tag_doctrine_version.py`. Major changes require board memo.
- CI gate: `doctrine-gate` job in `.github/workflows/ci.yml` blocks
  merge on any doctrine regression.

## 11. Ask

(Filled in by founder before sending; this template intentionally
leaves the ask blank because the ask is investor-specific.)

## 12. Verification

Investor diligence is self-serve:

1. Read `open-doctrine/11_NON_NEGOTIABLES.md`.
2. Read `docs/holding/HOLDING_CHARTER.md`.
3. Run `python scripts/verify_all_dealix.py` against the cloned repo.
4. Run `python scripts/validate_business_units.py`.
5. Run `python scripts/validate_capital_assets.py`.
6. Check `landing/assets/data/verifier-report.json` for the current
   30+ system state.

If the verifier does not report Overall PASS, the founder will
explain which two real-world gates (Partner Motion, First Invoice
Motion) remain — these are the only honest reasons the verifier can
be at FAIL.
