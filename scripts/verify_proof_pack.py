#!/usr/bin/env python3
"""Verify proof pack templates exist for blueprint services."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]


def main() -> int:
    mp = yaml.safe_load((REPO / "docs" / "company" / "SERVICE_ID_MAP.yaml").read_text(encoding="utf-8")) or {}
    missing: list[str] = []
    for row in mp.get("mappings") or []:
        folder = row.get("folder")
        if not folder:
            continue
        if folder in ("ai_governance_program", "client_ai_policy_pack"):
            continue  # program / policy pack: proof optional or different shape
        candidates = [
            REPO / "docs" / "services" / folder / "proof_pack_template.md",
            REPO / "docs" / "services" / folder / "proof_pack.md",
        ]
        if not any(p.is_file() for p in candidates):
            missing.append(f"missing_proof_template:{folder}")
    for m in missing:
        print(m, file=sys.stderr)
    ok = not missing
    print(f"PROOF_PACK_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
