#!/usr/bin/env python3
"""Audit frontend ↔ backend wiring drift.

Per Track B6 of the 30-day plan, this script:

1. Walks `api/routers/` to enumerate every public endpoint (METHOD, path).
2. Walks `landing/**/*.html`, `landing/assets/js/*.js`, and
   `frontend/src/**/*.{ts,tsx,js,jsx}` to find every `/api/v1/...` reference
   (calls + documentation strings).
3. Reports:
   - Orphan endpoints — declared in code, never referenced from frontend
   - Phantom references — frontend mentions an endpoint that doesn't exist
   - Healthy pairs — backend declares + frontend uses

Exits 0 if everything is healthy or has known allowlist entries.
Exits 1 if a phantom reference is found (frontend lies > orphan code).

Usage:
    python scripts/audit_orphan_endpoints.py [--quiet] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parents[1]
ROUTERS_DIR = REPO / "api" / "routers"
LANDING_DIR = REPO / "landing"
FRONTEND_SRC_DIR = REPO / "frontend" / "src"

# These patterns extract endpoint declarations from FastAPI routers.
ROUTER_DECORATOR = re.compile(
    r"""@router\.(get|post|put|patch|delete|options|head)\(\s*["']([^"']+)["']""",
    re.IGNORECASE,
)
PREFIX_PATTERN = re.compile(
    r"""router\s*=\s*APIRouter\([^)]*prefix\s*=\s*["']([^"']+)["']""",
)

# Anything matching this in a landing file is treated as a frontend
# reference to a backend endpoint.
FRONTEND_API_REF = re.compile(r"""['"`](/api/v1/[a-zA-Z0-9_\-/{}]+)['"`]""")

# Endpoints that are SUPPOSED to be backend-only (webhooks, internal jobs,
# admin-only). Listing them here suppresses the "orphan" warning.
ORPHAN_ALLOWLIST: set[str] = {
    # Webhook receivers — called by external services, never by our frontend
    "/api/v1/webhooks/calendly",
    "/api/v1/webhooks/moyasar",
    "/api/v1/webhooks/whatsapp",
    "/api/v1/webhooks/github",
    "/api/v1/webhooks/resend",
    # Internal admin / debug only
    "/api/v1/admin/health",
    "/api/v1/admin/diagnostics",
    "/api/v1/jobs/status",
    "/api/v1/jobs/run",
    # Auth refresh / impersonation — not yet wired to a frontend page
    "/api/v1/auth/revoke",
    # Background-job triggers (cron-only)
    "/api/v1/automation/run",
    "/api/v1/automation/schedule",
    # Embedding generation (job-only)
    "/api/v1/embeddings/generate",
    "/api/v1/embeddings/search",
}


def walk_routers() -> dict[str, set[str]]:
    """Return {endpoint_path: {METHOD,...}} for every declared route."""
    endpoints: dict[str, set[str]] = {}
    for path in ROUTERS_DIR.rglob("*.py"):
        if path.name == "__init__.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        prefix_match = PREFIX_PATTERN.search(text)
        prefix = prefix_match.group(1) if prefix_match else ""
        for verb_match in ROUTER_DECORATOR.finditer(text):
            verb = verb_match.group(1).upper()
            sub_path = verb_match.group(2)
            if not sub_path.startswith("/"):
                sub_path = "/" + sub_path
            full = prefix.rstrip("/") + sub_path
            # Routers mounted in api/main.py with an extra ``/api/v1`` prefix
            # (e.g. auth.router, jobs.router) declare ``/auth/...`` locally.
            if path.name in {"auth.py", "jobs.py"} and not full.startswith("/api/"):
                full = "/api/v1" + full
            if not full.startswith("/api/"):
                # Routes that don't live under /api are not in our wiring
                # contract (e.g. /healthz, /metrics).
                continue
            endpoints.setdefault(full, set()).add(verb)
    return endpoints


def _merge_ref_dicts(
    a: dict[str, set[str]], b: dict[str, set[str]]
) -> dict[str, set[str]]:
    out = {k: set(v) for k, v in a.items()}
    for k, files in b.items():
        out.setdefault(k, set()).update(files)
    return out


def walk_landing() -> dict[str, set[str]]:
    """Return {endpoint_path: {file_paths_referencing_it}}."""
    refs: dict[str, set[str]] = {}
    if not LANDING_DIR.exists():
        return refs
    for path in LANDING_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in {".html", ".js"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in FRONTEND_API_REF.finditer(text):
            ref = match.group(1)
            # Strip path params before matching against router declarations
            normalized = re.sub(r"\{[^}]+\}", "{x}", ref)
            refs.setdefault(normalized, set()).add(
                path.relative_to(REPO).as_posix()
            )
    return refs


def walk_frontend_src() -> dict[str, set[str]]:
    """Collect /api/v1/... string references from the Next.js app."""
    refs: dict[str, set[str]] = {}
    if not FRONTEND_SRC_DIR.exists():
        return refs
    for path in FRONTEND_SRC_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in {".ts", ".tsx", ".js", ".jsx"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in FRONTEND_API_REF.finditer(text):
            ref = match.group(1)
            normalized = re.sub(r"\{[^}]+\}", "{x}", ref)
            refs.setdefault(normalized, set()).add(
                path.relative_to(REPO).as_posix()
            )
    return refs


def normalize_path(p: str) -> str:
    """Replace {handle}, {id}, {service_id} etc. with a generic {x} so that
    a frontend ref to /customer-portal/Slot-A matches a router decl of
    /customer-portal/{handle}."""
    return re.sub(r"\{[^}]+\}", "{x}", p)


def _path_matches_dynamic(ref: str, pattern: str) -> bool:
    """True if ref matches pattern where pattern may include ``{param}`` segments."""
    r_parts = [p for p in ref.strip("/").split("/") if p]
    p_parts = [p for p in pattern.strip("/").split("/") if p]
    if len(r_parts) != len(p_parts):
        return False
    for rp, pp in zip(r_parts, p_parts):
        if pp.startswith("{") and pp.endswith("}"):
            continue
        if rp != pp:
            return False
    return True


def matches_any(ref: str, declared: Iterable[str]) -> bool:
    norm_ref = normalize_path(ref)
    for endpoint in declared:
        if _path_matches_dynamic(ref, endpoint):
            return True
        norm_endpoint = normalize_path(endpoint)
        if norm_endpoint == norm_ref:
            return True
        # Accept prefix matches when the frontend concatenates path
        # fragments at runtime (e.g. `apiBase + "/api/v1/payment-ops/"
        # + invoiceId + "/state"` — the literal string in the source is
        # `/api/v1/payment-ops/` which is a prefix of `/api/v1/payment-ops/{id}/state`).
        if norm_ref.endswith("/") and norm_endpoint.startswith(norm_ref):
            return True
        # Accept when ref is a parent of declared (no trailing slash)
        if norm_endpoint.startswith(norm_ref + "/"):
            return True
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="suppress per-line output")
    parser.add_argument("--json", action="store_true", help="emit JSON to stdout")
    args = parser.parse_args(argv)

    endpoints = walk_routers()
    refs = _merge_ref_dicts(walk_landing(), walk_frontend_src())

    # Classify
    healthy: list[tuple[str, set[str]]] = []
    orphans: list[str] = []
    phantoms: list[tuple[str, set[str]]] = []

    allowlist_norm = {normalize_path(a) for a in ORPHAN_ALLOWLIST}
    for endpoint in sorted(endpoints):
        norm = normalize_path(endpoint)
        # Endpoint is healthy if any frontend ref matches it (incl. prefix).
        is_used = False
        for ref in refs:
            if matches_any(ref, [endpoint]):
                is_used = True
                healthy.append((endpoint, refs[ref]))
                break
        if is_used:
            continue
        if endpoint in ORPHAN_ALLOWLIST or norm in allowlist_norm:
            continue
        # Skip /api/v1/admin/* and /api/v1/jobs/* by default — these are
        # backend-only by design.
        if "/admin/" in endpoint or "/jobs/" in endpoint or "/agent-governance/" in endpoint:
            continue
        orphans.append(endpoint)

    for ref in sorted(refs):
        if not matches_any(ref, endpoints):
            phantoms.append((ref, refs[ref]))

    report = {
        "summary": {
            "total_endpoints": len(endpoints),
            "total_refs": len(refs),
            "healthy_pairs": len(healthy),
            "orphan_endpoints": len(orphans),
            "phantom_refs": len(phantoms),
        },
        "orphans": orphans,
        "phantoms": [{"ref": r, "files": sorted(f)} for r, f in phantoms],
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif not args.quiet:
        print(f"FRONTEND ↔ BACKEND WIRING AUDIT")
        print(f"================================")
        print(f"Total endpoints declared : {report['summary']['total_endpoints']}")
        print(f"Total frontend refs      : {report['summary']['total_refs']}")
        print(f"Healthy pairs            : {report['summary']['healthy_pairs']}")
        print(f"Orphan endpoints         : {report['summary']['orphan_endpoints']}")
        print(f"Phantom references       : {report['summary']['phantom_refs']}")
        print()
        if orphans:
            print("ORPHAN ENDPOINTS (declared, never used by frontend):")
            for o in orphans[:30]:
                print(f"  - {o}")
            if len(orphans) > 30:
                print(f"  ... and {len(orphans) - 30} more (re-run with --json for full list)")
            print()
        if phantoms:
            print("PHANTOM REFERENCES (frontend says it uses these but they don't exist):")
            for ref, files in phantoms[:30]:
                print(f"  - {ref}")
                for f in sorted(files)[:3]:
                    print(f"      · {f}")
            print()

    # Phantom references = frontend lying about backend = critical.
    # Orphan endpoints = backend code without consumer = mild waste.
    if phantoms:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
