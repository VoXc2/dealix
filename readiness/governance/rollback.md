# Governance Layer — rollback

- Rollback trigger:
  - Layer status flips from PASS to FIX after code/config change.

- Immediate actions:
  1. Revert last deployment/config affecting this layer.
  2. Re-run enterprise validation and targeted tests.
  3. Open incident log with missing evidence paths.

- Recovery acceptance criteria:
  - `LAYER_GOVERNANCE_STATUS=PASS`
  - `CROSS_LAYER_STATUS=PASS`
