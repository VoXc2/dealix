#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data" / "commercial" / "commercial_authority_source_map_v1.json"


def _load() -> dict[str, Any]:
    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError("source map must be a JSON object")
    return data


def main() -> int:
    data = _load()
    required_path = [
        "FREE_MINI_DIAGNOSTIC",
        "QUALIFIED_DISCOVERY",
        "CUSTOMER_SPECIFIC_QUOTE",
        "REVENUE_COMMAND_PILOT_30D",
        "VERIFIED_PAYMENT",
        "DELIVERY",
        "CUSTOMER_VALIDATED_PROOF",
        "STOP_EXPAND_REDESIGN",
    ]
    assert data.get("canonical_commercial_path") == required_path
    assert data.get("closure_issue") == 1162

    allowed = set(data.get("allowed_classifications") or [])
    sources = data.get("sources") or []
    assert sources and all(isinstance(row, dict) for row in sources)
    ids = [str(row.get("id") or "") for row in sources]
    assert len(ids) == len(set(ids))

    unresolved = set((data.get("closure") or {}).get("unresolved_ids") or [])
    retired_ids: set[str] = set()

    for row in sources:
        source_id = str(row["id"])
        classification = str(row["classification"])
        assert classification in allowed

        if classification == "HISTORICAL_REFERENCE":
            assert row.get("authority") is False
            assert row.get("runtime_consumed") is False
            continue

        path = ROOT / str(row["path"])
        assert path.is_file(), f"mapped source missing: {path}"
        text = path.read_text(encoding="utf-8")
        for marker in row.get("expected_markers") or []:
            assert marker in text, f"missing marker for {source_id}: {marker}"
        for marker in row.get("forbidden_markers") or []:
            assert marker not in text, f"forbidden marker for {source_id}: {marker}"

        if classification == "CURRENT_CANONICAL_AUTHORITY":
            assert row.get("fixed_public_price_authority") is False
        if classification == "RETIRED_RUNTIME_AUTHORITY":
            assert row.get("runtime_consumed") is True
            retired_ids.add(source_id)

    assert retired_ids == unresolved
    closure = data.get("closure") or {}
    assert closure.get("verdict") == "BLOCKED_RETIRED_RUNTIME_AUTHORITY"
    assert closure.get("ready_for_issue_closure") is False

    guardrails = data.get("guardrails") or {}
    for key in (
        "no_new_pricing_catalog",
        "no_public_checkout",
        "no_automatic_quote_discount_or_payment",
        "no_historical_mass_rewrite",
        "draft_is_not_sent",
        "invoice_is_not_payment",
        "payment_requires_independent_evidence",
    ):
        assert guardrails.get(key) is True, f"guardrail must remain true: {key}"

    print("COMMERCIAL_AUTHORITY_SOURCE_MAP_V1_PASS")
    print(f"closure_verdict={closure['verdict']}")
    print(f"unresolved_count={len(unresolved)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
