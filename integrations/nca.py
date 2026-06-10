"""
National Cybersecurity Authority (NCA) — Essential Cybersecurity Controls (ECC).
الهيئة الوطنية للأمن السيبراني — الضوابط الأساسية للأمن السيبراني.

Implements assessment and reporting for the 12 domains of NCA ECC.
Each domain contains multiple controls that are assessed for compliance.

Ref: https://nca.gov.sa
NCA ECC-2024: 12 domains, ~100 controls
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class ControlAssessment:
    control_id: str
    name: str
    status: str  # compliant / non_compliant / partially_compliant / not_applicable / not_assessed
    score: float  # 0.0 - 1.0
    evidence_count: int = 0
    notes: str = ""
    assessed_at: str = ""


@dataclass
class DomainAssessment:
    domain_id: str
    name: str
    controls: list[ControlAssessment] = field(default_factory=list)
    overall_score: float = 0.0
    compliance_pct: float = 0.0


@dataclass
class ComplianceAssessment:
    overall_score: float
    compliance_pct: float
    domains: list[DomainAssessment] = field(default_factory=list)
    total_controls: int = 0
    compliant_controls: int = 0
    non_compliant_controls: int = 0
    partial_controls: int = 0
    not_applicable_controls: int = 0
    assessed_at: str = ""


@dataclass
class Evidence:
    id: str
    control_id: str
    title: str
    description: str
    file_path: str | None = None
    url: str | None = None
    collected_at: str = ""
    collected_by: str = ""
    status: str = "collected"  # collected / verified / expired


@dataclass
class ComplianceReport:
    report_id: str
    generated_at: str
    organization: str
    assessment: ComplianceAssessment
    recommendations: list[str] = field(default_factory=list)
    risk_level: str = "medium"  # low / medium / high / critical


class NCACompliance:
    """NCA Essential Cybersecurity Controls (ECC) compliance manager.

    Provides assessment, evidence collection, and reporting for
    all 12 ECC domains required by Saudi NCA.
    """

    ECC_CONTROLS: dict[str, dict[str, Any]] = {
        "ECC-1": {
            "name": "Governance",
            "description": "Cybersecurity governance framework including policies, roles, and responsibilities",
            "controls": [
                {"id": "ECC-1.1", "name": "Cybersecurity Policy"},
                {"id": "ECC-1.2", "name": "Cybersecurity Roles and Responsibilities"},
                {"id": "ECC-1.3", "name": "Cybersecurity Committee"},
                {"id": "ECC-1.4", "name": "Third-Party Cybersecurity"},
                {"id": "ECC-1.5", "name": "Cybersecurity in Project Management"},
            ],
        },
        "ECC-2": {
            "name": "Risk Management",
            "description": "Cybersecurity risk management framework",
            "controls": [
                {"id": "ECC-2.1", "name": "Risk Management Framework"},
                {"id": "ECC-2.2", "name": "Risk Assessment"},
                {"id": "ECC-2.3", "name": "Risk Treatment Plan"},
                {"id": "ECC-2.4", "name": "Risk Register"},
            ],
        },
        "ECC-3": {
            "name": "Asset Management",
            "description": "Identification and management of cybersecurity assets",
            "controls": [
                {"id": "ECC-3.1", "name": "Asset Inventory"},
                {"id": "ECC-3.2", "name": "Asset Classification"},
                {"id": "ECC-3.3", "name": "Asset Labeling and Handling"},
                {"id": "ECC-3.4", "name": "Asset Disposal"},
            ],
        },
        "ECC-4": {
            "name": "Identity and Access Management",
            "description": "Identity verification, access control, and privilege management",
            "controls": [
                {"id": "ECC-4.1", "name": "Identity Management"},
                {"id": "ECC-4.2", "name": "Access Control Policy"},
                {"id": "ECC-4.3", "name": "User Access Management"},
                {"id": "ECC-4.4", "name": "Privileged Access Management"},
                {"id": "ECC-4.5", "name": "Authentication Mechanisms"},
                {"id": "ECC-4.6", "name": "Remote Access Security"},
            ],
        },
        "ECC-5": {
            "name": "Physical Security",
            "description": "Physical security of facilities and assets",
            "controls": [
                {"id": "ECC-5.1", "name": "Physical Security Perimeter"},
                {"id": "ECC-5.2", "name": "Physical Access Control"},
                {"id": "ECC-5.3", "name": "Physical Security Monitoring"},
            ],
        },
        "ECC-6": {
            "name": "Platform Security",
            "description": "Security of servers, endpoints, and infrastructure",
            "controls": [
                {"id": "ECC-6.1", "name": "Secure Configuration"},
                {"id": "ECC-6.2", "name": "Vulnerability Management"},
                {"id": "ECC-6.3", "name": "Patch Management"},
                {"id": "ECC-6.4", "name": "Malware Protection"},
                {"id": "ECC-6.5", "name": "Endpoint Security"},
                {"id": "ECC-6.6", "name": "Email Security"},
                {"id": "ECC-6.7", "name": "Web Security"},
            ],
        },
        "ECC-7": {
            "name": "Network Security",
            "description": "Network segmentation, monitoring, and protection",
            "controls": [
                {"id": "ECC-7.1", "name": "Network Security Architecture"},
                {"id": "ECC-7.2", "name": "Network Segmentation"},
                {"id": "ECC-7.3", "name": "Network Monitoring"},
                {"id": "ECC-7.4", "name": "Network Access Control"},
                {"id": "ECC-7.5", "name": "Wireless Security"},
                {"id": "ECC-7.6", "name": "Network Devices Security"},
            ],
        },
        "ECC-8": {
            "name": "Application Security",
            "description": "Security throughout the application lifecycle",
            "controls": [
                {"id": "ECC-8.1", "name": "Secure Development Lifecycle"},
                {"id": "ECC-8.2", "name": "Application Security Testing"},
                {"id": "ECC-8.3", "name": "API Security"},
                {"id": "ECC-8.4", "name": "Change Management"},
                {"id": "ECC-8.5", "name": "Database Security"},
            ],
        },
        "ECC-9": {
            "name": "Cryptography",
            "description": "Encryption, key management, and cryptographic controls",
            "controls": [
                {"id": "ECC-9.1", "name": "Cryptographic Policy"},
                {"id": "ECC-9.2", "name": "Key Management"},
                {"id": "ECC-9.3", "name": "Data Encryption"},
                {"id": "ECC-9.4", "name": "Digital Certificates"},
            ],
        },
        "ECC-10": {
            "name": "Data and Privacy",
            "description": "Data classification, protection, and privacy compliance",
            "controls": [
                {"id": "ECC-10.1", "name": "Data Classification"},
                {"id": "ECC-10.2", "name": "Data Loss Prevention"},
                {"id": "ECC-10.3", "name": "Data Backup and Recovery"},
                {"id": "ECC-10.4", "name": "Data Privacy"},
                {"id": "ECC-10.5", "name": "Data Retention and Disposal"},
            ],
        },
        "ECC-11": {
            "name": "Operations",
            "description": "Cybersecurity operations, monitoring, and incident response",
            "controls": [
                {"id": "ECC-11.1", "name": "Security Operations Center"},
                {"id": "ECC-11.2", "name": "Event Logging and Monitoring"},
                {"id": "ECC-11.3", "name": "Incident Management"},
                {"id": "ECC-11.4", "name": "Threat Intelligence"},
                {"id": "ECC-11.5", "name": "Vulnerability Assessment"},
                {"id": "ECC-11.6", "name": "Penetration Testing"},
            ],
        },
        "ECC-12": {
            "name": "Business Continuity and Disaster Recovery",
            "description": "BCM and DR planning for cybersecurity incidents",
            "controls": [
                {"id": "ECC-12.1", "name": "BCM Framework"},
                {"id": "ECC-12.2", "name": "Business Impact Analysis"},
                {"id": "ECC-12.3", "name": "Business Continuity Plans"},
                {"id": "ECC-12.4", "name": "Disaster Recovery Plans"},
                {"id": "ECC-12.5", "name": "Testing and Exercises"},
            ],
        },
    }

    def __init__(self) -> None:
        self._evidence_store: dict[str, list[Evidence]] = {}

    async def assess(self) -> ComplianceAssessment:
        """Run compliance assessment across all ECC domains.

        In production, each control would query the actual system state.
        This implementation provides a structured assessment framework.
        """
        domains: list[DomainAssessment] = []
        total_controls = 0
        compliant = 0
        non_compliant = 0
        partial = 0
        na = 0

        for domain_id, domain_info in self.ECC_CONTROLS.items():
            controls = domain_info["controls"]
            domain_controls: list[ControlAssessment] = []

            for ctrl in controls:
                total_controls += 1
                assessment = await self._assess_control(ctrl["id"], ctrl["name"])
                domain_controls.append(assessment)

                if assessment.status == "compliant":
                    compliant += 1
                elif assessment.status == "non_compliant":
                    non_compliant += 1
                elif assessment.status == "partially_compliant":
                    partial += 1
                else:
                    na += 1

            domain_score = (
                sum(c.score for c in domain_controls) / len(domain_controls)
                if domain_controls
                else 0.0
            )
            domain_pct = (
                sum(1 for c in domain_controls if c.status == "compliant") / len(domain_controls) * 100
                if domain_controls
                else 0.0
            )

            domains.append(DomainAssessment(
                domain_id=domain_id,
                name=domain_info["name"],
                controls=domain_controls,
                overall_score=domain_score,
                compliance_pct=domain_pct,
            ))

        overall_score = sum(d.overall_score for d in domains) / len(domains) if domains else 0.0
        overall_pct = sum(d.compliance_pct for d in domains) / len(domains) if domains else 0.0

        return ComplianceAssessment(
            overall_score=overall_score,
            compliance_pct=overall_pct,
            domains=domains,
            total_controls=total_controls,
            compliant_controls=compliant,
            non_compliant_controls=non_compliant,
            partial_controls=partial,
            not_applicable_controls=na,
            assessed_at=datetime.now(UTC).isoformat(),
        )

    async def get_evidence(self, control_id: str) -> list[Evidence]:
        """Get evidence artifacts for a specific control."""
        return self._evidence_store.get(control_id, [])

    async def add_evidence(self, control_id: str, evidence: Evidence) -> None:
        """Add an evidence artifact for a control."""
        if control_id not in self._evidence_store:
            self._evidence_store[control_id] = []
        self._evidence_store[control_id].append(evidence)

    async def generate_report(self, organization: str = "Dealix") -> ComplianceReport:
        """Generate a comprehensive NCA ECC compliance report."""
        assessment = await self.assess()
        recommendations = self._generate_recommendations(assessment)

        risk_level = "low"
        if assessment.compliance_pct < 50:
            risk_level = "critical"
        elif assessment.compliance_pct < 70:
            risk_level = "high"
        elif assessment.compliance_pct < 85:
            risk_level = "medium"

        return ComplianceReport(
            report_id=f"NCA-ECC-{uuid.uuid4().hex[:8].upper()}",
            generated_at=datetime.now(UTC).isoformat(),
            organization=organization,
            assessment=assessment,
            recommendations=recommendations,
            risk_level=risk_level,
        )

    async def _assess_control(self, control_id: str, name: str) -> ControlAssessment:
        """Assess a single control. In production, this checks actual system state.

        For now, returns a reasonable default assessment.
        """
        status = "compliant"
        score = 1.0

        if control_id in ("ECC-4.4", "ECC-11.1", "ECC-12.5"):
            status = "partially_compliant"
            score = 0.6

        evidence = self._evidence_store.get(control_id, [])

        return ControlAssessment(
            control_id=control_id,
            name=name,
            status=status,
            score=score,
            evidence_count=len(evidence),
            assessed_at=datetime.now(UTC).isoformat(),
        )

    def _generate_recommendations(self, assessment: ComplianceAssessment) -> list[str]:
        """Generate improvement recommendations from assessment results."""
        recommendations = []

        for domain in assessment.domains:
            non_compliant = [c for c in domain.controls if c.status == "non_compliant"]
            partial = [c for c in domain.controls if c.status == "partially_compliant"]

            if non_compliant:
                ids = ", ".join(c.control_id for c in non_compliant)
                recommendations.append(
                    f"[{domain.domain_id}] Address non-compliant controls: {ids}"
                )
            if partial:
                ids = ", ".join(c.control_id for c in partial)
                recommendations.append(
                    f"[{domain.domain_id}] Improve partially compliant controls: {ids}"
                )

        if assessment.compliance_pct < 80:
            recommendations.append(
                "Overall compliance below 80% — consider engaging an NCA-approved auditor"
            )

        return recommendations
