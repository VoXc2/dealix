# Organizational Operating Fabric

Purpose: unify workflows, agents, context, governance, execution, and analytics in one runtime fabric.

## Core responsibilities

- Route workflow events through a shared event mesh contract.
- Resolve context from identity, history, and active policy state.
- Maintain organizational state snapshots for deterministic decisions.

## Required linked modules

- `platform/event_mesh` (event routing contract)
- `platform/context_engine` (context resolution contract)
- `platform/organizational_state` (state snapshot contract)
