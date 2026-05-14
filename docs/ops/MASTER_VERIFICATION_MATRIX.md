# Master Verification Matrix — Wave 19 Recovery

This matrix is the canonical reference for the difference between
build-complete and company-complete in Dealix.

## How To Run

```
python scripts/verify_all_dealix.py
python scripts/verify_all_dealix.py --json
```

Exit code 0 means all systems pass at score ≥ 3. CEO-complete requires
Partner Motion AND First Invoice Motion at 5/5, which by definition
requires real founder-confirmed market actions (not just artifacts).

## Scoring Rubric (0..5)

| Score | Meaning |
|-------|---------|
| 0 | Nothing present |
| 1 | Partial artifact, dishonest log, or doctrinal violation |
| 2 | Artifact present but missing required content |
| 3 | Runbook + honest log present; market action not yet taken |
| 4 | Full evidence, no market action required for this system |
| 5 | Real founder-confirmed market action logged |

## Systems

| System | Source Of Truth | Score-5 Requirement |
|--------|------------------|---------------------|
| Offer Ladder | docs/sales-kit/INVESTOR_ONE_PAGER.md | one-pager + Ladder + discipline (max 4/5 for artifact-only) |
| Founder Command Center | landing/founder-command-bus.html + data/founder_command_center_status.json | marker present + page rendered (max 4/5 in repo) |
| Partner Motion | docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md + data/anchor_partner_pipeline.json + data/partner_outreach_log.json | at least one founder-confirmed outreach entry |
| First Invoice Motion | docs/ops/FIRST_INVOICE_UNLOCK.md + data/first_invoice_log.json | at least one invoice sent (4/5) or paid (5/5) |
| Funding Pack | docs/funding/FUNDING_MEMO.md, USE_OF_FUNDS.md, HIRING_SCORECARDS.md, FIRST_3_HIRES.md, INVESTOR_QA.md | discipline language + Do-Not-Hire gates (max 4/5 for artifact-only) |
| GCC Expansion | docs/gcc-expansion/GCC_EXPANSION_THESIS.md + COUNTRY_PRIORITY_MAP + GO_TO_MARKET_SEQUENCE | Saudi-beachhead lock language present (max 4/5 for artifact-only) |
| Open Doctrine | open-doctrine/README.md + 11_NON_NEGOTIABLES.md + CONTROL_MAPPING.md | secret-clean public doctrine (max 4/5 for artifact-only) |

## Honest Logging Rules

These rules are enforced by `scripts/verify_all_dealix.py` and the
matching pytest files. They exist so that the marker JSON cannot lie.

- `partner_outreach_log.json` — `outreach_sent_count` MUST equal
  `len(entries)`. If 0, `ceo_complete` MUST be false.
- `first_invoice_log.json` — `invoice_sent_count` MUST equal
  `len(entries)`. `invoice_paid_count` MUST be ≤ `invoice_sent_count`.

If a log diverges from its entries, the verifier downgrades the system
to FAIL with score 2 ("log dishonest").

## What CEO-Complete Means

CEO-complete is NOT a celebration. It is a single signal that the
operating system has demonstrably crossed from build to market:
at least one anchor partner outreach has been sent and recorded, AND
at least one invoice has been sent. Nothing else clears that bar.
