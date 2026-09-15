#!/usr/bin/env python3
"""Apply explicit, verified platform KPI signals without fabricating baseline freshness.

This updater is fail-closed. It does not derive commercial proof from the placeholder
defaults in ``weekly_cross_os_snapshot`` and it does not invent zero guardrail counts.
Without an explicit verified-signals receipt, the baseline file is left unchanged.
Partial platform updates never refresh the global ``updated_period_iso`` because that
field describes the complete CRM/finance/delivery/platform baseline set.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

_ALLOWED_PLATFORM_KEYS = {
    "reliability_posture_score",
    "unauthorized_external_action_count",
    "measured_metric_without_source_ref_count",
    "tenant_isolation_violation_count",
}
_UNVERIFIED_MARKERS = (
    "not_synced",
    "synthetic",
    "demo",
    "sample",
    "placeholder",
    "none_active",
    "pass_required",
)


def _patch_snapshot_line(text: str, key: str, value: float, source_ref: str) -> str:
    lines = text.splitlines(keepends=True)
    in_key = False
    found_value = False
    found_ref = False
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
                nl = "\n" if line.endswith("\n") else ""
                out.append(f"{m_val.group(1)}value_numeric: {value}{nl}")
                found_value = True
                continue
            m_ref = ref_re.match(line.rstrip("\n"))
            if m_ref:
                nl = "\n" if line.endswith("\n") else ""
                safe_ref = source_ref.replace('"', "'")
                out.append(f'{m_ref.group(1)}source_ref: "{safe_ref}"{nl}')
                found_ref = True
                in_key = False
                continue
            if line.strip() and not line.startswith(" "):
                in_key = False
        out.append(line)
    if not (found_value and found_ref):
        raise ValueError(f"baseline key is missing value/source fields: {key}")
    return "".join(out)


def _load_verified_signals(path: Path) -> dict[str, tuple[float, str]]:
    payload: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema") != "dealix.kpi_platform_signals.v1":
        raise ValueError("verified signals must use schema dealix.kpi_platform_signals.v1")
    signals = payload.get("signals")
    if not isinstance(signals, dict) or not signals:
        raise ValueError("verified signals receipt must contain a non-empty signals object")

    result: dict[str, tuple[float, str]] = {}
    for key, row in signals.items():
        if key not in _ALLOWED_PLATFORM_KEYS:
            raise ValueError(f"key is not platform-owned baseline authority: {key}")
        if not isinstance(row, dict):
            raise ValueError(f"signal row must be an object: {key}")
        value = row.get("value_numeric")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"signal value must be numeric: {key}")
        source_ref = str(row.get("source_ref") or "").strip()
        if not source_ref:
            raise ValueError(f"signal source_ref is required: {key}")
        lower = source_ref.lower()
        if any(marker in lower for marker in _UNVERIFIED_MARKERS):
            raise ValueError(f"signal source_ref is explicitly unverified: {key}")
        result[key] = (float(value), source_ref)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--verified-signals-json", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    path = args.repo_root / "dealix/transformation/kpi_baselines.yaml"
    if not path.exists():
        print("missing_kpi_baselines")
        return 1

    if args.verified_signals_json is None:
        print("PLATFORM_SIGNALS=NO_VERIFIED_INPUT")
        print("BASELINE_MUTATION=NONE")
        print("GLOBAL_UPDATED_PERIOD=UNCHANGED")
        return 0

    try:
        metrics = _load_verified_signals(args.verified_signals_json)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"VERIFIED_PLATFORM_SIGNALS=REJECTED reason={exc}")
        return 2

    text = path.read_text(encoding="utf-8")
    try:
        for key, (value, source_ref) in metrics.items():
            text = _patch_snapshot_line(text, key, value, source_ref)
    except ValueError as exc:
        print(f"VERIFIED_PLATFORM_SIGNALS=REJECTED reason={exc}")
        return 2

    if args.dry_run:
        for key, (value, source_ref) in sorted(metrics.items()):
            print(f"{key}: {value} ref={source_ref}")
        print("BASELINE_MUTATION=DRY_RUN_NONE")
        print("GLOBAL_UPDATED_PERIOD=UNCHANGED")
        return 0

    path.write_text(text, encoding="utf-8")
    print(f"VERIFIED_PLATFORM_SIGNALS=APPLIED count={len(metrics)}")
    print("GLOBAL_UPDATED_PERIOD=UNCHANGED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
