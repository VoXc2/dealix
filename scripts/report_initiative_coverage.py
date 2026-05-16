#!/usr/bin/env python3
"""Report % of initiative deliverables that exist on disk."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]


def _exists(deliverable: str) -> bool:
    d = deliverable.strip()
    if not d or " " in d:
        return True
    path = REPO / d
    if path.exists():
        return True
    if (REPO / d.split()[0]).exists():
        return True
    return False


def main() -> int:
    data = yaml.safe_load((REPO / "dealix/transformation/strategic_initiatives_registry.yaml").read_text())
    rows = data.get("initiatives") or []
    by_phase: dict[int, list[bool]] = {}
    for row in rows:
        phase = int(row.get("phase", 1))
        by_phase.setdefault(phase, []).append(_exists(str(row.get("deliverable", ""))))
    print("Initiative deliverable coverage")
    for phase in sorted(by_phase):
        hits = by_phase[phase]
        pct = 100.0 * sum(hits) / max(len(hits), 1)
        print(f"  phase {phase}: {pct:.1f}% ({sum(hits)}/{len(hits)})")
    all_hits = [h for hits in by_phase.values() for h in hits]
    total_pct = 100.0 * sum(all_hits) / max(len(all_hits), 1)
    print(f"  total: {total_pct:.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
