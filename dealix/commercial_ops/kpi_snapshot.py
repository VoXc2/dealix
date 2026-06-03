"""Founder commercial KPI status — registry/import only, no invented numbers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.paths import REPO_ROOT

_REGISTRY = REPO_ROOT / "dealix/transformation/kpi_founder_commercial_registry.yaml"
_IMPORT = REPO_ROOT / "dealix/transformation/kpi_founder_commercial_import.yaml"
_FORBIDDEN_REF = re.compile(
    r"REPLACE:|fake|invented|synthetic_default|example_only|placeholder",
    re.I,
)


def load_kpi_commercial_status() -> dict[str, Any]:
    """Pending vs ready keys; never fabricates CRM values."""
    if not _REGISTRY.is_file():
        return {
            "registry_exists": False,
            "pending": [],
            "ready": [],
            "import_file_exists": False,
            "hint_ar": "ملف kpi_founder_commercial_registry.yaml غير موجود",
        }

    reg = yaml.safe_load(_REGISTRY.read_text(encoding="utf-8")) or {}
    entries = reg.get("commercial_entries") or {}
    pending: list[str] = []
    ready: list[str] = []
    for key, row in entries.items():
        val = row.get("value_numeric")
        ref = (row.get("source_ref") or "").strip()
        if val is None or not ref or _FORBIDDEN_REF.search(ref):
            pending.append(key)
        else:
            ready.append(key)

    import_exists = _IMPORT.is_file()
    hint_ar = ""
    if pending and not import_exists:
        hint_ar = (
            "انسخ kpi_founder_commercial_import.example.yaml → "
            "kpi_founder_commercial_import.yaml وعبّئ من CRM"
        )
    elif pending:
        hint_ar = f"{len(pending)} KPI معلّقة — أكمل source_ref من CRM"

    return {
        "registry_exists": True,
        "updated_period_iso": reg.get("updated_period_iso"),
        "pending": pending,
        "ready": ready,
        "pending_count": len(pending),
        "ready_count": len(ready),
        "import_file_exists": import_exists,
        "hint_ar": hint_ar,
        "apply_script": "scripts/apply_kpi_founder_commercial.py",
    }
