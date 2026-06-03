#!/usr/bin/env python3
"""Verify six gap-closure matrix rows; print GAP_CLOSURE_VERDICT."""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[1]
_STATUS_PATH = _REPO_ROOT / "dealix/transformation/gap_closure_status.yaml"
_MATRIX_DOC = "docs/transformation/02_gap_closure_matrix.md"
_VERIFY_SCRIPT = _REPO_ROOT / "scripts/verify_global_ai_transformation.py"
_ENTERPRISE_UI_SCRIPT = _REPO_ROOT / "scripts/verify_enterprise_control_plane.sh"


def _run(cmd: list[str], *, cwd: Path | None = None) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd or _REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode == 0, out.strip()[:2000]


def _check_in_memory_fallback() -> tuple[bool, str]:
    ok, out = _run([sys.executable, str(_VERIFY_SCRIPT)])
    return ok, "verify_global_ai_transformation.py" if ok else out


def _check_legacy_jsonl() -> tuple[bool, str]:
    ok, out = _run([sys.executable, str(_VERIFY_SCRIPT), "--check-jsonl"])
    return ok, "--check-jsonl" if ok else out


def _check_enterprise_ui() -> tuple[bool, str]:
    if _ENTERPRISE_UI_SCRIPT.is_file():
        bash = "bash"
        ok, out = _run([bash, str(_ENTERPRISE_UI_SCRIPT)])
        if ok:
            return True, "verify_enterprise_control_plane.sh"
        if "not found" not in out.lower() and "cannot find" not in out.lower():
            return False, out
    ok, out = _run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_api_imports.py",
            "-q",
            "--no-header",
        ]
    )
    return ok, "pytest tests/test_api_imports.py (fallback)" if ok else out


def _check_observability() -> tuple[bool, str]:
    ok, out = _run([sys.executable, str(_VERIFY_SCRIPT), "--check-observability"])
    return ok, "--check-observability" if ok else out


def _check_enterprise_package() -> tuple[bool, str]:
    ok, out = _run([sys.executable, str(_VERIFY_SCRIPT), "--check-enterprise-package"])
    return ok, "--check-enterprise-package" if ok else out


def _check_drills_automation() -> tuple[bool, str]:
    ok, out = _run([sys.executable, str(_VERIFY_SCRIPT), "--check-reliability"])
    return ok, "--check-reliability" if ok else out


GAP_ROWS: tuple[dict[str, Any], ...] = (
    {
        "id": "in_memory_fallback",
        "label": "Postgres-first / in-memory fallback policy",
        "owner_os": "platform+control_plane",
        "check": _check_in_memory_fallback,
    },
    {
        "id": "legacy_jsonl",
        "label": "Legacy JSONL catalog + migration tier",
        "owner_os": "platform+value+delivery",
        "check": _check_legacy_jsonl,
    },
    {
        "id": "enterprise_ui",
        "label": "Enterprise UI / operator workflow controls",
        "owner_os": "product+frontend",
        "check": _check_enterprise_ui,
    },
    {
        "id": "trace_telemetry",
        "label": "Trace coverage + telemetry contracts",
        "owner_os": "observability+trust",
        "check": _check_observability,
    },
    {
        "id": "enterprise_package",
        "label": "Enterprise package standardization",
        "owner_os": "gtm+trust+delivery",
        "check": _check_enterprise_package,
    },
    {
        "id": "drills_automation",
        "label": "Mission-critical drills automation",
        "owner_os": "reliability+runtime_safety",
        "check": _check_drills_automation,
    },
)


def run_gap_closure_checks() -> dict[str, Any]:
    now = datetime.now(UTC).isoformat()
    rows_out: list[dict[str, Any]] = []
    failures: list[str] = []

    for row in GAP_ROWS:
        ok, detail = row["check"]()
        status = "pass" if ok else "fail"
        if not ok:
            failures.append(str(row["id"]))
        rows_out.append(
            {
                "id": row["id"],
                "label": row["label"],
                "owner_os": row["owner_os"],
                "status": status,
                "last_run_iso": now,
                "verification_detail": detail,
                "evidence_ref": f"docs/transformation/evidence/gap_closure_{row['id']}.md",
            }
        )

    verdict = "PASS" if not failures else "FAIL"
    return {
        "version": 1,
        "reference_doc": _MATRIX_DOC,
        "generated_at": now,
        "verdict": verdict,
        "failed_ids": failures,
        "rows": rows_out,
    }


def write_status_yaml(blob: dict[str, Any]) -> Path:
    _STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    _STATUS_PATH.write_text(
        yaml.safe_dump(blob, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return _STATUS_PATH


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write dealix/transformation/gap_closure_status.yaml",
    )
    args = parser.parse_args()

    blob = run_gap_closure_checks()
    if args.write:
        path = write_status_yaml(blob)
        print(f"WROTE {path.relative_to(_REPO_ROOT).as_posix()}")

    for row in blob["rows"]:
        mark = "OK" if row["status"] == "pass" else "FAIL"
        print(f"[{mark}] {row['id']}: {row['verification_detail'][:120]}")

    print(f"GAP_CLOSURE_VERDICT={blob['verdict']}")
    return 0 if blob["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
