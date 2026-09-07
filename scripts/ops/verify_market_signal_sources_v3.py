#!/usr/bin/env python3
"""Fail-closed verifier for Dealix Market Signal Source Registry V3."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "config" / "market" / "market_signal_sources_v3.json"

ALLOWED_GRADES = {"D1", "D2", "D3", "D4"}
REQUIRED_SOURCE_FIELDS = {
    "id",
    "name",
    "url",
    "lane",
    "default_grade",
    "purpose",
    "allowed_outputs",
    "forbidden_inference",
    "freshness_hours",
}
REQUIRED_SIGNAL_FIELDS = {
    "source_id",
    "source_url",
    "observed_at",
    "entity",
    "event",
    "evidence_excerpt_or_digest",
    "freshness",
    "sector",
    "geography",
    "demand_grade",
    "relationship_state",
    "consent_state",
    "confidence",
    "next_safe_action",
}
FORBIDDEN_AUTHORITY_TERMS = {
    "buyer_intent",
    "relationship",
    "consent",
}


def _fail(message: str) -> None:
    raise SystemExit(f"DEALIX_MARKET_SIGNAL_SOURCES_V3=FAIL: {message}")


def main() -> None:
    if not REGISTRY.is_file():
        _fail(f"missing registry: {REGISTRY}")

    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive boundary
        _fail(f"invalid JSON: {exc}")

    if data.get("schema_version") != 3:
        _fail("schema_version must be 3")

    authority = data.get("authority") or {}
    expected_truth_guards = {
        "source_registry_is_not_opportunity_graph": True,
        "research_is_not_relationship": True,
        "public_contact_is_not_consent": True,
        "signal_is_not_buyer_intent": True,
        "external_sources_may_not_self_create_commercial_authority": True,
    }
    for key, expected in expected_truth_guards.items():
        if authority.get(key) is not expected:
            _fail(f"authority guard {key} must be {expected}")

    grades = data.get("demand_grades") or {}
    if set(grades) != ALLOWED_GRADES:
        _fail("demand_grades must contain exactly D1-D4")

    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        _fail("sources must be a non-empty list")

    seen_ids: set[str] = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            _fail(f"source[{index}] must be an object")
        missing = sorted(REQUIRED_SOURCE_FIELDS - set(source))
        if missing:
            _fail(f"source[{index}] missing fields: {','.join(missing)}")

        source_id = str(source["id"]).strip()
        if not source_id or source_id in seen_ids:
            _fail(f"source id invalid/duplicate: {source_id!r}")
        seen_ids.add(source_id)

        if source["default_grade"] not in ALLOWED_GRADES:
            _fail(f"source {source_id} has invalid demand grade")
        if not str(source["url"]).startswith("https://"):
            _fail(f"source {source_id} must use https URL")
        if not isinstance(source["freshness_hours"], int) or source["freshness_hours"] <= 0:
            _fail(f"source {source_id} freshness_hours must be positive int")

        forbidden = set(source.get("forbidden_inference") or [])
        if not (forbidden & FORBIDDEN_AUTHORITY_TERMS):
            _fail(
                f"source {source_id} must explicitly forbid at least one commercial-authority inference"
            )

    contract = data.get("signal_contract") or {}
    required_fields = set(contract.get("required_fields") or [])
    if required_fields != REQUIRED_SIGNAL_FIELDS:
        missing = sorted(REQUIRED_SIGNAL_FIELDS - required_fields)
        extra = sorted(required_fields - REQUIRED_SIGNAL_FIELDS)
        _fail(f"signal contract drift missing={missing} extra={extra}")

    if contract.get("default_relationship_state") != "RESEARCH_ONLY":
        _fail("default relationship state must remain RESEARCH_ONLY")
    if contract.get("default_consent_state") != "NOT_PROVEN":
        _fail("default consent state must remain NOT_PROVEN")

    print("DEALIX_MARKET_SIGNAL_SOURCES_V3=PASS")
    print(f"source_count={len(sources)}")
    print("commercial_authority_from_external_sources=false")
    print("default_relationship_state=RESEARCH_ONLY")
    print("default_consent_state=NOT_PROVEN")


if __name__ == "__main__":
    main()
