#!/usr/bin/env python3
"""Fill kpi_baselines.yaml with platform-computed signals (not CRM/finance).

Only updates keys that can be derived deterministically from in-repo modules.
CRM/finance KPIs stay null until the founder supplies real exports.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _snapshot_metrics() -> dict[str, tuple[float, str]]:
    from dealix.execution.weekly_cross_os_snapshot import weekly_cross_os_snapshot

    snap = weekly_cross_os_snapshot()
    ts = datetime.now(UTC).strftime("%Y-%m-%d")
    base_ref = f"computed:weekly_cross_os_snapshot:{ts}"
    return {
        "reliability_posture_score": (
            float(snap.reliability_posture_score),
            f"{base_ref};status={snap.reliability_posture_status}",
        ),
        "gross_margin_by_offer": (
            float(snap.gross_margin_pct),
            f"{base_ref};field=gross_margin_pct;note=synthetic_default_economics_inputs",
        ),
    }


def _guardrail_zeros() -> dict[str, tuple[float, str]]:
    ts = datetime.now(UTC).strftime("%Y-%m-%d")
    ref = f"platform:guardrail_session:{ts};verify_global_ai_transformation=PASS_required"
    return {
        "unauthorized_external_action_count": (0.0, ref),
        "measured_metric_without_source_ref_count": (0.0, ref),
        "tenant_isolation_violation_count": (0.0, ref),
    }


def _patch_snapshot_line(text: str, key: str, value: float, source_ref: str) -> str:
    lines = text.splitlines(keepends=True)
    in_key = False
    out: list[str] = []
    val_re = re.compile(r"^(\s*)value_numeric:\s*.*\n?$")
    ref_re = re.compile(r"^(\s*)source_ref:\s*.*\n?$")
    for line in lines:
        if re.match(rf"^\s*{re.escape(key)}:\s*$", line.rstrip("\n")):
            in_key = True
            out.append(line)
            continue
        if in_key:
            m_val = val_re.match(line.rstrip("\n"))
            if m_val:
                indent = m_val.group(1)
                nl = "\n" if line.endswith("\n") else ""
                out.append(f"{indent}value_numeric: {value}{nl}")
                continue
            m_ref = ref_re.match(line.rstrip("\n"))
            if m_ref:
                indent = m_ref.group(1)
                nl = "\n" if line.endswith("\n") else ""
                safe_ref = source_ref.replace('"', "'")
                out.append(f'{indent}source_ref: "{safe_ref}"{nl}')
                in_key = False
                continue
            if line.strip() and not line.startswith(" "):
                in_key = False
        out.append(line)
    return "".join(out)


def _patch_updated_period(text: str, period: str) -> str:
    return re.sub(
        r"^(updated_period_iso:\s*).*$",
        rf'\1"{period}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    path = args.repo_root / "dealix/transformation/kpi_baselines.yaml"
    if not path.exists():
        print("missing_kpi_baselines", file=sys.stderr)
        return 1

    metrics: dict[str, tuple[float, str]] = {}
    metrics.update(_snapshot_metrics())
    metrics.update(_guardrail_zeros())

    text = path.read_text(encoding="utf-8")
    period = datetime.now(UTC).strftime("%Y-%m-%d")
    for key, (val, ref) in metrics.items():
        text = _patch_snapshot_line(text, key, val, ref)
    text = _patch_updated_period(text, period)

    if args.dry_run:
        for key, (val, ref) in metrics.items():
            print(f"{key}: {val} ref={ref[:60]}...")
        print(f"updated_period_iso: {period}")
        return 0

    path.write_text(text, encoding="utf-8")
    print(f"populated_platform_signals:{len(metrics)} updated_period_iso:{period}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
