"""Tests for v5 layers part 4 (final): proof_ledger + gtm_os + security_privacy."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.gtm_os import (
    build_weekly_calendar,
    draft_experiment,
)
from auto_client_acquisition.gtm_os.message_experiment import (
    ExperimentStatus,
)
from auto_client_acquisition.proof_ledger import (
    FileProofLedger,
    ProofEvent,
    ProofEventType,
    RevenueWorkUnit,
    RevenueWorkUnitType,
    export_for_audit,
    export_redacted,
)
from auto_client_acquisition.security_privacy import (
    data_minimization_for,
    list_known_object_types,
    redact_log_entry,
    scan_text_for_secrets,
)


# ════════════════════ proof_ledger ════════════════════


@pytest.fixture
def tmp_ledger(tmp_path: Path) -> FileProofLedger:
    return FileProofLedger(base_dir=tmp_path)


def test_record_event_persists_to_file(tmp_ledger: FileProofLedger):
    ev = ProofEvent(
        event_type=ProofEventType.PILOT_OFFERED,
        customer_handle="ACME-001",
        service_id="growth_starter",
        summary_ar="عرض pilot 499 ريال",
        summary_en="Offered pilot at 499 SAR",
    )
    stored = tmp_ledger.record(ev)
    rows = tmp_ledger.list_events(customer_handle="ACME-001")
    assert any(r.id == stored.id for r in rows)


def test_record_event_redacts_pii_in_summaries(tmp_ledger: FileProofLedger):
    ev = ProofEvent(
        event_type=ProofEventType.LEAD_INTAKE,
        customer_handle="cust-pii-test",
        summary_ar="وصلت رسالة من ahmad@example.sa جوال 0501234567",
        summary_en="Reached out via ahmad@example.sa phone 0501234567",
    )
    stored = tmp_ledger.record(ev)
    # On-disk version (the stored copy) carries redacted_*.
    assert "ahmad@example.sa" not in stored.redacted_summary_ar
    assert "0501234567" not in stored.redacted_summary_ar
    assert "ahmad@example.sa" not in stored.redacted_summary_en


def test_filter_events_by_customer_and_type(tmp_ledger: FileProofLedger):
    tmp_ledger.record(ProofEvent(
        event_type=ProofEventType.PILOT_OFFERED,
        customer_handle="A",
    ))
    tmp_ledger.record(ProofEvent(
        event_type=ProofEventType.DIAGNOSTIC_DELIVERED,
        customer_handle="A",
    ))
    tmp_ledger.record(ProofEvent(
        event_type=ProofEventType.PILOT_OFFERED,
        customer_handle="B",
    ))
    pilots_a = tmp_ledger.list_events(
        customer_handle="A", event_type="pilot_offered",
    )
    assert len(pilots_a) == 1
    assert pilots_a[0].customer_handle == "A"


def test_record_unit(tmp_ledger: FileProofLedger):
    u = RevenueWorkUnit(
        unit_type=RevenueWorkUnitType.PROOF_PACK_ASSEMBLED,
        customer_handle="ACME",
        quantity=1,
    )
    stored = tmp_ledger.record_unit(u)
    units = tmp_ledger.list_units()
    assert any(x.id == stored.id for x in units)


def test_export_redacted_strips_handle_without_consent(tmp_ledger: FileProofLedger):
    tmp_ledger.record(ProofEvent(
        event_type=ProofEventType.PILOT_OFFERED,
        customer_handle="REAL-CUSTOMER-NAME",
        consent_for_publication=False,
    ))
    out = export_redacted(ledger=tmp_ledger)
    text = str(out)
    assert "REAL-CUSTOMER-NAME" not in text


def test_export_redacted_keeps_handle_with_consent(tmp_ledger: FileProofLedger):
    tmp_ledger.record(ProofEvent(
        event_type=ProofEventType.PILOT_OFFERED,
        customer_handle="PUBLIC-OK",
        consent_for_publication=True,
    ))
    out = export_redacted(ledger=tmp_ledger)
    assert any(
        e.get("customer_handle") == "PUBLIC-OK"
        for e in out["events"]
    )


def test_export_for_audit_returns_redacted_pack(tmp_ledger: FileProofLedger):
    tmp_ledger.record(ProofEvent(
        event_type=ProofEventType.LEAD_INTAKE,
        customer_handle="X",
        summary_ar="بريد x@y.sa جوال 0501112233",
    ))
    out = export_for_audit(ledger=tmp_ledger)
    assert out["events_count"] >= 1
    text = str(out)
    assert "x@y.sa" not in text
    assert "0501112233" not in text


def test_proof_event_default_approval_status_is_approval_required():
    ev = ProofEvent(event_type=ProofEventType.PILOT_OFFERED)
    assert ev.approval_status == "approval_required"


# ════════════════════ gtm_os ════════════════════


def test_content_calendar_returns_slots():
    cal = build_weekly_calendar(slots_per_week=3)
    assert cal["slots_total"] >= 1
    for slot in cal["slots"]:
        assert slot["approval_status"] == "approval_required"
        assert slot["channel"] in {
            "landing_page", "linkedin_manual_post",
            "x_manual_post", "email_draft",
        }
    assert cal["guardrails"]["no_auto_publish"] is True


def test_content_calendar_anchors_to_real_signal():
    cal = build_weekly_calendar(slots_per_week=2)
    if cal["slots"]:
        # Each slot's rationale must mention "GEO/AIO" or "lowest-scoring"
        for slot in cal["slots"]:
            assert "GEO" in slot["rationale"] or "lowest" in slot["rationale"].lower()


def test_draft_experiment_safe_text_passes():
    exp = draft_experiment(
        name="founder vs partner intro",
        hypothesis_ar="مقدّمة المؤسس تتفوّق على مقدّمة الشريك",
        hypothesis_en="Founder intro outperforms partner intro",
        variant_a_ar="السلام عليكم، شفت شغلكم...",
        variant_a_en="Hi, saw your work...",
        variant_b_ar="مرحباً، شريك مشترك ينصح بكم...",
        variant_b_en="Hi, mutual partner recommended you...",
        success_metric="reply_rate",
        target_audience="saudi_b2b_agencies",
    )
    assert exp.status == ExperimentStatus.DRAFT.value
    assert exp.safe_publishing_check["all_safe"] is True


def test_draft_experiment_blocked_on_forbidden_vocabulary():
    exp = draft_experiment(
        name="bad",
        hypothesis_ar="نضمن إيراد مضمون",  # forbidden
        hypothesis_en="we guarantee revenue",  # forbidden
        variant_a_ar="x",
        variant_a_en="x",
        variant_b_ar="y",
        variant_b_en="y",
        success_metric="x",
        target_audience="x",
    )
    # The hypothesis fields are NOT gate-checked (intentional — they're
    # internal). Only the variants are. Variants are safe → status DRAFT.
    # But if we put forbidden vocab in variants...
    bad_exp = draft_experiment(
        name="bad-variant",
        hypothesis_ar="x", hypothesis_en="x",
        variant_a_ar="نضمن لكم نتائج",  # forbidden
        variant_a_en="we guarantee results",  # forbidden
        variant_b_ar="x", variant_b_en="x",
        success_metric="x", target_audience="x",
    )
    assert bad_exp.status == ExperimentStatus.BLOCKED.value
    assert bad_exp.safe_publishing_check["all_safe"] is False


def test_message_experiment_lists_forbidden_channels():
    exp = draft_experiment(
        name="x",
        hypothesis_ar="x", hypothesis_en="x",
        variant_a_ar="مرحباً", variant_a_en="hi",
        variant_b_ar="السلام عليكم", variant_b_en="hello",
        success_metric="x", target_audience="x",
    )
    forbidden = exp.forbidden_channels
    assert "cold_whatsapp" in forbidden
    assert "linkedin_automation" in forbidden
    assert "purchased_lists" in forbidden


# ════════════════════ security_privacy ════════════════════


def test_secret_scan_finds_moyasar_live_key():
    # Build from parts to avoid GitHub secret-scanning push-protection.
    test_key = "sk_" + "live" + "_" + "abcdefghijklmnop"
    findings = scan_text_for_secrets(f"MOYASAR_SECRET_KEY={test_key}")
    assert findings
    assert findings[0].pattern_id == "moyasar_live_secret"
    # Output must NOT contain the raw key
    assert "abcdefghijklmnop" not in findings[0].excerpt_redacted


def test_secret_scan_finds_anthropic_key():
    findings = scan_text_for_secrets(
        "ANTHROPIC_API_KEY=sk-ant-api03-abc-de-fg-hijklmnop_qrstuvwxyz12"
    )
    pattern_ids = {f.pattern_id for f in findings}
    assert "anthropic_key" in pattern_ids


def test_secret_scan_finds_aws_access_key():
    findings = scan_text_for_secrets("AWS_ACCESS_KEY=AKIA0123456789ABCDEF")
    pattern_ids = {f.pattern_id for f in findings}
    assert "aws_access_key" in pattern_ids


def test_secret_scan_redacts_match_in_excerpt():
    # Build the test string from parts so GitHub push-protection
    # doesn't flag this test fixture as a real Stripe-style key.
    raw_secret = "sk_" + "live" + "_" + ("Z" * 24)
    findings = scan_text_for_secrets(f"key={raw_secret}")
    assert findings
    assert raw_secret not in findings[0].excerpt_redacted


def test_secret_scan_clean_text_returns_empty():
    findings = scan_text_for_secrets("nothing_secret_here = ordinary words")
    assert findings == []


def test_redact_log_entry_string_redacts_pii_and_secrets():
    # Built from parts to avoid GitHub secret-scanning push-protection.
    fake_key = "sk_" + "live" + "_" + "abc123def456ghi789jkl"
    raw = f"Lead from ahmad@example.sa with key {fake_key}"
    out = redact_log_entry(raw)
    assert isinstance(out, str)
    assert "ahmad@example.sa" not in out
    assert fake_key not in out


def test_redact_log_entry_dict_walks_recursively():
    fake_key = "sk_" + "live" + "_" + "xyzxyzxyzxyzxyzxyz"
    entry = {
        "msg": "intake from a@b.sa",
        "details": {"phone": "+966501112233", "key": fake_key},
        "list": ["a@b.sa", "ok"],
    }
    out = redact_log_entry(entry)
    assert isinstance(out, dict)
    text = str(out)
    assert "a@b.sa" not in text
    assert "+966501112233" not in text
    assert fake_key not in text


def test_data_minimization_known_types():
    types = list_known_object_types()
    for required in {"lead", "consent_record", "proof_event", "draft_message"}:
        assert required in types


def test_data_minimization_lead_strips_contact_pii():
    contract = data_minimization_for("lead")
    pii = set(contract.pii_fields)
    assert "contact_email" in pii
    assert "contact_phone" in pii
    safe = set(contract.safe_to_export)
    assert "contact_email" not in safe


def test_data_minimization_unknown_raises():
    with pytest.raises(KeyError):
        data_minimization_for("__not_real__")


# ════════════════════ API endpoint tests ════════════════════


@pytest.mark.asyncio
async def test_proof_ledger_record_event_endpoint(tmp_path: Path):
    """Substitute the default ledger with a test-scoped one for safety."""
    from auto_client_acquisition.proof_ledger import file_backend as fb
    from api.main import app

    test_ledger = FileProofLedger(base_dir=tmp_path)
    transport = ASGITransport(app=app)
    with patch.object(fb, "_DEFAULT", test_ledger):
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            r = await client.post(
                "/api/v1/proof-ledger/events",
                json={
                    "event_type": "diagnostic_delivered",
                    "customer_handle": "TEST-CUST",
                    "summary_ar": "تم تسليم Diagnostic",
                    "summary_en": "Diagnostic delivered",
                },
            )
        assert r.status_code == 200


@pytest.mark.asyncio
async def test_gtm_content_calendar_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/gtm/content-calendar?slots_per_week=3")
    assert r.status_code == 200
    payload = r.json()
    assert payload["slots_total"] <= 3


@pytest.mark.asyncio
async def test_gtm_experiment_draft_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/gtm/experiment/draft",
            json={
                "name": "test",
                "hypothesis_ar": "x", "hypothesis_en": "x",
                "variant_a_ar": "مرحباً", "variant_a_en": "hi",
                "variant_b_ar": "أهلاً", "variant_b_en": "hello",
                "success_metric": "reply_rate",
                "target_audience": "saudi_b2b",
            },
        )
    assert r.status_code == 200
    assert r.json()["status"] == "draft"


@pytest.mark.asyncio
async def test_gtm_experiment_400_on_missing_field():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/gtm/experiment/draft",
            json={"name": "incomplete"},
        )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_security_scan_text_endpoint():
    from api.main import app

    fake_key = "sk_" + "live" + "_" + "abcdefghijklmnop"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/security-privacy/scan-text",
            json={"text": f"key {fake_key}"},
        )
    assert r.status_code == 200
    payload = r.json()
    assert payload["clean"] is False
    assert payload["findings_count"] >= 1


@pytest.mark.asyncio
async def test_security_redact_log_endpoint():
    from api.main import app

    fake_key = "sk_" + "live" + "_" + "xyzxyzxyzxyzxyzxyz"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/security-privacy/redact-log",
            json={"entry": f"user a@b.sa key {fake_key}"},
        )
    assert r.status_code == 200
    text = str(r.json()["redacted"])
    assert "a@b.sa" not in text
    assert fake_key not in text


@pytest.mark.asyncio
async def test_security_data_minimization_lead_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/security-privacy/data-minimization/lead")
    assert r.status_code == 200
    assert "contact_email" in r.json()["pii_fields"]
