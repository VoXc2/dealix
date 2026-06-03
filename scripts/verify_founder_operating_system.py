#!/usr/bin/env python3
"""Verify the founder operating system files that keep Dealix production-ready.

The check is dependency-free and focuses on repo governance, deploy safety,
incident response, and evidence discipline.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = {
    "deployment": [
        "railway.json",
        "frontend/railway.json",
        "apps/web/railway.json",
        "dealix/config/railway_services.json",
        "scripts/verify_railway_surfaces.py",
        "scripts/railway_smoke_matrix.py",
        "scripts/founder_launch_final_check.py",
        "scripts/founder_a_to_z_finalize.sh",
    ],
    "ci_security": [
        ".github/workflows/ci.yml",
        ".github/workflows/security.yml",
        ".github/workflows/repository-hardening.yml",
        ".github/workflows/scorecard.yml",
        ".github/dependabot.yml",
        ".pre-commit-config.yaml",
        "SECURITY.md",
    ],
    "governance": [
        ".github/CODEOWNERS",
        ".github/pull_request_template.md",
        ".github/ISSUE_TEMPLATE/production_incident.yml",
        "docs/ops/FOUNDER_A_TO_Z_LAUNCH_RUNBOOK_AR.md",
        "docs/ops/RAILWAY_SERVICE_ENV_MATRIX_AR.md",
        "docs/ops/POST_DEPLOY_EVIDENCE_TEMPLATE_AR.md",
        "docs/ops/RAILWAY_FAILURE_RESPONSE_AR.md",
    ],
}

FORBIDDEN_MARKERS = [
    "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY",
    "NEXT_PUBLIC_ADMIN_API_KEY",
    "sk_live_REAL",
    "BEGIN PRIVATE KEY",
]


def fail(message: str) -> None:
    raise SystemExit(f"FOUNDER_OS_FAIL: {message}")


def read(path: str) -> str:
    target = ROOT / path
    if not target.exists():
        fail(f"missing {path}")
    return target.read_text(encoding="utf-8", errors="replace")


def main() -> None:
    for group, paths in REQUIRED_FILES.items():
        for path in paths:
            read(path)
        print(f"FOUNDER_OS_GROUP_OK {group} files={len(paths)}")

    checked_paths = [
        "frontend/Dockerfile",
        "apps/web/Dockerfile",
        ".env.example",
        "docs/ops/RAILWAY_SERVICE_ENV_MATRIX_AR.md",
    ]
    for path in checked_paths:
        content = read(path)
        for marker in FORBIDDEN_MARKERS:
            if marker in content:
                fail(f"forbidden marker {marker!r} found in {path}")

    print("FOUNDER_OS_OK")


if __name__ == "__main__":
    main()
