"""Shared helpers for the Ops Console domain routers.

أدوات مشتركة لموجّهات غرفة التشغيل.

Every Ops Console response is wrapped by `governed()` so that the doctrine
fields — `governance_decision` and `is_estimate` — are always present and
cannot be forgotten (enforced by tests/governance/test_ops_console_doctrine.py).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    """UTC timestamp in ISO-8601."""
    return datetime.now(timezone.utc).isoformat()


def governed(
    payload: dict[str, Any],
    *,
    decision: str = "allow",
    is_estimate: bool = True,
) -> dict[str, Any]:
    """Wrap a response payload with the mandatory doctrine envelope.

    `is_estimate=True` is the default: any composed/projected number on these
    read surfaces is an estimate. Confirmed ground-truth figures (e.g. paid
    invoice amounts) are marked individually inside the payload with their
    own `is_estimate: False`.
    """
    out: dict[str, Any] = {"generated_at": now_iso()}
    out.update(payload)
    out["governance_decision"] = decision
    out["is_estimate"] = is_estimate
    return out
