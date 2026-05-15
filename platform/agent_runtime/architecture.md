# Agent Runtime Architecture

## Runtime Responsibilities

The runtime executes governed agent actions with:
- explicit identity,
- tool-level permissions,
- memory scope controls,
- risk-aware approval routing,
- evaluation and rollback controls.

## Core Runtime Components

1. Agent Registry (identity, version, permissions, risk profile).
2. Tool Registry (allowed tools, risk class, side-effect class).
3. Policy Guard (pre-action checks).
4. Approval Hook (human-in-the-loop for high risk).
5. Memory Scope Guard (tenant and domain boundaries).
6. Runtime Observability emitter (trace, logs, metrics).

## Mandatory Runtime Gates

| Gate ID | Requirement | Test ID |
|---|---|---|
| G-ART-001 | agent cannot call unauthorized tool | T-ART-001 |
| G-ART-002 | memory access remains scope-safe | T-ART-002 |
| G-ART-003 | high-risk action requires approval | T-ART-003 |
| G-ART-004 | runtime decision logged with trace correlation | T-ART-004 |
| G-ART-005 | agent version can rollback safely | T-ART-005 |

## Runtime State Model

- `active`: normal execution
- `watch`: elevated monitoring
- `restricted`: no external side effects
- `killed`: emergency halt

Transition rules are policy-driven and auditable.

## Minimum Per-Agent Control Pack

- `agent.yaml`
- `system_prompt.md`
- `tools.md`
- `permissions.md`
- `risk_profile.md`
- `evals.md`
- `kpis.md`
- `rollback.md`

These files are required before promoting a new production-grade agent.
