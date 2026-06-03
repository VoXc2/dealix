"""Founder production gates — Railway config + live API trust layer + GTM surfaces."""

from __future__ import annotations

from typing import Any

from dealix.commercial_ops.founder_weekly_metrics import build_founder_weekly_metrics
from dealix.commercial_ops.gtm_public_surfaces import verify_gtm_public_surfaces_repo
from dealix.commercial_ops.railway_production import (
    DEFAULT_API_BASE,
    analyze_railway_production,
    parse_railway_ui_drift_hint,
    parse_railway_ui_predeploy_drift,
)


def build_founder_production_gates(
    *,
    api_base: str | None = None,
    skip_live: bool = False,
    ui_start_command: str = "",
    ui_predeploy: str = "",
) -> dict[str, Any]:
    """Single executive snapshot for pre-flight and post-deploy checks."""
    base = False if skip_live else (api_base or DEFAULT_API_BASE)
    railway = analyze_railway_production(api_base=base)
    gtm_repo = verify_gtm_public_surfaces_repo()
    weekly = build_founder_weekly_metrics()

    founder_actions: list[str] = []
    drift_start = parse_railway_ui_drift_hint(ui_start_command)
    drift_pre = parse_railway_ui_predeploy_drift(ui_predeploy)
    if drift_start:
        founder_actions.append(drift_start)
    if drift_pre:
        founder_actions.append(drift_pre)

    trust = railway.get("live_trust_layer") or {}
    hint = trust.get("deploy_stale_hint_ar")
    if hint:
        founder_actions.append(hint)

    for b in weekly.get("blockers_ar") or []:
        founder_actions.append(b)

    verdict = railway["verdict"]
    if not gtm_repo.get("ok"):
        verdict = "FAIL"
    if verdict == "PASS" and founder_actions:
        verdict = "WARN"

    return {
        "verdict": verdict,
        "api_base": base if base is not False else None,
        "railway": railway,
        "gtm_surfaces_repo": gtm_repo,
        "weekly_metrics": {
            "iso_week": weekly.get("iso_week"),
            "verdict": weekly.get("verdict"),
            "blockers_ar": weekly.get("blockers_ar"),
        },
        "founder_actions_ar": founder_actions,
        "commands": {
            "railway_verify": "python scripts/verify_railway_production_config.py",
            "production_smoke": "bash scripts/founder_production_smoke.sh",
            "weekly_metrics": "python scripts/founder_weekly_metrics_bundle.py --write",
            "agent_packets": "python scripts/print_agent_work_packets.py --cadence daily",
        },
    }
