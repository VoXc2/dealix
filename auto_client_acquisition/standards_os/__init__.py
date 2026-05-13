"""Dealix Standards OS — D-GAOS sub-standards as typed surfaces."""

from __future__ import annotations

from auto_client_acquisition.standards_os.qa_standard import (
    QA_DIMENSIONS,
    QADecision,
    QAResult,
    classify_qa_score,
)
from auto_client_acquisition.standards_os.standards_index import (
    DEALIX_SUB_STANDARDS,
    SubStandard,
)

__all__ = [
    "QA_DIMENSIONS",
    "QADecision",
    "QAResult",
    "classify_qa_score",
    "DEALIX_SUB_STANDARDS",
    "SubStandard",
]
