"""Catalog and file loaders for Saudi AI provider CLI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent

CATALOG_PATH = ROOT / "dealix/catalogs/saudi_ai_service_catalog_v2.json"
PRICING_MODEL_PATH = ROOT / "pricing/pricing_model.json"
SEGMENT_RULES_PATH = ROOT / "pricing/segment_rules.json"
DISCOUNT_POLICY_PATH = ROOT / "pricing/discount_policy.json"
MARGIN_GUARDRAILS_PATH = ROOT / "pricing/margin_guardrails.json"
PACKAGING_MATRIX_PATH = ROOT / "pricing/packaging_matrix.json"
ROI_FORMULAS_PATH = ROOT / "pricing/roi_formulas.json"
SLA_MATRIX_PATH = ROOT / "pricing/sla_matrix.json"
MONETIZATION_STRATEGY_PATH = ROOT / "pricing/monetization_strategy.json"
SELLABLE_RULES_PATH = ROOT / "governance/sellable_rules.json"
DEPLOYMENT_RULES_PATH = ROOT / "governance/deployment_rules.json"
COMPLIANCE_RULES_PATH = ROOT / "governance/compliance_rules.json"
AUDIT_RULES_PATH = ROOT / "governance/audit_rules.json"
ESCALATION_MATRIX_PATH = ROOT / "governance/escalation_matrix.json"
KPI_TREE_PATH = ROOT / "kpis/kpi_tree.json"
NORTH_STAR_METRICS_PATH = ROOT / "kpis/north_star_metrics.json"
OPERATIONAL_METRICS_PATH = ROOT / "kpis/operational_metrics.json"
EXECUTIVE_METRICS_PATH = ROOT / "kpis/executive_metrics.json"
GUARDRAIL_METRICS_PATH = ROOT / "kpis/guardrails.json"
BENCHMARK_TARGETS_PATH = ROOT / "kpis/benchmark_targets.json"
RISK_REGISTER_PATH = ROOT / "risk/risk_register.json"
PLAYBOOK_CATALOG_PATH = ROOT / "playbooks/playbook_catalog.json"

TEMPLATES_DIR = ROOT / "templates"
OFFERS_OUT_DIR = ROOT / "out/offers"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_service_catalog() -> dict[str, Any]:
    return load_json(CATALOG_PATH)


def load_pricing_model() -> dict[str, Any]:
    return load_json(PRICING_MODEL_PATH)


def load_segment_rules() -> dict[str, Any]:
    return load_json(SEGMENT_RULES_PATH)


def load_discount_policy() -> dict[str, Any]:
    return load_json(DISCOUNT_POLICY_PATH)


def load_margin_guardrails() -> dict[str, Any]:
    return load_json(MARGIN_GUARDRAILS_PATH)


def load_packaging_matrix() -> dict[str, Any]:
    return load_json(PACKAGING_MATRIX_PATH)


def load_roi_formulas() -> dict[str, Any]:
    return load_json(ROI_FORMULAS_PATH)


def load_sla_matrix() -> dict[str, Any]:
    return load_json(SLA_MATRIX_PATH)


def load_monetization_strategy() -> dict[str, Any]:
    return load_json(MONETIZATION_STRATEGY_PATH)


def load_sellable_rules() -> dict[str, Any]:
    return load_json(SELLABLE_RULES_PATH)


def load_deployment_rules() -> dict[str, Any]:
    return load_json(DEPLOYMENT_RULES_PATH)


def load_compliance_rules() -> dict[str, Any]:
    return load_json(COMPLIANCE_RULES_PATH)


def load_audit_rules() -> dict[str, Any]:
    return load_json(AUDIT_RULES_PATH)


def load_escalation_matrix() -> dict[str, Any]:
    return load_json(ESCALATION_MATRIX_PATH)


def load_kpi_tree() -> dict[str, Any]:
    return load_json(KPI_TREE_PATH)


def load_north_star_metrics() -> dict[str, Any]:
    return load_json(NORTH_STAR_METRICS_PATH)


def load_operational_metrics() -> dict[str, Any]:
    return load_json(OPERATIONAL_METRICS_PATH)


def load_executive_metrics() -> dict[str, Any]:
    return load_json(EXECUTIVE_METRICS_PATH)


def load_guardrail_metrics() -> dict[str, Any]:
    return load_json(GUARDRAIL_METRICS_PATH)


def load_benchmark_targets() -> dict[str, Any]:
    return load_json(BENCHMARK_TARGETS_PATH)


def load_risk_register() -> dict[str, Any]:
    return load_json(RISK_REGISTER_PATH)


def load_playbook_catalog() -> dict[str, Any]:
    return load_json(PLAYBOOK_CATALOG_PATH)
