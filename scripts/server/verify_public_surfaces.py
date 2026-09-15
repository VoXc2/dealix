#!/usr/bin/env python3
"""
Verify public frontend/backend surfaces are documented.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

SURFACES = {
    "backend": {
        "health": "/health",
        "version": "/version",
        "meta": "/api/v1/meta",
        "leads": "/api/v1/leads",
        "business_now": "/api/v1/business-now/snapshot",
    },
    "frontend": {
        "home": "/",
        "diagnostic": "/dealix-diagnostic",
        "command_room": "/ops/command-room",
        "founder": "/ops/founder",
    },
}


def main() -> int:
    out_dir = REPO_ROOT / "reports" / "server"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "public_surfaces.json"
    path.write_text(json.dumps(SURFACES, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Public surfaces documented:")
    for layer, routes in SURFACES.items():
        print(f"  {layer}:")
        for name, route in routes.items():
            print(f"    {name}: {route}")
    print(f"\nSaved to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
