# Execution Dominance Engine

Purpose: run, coordinate, monitor, and recover workflows under governance.

## Core responsibilities

- Orchestrate idempotent workflow steps.
- Manage retries, queue semantics, and compensation logic.
- Provide deterministic recovery after failures.

## Required linked modules

- `platform/orchestration`
- `platform/queues`
- `platform/compensation_logic`
- `platform/recovery_engine`
