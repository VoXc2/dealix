"""Board-Ready Risk Register v2 — typed row + 12 doctrine risks.

See ``docs/board_ready/RISK_REGISTER_V2.md``. Re-uses the doctrine risk
enumeration from ``institutional_scaling_os.risk_register`` and adds the
board-ready row shape with severity/likelihood bands.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.institutional_scaling_os.risk_register import (
    DOCTRINE_RISKS,
    DoctrineRisk,
    RiskLevel,
)


@dataclass(frozen=True)
class BoardRiskRow:
    risk: DoctrineRisk
    owner: str
    likelihood: RiskLevel
    impact: RiskLevel
    early_warning_signal: str
    control: str
    response_plan: str

    def severity_band(self) -> str:
        """Composite band: ``critical`` if both impact and likelihood are high."""

        if self.impact in {RiskLevel.HIGH, RiskLevel.CRITICAL} and self.likelihood in {
            RiskLevel.HIGH,
            RiskLevel.CRITICAL,
        }:
            return "critical"
        if self.impact in {RiskLevel.HIGH, RiskLevel.CRITICAL}:
            return "high"
        if self.likelihood in {RiskLevel.HIGH, RiskLevel.CRITICAL}:
            return "high"
        return "medium"


__all__ = ["BoardRiskRow", "DOCTRINE_RISKS", "DoctrineRisk", "RiskLevel"]
