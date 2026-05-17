"""Pluggable adapters that read existing Dealix infrastructure.

Each adapter returns an ``AdapterResult``. When a source is not wired or
holds no data, the adapter returns ``Status.UNKNOWN`` with ``value=None``
— it never fabricates a number.
"""
from __future__ import annotations

from auto_client_acquisition.assurance_os.adapters.approval_adapter import (
    ApprovalAdapter,
)
from auto_client_acquisition.assurance_os.adapters.base import BaseAdapter
from auto_client_acquisition.assurance_os.adapters.claim_adapter import ClaimAdapter
from auto_client_acquisition.assurance_os.adapters.evidence_adapter import (
    EvidenceAdapter,
)
from auto_client_acquisition.assurance_os.adapters.kpi_adapter import KpiAdapter
from auto_client_acquisition.assurance_os.adapters.pipeline_adapter import (
    PipelineAdapter,
)
from auto_client_acquisition.assurance_os.adapters.scorecard_adapter import (
    ScorecardAdapter,
)

__all__ = [
    "BaseAdapter",
    "ApprovalAdapter",
    "ClaimAdapter",
    "EvidenceAdapter",
    "KpiAdapter",
    "PipelineAdapter",
    "ScorecardAdapter",
]
