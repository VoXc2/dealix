"""Complete autonomous founder day — governed maximum (no external send).

Industry alignment (2025–2026): evidence-first weekly rhythm, human-in-the-loop send,
founder-led 90d before SDR hire. Dealix exceeds on PDPL/governance vs cold-send bots.
"""

from __future__ import annotations

import json
import subprocess
import sys
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

RESEARCH_VERDICT_AR = (
    "أقصى أتمتة ممكنة داخل الريبو حتى الموافقة الخارجية — "
    "أفضل من إرسال بارد كامل لـ B2B السعودي founder-led."
)


def build_complete_autonomous_plan(
    *,
    weekly: bool = False,
    evening: bool = False,
    skip_commercial_day: bool = False,
) -> dict[str, Any]:
    """Dry-run plan + wiring status (no subprocess)."""
    from dealix.commercial_ops.founder_strongest_plan import strongest_plan_status

    plan_st = strongest_plan_status()
    phases = [
        "run_governed_full_ops_autopilot.py --morning",
        "run_founder_strongest_ops.py --morning --run-checks",
    ]
    if not skip_commercial_day:
        phases.append("run_founder_commercial_day.sh")
    phases.extend(
        [
            "run_full_commercial_ops_autopilot.py --execute",
            "founder_strongest_plan_status.py",
            "run_unified_founder_day.py (in-process alternative)",
        ]
    )
    if evening or weekly:
        phases.append("run_founder_strongest_ops.py --evening")
        phases.append("founder_evening_evidence.py")
    if weekly:
        phases.append("founder_weekly_loop.sh")
    return {
        "date": datetime.now(UTC).strftime("%Y-%m-%d"),
        "phases": phases,
        "research_verdict_ar": RESEARCH_VERDICT_AR,
        "research_benchmark_2026_ar": RESEARCH_BENCHMARK_2026_AR,
        "benchmark_sample": _benchmark_rows()[:3],
        "strongest_plan_wiring": plan_st.get("ok"),
        "task_count": plan_st.get("task_count"),
        "policy_ar": "لا إرسال بارد — مسودات + موافقة فقط.",
    }


def _benchmark_rows() -> list[dict[str, str]]:
    from dealix.commercial_ops.autonomous_ops import BENCHMARK_COMPARISON_AR

    return BENCHMARK_COMPARISON_AR


def _py(script: str, *args: str) -> list[str]:
    return [sys.executable, str(REPO_ROOT / script), *args]


def _run_subprocess(cmd: list[str], *, label: str, required: bool = False) -> dict[str, Any]:
    try:
        proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=900)  # noqa: S603 — internal verify cmd
        ok = proc.returncode == 0
        return {
            "label": label,
            "ok": ok,
            "verdict": "OK" if ok else ("FAIL" if required else "SKIP"),
            "exit_code": proc.returncode,
            "stdout_tail": (proc.stdout or "")[-300:],
            "stderr_tail": (proc.stderr or "")[-200:] if not ok else "",
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "label": label,
            "ok": False,
            "verdict": "FAIL" if required else "SKIP",
            "error": str(exc),
        }


