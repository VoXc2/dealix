#!/usr/bin/env python3
"""Validate Hermes/OpenClaw profile mappings for service stack."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from saudi_ai_provider.catalog import load_agent_profiles, load_final_service_stack


def main() -> int:
    errors: list[str] = []
    data = load_agent_profiles()
    stack = load_final_service_stack()

    required_profiles = {"hermes_agents", "openclaw_runtime", "hybrid_governed_execution"}
    profiles = data.get("profiles", {})
    missing_profiles = sorted(required_profiles - set(profiles.keys()))
    if missing_profiles:
        errors.append(f"missing profiles: {', '.join(missing_profiles)}")

    recommendations = data.get("service_profile_recommendations", {})
    service_apps = data.get("service_applications", {})
    service_ids = {service["service_id"] for service in stack.get("services", [])}

    for service_id in sorted(service_ids):
        profile = recommendations.get(service_id)
        if profile not in required_profiles:
            errors.append(f"{service_id}: missing or invalid profile recommendation")
        app = service_apps.get(service_id)
        if not app:
            errors.append(f"{service_id}: missing service_applications entry")
            continue
        if not app.get("business_goal"):
            errors.append(f"{service_id}: missing business_goal")
        if not isinstance(app.get("applications"), list) or len(app["applications"]) < 2:
            errors.append(f"{service_id}: applications must include at least 2 entries")

    if errors:
        print("AGENT_PROFILE_VALIDATION=FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("AGENT_PROFILE_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
