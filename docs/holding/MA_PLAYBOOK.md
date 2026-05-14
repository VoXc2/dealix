# M&A Playbook — Dealix Group

> Companion: `ACQUISITION_THESIS.md` (criteria) and
> `SUBSIDIARY_ONBOARDING.md` (post-close 90 days).

## Six Stages

Every acquisition passes through the six stages in order. Each stage
names the **artifact** it must produce. Skipping an artifact blocks the
next stage.

### Stage 1 — Thesis

Required artifact: a **one-page thesis** stored under
`data/_state/ma/<target_slug>/thesis.md`.

Contents: which of the four ACQUISITION_THESIS criteria the target
satisfies, the sector fit narrative, the named board sponsor.

### Stage 2 — Screen

Required artifact: a **screen scorecard** referencing
`auto_client_acquisition/board_decision_os/board_scorecards.py`
(`OfferScorecardDimensions` + `ProductizationScorecardDimensions`).
Stored under `data/_state/ma/<target_slug>/screen.json`.

Stage 2 outcome: PROCEED / HOLD / REJECT. HOLD or REJECT close the
file.

### Stage 3 — Diligence

Required artifact: a **diligence pack** under
`data/_state/ma/<target_slug>/diligence/`:

- Doctrine compatibility audit (forbidden-feature scan against the
  target's repo or operations description).
- Financial diligence (revenue confirmation, margin, runway —
  reuses `operating_finance_os` modules conceptually).
- Customer concentration (no single customer > 40%).
- Legal compatibility (sketch only — formal review external).

### Stage 4 — Letter of Intent

Required artifact: a **signed LOI** referenced (not stored) in
`data/_state/ma/<target_slug>/loi.md`. Public surface: NONE; LOIs are
internal until close.

### Stage 5 — Close

Required artifacts at close:

- New `data/business_units.json` entry registered via
  `scripts/register_business_unit.py --really-this-is-a-bu`.
- New BU charter under `docs/holding/units/<slug>.md`.
- Doctrine adoption certificate from
  `partner-kit/DOCTRINE_ADOPTION_CHECKLIST.md`.
- Capital Asset entry of type `governance_rule` recording the
  acquisition rationale (no amount in the public projection).

### Stage 6 — Post-Close (90-day integration)

Follow `SUBSIDIARY_ONBOARDING.md`. Required milestones at 30 / 60 /
90 days.

## Forbidden

- Acquisitions without board memo when ≥ 6 months retainer revenue
  (see ACQUISITION_THESIS Decision Authority).
- Stock-only deals.
- Acquisitions whose Stage 3 diligence surfaces any of the eleven
  non-negotiables in active practice. No "fix-after-close" reasoning.

## Verification

The artifact list in this document is locked by
`tests/test_ma_playbook_lists_required_artifacts.py`.
