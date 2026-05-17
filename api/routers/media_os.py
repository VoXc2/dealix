"""Media OS router — GCC Governed AI Ops Pulse.

Authority/media capability. Aggregates governance risk-score signals
into a quarterly, anonymized "GCC Governed AI Ops Pulse" report.

DOCTRINE — the report is aggregate/anonymized only. No individual
client's data is exposed without consent.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Query

from api.routers.governance_risk_dashboard import build_risk_dashboard_payload
from auto_client_acquisition.media_os import build_gcc_pulse

router = APIRouter(prefix="/api/v1/media-os", tags=["media-os"])


def _risk_scores_path() -> Path:
    """Resolve the governance risk-scores JSONL store (env override aware)."""
    raw = os.environ.get("DEALIX_GOVERNANCE_RISK_SCORES_PATH")
    if raw:
        return Path(raw)
    return Path("data") / "governance_risk_scores.jsonl"


def _load_risk_records() -> list[dict[str, Any]]:
    """Read governance risk-score records from the JSONL store.

    Returns an empty list when the store does not exist yet.
    """
    path = _risk_scores_path()
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


@router.get("/status")
async def media_os_status() -> dict[str, Any]:
    return {
        "service": "media_os",
        "module": "media_os",
        "status": "operational",
        "checks": {"gcc_pulse": "ok"},
        "doctrine": "aggregate_anonymized_reporting_only",
    }


@router.get("/gcc-pulse")
async def gcc_pulse(
    quarter: str = Query(default="", description="e.g. 2026-Q2"),
) -> dict[str, Any]:
    """Quarterly GCC Governed AI Ops Pulse — aggregated, anonymized.

    Aggregates governance risk-score records into counts of risk
    scores, most-frequent risks, most-requested workflows, evidence
    gaps and best practices.

    DOCTRINE — output is anonymized. Per-client identifiers are used
    only for the distinct-client count and are never emitted. Groups
    below the k-anonymity floor are withheld.
    """
    records = _load_risk_records()
    pulse = build_gcc_pulse(records, quarter=quarter or "current")
    dashboard = build_risk_dashboard_payload()
    payload = pulse.to_dict()
    payload["governance_context"] = {
        "policy_registry_version": dashboard.get("policy_registry_version"),
        "forbidden_actions": dashboard.get("forbidden_actions", []),
        "service_sessions_sampled": dashboard.get("service_sessions", {}).get(
            "sampled", 0
        ),
    }
    payload["data_status"] = "live" if records else "no_risk_scores_recorded_yet"
    payload["read_only"] = True
    payload["governance_decision"] = "allow"
    return payload
