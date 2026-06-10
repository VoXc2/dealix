#!/usr/bin/env python3
"""Export a lightweight Dealix dependency inventory.

This script avoids third-party dependencies. It records declared Python project
metadata and web package metadata so releases can keep a basic supply-chain
inventory even before a full SBOM workflow is available.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "generated" / "dependency-inventory.json"


def read_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict | None:
    text = read_text(path)
    if text is None:
        return None
    return json.loads(text)


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    web_package = read_json(ROOT / "apps" / "web" / "package.json") or {}
    web_lock_exists = (ROOT / "apps" / "web" / "package-lock.json").exists()

    inventory = {
        "schema": "dealix.dependency_inventory.v1",
        "python": {
            "pyproject_present": (ROOT / "pyproject.toml").exists(),
            "requirements_present": (ROOT / "requirements.txt").exists(),
            "requirements_dev_present": (ROOT / "requirements-dev.txt").exists(),
        },
        "web": {
            "package_name": web_package.get("name"),
            "package_version": web_package.get("version"),
            "dependencies": web_package.get("dependencies", {}),
            "devDependencies": web_package.get("devDependencies", {}),
            "package_lock_present": web_lock_exists,
        },
        "release_inputs": {
            "commit_sha_required": True,
            "image_digest_required_for_container_deploy": True,
            "high_critical_vulnerability_disposition_required": True,
        },
    }

    OUTPUT.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
