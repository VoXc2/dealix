# Dealix Market + Commercial Tests

Pytest suite that enforces the non-negotiable safety + commercial rules of the
Market Production OS. The rules live in `tests/_loaders.py` (the authoritative
Python spec) and are mirrored at runtime by `scripts/_lib/dealix.js`.

## Run

```bash
pip install -r requirements-dev.txt   # pytest + PyYAML
pytest                                # from repo root
```

The Node gate is cross-checked from `test_gtm_quality_gate.py` (skipped only if
`node` is not on PATH). The commercial scripts can be exercised directly with:

```bash
npm run commercial:all
node scripts/draft-quality-gate.js --eval
```

## What is covered

| Test | Guarantees |
|------|-----------|
| test_gtm_quality_gate | draft gate verdicts match labeled evals; production drafts pass; P0 not send-ready |
| test_outreach_no_guaranteed_claims | zero forbidden claims in outbound artifacts |
| test_no_guaranteed_revenue_claims | specific banned phrases ("نضمن زيادة المبيعات", "10x revenue") are caught |
| test_outreach_unsubscribe_required | cold drafts must carry opt-out |
| test_outreach_suppression_blocks_send | suppressed recipients can never be send-ready |
| test_commercial_offer_mapping | every pain maps to a real catalog offer; offers well-formed |
| test_pricing_requires_approval | final price needs approval; custom scope ≠ starter price |
| test_proposal_requires_qualified_opportunity | no proposal without a qualified, mapped opportunity |
| test_walk_away_rules | spam / guaranteed-sales / no-approval clients are disqualified |
| test_partner_model_margin_rules | partner deals respect the margin floor |
