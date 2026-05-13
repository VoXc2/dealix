# Lead Intelligence Sprint — QA Checklist

Project ships only when ALL gates pass AND Quality Score ≥ 80 (see W6.T36).

## Business QA
- [ ] Problem statement explicit (in customer's words).
- [ ] Output speaks to executive decision-maker (Head of Sales / CEO).
- [ ] Numeric KPI defined (top-50 delivered? pipeline value created?).
- [ ] Clear next action surfaced for sales reps.
- [ ] Upsell path documented (Monthly RevOps / Pipeline Setup).

## Data QA
- [ ] Every record has a source or is flagged.
- [ ] Duplicates handled (dedupe report attached).
- [ ] Missing-field counts documented.
- [ ] PII detected via `dealix/trust/pii_detector.py` (Card / IBAN auto-blocked).
- [ ] Lawful basis (PDPL Art. 5) recorded.
- [ ] Data Quality Score ≥ 90 on cleaned dataset.

## AI QA (scoring + drafts)
- [ ] Every score has a feature-level rationale (LeadScore.features).
- [ ] Top-10 outreach drafts reviewed by a human.
- [ ] No "نضمن / guarantee" or other forbidden claims (auto-checked via `dealix/trust/forbidden_claims.py`).
- [ ] AR tone appropriate for sector (not literal MT).
- [ ] Edge-case sample tested: empty name, missing CR, Arabic-only record.

## Compliance QA
- [ ] PDPL Art. 13 notice text present in every draft.
- [ ] No PII surfaced in the executive report.
- [ ] Approval log captured (per draft → approved / rejected events).
- [ ] Audit trail queryable in event store (filter on project_id).

## Delivery QA
- [ ] All deliverables present (dataset / scoring / Mini CRM / report / proof pack).
- [ ] Executive report is clear to a non-technical reader.
- [ ] Customer knows the next 30-day action (in writing).
- [ ] Handoff session scheduled or completed.
- [ ] Renewal proposal drafted (Monthly RevOps suggestion).

## Reviewer
- Owner: HoCS.
- Counter-sign: CRO for SOWs > SAR 15,000.
