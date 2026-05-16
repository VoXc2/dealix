# ADR 0010: Organizational Intelligence Dominance as Canonical Overlay

- Status: Accepted
- Date: 2026-05-15
- Decision owners: Dealix core architecture

## Context

Dealix repository contains broad capabilities across `auto_client_acquisition/`, `dealix/`, `api/`, `docs/`, and `evals/`.
We need a single executive-grade operating model that:

1. maps capabilities to a dominance architecture,
2. stays compatible with existing modules,
3. is machine-readable and testable,
4. avoids unsafe refactors and rename churn.

## Decision

Adopt a 10-layer **Organizational Intelligence Dominance** overlay and implement it as:

1. Documentation map: `docs/architecture/ORGANIZATIONAL_INTELLIGENCE_DOMINANCE_AR.md`
2. Code registry: `OI_DOMINANCE_LAYERS` in `auto_client_acquisition/dealix_master_layers/registry.py`
3. Lookup helpers for runtime/readability: `dominance_layer_by_slug()`, `dominance_layer_by_id()`
4. Test coverage ensuring mapping integrity: `tests/test_dealix_master_layers_registry.py`

## Key Architectural Constraints

- **Capability-first, not feature-first**: each layer maps to operational contracts and outcomes.
- **No breaking rename migration**: reuse existing modules via mapping.
- **No root `platform/` Python package**: preserve compatibility with Python stdlib `platform`.
- **Governance defaults remain intact**: no changes to external-action safety principles.

## Consequences

### Positive

- Shared language for strategy, product, and engineering.
- Traceable map from blueprint paths to real implementation.
- Low-risk adoption; no router/import churn.
- CI-verifiable architecture registry.

### Trade-offs

- Overlay introduces a second map (10 layers over existing 12/37 maps).
- Some target blueprint paths remain virtual (documented aliases), not physical folders.

## Follow-up Work

1. Bind release automation to evaluation-dominance gates.
2. Add capability scorecards for each layer.
3. Promote critical workflows to explicit capability contracts.