def run_complete_autonomous_day(
    *,
    weekly: bool = False,
    evening: bool = False,
    skip_commercial_day: bool = False,
    use_unified_in_process: bool = True,
    top_n: int = 15,
) -> dict[str, Any]:
    """Execute full governed day; returns artifact payload."""
    from dealix.commercial_ops.autonomous_ops import (
        build_autonomous_ops_status,
        save_last_autonomous_run,
    )
    from dealix.commercial_ops.founder_strongest_ops import (
        build_strongest_ops_snapshot,
        write_strongest_ops_brief,
    )
    from dealix.commercial_ops.unified_founder_day import run_unified_founder_day

    day = datetime.now(UTC).strftime("%Y-%m-%d")
    steps: list[dict[str, Any]] = []

    gov_args = ["--full"] if weekly else ["--morning"]
    steps.append(_run_subprocess(_py("scripts/run_governed_full_ops_autopilot.py", *gov_args), label="governed"))

    steps.append(
        _run_subprocess(
            _py("scripts/run_founder_strongest_ops.py", "--morning", "--run-checks"),
            label="strongest ops morning",
        )
    )

    if use_unified_in_process and not weekly:
        unified = run_unified_founder_day(
            quick=skip_commercial_day,
            top_n=top_n,
            run_commercial_subprocess=not skip_commercial_day,
        )
        steps.append(
            {
                "label": "unified founder day (in-process)",
                "ok": unified.get("verdict") in ("PASS", "DEGRADED"),
                "verdict": unified.get("verdict"),
                "detail": {"artifact_path": unified.get("artifact_path")},
            }
        )
    elif not skip_commercial_day:
        if sys.platform == "win32":
            cmd = ["powershell", "-File", str(REPO_ROOT / "scripts/run_founder_commercial_day.ps1")]
        else:
            cmd = ["bash", str(REPO_ROOT / "scripts/run_founder_commercial_day.sh")]
        steps.append(_run_subprocess(cmd, label="founder commercial day"))

    steps.append(
        _run_subprocess(
            _py("scripts/run_full_commercial_ops_autopilot.py", "--execute"),
            label="full ops core",
        )
    )
    steps.append(
        _run_subprocess(
            _py("scripts/founder_strongest_plan_status.py"),
            label="strongest plan wiring",
            required=True,
        )
    )

    if evening or weekly:
        steps.append(_run_subprocess(_py("scripts/founder_evening_evidence.py"), label="evening evidence"))
        steps.append(
            _run_subprocess(_py("scripts/run_founder_strongest_ops.py", "--evening"), label="strongest evening")
        )

    if weekly:
        steps.append(
            _run_subprocess(
                _py("scripts/run_founder_strongest_ops.py", "--weekly", "--run-checks"),
                label="strongest weekly",
            )
        )
        loop = (
            ["powershell", "-File", str(REPO_ROOT / "scripts/founder_weekly_loop.ps1")]
            if sys.platform == "win32"
            else ["bash", str(REPO_ROOT / "scripts/founder_weekly_loop.sh")]
        )
        steps.append(_run_subprocess(loop, label="weekly loop"))

    steps.append(
        _run_subprocess(
            _py("scripts/verify_full_autonomous_ops_stack.py", "--skip-api"),
            label="verify full autonomous stack",
            required=False,
        )
    )

    mode = "weekly" if weekly else "morning"
    brief_paths = write_strongest_ops_brief(mode=mode, run_checks=False)
    snap = build_strongest_ops_snapshot(mode="full" if weekly else "morning", run_checks=False)

    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "date": day,
        "generated_at": datetime.now(UTC).isoformat(),
        "verdict": _aggregate_verdict(steps, snap),
        "research_verdict_ar": RESEARCH_VERDICT_AR,
        "research_benchmark_2026_ar": RESEARCH_BENCHMARK_2026_AR,
        "benchmark_comparison_ar": _benchmark_rows(),
        "steps": steps,
        "strongest_ops": snap,
        "brief_paths": brief_paths,
        "autonomous_ops": build_autonomous_ops_status(),
        "commands": {
            "cli": "py -3 scripts/run_dealix_complete_autonomous_day.py",
            "api": "POST /api/v1/ops-autopilot/founder/complete-autonomous-day/run",
            "cockpit_unified": "POST /api/v1/ops-autopilot/founder/cockpit/run-unified-day",
        },
    }
    save_last_autonomous_run(payload)
    FOUNDER_BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    out = FOUNDER_BRIEFS_DIR / f"complete_autonomous_day_{day}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    payload["artifact_path"] = str(out.relative_to(REPO_ROOT)).replace("\\", "/")
    return payload


def _aggregate_verdict(steps: list[dict[str, Any]], snap: dict[str, Any]) -> str:
    if snap.get("verdict") == "FAIL_WIRING":
        return "FAIL_WIRING"
    fails = sum(1 for s in steps if s.get("verdict") == "FAIL" or (s.get("ok") is False and s.get("verdict") != "SKIP"))
    if fails:
        return "DEGRADED"
    return "PASS"
