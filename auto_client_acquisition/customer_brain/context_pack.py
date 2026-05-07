"""Context pack distillation — ≤3KB JSON for LLM context windows.

Takes a CustomerBrainSnapshot and emits the smallest dict that
captures: profile, top 3 channels, top 5 service_history items,
top 5 proof events, top 3 open decisions, top 3 growth opportunities.
"""
from __future__ import annotations

import json
from typing import Any

from auto_client_acquisition.full_ops_contracts.schemas import CustomerBrainSnapshot

_MAX_BYTES = 3072  # 3KB hard cap


def context_pack(snap: CustomerBrainSnapshot) -> dict[str, Any]:
    """Return a ≤3KB dict suitable for an LLM system message."""
    pack: dict[str, Any] = {
        "customer_handle": snap.customer_handle,
        "profile": snap.profile,
        "channels": snap.channels[:3],
        "tone": snap.tone_of_voice.get("primary_language", "ar"),
        "constraints": snap.compliance_constraints[:5],
        "recent_services": snap.service_history[:5],
        "recent_proof": snap.proof_history[:5],
        "open_decisions": snap.open_decisions[:3],
        "support_open": snap.support_context.get("open_tickets_count", 0),
        "growth_watchlist": snap.growth_opportunities[:3],
        "safety_summary": snap.safety_summary,
    }

    # If over budget, progressively trim
    while len(json.dumps(pack, ensure_ascii=False).encode("utf-8")) > _MAX_BYTES:
        if pack.get("recent_services"):
            pack["recent_services"] = pack["recent_services"][:-1]
            continue
        if pack.get("recent_proof"):
            pack["recent_proof"] = pack["recent_proof"][:-1]
            continue
        if pack.get("growth_watchlist"):
            pack["growth_watchlist"] = pack["growth_watchlist"][:-1]
            continue
        if pack.get("open_decisions"):
            pack["open_decisions"] = pack["open_decisions"][:-1]
            continue
        # If still over, drop constraints
        if pack.get("constraints"):
            pack["constraints"] = pack["constraints"][:1]
            continue
        break

    return pack
