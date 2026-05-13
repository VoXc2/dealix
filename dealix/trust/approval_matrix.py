"""Approval Matrix — maps (action, evidence_level) → required approver role.

مصفوفة الموافقات — تحدد الدور المخوّل للموافقة على كل نوع إجراء.
"""
from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class ActionKind(StrEnum):
    OUTBOUND_EMAIL = "outbound_email"
    OUTBOUND_WHATSAPP = "outbound_whatsapp"
    OUTBOUND_SMS = "outbound_sms"
    PUBLIC_POST = "public_post"
    EXTERNAL_API_WRITE = "external_api_write"
    DATA_EXPORT = "data_export"
    CRM_BULK_UPDATE = "crm_bulk_update"
    INVOICE_GENERATION = "invoice_generation"
    POLICY_OVERRIDE = "policy_override"


class ApproverRole(StrEnum):
    AUTO = "auto"  # no human needed
    CSM = "csm"
    AE = "ae"
    HEAD_CS = "head_cs"
    HEAD_LEGAL = "head_legal"
    CTO = "cto"
    CEO = "ceo"


class ApprovalRequirement(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="forbid")
    action: ActionKind
    min_evidence_level: int  # 0..5 (L0..L5)
    approver: ApproverRole
    reason_ar: str
    reason_en: str


# Maps (action, min_evidence) -> approver. Evidence below the min upgrades approver.
_BASE_MATRIX: dict[ActionKind, ApprovalRequirement] = {
    ActionKind.OUTBOUND_EMAIL: ApprovalRequirement(
        action=ActionKind.OUTBOUND_EMAIL,
        min_evidence_level=2,
        approver=ApproverRole.CSM,
        reason_ar="بريد خارجي يحتاج موافقة CSM ومستوى دليل L2.",
        reason_en="Outbound email requires CSM approval and evidence L2+.",
    ),
    ActionKind.OUTBOUND_WHATSAPP: ApprovalRequirement(
        action=ActionKind.OUTBOUND_WHATSAPP,
        min_evidence_level=3,
        approver=ApproverRole.HEAD_CS,
        reason_ar="WhatsApp يحتاج موافقة Head of CS ودليل L3.",
        reason_en="WhatsApp requires Head of CS approval and evidence L3+.",
    ),
    ActionKind.OUTBOUND_SMS: ApprovalRequirement(
        action=ActionKind.OUTBOUND_SMS,
        min_evidence_level=3,
        approver=ApproverRole.HEAD_CS,
        reason_ar="SMS خارجي يحتاج موافقة Head of CS.",
        reason_en="Outbound SMS requires Head of CS approval.",
    ),
    ActionKind.PUBLIC_POST: ApprovalRequirement(
        action=ActionKind.PUBLIC_POST,
        min_evidence_level=4,
        approver=ApproverRole.HEAD_LEGAL,
        reason_ar="منشور علني يحتاج موافقة قانونية.",
        reason_en="Public posts require Legal approval.",
    ),
    ActionKind.EXTERNAL_API_WRITE: ApprovalRequirement(
        action=ActionKind.EXTERNAL_API_WRITE,
        min_evidence_level=3,
        approver=ApproverRole.CTO,
        reason_ar="كتابة على API خارجي تحتاج موافقة CTO.",
        reason_en="External API writes require CTO approval.",
    ),
    ActionKind.DATA_EXPORT: ApprovalRequirement(
        action=ActionKind.DATA_EXPORT,
        min_evidence_level=2,
        approver=ApproverRole.HEAD_LEGAL,
        reason_ar="تصدير بيانات يحتاج موافقة Legal/DPO.",
        reason_en="Data export requires Legal/DPO approval.",
    ),
    ActionKind.CRM_BULK_UPDATE: ApprovalRequirement(
        action=ActionKind.CRM_BULK_UPDATE,
        min_evidence_level=2,
        approver=ApproverRole.AE,
        reason_ar="تحديث جماعي على CRM يحتاج موافقة AE.",
        reason_en="CRM bulk update requires AE approval.",
    ),
    ActionKind.INVOICE_GENERATION: ApprovalRequirement(
        action=ActionKind.INVOICE_GENERATION,
        min_evidence_level=3,
        approver=ApproverRole.HEAD_CS,
        reason_ar="إصدار فاتورة يحتاج موافقة Head of CS.",
        reason_en="Invoice generation requires Head of CS approval.",
    ),
    ActionKind.POLICY_OVERRIDE: ApprovalRequirement(
        action=ActionKind.POLICY_OVERRIDE,
        min_evidence_level=5,
        approver=ApproverRole.CEO,
        reason_ar="تجاوز السياسة لا يحدث إلا بموافقة CEO.",
        reason_en="Policy override requires CEO approval.",
    ),
}


def required_approver(action: ActionKind, evidence_level: int) -> ApprovalRequirement:
    """Return the approver requirement; auto-escalates if evidence is below the floor."""
    base = _BASE_MATRIX[action]
    if evidence_level >= base.min_evidence_level:
        return base
    # Evidence below floor → escalate one role up.
    escalation: dict[ApproverRole, ApproverRole] = {
        ApproverRole.CSM: ApproverRole.HEAD_CS,
        ApproverRole.AE: ApproverRole.HEAD_CS,
        ApproverRole.HEAD_CS: ApproverRole.HEAD_LEGAL,
        ApproverRole.HEAD_LEGAL: ApproverRole.CEO,
        ApproverRole.CTO: ApproverRole.CEO,
        ApproverRole.CEO: ApproverRole.CEO,
        ApproverRole.AUTO: ApproverRole.CSM,
    }
    return base.model_copy(
        update={
            "approver": escalation[ApproverRole(base.approver)],
            "reason_ar": base.reason_ar + " (تصعيد بسبب نقص الدليل).",
            "reason_en": base.reason_en + " (Escalated due to evidence shortfall).",
        }
    )
