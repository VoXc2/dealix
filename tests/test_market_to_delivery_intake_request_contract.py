"""Pure contract tests: no DB, real auth, network, or production-readiness claim."""
import importlib.util
from pathlib import Path
import sys

import pytest
from pydantic import ValidationError

PATH = Path(__file__).resolve().parents[1] / "auto_client_acquisition/service_catalog/intake_request_contract.py"
SPEC = importlib.util.spec_from_file_location("mtd_intake_contract_under_test", PATH)
assert SPEC and SPEC.loader
contract = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = contract
SPEC.loader.exec_module(contract)
Body = contract.MarketToDeliveryIntakeBody
fingerprint = contract.intake_request_fingerprint


def payload(**changes):
    data = dict(request_id="request-1", account_id="account-1", company_name="Synthetic Co",
                source_id="source-1", project_id="construction-01", problem="Synthetic RFI queue",
                data_authorized=True, estimated_cost_sar="100.00", target_margin_pct="40.00",
                evidence_refs=[{"ref": "synthetic://a", "sha256": "a" * 64}])
    data.update(changes)
    return data


@pytest.mark.parametrize("value", ["true", "false", "yes", "1", 1, 0, [], {}, None])
def test_authority_cannot_be_coerced(value):
    with pytest.raises(ValidationError):
        Body.model_validate(payload(data_authorized=value))


@pytest.mark.parametrize("field", ["account_id", "source_id", "company_name", "problem", "project_id", "request_id"])
def test_whitespace_only_required_values_rejected(field):
    with pytest.raises(ValidationError):
        Body.model_validate(payload(**{field: "   "}))


def test_identifiers_normalized_before_lookup():
    body = Body.model_validate(payload(account_id=" account-1 ", source_id=" source-1 "))
    assert body.account_id == "account-1"
    assert body.source_id == "source-1"
    assert fingerprint(body, "tenant-a") == fingerprint(Body.model_validate(payload()), "tenant-a")


@pytest.mark.parametrize("field,value", [
    ("company_name", "Changed Company"), ("account_id", "account-2"),
    ("source_id", "source-2"), ("project_id", "construction-02"),
    ("problem", "Changed requirement"), ("estimated_cost_sar", "101"),
    ("target_margin_pct", "41"), ("customer_context", "New context"),
    ("baseline", "Changed baseline"), ("current_workflow", "Changed workflow"),
    ("desired_outcome", "Changed outcome"), ("constraints", "New constraints"),
    ("request_id", "request-2"), ("data_authorized", False),
])
def test_material_input_change_changes_fingerprint(field, value):
    before = fingerprint(Body.model_validate(payload()), "tenant-a")
    after = fingerprint(Body.model_validate(payload(**{field: value})), "tenant-a")
    assert after != before


def test_tenant_is_bound():
    body = Body.model_validate(payload())
    assert fingerprint(body, "tenant-a") != fingerprint(body, "tenant-b")


def test_equivalent_decimal_representations_are_stable():
    a = Body.model_validate(payload(estimated_cost_sar="100", target_margin_pct=40))
    b = Body.model_validate(payload())
    assert fingerprint(a, "tenant-a") == fingerprint(b, "tenant-a")


def test_evidence_is_deduplicated_and_order_independent():
    a = {"ref": "synthetic://a", "sha256": "a" * 64}
    b = {"ref": "synthetic://b", "sha256": "b" * 64}
    left = Body.model_validate(payload(evidence_refs=[a,b,a]))
    right = Body.model_validate(payload(evidence_refs=[b,a]))
    assert fingerprint(left, "tenant-a") == fingerprint(right, "tenant-a")
    assert fingerprint(left, "tenant-a") != fingerprint(Body.model_validate(payload()), "tenant-a")


@pytest.mark.parametrize("value", ["NaN", "Infinity", "-1", "1.001", True])
def test_invalid_money_rejected(value):
    with pytest.raises(ValidationError):
        Body.model_validate(payload(estimated_cost_sar=value))


@pytest.mark.parametrize("field", ["tenant_id", "consent", "auto_approve", "request_digest", "engine_sha256"])
def test_client_cannot_inject_server_authority(field):
    with pytest.raises(ValidationError):
        Body.model_validate(payload(**{field: "attacker"}))


def test_fingerprint_is_independent_of_runtime_engine_version():
    body = Body.model_validate(payload())
    first = fingerprint(body, "tenant-a")
    contract.ENGINE_SHA256 = "changed-engine-not-an-input"
    assert fingerprint(body, "tenant-a") == first
    assert len(first) == 64


def test_controls_and_extra_evidence_keys_rejected():
    with pytest.raises(ValidationError):
        Body.model_validate(payload(company_name="A\x00B"))
    with pytest.raises(ValidationError):
        Body.model_validate(payload(evidence_refs=[{"ref":"x","sha256":"a"*64,"tenant_id":"other"}]))


def test_false_is_preserved_not_upgraded():
    assert Body.model_validate(payload(data_authorized=False)).data_authorized is False


@pytest.mark.parametrize("field", ["baseline", "current_workflow", "constraints", "customer_context", "desired_outcome"])
def test_optional_blank_normalizes_to_missing(field):
    body = Body.model_validate(payload(**{field: " \t "}))
    assert getattr(body, field) is None
    assert fingerprint(body, "tenant-a") == fingerprint(Body.model_validate(payload()), "tenant-a")


@pytest.mark.parametrize("tenant", ["", "x" * 65, "a/b", "../a", " tenant-a", None])
def test_invalid_authenticated_tenant_rejected(tenant):
    with pytest.raises(ValueError):
        fingerprint(Body.model_validate(payload()), tenant)
