#!/usr/bin/env python3
"""Daily Dealix system snapshot — silent audit trail.

Composes the same read-only sections as ``GET /api/v1/founder/dashboard``
but reads them directly from local Python modules so it works in a CI
runner that has the repo (no deployed API needed). The output is a
single JSON file at ``docs/snapshots/<YYYY-MM-DD>.json`` that is
committed to the repo to provide a daily audit trail of system state.

Hard rules (enforced by tests):
    - No HTTP requests, no LLM calls, no outbound notifications.
    - No secrets required to run.
    - Never reports ``live_gates`` as ``ALLOWED`` on a clean checkout.
    - No PII — counts, statuses, and IDs only.
    - Idempotent — re-running on the same day overwrites cleanly.

Usage:
    python scripts/dealix_snapshot.py                # writes docs/snapshots/<today>.json
    python scripts/dealix_snapshot.py --print        # writes nothing, prints to stdout
    python scripts/dealix_snapshot.py --out PATH     # writes to PATH instead
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SNAPSHOT_DIR = REPO_ROOT / "docs" / "snapshots"

# Allow `python scripts/dealix_snapshot.py` from any cwd to find the
# in-repo packages without needing an editable install.
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _safe(fn, *, default: Any) -> Any:
    """Run fn(); on any error, return a typed error blob.

    Mirrors api/routers/founder.py::_safe — one probe failure must not
    poison the whole snapshot. Audit trails should still record what
    they could read.
    """
    try:
        return fn()
    except BaseException as exc:  # noqa: BLE001
        return {
            "_error": True,
            "_type": type(exc).__name__,
            "_message": str(exc)[:200],
            "_default": default,
        }


def _service_counts() -> dict[str, Any]:
    from auto_client_acquisition.self_growth_os import service_activation_matrix
    return service_activation_matrix.counts()


def _reliability() -> dict[str, Any]:
    from auto_client_acquisition.reliability_os import build_health_matrix
    matrix = build_health_matrix()
    subs = [
        {"name": s.get("name"), "status": s.get("status")}
        for s in matrix.get("subsystems") or []
    ]
    return {
        "overall_status": matrix.get("overall_status"),
        "counts": matrix.get("counts"),
        "subsystems": subs,
    }


def _live_gates() -> dict[str, str]:
    out: dict[str, str] = {}
    try:
        from auto_client_acquisition.finance_os import is_live_charge_allowed
        live = is_live_charge_allowed()
        out["live_charge"] = "BLOCKED" if not live.get("allowed") else "ALLOWED"
    except BaseException as exc:  # noqa: BLE001
        out["live_charge"] = f"UNKNOWN ({type(exc).__name__})"
    return out


def _daily_loop_summary() -> dict[str, Any]:
    from auto_client_acquisition.self_growth_os import daily_growth_loop
    loop = daily_growth_loop.build_today()
    decisions = loop.get("decisions") or []
    return {
        "decisions_count": len(decisions),
        "top_3_decisions": decisions[:3],
    }


def _weekly_summary() -> dict[str, Any]:
    from auto_client_acquisition.self_growth_os import weekly_growth_scorecard
    return weekly_growth_scorecard.build_scorecard()


def _promotion_candidates_top3() -> list[dict[str, Any]]:
    from auto_client_acquisition.self_growth_os import service_activation_matrix
    cands = service_activation_matrix.candidates_for_promotion()
    return [
        {
            "service_id": c.service_id,
            "name_ar": c.name_ar,
            "name_en": c.name_en,
            "status": c.status,
            "blocking_reasons": c.blocking_reasons[:5],
        }
        for c in cands[:3]
    ]


def build_snapshot() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "services": _safe(_service_counts, default={}),
        "reliability": _safe(_reliability, default={}),
        "live_gates": _live_gates(),
        "daily_loop": _safe(_daily_loop_summary, default={}),
        "weekly_scorecard": _safe(_weekly_summary, default={}),
        "promotion_candidates": _safe(_promotion_candidates_top3, default=[]),
    }


def default_out_path(now: datetime | None = None) -> Path:
    now = now or datetime.now(UTC)
    return DEFAULT_SNAPSHOT_DIR / f"{now.strftime('%Y-%m-%d')}.json"


def write_snapshot(snap: dict[str, Any], out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    # Plain write — overwrites if same-day; no append, no merge.
    out.write_text(json.dumps(snap, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Daily Dealix system snapshot.")
    p.add_argument("--out", type=Path, default=None, help="Override output path.")
    p.add_argument("--print", dest="print_only", action="store_true",
                   help="Print to stdout, write nothing.")
    args = p.parse_args(argv)

    snap = build_snapshot()

    if args.print_only:
        json.dump(snap, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0

    out = args.out or default_out_path()
    written = write_snapshot(snap, out)
    print(f"snapshot written: {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
