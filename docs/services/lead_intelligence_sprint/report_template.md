# Executive Report Template — Lead Intelligence Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Revenue Capability Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [report_template_AR.md](./report_template_AR.md)

## Context
This file defines the executive report Dealix produces at the close of every Lead Intelligence Sprint. It is the artifact the client's CEO/GM/sales lead reviews to decide whether to continue (retainer), expand (Pilot Conversion), or pause. The report links the operating layers via `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and pairs with `docs/templates/PROOF_PACK_TEMPLATE.md`.

## Structure

### 1. Executive Summary
- One paragraph stating the outcome: what was cleaned, ranked, drafted, and proven.
- One sentence on the next-best step for the buyer.

### 2. Data Quality Before / After
- Records imported · Records valid · Records invalid · Duplicates found · PII fields detected.
- Source-coverage score before vs after · Completeness · Freshness · Consistency.
- Overall Data Readiness Score (numeric) with band (Ready / Usable with review / Needs cleanup / Not ready).

### 3. Top 50 Ranked Accounts (summary)
- Sample table (top 10 visible in the executive report; full 50 in the appendix).
- Columns: rank · company · sector · city · final score · one-line reason · recommended action.

### 4. Top 10 Immediate Actions
- Per account: owner · channel · suggested first touch · expected objection · fallback.

### 5. Outreach Draft Pack Summary
- Count of drafts produced (intro / follow-up / referral / re-engagement).
- Claims-safety check status (passed / blocked rules).
- All drafts flagged `draft_only` and require human approval before send.

### 6. Governance Events
- Blocked actions count and reasons (e.g., cold WhatsApp blocked, unsourced PII redacted).
- Approvals captured.
- Audit events written.

### 7. Business Value
- Revenue Value · Time Value · Quality Value · Risk Value · Knowledge Value (with metric + evidence).

### 8. Risks & Limitations
- What this sprint did not measure.
- Open data gaps.
- Recommended follow-up controls.

### 9. Recommended Next Step
- One of: Continue (Monthly RevOps OS) · Expand (Pilot Conversion Sprint) · Pause (no proof yet).
- Justification tied to the metrics above.

## Output rules
- Bilingual: executive summary in Arabic + English.
- No guaranteed claims. No fabricated metrics.
- Every metric must trace back to an audit event or proof event ID.
- File size ≤ 15 pages including appendix.
- Anonymized version filed in `docs/case_studies/` after client approval.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Cleaned accounts, scoring output, draft pack, governance events, proof events | Executive Report PDF + bilingual summary | Revenue Capability Lead | End of sprint |

## Metrics
- Executive summary clarity (reviewed in QA)
- Number of metrics with source-traceable evidence
- Time to deliver after sprint close (target ≤ 24 hours)

## Related
- `docs/services/lead_intelligence_sprint/proof_pack_template.md` — proof events captured
- `docs/services/lead_intelligence_sprint/qa_checklist.md` — review checklist
- `docs/templates/PROOF_PACK_TEMPLATE.md` — canonical proof pack template
- `docs/quality/QUALITY_STANDARD_V1.md` — quality standard
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
