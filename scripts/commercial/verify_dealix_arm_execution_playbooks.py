#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PLAYBOOKS = ROOT / "config" / "company" / "dealix_arm_execution_playbooks.json"
DEFAULT_REGISTRY = ROOT / "config" / "company" / "dealix_arm_registry.json"

ALLOWED_HORIZONS = {"NOW-30D", "30-90D", "90-180D", "180-365D", "HOLD"}
REQUIRED_TEXT_FIELDS = {
    "first_experiment",
    "primary_kpi",
    "expansion_path",
    "strategic_dependency",
}


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("root_not_object")
    return payload


def verify(playbooks: dict[str, Any], registry: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            failures.append(code)

    require(playbooks.get("schema_version") == 1, "SCHEMA_VERSION")
    require(playbooks.get("registry") == "config/company/dealix_arm_registry.json", "REGISTRY_LINK")
    require(playbooks.get("deep_wip_max") == registry.get("deep_wip_max") == 3, "DEEP_WIP_MATCH")

    declared_horizons = {
        str(value) for value in playbooks.get("allowed_horizons", []) if isinstance(value, str)
    }
    require(declared_horizons == ALLOWED_HORIZONS, "ALLOWED_HORIZONS")

    registry_arms = registry.get("arms")
    raw_playbooks = playbooks.get("playbooks")
    require(isinstance(registry_arms, list) and bool(registry_arms), "REGISTRY_ARMS")
    require(isinstance(raw_playbooks, list) and bool(raw_playbooks), "PLAYBOOKS")
    if not isinstance(registry_arms, list) or not isinstance(raw_playbooks, list):
        return failures

    registry_by_id = {
        str(arm.get("id")): arm
        for arm in registry_arms
        if isinstance(arm, dict) and isinstance(arm.get("id"), str)
    }

    playbook_ids: list[str] = []
    for index, raw in enumerate(raw_playbooks, start=1):
        code = f"PLAYBOOK_{index:03d}"
        require(isinstance(raw, dict), f"{code}_OBJECT")
        if not isinstance(raw, dict):
            continue

        arm_id = raw.get("arm_id")
        horizon = raw.get("horizon")
        require(isinstance(arm_id, str) and bool(arm_id.strip()), f"{code}_ARM_ID")
        require(horizon in ALLOWED_HORIZONS, f"{code}_HORIZON")

        if isinstance(arm_id, str):
            playbook_ids.append(arm_id)

        for field in REQUIRED_TEXT_FIELDS:
            value = raw.get(field)
            require(isinstance(value, str) and bool(value.strip()), f"{code}_{field.upper()}")

        registry_arm = registry_by_id.get(str(arm_id))
        require(registry_arm is not None, f"{code}_REGISTRY_ARM")
        if registry_arm is None:
            continue

        state = registry_arm.get("state")
        priority = registry_arm.get("priority")
        if state == "BLOCKED":
            require(horizon == "HOLD", f"{code}_BLOCKED_MUST_HOLD")
        if state == "ACTIVE_DEEP":
            require(horizon == "NOW-30D", f"{code}_DEEP_MUST_BE_NOW")
        if state == "WATCH":
            require(horizon != "NOW-30D", f"{code}_WATCH_CANNOT_BE_NOW")
        if priority == "P3":
            require(horizon in {"180-365D", "HOLD"}, f"{code}_P3_HORIZON")

    require(len(playbook_ids) == len(set(playbook_ids)), "PLAYBOOK_IDS_UNIQUE")
    require(set(playbook_ids) == set(registry_by_id), "PLAYBOOK_IDS_MATCH_REGISTRY")

    deep_ids = {
        str(arm.get("id"))
        for arm in registry_arms
        if isinstance(arm, dict) and arm.get("state") == "ACTIVE_DEEP"
    }
    require(1 <= len(deep_ids) <= int(playbooks.get("deep_wip_max", 0) or 0), "DEEP_WIP_WITHIN_LIMIT")

    scorecard = playbooks.get("common_scorecard")
    require(
        isinstance(scorecard, list)
        and len(scorecard) >= 8
        and all(isinstance(value, str) and value.strip() for value in scorecard),
        "COMMON_SCORECARD",
    )

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Dealix arm execution playbooks")
    parser.add_argument("--playbooks", default=str(DEFAULT_PLAYBOOKS))
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    args = parser.parse_args()

    playbook_path = Path(args.playbooks)
    registry_path = Path(args.registry)
    if not playbook_path.is_file():
        print(f"DEALIX_ARM_EXECUTION_VERIFY=FAIL missing_playbooks={playbook_path}")
        return 2
    if not registry_path.is_file():
        print(f"DEALIX_ARM_EXECUTION_VERIFY=FAIL missing_registry={registry_path}")
        return 2

    try:
        playbooks = _read_json(playbook_path)
        registry = _read_json(registry_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"DEALIX_ARM_EXECUTION_VERIFY=FAIL parse={type(exc).__name__}")
        return 2

    failures = verify(playbooks, registry)
    if failures:
        print("DEALIX_ARM_EXECUTION_VERIFY=FAIL " + ",".join(failures))
        return 2

    horizons: dict[str, int] = {value: 0 for value in sorted(ALLOWED_HORIZONS)}
    for playbook in playbooks["playbooks"]:
        horizons[str(playbook["horizon"])] += 1

    print("DEALIX_ARM_EXECUTION_VERIFY=PASS")
    print(f"PLAYBOOKS_TOTAL={len(playbooks['playbooks'])}")
    for horizon in ["NOW-30D", "30-90D", "90-180D", "180-365D", "HOLD"]:
        print(f"HORIZON_{horizon.replace('-', '_')}={horizons[horizon]}")
    print("DEEP_WIP_MAX=3")
    print("EXECUTION_TRUTH=EVIDENCE_GATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
