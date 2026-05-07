"""Customer-safe renderer — strips internal terms before display.

Used by the frontend HTML/JS to ensure the Executive Command Center
never leaks v11/v12/router/verifier/growth_beast/etc to the customer.
"""
from __future__ import annotations

import json
from typing import Any

from auto_client_acquisition.integration_upgrade import hide_internal_terms
from auto_client_acquisition.executive_command_center.schemas import (
    CommandCenterView,
)


def render_customer_safe(view: CommandCenterView) -> dict[str, Any]:
    """Walk the view dict and scrub internal terms in every string."""
    raw = view.model_dump(mode="json")
    return _scrub_recursive(raw)


def _scrub_recursive(obj: Any) -> Any:
    if isinstance(obj, str):
        return hide_internal_terms(obj)
    if isinstance(obj, list):
        return [_scrub_recursive(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _scrub_recursive(v) for k, v in obj.items()}
    return obj
