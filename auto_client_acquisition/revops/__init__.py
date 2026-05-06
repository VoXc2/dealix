"""RevOps layer — revenue truth, pipeline aggregates, finance brief (deterministic).

Draft invoices and verbal interest do not count as revenue. Payment evidence rules
stay aligned with ``revenue_pipeline.stage_policy``.
"""
from auto_client_acquisition.revops.finance_brief import build_finance_brief
from auto_client_acquisition.revops.margin import MarginInputs, estimate_margin
from auto_client_acquisition.revops.revenue_truth import build_revops_truth_snapshot

__all__ = [
    "build_finance_brief",
    "build_revops_truth_snapshot",
    "MarginInputs",
    "estimate_margin",
]
