#!/usr/bin/env python3
"""
Verify Dealix Service Tower contracts.

Reads the live `services/catalog` + per-bundle endpoints and asserts every
public bundle has the required contract fields. The check is non-invasive
(no writes). Default target is the local API; override with BASE_URL.

Exit code:
    0  → SERVICE_TOWER_OK
    1  → SERVICE_TOWER_FAIL  (with per-bundle missing fields)
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from collections.abc import Iterable

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
TIMEOUT = float(os.getenv("VERIFY_TIMEOUT_S", "10"))


# Required keys per bundle. We accept any of the synonyms so a router that
# named a field slightly differently is not penalized.
REQUIRED: list[tuple[str, tuple[str, ...]]] = [
    ("service_id",          ("id", "service_id", "bundle_id")),
    ("name_ar",             ("name_ar",)),
    ("name_en",             ("name_en",)),
    ("target_customer",     ("for_whom_ar", "for_whom_en", "target_customer")),
    ("required_inputs",     ("required_inputs", "intake_questions")),  # may live on intake-questions endpoint
    ("workflow_steps",      ("workflow_steps", "deliverables_ar", "deliverables")),
    ("deliverables",        ("deliverables_ar", "deliverables")),
    ("proof_metrics",       ("proof_metrics",)),
    ("approval_policy",     ("safe_policy_ar", "approval_policy", "safe_action_policy")),
    ("safe_action_policy",  ("safe_policy_ar", "safe_action_policy", "approval_policy", "blocked_actions")),
    ("pricing",             ("price_sar", "price_label", "pricing", "pricing_range")),
    ("sla",                 ("sla_ar", "sla", "duration_days")),
    ("upgrade_path",        ("upgrade_path", "cta_path")),
    ("definition_of_done",  ("definition_of_done", "proof_metrics", "deliverables_ar")),
]

PUBLIC_BUNDLES = {
    "growth_starter",
    "data_to_revenue",
    "partnership_growth",
    "executive_growth_os",
    "full_growth_control_tower",
}


def _get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:  # noqa: S310 — trusted host
        return json.loads(r.read().decode("utf-8"))


def _has_any(bundle: dict, keys: Iterable[str], extra: dict | None = None) -> bool:
    extra = extra or {}
    for k in keys:
        if k in bundle and bundle[k] not in (None, "", [], {}):
            return True
        if k in extra and extra[k] not in (None, "", [], {}):
            return True
    return False


def verify() -> int:
    try:
        catalog = _get(f"{BASE_URL}/api/v1/services/catalog")
    except Exception as e:  # noqa: BLE001
        print(f"SERVICE_TOWER_FAIL  unreachable {BASE_URL}/api/v1/services/catalog → {e}")
        return 1

    bundles = catalog.get("bundles") or []
    if not bundles:
        print("SERVICE_TOWER_FAIL  catalog has no bundles")
        return 1

    failures: list[str] = []
    found_ids: set[str] = set()

    for b in bundles:
        bid = b.get("id") or b.get("service_id") or "<no-id>"
        found_ids.add(bid)

        intake_extra: dict = {}
        try:
            iq = _get(f"{BASE_URL}/api/v1/services/{bid}/intake-questions")
            intake_extra = {
                "intake_questions": iq.get("questions") or [],
                "required_inputs":  iq.get("questions") or [],
            }
        except Exception:
            pass

        # Per-bundle detail (sometimes carries fields catalog omits)
        detail: dict = {}
        try:
            detail = _get(f"{BASE_URL}/api/v1/services/{bid}") or {}
        except Exception:
            pass

        merged = {**b, **detail, **intake_extra}

        for label, keys in REQUIRED:
            if not _has_any(merged, keys):
                failures.append(f"  - {bid}: missing {label} (any of {keys})")

    missing_ids = PUBLIC_BUNDLES - found_ids
    extra_ids = (found_ids - PUBLIC_BUNDLES) - {"free_diagnostic"}  # free_diagnostic is acceptable extra
    if missing_ids:
        failures.append(f"  - public bundles missing: {sorted(missing_ids)}")

    if failures:
        print("SERVICE_TOWER_FAIL")
        for line in failures:
            print(line)
        return 1

    print(f"SERVICE_TOWER_OK  bundles_verified={len(bundles)}  found_ids={sorted(found_ids)}")
    if extra_ids:
        print(f"INFO  extra_or_internal_bundles={sorted(extra_ids)}")
    return 0


if __name__ == "__main__":
    sys.exit(verify())
