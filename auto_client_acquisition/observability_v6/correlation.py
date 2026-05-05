"""Stable correlation-id helper used across the trace contract."""
from __future__ import annotations

from uuid import uuid4


def build_correlation_id() -> str:
    """Return a fresh correlation id of the form ``cor_<uuid4hex>``."""
    return f"cor_{uuid4().hex}"
