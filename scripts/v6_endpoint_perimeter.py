#!/usr/bin/env python3
"""v6 Phase 1 — endpoint perimeter check (read-only, stdlib-only).

Hits every v5/v6 read-only status endpoint shipped on this branch and
prints a bilingual PASS/FAIL table (Arabic primary, English secondary).
Mirrors the spirit of ``scripts/dealix_smoke_test.py`` but is scoped to
the *perimeter* — one row per endpoint, no body assertions, no secrets,
no POST, no outbound write.

Usage:
    python scripts/v6_endpoint_perimeter.py
    python scripts/v6_endpoint_perimeter.py --base-url http://127.0.0.1:8000
    python scripts/v6_endpoint_perimeter.py --json
    python scripts/v6_endpoint_perimeter.py --timeout 5

Exit codes:
    0  every required endpoint returned the expected status
    1  at least one required endpoint failed
    2  base URL was unreachable on every probe
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any


DEFAULT_BASE_URL = os.getenv("DEALIX_BASE_URL", "https://api.dealix.me")
DEFAULT_TIMEOUT = float(os.getenv("DEALIX_PERIMETER_TIMEOUT", "10"))


@dataclass
class Check:
    path: str
    expected_status: int = 200
    required: bool = True


@dataclass
class CheckResult:
    path: str
    expected_status: int
    actual_status: int | None
    ok: bool
    elapsed_ms: float
    required: bool
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# Every endpoint below is GET-only and expected to return 200 on a
# healthy deploy. Order roughly follows the v5 layer numbering with
# v6-era additions (founder, diagnostic, company-brain, search-radar,
# self-growth) appended.
CHECKS: list[Check] = [
    Check(path="/health"),
    Check(path="/api/v1/customer-loop/status"),
    Check(path="/api/v1/customer-data/status"),
    Check(path="/api/v1/agent-governance/status"),
    Check(path="/api/v1/delivery-factory/status"),
    Check(path="/api/v1/proof-ledger/status"),
    Check(path="/api/v1/finance/status"),
    Check(path="/api/v1/gtm/status"),
    Check(path="/api/v1/role-command/ceo"),
    Check(path="/api/v1/role-command/sales"),
    Check(path="/api/v1/reliability/status"),
    Check(path="/api/v1/security-privacy/status"),
    Check(path="/api/v1/vertical-playbooks/status"),
    Check(path="/api/v1/founder/dashboard"),
    Check(path="/api/v1/founder/status"),
    Check(path="/api/v1/diagnostic/status"),
    Check(path="/api/v1/company-brain/status"),
    Check(path="/api/v1/search-radar/status"),
    Check(path="/api/v1/self-growth/status"),
    Check(path="/api/v1/self-growth/service-activation"),
    Check(path="/api/v1/self-growth/seo/audit"),
    Check(path="/api/v1/service-quality/status"),
]


def _do_request(base_url: str, check: Check, timeout: float) -> CheckResult:
    url = f"{base_url.rstrip('/')}{check.path}"
    started = datetime.now(UTC)
    actual: int | None = None
    detail = ""
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            actual = resp.status
            # drain body so the connection is reusable
            resp.read()
    except urllib.error.HTTPError as exc:
        actual = exc.code
    except (urllib.error.URLError, TimeoutError) as exc:
        detail = f"network: {type(exc).__name__}: {exc}"
    except Exception as exc:  # noqa: BLE001
        detail = f"error: {type(exc).__name__}: {exc}"

    elapsed_ms = round((datetime.now(UTC) - started).total_seconds() * 1000, 1)
    ok = actual == check.expected_status
    if not ok and not detail:
        detail = f"expected {check.expected_status}, got {actual}"
    return CheckResult(
        path=check.path,
        expected_status=check.expected_status,
        actual_status=actual,
        ok=ok,
        elapsed_ms=elapsed_ms,
        required=check.required,
        detail=detail,
    )


def run(base_url: str, timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    results = [_do_request(base_url, c, timeout) for c in CHECKS]
    passed = sum(1 for r in results if r.ok)
    failed_required = sum(1 for r in results if not r.ok and r.required)
    passed_required = sum(1 for r in results if r.ok and r.required)
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "base_url": base_url,
        "total": len(results),
        "passed": passed,
        "passed_required": passed_required,
        "failed_required": failed_required,
        "results": [r.to_dict() for r in results],
    }


def render_text(report: dict[str, Any]) -> str:
    """Bilingual perimeter table (Arabic primary, English secondary)."""
    lines: list[str] = []
    lines.append("═════════════════════════════════════════════════════════════")
    lines.append(
        " فحص محيط v6 — v6 endpoint perimeter check"
    )
    lines.append(f" القاعدة (base): {report['base_url']}")
    lines.append(f" التاريخ (generated_at): {report['generated_at']}")
    lines.append("═════════════════════════════════════════════════════════════")
    # Header row — Arabic primary, English secondary
    header = (
        f" {'الحالة/Status':<14}"
        f" {'المسار/Path':<48}"
        f" {'متوقع/Exp':>9}"
        f" {'فعلي/Got':>9}"
        f" {'الزمن/ms':>10}"
    )
    lines.append(header)
    lines.append("─" * len(header))
    for r in report["results"]:
        marker = "نجاح PASS" if r["ok"] else ("فشل FAIL" if r["required"] else "تنبيه WARN")
        actual = r["actual_status"] if r["actual_status"] is not None else "—"
        line = (
            f" {marker:<14}"
            f" {r['path']:<48}"
            f" {r['expected_status']:>9}"
            f" {str(actual):>9}"
            f" {r['elapsed_ms']:>10.1f}"
        )
        if not r["ok"] and r["detail"]:
            line += f"  {r['detail']}"
        lines.append(line)
    lines.append("─" * len(header))
    lines.append(
        f" نجح/passed: {report['passed']}/{report['total']}    "
        f"فشل مطلوب/failed_required: {report['failed_required']}"
    )
    if report["failed_required"] == 0:
        lines.append(" الحكم/VERDICT: نجاح — كل الفحوصات المطلوبة عبرت / all required PASS")
    else:
        lines.append(" الحكم/VERDICT: فشل — فحص مطلوب فشل / at least one required FAIL")
    lines.append("═════════════════════════════════════════════════════════════")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="v6 endpoint perimeter check (read-only).",
    )
    p.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="root URL of the deploy (default: %(default)s)",
    )
    p.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help="per-request timeout in seconds (default: %(default)s)",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="emit JSON report instead of the bilingual table",
    )
    args = p.parse_args(argv)

    report = run(args.base_url, timeout=args.timeout)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_text(report))

    # If every probe failed with no HTTP status at all, the base URL
    # is unreachable. Exit 2 so callers can distinguish "deploy down"
    # from "deploy up but a route regressed".
    network_failures = sum(
        1 for r in report["results"] if r["actual_status"] is None
    )
    if network_failures == report["total"]:
        return 2
    return 0 if report["failed_required"] == 0 else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
