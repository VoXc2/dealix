"""Customer-safe summarizer for the unified operating graph.

Produces a bilingual short summary suitable for the customer portal.
Uses customer_safe_label and hide_internal_terms to scrub anything
internal before display.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.integration_upgrade import (
    customer_safe_label,
    hide_internal_terms,
)
from auto_client_acquisition.unified_operating_graph.schemas import UnifiedGraph


def summarize_graph_for_customer(graph: UnifiedGraph) -> dict[str, Any]:
    """Customer-facing short summary. Arabic primary, English secondary.

    Returns: { 'headline_ar', 'headline_en', 'counts_by_type', 'data_status' }
    """
    counts: dict[str, int] = {}
    for n in graph.nodes:
        counts[n.node_type] = counts.get(n.node_type, 0) + 1

    bilingual_counts: list[dict[str, Any]] = []
    for node_type, count in counts.items():
        label = customer_safe_label(node_type)
        bilingual_counts.append({
            "node_type": node_type,
            "count": count,
            "label_ar": label["label_ar"],
            "label_en": label["label_en"],
        })

    # Headline depends on data_status
    if graph.is_empty() or graph.data_status == "insufficient_data":
        headline_ar = "لا توجد بيانات تشغيليّة كافية بعد."
        headline_en = "Not enough operational data yet."
    elif graph.data_status == "partial":
        headline_ar = (
            f"تتبّع {len(graph.nodes)} عنصر تشغيلي — بعض الأقسام في وضع التدهور."
        )
        headline_en = (
            f"Tracking {len(graph.nodes)} operational items — some sections degraded."
        )
    else:
        headline_ar = f"تتبّع {len(graph.nodes)} عنصر تشغيلي عبر {len(counts)} نوع."
        headline_en = f"Tracking {len(graph.nodes)} operational items across {len(counts)} types."

    return {
        "headline_ar": hide_internal_terms(headline_ar),
        "headline_en": hide_internal_terms(headline_en),
        "counts_by_type": bilingual_counts,
        "data_status": graph.data_status,
        "edge_count": len(graph.edges),
        "degraded_section_count": len(graph.degraded_sections),
    }
