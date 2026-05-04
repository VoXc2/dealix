#!/usr/bin/env python3
"""Cross-platform smoke test for a Dealix deploy.

Equivalent to ``scripts/post_redeploy_verify.sh`` but written in
Python so it runs identically on Linux, macOS, and Windows. Hits
every public read-only endpoint added by the v5 + Phase H work and
asserts the safety perimeter is intact.

Usage:
    python scripts/dealix_smoke_test.py
    python scripts/dealix_smoke_test.py --base-url https://staging.dealix.me
    python scripts/dealix_smoke_test.py --json   # machine-readable

Exit codes:
    0  all required checks passed
    1  one or more required checks failed
    2  unable to reach the deploy at all (network / config issue)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


DEFAULT_BASE_URL = os.getenv("DEALIX_BASE_URL", "https://api.dealix.me")
DEFAULT_TIMEOUT = float(os.getenv("DEALIX_SMOKE_TIMEOUT", "15"))


@dataclass
class Check:
    name: str
    method: str
    path: str
    required: bool = True
    expect_status: int = 200
    expect_in_body: list[str] = field(default_factory=list)
    expect_not_in_body: list[str] = field(default_factory=list)


@dataclass
class CheckResult:
    name: str
    method: str
    path: str
    required: bool
    status: int | None
    elapsed_ms: float
    ok: bool
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# Every required check below corresponds to a real endpoint shipped
# in this branch. Body assertions are intentionally minimal — we
# verify the endpoint is reachable + carries the expected guardrails,
# never that the data matches a specific value (which would couple
# this script to data that legitimately changes day-to-day).
CHECKS: list[Check] = [
    # Liveness
    Check(
        name="health",
        method="GET",
        path="/health",
        expect_in_body=["status", "git_sha"],
    ),
    # Self-Growth OS perimeter
    Check(
        name="self_growth_status",
        method="GET",
        path="/api/v1/self-growth/status",
        expect_in_body=["no_live_send"],
    ),
    Check(
        name="service_activation",
        method="GET",
        path="/api/v1/self-growth/service-activation",
        expect_in_body=["counts", "total"],
    ),
    Check(
        name="seo_audit",
        method="GET",
        path="/api/v1/self-growth/seo/audit",
        expect_in_body=["pages_with_required_gap"],
    ),
    Check(
        name="weekly_scorecard",
        method="GET",
        path="/api/v1/self-growth/scorecard/weekly",
    ),
    # v5 layer 1 — Customer Loop
    Check(name="customer_loop_status", method="GET",
          path="/api/v1/customer-loop/status",
          expect_in_body=["no_live_send"]),
    Check(name="customer_loop_states", method="GET",
          path="/api/v1/customer-loop/states"),
    # v5 layer 2 — Role Command OS
    Check(name="role_command_status", method="GET",
          path="/api/v1/role-command/status",
          expect_in_body=["no_live_send"]),
    Check(name="role_command_ceo", method="GET",
          path="/api/v1/role-command/ceo"),
    # v5 layer 3 — Service Quality
    Check(name="service_quality_status", method="GET",
          path="/api/v1/service-quality/status"),
    Check(name="service_quality_sla", method="GET",
          path="/api/v1/service-quality/sla"),
    # v5 layer 4 — Agent Governance
    Check(name="agent_governance_status", method="GET",
          path="/api/v1/agent-governance/status"),
    Check(name="agent_governance_agents", method="GET",
          path="/api/v1/agent-governance/agents"),
    # v5 layer 5 — Reliability OS
    Check(name="reliability_status", method="GET",
          path="/api/v1/reliability/status"),
    Check(name="reliability_health_matrix", method="GET",
          path="/api/v1/reliability/health-matrix",
          expect_in_body=["overall_status", "subsystems"]),
    # v5 layer 6 — Vertical Playbooks
    Check(name="vertical_playbooks_status", method="GET",
          path="/api/v1/vertical-playbooks/status"),
    Check(name="vertical_playbooks_list", method="GET",
          path="/api/v1/vertical-playbooks/list"),
    # v5 layer 7 — Customer Data Plane
    Check(name="customer_data_status", method="GET",
          path="/api/v1/customer-data/status"),
    # v5 layer 8 — Finance OS
    Check(name="finance_status", method="GET",
          path="/api/v1/finance/status"),
    Check(name="finance_pricing", method="GET",
          path="/api/v1/finance/pricing"),
    # v5 layer 9 — Delivery Factory
    Check(name="delivery_factory_status", method="GET",
          path="/api/v1/delivery-factory/status"),
    Check(name="delivery_factory_services", method="GET",
          path="/api/v1/delivery-factory/services"),
    # v5 layer 10 — Proof Ledger
    Check(name="proof_ledger_status", method="GET",
          path="/api/v1/proof-ledger/status"),
    # v5 layer 11 — GTM OS
    Check(name="gtm_status", method="GET",
          path="/api/v1/gtm/status"),
    Check(name="gtm_content_calendar", method="GET",
          path="/api/v1/gtm/content-calendar"),
    # v5 layer 12 — Security & Privacy
    Check(name="security_privacy_status", method="GET",
          path="/api/v1/security-privacy/status"),
    Check(name="security_privacy_minimization", method="GET",
          path="/api/v1/security-privacy/data-minimization"),
    # Phase I — founder aggregate dashboard
    Check(name="founder_dashboard", method="GET",
          path="/api/v1/founder/dashboard",
          expect_in_body=["live_gates", "title_ar", "title_en"],
          # Hard rule: dashboard must NEVER report ALLOWED on a
          # clean production deploy. If it does, that's a security
          # incident — fail loud.
          expect_not_in_body=['"ALLOWED"']),
]


def _do_request(base_url: str, check: Check, timeout: float) -> CheckResult:
    url = f"{base_url.rstrip('/')}{check.path}"
    started = datetime.now(UTC)
    try:
        req = urllib.request.Request(url, method=check.method)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            status = resp.status
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            pass
        status = exc.code
    except (urllib.error.URLError, TimeoutError) as exc:
        elapsed = (datetime.now(UTC) - started).total_seconds() * 1000
        return CheckResult(
            name=check.name,
            method=check.method,
            path=check.path,
            required=check.required,
            status=None,
            elapsed_ms=round(elapsed, 1),
            ok=False,
            detail=f"network: {type(exc).__name__}: {exc}",
        )

    elapsed = (datetime.now(UTC) - started).total_seconds() * 1000

    if status != check.expect_status:
        return CheckResult(
            name=check.name,
            method=check.method,
            path=check.path,
            required=check.required,
            status=status,
            elapsed_ms=round(elapsed, 1),
            ok=False,
            detail=f"expected status {check.expect_status}, got {status}",
        )

    for needle in check.expect_in_body:
        if needle not in body:
            return CheckResult(
                name=check.name,
                method=check.method,
                path=check.path,
                required=check.required,
                status=status,
                elapsed_ms=round(elapsed, 1),
                ok=False,
                detail=f"missing expected substring {needle!r}",
            )

    for forbidden in check.expect_not_in_body:
        if forbidden in body:
            return CheckResult(
                name=check.name,
                method=check.method,
                path=check.path,
                required=check.required,
                status=status,
                elapsed_ms=round(elapsed, 1),
                ok=False,
                detail=f"forbidden substring present: {forbidden!r}",
            )

    return CheckResult(
        name=check.name,
        method=check.method,
        path=check.path,
        required=check.required,
        status=status,
        elapsed_ms=round(elapsed, 1),
        ok=True,
    )


def run(base_url: str, timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    results = [_do_request(base_url, c, timeout) for c in CHECKS]
    passed = sum(1 for r in results if r.ok)
    failed_required = [r for r in results if not r.ok and r.required]
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "base_url": base_url,
        "total": len(results),
        "passed": passed,
        "failed_required": len(failed_required),
        "results": [r.to_dict() for r in results],
    }


def render_text(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("═════════════════════════════════════════════════════════════")
    lines.append(f" Dealix smoke test — {report['base_url']}")
    lines.append(f" generated_at: {report['generated_at']}")
    lines.append("═════════════════════════════════════════════════════════════")
    for r in report["results"]:
        marker = "✅" if r["ok"] else ("❌" if r["required"] else "⚠️ ")
        status = r["status"] if r["status"] is not None else "—"
        line = f"{marker} {r['name']:<32} {r['method']} {r['path']:<48} {status:>4}  {r['elapsed_ms']:>7.1f} ms"
        if not r["ok"]:
            line += f"  {r['detail']}"
        lines.append(line)
    lines.append("─────────────────────────────────────────────────────────────")
    lines.append(
        f" passed: {report['passed']}/{report['total']}    "
        f"failed_required: {report['failed_required']}"
    )
    if report["failed_required"] == 0:
        lines.append(" VERDICT: ✅ all required checks passed")
    else:
        lines.append(" VERDICT: ❌ at least one required check failed")
    lines.append("═════════════════════════════════════════════════════════════")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Dealix cross-platform smoke test.")
    p.add_argument("--base-url", default=DEFAULT_BASE_URL,
                   help="root URL of the deploy (default: %(default)s)")
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                   help="per-request timeout in seconds (default: %(default)s)")
    p.add_argument("--json", action="store_true",
                   help="emit JSON report instead of the text dashboard")
    args = p.parse_args(argv)

    report = run(args.base_url, timeout=args.timeout)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_text(report))

    # If we couldn't reach the deploy at all (every request failed
    # with a network error), exit 2.
    network_failures = sum(
        1 for r in report["results"] if r["status"] is None
    )
    if network_failures == report["total"]:
        return 2
    return 0 if report["failed_required"] == 0 else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
