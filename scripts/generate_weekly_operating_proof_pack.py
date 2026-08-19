#!/usr/bin/env python3
"""Generate Weekly Operating Proof Pack markdown from KPI + ownership registries.

The generator is intentionally conservative: a numeric value plus a source_ref is
not the same thing as verified proof. Stale baseline periods and source references
that explicitly identify synthetic, demo, placeholder, inactive, or unsynced data
are reported as NOT_READY rather than being presented as complete evidence.
"""

from __future__ import annotations

import argparse
from datetime import UTC, date, datetime
from pathlib import Path

import yaml

_UNVERIFIED_SOURCE_MARKERS = (
    "not_synced",
    "synthetic",
    "demo",
    "sample",
    "placeholder",
    "none_active",
    "pass_required",
)
_MAX_BASELINE_AGE_DAYS = 14


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _source_status(value: object, source_ref: object) -> str:
    """Classify evidence posture without pretending source presence is proof."""
    ref = str(source_ref or "").strip()
    if value is None or not ref:
        return "PENDING_NULL"
    ref_lower = ref.lower()
    if any(marker in ref_lower for marker in _UNVERIFIED_SOURCE_MARKERS):
        return "UNVERIFIED_SOURCE"
    return "SOURCE_REF_PRESENT"


def _baseline_freshness(updated_period_iso: object, *, today: date) -> tuple[str, int | None]:
    raw = str(updated_period_iso or "").strip()
    if not raw:
        return "UNSET", None
    try:
        baseline_date = date.fromisoformat(raw)
    except ValueError:
        return "INVALID_DATE", None
    age_days = (today - baseline_date).days
    if age_days < 0:
        return "FUTURE_DATE", age_days
    if age_days > _MAX_BASELINE_AGE_DAYS:
        return "STALE", age_days
    return "CURRENT", age_days


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path, default=None, help="Write file instead of stdout")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero unless baselines are current and every metric has a non-placeholder source_ref.",
    )
    args = parser.parse_args()
    root: Path = args.repo_root

    kpi_path = root / "dealix/transformation/kpi_registry.yaml"
    own_path = root / "dealix/transformation/ownership_matrix.yaml"
    baselines_path = root / "dealix/transformation/kpi_baselines.yaml"
    kpis = _load(kpi_path)
    owners = _load(own_path)
    baselines = _load(baselines_path)

    today = datetime.now(UTC).date()
    period = today.isoformat()
    freshness, age_days = _baseline_freshness(baselines.get("updated_period_iso"), today=today)

    snaps = baselines.get("snapshots") or {}
    status_by_key: dict[str, str] = {}
    for key in sorted(snaps.keys()):
        row = snaps.get(key) or {}
        status_by_key[key] = _source_status(row.get("value_numeric"), row.get("source_ref"))

    source_ready = bool(status_by_key) and all(
        status == "SOURCE_REF_PRESENT" for status in status_by_key.values()
    )
    proof_ready = freshness == "CURRENT" and source_ready
    proof_readiness = "READY_FOR_VERIFICATION" if proof_ready else "NOT_READY"

    lines: list[str] = [
        f"# Weekly Operating Proof Pack — {period}",
        "",
        "## Proof readiness",
        "",
        f"- **proof_readiness**: `{proof_readiness}`",
        f"- **baseline_freshness**: `{freshness}`",
        f"- **baseline_age_days**: `{age_days if age_days is not None else 'UNKNOWN'}`",
        "- `SOURCE_REF_PRESENT` means a reference exists and is not explicitly marked synthetic/demo/placeholder/unsynced; it is still a verification candidate, not automatic customer proof.",
        "- `UNVERIFIED_SOURCE`, stale baselines, or missing values keep this pack NOT_READY for commercial proof claims.",
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
            "- Fill each `snapshots.*.value_numeric` from CRM / finance / delivery only when figures and sources exist.",
            "- Every non-null value must have a non-empty `source_ref`; source presence alone does not prove truth.",
            "- After editing numbers, set `updated_period_iso` to the reporting week (UTC `YYYY-MM-DD`).",
            "",
        ]
    )

    for key in sorted(snaps.keys()):
        row = snaps.get(key) or {}
        val = row.get("value_numeric")
        ref = row.get("source_ref") or ""
        lines.append(f"- **{key}**: value={val!r} source_ref=`{ref}` ({status_by_key[key]})")
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

    if args.strict and not proof_ready:
        raise SystemExit(
            "weekly proof pack is NOT_READY: refresh baselines and replace unverified source references before commercial proof use"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
