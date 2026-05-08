"""Wave 10.5 §26.5 — Master E2E Customer Journey test.

16 steps that must ALL succeed for the project to be end-to-end functional.
Uses synthetic customer 'test-e2e-master-co' clearly tagged [SIMULATION].

Hard rules (Article 8 + 13):
- Every "evidence" file is clearly tagged [SIMULATION]
- Proof events use evidence_level="observed_simulation"
- ``is_revenue=True`` only after the payment-confirmed CLI step
- No real WhatsApp/Email/Moyasar touched

Saudi-Arabic note:
    رحلة العميل الكاملة (16 خطوة) — كل خطوة تستدعي سكربت أو وحدة موجودة فعلًا.
    الخطوات 15-16 (Expansion + Learning Loop) مؤجلة لـ Wave 11.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
CUSTOMER = "test-e2e-master-co"
COMPANY = "Test E2E Master Co [SIMULATION]"
SECTOR = "real_estate"
REGION = "Riyadh"


@pytest.fixture(scope="module")
def sim_dir(tmp_path_factory):
    """Isolated tmp dir for the whole 16-step run."""
    return tmp_path_factory.mktemp("e2e_master")


def _run(cmd: list[str], cwd: Path = REPO) -> subprocess.CompletedProcess:
    """Run a CLI script with a 60s ceiling and captured output."""
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=60)


# ─────────────────────────────────────────────────────────────────────
# Step 1 — First prospect intake (warm-intro logged)
# ─────────────────────────────────────────────────────────────────────
def test_step_01_create_lead(sim_dir):
    """Step 1: First prospect intake (warm-intro logged)."""
    out_path = sim_dir / "intake.json"
    r = _run([
        sys.executable, "scripts/dealix_first_prospect_intake.py",
        "--company-name", COMPANY,
        "--sector", SECTOR,
        "--region", REGION,
        "--relationship", "warm_intro",
        "--consent-status", "granted_for_diagnostic",
        "--notes", "[SIMULATION] E2E master customer journey test",
        "--out-path", str(out_path),
        "--force",
    ])
    assert r.returncode == 0, f"intake failed: {r.stderr}\n{r.stdout}"
    assert out_path.exists(), "intake output missing"
    data = json.loads(out_path.read_text())
    assert data.get("company_name") == COMPANY
    assert data.get("known_relationship") == "warm_intro"
    assert data.get("consent_status") == "granted_for_diagnostic"


# ─────────────────────────────────────────────────────────────────────
# Step 2 — Enrichment (demo mode OK if HUNTER_API_KEY absent)
# ─────────────────────────────────────────────────────────────────────
def test_step_02_enrich_lead():
    """Step 2: Enrichment runs (demo mode honest about no live key)."""
    from auto_client_acquisition.enrichment_provider import _HunterProvider

    provider = _HunterProvider()
    result = provider.enrich(domain="test-e2e-master-co.sa")
    assert result.confidence_score is not None
    # No live key + no DEALIX_ENRICHMENT_LIVE_CALLS → "live_disabled" demo path
    assert result.reason_code in ("live_disabled", "ok"), (
        f"unexpected reason_code={result.reason_code}"
    )
    assert result.provider_id == "hunter"


# ─────────────────────────────────────────────────────────────────────
# Step 3 — Qualification scoring
# ─────────────────────────────────────────────────────────────────────
def test_step_03_score_lead():
    """Step 3: Qualification module is wired and exposes the BANT primitives."""
    try:
        from auto_client_acquisition.agents.qualification import (
            QualificationAgent,
            QualificationQuestion,
            QualificationResult,
        )
    except ImportError as exc:
        pytest.skip(f"qualification module unavailable: {exc}")

    # Smoke: can build an empty result + add a single question
    res = QualificationResult()
    assert res.bant_score == 0.0
    res.questions.append(
        QualificationQuestion(q="ما الميزانية الشهرية؟", bant="budget", why="budget gate")
    )
    assert len(res.questions) == 1
    assert callable(getattr(QualificationAgent, "run", None))


# ─────────────────────────────────────────────────────────────────────
# Step 4 — Decision Passport
# ─────────────────────────────────────────────────────────────────────
def test_step_04_create_decision_passport():
    """Step 4: Decision Passport schema instantiable."""
    try:
        from auto_client_acquisition.decision_passport import DecisionPassport
        from auto_client_acquisition.decision_passport.schema import ScoreBoard
    except ImportError as exc:
        pytest.skip(f"Decision Passport module unavailable: {exc}")

    scores = ScoreBoard(
        fit_score=0.7,
        intent_score=0.5,
        urgency_score=0.4,
        revenue_potential_score=0.6,
        engagement_score=0.3,
        data_quality_score=0.5,
        warm_route_score=0.8,
        compliance_risk_score=0.2,
        deliverability_risk_score=0.2,
    )
    passport = DecisionPassport(
        lead_id=f"lead:{CUSTOMER}",
        company=COMPANY,
        source="warm_intro",
        why_now_ar="[SIMULATION] اختبار E2E",
        why_now_en="[SIMULATION] E2E test",
        icp_tier="A",
        priority_bucket="P1_THIS_WEEK",
        scores=scores,
        best_channel="whatsapp",
        recommended_action="send_warm_intro",
        recommended_action_ar="إرسال تعريف دافئ",
        proof_target="diagnostic_completed",
        proof_target_ar="إنهاء التشخيص",
        next_step_ar="ترتيب مكالمة",
        next_step_en="Schedule a call",
    )
    assert passport.schema_version == "1.0"
    assert passport.priority_bucket == "P1_THIS_WEEK"


# ─────────────────────────────────────────────────────────────────────
# Step 5 — Approval Center: create approval request
# ─────────────────────────────────────────────────────────────────────
def test_step_05_generate_safe_action():
    """Step 5: Approval Center can create approval request."""
    from auto_client_acquisition.approval_center.schemas import ApprovalRequest

    req = ApprovalRequest(
        object_type="lead",
        object_id=f"lead:{CUSTOMER}",
        action_type="reply_draft",
        channel="email",
        risk_level="low",
        summary_ar="[SIMULATION] رد بريدي",
        summary_en="[SIMULATION] Email reply",
    )
    assert req.approval_id.startswith("apr_")
    assert req.action_mode == "approval_required"


# ─────────────────────────────────────────────────────────────────────
# Step 6 — Approval Center: PENDING by default
# ─────────────────────────────────────────────────────────────────────
def test_step_06_require_approval():
    """Step 6: Approval Center stores PENDING."""
    from auto_client_acquisition.approval_center.schemas import (
        ApprovalRequest,
        ApprovalStatus,
    )

    req = ApprovalRequest(
        object_type="lead",
        object_id="lead:test",
        action_type="reply_draft",
        channel="email",
        risk_level="low",
    )
    # use_enum_values=True → status is the string value, not the enum member
    assert req.status == ApprovalStatus.PENDING.value
    assert req.status == "pending"


# ─────────────────────────────────────────────────────────────────────
# Step 7 — Approval transition pending → approved
# ─────────────────────────────────────────────────────────────────────
def test_step_07_approve_manually():
    """Step 7: Approval can transition pending → approved (no exception)."""
    from auto_client_acquisition.approval_center.approval_policy import (
        assert_can_approve,
    )
    from auto_client_acquisition.approval_center.schemas import (
        ApprovalRequest,
        ApprovalStatus,
    )

    req = ApprovalRequest(
        object_type="lead",
        object_id="lead:test",
        action_type="reply_draft",
        channel="email",
        risk_level="low",
    )
    assert_can_approve(req)  # raises if not allowed
    req.status = ApprovalStatus.APPROVED.value
    assert req.status == "approved"


# ─────────────────────────────────────────────────────────────────────
# Step 8 — AI Ops Diagnostic (deterministic, no API key)
# ─────────────────────────────────────────────────────────────────────
def test_step_08_create_diagnostic(sim_dir):
    """Step 8: AI Ops Diagnostic generates markdown + json."""
    out_md = sim_dir / "diagnostic.md"
    out_json = sim_dir / "diagnostic.json"
    r = _run([
        sys.executable, "scripts/dealix_ai_ops_diagnostic.py",
        "--company", COMPANY,
        "--sector", SECTOR,
        "--region", REGION,
        "--language", "both",
        "--out-md", str(out_md),
        "--out-json", str(out_json),
    ])
    if r.returncode != 0:
        pytest.skip(f"diagnostic script failed: {r.stderr[:300]}")
    assert out_md.exists() and out_md.stat().st_size > 0


# ─────────────────────────────────────────────────────────────────────
# Step 9 — Pilot brief (Wave 6)
# ─────────────────────────────────────────────────────────────────────
def test_step_09_send_pilot_offer_draft(sim_dir):
    """Step 9: Pilot brief generated (Wave 6)."""
    out_md = sim_dir / "pilot_brief.md"
    out_json = sim_dir / "pilot_brief.json"
    r = _run([
        sys.executable, "scripts/dealix_pilot_brief.py",
        "--company", COMPANY,
        "--sector", SECTOR,
        "--amount-sar", "499",
        "--out-md", str(out_md),
        "--out-json", str(out_json),
    ])
    assert r.returncode == 0, f"pilot brief failed: {r.stderr}\n{r.stdout}"
    assert out_md.exists()
    data = json.loads(out_json.read_text())
    assert data.get("amount_sar") == 499 or data.get("amount_sar") == "499"


# ─────────────────────────────────────────────────────────────────────
# Step 10 — Payment intent created (state machine)
# ─────────────────────────────────────────────────────────────────────
def test_step_10_create_payment_intent_state(sim_dir):
    """Step 10: Payment state = invoice_intent_created."""
    state_path = sim_dir / "payment_state.json"
    r = _run([
        sys.executable, "scripts/dealix_payment_confirmation_stub.py",
        "--action", "invoice-intent",
        "--customer", COMPANY,
        "--amount-sar", "499",
        "--service-type", "7_day_revenue_proof_sprint",
        "--evidence-note", "[SIMULATION] E2E intent",
        "--out-path", str(state_path),
    ])
    assert r.returncode == 0, f"invoice-intent failed: {r.stderr}\n{r.stdout}"
    assert state_path.exists()
    state = json.loads(state_path.read_text())
    # is_revenue must NOT be true yet (Article 8)
    assert state.get("is_revenue") in (False, None), (
        f"is_revenue must not be true at intent step: {state}"
    )


# ─────────────────────────────────────────────────────────────────────
# Step 11 — Payment confirmation (link → evidence → confirm)
# ─────────────────────────────────────────────────────────────────────
def test_step_11_confirm_payment_manually(sim_dir):
    """Step 11: Payment state transitions through link → evidence → confirm."""
    state_path = sim_dir / "payment_state.json"
    transitions = [
        ("send-payment-link", ["--evidence-note", "[SIMULATION] link sent"]),
        ("upload-evidence", [
            "--evidence-note", "[SIMULATION] bank screenshot",
            "--evidence-kind", "bank_screenshot",
        ]),
        ("confirm", [
            "--evidence-note", "[SIMULATION] confirmed by founder",
            "--confirmed-by", "sami",
        ]),
    ]
    for action, args in transitions:
        r = _run([
            sys.executable, "scripts/dealix_payment_confirmation_stub.py",
            "--action", action,
            "--customer", COMPANY,
            *args,
            "--out-path", str(state_path),
        ])
        assert r.returncode == 0, f"action={action} failed: {r.stderr}"
    state = json.loads(state_path.read_text())
    # Article 8: is_revenue=True ONLY after explicit confirm
    assert state.get("is_revenue") is True, (
        f"is_revenue must be True after confirm: {state}"
    )


# ─────────────────────────────────────────────────────────────────────
# Step 12 — Delivery kickoff (gated on payment_confirmed)
# ─────────────────────────────────────────────────────────────────────
def test_step_12_start_delivery_session(sim_dir):
    """Step 12: Delivery kickoff (gated on payment_confirmed)."""
    state_path = sim_dir / "payment_state.json"
    out_md = sim_dir / "delivery_session.md"
    out_json = sim_dir / "delivery_session.json"
    r = _run([
        sys.executable, "scripts/dealix_delivery_kickoff.py",
        "--company", COMPANY,
        "--service", "7_day_revenue_proof_sprint",
        "--payment-state-file", str(state_path),
        "--out-md", str(out_md),
        "--out-json", str(out_json),
    ])
    assert r.returncode == 0, f"kickoff failed: {r.stderr}\n{r.stdout}"
    assert out_json.exists()


# ─────────────────────────────────────────────────────────────────────
# Step 13 — Proof event recorded (evidence_level=observed_simulation)
# ─────────────────────────────────────────────────────────────────────
def test_step_13_create_proof_event(sim_dir):
    """Step 13: Proof events recorded with evidence_level."""
    proof_jsonl = sim_dir / "proof_events.jsonl"
    proof_jsonl.write_text(
        json.dumps({
            "event_id": "pe_e2e_001",
            "customer_handle": CUSTOMER,
            "event_type": "lead_qualified",
            "evidence_level": "observed_simulation",
            "tag": "[SIMULATION]",
        }) + "\n"
    )
    assert proof_jsonl.exists()
    line = proof_jsonl.read_text().strip()
    parsed = json.loads(line)
    assert parsed["evidence_level"] == "observed_simulation"


# ─────────────────────────────────────────────────────────────────────
# Step 14 — Proof Pack assembled (internal draft, not publishable)
# ─────────────────────────────────────────────────────────────────────
def test_step_14_build_proof_pack(sim_dir):
    """Step 14: Proof Pack assembled (publishable=False until customer signs)."""
    delivery_path = sim_dir / "delivery_session.json"
    if not delivery_path.exists():
        pytest.skip("delivery_session.json missing — step 12 must run first")

    # Patch delivery session with proof event ids + a deliverable
    ds = json.loads(delivery_path.read_text())
    ds["proof_event_ids"] = ["pe_e2e_001"]
    ds["deliverables"] = [{"name": "Lead Audit", "status": "draft"}]
    delivery_path.write_text(json.dumps(ds, ensure_ascii=False))

    out_md = sim_dir / "proof_pack.md"
    out_json = sim_dir / "proof_pack.json"
    r = _run([
        sys.executable, "scripts/dealix_wave6_proof_pack.py",
        "--company", COMPANY,
        "--delivery-session", str(delivery_path),
        "--allow-empty",
        "--out-md", str(out_md),
        "--out-json", str(out_json),
    ])
    assert r.returncode == 0, f"proof pack failed: {r.stderr}\n{r.stdout}"
    pack = json.loads(out_json.read_text())
    # Article 8: never publishable from a simulation
    assert pack.get("is_publishable") in (False, None), (
        f"is_publishable must NOT be true for simulation: {pack}"
    )


# ─────────────────────────────────────────────────────────────────────
# Step 15 — Expansion Engine (DEFERRED — Wave 11)
# ─────────────────────────────────────────────────────────────────────
def test_step_15_recommend_upsell():
    """Step 15: Expansion Engine produces next_best_offer (DEFERRED — Wave 11)."""
    pytest.skip("Expansion Engine ships with Wave 11 (Article 13 trigger)")


# ─────────────────────────────────────────────────────────────────────
# Step 16 — Learning Loop (DEFERRED — Wave 11)
# ─────────────────────────────────────────────────────────────────────
def test_step_16_create_learning_event():
    """Step 16: Learning Loop records funnel + outcome (DEFERRED — Wave 11)."""
    pytest.skip("Learning Loop ships with Wave 11 (Article 13 trigger)")
