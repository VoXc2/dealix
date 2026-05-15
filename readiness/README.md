# Enterprise Layer Validation System

This directory defines the 8-layer enterprise readiness model for Dealix.

## Layers
- `foundation` — owner `Platform + Security`
- `agents` — owner `Agent Platform`
- `workflows` — owner `Delivery + Platform`
- `memory` — owner `Knowledge + Data`
- `governance` — owner `Governance + Compliance`
- `observability` — owner `Reliability + Platform`
- `evals` — owner `Quality + Product`
- `executive` — owner `CEO Office + Reporting`

## Verification
- Non-strict: `python3 scripts/verify_enterprise_layer_readiness.py`
- Strict gate: `python3 scripts/verify_enterprise_layer_readiness.py --strict`
