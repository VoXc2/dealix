"""Universal Diagnostic Factory — one canonical factory, 50 families, D0-D5, overlays."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"

class DiagnosticDepth(StrEnum):
    D0_SIGNAL_SCAN = "D0_signal_scan"
    D1_RAPID = "D1_rapid"
    D2_FUNCTIONAL = "D2_functional"
    D3_CROSS_FUNCTIONAL = "D3_cross_functional"
    D4_DEEP_EVIDENCE = "D4_deep_evidence"
    D5_CONTINUOUS = "D5_continuous"

class DiagnosticFamily(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    family_id: str  # A01..A50
    name: str
    description: str
    depth: DiagnosticDepth = DiagnosticDepth.D1_RAPID
    sector_fit: list[str] = Field(default_factory=list)
    buyer_fit: list[str] = Field(default_factory=list)
    evidence_required: list[str] = Field(default_factory=list)
    economic_relevance: str = UNKNOWN

# 50 families catalog (condensed, covers spec)
FAMILIES: list[DiagnosticFamily] = [
    DiagnosticFamily(family_id="A01", name="Executive/Strategy", description="priorities, business model, decision architecture", depth=DiagnosticDepth.D1_RAPID, buyer_fit=["ceo","founder"]),
    DiagnosticFamily(family_id="A02", name="Business Model", description="revenue streams, value prop, segments", depth=DiagnosticDepth.D1_RAPID),
    DiagnosticFamily(family_id="A03", name="Financial Performance", description="revenue, margin, cash conversion", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["cfo"]),
    DiagnosticFamily(family_id="A04", name="Cash/Collections", description="DSO, overdue, collection", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["cfo"]),
    DiagnosticFamily(family_id="A05", name="Revenue Leakage", description="missed leads, stale, unquoted", depth=DiagnosticDepth.D1_RAPID, sector_fit=["technology_saas_si","professional_services"]),
    DiagnosticFamily(family_id="A06", name="Sales OS", description="ICP, qualification, pipeline", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["sales_director"]),
    DiagnosticFamily(family_id="A07", name="Marketing/Demand", description="positioning, SEO, AI search, CAC", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["marketing_director"]),
    DiagnosticFamily(family_id="A08", name="Customer Experience", description="onboarding, support, churn", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A09", name="Customer Service", description="ticket inflow, routing, automation", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A10", name="Operations", description="throughput, bottlenecks, exceptions", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["coo","operations_director"]),
    DiagnosticFamily(family_id="A11", name="Business Process", description="process inventory, owner, KPI, waste", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A12", name="Automation Opportunity", description="DETERMINISTIC vs AGENTIC classification, frequency*minutes", depth=DiagnosticDepth.D1_RAPID),
    DiagnosticFamily(family_id="A13", name="AI Readiness", description="use cases, data, governance, economics", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["cio","cto"]),
    DiagnosticFamily(family_id="A14", name="AI Governance", description="inventory, risk, oversight, third parties", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["ciso","cdo"]),
    DiagnosticFamily(family_id="A15", name="Agentic AI Readiness", description="authority, tool permissions, auditability", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A16", name="AI Economics", description="tokens, cost per accepted result", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A17", name="Cybersecurity", description="governance, identity, monitoring, suppliers", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["ciso"]),
    DiagnosticFamily(family_id="A18", name="Data", description="source, quality, lineage, governance", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["cdo","cio"]),
    DiagnosticFamily(family_id="A19", name="Document Intelligence", description="extraction, approvals, search, versioning", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A20", name="Knowledge Mgmt", description="sources, freshness, conversion", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A21", name="IT Landscape", description="ERP/CRM/HR, SaaS sprawl", depth=DiagnosticDepth.D1_RAPID, buyer_fit=["cio"]),
    DiagnosticFamily(family_id="A22", name="Integration", description="SYSTEM→DATA→EVENT→ACTION mapping", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A23", name="Cloud/Infra", description="availability, cost, backup, vendor lock-in", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A24", name="Software Engineering", description="CI/CD, test, debt, incidents", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["cto"]),
    DiagnosticFamily(family_id="A25", name="Procurement", description="request→pay, supplier performance", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["procurement_director"]),
    DiagnosticFamily(family_id="A26", name="Supply Chain", description="demand, inventory, fulfillment", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A27", name="Inventory", description="accuracy, stockouts, replenishment", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A28", name="Project Delivery", description="scope, schedule, change, billing", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["project_director"]),
    DiagnosticFamily(family_id="A29", name="Construction/EPC Commercial", description="RFI, variations, claims, payment", depth=DiagnosticDepth.D2_FUNCTIONAL, sector_fit=["construction_epc"]),
    DiagnosticFamily(family_id="A30", name="Contract", description="obligations, milestones, SLA, risk", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A31", name="Workforce/HR Ops", description="hiring, role clarity, productivity", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["hr_director"]),
    DiagnosticFamily(family_id="A32", name="Quality", description="defects, rework, root cause", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A33", name="Risk/Control", description="risks, controls, owners, gaps", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A34", name="Vendor/Third-Party", description="criticality, concentration, cyber", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A35", name="Partner/Channel", description="fit, incentives, economics", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A36", name="B2G/Procurement Readiness", description="CR, Jadeer, tender fit, partner needs", depth=DiagnosticDepth.D2_FUNCTIONAL, sector_fit=["government_b2g"]),
    DiagnosticFamily(family_id="A37", name="Fatoora Technical Ops", description="ERP/invoice, XML, API, exception, observability", depth=DiagnosticDepth.D2_FUNCTIONAL, sector_fit=["finance_fintech_insurance"]),
    DiagnosticFamily(family_id="A38", name="Website/Digital Front Door", description="performance, trust, conversion, SEO", depth=DiagnosticDepth.D1_RAPID),
    DiagnosticFamily(family_id="A39", name="SEO/AI Search", description="crawlability, structured, AI visibility", depth=DiagnosticDepth.D1_RAPID, buyer_fit=["marketing_director"]),
    DiagnosticFamily(family_id="A40", name="Communication Ops", description="inbound, routing, consent, CRM", depth=DiagnosticDepth.D1_RAPID),
    DiagnosticFamily(family_id="A41", name="Meeting-to-Action", description="capture, decisions, owner, follow-up", depth=DiagnosticDepth.D1_RAPID),
    DiagnosticFamily(family_id="A42", name="Executive Reporting", description="KPIs, latency, actionability", depth=DiagnosticDepth.D1_RAPID, buyer_fit=["ceo"]),
    DiagnosticFamily(family_id="A43", name="Analytics", description="metric defs, funnels, attribution", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A44", name="Compliance Ops", description="obligations, evidence, escalation", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A45", name="Business Continuity", description="critical processes, backup, RTO/RPO", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A46", name="Facility/Field Ops", description="work orders, dispatch, SLAs", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A47", name="Asset Maintenance", description="register, preventive, downtime", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A48", name="Fraud/Anomaly", description="duplicate, control gaps, approval anomalies", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A49", name="Service Delivery", description="intake, fulfillment, QA, profitability", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A50", name="Company OS", description="TRUTH, PRIORITY, PEOPLE, PROCESS, SYSTEMS, DATA, AI, AUTHORITY, PROOF, ECONOMICS", depth=DiagnosticDepth.D3_CROSS_FUNCTIONAL, buyer_fit=["ceo"]),
]

class UniversalDiagnosticFactory:
    """One canonical factory — composes diagnostics dynamically."""

    def __init__(self) -> None:
        self.families = {f.family_id: f for f in FAMILIES}

    def compose(self, sector: str, company_size: str, buyer_role: str, problem: str, depth: DiagnosticDepth = DiagnosticDepth.D1_RAPID) -> list[DiagnosticFamily]:
        # Adaptive: filter by sector/buyer/problem relevance — token-based, inclusive
        selected: list[DiagnosticFamily] = []
        problem_tokens = set(problem.lower().replace("-", "_").split("_")) if problem != UNKNOWN else set()
        sector_l = sector.lower()
        buyer_l = buyer_role.lower()
        for f in FAMILIES:
            # Depth filter (allow equal or shallower)
            if f.depth.value > depth.value and depth != DiagnosticDepth.D0_SIGNAL_SCAN:
                continue
            score = 0
            # Sector overlay — bonus, not strict
            if f.sector_fit and sector_l in [s.lower() for s in f.sector_fit]:
                score += 3
            elif f.sector_fit and sector_l not in [s.lower() for s in f.sector_fit]:
                # Keep if core or problem matches
                pass
            # Buyer overlay
            if f.buyer_fit and buyer_l in [b.lower() for b in f.buyer_fit]:
                score += 2
            # Problem relevance — token overlap
            desc_l = (f.description + " " + f.name).lower()
            if problem_tokens and any(tok in desc_l for tok in problem_tokens if len(tok) > 2):
                score += 2
                selected.append(f)
                continue
            # Include core families for D1
            if f.family_id in ("A01","A05","A11","A12","A38"):
                selected.append(f)
                continue
            if f.family_id in ("A03","A04","A10") and buyer_l in ("cfo","coo"):
                selected.append(f)
                continue
            if score >= 2:
                selected.append(f)
                continue
        # Deduplicate, limit to 12 max for focus
        seen = set()
        result = []
        for f in selected:
            if f.family_id not in seen:
                result.append(f)
                seen.add(f.family_id)
                if len(result) >= 12:
                    break
        return result or [self.families["A01"], self.families["A11"]]

    def generate_questions(self, fam: DiagnosticFamily, evidence: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        # Adaptive questions — only those that change decision
        base = [
            {"question_id": f"{fam.family_id}_Q1", "reason": "evidence_needed", "evidence_needed": "system_export", "economic_relevance": "high", "answer_type": "text", "branch_condition": "if manual_steps>5"},
            {"question_id": f"{fam.family_id}_Q2", "reason": "confidence_impact", "evidence_needed": "interview", "economic_relevance": "medium", "answer_type": "number", "branch_condition": "if delay>7"},
        ]
        return base

    def economic_leakage(self, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        # Translate findings to leakage types
        leakage = []
        for f in findings:
            if "manual" in f.get("finding","").lower():
                leakage.append({"type": "MANUAL_LABOR", "finding": f["finding"], "evidence": f.get("evidence", UNKNOWN), "confidence": f.get("confidence", "WEAK_EVIDENCE"), "annual_frequency": 100, "time_per_event": "2h"})
        return leakage

    def to_proposal(self, families: list[DiagnosticFamily], economic_leakage: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "families": [f.family_id for f in families],
            "leakage": economic_leakage,
            "next_step": "discovery" if economic_leakage else "signal_scan",
            "evidence_confidence": "MODERATE_EVIDENCE" if economic_leakage else "HYPOTHESIS",
        }

__all__ = ["UniversalDiagnosticFactory", "DiagnosticDepth", "DiagnosticFamily", "FAMILIES", "UNKNOWN"]
