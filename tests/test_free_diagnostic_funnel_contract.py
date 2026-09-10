"""Contracts for the public free-first commercial funnel."""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from auto_client_acquisition.service_catalog.registry import list_offerings

ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC_HTML = ROOT / "landing" / "diagnostic.html"
PUBLIC_ROUTER = ROOT / "api" / "routers" / "public.py"
GROWTH_ENGINE = (
    ROOT / "auto_client_acquisition" / "company_growth_beast" / "engine.py"
)
LANDING_SCRIPT = ROOT / "landing" / "script.js"


def _load_public_intake_helpers() -> dict[str, Any]:
    tree = ast.parse(PUBLIC_ROUTER.read_text(encoding="utf-8"))
    wanted = {"_is_free_diagnostic_source", "_intake_response"}
    definitions = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name in wanted
    ]
    assert {node.name for node in definitions} == wanted
    namespace: dict[str, Any] = {
        "Any": Any,
        "CALENDLY_URL": "https://calendar.example.test/booking",
    }
    exec(compile(ast.Module(body=definitions, type_ignores=[]), str(PUBLIC_ROUTER), "exec"), namespace)
    return namespace


def test_service_catalog_starts_with_free_diagnostic() -> None:
    offerings = list_offerings()
    free = offerings[0]
    assert free.id == "free_mini_diagnostic"
    assert free.price_sar == 0
    assert free.customer_journey_stage == "discovery"
    assert set(free.action_modes_used) <= {"suggest_only", "draft_only"}
    assert {"no_live_send", "no_live_charge"} <= set(free.hard_gates)
    assert "no payment" in free.refund_policy_en.lower()


def test_diagnostic_page_has_no_paid_or_qualification_shortcut() -> None:
    html = DIAGNOSTIC_HTML.read_text(encoding="utf-8")
    forbidden = (
        "/start.html",
        "/checkout",
        "499",
        "service-setup/qualify",
        "7_day_proof_sprint",
        "calendly",
    )
    assert not [fragment for fragment in forbidden if fragment.lower() in html.lower()]
    assert "free_mini_diagnostic" in html
    assert "NO_PII_CAPTURE" in html
    assert "NO_LEAD_PERSISTENCE" in html
    assert "HUMAN_REVIEW_REQUIRED" in html


def test_diagnostic_page_separates_honeypot_and_company_url() -> None:
    html = DIAGNOSTIC_HTML.read_text(encoding="utf-8")
    assert html.count('name="website"') == 1
    assert html.count('name="company_url"') == 1
    assert 'type="url" name="company_url"' in html
    assert "form.elements.namedItem('website')" in html


def test_free_intake_never_auto_books_charges_or_sends() -> None:
    helpers = _load_public_intake_helpers()
    response = helpers["_intake_response"](
        source="landing/diagnostic",
        lead_id="lead_test",
        transactional_status="sent",
    )
    assert response["calendly_url"] is None
    assert response["funnel_stage"] == "free_diagnostic"
    assert response["next_step"] == "human_review"
    assert response["payment_required"] is False
    assert response["external_action_allowed"] is False


def test_non_diagnostic_intake_retains_only_optional_booking() -> None:
    helpers = _load_public_intake_helpers()
    response = helpers["_intake_response"](
        source="landing.demo_form",
        lead_id=None,
        transactional_status="not_configured",
    )
    assert response["funnel_stage"] == "demo_request"
    assert response["next_step"] == "optional_booking"
    assert response["payment_required"] is False
    assert response["external_action_allowed"] is False


def test_growth_diagnostic_source_is_preliminary_and_approval_gated() -> None:
    source = GROWTH_ENGINE.read_text(encoding="utf-8")
    required = (
        '"status": "preliminary_free_mini_diagnostic"',
        '"requires_human_review": True',
        '"requires_source_validation": True',
        '"payment_required": False',
        '"external_action_allowed": False',
        '"next_step": "human_review_then_qualified_discovery_if_evidence_supports_fit"',
    )
    assert not [fragment for fragment in required if fragment not in source]


def test_landing_script_restricts_external_prospect_links() -> None:
    source = LANDING_SCRIPT.read_text(encoding="utf-8")
    assert "function safeHttpUrl" in source
    assert "url.protocol === 'http:' || url.protocol === 'https:'" in source
    assert 'rel="noopener noreferrer"' in source
    assert "طلب فحص مجاني Dealix" in source
    assert "dealix-api.up.railway.app" not in source
