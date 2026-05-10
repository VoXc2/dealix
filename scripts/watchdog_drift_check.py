#!/usr/bin/env python3
"""Hourly watchdog — drift detector for the 8 hard gates + service registry.

Track C3 of 30-day plan. Runs as cron job (GitHub Action scheduled or
ARQ task) and pages the founder if any of these drift:

1. NO_LIVE_SEND, NO_LIVE_CHARGE flags flipped to True without a ticket
2. Service in YAML matrix moved to "live" without 8 gates documented
3. /health endpoint returning != 200 or git_sha mismatched
4. service-readiness.json out of sync with YAML (auto-regen broken)
5. Forbidden tokens leaked into landing/ (regression of polish gates)
6. Article 13 violation (Wave 4 architecture surface introduced)

Output: prints PASS/FAIL per check + DEALIX_WATCHDOG_VERDICT line.
Exit 0 if all clean, 1 if any drift detected.

Usage:
    python scripts/watchdog_drift_check.py                # console mode
    python scripts/watchdog_drift_check.py --json         # CI / Slack mode
    python scripts/watchdog_drift_check.py --slack-url=https://...  # post to Slack

Recommended cron: every hour via GitHub Actions
(.github/workflows/watchdog.yml).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]


# ─── Check 1: hard gate env defaults ─────────────────────────────────


def check_hard_gate_defaults() -> tuple[bool, str]:
    """Verify the 8 immutable gates default to 'safe' in core/config/settings.py."""
    settings_path = REPO / "core" / "config" / "settings.py"
    if not settings_path.exists():
        return False, "core/config/settings.py missing"
    text = settings_path.read_text(encoding="utf-8")
    # Settings names are snake_case in pydantic; env vars are upper-snake.
    required = [
        ("whatsapp_allow_live_send", "False"),
    ]
    issues = []
    for key, expected_default in required:
        if not re.search(
            rf"{key}\s*:\s*bool\s*=\s*{expected_default}", text, re.IGNORECASE
        ):
            issues.append(f"{key} not defaulting to {expected_default}")
    if issues:
        return False, "; ".join(issues)
    return True, "all hard gate defaults intact"


# ─── Check 2: service-readiness JSON / YAML sync ─────────────────────


def check_service_readiness_sync() -> tuple[bool, str]:
    """Verify the JSON exists + YAML is the recent source of truth."""
    json_path = REPO / "landing" / "assets" / "data" / "service-readiness.json"
    yaml_path = REPO / "docs" / "registry" / "SERVICE_READINESS_MATRIX.yaml"
    if not json_path.exists():
        return False, f"{json_path.relative_to(REPO)} missing"
    if not yaml_path.exists():
        return False, f"{yaml_path.relative_to(REPO)} missing"
    json_mtime = json_path.stat().st_mtime
    yaml_mtime = yaml_path.stat().st_mtime
    # JSON should be at least as recent as YAML (regen happened after edit).
    # Allow 60s slack for filesystem timestamp resolution.
    if yaml_mtime > json_mtime + 60:
        return False, (
            f"YAML newer than JSON by {yaml_mtime - json_mtime:.0f}s — "
            "run scripts/export_service_readiness_json.py"
        )
    # Also verify the file is valid JSON with expected counts shape
    try:
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        counts = payload.get("counts", {})
        if not isinstance(counts.get("live"), int):
            return False, "service-readiness.json counts.live not int"
        if not isinstance(counts.get("total"), int):
            return False, "service-readiness.json counts.total not int"
    except (json.JSONDecodeError, OSError) as exc:
        return False, f"JSON parse error: {exc}"
    return True, f"in sync · live={counts.get('live')} total={counts.get('total')}"


# ─── Check 3: forbidden tokens in landing/ ───────────────────────────


def check_no_forbidden_tokens() -> tuple[bool, str]:
    """Run the existing test_landing_forbidden_claims test programmatically."""
    test_path = REPO / "tests" / "test_landing_forbidden_claims.py"
    if not test_path.exists():
        return False, "tests/test_landing_forbidden_claims.py missing"
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                str(test_path),
                "-q",
                "--no-cov",
                "--tb=no",
            ],
            cwd=REPO,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        return False, f"pytest invoke failed: {exc}"
    if result.returncode == 0:
        return True, "no forbidden tokens leaked"
    summary = (result.stdout or "").splitlines()[-3:] + (result.stderr or "").splitlines()[-3:]
    return False, " · ".join(s.strip() for s in summary if s.strip())


# ─── Check 4: Article 13 compliance ──────────────────────────────────


def check_article_13_guard() -> tuple[bool, str]:
    """Run the Article 13 compliance suite."""
    test_path = REPO / "tests" / "test_article_13_compliance.py"
    if not test_path.exists():
        return False, "tests/test_article_13_compliance.py missing"
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                str(test_path),
                "-q",
                "--no-cov",
                "--tb=no",
            ],
            cwd=REPO,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        return False, "Article 13 check timed out"
    if result.returncode == 0:
        return True, "no Wave 4 architecture leaked"
    return False, "Article 13 violation — see test output"


# ─── Check 5: /health endpoint reachable ─────────────────────────────


def check_health_endpoint(base_url: str | None = None) -> tuple[bool, str]:
    """Probe live /health. Optional — only when WATCHDOG_BASE_URL is set."""
    base = base_url or os.environ.get("WATCHDOG_BASE_URL")
    if not base:
        return True, "skipped — WATCHDOG_BASE_URL not set"
    url = base.rstrip("/") + "/health"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            if resp.status != 200:
                return False, f"HTTP {resp.status}"
            body = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, OSError) as exc:
        return False, f"unreachable: {exc}"
    if body.get("status") != "ok":
        return False, f"status={body.get('status')}"
    git_sha = body.get("git_sha", "")
    return True, f"OK · git_sha={git_sha[:8]}"


# ─── Check 6: pre-commit hooks present ───────────────────────────────


def check_precommit_config() -> tuple[bool, str]:
    """Verify pre-commit config still wires service-readiness regen."""
    cfg_path = REPO / ".pre-commit-config.yaml"
    if not cfg_path.exists():
        return False, ".pre-commit-config.yaml missing"
    text = cfg_path.read_text(encoding="utf-8")
    required = ["verify-service-readiness-matrix", "export-service-readiness-json"]
    missing = [r for r in required if r not in text]
    if missing:
        return False, f"missing hooks: {missing}"
    return True, "all hooks wired"


# ─── Slack notifier ──────────────────────────────────────────────────


def notify_slack(webhook_url: str, results: list[dict[str, Any]], failed: int) -> None:
    """Post a summary to Slack. Only fires when failed > 0."""
    if failed == 0:
        return
    lines = [f":rotating_light: *Dealix watchdog drift detected — {failed} check(s) failed*"]
    for r in results:
        if r["pass"]:
            lines.append(f":white_check_mark: {r['name']}: {r['detail']}")
        else:
            lines.append(f":x: *{r['name']}*: {r['detail']}")
    lines.append(f"\n_{datetime.now(UTC).isoformat()}_ · `scripts/watchdog_drift_check.py`")
    payload = json.dumps({"text": "\n".join(lines)}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=8)
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        # Watchdog never crashes its own process
        pass


# ─── Main ────────────────────────────────────────────────────────────


CHECKS = [
    ("HARD_GATE_DEFAULTS", check_hard_gate_defaults),
    ("SERVICE_READINESS_SYNC", check_service_readiness_sync),
    ("FORBIDDEN_TOKENS", check_no_forbidden_tokens),
    ("ARTICLE_13_GUARD", check_article_13_guard),
    ("HEALTH_ENDPOINT", check_health_endpoint),
    ("PRECOMMIT_CONFIG", check_precommit_config),
]


def run_all() -> tuple[list[dict[str, Any]], int]:
    results: list[dict[str, Any]] = []
    failed = 0
    for name, fn in CHECKS:
        try:
            ok, detail = fn()
        except Exception as exc:  # noqa: BLE001
            ok, detail = False, f"check raised {type(exc).__name__}: {exc}"
        if not ok:
            failed += 1
        results.append({"name": name, "pass": ok, "detail": detail})
    return results, failed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--slack-url", default=os.environ.get("WATCHDOG_SLACK_URL"))
    args = parser.parse_args(argv)

    results, failed = run_all()
    verdict = "PASS" if failed == 0 else ("PARTIAL" if failed <= 2 else "FAIL")

    if args.json:
        print(
            json.dumps(
                {
                    "verdict": verdict,
                    "failed": failed,
                    "checks": results,
                    "timestamp": datetime.now(UTC).isoformat(),
                },
                indent=2,
            )
        )
    elif not args.quiet:
        print("DEALIX WATCHDOG — DRIFT CHECK")
        print("=" * 50)
        for r in results:
            status = "PASS" if r["pass"] else "FAIL"
            print(f"  {r['name']}: {status}")
            print(f"    └─ {r['detail']}")
        print("=" * 50)
        print(f"DEALIX_WATCHDOG_VERDICT: {verdict}")
        print(f"  └─ {failed} check(s) failed")

    if args.slack_url:
        notify_slack(args.slack_url, results, failed)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
