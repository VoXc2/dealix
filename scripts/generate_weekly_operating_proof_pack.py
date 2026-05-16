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
    initiatives_path = root / "dealix/transformation/strategic_initiatives_registry.yaml"
    manifest_path = root / "dealix/transformation/north_star_manifest.yaml"
    kpis = _load(kpi_path)
    owners = _load(own_path)
    baselines = _load(baselines_path)
    initiatives = _load(initiatives_path)
    manifest = _load(manifest_path)

    period = datetime.now(UTC).strftime("%Y-%m-%d")
    lines: list[str] = [
        f"# Weekly Operating Proof Pack — {period}",
        "",
        "## North Star (canonical manifest)",
        "",
        f"- **statement**: {manifest.get('statement_en', manifest.get('statement_ar', ''))}",
        f"- **primary_metric_key**: `{manifest.get('primary_metric_key', '')}`",
        "",
        "## Product Evidence Review Board (PERB)",
        "",
        "| decision | evidence_level | kpi_impact | owner | status |",
        "| --- | --- | --- | --- | --- |",
        "| _fill during Wednesday PERB_ | L2+ | _kpi key_ | product | proposed |",
        "",
        "Log file: `docs/transformation/evidence/perb_decisions.log`",
        "",
        "## Strategic initiatives rollup",
        "",
    ]

    init_rows = initiatives.get("initiatives") or []
    status_counts: dict[str, int] = {}
    for row in init_rows:
        st = str(row.get("status", "proposed"))
        status_counts[st] = status_counts.get(st, 0) + 1
    for st, count in sorted(status_counts.items()):
        lines.append(f"- **{st}**: {count}")
    phase_counts: dict[int, int] = {}
    for row in init_rows:
        ph = int(row.get("phase", 1))
        phase_counts[ph] = phase_counts.get(ph, 0) + 1
    lines.append("")
    lines.append("### Phase rollup")
    for ph in sorted(phase_counts):
        lines.append(f"- **phase {ph}**: {phase_counts[ph]} initiatives")
    ai_econ = root / "dealix/transformation/ai_unit_economics.yaml"
    if ai_econ.exists():
        lines.append("")
        lines.append("## AI unit economics (phase 2)")
        lines.append("")
        lines.append(f"- config: `{ai_econ.relative_to(root).as_posix()}`")
    active = [r for r in init_rows if r.get("status") == "active"]
    if active:
        lines.append("")
        lines.append("### Active initiatives (sample)")
        for row in active[:10]:
            lines.append(
                f"- #{row.get('id')} {row.get('title_en', '')} — wave {row.get('wave')} "
                f"(`{row.get('deliverable', '')}`)"
            )
    lines.extend(["", "## KPI evidence checklist", ""])

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

    founder_required: set[str] = set()
    founder_path = root / "dealix/transformation/kpi_founder_required.yaml"
    if founder_path.exists():
        founder_required = set(
            (yaml.safe_load(founder_path.read_text(encoding="utf-8")) or {}).get(
                "founder_required_keys"
            )
            or []
        )

    snaps = baselines.get("snapshots") or {}
    for key in sorted(snaps.keys()):
        row = snaps.get(key) or {}
        val = row.get("value_numeric")
        ref = row.get("source_ref") or ""
        if val is not None and str(ref).strip():
            status = "FILLED"
        elif key in founder_required:
            status = "FOUNDER_REQUIRED"
        else:
            status = "PENDING_NULL"
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
