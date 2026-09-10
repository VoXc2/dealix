#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = ROOT / "config" / "company" / "dealix_arm_registry.json"
DEFAULT_CONSTITUTION = ROOT / "config" / "company" / "dealix_operating_constitution.json"

EXPECTED_AGENTS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}
ALLOWED_STATES = {
    "ACTIVE_DEEP",
    "ACTIVE_LIGHT",
    "VALIDATE",
    "WATCH",
    "BLOCKED",
    "STOPPED",
}
ALLOWED_ENGINES = {
    "CORE_CASH_ENGINE",
    "RECURRING_REVENUE_ENGINE",
    "PRODUCTIZED_SERVICE_ENGINE",
    "DATA_AND_INTELLIGENCE_ENGINE",
    "SOFTWARE_AND_API_ENGINE",
    "PARTNER_AND_CHANNEL_ENGINE",
    "EDUCATION_MEDIA_AND_IP_ENGINE",
    "B2G_AND_REGULATED_ENTERPRISE_ENGINE",
    "VENTURE_AND_ASSET_ENGINE",
}
ALLOWED_PRIORITIES = {"P0", "P1", "P2", "P3"}
REQUIRED_BOUNDARY_SNIPPETS = (
    "sixth permanent agent",
    "duplicate Company Brain",
    "Research never implies relationship",
    "Regulated, licensed or safety-critical",
    "L5 material actions remain exact-action-bound",
)


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("root_not_object")
    return data


