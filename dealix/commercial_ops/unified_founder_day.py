"""Unified founder day — in-process governed pipeline (API + CLI)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dealix.commercial_ops.paths import FOUNDER_BRIEFS_DIR, REPO_ROOT

RESEARCH_BENCHMARK_2026_AR = {
    "consensus": [
        "إيقاع أسبوعي قرارات + أدلة (ليس vanity metrics)",
        "AI يُعدّ المسودات والحزم — المؤسس يوافق ويرسل",
        "90 يوم founder-led قبل توظيف SDR",
        "لا إرسال خارجي كامل بدون مراجعة بشرية",
    ],
    "dealix_position_ar": (
        "Dealix = Revenue OS بحوكمة: أقصى أتمتة داخل الريبو حتى حد الموافقة — "
        "أفضل مسار لـ B2B السعودي من «أتمتة إرسال كاملة»."
    ),
}


def _run_subprocess(
    label: str,
    cmd: list[str],
    *,
    optional: bool = False,
    timeout_s: int = 600,
) -> dict[str, Any]:
    t0 = time.monotonic()
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "APP_ENV": os.environ.get("APP_ENV", "test")}
    try:
        proc = subprocess.run(  # noqa: S603 — cmd built from internal script list
            cmd,
            cwd=str(REPO_ROOT),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_s,
        )
        ok = proc.returncode == 0
        verdict = "OK" if ok else ("SKIP" if optional else "FAIL")
        return {
            "label": label,
            "verdict": verdict,
            "exit_code": proc.returncode,
            "elapsed_s": round(time.monotonic() - t0, 1),
            "stdout_tail": (proc.stdout or "")[-400:],
            "stderr_tail": (proc.stderr or "")[-200:] if not ok else "",
        }
    except subprocess.TimeoutExpired:
        return {
            "label": label,
            "verdict": "FAIL",
            "error": "timeout",
            "elapsed_s": round(time.monotonic() - t0, 1),
        }
    except OSError as exc:
        return {
            "label": label,
            "verdict": "FAIL" if not optional else "SKIP",
            "error": str(exc),
            "elapsed_s": round(time.monotonic() - t0, 1),
        }


def _write_autopilot_artifact() -> dict[str, Any]:
    from dealix.commercial_ops.founder_full_autopilot import (
        build_autopilot_snapshot,
        write_autopilot_brief,
    )

    snap = build_autopilot_snapshot()
    path = write_autopilot_brief()
    return {
        "ok": True,
        "path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "verdict_level": (snap.get("verdict") or {}).get("level"),
        "queue_len": len(snap.get("queue") or []),
    }


def _phase_in_process(label: str, fn: Any, **kwargs: Any) -> dict[str, Any]:
    t0 = time.monotonic()
    try:
        result = fn(**kwargs)
        if isinstance(result, dict):
            v = result.get("verdict")
            ok = result.get("ok", v in ("PASS", "PARTIAL", "OK", True) if v is not None else True)
        else:
            ok = True
        return {
            "label": label,
            "verdict": "OK" if ok else "FAIL",
            "elapsed_s": round(time.monotonic() - t0, 1),
            "detail": result,
        }
    except Exception as exc:
        return {
            "label": label,
            "verdict": "FAIL",
            "error": str(exc),
            "elapsed_s": round(time.monotonic() - t0, 1),
        }


def run_unified_founder_day(
    *,
    quick: bool = False,
    top_n: int = 15,
    run_commercial_subprocess: bool = True,
    run_optional_scripts: bool = True,
) -> dict[str, Any]:
    """Full governed day in-process where possible; subprocess for heavy commercial shell."""
    from dealix.commercial_ops.evidence_append import log_founder_commercial_day_if_needed
    from dealix.commercial_ops.founder_comprehensive_plan import build_comprehensive_status
    from dealix.commercial_ops.founder_strongest_ops import (
        build_strongest_ops_snapshot,
        write_strongest_ops_brief,
    )
    from dealix.commercial_ops.full_ops_autopilot import run_morning_core

    n = max(1, min(top_n, 30))
    phases: list[dict[str, Any]] = []

    phases.append(
        _phase_in_process(
            "Strongest Ops (morning)",
            lambda: {
                "ok": True,
                "paths": write_strongest_ops_brief(mode="morning", run_checks=False),
                "snapshot": build_strongest_ops_snapshot(mode="morning", run_checks=False),
            },
        )
    )

    phases.append(
        _phase_in_process(
            "Morning core (War Room · dogfooding · packs)",
            lambda: run_morning_core(top_n=n, run_optional_scripts=run_optional_scripts),
        )
    )

    if not quick and run_commercial_subprocess:
        if sys.platform == "win32":
            cmd = ["powershell", "-File", str(REPO_ROOT / "scripts/run_founder_commercial_day.ps1")]
        else:
            cmd = ["bash", str(REPO_ROOT / "scripts/run_founder_commercial_day.sh")]
        phases.append(
            _run_subprocess("Founder commercial day", cmd, optional=True, timeout_s=900)
        )

    phases.append(
        _phase_in_process(
            "Evidence log",
            lambda: log_founder_commercial_day_if_needed(verdict="PASS", dry_run=False),
        )
    )

    comprehensive = build_comprehensive_status()
    phases.append(
        {
            "label": "Comprehensive plan snapshot",
            "verdict": "OK",
            "detail": {
                "phase_gate": comprehensive.get("phase_0_1_gate", {}).get("verdict"),
                "weekly": comprehensive.get("weekly_one_decision", {}).get("verdict"),
                "backlog_done": (comprehensive.get("max_ops_backlog") or {}).get("done"),
            },
        }
    )

    phases.append(
        _phase_in_process(
            "Full autopilot brief",
            lambda: _write_autopilot_artifact(),
        )
    )

    fail = sum(1 for p in phases if p.get("verdict") == "FAIL")
    payload = {
        "schema_version": "1.0",
        "date": datetime.now(UTC).strftime("%Y-%m-%d"),
        "generated_at": datetime.now(UTC).isoformat(),
        "verdict": "PASS" if fail == 0 else "DEGRADED",
        "policy_ar": "أتمتة كاملة — إرسال خارجي بموافقة يدوية فقط.",
        "research_benchmark_2026_ar": RESEARCH_BENCHMARK_2026_AR,
        "phases": phases,
        "comprehensive_plan": comprehensive,
        "governed_autopilot": _governed_autopilot_slice(),
        "next_ar": [
            "/ar/ops/founder",
            "/ar/ops/approvals",
            "مساءً: py -3 scripts/founder_evening_evidence.py",
        ],
    }

    FOUNDER_BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    day = payload["date"]
    path = FOUNDER_BRIEFS_DIR / f"unified_founder_day_{day}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    payload["artifact_path"] = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    return payload


def _governed_autopilot_slice() -> dict[str, Any]:
    from dealix.commercial_ops.founder_full_autopilot import build_autopilot_snapshot

    snap = build_autopilot_snapshot()
    return {
        "verdict": snap.get("verdict"),
        "queue": snap.get("queue"),
        "customer_stage": snap.get("customer_stage"),
        "pls_readiness": snap.get("pls_readiness"),
    }
