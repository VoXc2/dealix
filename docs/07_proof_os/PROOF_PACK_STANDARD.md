# Proof Pack Standard — معيار حزمة الإثبات

> Purpose: define the 14-section schema that every Dealix project must assemble at close, the formula that computes the proof score, and the tier classification that determines how a Proof Pack may be used externally.

A Proof Pack is the artifact that converts work into evidence. Every project — sprint, retainer month, sector engagement — produces exactly one Proof Pack, with a computed proof score and a tier classification. Without a Proof Pack, a project cannot be invoiced, referenced, or used to unlock the next rung.

## The 14 sections — الأقسام الأربعة عشر

```
1.  Executive Summary
2.  Problem
3.  Inputs
4.  Source Passports
5.  Work Completed
6.  Outputs
7.  Quality Scores
8.  Governance Decisions
9.  Blocked Risks
10. Value Metrics
11. Limitations
12. Recommended Next Step
13. Capital Assets Created
14. Appendix
```

Section content rules:

1. **Executive Summary** — one page maximum, bilingual where appropriate. Names the workflow owner, the headline outcome, the proof score, the tier.
2. **Problem** — the written problem statement the client agreed to at intake.
3. **Inputs** — the data, channels, and people involved. Counts only; no raw PII.
4. **Source Passports** — every [Source Passport](../04_data_os/SOURCE_PASSPORT.md) used, listed by `source_id`, `source_type`, `owner`, `sensitivity`, `retention_policy`.
5. **Work Completed** — the workflow steps actually executed, in order, with who/what executed each.
6. **Outputs** — the deliverables (ranked accounts, drafts, reports). Each output carries a `source_ref` back to a passport.
7. **Quality Scores** — DQ score on input, output quality scores per deliverable.
8. **Governance Decisions** — every decision returned by `decide(action, context)`. See [Runtime Governance](../05_governance_os/RUNTIME_GOVERNANCE.md).
9. **Blocked Risks** — every action the governance layer refused, with the reason category (no consent, no passport, guarantee language, etc.).
10. **Value Metrics** — value entries classified per the [Value Ledger](../08_value_os/VALUE_LEDGER.md): Estimated / Observed / Verified / Client-Confirmed.
11. **Limitations** — what the project did *not* do, what could not be measured, what should not be generalized.
12. **Recommended Next Step** — the deterministic recommendation (second sprint, retainer eligibility, remediation, pause).
13. **Capital Assets Created** — every asset deposited into the [Capital Ledger](../09_capital_os/CAPITAL_LEDGER.md). At least one is required.
14. **Appendix** — supporting tables, schema dumps, decision logs (counts only, never raw PII).

## Proof score formula — معادلة درجة الإثبات

The proof score is a single number in `[0, 100]`, computed as a weighted sum of five components.

```
proof_score = round(
    0.25 * source_coverage
  + 0.25 * output_quality
  + 0.20 * governance_integrity
  + 0.15 * value_evidence
  + 0.15 * capital_asset_creation
)
```

Components:

- **source_coverage (25%)** — share of outputs that carry a valid `source_ref` to a Source Passport. Missing references reduce the score linearly.
- **output_quality (25%)** — aggregate of per-deliverable quality scores: ranking precision, draft acceptance rate at review, bilingual completeness.
- **governance_integrity (20%)** — share of governance decisions that resolved cleanly (no `ESCALATE` left unresolved, no `BLOCK` events on actions that should have been refusable upstream).
- **value_evidence (15%)** — strength of the value classification: Observed entries with measurement, Verified entries with cross-checks, Client-Confirmed entries where applicable.
- **capital_asset_creation (15%)** — count and quality of capital assets deposited. Zero deposits caps this component at 0.

Each component is itself a number in `[0, 100]`. Components are reproducible: given the same project state, two recomputations must yield the same proof score.

## Tier classification — التصنيف

The score maps deterministically to a tier:

| Score range | Tier | What it unlocks |
|-------------|------|-----------------|
| ≥ 85 | **case candidate** | Eligible to become a public case study after client confirmation. |
| 70 – 84 | **sales support** | May be referenced in sales conversations (anonymized) but not published. |
| 55 – 69 | **internal learning** | Used inside Dealix for capital review and team learning. Not externally referenced. |
| < 55 | **weak** | Treated as a productization failure. Triggers a retrospective. Cannot be invoiced as a full deliverable without remediation. |

A high score does not authorize external use by itself. External use also requires:

- The Source Passports to have `external_use_allowed = true` or an explicit override approval.
- A Client-Confirmed value entry, if value numbers are referenced.
- A governance decision of `ALLOW` for the specific publication action.

## How the Proof Pack is built — كيف تُجمَّع

The pack is assembled by `proof_os.proof_pack.assemble()`. The function:

- Reads inputs, outputs, governance decisions, value entries, and capital deposits from the project state.
- Renders the 14 sections in fixed order, bilingual where applicable.
- Computes the proof score and tier.
- Writes the result to the project's proof archive with a content hash.
- Calls `capital_os.capital_ledger.add_asset(...)` for each asset, enforcing the "at least one" rule.

If the assembler cannot locate at least one capital asset, it raises and the project does not close. This enforces the constitutional rule "no project without a Capital Asset". See [NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md).

## What a Proof Pack is not — ما ليست حزمة الإثبات

- Not a marketing artifact. Marketing artifacts may be derived from it, subject to tier and consent.
- Not a slide deck. The Proof Pack is structured data first, rendered second.
- Not negotiable in scope. All 14 sections are required, every project, every time.

## Cross-references

- [Source Passport](../04_data_os/SOURCE_PASSPORT.md), [Runtime Governance](../05_governance_os/RUNTIME_GOVERNANCE.md), [Value Ledger](../08_value_os/VALUE_LEDGER.md), [Capital Ledger](../09_capital_os/CAPITAL_LEDGER.md).
