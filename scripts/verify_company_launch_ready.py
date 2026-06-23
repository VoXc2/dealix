#!/usr/bin/env python3
"""
Dealix Verify Company Launch Ready
Checks if the codebase is ready for controlled launch and deployment prep.
"""

import os
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


REQUIRED_ENV_VARS = [
    "DATABASE_URL",
]

REQUIRED_DIRS = [
    "api",
    "src",
    "db",
    "scripts",
    "company_os",
]

REQUIRED_FILES = [
    "package.json",
    "Dockerfile",
    "docker-compose.yml",
    "db/schema.ts",
    "api/router.ts",
    "src/App.tsx",
    "scripts/verify_no_auto_external_send.py",
    ".env.example",
]

ENV_DOC_PATH = "docs/ops/ENVIRONMENT_VARIABLES.md"
ENV_EXAMPLE_PATH = ".env.example"


def load_local_env_files() -> None:
    base = Path(__file__).parent.parent
    for env_name in [".env", ".env.local"]:
        env_path = base / env_name
        if not env_path.exists():
            continue

        for raw_line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            if key and key not in os.environ:
                os.environ[key] = value


def check_env_vars() -> list[dict]:
    issues = []
    base = Path(__file__).parent.parent
    env_doc = base / ENV_DOC_PATH
    for env_name in REQUIRED_ENV_VARS:
        value = os.environ.get(env_name, "")
        if value:
            status = "OK"
            detail = value[:50]
        elif env_doc.exists():
            status = "WARNING"
            detail = f"Missing in current shell; see {ENV_DOC_PATH}"
        else:
            status = "MISSING"
            detail = ""
        issues.append(
            {
                "check": f"Env: {env_name}",
                "status": status,
                "detail": detail,
            }
        )
    return issues


def check_directory_structure() -> list[dict]:
    issues = []
    base = Path(__file__).parent.parent
    for directory in REQUIRED_DIRS:
        path = base / directory
        issues.append(
            {
                "check": f"Dir: {directory}",
                "status": "OK" if path.exists() else "MISSING",
                "detail": "",
            }
        )
    return issues


def check_files() -> list[dict]:
    issues = []
    base = Path(__file__).parent.parent
    for file_path in REQUIRED_FILES:
        path = base / file_path
        issues.append(
            {
                "check": f"File: {file_path}",
                "status": "OK" if path.exists() else "MISSING",
                "detail": "",
            }
        )
    return issues


def check_db_connection() -> dict:
    database_url = os.environ.get("DATABASE_URL", "").strip()
    if not database_url:
        return {
            "check": "DB: MySQL connection",
            "status": "WARNING",
            "detail": f"Skipped; DATABASE_URL not loaded. See {ENV_DOC_PATH}",
        }

    try:
        parsed = urlparse(database_url)
        host = parsed.hostname or "localhost"
        port = parsed.port or 3306
        with socket.create_connection((host, port), timeout=5):
            pass
        return {
            "check": "DB: MySQL connection",
            "status": "OK",
            "detail": f"TCP reachable at {host}:{port}",
        }
    except Exception as error:
        return {
            "check": "DB: MySQL connection",
            "status": "BLOCKING",
            "detail": str(error),
        }


def check_node_modules() -> dict:
    base = Path(__file__).parent.parent
    node_modules = base / "node_modules"
    react_module = node_modules / "react"
    return {
        "check": "Node modules",
        "status": "OK" if node_modules.exists() and react_module.exists() else "MISSING",
        "detail": "node_modules present" if node_modules.exists() and react_module.exists() else "node_modules not found or incomplete",
    }


def check_diagnostic_scripts() -> list[dict]:
    issues = []
    base = Path(__file__).parent.parent
    scripts_dir = base / "scripts"
    if not scripts_dir.exists():
        return issues

    for script_path in sorted(scripts_dir.glob("*.py")):
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(script_path)],
            capture_output=True,
            text=True,
        )
        issues.append(
            {
                "check": f"Compile: scripts/{script_path.name}",
                "status": "OK" if result.returncode == 0 else "ERROR",
                "detail": "",
            }
        )
    return issues


