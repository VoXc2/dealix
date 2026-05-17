"""Stage Exit Criteria — a stage may not be left without evidence."""

from __future__ import annotations

from auto_client_acquisition.revenue_assurance_os.stage_exit import (
    PipelineStage,
    stage_exit_check,
)


def test_qualified_stage_requires_four_criteria() -> None:
    ok, missing = stage_exit_check(PipelineStage.QUALIFIED, set())
    assert ok is False
    assert set(missing) == {"icp_fit", "pain", "likely_budget", "owner"}


def test_complete_evidence_passes() -> None:
    evidence = {"approved_invoice", "approved_scope"}
    ok, missing = stage_exit_check(PipelineStage.INVOICE_SENT, evidence)
    assert ok is True
    assert missing == ()


def test_string_stage_is_accepted() -> None:
    ok, missing = stage_exit_check("paid", set())
    assert ok is False
    assert missing == ("payment_proof_or_signed_commitment",)
