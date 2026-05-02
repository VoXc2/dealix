#!/usr/bin/env python3
"""
Launch Readiness Check — single command that decides GO_PRIVATE_BETA vs BLOCKED.

Runs (in order):
  1. compileall on product packages
  2. pytest -q --no-cov
  3. print_routes (no duplicates)
  4. smoke_inprocess (asgi-transport smoke)
  5. repo_architecture_audit
  6. env sanity (live-action flags default false)
  7. files_exist (Dockerfile, railway.json, landing/command-center.html, landing/index.html)

Flags:
  --strict   fail if pytest reports any skipped tests

Run:
  python scripts/launch_readiness_check.py
Exit 0 = GO_PRIVATE_BETA, exit 1 = BLOCKED.

Importable: scripts.launch_readiness_check.run_checks() -> ReadinessReport.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


PYTHON = sys.executable

PRODUCT_PACKAGES: tuple[str, ...] = (
    "api", "auto_client_acquisition", "core", "dealix", "integrations",
)

REQUIRED_FILES: tuple[str, ...] = (
    "Dockerfile",
    "railway.json",
    "landing/command-center.html",
    "landing/index.html",
)

# Flags whose default in settings must be False (audit also enforces presence).
FLAGS_DEFAULT_FALSE: tuple[str, ...] = (
    "whatsapp_allow_live_send",
    "gmail_allow_live_send",
    "moyasar_allow_live_charge",
    "linkedin_allow_auto_dm",
)


@dataclass
class StepResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class ReadinessReport:
    steps: list[StepResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(s.passed for s in self.steps)


def _run(cmd: list[str], cwd: Path | None = None, timeout: int = 600) -> tuple[int, str]:
    proc = subprocess.run(
        cmd,
        cwd=cwd or _REPO,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def step_compileall() -> StepResult:
    rc, out = _run([PYTHON, "-m", "compileall", "-q", *PRODUCT_PACKAGES])
    if rc != 0:
        return StepResult("compileall", False, out.splitlines()[-1] if out else f"exit {rc}")
    return StepResult("compileall", True, "OK")


def step_pytest(strict: bool) -> StepResult:
    rc, out = _run([PYTHON, "-m", "pytest", "-q", "--no-cov", "--no-header"], timeout=900)
    last_line = ""
    for line in reversed(out.splitlines()):
        if line.strip():
            last_line = line.strip()
            break

    if rc != 0:
        return StepResult("pytest", False, last_line or f"exit {rc}")

    if strict and "skipped" in last_line:
        return StepResult("pytest", False, f"strict: {last_line}")

    return StepResult("pytest", True, last_line)


def step_print_routes() -> StepResult:
    rc, out = _run([PYTHON, "scripts/print_routes.py"])
    last = next((line for line in reversed(out.splitlines()) if line.strip()), "")
    if rc != 0 or "ROUTE_CHECK_OK" not in out:
        return StepResult("print_routes", False, last or f"exit {rc}")
    # Pull the total-row count for color.
    m = re.search(r"TOTAL_ROUTE_ROWS\s+(\d+)", out)
    total = m.group(1) if m else "?"
    return StepResult("print_routes", True, f"ROUTE_CHECK_OK ({total} rows)")


def step_smoke_inprocess() -> StepResult:
    rc, out = _run([PYTHON, "scripts/smoke_inprocess.py"], timeout=180)
    last = next((line for line in reversed(out.splitlines()) if line.strip()), "")
    if rc != 0 or "SMOKE_INPROCESS_OK" not in out:
        return StepResult("smoke_inprocess", False, last or f"exit {rc}")
    return StepResult("smoke_inprocess", True, "SMOKE_INPROCESS_OK")


def step_arch_audit() -> StepResult:
    from scripts.repo_architecture_audit import run_audit
    report = run_audit()
    if report.passed:
        return StepResult("arch_audit", True, f"{report.pass_count}/{len(report.checks)} PASS")
    fails = [c.name for c in report.checks if not c.passed]
    return StepResult("arch_audit", False, "fails: " + ", ".join(fails))


def step_env_sanity() -> StepResult:
    """Check that live-action flags resolve to False in current environment."""
    try:
        # Re-import settings fresh — get_settings() is cached, so we go to the class.
        from core.config.settings import Settings
        s = Settings()
    except Exception as exc:  # noqa: BLE001
        return StepResult("env_sanity", False, f"settings load failed: {exc}")

    bad: list[str] = []
    for flag in FLAGS_DEFAULT_FALSE:
        val = getattr(s, flag, None)
        if val is None:
            bad.append(f"{flag}=missing")
            continue
        if val is True:
            bad.append(f"{flag}=True")
    if bad:
        return StepResult("env_sanity", False, "; ".join(bad))
    return StepResult("env_sanity", True, f"all {len(FLAGS_DEFAULT_FALSE)} flags False")


def step_files_exist() -> StepResult:
    missing = [f for f in REQUIRED_FILES if not (_REPO / f).exists()]
    if missing:
        return StepResult("files_exist", False, "missing: " + ", ".join(missing))
    return StepResult("files_exist", True, f"{len(REQUIRED_FILES)} required files present")


def run_checks(*, strict: bool = False, skip_pytest: bool = False) -> ReadinessReport:
    report = ReadinessReport()
    report.steps.append(step_compileall())
    if not skip_pytest:
        report.steps.append(step_pytest(strict=strict))
    report.steps.append(step_print_routes())
    report.steps.append(step_smoke_inprocess())
    report.steps.append(step_arch_audit())
    report.steps.append(step_env_sanity())
    report.steps.append(step_files_exist())
    return report


def render(report: ReadinessReport) -> str:
    lines = ["DEALIX_LAUNCH_READINESS v1.0", "=" * 36]
    for i, s in enumerate(report.steps, start=1):
        tag = "OK  " if s.passed else "FAIL"
        line = f"[{i}/{len(report.steps)}] {s.name:<18} {tag}"
        if s.detail:
            line += f"  — {s.detail}"
        lines.append(line)
    lines.append("=" * 36)
    lines.append("RESULT: " + ("GO_PRIVATE_BETA" if report.passed else "BLOCKED"))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix launch-readiness check")
    parser.add_argument("--strict", action="store_true",
                        help="fail if pytest reports any skipped tests")
    parser.add_argument("--skip-pytest", action="store_true",
                        help="skip pytest step (for fast local iteration)")
    args = parser.parse_args()

    # Force live-send flags to default-false for the readiness check itself.
    for flag in FLAGS_DEFAULT_FALSE:
        os.environ.setdefault(flag.upper(), "false")

    report = run_checks(strict=args.strict, skip_pytest=args.skip_pytest)
    print(render(report))
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
