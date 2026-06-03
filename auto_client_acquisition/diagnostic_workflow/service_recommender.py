"""Pick the customer-facing bundle for a given diagnostic.

Thin delegate over ``company_brain_v6.recommend_service`` so the
workflow has a single canonical entry point.
"""
from __future__ import annotations

from auto_client_acquisition.company_brain_v6 import recommend_service as _recommend
from auto_client_acquisition.diagnostic_workflow.schemas import DiagnosticBundle


def recommend_service(bundle: DiagnosticBundle) -> str:
    """Return the customer-facing bundle id for the diagnostic."""
    return _recommend(bundle.brain)
