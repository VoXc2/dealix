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
SELLABLE_RULES_PATH = ROOT / "governance/sellable_rules.json"
KPI_TREE_PATH = ROOT / "kpis/kpi_tree.json"
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


def load_sellable_rules() -> dict[str, Any]:
    return load_json(SELLABLE_RULES_PATH)


def load_kpi_tree() -> dict[str, Any]:
    return load_json(KPI_TREE_PATH)


def load_risk_register() -> dict[str, Any]:
    return load_json(RISK_REGISTER_PATH)


def load_playbook_catalog() -> dict[str, Any]:
    return load_json(PLAYBOOK_CATALOG_PATH)
