# Server / Company Machine Blueprint — Partner Network V3

## Do not create a second Company Machine
Partner Network plugs into canonical Dealix Company Machine, Opportunity Graph, Approval Queue, Proof Ledger and Economic Truth.

## Required Modules
1. Partner Application Intake.
2. Legal Classification Engine.
3. Consent & Privacy Evidence Store.
4. Partner Identity/Business Verification references.
5. Terms Versioning + Acceptance Ledger.
6. Micro-Certification Engine.
7. Partner ID / referral link/code service.
8. Deal Registration + duplicate/fingerprint engine.
9. Attribution Graph.
10. NCCR + Commission Engine.
11. Clearing / Adjustment Ledger.
12. Payout Approval Queue (no bank execution).
13. Partner Portal API/UI.
14. Recruitment Content Factory.
15. Compliance/Claims Scanner.
16. Fraud/Anomaly detection.
17. Dispute workflow.
18. Partner Performance + concentration risk.

## Core Tables
`partners`, `partner_legal_profiles`, `partner_consents`, `partner_agreement_acceptances`, `partner_certifications`, `partner_channels`, `deal_registrations`, `attribution_events`, `commission_events`, `commission_adjustments`, `payout_staging`, `payout_receipts`, `partner_disputes`, `claims_registry`, `campaign_assets`, `compliance_incidents`, `policy_versions`.

## Hard Invariants
- public_contact != consent
- research_candidate != partner
- application != activation
- registration != accepted attribution
- won != cash
- cash != revenue unless finance truth recognizes it
- projected_commission != eligible_commission
- eligible != approved
- staged_not_paid != paid
- partner != employee unless classified
- recruiter != downline sponsor
- government_opportunity = compliance_hold
- non_saudi_independent_activity = hold until authorization proven

## Automation Jobs
### Daily
- reconcile applications and classifications
- expire stale attribution windows
- duplicate/fraud scan
- detect consent withdrawals
- reconcile collections vs commission projections
- content/claim lint
- partner action queue

### Weekly
- partner activation cohort
- dispute SLA report
- commission aging
- compliance incidents
- concentration risk
- recruiter funnel quality
- top sector opportunities

### Monthly
- policy/version review
- tax/VAT profile refresh prompts
- legal exceptions audit
- inactive partner cleanup review
- open-source dependency/security review

## API Endpoints — Draft
`POST /partners/apply`
`POST /partners/{id}/consents`
`POST /partners/{id}/accept-terms`
`POST /partners/{id}/certifications`
`POST /partner-deals/register`
`GET /partner-deals/{id}`
`GET /partners/{id}/commissions`
`POST /partner-disputes`
`GET /partner-assets`

All mutation endpoints require authenticated actor, policy version, idempotency key and audit receipt.

## Observability
Metrics:
- opt-in application → certified activation
- certified → first accepted deal
- accepted deal → discovery
- discovery → quote
- quote → verified collection
- collection → commission paid
- time-to-first-deal
- NCCR/partner
- compliance incidents/100 partners
- dispute rate and resolution time
- partner concentration HHI/top-10 share