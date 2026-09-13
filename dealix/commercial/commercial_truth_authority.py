"""Canonical commercial-truth classification for retrieval and agent context.

This module does not delete history. It prevents known historical or synthetic
repository material from silently becoming current commercial authority.
Unknown/customer-provided sources remain retrievable as context, but are not
promoted to Dealix current-price/current-architecture authority by this helper.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY_PATH = REPO_ROOT / "config/company/commercial_truth_authority.json"

CURRENT_AUTHORITY = "CURRENT_AUTHORITY"
HISTORICAL_REFERENCE_NON_AUTHORITATIVE = "HISTORICAL_REFERENCE_NON_AUTHORITATIVE"
DEPRECATED_REPLACED = "DEPRECATED_REPLACED"
SYNTHETIC_DEMO_ONLY = "SYNTHETIC_DEMO_ONLY"
UNCLASSIFIED_CONTEXT = "UNCLASSIFIED_CONTEXT"

_EXCLUDED_FROM_CURRENT = frozenset(
    {
        HISTORICAL_REFERENCE_NON_AUTHORITATIVE,
        DEPRECATED_REPLACED,
        SYNTHETIC_DEMO_ONLY,
    }
)


@lru_cache(maxsize=4)
def load_registry(path: str | None = None) -> dict[str, Any]:
    target = Path(path) if path else DEFAULT_REGISTRY_PATH
    payload = json.loads(target.read_text(encoding="utf-8"))
    if payload.get("schema") != "dealix.commercial_truth_authority.v1":
        raise ValueError("unsupported commercial truth authority schema")
    return payload


def normalize_source_id(source_id: str) -> str:
    """Normalize common repo/file source identifiers into a repository path."""
    value = str(source_id or "").strip().replace("\\", "/")
    if value.startswith("file://"):
        value = value[7:]
    repo_prefix = str(REPO_ROOT).replace("\\", "/").rstrip("/") + "/"
    if value.startswith(repo_prefix):
        value = value[len(repo_prefix) :]
    marker = "/Dealix-sa/dealix/blob/"
    if marker in value:
        tail = value.split(marker, 1)[1]
        parts = tail.split("/", 1)
        if len(parts) == 2:
            value = parts[1]
    return value.lstrip("./")


def _looks_like_repo_source(source_id: str) -> bool:
    value = normalize_source_id(source_id)
    return value.startswith(
        (
            "docs/",
            "business/",
            "config/",
            "dealix/",
            "scripts/",
            "auto_client_acquisition/",
            "landing/",
            "apps/",
        )
    )


def classify_source(source_id: str, *, text: str = "", registry_path: str | None = None) -> str:
    registry = load_registry(registry_path)
    source = normalize_source_id(source_id)

    current_paths = {str(item.get("path")) for item in registry.get("current_authority", [])}
    if source in current_paths:
        return CURRENT_AUTHORITY

    for prefix in registry.get("synthetic_prefixes", []):
        if source.startswith(str(prefix)):
            return SYNTHETIC_DEMO_ONLY

    for prefix in registry.get("deprecated_prefixes", []):
        if source.startswith(str(prefix)):
            return DEPRECATED_REPLACED

    if source in {str(path) for path in registry.get("historical_exact_paths", [])}:
        return HISTORICAL_REFERENCE_NON_AUTHORITATIVE

    if _looks_like_repo_source(source):
        lowered = text.casefold()
        for marker in registry.get("legacy_content_markers", []):
            if str(marker).casefold() in lowered:
                return HISTORICAL_REFERENCE_NON_AUTHORITATIVE

    return UNCLASSIFIED_CONTEXT


def should_exclude_from_current_retrieval(
    source_id: str,
    *,
    text: str = "",
    registry_path: str | None = None,
) -> bool:
    return classify_source(source_id, text=text, registry_path=registry_path) in _EXCLUDED_FROM_CURRENT


def authority_receipt(
    source_id: str,
    *,
    text: str = "",
    registry_path: str | None = None,
) -> dict[str, Any]:
    classification = classify_source(source_id, text=text, registry_path=registry_path)
    return {
        "source_id": source_id,
        "normalized_source_id": normalize_source_id(source_id),
        "classification": classification,
        "current_retrieval_allowed": classification not in _EXCLUDED_FROM_CURRENT,
        "may_establish_current_public_price": classification == CURRENT_AUTHORITY,
        "may_establish_current_architecture": classification == CURRENT_AUTHORITY,
        "history_preserved": True,
    }


__all__ = [
    "CURRENT_AUTHORITY",
    "DEPRECATED_REPLACED",
    "HISTORICAL_REFERENCE_NON_AUTHORITATIVE",
    "SYNTHETIC_DEMO_ONLY",
    "UNCLASSIFIED_CONTEXT",
    "authority_receipt",
    "classify_source",
    "load_registry",
    "normalize_source_id",
    "should_exclude_from_current_retrieval",
]
