#!/usr/bin/env python3
"""Smoke-test the public Railway deployment matrix.

The script is dependency-free and safe for GitHub Actions. It verifies that
public health endpoints respond quickly and, when JSON is returned, expose an
`ok`, `ready`, or `alive` status.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections.abc import Iterable
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class Target:
    name: str
    base_url: str
    paths: tuple[str, ...]


def _clean_base_url(value: str) -> str:
    return value.rstrip("/") + "/"


def _request_json(url: str, timeout: float) -> tuple[int, str, dict[str, object] | None, float]:
    started = time.perf_counter()
    req = Request(url, headers={"User-Agent": "dealix-railway-smoke/1.0"})
    try:
        with urlopen(req, timeout=timeout) as response:  # noqa: S310 - operator-supplied URLs
            body = response.read(4096).decode("utf-8", errors="replace")
            elapsed_ms = (time.perf_counter() - started) * 1000
            try:
                parsed = json.loads(body)
            except json.JSONDecodeError:
                parsed = None
            return int(response.status), body, parsed, elapsed_ms
    except HTTPError as exc:
        elapsed_ms = (time.perf_counter() - started) * 1000
        body = exc.read(4096).decode("utf-8", errors="replace")
        return int(exc.code), body, None, elapsed_ms
    except URLError as exc:
        raise RuntimeError(f"network error: {exc.reason}") from exc
    except TimeoutError as exc:
        raise RuntimeError("request timed out") from exc


def _status_ok(parsed: dict[str, object] | None) -> bool:
    if parsed is None:
        return True
    status = str(parsed.get("status", "")).lower()
    return status in {"ok", "ready", "alive", "operational"}


def _iter_targets(args: argparse.Namespace) -> Iterable[Target]:
    api_url = args.api_url or os.getenv("DEALIX_API_URL") or os.getenv("PRODUCTION_BASE_URL")
    frontend_url = args.frontend_url or os.getenv("DEALIX_FRONTEND_URL")
    web_url = args.web_url or os.getenv("DEALIX_WEB_URL")

    if api_url:
        yield Target("api", _clean_base_url(api_url), ("healthz", "ready"))
    if frontend_url:
        yield Target("frontend", _clean_base_url(frontend_url), ("healthz",))
    if web_url:
        yield Target("apps-web", _clean_base_url(web_url), ("healthz",))


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-test Dealix Railway public surfaces")
    parser.add_argument("--api-url", help="API base URL, e.g. https://api.dealix.me")
    parser.add_argument("--frontend-url", help="Frontend base URL, e.g. https://dealix.me")
    parser.add_argument("--web-url", help="Apps web base URL, if deployed separately")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    targets = list(_iter_targets(args))
    if not targets:
        print("RAILWAY_SMOKE_SKIP no targets configured")
        return 0

    failures: list[str] = []
    for target in targets:
        for path in target.paths:
            url = urljoin(target.base_url, path)
            try:
                code, body, parsed, elapsed_ms = _request_json(url, timeout=args.timeout)
            except RuntimeError as exc:
                failures.append(f"{target.name}:{path} {exc}")
                print(f"RAILWAY_SMOKE_FAIL {target.name} {url} error={exc}")
                continue

            if code >= 400 or not _status_ok(parsed):
                failures.append(f"{target.name}:{path} status={code} body={body[:200]!r}")
                print(f"RAILWAY_SMOKE_FAIL {target.name} {url} status={code} ms={elapsed_ms:.1f}")
                continue

            print(f"RAILWAY_SMOKE_OK {target.name} {url} status={code} ms={elapsed_ms:.1f}")

    if failures:
        print("RAILWAY_SMOKE_SUMMARY_FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("RAILWAY_SMOKE_SUMMARY_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
