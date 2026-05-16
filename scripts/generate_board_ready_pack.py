#!/usr/bin/env python3
"""Generate a board-ready markdown pack from transformation spine."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import yaml


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    out_dir = root / "docs/transformation/evidence"
    out_dir.mkdir(parents=True, exist_ok=True)
    period = datetime.now(UTC).strftime("%Y-%m-%d")
    out = out_dir / f"board_ready_pack_{period}.md"

    kpi = yaml.safe_load((root / "dealix/transformation/kpi_registry.yaml").read_text(encoding="utf-8"))
    init = yaml.safe_load(
        (root / "dealix/transformation/strategic_initiatives_registry.yaml").read_text(encoding="utf-8")
    )
    initiatives = init.get("initiatives") or []
    active = sum(1 for r in initiatives if r.get("status") == "active")
    done = sum(1 for r in initiatives if r.get("status") == "done")

    lines = [
        f"# Board-Ready Pack — {period}",
        "",
        "## North Star",
        "",
    ]
    for row in (kpi.get("kpis") or {}).get("north_star", []):
        lines.append(f"- **{row.get('key')}**: {row.get('definition', row.get('definition_en', ''))}")

    lines.extend(
        [
            "",
            "## Strategic program",
            "",
            f"- Total initiatives: {len(initiatives)}",
            f"- Active: {active}",
            f"- Done: {done}",
            "",
            "## Verification",
            "",
            "```bash",
            "python3 scripts/verify_global_ai_transformation.py --check-initiatives",
            "bash scripts/run_executive_weekly_checklist.sh",
            "```",
            "",
        ]
    )
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
