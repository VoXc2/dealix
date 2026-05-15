# Dealix Agentic Economic Operating Layer

This folder is the contract surface for the final civilizational systems (46-55).

## Objective

Dealix is measured by **organizational dependency**, not model sophistication:

- Can the organization run critical operations without Dealix?
- Are core workflows executed, governed, and auditable through Dealix?
- Does the system survive failures through pause, reroute, rollback, and recovery?

## Final systems map

The canonical registry and path matrix lives in:

- `platform/final_civilization_model.yaml`
- `auto_client_acquisition/agentic_economic_os/systems_registry.py`

## Dependency gates

Infrastructure status is reached only when all gates are true:

1. `ODI >= 75`
2. `No-Bypass Rate >= 98%`
3. `Rollback Coverage >= 90%`
4. `Audit Coverage >= 95%`
5. `Executive Dependency >= 60%`

Scoring logic is implemented in:

- `auto_client_acquisition/agentic_economic_os/dependency_engine.py`
