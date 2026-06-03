#!/usr/bin/env python3
"""Generate Weekly Operating Proof Pack markdown from KPI + ownership registries."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

import yaml


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path, default=None, help="Write file instead of stdout")
    args = parser.parse_args()
    root: Path = args.repo_root

    kpi_path = root / "dealix/transformation/kpi_registry.yaml"
    own_path = root / "dealix/transformation/ownership_matrix.yaml"
    baselines_path = root / "dealix/transformation/kpi_baselines.yaml"
    kpis = _load(kpi_path)
    owners = _load(own_path)
    baselines = _load(baselines_path)

    period = datetime.now(UTC).strftime("%Y-%m-%d")
    lines: list[str] = [
        f"# Weekly Operating Proof Pack — {period}",
        "",
        "## KPI evidence checklist",
        "",
    ]

    if int(kpis.get("version", 0)) < 2:
        raise SystemExit("kpi_registry.yaml version must be >= 2")

    buckets = kpis.get("kpis", {})
    for bucket_name in ("north_star", "leading", "guardrails"):
        lines.append(f"### {bucket_name}")
        lines.append("")
        for row in buckets.get(bucket_name, []):
            key = row.get("key", "?")
            ev = row.get("evidence") or {}
            lines.append(f"- **{key}** ({row.get('owner_os', '')})")
            lines.append(f"  - primary_source: {ev.get('primary_source', '')}")
            fields = ev.get("weekly_proof_fields") or []
            lines.append(f"  - weekly_proof_fields: {', '.join(str(x) for x in fields)}")
            cmds = ev.get("verification_commands") or []
            for cmd in cmds:
                lines.append(f"  - verify: `{cmd}`")
            lines.append("")
        lines.append("")

    lines.extend(
        [
            "## KPI baselines (`kpi_baselines.yaml`)",
            "",
            f"- **updated_period_iso**: `{baselines.get('updated_period_iso', '') or 'UNSET'}`",
            "- Fill each `snapshots.*.value_numeric` from CRM / finance / delivery when figures exist.",
            "- Every non-null value must have a non-empty `source_ref` (invoice id, CRM link, or weekly proof path).",
            "- After editing numbers, set `updated_period_iso` to the reporting week (UTC `YYYY-MM-DD`).",
            "",
        ]
    )

    snaps = baselines.get("snapshots") or {}
    for key in sorted(snaps.keys()):
        row = snaps.get(key) or {}
        val = row.get("value_numeric")
        ref = row.get("source_ref") or ""
        status = "FILLED" if val is not None and str(ref).strip() else "PENDING_NULL"
        lines.append(f"- **{key}**: value={val!r} source_ref=`{ref}` ({status})")
    lines.append("")

    lines.extend(
        [
            "## Ownership assignees (human names)",
            "",
            "Complete `human_assignee_name` weekly in `dealix/transformation/ownership_matrix.yaml`.",
            "When hiring a named owner, replace founder placeholders and update `human_assignee_notes_ar`.",
            "",
        ]
    )

    os_own = owners.get("os_ownership", {})
    for os_key, row in sorted(os_own.items()):
        name = row.get("human_assignee_name", "")
        status = "OK" if str(name).strip() else "TODO_ASSIGN_NAME"
        lines.append(f"- **{os_key}**: `{name or 'UNASSIGNED'}` ({status})")

    text = "\n".join(lines) + "\n"

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
