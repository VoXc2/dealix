"""Weekly CEO Review and Monthly Quality Audit generators.

The Weekly CEO Review turns the registry + scorecard into the founder's
12-question review with a forced weekly decision. The Monthly Quality
Audit reconciles the registry's declared Definition-of-Done claims against
what the Evidence Ledger actually contains — catching fake green.

Pure data assembly + markdown rendering. Never raises.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from auto_client_acquisition.execution_assurance_os.definition_of_done import (
    evaluate_acceptance_gate,
    evaluate_dod,
)
from auto_client_acquisition.execution_assurance_os.registry import (
    EVENT_EVIDENCE_CATEGORY,
    MachineRegistry,
)
from auto_client_acquisition.execution_assurance_os.scorecard import (
    aggregate_score,
    score_machine,
)

# The nine standing weekly decisions (founder's improvement loop).
WEEKLY_DECISIONS: tuple[str, ...] = (
    "Double down",
    "Fix bottleneck",
    "Kill channel",
    "Improve message",
    "Improve proof asset",
    "Improve KB",
    "Improve agent guardrail",
    "No-build",
    "Build only a repeated workflow",
)

# The 12 standing CEO questions (EN + AR).
_CEO_QUESTIONS: tuple[tuple[str, str, str], ...] = (
    ("Did qualified leads come in?", "هل جتنا leads مؤهلة؟", "live"),
    ("Where did they come from?", "من أين جاءت؟", "live"),
    ("Did the system classify them correctly?", "هل النظام صنفها صح؟", "registry"),
    ("How many meetings?", "كم meeting؟", "live"),
    ("How many scopes?", "كم scope؟", "live"),
    ("How many invoices?", "كم invoice؟", "live"),
    ("How many paid?", "كم paid؟", "live"),
    ("Where did the funnel break?", "أين تعطل الـfunnel؟", "registry"),
    ("What was the most common support question?", "ما أكثر سؤال دعم؟", "live"),
    ("What was the most common objection?", "ما أكثر objection؟", "live"),
    ("What dangerous action was blocked?", "ما action خطير تم حظره؟", "registry"),
    ("Do we need to build, or not?", "هل نحتاج build أو لا؟", "registry"),
)


@dataclass(frozen=True, slots=True)
class CeoReviewReport:
    """A complete Weekly CEO Review."""

    generated_at: str
    portfolio: dict[str, Any]
    questions: tuple[dict[str, Any], ...]
    flagged_machines: tuple[dict[str, Any], ...]
    weekly_decisions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "portfolio": self.portfolio,
            "questions": list(self.questions),
            "flagged_machines": list(self.flagged_machines),
            "weekly_decisions": list(self.weekly_decisions),
        }


@dataclass(frozen=True, slots=True)
class QualityAuditReport:
    """A complete Monthly Quality Audit."""

    generated_at: str
    evidence_available: bool
    evidence_path: str
    machine_findings: tuple[dict[str, Any], ...]
    contradictions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "evidence_available": self.evidence_available,
            "evidence_path": self.evidence_path,
            "machine_findings": list(self.machine_findings),
            "contradictions": list(self.contradictions),
        }


def _now() -> str:
    return datetime.now(UTC).isoformat()


# ── Weekly CEO Review ────────────────────────────────────────────────
def generate_weekly_ceo_review(reg: MachineRegistry) -> CeoReviewReport:
    """Build the Weekly CEO Review from the registry and scorecard."""
    portfolio = aggregate_score(reg)
    scores = {s.machine_id: s for s in portfolio.machines}

    flagged: list[dict[str, Any]] = []
    for spec in reg.machines:
        score = scores[spec.id]
        gate = evaluate_acceptance_gate(spec)
        if gate.passed and score.consistency == "consistent":
            continue
        flagged.append(
            {
                "machine_id": spec.id,
                "name": spec.name,
                "owner": spec.owner,
                "maturity": score.declared_score,
                "target": score.target_score,
                "gap_to_target": score.gap_to_target,
                "consistency": score.consistency,
                "gate_unmet": list(gate.unmet),
                "decision_options": list(WEEKLY_DECISIONS),
            }
        )

    inconsistent = [s.name for s in portfolio.machines if s.consistency == "inconsistent"]
    below_target = [
        f"{s.name} ({s.declared_score}/{s.target_score})"
        for s in portfolio.machines
        if s.declared_score < s.target_score
    ]
    blocked_actions = sorted(
        {a for spec in reg.machines for a in spec.approval_required_actions}
    )
    biggest_gap = max(
        portfolio.machines,
        key=lambda s: s.gap_to_target,
        default=None,
    )

    prefill: dict[int, str] = {
        3: (
            "No maturity/DoD inconsistencies detected."
            if not inconsistent
            else "Inconsistent maturity claims: " + ", ".join(inconsistent)
        ),
        8: (
            "All machines at target."
            if not below_target
            else "Machines below target: " + ", ".join(below_target)
        ),
        11: (
            "Approval-gated actions this period: " + ", ".join(blocked_actions)
            if blocked_actions
            else "No approval-gated actions registered."
        ),
        12: (
            f"Largest gap: {biggest_gap.name} "
            f"(+{biggest_gap.gap_to_target} to target). "
            "Build only if this is a repeated, paid workflow."
            if biggest_gap and biggest_gap.gap_to_target > 0
            else "No build implied — every machine is at target."
        ),
    }

    questions = tuple(
        {
            "n": i + 1,
            "question_en": en,
            "question_ar": ar,
            "answer_source": source,
            "prefilled": prefill.get(i + 1),
        }
        for i, (en, ar, source) in enumerate(_CEO_QUESTIONS)
    )

    return CeoReviewReport(
        generated_at=_now(),
        portfolio=portfolio.to_dict(),
        questions=questions,
        flagged_machines=tuple(flagged),
        weekly_decisions=WEEKLY_DECISIONS,
    )


# ── Monthly Quality Audit ────────────────────────────────────────────
def _evidence_path(override: str | None) -> Path:
    if override:
        return Path(override)
    env = os.environ.get("DEALIX_EVIDENCE_CONTROL_PATH")
    if env:
        p = Path(env)
        if p.is_absolute():
            return p
        return Path(__file__).resolve().parents[2] / p
    return (
        Path(__file__).resolve().parents[2]
        / "var"
        / "evidence-control.jsonl"
    )


def _count_evidence_by_category(path: Path) -> dict[str, int]:
    """Count Evidence Ledger items by type. Empty dict if unavailable."""
    if not path.exists():
        return {}
    counts: dict[str, int] = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            cat = str(data.get("type", ""))
            if cat:
                counts[cat] = counts.get(cat, 0) + 1
    except OSError:
        return {}
    return counts


def generate_monthly_quality_audit(
    reg: MachineRegistry,
    evidence_path: str | None = None,
) -> QualityAuditReport:
    """Reconcile declared DoD claims against the Evidence Ledger.

    A machine claiming Automated maturity (>=3) while its expected evidence
    categories are entirely absent from the ledger is a contradiction —
    the registry claim is not backed by recorded proof.
    """
    path = _evidence_path(evidence_path)
    counts = _count_evidence_by_category(path)
    available = bool(counts)

    findings: list[dict[str, Any]] = []
    contradictions: list[str] = []

    for spec in reg.machines:
        score = score_machine(spec)
        dod = evaluate_dod(spec)
        expected_categories = sorted(
            {
                EVENT_EVIDENCE_CATEGORY[e]
                for e in spec.evidence_event_names
                if e in EVENT_EVIDENCE_CATEGORY
            }
        )
        observed = (
            sum(counts.get(cat, 0) for cat in expected_categories)
            if available
            else None
        )
        verdict = "no_evidence_baseline"
        if available:
            if score.declared_score >= 3 and observed == 0:
                verdict = "contradiction"
                contradictions.append(
                    f"{spec.name}: registry claims maturity "
                    f"{score.declared_score} but the Evidence Ledger has no "
                    f"events in its expected categories "
                    f"({', '.join(expected_categories) or 'none'})"
                )
            elif observed and observed > 0:
                verdict = "supported"
            else:
                verdict = "below_automated_no_evidence_expected"
        findings.append(
            {
                "machine_id": spec.id,
                "name": spec.name,
                "declared_maturity": score.declared_score,
                "dod_pct": dod.pct,
                "dod_met": f"{dod.items_met}/{dod.items_total}",
                "expected_evidence_categories": expected_categories,
                "observed_evidence_count": observed,
                "verdict": verdict,
            }
        )

    return QualityAuditReport(
        generated_at=_now(),
        evidence_available=available,
        evidence_path=str(path),
        machine_findings=tuple(findings),
        contradictions=tuple(contradictions),
    )


# ── Markdown renderers ───────────────────────────────────────────────
def render_ceo_review_markdown(report: CeoReviewReport) -> str:
    """Render a Weekly CEO Review as markdown."""
    p = report.portfolio
    lines: list[str] = [
        "# Weekly CEO Review — Dealix Execution Assurance",
        "",
        f"_Generated: {report.generated_at}_",
        "",
        "## Portfolio",
        "",
        f"- Mean maturity: **{p['mean_maturity']}/5** "
        f"(target {p['target_mean']}/5)",
        f"- Readiness: **{p['readiness_label']}** ({p['percentage']}%)",
        f"- Machines at target: **{p['machines_at_target']}/"
        f"{p['machines_total']}**",
        f"- Inconsistent maturity claims: **{p['inconsistent_count']}**",
        "",
        "## The 12 Questions",
        "",
    ]
    for q in report.questions:
        lines.append(f"**{q['n']}. {q['question_en']}** — {q['question_ar']}")
        if q["prefilled"]:
            lines.append(f"  - System: {q['prefilled']}")
        else:
            lines.append(f"  - Answer from: {q['answer_source']} data (founder to fill)")
        lines.append("")

    lines.append("## Flagged Machines")
    lines.append("")
    if not report.flagged_machines:
        lines.append("None — every machine passed its acceptance gate.")
    else:
        for m in report.flagged_machines:
            lines.append(
                f"### {m['name']} — maturity {m['maturity']}/{m['target']} "
                f"({m['consistency']})"
            )
            for u in m["gate_unmet"]:
                lines.append(f"  - {u}")
            lines.append(
                "  - Decision options: " + ", ".join(m["decision_options"])
            )
            lines.append("")

    lines.append("## Weekly Decision (pick at least one)")
    lines.append("")
    for d in report.weekly_decisions:
        lines.append(f"- [ ] {d}")
    lines.append("")
    return "\n".join(lines)


def render_audit_markdown(report: QualityAuditReport) -> str:
    """Render a Monthly Quality Audit as markdown."""
    lines: list[str] = [
        "# Monthly Quality Audit — Dealix Execution Assurance",
        "",
        f"_Generated: {report.generated_at}_",
        f"_Evidence Ledger: {report.evidence_path} "
        f"({'available' if report.evidence_available else 'no baseline yet'})_",
        "",
        "## Registry vs. Evidence Ledger",
        "",
    ]
    for f in report.machine_findings:
        observed = f["observed_evidence_count"]
        observed_txt = "n/a" if observed is None else str(observed)
        lines.append(
            f"- **{f['name']}** — maturity {f['declared_maturity']}, "
            f"DoD {f['dod_met']} ({f['dod_pct']}%), "
            f"evidence events: {observed_txt} → `{f['verdict']}`"
        )
    lines.append("")
    lines.append("## Contradictions")
    lines.append("")
    if not report.contradictions:
        lines.append(
            "None detected."
            if report.evidence_available
            else "No evidence baseline yet — cannot verify. Re-run once the "
            "Evidence Ledger has data."
        )
    else:
        for c in report.contradictions:
            lines.append(f"- {c}")
    lines.append("")
    return "\n".join(lines)


__all__ = [
    "WEEKLY_DECISIONS",
    "CeoReviewReport",
    "QualityAuditReport",
    "generate_monthly_quality_audit",
    "generate_weekly_ceo_review",
    "render_audit_markdown",
    "render_ceo_review_markdown",
]
