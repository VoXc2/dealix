from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "apps" / "web" / "app" / "book" / "page.tsx"
ENV_EXAMPLE = ROOT / "apps" / "web" / ".env.example"
PUBLIC_INTAKE = ROOT / "api" / "routers" / "public_intake.py"
ORCHESTRATOR = ROOT / "auto_client_acquisition" / "diagnostic_intake_orchestrator.py"


def test_book_page_submits_to_canonical_execution_diagnostic_endpoint():
    text = BOOK.read_text(encoding="utf-8")
    assert 'fetch("/api/v1/public/execution-diagnostic"' in text
    assert "workflow" in text
    assert "decision_owner" in text
    assert "tools_data" in text
    assert "business_impact" in text
    assert "proof_metric" in text
    assert "baseline" in text
    assert "target_outcome" in text
    assert "followup_requested" in text
    assert "لا يتم اعتبار المشكلة أو العائد أو Proof مثبتًا" in text


def test_diagnostic_followup_is_explicit_and_fail_closed_by_default():
    page = BOOK.read_text(encoding="utf-8")
    public_text = PUBLIC_INTAKE.read_text(encoding="utf-8")

    assert 'name="followup_requested"' in page
    assert "defaultChecked" not in page
    assert "followup_requested: bool = False" in public_text
    assert '"marketing_consent": False' in public_text
    assert '"customer_proof_consent": False' in public_text


def test_founder_public_contact_is_explicit_and_environment_overrideable():
    page = BOOK.read_text(encoding="utf-8")
    env = ENV_EXAMPLE.read_text(encoding="utf-8")

    assert "NEXT_PUBLIC_FOUNDER_EMAIL" in page
    assert "NEXT_PUBLIC_FOUNDER_PHONE" in page
    assert "NEXT_PUBLIC_WHATSAPP_URL" in page
    assert '"+966 59 778 8539"' in page
    assert "NEXT_PUBLIC_FOUNDER_EMAIL=sami.assiri11@gmail.com" in env
    assert "NEXT_PUBLIC_FOUNDER_PHONE=+966597788539" in env
    assert "NEXT_PUBLIC_WHATSAPP_URL=" in env


def test_public_intake_creates_internal_agent_handoff_without_material_authority():
    public_text = PUBLIC_INTAKE.read_text(encoding="utf-8")
    orchestration_text = ORCHESTRATOR.read_text(encoding="utf-8")

    assert '@router.post("/execution-diagnostic")' in public_text
    assert "build_agent_handoff" in public_text
    assert "mirror_to_revenue_autopilot" in public_text
    assert '"marketing_consent": False' in public_text
    assert '"customer_proof_consent": False' in public_text
    assert '"external_action": "none"' in public_text

    for agent in (
        "dealix-pm",
        "dealix-sales",
        "dealix-delivery",
        "dealix-engineer",
        "dealix-content",
    ):
        assert agent in orchestration_text

    for boundary in (
        '"external_send": False',
        '"public_publish": False',
        '"paid_spend": False',
        '"payment_execution": False',
        '"production_mutation": False',
        '"binding_commercial_commitment": False',
    ):
        assert boundary in orchestration_text
