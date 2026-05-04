#!/usr/bin/env python3
"""
Staging Smoke Test — verifies a deployed Dealix URL is launch-ready.

Hits 12 critical endpoints over real HTTP:
  GET  /healthz                                    → 200
  GET  /health/deep                                → 200 (subsystems healthy)
  GET  /api/v1/services/catalog                    → 200 + 6 bundles
  GET  /api/v1/cards/feed?role=ceo                 → 200 + cards
  GET  /api/v1/role-briefs/daily?role=sales_manager → 200
  GET  /api/v1/proof-ledger/units                  → 200 + RWU catalog
  GET  /api/v1/observability/quality?days=7        → 200 + KPIs
  GET  /api/v1/observability/unsafe/summary        → 200 + invariant true
  GET  /api/v1/daily-ops/windows                   → 200 + 4 windows
  GET  /api/v1/auth/me                             → 401 (no cookie)
  POST /api/v1/auth/magic-link/send                → 200 + sent=true (anti-enum)
  POST /api/v1/calls/dial-live                     → 403 (gate off)
  POST /api/v1/whatsapp/brief/send-internal        → 403 (gate off)

Usage:
    export STAGING_BASE_URL=https://api.dealix.me   # or app URL
    python scripts/staging_smoke.py --base-url $STAGING_BASE_URL
    python scripts/staging_smoke.py --base-url $STAGING_BASE_URL --json

Exit code 0 on STAGING_SMOKE_PASS, 1 on FAIL.

Importable as `from scripts.staging_smoke import run_smoke`.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from typing import Any

try:
    import httpx  # type: ignore
except ImportError:  # pragma: no cover
    print("staging_smoke requires httpx. install with: pip install httpx", file=sys.stderr)
    raise


# ── Probe definitions ────────────────────────────────────────────


@dataclass
class Probe:
    name: str
    method: str
    path: str
    expected_status: int
    extra_check: str | None = None  # human-readable hint
    body: dict[str, Any] | None = None


PROBES: tuple[Probe, ...] = (
    Probe("healthz",                   "GET",  "/healthz", 200),
    Probe("health_deep",               "GET",  "/health/deep", 200),
    Probe("services_catalog",          "GET",  "/api/v1/services/catalog", 200,
          "expects bundles>=6"),
    Probe("cards_feed_ceo",            "GET",  "/api/v1/cards/feed?role=ceo", 200,
          "expects is_demo present"),
    Probe("role_briefs_daily_sales",   "GET",  "/api/v1/role-briefs/daily?role=sales_manager", 200),
    Probe("proof_ledger_units",        "GET",  "/api/v1/proof-ledger/units", 200,
          "expects rwu count>=10"),
    Probe("observability_quality",     "GET",  "/api/v1/observability/quality?days=7", 200),
    Probe("observability_unsafe_sum",  "GET",  "/api/v1/observability/unsafe/summary?days=7", 200,
          "expects no_unsafe_action_executed=true"),
    Probe("daily_ops_windows",         "GET",  "/api/v1/daily-ops/windows", 200,
          "expects 4 windows"),
    Probe("auth_me_unauthed",          "GET",  "/api/v1/auth/me", 401,
          "must reject without cookie"),
    Probe("auth_magic_link_send",      "POST", "/api/v1/auth/magic-link/send", 200,
          "anti-enumeration: always sent=true",
          body={"email": "smoke-probe@example.invalid"}),
    Probe("calls_dial_live_gated",     "POST", "/api/v1/calls/dial-live", 403,
          "live-call gate must be off",
          body={"to": "+966500000000"}),
    Probe("whatsapp_send_internal_gated", "POST", "/api/v1/whatsapp/brief/send-internal", 403,
          "internal whatsapp gate must be off",
          body={"role": "ceo"}),
)


@dataclass
class ProbeResult:
    name: str
    passed: bool
    status_code: int | None
    detail: str = ""
    duration_ms: int = 0


@dataclass
class SmokeReport:
    base_url: str
    results: list[ProbeResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results)

    @property
    def fail_count(self) -> int:
        return sum(1 for r in self.results if not r.passed)


# ── Body validators (light — just sanity, not exhaustive) ────────


def _validate_body(probe: Probe, body: Any) -> str:
    """Return empty string if body looks right, else a short message."""
    try:
        if probe.name == "services_catalog":
            n = len((body or {}).get("bundles") or [])
            if n < 6:
                return f"expected ≥6 bundles, got {n}"
        elif probe.name == "cards_feed_ceo":
            if "is_demo" not in (body or {}):
                return "missing is_demo"
        elif probe.name == "proof_ledger_units":
            n = len((body or {}).get("units") or [])
            if n < 10:
                return f"expected ≥10 RWUs, got {n}"
        elif probe.name == "observability_unsafe_sum":
            if (body or {}).get("no_unsafe_action_executed") is not True:
                return "invariant no_unsafe_action_executed != true"
        elif probe.name == "daily_ops_windows":
            n = (body or {}).get("count") or 0
            if n != 4:
                return f"expected 4 windows, got {n}"
        elif probe.name == "auth_magic_link_send":
            if (body or {}).get("sent") is not True:
                return "expected sent=true (anti-enumeration)"
    except Exception as exc:  # noqa: BLE001
        return f"body parse: {exc}"
    return ""


# ── Runner ───────────────────────────────────────────────────────


def run_smoke(base_url: str, *, timeout: float = 15.0) -> SmokeReport:
    base = base_url.rstrip("/")
    rep = SmokeReport(base_url=base)
    with httpx.Client(timeout=timeout, follow_redirects=False) as client:
        for probe in PROBES:
            url = base + probe.path
            try:
                if probe.method == "GET":
                    r = client.get(url)
                else:
                    r = client.post(url, json=probe.body or {})
                duration = int(r.elapsed.total_seconds() * 1000)
                status = r.status_code
                if status != probe.expected_status:
                    rep.results.append(ProbeResult(
                        probe.name, False, status,
                        f"expected {probe.expected_status}, got {status}",
                        duration,
                    ))
                    continue
                # Body validation only when status OK
                body_msg = ""
                if status == 200 and r.headers.get("content-type", "").startswith("application/json"):
                    try:
                        body_msg = _validate_body(probe, r.json())
                    except Exception as exc:  # noqa: BLE001
                        body_msg = f"json: {exc}"
                if body_msg:
                    rep.results.append(ProbeResult(probe.name, False, status, body_msg, duration))
                else:
                    detail = probe.extra_check or "ok"
                    rep.results.append(ProbeResult(probe.name, True, status, detail, duration))
            except Exception as exc:  # noqa: BLE001
                rep.results.append(ProbeResult(probe.name, False, None, f"error: {exc}", 0))
    return rep


def render(report: SmokeReport, *, as_json: bool = False) -> str:
    if as_json:
        return json.dumps({
            "base_url": report.base_url,
            "passed": report.passed,
            "fail_count": report.fail_count,
            "results": [
                {
                    "name": r.name, "passed": r.passed,
                    "status": r.status_code, "duration_ms": r.duration_ms,
                    "detail": r.detail,
                } for r in report.results
            ],
        }, indent=2)
    lines = [f"DEALIX_STAGING_SMOKE v1.0  →  {report.base_url}", "=" * 60]
    for r in report.results:
        flag = "OK  " if r.passed else "FAIL"
        s = str(r.status_code) if r.status_code is not None else "—"
        lines.append(f"[{flag}] {r.name:32s}  {s:4s}  {r.duration_ms:5d}ms  {r.detail}")
    lines.append("=" * 60)
    lines.append(f"RESULT: {'STAGING_SMOKE_PASS' if report.passed else 'STAGING_SMOKE_FAIL'}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Smoke-test a deployed Dealix URL")
    parser.add_argument("--base-url", required=True, help="e.g. https://api.dealix.me")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of human-readable text")
    parser.add_argument("--timeout", type=float, default=15.0)
    args = parser.parse_args(argv)
    report = run_smoke(args.base_url, timeout=args.timeout)
    print(render(report, as_json=args.json))
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
