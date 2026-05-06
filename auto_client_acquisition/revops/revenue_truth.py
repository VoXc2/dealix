"""Canonical RevOps revenue-truth labels for dashboards."""
from __future__ import annotations

from typing import Any


def build_revops_truth_snapshot(pipeline_summary: dict[str, Any]) -> dict[str, Any]:
    """Rules mirror ``revenue_pipeline/revenue_truth.py`` snapshot semantics.

    - Draft invoice ≠ revenue (handled at invoice layer — no SAR until paid).
    - Verbal interest ≠ revenue (pipeline stages enforce evidence).
    """
    paid_n = int(pipeline_summary.get("paid", 0))
    commitments_n = int(pipeline_summary.get("commitments", 0))
    total_revenue_sar = int(pipeline_summary.get("total_revenue_sar", 0))
    revenue_recorded = paid_n >= 1 and total_revenue_sar > 0

    return {
        "schema_version": 1,
        "draft_invoice_is_revenue": False,
        "verbal_interest_is_revenue": False,
        "diagnostic_delivered_is_revenue": False,
        "written_commitment_is_commitment": commitments_n >= 1,
        "payment_evidence_is_revenue": revenue_recorded,
        "pipeline_paid_count": paid_n,
        "pipeline_commitments_count": commitments_n,
        "total_revenue_sar": total_revenue_sar,
    }
