"""Load founder integration truth matrix — deterministic YAML, no live credential probes."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_REPO = Path(__file__).resolve().parents[2]
_TRUTH_YAML = _REPO / "dealix" / "transformation" / "founder_integration_truth.yaml"

def _load_truth() -> dict[str, Any]:
    if not _TRUTH_YAML.exists():
        return {}
    data = yaml.safe_load(_TRUTH_YAML.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def _count_status(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"green": 0, "yellow": 0, "red": 0}
    for row in rows:
        st = str(row.get("status", "yellow")).lower()
        if st in counts:
            counts[st] += 1
    return counts


def build_integration_truth_summary() -> dict[str, Any]:
    """Summary for commercial-strategy API and Business NOW UI."""
    data = _load_truth()
    ladder = list(data.get("ladder") or [])
    integrations = list(data.get("integrations") or [])
    platform = list(data.get("platform_checks") or [])

    all_rows = ladder + integrations + platform
    counts = _count_status(all_rows)
    worst = "green"
    if counts.get("red", 0) > 0:
        worst = "red"
    elif counts.get("yellow", 0) > 0:
        worst = "yellow"

    return {
        "source_yaml": "dealix/transformation/founder_integration_truth.yaml",
        "doc_matrix": "docs/ops/FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md",
        "verify_script": "scripts/founder_go_live_verify.sh",
        "overall_status": worst,
        "counts": counts,
        "ladder": ladder,
        "integrations": integrations,
        "platform_checks": platform,
        "founder_rule_ar": (
            "لا تعد العميل بما هو red — استخدم yellow كـ «يدوي/sandbox» و green كـ «جاهز محلياً»."
        ),
    }
