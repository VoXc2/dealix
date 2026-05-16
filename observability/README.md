# Observability Baseline

Every governed workflow run must emit:

- traceable run id (`run_*`)
- step-level latency metrics
- workflow status metrics (completed, pending_approval, denied)
- audit trail entries per control point

Baseline implemented in:

- `dealix/workflows/lead_qualification.py`
