#!/usr/bin/env python3
"""Export a lightweight release manifest for Dealix production handoff."""

from __future__ import annotations

import json
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "generated" / "release-manifest.json"


def current_commit() -> str:
    env_sha = os.getenv("GITHUB_SHA")
    if env_sha:
        return env_sha
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "dealix.release_manifest.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "commit_sha": current_commit(),
        "checks": [
            "make env-check",
            "make api-contract-check",
            "make security-smoke",
            "make dependency-inventory",
            "make prod-verify",
        ],
        "documents": {
            "production_readiness": exists("docs/ops/PRODUCTION_READINESS_CHECKLIST.md"),
            "commercial_go_live": exists("docs/ops/COMMERCIAL_GO_LIVE_GATE.md"),
            "domain_runbook": exists("docs/ops/DOMAIN_OPERATIONS_RUNBOOK.md"),
            "frontend_runbook": exists("docs/ops/FRONTEND_PRODUCTION_RUNBOOK.md"),
            "server_hardening": exists("docs/ops/SERVER_HARDENING_CHECKLIST.md"),
            "monitoring": exists("docs/ops/MONITORING_MATRIX.md"),
            "incident_drill": exists("docs/ops/LIVE_DOMAIN_INCIDENT_DRILL.md"),
            "supply_chain_policy": exists("docs/ops/SBOM_AND_SUPPLY_CHAIN_POLICY.md"),
        },
        "artifacts": {
            "dependency_inventory": "docs/generated/dependency-inventory.json",
            "openapi_baseline": "docs/architecture/openapi.json",
        },
    }
    OUTPUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
