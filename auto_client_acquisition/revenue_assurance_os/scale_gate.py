"""Scale Gate — the 7 hard thresholds that must hold before expansion.

No ads, no affiliate expansion, no portal build, no hiring until every
threshold passes. Conservative by default: missing signal blocks scaling.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

# Threshold spec — (key, human description, predicate-passes-when).
MIN_ASSURANCE_SCORE = 75
MIN_APPROVAL_COMPLIANCE = 1.0
MAX_HIGH_RISK_AUTO_SEND = 0
MIN_LEAD_SCORING_COVERAGE = 1.0
MIN_EVIDENCE_COMPLETENESS = 0.90
MIN_SUPPORT_HIGH_RISK_ESCALATION = 1.0
MAX_AFFILIATE_PAYOUT_BEFORE_PAYMENT = 0


@dataclass(frozen=True, slots=True)
class GateCheck:
    key: str
    passed: bool
    observed: Any
    threshold: Any
    note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ScaleGateResult:
    can_scale: bool
    checks: tuple[GateCheck, ...]
    blocking_reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "can_scale": self.can_scale,
            "checks": [c.to_dict() for c in self.checks],
            "blocking_reasons": list(self.blocking_reasons),
        }


def _check(key: str, observed: Any, threshold: Any, passed: bool) -> GateCheck:
    note = "ok" if passed else "below_threshold"
    if observed is None:
        passed = False
        note = "no_signal:blocks_scaling"
    return GateCheck(key, passed, observed, threshold, note)


def can_scale(signals: dict[str, Any] | None = None) -> ScaleGateResult:
    """Evaluate the 7 scale thresholds.

    ``signals`` keys: assurance_score, approval_compliance,
    high_risk_auto_send, lead_scoring_coverage, evidence_completeness,
    support_high_risk_escalation, affiliate_payout_before_payment.
    Any missing key is treated as an unmet threshold.
    """
    s = signals or {}
    checks: list[GateCheck] = []

    score = s.get("assurance_score")
    checks.append(
        _check(
            "assurance_score",
            score,
            MIN_ASSURANCE_SCORE,
            score is not None and score >= MIN_ASSURANCE_SCORE,
        )
    )
    ac = s.get("approval_compliance")
    checks.append(
        _check(
            "approval_compliance",
            ac,
            MIN_APPROVAL_COMPLIANCE,
            ac is not None and ac >= MIN_APPROVAL_COMPLIANCE,
        )
    )
    hr = s.get("high_risk_auto_send")
    checks.append(
        _check(
            "high_risk_auto_send",
            hr,
            MAX_HIGH_RISK_AUTO_SEND,
            hr is not None and hr <= MAX_HIGH_RISK_AUTO_SEND,
        )
    )
    lsc = s.get("lead_scoring_coverage")
    checks.append(
        _check(
            "lead_scoring_coverage",
            lsc,
            MIN_LEAD_SCORING_COVERAGE,
            lsc is not None and lsc >= MIN_LEAD_SCORING_COVERAGE,
        )
    )
    ec = s.get("evidence_completeness")
    checks.append(
        _check(
            "evidence_completeness",
            ec,
            MIN_EVIDENCE_COMPLETENESS,
            ec is not None and ec >= MIN_EVIDENCE_COMPLETENESS,
        )
    )
    se = s.get("support_high_risk_escalation")
    checks.append(
        _check(
            "support_high_risk_escalation",
            se,
            MIN_SUPPORT_HIGH_RISK_ESCALATION,
            se is not None and se >= MIN_SUPPORT_HIGH_RISK_ESCALATION,
        )
    )
    ap = s.get("affiliate_payout_before_payment")
    checks.append(
        _check(
            "affiliate_payout_before_payment",
            ap,
            MAX_AFFILIATE_PAYOUT_BEFORE_PAYMENT,
            ap is not None and ap <= MAX_AFFILIATE_PAYOUT_BEFORE_PAYMENT,
        )
    )

    blocking = tuple(c.key for c in checks if not c.passed)
    return ScaleGateResult(
        can_scale=not blocking,
        checks=tuple(checks),
        blocking_reasons=blocking,
    )


__all__ = [
    "GateCheck",
    "ScaleGateResult",
    "can_scale",
]
