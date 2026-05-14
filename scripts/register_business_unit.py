#!/usr/bin/env python3
"""Register or update a Business Unit in `data/business_units.json`.

Honest-marker discipline: requires `--really-this-is-a-bu` (no
`--force` shortcut). Records `entry_id` (UUID), `git_author`,
`created_at`. Validates `status` against the existing
`UnitPortfolioDecision` enum (zero parallel enums).

Usage:
    python scripts/register_business_unit.py --really-this-is-a-bu \\
        --slug sprint-delivery \\
        --name "Dealix Sprint Delivery" \\
        --owner founder \\
        --status BUILD \\
        --kpi "Sprints delivered per month" \\
        --charter-path docs/holding/units/dealix-sprint-delivery.md \\
        --sector b2b_services

    # Update existing BU status (e.g., promote to SCALE):
    python scripts/register_business_unit.py --really-this-is-a-bu \\
        --slug core-os --update-status SCALE --reason "MRR > baseline 3 months"

    # KILL requires a reason:
    python scripts/register_business_unit.py --really-this-is-a-bu \\
        --slug experimental --update-status KILL \\
        --reason "no client demand after 90 days"
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "data" / "business_units.json"

sys.path.insert(0, str(REPO_ROOT))
from auto_client_acquisition.holding_os.unit_governance import (  # noqa: E402
    UnitPortfolioDecision,
)

VALID_STATUSES = {s.name for s in UnitPortfolioDecision}


def _git_author() -> str:
    try:
        out = subprocess.run(
            ["git", "config", "user.email"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=False, timeout=2,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except Exception:
        pass
    return "unknown"


def _load() -> dict:
    if not REGISTRY.exists():
        return {
            "registry_id": "DEALIX-GROUP-BU-REGISTRY-001",
            "updated_at": datetime.now(timezone.utc).date().isoformat(),
            "doctrine_version_required": "v1.0.0",
            "entries": [],
        }
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def _write(data: dict) -> None:
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def register_new(
    *, slug: str, name: str, owner: str, status: str, kpi: str,
    charter_path: str, sector: str, doctrine_version: str = "v1.0.0",
    reason: str | None = None,
) -> dict:
    if status not in VALID_STATUSES:
        raise SystemExit(f"unknown status {status!r}. Valid: {sorted(VALID_STATUSES)}")
    if status in ("KILL", "HOLD") and not reason:
        raise SystemExit(f"status {status} requires --reason")

    now = datetime.now(timezone.utc).isoformat()
    entry = {
        "entry_id": uuid.uuid4().hex,
        "slug": slug.strip(),
        "name": name.strip(),
        "status": status,
        "owner": owner.strip(),
        "kpi": kpi.strip(),
        "doctrine_version": doctrine_version,
        "charter_path": charter_path.strip(),
        "sector": sector.strip(),
        "created_at": now,
        "git_author": _git_author(),
        "reason": reason,
    }
    data = _load()
    if any(e["slug"] == entry["slug"] for e in (data.get("entries") or [])):
        raise SystemExit(
            f"slug {entry['slug']!r} already registered. "
            f"Use --update-status to change its status."
        )
    entries = list(data.get("entries") or [])
    entries.append(entry)
    data["entries"] = entries
    data["updated_at"] = now[:10]
    _write(data)
    return entry


def update_status(*, slug: str, new_status: str, reason: str | None) -> dict:
    if new_status not in VALID_STATUSES:
        raise SystemExit(f"unknown status {new_status!r}. Valid: {sorted(VALID_STATUSES)}")
    if new_status in ("KILL", "HOLD") and not reason:
        raise SystemExit(f"status {new_status} requires --reason")

    data = _load()
    entries = list(data.get("entries") or [])
    for e in entries:
        if e["slug"] == slug:
            e["status"] = new_status
            e["reason"] = reason
            e["updated_at"] = datetime.now(timezone.utc).isoformat()
            data["entries"] = entries
            data["updated_at"] = e["updated_at"][:10]
            _write(data)
            return e
    raise SystemExit(f"slug {slug!r} not found in registry")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="register / update a business unit")
    parser.add_argument(
        "--really-this-is-a-bu",
        dest="really", action="store_true",
        help="REQUIRED. Confirms this is a real BU registration / change.",
    )
    parser.add_argument("--slug", required=True)
    parser.add_argument("--update-status", default=None,
                        help="if set, update existing BU's status")
    parser.add_argument("--reason", default=None,
                        help="required for KILL or HOLD status")
    # New-BU fields.
    parser.add_argument("--name", default=None)
    parser.add_argument("--owner", default=None)
    parser.add_argument("--status", default=None,
                        help=f"one of: {sorted(VALID_STATUSES)}")
    parser.add_argument("--kpi", default=None)
    parser.add_argument("--charter-path", default=None)
    parser.add_argument("--sector", default="b2b_services")
    parser.add_argument("--doctrine-version", default="v1.0.0")
    args = parser.parse_args(argv)

    if not args.really:
        print(
            "REFUSED. Pass --really-this-is-a-bu to confirm this is a real "
            "BU change, not a test.",
            file=sys.stderr,
        )
        return 2

    if args.update_status:
        entry = update_status(
            slug=args.slug,
            new_status=args.update_status,
            reason=args.reason,
        )
        print(f"updated {entry['slug']}: status -> {entry['status']}")
        return 0

    required_missing = [
        f for f, v in [
            ("--name", args.name), ("--owner", args.owner),
            ("--status", args.status), ("--kpi", args.kpi),
            ("--charter-path", args.charter_path),
        ] if not v
    ]
    if required_missing:
        print(f"REFUSED. Missing for new BU: {required_missing}", file=sys.stderr)
        return 2

    entry = register_new(
        slug=args.slug, name=args.name, owner=args.owner,
        status=args.status, kpi=args.kpi,
        charter_path=args.charter_path, sector=args.sector,
        doctrine_version=args.doctrine_version,
        reason=args.reason,
    )
    print(f"registered BU: {entry['slug']} ({entry['status']})")
    print(f"  entry_id: {entry['entry_id']}")
    print(f"  re-run: python scripts/validate_business_units.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
