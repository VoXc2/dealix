"""Value OS: discipline (verified/client_confirmed require refs), summarize, monthly markdown."""
from __future__ import annotations

import pytest

from auto_client_acquisition.value_os.monthly_report import (
    generate as generate_monthly,
)
from auto_client_acquisition.value_os.value_ledger import (
    ValueDisciplineError,
    add_event,
    clear_for_test as clear_value_for_test,
    list_events,
    summarize,
)


@pytest.fixture(autouse=True)
def isolated_ledgers(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "friction.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "capital.jsonl"))
    for cid in ("X", "acme", "tenantA"):
        try:
            clear_value_for_test(cid)
        except Exception:
            pass
    yield
    for cid in ("X", "acme", "tenantA"):
        try:
            clear_value_for_test(cid)
        except Exception:
            pass


def test_verified_tier_requires_source_ref() -> None:
    with pytest.raises(ValueDisciplineError):
        add_event(
            customer_id="acme",
            kind="revenue_uplift",
            amount=1000.0,
            tier="verified",
            source_ref="",
        )


def test_client_confirmed_requires_both_refs() -> None:
    # Missing confirmation_ref
    with pytest.raises(ValueDisciplineError):
        add_event(
            customer_id="acme",
            kind="revenue_uplift",
            amount=1000.0,
            tier="client_confirmed",
            source_ref="invoice#123",
            confirmation_ref="",
        )
    # Missing source_ref
    with pytest.raises(ValueDisciplineError):
        add_event(
            customer_id="acme",
            kind="revenue_uplift",
            amount=1000.0,
            tier="client_confirmed",
            source_ref="",
            confirmation_ref="signed_doc#9",
        )


def test_estimated_tier_accepted() -> None:
    ev = add_event(
        customer_id="acme",
        kind="revenue_uplift",
        amount=1000.0,
        tier="estimated",
        source_ref="",
    )
    assert ev.tier == "estimated"
    assert ev.amount == 1000.0


def test_summarize_aggregates_by_tier() -> None:
    add_event(customer_id="tenantA", kind="x", amount=100.0, tier="estimated")
    add_event(
        customer_id="tenantA",
        kind="x",
        amount=200.0,
        tier="observed",
        source_ref="log#1",
    )
    add_event(
        customer_id="tenantA",
        kind="x",
        amount=300.0,
        tier="verified",
        source_ref="invoice#1",
    )

    summary = summarize(customer_id="tenantA", period_days=30)
    assert isinstance(summary, dict)
    # Per-tier totals (whatever the key names are, at least one of them should
    # match these literal tier strings since they come from the doctrine).
    for tier in ("estimated", "observed", "verified"):
        assert tier in summary, f"summary missing tier key: {tier}"


def test_estimated_never_auto_promoted() -> None:
    add_event(customer_id="tenantA", kind="x", amount=100.0, tier="estimated")
    summarize(customer_id="tenantA", period_days=30)
    events = list_events(customer_id="tenantA")
    assert events, "no events after summarize"
    assert all(e.tier == "estimated" for e in events)


def test_monthly_report_to_markdown_contains_limitations() -> None:
    report = generate_monthly(customer_id="X")
    md = report.to_markdown()
    assert "## Limitations" in md


def test_monthly_report_to_markdown_contains_bilingual_disclaimer() -> None:
    report = generate_monthly(customer_id="X")
    md = report.to_markdown()
    assert "Estimated value is not Verified value" in md
    assert "القيمة التقديرية ليست قيمة مُتحقَّقة" in md


def test_monthly_report_has_governance_decision() -> None:
    report = generate_monthly(customer_id="X")
    assert isinstance(report.governance_decision, str)
    assert report.governance_decision != ""