def verify(registry: dict[str, Any], constitution: dict[str, Any] | None = None) -> list[str]:
    failures: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            failures.append(code)

    require(registry.get("schema_version") == 1, "SCHEMA_VERSION")
    require(registry.get("deep_wip_max") == 3, "DEEP_WIP_MAX")
    require(registry.get("constitution") == "config/company/dealix_operating_constitution.json", "CONSTITUTION_LINK")

    declared_states = set(str(x) for x in registry.get("states", []) if isinstance(x, str))
    require(ALLOWED_STATES <= declared_states, "DECLARED_STATES")

    boundaries = [str(x) for x in registry.get("global_boundaries", [])]
    for snippet in REQUIRED_BOUNDARY_SNIPPETS:
        require(any(snippet.lower() in boundary.lower() for boundary in boundaries), f"BOUNDARY_{snippet.upper().replace(' ', '_')}")

    arms = registry.get("arms")
    require(isinstance(arms, list) and bool(arms), "ARMS")
    if not isinstance(arms, list):
        return failures

    ids: list[str] = []
    names: list[str] = []
    active_deep = 0
    engine_coverage: set[str] = set()

    for index, raw_arm in enumerate(arms, start=1):
        code = f"ARM_{index:03d}"
        require(isinstance(raw_arm, dict), f"{code}_OBJECT")
        if not isinstance(raw_arm, dict):
            continue

        arm_id = raw_arm.get("id")
        name = raw_arm.get("name")
        owner = raw_arm.get("owner")
        state = raw_arm.get("state")
        engine = raw_arm.get("engine")
        priority = raw_arm.get("priority")

        require(isinstance(arm_id, str) and arm_id.startswith("ARM-") and len(arm_id) == 7, f"{code}_ID")
        require(isinstance(name, str) and bool(name.strip()), f"{code}_NAME")
        require(owner in EXPECTED_AGENTS, f"{code}_OWNER")
        require(state in ALLOWED_STATES, f"{code}_STATE")
        require(engine in ALLOWED_ENGINES, f"{code}_ENGINE")
        require(priority in ALLOWED_PRIORITIES, f"{code}_PRIORITY")

        monetization = raw_arm.get("monetization")
        evidence_sources = raw_arm.get("evidence_sources")
        require(isinstance(monetization, list) and bool(monetization) and all(isinstance(x, str) and x.strip() for x in monetization), f"{code}_MONETIZATION")
        require(isinstance(evidence_sources, list) and bool(evidence_sources) and all(isinstance(x, str) and x.strip() for x in evidence_sources), f"{code}_EVIDENCE")
        require(isinstance(raw_arm.get("promotion_gate"), str) and bool(raw_arm.get("promotion_gate", "").strip()), f"{code}_PROMOTION_GATE")
        require(isinstance(raw_arm.get("kill_condition"), str) and bool(raw_arm.get("kill_condition", "").strip()), f"{code}_KILL_CONDITION")
        require(isinstance(raw_arm.get("buyer"), str) and bool(raw_arm.get("buyer", "").strip()), f"{code}_BUYER")

        if isinstance(arm_id, str):
            ids.append(arm_id)
        if isinstance(name, str):
            names.append(name.strip().lower())
        if state == "ACTIVE_DEEP":
            active_deep += 1
        if isinstance(engine, str):
            engine_coverage.add(engine)

    require(len(ids) == len(set(ids)), "ARM_IDS_UNIQUE")
    require(len(names) == len(set(names)), "ARM_NAMES_UNIQUE")
    require(1 <= active_deep <= 3, "ACTIVE_DEEP_WIP")
    require(active_deep <= int(registry.get("deep_wip_max", 0) or 0), "ACTIVE_DEEP_WITHIN_REGISTRY_LIMIT")
    require(ALLOWED_ENGINES <= engine_coverage, "ENGINE_COVERAGE")

    if constitution is not None:
        arm_config = constitution.get("arm_registry", {})
        compression = constitution.get("compression_law", {})
        require(isinstance(arm_config, dict), "CONSTITUTION_ARM_CONFIG")
        require(isinstance(compression, dict), "CONSTITUTION_COMPRESSION")
        if isinstance(arm_config, dict):
            require(arm_config.get("path") == "config/company/dealix_arm_registry.json", "CONSTITUTION_REGISTRY_PATH")
            require(arm_config.get("deep_wip_max") == registry.get("deep_wip_max"), "CONSTITUTION_REGISTRY_WIP_MATCH")
        if isinstance(compression, dict):
            require(compression.get("deep_wip_max") == registry.get("deep_wip_max"), "CONSTITUTION_COMPRESSION_WIP_MATCH")
        engines = set(str(x) for x in constitution.get("strategic_engines", []) if isinstance(x, str))
        require(ALLOWED_ENGINES <= engines, "CONSTITUTION_ENGINE_COVERAGE")
        agents = set(str(x) for x in constitution.get("permanent_agents", []) if isinstance(x, str))
        require(agents == EXPECTED_AGENTS, "CONSTITUTION_AGENT_MATCH")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Dealix governed business-arm registry")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--constitution", default=str(DEFAULT_CONSTITUTION))
    args = parser.parse_args()

    registry_path = Path(args.registry)
    constitution_path = Path(args.constitution)
    if not registry_path.is_file():
        print(f"DEALIX_ARM_REGISTRY_VERIFY=FAIL missing_registry={registry_path}")
        return 2
    if not constitution_path.is_file():
        print(f"DEALIX_ARM_REGISTRY_VERIFY=FAIL missing_constitution={constitution_path}")
        return 2

    try:
        registry = _read_json(registry_path)
        constitution = _read_json(constitution_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"DEALIX_ARM_REGISTRY_VERIFY=FAIL parse={type(exc).__name__}")
        return 2

    failures = verify(registry, constitution)
    if failures:
        print("DEALIX_ARM_REGISTRY_VERIFY=FAIL " + ",".join(failures))
        return 2

    arms = registry["arms"]
    active_deep = sum(1 for arm in arms if arm.get("state") == "ACTIVE_DEEP")
    active_light = sum(1 for arm in arms if arm.get("state") == "ACTIVE_LIGHT")
    validate = sum(1 for arm in arms if arm.get("state") == "VALIDATE")
    watch = sum(1 for arm in arms if arm.get("state") == "WATCH")
    blocked = sum(1 for arm in arms if arm.get("state") == "BLOCKED")

    print("DEALIX_ARM_REGISTRY_VERIFY=PASS")
    print(f"ARMS_TOTAL={len(arms)}")
    print(f"ACTIVE_DEEP={active_deep}")
    print(f"ACTIVE_LIGHT={active_light}")
    print(f"VALIDATE={validate}")
    print(f"WATCH={watch}")
    print(f"BLOCKED={blocked}")
    print("DEEP_WIP_MAX=3")
    print("PERMANENT_AGENTS=5")
    print("L5=EXACT_ACTION_BOUND_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
