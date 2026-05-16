#!/usr/bin/env python3
"""Dealix Organizational Intelligence Dominance status terminal."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _build_payload() -> dict[str, Any]:
    from auto_client_acquisition.dealix_master_layers import (  # noqa: WPS433
        DOMINANCE_GATES,
        OI_DOMINANCE_LAYERS,
        dominance_readiness_snapshot,
    )

    snapshot = dominance_readiness_snapshot()
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "dominance_layers": len(OI_DOMINANCE_LAYERS),
        "dominance_gates": [gate.gate_id for gate in DOMINANCE_GATES],
        "snapshot": snapshot,
    }


def _line(prefix: str, value: str) -> str:
    return f"{prefix:<33} │ {value}"


def render_text(payload: dict[str, Any]) -> str:
    snapshot = payload.get("snapshot", {})
    status_counts = snapshot.get("status_counts", {})
    lines: list[str] = []
    lines.append("════════════════════════════════════════════════════════════════════")
    lines.append(" Dealix Dominance Status / حالة الهيمنة التنظيمية")
    lines.append(f" generated_at: {payload.get('generated_at')}")
    lines.append("════════════════════════════════════════════════════════════════════")
    lines.append("")
    lines.append(" Gate readiness / جاهزية البوابات")
    lines.append("────────────────────────────────────────────────────────────────────")
    lines.append(_line("dominance_layers", str(payload.get("dominance_layers", "—"))))
    lines.append(_line("dominance_gates", ",".join(payload.get("dominance_gates", []))))
    lines.append(_line("contracts_total", str(snapshot.get("contract_count", "—"))))
    lines.append(_line("status_planned", str(status_counts.get("planned", 0))))
    lines.append(_line("status_in_progress", str(status_counts.get("in_progress", 0))))
    lines.append(_line("status_operational", str(status_counts.get("operational", 0))))
    lines.append("")
    lines.append(" Missing contracts by layer / الطبقات غير المغطاة")
    lines.append("────────────────────────────────────────────────────────────────────")
    missing = snapshot.get("missing_layer_contracts", [])
    if missing:
        for slug in missing:
            lines.append(_line("missing", str(slug)))
    else:
        lines.append(_line("missing", "none"))
    lines.append("")
    lines.append(" Layer contract view / عرض العقود لكل طبقة")
    lines.append("────────────────────────────────────────────────────────────────────")
    for item in snapshot.get("layer_readiness", []):
        statuses = ",".join(item.get("statuses", [])) if item.get("statuses") else "none"
        lines.append(
            _line(
                f"{item.get('layer_id')}.{item.get('slug')}",
                f"contracts={item.get('contract_count')} statuses={statuses}",
            )
        )
    lines.append("")
    lines.append("════════════════════════════════════════════════════════════════════")
    lines.append(" Dominance = governed + reliable + explainable + measurable.")
    lines.append(" الهيمنة = حوكمة + تنفيذ موثوق + تفسير + قياس أثر.")
    lines.append("════════════════════════════════════════════════════════════════════")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dealix dominance status CLI.")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)

    payload = _build_payload()
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(render_text(payload))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
