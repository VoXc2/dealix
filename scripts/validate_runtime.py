#!/usr/bin/env python3
"""Validate runtime/policy/evidence operating skeleton."""

from __future__ import annotations

import json
from pathlib import Path


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    required_paths = {
        "workflow_registry": Path("runtime/workflows/workflow_registry.json"),
        "execution_event": Path("runtime/execution_registry/sample_execution_event.json"),
        "orchestration_policy": Path("runtime/orchestration/orchestration_policy.json"),
        "policy_rules": Path("policy_engine/rules/core_policies.json"),
        "risk_model": Path("policy_engine/risk_scoring/model.json"),
        "evidence_export": Path("evidence/exports/evidence_export_template.json"),
        "policy_trace": Path("evidence/policy_traces/policy_trace_template.json"),
    }

    loaded: dict[str, dict] = {}
    for name, path in required_paths.items():
        if not path.exists():
            errors.append(f"missing file: {path}")
            continue
        loaded[name] = _load(path)

    if "execution_event" in loaded:
        for field in (
            "execution_id",
            "workflow",
            "decision",
            "policy_snapshot",
            "initiator",
            "timestamp",
            "risk_score",
            "evidence_artifact",
        ):
            if field not in loaded["execution_event"]:
                errors.append(f"execution_event: missing field {field}")

    if "policy_rules" in loaded and not loaded["policy_rules"].get("policies"):
        errors.append("policy_rules: policies array empty")
    if "workflow_registry" in loaded and not loaded["workflow_registry"].get("workflows"):
        errors.append("workflow_registry: workflows array empty")

    if errors:
        print("RUNTIME_VALIDATION=FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("RUNTIME_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
