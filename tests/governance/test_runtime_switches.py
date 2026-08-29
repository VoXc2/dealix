from __future__ import annotations

import pytest

from dealix.governance.runtime_switches import RuntimeSwitchGate, SENSITIVE_SWITCHES


def test_runtime_switch_cannot_raise_denied_authority() -> None:
    gate = RuntimeSwitchGate(evaluator=lambda _key, _default: True)

    for key in SENSITIVE_SWITCHES:
        decision = gate.evaluate(key, authority_allows=False)
        assert decision.effective_allowed is False
        assert decision.runtime_switch_allows is False
        assert decision.reason == "DENIED_BY_CANONICAL_AUTHORITY"


def test_missing_or_false_runtime_switch_lowers_existing_authority() -> None:
    gate = RuntimeSwitchGate(evaluator=lambda _key, default: default)

    for key in SENSITIVE_SWITCHES:
        decision = gate.evaluate(key, authority_allows=True)
        assert decision.effective_allowed is False
        assert decision.reason == "LOWERED_BY_RUNTIME_SWITCH"


def test_runtime_switch_may_allow_only_when_canonical_authority_already_allows() -> None:
    gate = RuntimeSwitchGate(evaluator=lambda _key, _default: True)

    decision = gate.evaluate("connector_write", authority_allows=True)
    assert decision.runtime_switch_allows is True
    assert decision.effective_allowed is True
    assert decision.reason == "ALLOWED_BY_AUTHORITY_AND_RUNTIME_SWITCH"


def test_provider_or_evaluator_failure_is_fail_closed() -> None:
    def boom(_key: str, _default: bool) -> bool:
        raise RuntimeError("provider unavailable")

    gate = RuntimeSwitchGate(evaluator=boom)
    assert gate.allowed("cloud_model_route", authority_allows=True) is False


def test_unknown_runtime_switch_is_rejected() -> None:
    gate = RuntimeSwitchGate(evaluator=lambda _key, _default: True)
    with pytest.raises(ValueError, match="unsupported Dealix runtime switch"):
        gate.allowed("make_everything_live", authority_allows=True)