def generate_launch_report(results: list[dict], output_path: str | None = None) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = len(results)
    passed = sum(1 for result in results if result["status"] == "OK")
    blocking = [result for result in results if result["status"] in ("BLOCKING", "MISSING", "ERROR")]
    warnings = [result for result in results if result["status"] == "WARNING"]

    report = f"""# Dealix Launch Readiness Report
*Generated: {generated_at}*

---

## Summary

| Metric | Count |
|--------|-------|
| Total Checks | {total} |
| Passed | {passed} |
| Blocking | {len(blocking)} |
| Warnings | {len(warnings)} |

## Status

| Check | Status | Detail |
|-------|--------|--------|
"""
    for result in results:
        report += f"| {result['check']} | {result['status']} | {result.get('detail', '')} |\n"

    report += "\n---\n\n"

    if blocking:
        report += "## BLOCKING ISSUES\n\n"
        for item in blocking:
            report += f"- **{item['check']}**: {item.get('detail', '')}\n"
        report += "\n"

    if warnings:
        report += "## WARNINGS\n\n"
        for item in warnings:
            report += f"- **{item['check']}**: {item.get('detail', '')}\n"
        report += "\n"

    if not blocking:
        report += "## LAUNCH DECISION: GO\n\n"
        report += "All critical checks passed.\n"
    else:
        report += "## LAUNCH DECISION: NO-GO\n\n"
        report += "Fix blockers before external launch activity.\n"

    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(report, encoding="utf-8")

    return report


def check_env_doc() -> dict:
    base = Path(__file__).parent.parent
    env_doc = base / ENV_DOC_PATH
    env_example = base / ENV_EXAMPLE_PATH
    if not env_example.exists():
        return {
            "check": "Env: .env.example contract file",
            "status": "MISSING",
            "detail": f"Create {ENV_EXAMPLE_PATH} with safe placeholder values",
        }
    if not env_doc.exists():
        return {
            "check": "Env: environment docs",
            "status": "WARNING",
            "detail": f"{ENV_DOC_PATH} missing; create from {ENV_EXAMPLE_PATH}",
        }
    return {
        "check": "Env: environment contract",
        "status": "OK",
        "detail": f"{ENV_EXAMPLE_PATH} present; see {ENV_DOC_PATH}",
    }


def main():
    load_local_env_files()

    print("=" * 70)
    print("  DEALIX - COMPANY LAUNCH READINESS CHECK")
    print("=" * 70)
    print()

    all_results = []
    all_results.extend(check_env_vars())
    all_results.append(check_env_doc())
    all_results.extend(check_directory_structure())
    all_results.extend(check_files())
    all_results.append(check_db_connection())
    all_results.append(check_node_modules())
    all_results.extend(check_diagnostic_scripts())

    print(f"  {'Check':<40} {'Status':<12} Detail")
    print("  " + "-" * 90)
    for result in all_results:
        status_icon = (
            "[OK]"
            if result["status"] == "OK"
            else "[BLOCK]"
            if result["status"] in ("BLOCKING", "ERROR")
            else "[WARN]"
        )
        detail = result.get("detail", "")[:40]
        print(f"  {result['check']:<40} {status_icon} {result['status']:<10} {detail}")

    print()

    blocking = [result for result in all_results if result["status"] in ("BLOCKING", "ERROR", "MISSING")]
    warnings = [result for result in all_results if result["status"] == "WARNING"]
    ok_count = sum(1 for result in all_results if result["status"] == "OK")
    print(f"  Total: {len(all_results)} | OK: {ok_count} | Blocking: {len(blocking)} | Warnings: {len(warnings)}")
    print()

    base = Path(__file__).parent.parent
    report_path = base / "company_os" / "reports" / "LAUNCH_READINESS_REPORT.md"
    generate_launch_report(all_results, str(report_path))

    if blocking:
        print("  LAUNCH DECISION: NO-GO")
        print(f"  Report saved: {report_path}")
        sys.exit(1)

    print("  LAUNCH DECISION: GO")
    print(f"  Report saved: {report_path}")
    sys.exit(0)


if __name__ == "__main__":
    main()