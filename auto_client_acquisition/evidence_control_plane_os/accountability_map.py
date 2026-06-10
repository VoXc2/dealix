"""Accountability map — owners for execution and external use."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AccountabilityRecord:
    output_id: str
    generated_by: str
    reviewed_by: str
    approved_by: str
    governed_by: str
    owned_by: str
    client_sponsor: str
    dealix_owner: str


def accountability_valid_for_execution(rec: AccountabilityRecord) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    if not rec.owned_by.strip():
        errors.append("no_owner_no_execution")
    if not rec.generated_by.strip():
        errors.append("generated_by_required")
    return not errors, tuple(errors)


def external_action_accountable(rec: AccountabilityRecord) -> tuple[bool, tuple[str, ...]]:
    _exec_ok, exec_err = accountability_valid_for_execution(rec)
    extra: list[str] = []
    if not rec.approved_by.strip():
        extra.append("no_approval_owner_no_external_action")
    if not rec.client_sponsor.strip():
        extra.append("client_sponsor_required_for_external")
    merged = tuple(exec_err) + tuple(extra)
    return not merged, merged
