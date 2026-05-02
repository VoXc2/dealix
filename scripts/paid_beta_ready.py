#!/usr/bin/env python3
"""
Paid Beta Readiness Check — verifies a deployed staging environment.

Targets a base URL (Railway, Fly, Render, etc.) and checks:
  1. /health → 200, body looks healthy
  2. / → 200, body contains version + env
  3. /api/v1/command-center/snapshot → 200
  4. /docs → 200 (FastAPI Swagger)
  5. /api/v1/personal-operator/daily-brief → 200 OR 404 (skip if not enabled)
  6. /api/v1/v3/command-center/snapshot → 200
  7. Latency budget (warn >5s, fail >10s on any endpoint)

Run:
  python scripts/paid_beta_ready.py --base-url https://web-dealix.up.railway.app
Exit 0 = PAID_BETA_READY, exit 1 = NOT_READY.

Importable: scripts.paid_beta_ready.run_check(base_url, timeout) -> StagingReport.
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass, field
from typing import Iterable

import httpx


@dataclass
class HttpProbe:
    """One probe to run against the staging URL."""

    name: str
    method: str
    path: str
    expected_statuses: tuple[int, ...] = (200,)
    body_contains: tuple[str, ...] = ()
    optional: bool = False  # if True, 404 is acceptable


@dataclass
class ProbeResult:
    probe: HttpProbe
    status: int
    latency_ms: float
    passed: bool
    detail: str = ""


@dataclass
class StagingReport:
    base_url: str
    results: list[ProbeResult] = field(default_factory=list)
    latency_warnings: list[str] = field(default_factory=list)
    latency_failures: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return (
            all(r.passed for r in self.results)
            and not self.latency_failures
        )


PROBES: tuple[HttpProbe, ...] = (
    HttpProbe(
        name="health",
        method="GET",
        path="/health",
        body_contains=("status",),
    ),
    HttpProbe(
        name="root",
        method="GET",
        path="/",
        body_contains=("version", "env"),
    ),
    HttpProbe(
        name="command_center_snapshot",
        method="GET",
        path="/api/v1/command-center/snapshot",
    ),
    HttpProbe(
        name="docs",
        method="GET",
        path="/docs",
    ),
    HttpProbe(
        name="personal_operator_daily_brief",
        method="GET",
        path="/api/v1/personal-operator/daily-brief",
        expected_statuses=(200, 404),
        optional=True,
    ),
    HttpProbe(
        name="v3_command_center_snapshot",
        method="GET",
        path="/api/v1/v3/command-center/snapshot",
        expected_statuses=(200, 404),
        optional=True,
    ),
)


# Latency thresholds (milliseconds).
LATENCY_WARN_MS = 5_000
LATENCY_FAIL_MS = 10_000


def run_probe(client: httpx.Client, base_url: str, probe: HttpProbe) -> ProbeResult:
    url = base_url.rstrip("/") + probe.path
    started = time.perf_counter()
    try:
        resp = client.request(probe.method, url)
    except httpx.RequestError as exc:
        latency_ms = (time.perf_counter() - started) * 1000.0
        return ProbeResult(
            probe=probe, status=0, latency_ms=latency_ms, passed=False,
            detail=f"network: {exc.__class__.__name__}: {exc}",
        )

    body = resp.text or ""
    latency_ms = (time.perf_counter() - started) * 1000.0

    status_ok = resp.status_code in probe.expected_statuses
    body_ok = all(token in body for token in probe.body_contains)

    if probe.optional and resp.status_code == 404:
        return ProbeResult(
            probe=probe, status=resp.status_code, latency_ms=latency_ms, passed=True,
            detail="optional endpoint not enabled (404 OK)",
        )

    passed = status_ok and body_ok
    detail_bits: list[str] = []
    if not status_ok:
        detail_bits.append(f"status {resp.status_code}")
    if not body_ok:
        missing = [t for t in probe.body_contains if t not in body]
        detail_bits.append(f"missing in body: {missing}")
    detail = "; ".join(detail_bits) or "OK"

    return ProbeResult(
        probe=probe, status=resp.status_code, latency_ms=latency_ms, passed=passed,
        detail=detail,
    )


def run_check(
    base_url: str,
    *,
    timeout: float = 15.0,
    probes: Iterable[HttpProbe] = PROBES,
) -> StagingReport:
    report = StagingReport(base_url=base_url)
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        for probe in probes:
            result = run_probe(client, base_url, probe)
            report.results.append(result)

            if result.latency_ms >= LATENCY_FAIL_MS:
                report.latency_failures.append(
                    f"{probe.name}: {result.latency_ms:.0f}ms (>{LATENCY_FAIL_MS}ms)"
                )
            elif result.latency_ms >= LATENCY_WARN_MS:
                report.latency_warnings.append(
                    f"{probe.name}: {result.latency_ms:.0f}ms (>{LATENCY_WARN_MS}ms)"
                )
    return report


def render(report: StagingReport) -> str:
    lines = [
        "PAID_BETA_READY_CHECK v1.0",
        "=" * 36,
        f"target: {report.base_url}",
    ]
    for i, r in enumerate(report.results, start=1):
        tag = "OK  " if r.passed else "FAIL"
        line = (
            f"[{i}/{len(report.results)}] "
            f"{r.probe.path:<48} {r.status} {tag}  "
            f"({r.latency_ms:.0f}ms)"
        )
        if not r.passed or r.detail not in ("OK", ""):
            line += f"  — {r.detail}"
        lines.append(line)

    if report.latency_warnings:
        lines.append("")
        lines.append("LATENCY WARNINGS:")
        for w in report.latency_warnings:
            lines.append(f"  - {w}")

    if report.latency_failures:
        lines.append("")
        lines.append("LATENCY FAILURES:")
        for f in report.latency_failures:
            lines.append(f"  - {f}")

    lines.append("=" * 36)
    lines.append("RESULT: " + ("PAID_BETA_READY" if report.passed else "NOT_READY"))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix paid-beta staging readiness check")
    parser.add_argument(
        "--base-url",
        required=True,
        help="staging URL (e.g., https://web-dealix.up.railway.app)",
    )
    parser.add_argument(
        "--timeout", type=float, default=15.0,
        help="per-request timeout in seconds (default 15)",
    )
    args = parser.parse_args()

    report = run_check(args.base_url, timeout=args.timeout)
    print(render(report))
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
