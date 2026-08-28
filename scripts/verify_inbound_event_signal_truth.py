#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "commercial" / "inbound_event_accounts"

ALLOWED_TRUTH_CLASSES = {
    "INBOUND_EVENT_SIGNAL",
    "REAL_INTERACTION",
    "VERIFIED_RELATIONSHIP",
    "QUALIFIED_PROBLEM",
    "OPPORTUNITY",
}


def present(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def verify_record(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{path.name}:invalid_json:{exc}"]

    truth = record.get("truth")
    if not isinstance(truth, dict):
        return [f"{path.name}:missing_truth_object"]

    truth_class = truth.get("truth_class")
    if truth_class not in ALLOWED_TRUTH_CLASSES:
        errors.append(f"{path.name}:invalid_truth_class:{truth_class}")

    real_interaction = truth.get("real_interaction") is True
    verified_relationship = truth.get("verified_relationship") is True
    qualified_problem = truth.get("qualified_problem") is True
    opportunity = truth.get("opportunity") is True
    customer = truth.get("customer") is True
    revenue = truth.get("revenue") is True

    # A raw event signal can never silently become commercial truth.
    if truth_class == "INBOUND_EVENT_SIGNAL":
        for field, value in (
            ("real_interaction", real_interaction),
            ("verified_relationship", verified_relationship),
            ("qualified_problem", qualified_problem),
            ("opportunity", opportunity),
            ("customer", customer),
            ("revenue", revenue),
        ):
            if value:
                errors.append(f"{path.name}:event_signal_illegal_promotion:{field}")

    evidence = record.get("evidence", {})
    if not isinstance(evidence, dict):
        evidence = {}

    if verified_relationship:
        if not real_interaction:
            errors.append(f"{path.name}:relationship_without_real_interaction")
        if not present(evidence.get("relationship_evidence_id")):
            errors.append(f"{path.name}:relationship_without_evidence_id")

    if qualified_problem and not verified_relationship:
        errors.append(f"{path.name}:qualified_problem_without_verified_relationship")

    if opportunity and not qualified_problem:
        errors.append(f"{path.name}:opportunity_without_qualified_problem")

    if customer and not verified_relationship:
        errors.append(f"{path.name}:customer_without_verified_relationship")

    if revenue and not present(evidence.get("payment_evidence_id")):
        errors.append(f"{path.name}:revenue_without_payment_evidence_id")

    account = record.get("account", {})
    if isinstance(account, dict) and account.get("identity_resolution") == "UNRESOLVED":
        # Unknown company facts must remain unknown until identity is resolved.
        for key in ("sector", "geography", "website"):
            if account.get(key) not in (None, ""):
                errors.append(f"{path.name}:unresolved_identity_has_claim:{key}")

    return errors


def main() -> int:
    if not DATA_DIR.is_dir():
        print("DEALIX_INBOUND_EVENT_TRUTH=FAIL")
        print(f"- missing_data_dir:{DATA_DIR}")
        return 1

    paths = sorted(DATA_DIR.glob("*.json"))
    if not paths:
        print("DEALIX_INBOUND_EVENT_TRUTH=FAIL")
        print("- no_inbound_event_records")
        return 1

    errors: list[str] = []
    for path in paths:
        errors.extend(verify_record(path))

    if errors:
        print("DEALIX_INBOUND_EVENT_TRUTH=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("DEALIX_INBOUND_EVENT_TRUTH=PASS")
    print(f"RECORDS={len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
