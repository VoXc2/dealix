"""Founder Master Strategic OS — waves A→F orchestrator."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from dealix.commercial_ops.paths import FOUNDER_BRIEFS_DIR, REPO_ROOT
from dealix.commercial_ops.phase_01_close_path import build_phase_01_close_path
from dealix.commercial_ops.platform_v10_readiness import analyze_platform_v10_readiness
from dealix.commercial_ops.railway_production import analyze_railway_production


def wave_d_cadence_unify() -> dict[str, Any]:
    canonical = REPO_ROOT / "scripts/run_dealix_unified_founder_day.py"
    return {
        "wave": "D",
        "verdict": "OK" if canonical.is_file() else "FAIL",
        "canonical_morning": "py -3 scripts/run_dealix_unified_founder_day.py",
    }


def run_founder_master_strategic_os(
    *,
    skip_live: bool = False,
    seed_queue: bool = False,
    **kwargs: Any,
) -> dict[str, Any]:
    _ = (seed_queue, kwargs)
    phase = build_phase_01_close_path()
    base = False if skip_live else "https://api.dealix.me"
    railway = analyze_railway_production(api_base=base)
    v10 = analyze_platform_v10_readiness()
    overall = "WARN"
    if railway.get("verdict") == "FAIL":
        overall = "FAIL"
    payload = {
        "verdict": overall,
        "date": datetime.now(UTC).strftime("%Y-%m-%d"),
        "results": {
            "wave_a": {"verdict": railway.get("verdict")},
            "wave_c": {"verdict": phase.get("verdict"), "blockers_ar": phase.get("blockers_ar")},
            "wave_d": wave_d_cadence_unify(),
            "wave_f": {"verdict": v10.get("verdict"), "blocked": v10.get("blocked_by") is not None},
        },
    }
    FOUNDER_BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    out = FOUNDER_BRIEFS_DIR / f"master_strategic_os_{payload['date']}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    payload["artifact_path"] = str(out.relative_to(REPO_ROOT)).replace("\\", "/")
    return payload
