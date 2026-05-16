#!/usr/bin/env python3
"""Generate docs/architecture/CAPABILITY_MAP.md from capability_map.yaml."""

from __future__ import annotations

from pathlib import Path

import yaml


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    src = root / "dealix/transformation/capability_map.yaml"
    out = root / "docs/architecture/CAPABILITY_MAP.md"
    data = yaml.safe_load(src.read_text(encoding="utf-8")) or {}
    caps = data.get("capabilities") or []
    lines = ["# Dealix Capability Map", "", "| ID | Layer | Modules | APIs |", "| --- | --- | --- | --- |"]
    for cap in caps:
        mods = ", ".join(cap.get("modules") or [])
        apis = ", ".join(cap.get("apis") or [])
        lines.append(f"| {cap.get('id', '')} | {cap.get('layer', '')} | `{mods}` | {apis} |")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
