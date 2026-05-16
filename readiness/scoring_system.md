# Dealix Readiness Scoring System (Release 0)

## Scoring objective

Use one deterministic scorecard to decide if a layer, workflow, or release can ship.

## Core equation

`Layer is real = Code + Tests + Evals + Observability + Governance + Rollback + Metrics + Business Impact`

Each dimension is scored from `0` to `5`:

- `0` = missing
- `1` = draft only
- `2` = partial implementation
- `3` = implemented with known gaps
- `4` = production-capable for pilot
- `5` = enterprise-hardened and repeatedly proven

Maximum per layer: `40` points.

## Release readiness thresholds

- **Not ready:** `< 24/40`
- **Pilot ready:** `24-31/40` and no dimension below `3`
- **Enterprise ready candidate:** `32-36/40` and all governance/evals gates pass
- **Mission-critical ready candidate:** `>= 37/40` with load-tested rollback + incident response evidence

## Mandatory gate conditions

The release is blocked if any of these are true:

1. Governance score < 3
2. Rollback score < 3
3. Evals score < 3
4. Observability score < 3
5. Business impact score < 2

## Release 0 + 1 minimum scoring target

- Target layer minimum: `>= 26/40`
- Global hard-stop gates enabled for:
  - tenant isolation checks
  - RBAC checks
  - audit logging coverage
  - rollback drill completion

## Evidence format

Each score update must attach:

1. code reference (path/symbol),
2. test output,
3. eval output or risk note,
4. observability evidence (trace/log/metric),
5. approval/audit evidence where applicable,
6. rollback drill result,
7. KPI trend and expected business effect.

No evidence means no score change.
