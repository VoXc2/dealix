# Internal Audit — Dealix Group

## Function

Internal audit is a quarterly **self-audit** + an annual **external
review** (when capital allows). The audit covers:

1. **Doctrine adherence.** Every BU's monthly snapshot matches a
   board-reviewed recommendation. Doctrine version pinned where
   claimed.
2. **Capital asset integrity.** Every entry passes the validator;
   public-safe projection contains no forbidden fields.
3. **Marker honesty.** `outreach_sent_count` and `invoice_sent_count`
   match `len(entries)` (the doctrine-as-code test).
4. **CI gates.** All drift gates green; no bypass commits.

## Quarterly Self-Audit

Owner: Audit Committee (until filled, founder + 1 advisor).

Steps:
1. Run `python scripts/verify_all_dealix.py` and snapshot the JSON.
2. Run `python scripts/validate_business_units.py`.
3. Run `python scripts/validate_capital_assets.py`.
4. Review the Group Risk Register (statuses + last-reviewed dates).
5. Compare against prior quarter's snapshot. Material drift triggers
   a board memo.
6. Output: a one-page Markdown stored at
   `data/_state/audit/<YYYY-Qn>.md`.

## Annual External Review

When the holding has the capital and a paying client base, the annual
review is conducted by an external firm:
- Reviews the doctrine-locked test suite.
- Reviews the verifier output against the underlying state.
- Confirms public surface safety (no PII leaks, ratio-only cap-table
  public projection).
- Sign-off: a Capital Asset entry of type `governance_rule`.

## Audit Independence

- Self-audit reviewers should rotate annually once 2+ advisor seats
  filled.
- External review firm rotates every 3 years.

## Verification

- `tests/test_marker_files_have_git_provenance.py` — every entry has
  audit-grade provenance.
- `tests/test_no_inflated_marker_counts.py` — counters match entries.
- `tests/test_doctrine_control_mapping_complete.py` — the 11
  commitments map to actual artifacts.
