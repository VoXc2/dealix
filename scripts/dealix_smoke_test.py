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
import re
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any

DEFAULT_BASE_URL = os.getenv("DEALIX_BASE_URL", "https://api.dealix.me")
DEFAULT_TIMEOUT = float(os.getenv("DEALIX_SMOKE_TIMEOUT", "15"))


@dataclass(frozen=True)
class APIKeyCandidate:
    value: str
    source: str


def _split_api_key_bundle(raw: str) -> list[str]:
    """Parse comma/newline/semicolon/JSON API key bundles without logging values."""
    raw = raw.strip()
    if not raw:
        return []

    if raw.startswith("["):
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, list):
            return [str(item).strip() for item in parsed if str(item).strip()]

    if raw.startswith("{"):
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, dict):
            likely_values = []
            for key in ("API_KEYS", "api_keys", "keys", "values", "value"):
                value = parsed.get(key)
                if isinstance(value, list):
                    likely_values.extend(str(item).strip() for item in value)
                elif isinstance(value, str):
                    likely_values.extend(_split_api_key_bundle(value))
            return [value for value in likely_values if value]

    return [part.strip() for part in re.split(r"[,;\n\r\t ]+", raw) if part.strip()]


def _first_configured_api_key() -> APIKeyCandidate:
    """Return the first configured smoke/API key without logging it.

    Production protects most /api/* endpoints with X-API-Key. The smoke test
    supports a dedicated smoke key, common production-key aliases, and the
    existing API_KEYS secret shape used by the app. Values are intentionally
    never rendered in reports or logs.
    """
    single_key_envs = (
        "DEALIX_SMOKE_API_KEY",
        "DEALIX_PRODUCTION_API_KEY",
        "DEALIX_READ_API_KEY",
        "DEALIX_API_KEY",
        "API_KEY",
    )
    for env_name in single_key_envs:
        value = os.getenv(env_name, "").strip()
        if value:
            return APIKeyCandidate(value=value, source=env_name)

    for env_name in ("API_KEYS", "DEALIX_API_KEYS"):
        for value in _split_api_key_bundle(os.getenv(env_name, "")):
            return APIKeyCandidate(value=value, source=env_name)

    return APIKeyCandidate(value="", source="")


DEFAULT_API_KEY_CANDIDATE = _first_configured_api_key()
DEFAULT_API_KEY = DEFAULT_API_KEY_CANDIDATE.value
DEFAULT_API_KEY_SOURCE = DEFAULT_API_KEY_CANDIDATE.source


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


def _do_request(
    base_url: str,
    check: Check,
    timeout: float,
    api_key: str = "",
) -> CheckResult:
    url = f"{base_url.rstrip('/')}{check.path}"
    started = datetime.now(UTC)
    try:
        headers: dict[str, str] = {}
        if api_key:
            headers["X-API-Key"] = api_key
        req = urllib.request.Request(url, method=check.method, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            status = resp.status
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:
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


def _infer_auth_problem(results: list[CheckResult], api_key: str) -> str:
    protected_results = [r for r in results if r.path.startswith("/api/")]
    if not protected_results:
        return ""
    protected_401 = [r for r in protected_results if r.status == 401]
    if len(protected_401) == len(protected_results):
        if not api_key:
            return "missing_smoke_api_key_secret"
        return "configured_smoke_api_key_rejected"
    return ""


def run(
    base_url: str,
    timeout: float = DEFAULT_TIMEOUT,
    api_key: str = "",
    api_key_source: str = "",
) -> dict[str, Any]:
    results = [_do_request(base_url, c, timeout, api_key=api_key) for c in CHECKS]
    passed = sum(1 for r in results if r.ok)
    failed_required = [r for r in results if not r.ok and r.required]
    auth_problem = _infer_auth_problem(results, api_key)
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "base_url": base_url,
        "total": len(results),
        "passed": passed,
        "failed_required": len(failed_required),
        "auth_header_configured": bool(api_key),
        "auth_key_source": api_key_source if api_key else "",
        "auth_problem": auth_problem,
        "results": [r.to_dict() for r in results],
    }


def render_text(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("═════════════════════════════════════════════════════════════")
    lines.append(f" Dealix smoke test — {report['base_url']}")
    lines.append(f" generated_at: {report['generated_at']}")
    lines.append(f" auth_header_configured: {report.get('auth_header_configured', False)}")
    if report.get("auth_key_source"):
        lines.append(f" auth_key_source: {report['auth_key_source']}")
    if report.get("auth_problem"):
        lines.append(f" auth_problem: {report['auth_problem']}")
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
    p.add_argument("--api-key", default=DEFAULT_API_KEY,
                   help="API key for protected /api/* smoke checks. Defaults to env.")
    p.add_argument("--json", action="store_true",
                   help="emit JSON report instead of the text dashboard")
    args = p.parse_args(argv)

    explicit_api_key = bool(args.api_key and args.api_key != DEFAULT_API_KEY)
    api_key_source = "--api-key" if explicit_api_key else DEFAULT_API_KEY_SOURCE
    report = run(
        args.base_url,
        timeout=args.timeout,
        api_key=args.api_key,
        api_key_source=api_key_source,
    )

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
