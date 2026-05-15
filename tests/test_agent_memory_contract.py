"""Agent OS — memory contract (task 5)."""
from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import (
    DataClass,
    LawfulBasis,
    MemoryItem,
    clear_for_test,
    is_expired,
    new_memory_contract,
    validate_memory_contract,
)


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "fr.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    clear_for_test()
    yield
    clear_for_test()


def test_pii_without_lawful_basis_rejected():
    contract = new_memory_contract(
        agent_id="a1",
        lawful_basis=LawfulBasis.NONE,
        max_retention_days=90,
        items=[
            MemoryItem(
                key="customer_record",
                data_class=DataClass.PII.value,
                purpose="follow-up",
                retention_days=30,
            ),
        ],
    )
    result = validate_memory_contract(contract)
    assert result.ok is False
    assert any(i.startswith("pii_without_lawful_basis") for i in result.issues)


def test_non_pii_no_basis_allowed():
    contract = new_memory_contract(
        agent_id="a1",
        lawful_basis=LawfulBasis.NONE,
        max_retention_days=90,
        items=[
            MemoryItem(
                key="account_status",
                data_class=DataClass.INTERNAL.value,
                purpose="scoring",
                retention_days=30,
            ),
        ],
    )
    assert validate_memory_contract(contract).ok is True


def test_retention_exceeds_max_rejected():
    contract = new_memory_contract(
        agent_id="a1",
        lawful_basis=LawfulBasis.CONTRACT,
        max_retention_days=90,
        items=[
            MemoryItem(
                key="account_status",
                data_class=DataClass.INTERNAL.value,
                purpose="scoring",
                retention_days=200,
            ),
        ],
    )
    result = validate_memory_contract(contract)
    assert result.ok is False
    assert any(i.startswith("retention_exceeds_max") for i in result.issues)


def test_retention_without_purpose_flagged():
    contract = new_memory_contract(
        agent_id="a1",
        lawful_basis=LawfulBasis.CONTRACT,
        max_retention_days=90,
        items=[
            MemoryItem(
                key="account_status",
                data_class=DataClass.INTERNAL.value,
                purpose="",
                retention_days=30,
            ),
        ],
    )
    result = validate_memory_contract(contract)
    assert result.ok is False
    assert any(i.startswith("retention_without_purpose") for i in result.issues)


def test_sensitive_pii_requires_consent():
    contract = new_memory_contract(
        agent_id="a1",
        lawful_basis=LawfulBasis.CONTRACT,
        max_retention_days=90,
        items=[
            MemoryItem(
                key="customer_record",
                data_class=DataClass.SENSITIVE_PII.value,
                purpose="support",
                retention_days=30,
            ),
        ],
    )
    result = validate_memory_contract(contract)
    assert result.ok is False
    assert any(i.startswith("sensitive_pii_requires_consent") for i in result.issues)


def test_is_expired_window_check():
    item = MemoryItem(
        key="account_status",
        data_class=DataClass.INTERNAL.value,
        purpose="scoring",
        retention_days=1,
    )
    assert is_expired(
        item,
        stored_at_iso="2026-05-10T00:00:00+00:00",
        now_iso="2026-05-14T00:00:00+00:00",
    ) is True
    assert is_expired(
        item,
        stored_at_iso="2026-05-14T00:00:00+00:00",
        now_iso="2026-05-14T06:00:00+00:00",
    ) is False
