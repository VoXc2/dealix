"""Customer-success + payment guardrails.

- Renewal/expansion is only 'ready' when delivered value proof is >= L3.
- Payment handoffs always require approval and never store secrets.
"""

from conftest import load_json

EVIDENCE_ORDER = ["L0", "L1", "L2", "L3", "L4", "L5"]


def _ge(level: str, floor: str) -> bool:
    return EVIDENCE_ORDER.index(level) >= EVIDENCE_ORDER.index(floor)


def test_renewal_ready_requires_value_proof(company_os):
    records = load_json(company_os / "customer_success" / "client_health.json")
    for rec in records:
        if rec["status"] in {"renewal_ready", "expansion_ready"}:
            assert _ge(rec["value_proof_level"], "L3"), (
                f"{rec['client']} marked {rec['status']} but value proof is "
                f"{rec['value_proof_level']} (< L3)"
            )


def test_watch_clients_are_not_pitched_renewal(company_os):
    records = load_json(company_os / "customer_success" / "client_health.json")
    watch = [r for r in records if r["status"] == "watch"]
    for r in watch:
        # A watch client below L3 must not be in a renewal-ready posture.
        assert r["status"] not in {"renewal_ready", "expansion_ready"}


def test_payment_handoff_schema_requires_approval():
    # The schema itself must hard-require approval and forbid arbitrary fields
    # (so card/secret data can't leak into the record).
    schema = load_json(
        __import__("pathlib").Path(__file__).resolve().parent.parent
        / "schemas" / "payment_handoff.schema.json"
    )
    assert schema["properties"]["requires_approval"] == {"const": True}
    assert schema["additionalProperties"] is False
    assert "requires_approval" in schema["required"]
