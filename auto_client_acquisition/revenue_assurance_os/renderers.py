"""Markdown renderers for Revenue Assurance artifacts (bilingual AR/EN).

Rendering only — no I/O, no live-send. CLI generators write the output.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.revenue_assurance_os.board_pack import BoardPack
from auto_client_acquisition.revenue_assurance_os.ceo_review import CeoReview
from auto_client_acquisition.revenue_assurance_os.funnel_scoreboard import FunnelScoreboard
from auto_client_acquisition.revenue_assurance_os.truth_report import TruthReport

_NO_LIVE_SEND = "> Internal document — NO_LIVE_SEND. Founder reviews and shares manually."


def render_truth_report(report: TruthReport) -> str:
    """Render the weekly Truth Report as markdown."""
    lines: list[str] = [
        "# Dealix Full Ops — Truth Report / تقرير الحقيقة",
        "",
        _NO_LIVE_SEND,
        "",
        f"- Generated: {report.generated_at}",
        f"- Local git SHA: `{report.local_git_sha}`",
        f"- Production git SHA: `{report.prod_git_sha}`",
        f"- SHA match / تطابق النسخة: **{report.git_sha_match}**",
        f"- Verifier status: {report.verifier_status}",
        f"- Health endpoint: {report.health_endpoint}",
        "",
        "## Hard Gates / البوابات الصارمة",
        "",
        "| Gate | Test files | Locked |",
        "| --- | --- | --- |",
    ]
    for gate in report.hard_gates:
        locked = "✅" if gate["locked"] else "❌"
        files = ", ".join(f"`{f}`" for f in gate["test_files"]) or "—"
        lines.append(f"| {gate['gate']} | {files} | {locked} |")

    ev = report.revenue_evidence
    lines += [
        "",
        "## Revenue Evidence / دليل الإيراد",
        "",
        f"- Value events: {ev.get('value_events', 0)}",
        f"- Verified: {ev.get('verified_count', 0)}",
        f"- Client-confirmed: {ev.get('client_confirmed_count', 0)}",
        f"- Bankable (SAR): {ev.get('bankable_sar', 0.0)}",
        f"- Paid intent / نية دفع: {'yes' if report.paid_intent else 'no'}",
        "",
        "## Next Revenue Action / الإجراء القادم",
        "",
        f"{report.next_revenue_action}",
        "",
    ]
    return "\n".join(lines)


def render_funnel_scoreboard(board: FunnelScoreboard) -> str:
    """Render the daily Funnel Scoreboard as markdown."""
    lines: list[str] = [
        f"# Funnel Scoreboard / لوحة القمع — {board.period}",
        "",
        _NO_LIVE_SEND,
        "",
        f"- On track / على المسار: {'yes' if board.on_track else 'no'}",
        f"- Bottleneck / نقطة الاختناق: **{board.bottleneck_stage}**",
        "",
        "| Stage | Count | Target | Gap |",
        "| --- | --- | --- | --- |",
    ]
    for stage, count in board.counts.items():
        target = board.targets.get(stage, 0)
        gap = board.gaps.get(stage, 0)
        lines.append(f"| {stage} | {count} | {target} | {gap} |")
    lines.append("")
    return "\n".join(lines)


def render_ceo_review(review: CeoReview) -> str:
    """Render the Weekly CEO Review scaffold as markdown."""
    lines: list[str] = [
        f"# Weekly CEO Review / مراجعة المدير الأسبوعية — {review.week_label}",
        "",
        _NO_LIVE_SEND,
        "",
        f"- Generated: {review.generated_at}",
        "",
        "## Questions / الأسئلة",
        "",
    ]
    for idx, (en, ar) in enumerate(review.questions, start=1):
        lines.append(f"{idx}. {en} — {ar}")
    if review.bottleneck:
        bn = review.bottleneck
        lines += [
            "",
            "## Funnel Bottleneck / نقطة الاختناق",
            "",
            f"- Stage: **{bn.get('bottleneck_stage', 'unknown')}**",
            f"- Likely causes: {', '.join(bn.get('likely_causes', ()))}",
            f"- Recommended action: {bn.get('recommended_action', '')}",
            f"- Build recommended: {bn.get('build_recommended', False)}",
        ]
    lines += [
        "",
        "## Required Decisions / القرارات المطلوبة (5)",
        "",
    ]
    for key, label in review.required_decisions:
        lines.append(f"- [ ] **{label}** (`{key}`): _____")
    lines.append("")
    return "\n".join(lines)


def _render_section(title: str, body: Any) -> list[str]:
    lines = [f"### {title}", ""]
    if isinstance(body, dict):
        for key, value in body.items():
            lines.append(f"- **{key}**: {value}")
    else:
        lines.append(f"{body}")
    lines.append("")
    return lines


def render_board_pack(pack: BoardPack) -> str:
    """Render the Monthly Board Pack as markdown."""
    lines: list[str] = [
        f"# Monthly Board Pack / حزمة المجلس الشهرية — {pack.month_label}",
        "",
        _NO_LIVE_SEND,
        "",
        f"- Generated: {pack.generated_at}",
        "",
    ]
    for section_key, body in pack.sections.items():
        lines.extend(_render_section(section_key, body))
    return "\n".join(lines)


__all__ = [
    "render_board_pack",
    "render_ceo_review",
    "render_funnel_scoreboard",
    "render_truth_report",
]
