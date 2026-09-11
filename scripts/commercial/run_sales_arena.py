#!/usr/bin/env python3
"""Run Dealix against a repeatable, adversarial Saudi B2B sales conversation."""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.company_os.sales_arena import (
    ArenaRun,
    DEFAULT_CHALLENGES,
    run_sales_arena,
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Test a real configured LLM on discovery and negotiation."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports/company_targeting/sales_arena"),
    )
    return parser.parse_args()


async def _run_isolated_arena(*, router: Any | None = None) -> ArenaRun:
    """Run each adversarial challenge with a fresh conversation context.

    The five cases are independent evaluation cases, not one customer thread.
    Replaying previous model answers into later cases increases CPU inference
    latency and makes scores order-dependent. Each turn therefore receives only
    its own scenario evidence + challenge while still using the same router.
    """

    turns = []
    first_run: ArenaRun | None = None
    for challenge in DEFAULT_CHALLENGES:
        run = await run_sales_arena(router=router, challenges=(challenge,))
        if first_run is None:
            first_run = run
        turns.extend(run.turns)

    if first_run is None:
        raise RuntimeError("sales_arena_has_no_challenges")

    passed = sum(turn.passed for turn in turns)
    average = round(sum(turn.total_score for turn in turns) / max(1, len(turns)), 2)
    recommendation = (
        "eligible_for_founder_loopback"
        if passed == len(turns) and average >= 85
        else "keep_in_shadow_mode"
    )
    return ArenaRun(
        arena_version=first_run.arena_version,
        scenario_id=first_run.scenario_id,
        mode=first_run.mode,
        provider_available=first_run.provider_available,
        turns=tuple(turns),
        average_score=average,
        passed_turns=passed,
        total_turns=len(turns),
        production_recommendation=recommendation,
        external_actions_performed=0,
    )


def _markdown(payload: dict) -> str:
    lines = [
        "# Dealix Sales Arena",
        "",
        f"- Arena: `{payload['arena_version']}`",
        f"- Scenario: `{payload['scenario_id']}`",
        f"- Mode: `{payload['mode']}`",
        f"- Average: **{payload['average_score']}/100**",
        f"- Passed: **{payload['passed_turns']}/{payload['total_turns']}**",
        f"- Recommendation: `{payload['production_recommendation']}`",
        f"- External actions: **{payload['external_actions_performed']}**",
        "",
    ]
    for index, turn in enumerate(payload["turns"], start=1):
        structured = turn["structured_output"]
        facts = structured.get("facts") or []
        inferences = structured.get("inferences") or []
        unknowns = structured.get("unknowns") or []
        negotiation = structured.get("negotiation") or {}
        concessions = negotiation.get("concessions") or []
        next_action = structured.get("next_action") or {}
        escalations = structured.get("escalations") or []
        lines.extend(
            [
                f"## {index}. {turn['challenge_id']}",
                "",
                f"**العميل:** {turn['customer_message_ar']}",
                "",
                f"**رد Dealix:** {turn['agent_message_ar'] or '(لم ينتج رداً صالحاً)'}",
                "",
                f"**النتيجة:** {turn['total_score']}/100 — "
                f"{'PASS' if turn['passed'] else 'FAIL'}",
                "",
                f"**النموذج:** {turn['provider']} / {turn['model']}",
                "",
                f"**الإجراءات الخارجية:** {turn['external_actions_performed']}",
                "",
            ]
        )
        lines.append("**الحقائق ومصادرها:**")
        lines.append("")
        for fact in facts:
            if isinstance(fact, dict):
                lines.append(
                    f"- [{fact.get('source_ref', '')}] {fact.get('claim', '')}"
                )
        lines.extend(["", "**الاستنتاجات:**", ""])
        lines.extend(f"- {item}" for item in inferences)
        lines.extend(["", "**المعلومات المجهولة:**", ""])
        lines.extend(f"- {item}" for item in unknowns)
        lines.extend(["", "**استراتيجية التفاوض وgive/get:**", ""])
        lines.append(f"- BATNA: {negotiation.get('batna', '')}")
        for concession in concessions:
            if isinstance(concession, dict):
                lines.append(
                    f"- give: {concession.get('give', '')} | "
                    f"get: {concession.get('get', '')} | "
                    f"approval: {concession.get('approval_required', False)}"
                )
        lines.extend(["", "**ما يحتاج موافقة الموظف:**", ""])
        lines.append(
            f"- next_action.approval_required: "
            f"{next_action.get('approval_required', False)}"
        )
        lines.extend(f"- {item}" for item in escalations)
        lines.append("")
        if turn["critical_failures"]:
            lines.append(
                "**إخفاقات حرجة:** " + ", ".join(turn["critical_failures"])
            )
            lines.append("")
        if turn["decision_trace"]:
            lines.append("**سجل القرار المهني:**")
            lines.append("")
            for item in turn["decision_trace"]:
                lines.append(f"- {item['decision']}: {item['because']}")
            lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = _parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    try:
        run = asyncio.run(_run_isolated_arena())
    except RuntimeError as exc:
        if str(exc) != "no_llm_provider_configured":
            raise
        payload = {
            "status": "blocked",
            "reason": "no_llm_provider_configured",
            "required_one_of": [
                "ANTHROPIC_API_KEY",
                "OPENAI_API_KEY",
                "GLM_API_KEY",
                "GROQ_API_KEY",
                "DEEPSEEK_API_KEY",
                "GOOGLE_API_KEY",
            ],
            "note": "The arena refuses to fake a model result.",
        }
        path = args.output_dir / "preflight.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(json.dumps(payload, indent=2))
        return 2

    payload = run.to_dict()
    payload["generated_at"] = datetime.now(UTC).isoformat()
    json_path = args.output_dir / "latest.json"
    md_path = args.output_dir / "latest.md"
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    md_path.write_text(_markdown(payload), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "passed"
                if payload["production_recommendation"]
                == "eligible_for_founder_loopback"
                else "failed",
                "average_score": payload["average_score"],
                "passed_turns": payload["passed_turns"],
                "total_turns": payload["total_turns"],
                "report_json": str(json_path),
                "report_md": str(md_path),
                "external_actions_performed": 0,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if payload["production_recommendation"] == "eligible_for_founder_loopback" else 1


if __name__ == "__main__":
    raise SystemExit(main())