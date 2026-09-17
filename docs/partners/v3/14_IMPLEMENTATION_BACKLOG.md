# Partner Network V3 — L0–L4 Implementation Backlog

## P0 — Legal / Truth Foundation
- [x] Add `legal_classification` policy + verifier.
- [x] Add `no_mlm_downline` invariant and tests.
- [x] Add non-Saudi authorization HOLD.
- [x] Add employment-misclassification signal HOLD.
- [x] Add electronic-ad disclosure/claims lint.
- [x] Add VAT/tax-profile activation status without inventing tax treatment.
- [ ] Persist versioned partner-terms acceptance receipt in canonical Company Machine (policy version enforcement is implemented).

## P0 — Rights Ledger
- [ ] Deal Registration immutable receipt.
- [ ] Attribution expiry/extension evidence.
- [ ] Commission statement breakdown.
- [ ] Dispute case object + evidence + resolution receipt.
- [ ] Policy-version pinning per deal.
- [ ] payout receipt verification.

## P1 — Recruitment System
- [ ] `/partners` bilingual responsive landing.
- [ ] opt-in application.
- [ ] recruiter Candidate Radar with RESEARCH_ONLY status.
- [ ] Persist micro-certification results; activation gate requiring certification is implemented.
- [ ] sector/motion routing.
- [ ] QR/referral-to-program attribution without recruitment commission.

## P1 — Partner Portal
- [ ] mobile-first PWA/RTL.
- [ ] partner profile/compliance status.
- [ ] register opportunity.
- [ ] view protected attribution window.
- [ ] commission statements.
- [ ] Build asset-library UI; approved-asset/disclosure enforcement is implemented.
- [ ] dispute submission.

## P1 — Growth Factory
- [ ] content templates AR/EN.
- [ ] campaign asset approval state machine.
- [ ] UTM/referral link generation.
- [ ] creator disclosure injection.
- [ ] sector landing pages.
- [ ] webinar/event QR opt-in.

## P2 — Open Source Evaluations
- [ ] RefRef security/license spike.
- [ ] Refferq security/license spike.
- [ ] Documenso signing/security spike.
- [ ] Formbricks intake/certification spike.
- [ ] Dub attribution spike.
- [ ] decide ADOPT / INTEGRATE / COPY-PATTERN / REJECT after security/license/data-location spikes.

## Acceptance
- no second CRM/economic ledger.
- all tests fail-closed.
- no secret literals.
- no automatic bank payout.
- no external send/publish in tests.
- accessibility + mobile + RTL.
- audit receipts for all material state changes.