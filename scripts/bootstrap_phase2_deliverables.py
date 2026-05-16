#!/usr/bin/env python3
"""Create stub deliverable files for phase-2 initiatives when missing."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "dealix/transformation/strategic_initiatives_registry.yaml"


def _touch(path: Path, header: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix in (".yaml", ".yml"):
        path.write_text(f"# {header}\nversion: 1\n", encoding="utf-8")
    elif path.suffix == ".py":
        path.write_text(
            f'"""{header} — stub."""\n\nfrom __future__ import annotations\n',
            encoding="utf-8",
        )
    elif path.suffix == ".md":
        path.write_text(f"# {header}\n\nStub — expand per initiative.\n", encoding="utf-8")
    elif path.suffix == ".sh":
        path.write_text("#!/bin/bash\nset -euo pipefail\necho \"stub: OK\"\n", encoding="utf-8")
    elif path.suffix == ".log":
        path.write_text(f"# {header}\n", encoding="utf-8")
    elif path.suffix == ".json":
        path.write_text("[]\n", encoding="utf-8")
    else:
        path.write_text(f"# {header}\n", encoding="utf-8")


def main() -> int:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}
    created = 0
    for row in data.get("initiatives") or []:
        if int(row.get("phase", 1)) != 2:
            continue
        deliverable = str(row.get("deliverable", "")).strip()
        if not deliverable or " " in deliverable or deliverable.endswith(".py"):
            continue
        path = REPO / deliverable
        if path.exists():
            continue
        _touch(path, f"Initiative {row.get('id')} — {row.get('title_en', '')}")
        created += 1
    print(f"Created {created} stub deliverable paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
