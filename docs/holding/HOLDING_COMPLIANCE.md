# Holding-Level Compliance — Dealix Group

## Scope

Group-level compliance covers:

1. **PDPL (Saudi Personal Data Protection Law).** Personal data
   handling, consent, lawful basis, cross-border. See
   `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` and the existing
   integrations under `integrations/pdpl.py`.
2. **SDAIA guidance.** Saudi AI Authority guidance on responsible AI
   use. Mapped to commitments #3 (Governance Runtime) and #9 (Agent
   Identity).
3. **Agent runtime safety.** Identity-card requirement, kill-switch,
   tool allow-list. Per commitments #9 and #11.
4. **Cross-border data transfer.** Pre-cleared only for the documented
   GCC priority sequence (`docs/gcc-expansion/GCC_COUNTRY_PRIORITY_MAP.md`).
5. **No-scraping, no-cold-WhatsApp, no-LinkedIn-automation.** Per
   commitments #5, #6, #7. Locked by tests in
   `tests/test_no_*.py`.

## Reviewing Compliance

The board's Audit Committee owns this document and reviews quarterly.
The annual report (`scripts/render_annual_report.py` Section 7)
includes a Doctrine Discipline summary that incorporates compliance
state.

## Out of Scope

This document is doctrine, not legal advice. Formal legal review is
outside-the-repo and required before any:

- Entity formation in a new jurisdiction.
- Cross-border data transfer with a real client dataset.
- Customer contract that materially exceeds the Sprint scope.

## Verification

- The doctrine-gate CI job (PR4) runs:
  `tests/test_no_cold_whatsapp.py`,
  `tests/test_no_linkedin_automation.py`,
  `tests/test_no_scraping_engine.py`,
  `tests/test_no_guaranteed_claims.py`,
  `tests/test_no_forbidden_features_in_diff.py`,
  `tests/test_pii_external_requires_approval.py`,
  `tests/test_no_source_passport_no_ai.py`.
- Any commit that introduces an active forbidden feature fails CI.
