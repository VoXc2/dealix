"""Eval OS — the 4-category evaluation taxonomy and pack loader.

Retrieval, response, workflow, and business quality. Pairs the
machine-readable metric catalog with the declarative YAML packs in
``evals/``.
"""

from __future__ import annotations

from auto_client_acquisition.eval_os.pack_loader import (
    TAXONOMY_PACKS,
    list_packs,
    load_pack,
    validate_pack,
    validate_taxonomy_packs,
)
from auto_client_acquisition.eval_os.taxonomy import (
    METRIC_IDS,
    EvalCategory,
    EvalMetric,
    MetricDirection,
    get_metric,
    list_metrics,
    metrics_for_category,
)

__all__ = [
    "METRIC_IDS",
    "TAXONOMY_PACKS",
    "EvalCategory",
    "EvalMetric",
    "MetricDirection",
    "get_metric",
    "list_metrics",
    "list_packs",
    "load_pack",
    "metrics_for_category",
    "validate_pack",
    "validate_taxonomy_packs",
]
