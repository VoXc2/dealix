#!/usr/bin/env python3
"""scripts/preflight_check.py

Single-command go/no-go gate before GA. Verifies that every claim in the
runbooks is actually satisfied by the running environment.

Exit codes:
    0   ALL CHECKS PASSED — safe to flip the GA switch
    1   one or more required checks failed
    2   one or more recommended checks failed (still go-able with risk)

Usage:
    BASE_URL=https://api.dealix.me \\
    DATABASE_URL=... \\
    REDIS_URL=... \\
    MOYASAR_SECRET_KEY=sk_live_... \\
        python scripts/preflight_check.py

    # or, against a local dev stack:
    BASE_URL=http://localhost:8000 python scripts/preflight_check.py --dev

Checks (P = required, R = recommended):
    P1  /healthz returns 200
    P2  /api/v1/pricing/plans returns ≥ 4 plans
    P3  Moyasar webhook rejects bad signature with 401
    P4  CORS strict (no Access-Control-Allow-Origin for unlisted origin)
    P5  ADMIN_API_KEYS configured in deployed env (admin endpoint requires it)
    P6  Alembic head == single revision (no branch split)
    P7  DLQ depth ≤ 5 on all queues
    R8  Sentry DSN configured (Sentry is enabled)
    R9  PostHog API key configured (analytics flowing)
    R10 Backup S3 bucket exists + recent object < 2h old
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Result:
    name: str
    status: str  # "pass" | "fail" | "skip"
    severity: str  # "P" required, "R" recommended
    detail: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


def check(name: str, severity: str = "P"):
    def deco(fn: Callable[..., tuple[bool, str, dict | None]]):
        def wrapper(*args, **kwargs) -> Result:
            try:
                ok, detail, extra = fn(*args, **kwargs)
            except SkipCheck as exc:
                return Result(name, "skip", severity, str(exc))
            except Exception as exc:
                return Result(name, "fail", severity, f"unhandled: {exc}")
            return Result(name, "pass" if ok else "fail", severity, detail, extra or {})
        wrapper._check_name = name  # type: ignore
        return wrapper
    return deco


class SkipCheck(Exception):
    pass


# ── P1 ────────────────────────────────────────────────────────

@check("P1 /healthz returns 200", "P")
def check_healthz(base_url: str) -> tuple[bool, str, dict | None]:
    import urllib.request
    try:
        with urllib.request.urlopen(f"{base_url}/healthz", timeout=10) as resp:
            return resp.status == 200, f"got {resp.status}", None
    except Exception as exc:
        return False, str(exc), None


# ── P2 ────────────────────────────────────────────────────────

@check("P2 /api/v1/pricing/plans returns >= 3 plans", "P")
def check_pricing(base_url: str) -> tuple[bool, str, dict | None]:
    import urllib.request
    with urllib.request.urlopen(f"{base_url}/api/v1/pricing/plans", timeout=10) as resp:
        body = json.loads(resp.read())
    n = len(body.get("plans") or [])
    # The public pricing endpoint returns 3 plans (starter/growth/scale);
    # pilot_1sar is intentionally hidden. See api/routers/pricing.py.
    return n >= 3, f"{n} plans returned", {"count": n}


# ── P3 ────────────────────────────────────────────────────────

@check("P3 Moyasar webhook rejects bad signature (401/403)", "P")
def check_webhook_signature(base_url: str) -> tuple[bool, str, dict | None]:
    import urllib.request
    req = urllib.request.Request(
        f"{base_url}/api/v1/webhooks/moyasar",
        data=b'{"id":"preflight","secret_token":"definitely-not-the-real-one"}',
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            code = resp.status
    except urllib.request.HTTPError as exc:
        code = exc.code
    return code in (401, 403), f"got {code}", {"code": code}


# ── P4 ────────────────────────────────────────────────────────

@check("P4 CORS rejects unlisted origin", "P")
def check_cors_strict(base_url: str) -> tuple[bool, str, dict | None]:
    import urllib.request
    req = urllib.request.Request(
        f"{base_url}/api/v1/pricing/plans",
        method="OPTIONS",
        headers={"Origin": "https://evil.example.com",
                 "Access-Control-Request-Method": "GET"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            headers = {k.lower(): v for k, v in resp.headers.items()}
            code = resp.status
    except urllib.request.HTTPError as exc:
        headers = {k.lower(): v for k, v in (exc.headers or {}).items()}
        code = exc.code
    allow = headers.get("access-control-allow-origin")
    # Pass only if no ACAO header at all. Reject if the server echoed the
    # evil origin OR returned a wildcard (which would allow any origin).
    if allow is None:
        ok = True
    elif allow.strip() == "*":
        ok = False
    else:
        ok = "evil.example.com" not in allow
    return ok, f"code={code} acao={allow}", {"code": code, "acao": allow}


# ── P5 — env vars sanity (caller must export them) ───────────

@check("P5 critical env vars present (caller-side)", "P")
def check_env() -> tuple[bool, str, dict | None]:
    # DATABASE_URL + BASE_URL are always required (the API can't boot
    # locally without them either).
    # ADMIN_API_KEYS + MOYASAR_WEBHOOK_SECRET are launch-critical for prod
    # only — the API refuses to boot in production without them, and the
    # webhook signature check fails closed without the latter. In --dev
    # mode (PREFLIGHT_DEV=1, set by main()), they're relaxed so local
    # invocations don't require production secrets.
    required = ["DATABASE_URL", "BASE_URL"]
    if not os.environ.get("PREFLIGHT_DEV"):
        required.extend(["ADMIN_API_KEYS", "MOYASAR_WEBHOOK_SECRET"])
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        return False, f"missing: {', '.join(missing)}", {"missing": missing}
    return True, "all required env vars set", None


# ── P6 — single Alembic head ─────────────────────────────────

@check("P6 single Alembic head", "P")
def check_alembic_head() -> tuple[bool, str, dict | None]:
    versions_dir = os.path.join(os.path.dirname(__file__), "..", "db", "migrations", "versions")
    if not os.path.isdir(versions_dir):
        raise SkipCheck("db/migrations/versions not found")
    files = [f for f in os.listdir(versions_dir) if f.endswith(".py") and not f.startswith("_")]
    # revisions: rev -> list of down_revisions (may be multiple for merges)
    revisions: dict[str, list[str]] = {}
    for f in files:
        path = os.path.join(versions_dir, f)
        with open(path) as fh:
            content = fh.read()
        rev_m = re.search(r'^revision\s*:?\s*[\w\[\], |]*=\s*[\'"]([^\'"]+)[\'"]', content, re.M)
        if not rev_m:
            continue
        rev = rev_m.group(1)
        # down_revision can be: None / "single" / ("a", "b") / ["a", "b"]
        down_m = re.search(r'^down_revision\s*:?\s*[\w\[\], |]*=\s*(.+?)$', content, re.M)
        downs: list[str] = []
        if down_m:
            tail = down_m.group(1).strip()
            if tail != "None":
                # Capture every quoted string in the tail (handles single + tuple + list)
                downs = re.findall(r'[\'"]([^\'"]+)[\'"]', tail)
        revisions[rev] = downs
    # A head is a revision that is not referenced as anyone's parent
    referenced = {d for downs in revisions.values() for d in downs}
    heads = [r for r in revisions if r not in referenced]
    return len(heads) == 1, f"heads={heads}", {"heads": heads, "count": len(heads)}


# ── P7 — DLQ ─────────────────────────────────────────────────

@check("P7 DLQ depth <= 5 on all queues", "P")
def check_dlq() -> tuple[bool, str, dict | None]:
    redis_url = os.environ.get("REDIS_URL")
    if not redis_url:
        raise SkipCheck("REDIS_URL not set")
    try:
        import redis
    except ImportError:
        raise SkipCheck("redis package not installed")
    r = redis.from_url(redis_url, socket_timeout=5, decode_responses=True)
    # Mirror dealix/queues.py — these are all production DLQs. crm_sync
    # was previously missing and could be over-threshold while preflight
    # reported green.
    queues = ["webhooks", "outbound", "enrichment", "crm_sync"]
    depths = {q: int(r.llen(f"dlq:{q}") or 0) for q in queues}
    over = {q: d for q, d in depths.items() if d > 5}
    return not over, json.dumps(depths), depths


# ── R8 — Sentry ──────────────────────────────────────────────

@check("R8 Sentry DSN configured", "R")
def check_sentry() -> tuple[bool, str, dict | None]:
    dsn = os.environ.get("SENTRY_DSN")
    if not dsn:
        return False, "missing SENTRY_DSN env", None
    # Use urlparse + hostname.endswith so attacker-controlled URLs like
    # https://x@evil.com/ingest.sentry.io/1 don't pass a substring check.
    try:
        from urllib.parse import urlparse
        host = (urlparse(dsn).hostname or "").lower()
    except Exception:
        return False, "DSN not parseable", None
    ok = host == "ingest.sentry.io" or host.endswith(".ingest.sentry.io")
    return ok, f"host={host}", {"host": host}


# ── R9 — PostHog ─────────────────────────────────────────────

@check("R9 PostHog API key configured", "R")
def check_posthog() -> tuple[bool, str, dict | None]:
    k = os.environ.get("POSTHOG_API_KEY")
    return bool(k and k.startswith("phc_")), \
           "configured" if k else "missing POSTHOG_API_KEY", None


# ── R10 — Backup freshness ───────────────────────────────────

@check("R10 S3 backup < 2h old", "R")
def check_backup_freshness() -> tuple[bool, str, dict | None]:
    bucket = os.environ.get("BACKUP_S3_BUCKET")
    if not bucket:
        raise SkipCheck("BACKUP_S3_BUCKET not set")
    try:
        import boto3
    except ImportError:
        raise SkipCheck("boto3 not installed")
    prefix = os.environ.get("BACKUP_S3_PREFIX", "dealix/hourly")
    s3 = boto3.client("s3", region_name=os.environ.get("AWS_DEFAULT_REGION", "me-south-1"))
    # Paginate through the entire prefix so we don't miss a newer object
    # buried deeper in the listing. MaxKeys=5 previously could report
    # stale backups for any bucket with > 5 matching objects.
    paginator = s3.get_paginator("list_objects_v2")
    latest = None
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix + "/"):
        for obj in page.get("Contents") or []:
            if latest is None or obj["LastModified"] > latest["LastModified"]:
                latest = obj
    if latest is None:
        return False, "no objects under prefix", {"prefix": prefix}
    age_sec = time.time() - latest["LastModified"].timestamp()
    return age_sec < 2 * 3600, f"latest age={int(age_sec/60)}min", {"age_sec": int(age_sec)}


# ── Driver ────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", action="store_true",
                        help="skip prod-only checks (Sentry/PostHog/S3/Redis) "
                             "and relax env requirements (no ADMIN_API_KEYS / "
                             "MOYASAR_WEBHOOK_SECRET needed locally)")
    parser.add_argument("--json", action="store_true", help="JSON output only")
    args = parser.parse_args()

    # Surface --dev to checks via env so individual @check functions
    # (which take no args by design) can branch on it.
    if args.dev:
        os.environ["PREFLIGHT_DEV"] = "1"

    base_url = os.environ.get("BASE_URL", "http://localhost:8000")

    checks: list[Result] = []
    checks.append(check_env())
    checks.append(check_healthz(base_url))
    checks.append(check_pricing(base_url))
    checks.append(check_webhook_signature(base_url))
    checks.append(check_cors_strict(base_url))
    checks.append(check_alembic_head())

    # Prod-only checks: skip in dev mode where these integrations are
    # expected to be absent (Sentry/PostHog/S3 not configured locally).
    if not args.dev:
        checks.append(check_dlq())
        checks.append(check_sentry())
        checks.append(check_posthog())
        checks.append(check_backup_freshness())

    # A skipped required (P) check is a failure — production runs must
    # never silently bypass a mandatory gate. Recommended (R) checks may
    # legitimately skip (e.g. Sentry not configured in --dev).
    p_fail = [r for r in checks if r.severity == "P" and r.status in ("fail", "skip")]
    r_fail = [r for r in checks if r.severity == "R" and r.status == "fail"]

    # Determine the exit code FIRST so JSON mode honors the same contract.
    if p_fail:
        exit_code = 1
    elif r_fail:
        exit_code = 2
    else:
        exit_code = 0

    if args.json:
        print(json.dumps({
            "checks": [vars(c) for c in checks],
            "p_fail": [c.name for c in p_fail],
            "r_fail": [c.name for c in r_fail],
            "exit_code": exit_code,
        }, indent=2, ensure_ascii=False, default=str))
        return exit_code

    ICON = {"pass": "✓", "fail": "✗", "skip": "–"}
    for c in checks:
        print(f"  [{ICON[c.status]}] {c.name:<50}  {c.detail}")
    print()
    if p_fail:
        print(f"FAIL — {len(p_fail)} required check(s) failed:")
        for c in p_fail:
            print(f"  - {c.name}: {c.detail}")
    elif r_fail:
        print(f"WARN — {len(r_fail)} recommended check(s) failed (proceed at risk):")
        for c in r_fail:
            print(f"  - {c.name}: {c.detail}")
    else:
        print("✓ ALL CHECKS PASSED — safe to flip the GA switch")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
