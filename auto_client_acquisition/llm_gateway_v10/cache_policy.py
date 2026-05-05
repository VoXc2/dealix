"""Deterministic cache key derivation for routing requests."""
from __future__ import annotations

import hashlib

from auto_client_acquisition.llm_gateway_v10.schemas import RoutingPolicy


def cache_key(req: RoutingPolicy) -> str:
    """Return a stable sha256 hex digest for ``req``.

    Canonicalises the four routing-relevant fields into a single
    string so identical requests collide and differing ones don't.
    """
    try:
        payload = "|".join(
            [
                (req.task_purpose or "").strip().lower(),
                str(req.language),
                (req.customer_handle or "").strip().lower(),
                str(int(req.max_tokens)),
                str(int(req.max_iterations)),
            ]
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()
    except Exception:  # noqa: BLE001 - defensive default
        return hashlib.sha256(b"llm_gateway_v10:fallback").hexdigest()
