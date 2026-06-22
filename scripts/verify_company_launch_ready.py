#!/usr/bin/env python3
"""
Dealix Verify Company Launch Ready
Checks if Dealix is ready for external operations (Sanity check before any real-world launch activity).
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


# ─── Configuration ───────────────────────────────────────────
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
]


def check_env_vars() -> list[dict]:
    """Check required environment variables."""
    issues = []
    for env in REQUIRED_ENV_VARS:
        value = os.environ.get(env, "")
        status = "OK" if value else "MISSING"
        issues.append({"check": f"Env: {env}", "status": status, "detail": value[:50] if value else ""})
    return issues


def check_directory_structure() -> list[dict]:
    """Check required directories exist."""
    issues = []
    base = Path(__file__).parent.parent
    for d in REQUIRED_DIRS:
        path = base / d
        status = "OK" if path.exists() else "MISSING"
        issues.append({"check": f"Dir: {d}", "status": status})
    return issues


def check_files() -> list[dict]:
    """Check required files exist."""
    issues = []
    base = Path(__file__).parent.parent
    for f in REQUIRED_FILES:
        path = base / f
        status = "OK" if path.exists() else "MISSING"
        issues.append({"check": f"File: {f}", "status": status})
    return issues


def check_db_connection() -> dict:
    """Check database connectivity."""
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host="localhost",
            user="dealix",
            password="dealix_pass_2026",
            database="dealix",
            port=3306,
            connect_timeout=5,
        )
        conn.ping(reconnect=True, attempts=3, delay=5)
        conn.close()
        return {"check": "DB: MySQL connection", "status": "OK", "detail": "Connected to dealix@localhost:3306"}
    except ImportError:
        return {"check": "DB: MySQL connection", "status": "WARNING", "detail": "mysql-connector not installed"}
    except Exception as e:
        return {"check": "DB: MySQL connection", "status": "BLOCKING", "detail": str(e)}


def check_node_modules() -> dict:
    """Check if node_modules is present."""
    base = Path(__file__).parent.parent
    nm = base / "node_modules"
    if nm.exists() and (nm / "react").exists():
        return {"check": "Node modules", "status": "OK", "detail": "node_modules present"}
    else:
        return {"check": "Node modules", "status": "MISSING", "detail": "node_modules not found or incomplete"}


def check_diagnostic_scripts() -> list[dict]:
    """Check diagnostic scripts compile."""
    issues = []
    base = Path(__file__).parent.parent
    scripts_dir = base / "scripts"
    if scripts_dir.exists():
        py_files = list(scripts_dir.glob("*.py"))
        for f in py_files:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(f)],
                capture_output=True,
                text=True,
            )
            status = "OK" if result.returncode == 0 else "ERROR"
            issues.append({"check": f"Compile: scripts/{f.name}", "status": status})
    return issues


def generate_launch_report(results: list[dict], output_path: str = None) -> str:
    """Generate launch readiness report."""
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    total = len(results)
    ok = sum(1 for r in results if r["status"] == "OK")
    blocking = [r for r in results if r["status"] in ("BLOCKING", "MISSING", "ERROR")]
    warnings = [r for r in results if r["status"] == "WARNING"]
    
    md = f"""# Dealix Launch Readiness Report
*Generated: {today}*

---

## Summary

| Metric | Count |
|--------|-------|
| Total Checks | {total} |
| Passed | {ok} |
| Blocking | {len(blocking)} |
| Warnings | {len(warnings)} |

## Status

| Check | Status | Detail |
|-------|--------|--------|
"""
    for r in results:
        status_icon = "✅" if r["status"] == "OK" else "🔴" if r["status"] in ("BLOCKING", "ERROR") else "🟡"
        detail = r.get("detail", "")
        md += f"| {r['check']} | {status_icon} {r['status']} | {detail} |\n"
    
    md += "\n---\n\n"
    
    if blocking:
        md += "## 🔴 BLOCKING ISSUES (Must fix before launch)\n\n"
        for b in blocking:
            md += f"- **{b['check']}**: {b.get('detail', '')}\n"
        md += "\n"
    
    if warnings:
        md += "## 🟡 WARNINGS (Should address soon)\n\n"
        for w in warnings:
            md += f"- **{w['check']}**: {w.get('detail', '')}\n"
        md += "\n"
    
    md += "---\n\n"
    
    if not blocking:
        md += "## ✅ LAUNCH DECISION: GO\n\n"
        md += "All critical checks passed. Dealix is ready for controlled external operations.\n\n"
        md += "**Next steps:\n"
        md += "1. Run `python scripts/verify_no_auto_external_send.py`\n"
        md += "2. Ensure OUTBOUND_MODE=draft_only\n"
        md += "3. Start `make company-day`\n"
    else:
        md += "## 🚫 LAUNCH DECISION: NO-GO\n\n"
        md += "Critical issues detected. Fix blockers before any external launch activity.\n\n"
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md)
    
    return md


def main():
    """Run all launch readiness checks."""
    print("=" * 70)
    print("  DEALIX — COMPANY LAUNCH READINESS CHECK")
    print("=" * 70)
    print()
    
    all_results = []
    
    all_results += check_env_vars()
    all_results += check_directory_structure()
    all_results += check_files()
    all_results.append(check_db_connection())
    all_results.append(check_node_modules())
    all_results += check_diagnostic_scripts()
    
    # Print table
    print(f"  {'Check':<40} {'Status':<12} Detail")
    print("  " + "-" * 90)
    for r in all_results:
        status_icon = "✅" if r["status"] == "OK" else "🔴" if r["status"] in ("BLOCKING", "ERROR") else "🟡"
        detail = r.get("detail", "")[:40]
        print(f"  {r['check']:<40} {status_icon} {r['status']:<10} {detail}")
    
    print()
    
    blocking = [r for r in all_results if r["status"] in ("BLOCKING", "ERROR")]
    warnings = [r for r in all_results if r["status"] in ("WARNING", "MISSING")]
    
    print(f"  Total: {len(all_results)} | OK: {sum(1 for r in all_results if r['status']=='OK')} | Blocking: {len(blocking)} | Warnings: {len(warnings)}")
    print()
    
    # Generate report
    base = Path(__file__).parent.parent
    report_path = base / "company_os" / "reports" / "LAUNCH_READINESS_REPORT.md"
    md = generate_launch_report(all_results, str(report_path))
    
    if blocking:
        print("  🚫 LAUNCH DECISION: NO-GO")
        print(f"  📄 Report saved: {report_path}")
        sys.exit(1)
    else:
        print("  ✅ LAUNCH DECISION: GO")
        print(f"  📄 Report saved: {report_path}")
        sys.exit(0)


if __name__ == "__main__":
    main()
