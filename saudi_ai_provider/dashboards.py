"""Dashboard export helpers for executive/sales/delivery/risk views."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .catalog import ROOT


def export_dashboard_bundle(
    *,
    output_dir: Path | None = None,
    metrics: dict[str, Any] | None = None,
) -> dict[str, Path]:
    target = output_dir or (ROOT / "dashboard/exports")
    target.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).isoformat()
    base = {
        "generated_at": now,
        "source": "saudi_ai_provider.dashboard_export",
    }
    input_metrics = metrics or {}

    executive = {
        **base,
        "arr_sar": input_metrics.get("arr_sar", 0),
        "pipeline_sar": input_metrics.get("pipeline_sar", 0),
        "gross_margin": input_metrics.get("gross_margin", 0),
        "sla_compliance": input_metrics.get("sla_compliance", 0),
    }
    sales = {
        **base,
        "warm_intros": input_metrics.get("warm_intros", 0),
        "demo_booked": input_metrics.get("demo_booked", 0),
        "proposal_sent": input_metrics.get("proposal_sent", 0),
        "close_rate": input_metrics.get("close_rate", 0),
    }
    delivery = {
        **base,
        "deployment_velocity": input_metrics.get("deployment_velocity", 0),
        "on_time_delivery_rate": input_metrics.get("on_time_delivery_rate", 0),
        "blocker_count": input_metrics.get("blocker_count", 0),
        "incident_count": input_metrics.get("incident_count", 0),
    }
    risk = {
        **base,
        "critical_incidents": input_metrics.get("critical_incidents", 0),
        "policy_violations": input_metrics.get("policy_violations", 0),
        "pii_leakage_incidents": input_metrics.get("pii_leakage_incidents", 0),
        "compliance_score": input_metrics.get("compliance_score", 0),
    }

    outputs = {
        "executive_dashboard": target / "executive_dashboard.json",
        "sales_dashboard": target / "sales_dashboard.json",
        "delivery_dashboard": target / "delivery_dashboard.json",
        "risk_dashboard": target / "risk_dashboard.json",
    }
    payloads = {
        "executive_dashboard": executive,
        "sales_dashboard": sales,
        "delivery_dashboard": delivery,
        "risk_dashboard": risk,
    }

    for key, path in outputs.items():
        path.write_text(
            json.dumps(payloads[key], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    return outputs
