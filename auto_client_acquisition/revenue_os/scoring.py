"""Deterministic lead / account scoring for Revenue OS (no LLM)."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.data_os.data_quality_score import account_row_completeness


def score_account_row(
    row: dict[str, Any],
    *,
    icp_sectors: frozenset[str] | None = None,
    icp_cities: frozenset[str] | None = None,
    required_keys: tuple[str, ...] = ("company_name", "sector", "city", "source"),
) -> dict[str, Any]:
    """
    Return score 0–100 with human-readable reasons and risks.

    Weights (deterministic):
    - row completeness vs required_keys: up to 35
    - documented source: 25
    - sector fit: up to 20
    - city fit: up to 20
    """
    reasons: list[str] = []
    risks: list[str] = []
    pts = 0.0

    comp = account_row_completeness(row, required_keys)
    pts += 35.0 * comp
    if comp < 1.0:
        risks.append("incomplete_row")

    src = row.get("source")
    if src is not None and str(src).strip():
        pts += 25.0
        reasons.append("source_present")
    else:
        risks.append("missing_source")

    sector_raw = str(row.get("sector") or "").strip().lower()
    if icp_sectors:
        icp_s = {s.strip().lower() for s in icp_sectors if s.strip()}
        if sector_raw and sector_raw in icp_s:
            pts += 20.0
            reasons.append("sector_icp_match")
        elif sector_raw:
            risks.append("sector_outside_icp")
        else:
            risks.append("sector_empty")
    else:
        if sector_raw:
            pts += 15.0
            reasons.append("sector_present")
        else:
            risks.append("sector_empty")
            pts += 5.0

    city_raw = str(row.get("city") or "").strip().lower()
    if icp_cities:
        icp_c = {c.strip().lower() for c in icp_cities if c.strip()}
        if city_raw and city_raw in icp_c:
            pts += 20.0
            reasons.append("city_icp_match")
        elif city_raw:
            risks.append("city_outside_icp")
        else:
            risks.append("city_empty")
    else:
        if city_raw:
            pts += 15.0
            reasons.append("city_present")
        else:
            risks.append("city_empty")
            pts += 5.0

    if str(row.get("company_name") or "").strip():
        pts += 10.0
        reasons.append("company_identified")
    else:
        risks.append("missing_company_name")

    rs = str(row.get("relationship_status") or "").strip().lower()
    if rs in ("explicit_consent", "warm_intro", "contracted"):
        pts += 5.0
        reasons.append("relationship_trust_signal")

    if bool(row.get("manual_priority")):
        pts += 5.0
        reasons.append("manual_priority")

    notes = str(row.get("notes") or "").strip()
    if len(notes) >= 40:
        pts += 5.0
        reasons.append("notes_substantive")

    lcd = row.get("last_contact_days")
    try:
        days = int(lcd)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        days = None
    if days is not None and 0 <= days <= 30:
        pts += 5.0
        reasons.append("recent_interaction")

    emp = row.get("employee_count")
    try:
        ec = int(emp)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        ec = None
    if ec is not None:
        if ec >= 200:
            pts += 5.0
            reasons.append("size_proxy_enterprise")
        elif ec >= 50:
            pts += 3.0
            reasons.append("size_proxy_midmarket")

    score = int(min(100, round(pts)))
    return {
        "score": score,
        "reasons": reasons,
        "risks": risks,
        "components": {
            "completeness": round(comp, 4),
            "points_raw": round(pts, 2),
        },
    }


__all__ = ["score_account_row"]
