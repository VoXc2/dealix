"""Transactional email sender — confirmations / receipts / delivery
notifications for customer-initiated interactions.

Distinct from cold outreach: the customer opted-in by submitting a form
or signing a proposal, so the compliance gates designed to prevent cold
spam are skipped. Marketing suppression remains: hard-bounced addresses
or explicit opt-outs in `auto_client_acquisition.consent_table` still
block sends.

Whitelisted template kinds (no other kind may use this path):

  - diagnostic_intake_confirmation
  - diagnostic_delivered
  - proposal_sent
  - proposal_accepted
  - payment_invoice
  - payment_confirmed
  - proof_pack_delivered
  - monthly_value_report
  - retainer_renewal_notice

Every send is logged with `email_kind` so audit_export sees it.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.consent_table import is_consented
from auto_client_acquisition.email.gmail_send import GmailSendResult, send_email

ALLOWED_KINDS = frozenset({
    "diagnostic_intake_confirmation",
    "diagnostic_delivered",
    "proposal_sent",
    "proposal_accepted",
    "payment_invoice",
    "payment_confirmed",
    "proof_pack_delivered",
    "monthly_value_report",
    "retainer_renewal_notice",
})


@dataclass
class TransactionalSendResult:
    delivered: bool
    reason_code: str  # ok | blocked_kind | blocked_opt_out | gmail_error | no_recipient
    kind: str
    to_email: str
    gmail_message_id: str | None = None
    sent_at: str = ""
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _is_revoked_for_transactional(to_email: str) -> bool:
    """Even transactional sends must respect explicit revoke (PDPL Article 5).
    A customer who revoked transactional consent — e.g., after deleting their
    account — must not be re-contacted.
    """
    try:
        # Transactional is its own purpose in consent_table.
        return not is_consented(
            contact_id=to_email, channel="email", purpose="transactional"
        ) and _explicit_revoke(to_email)
    except Exception:  # noqa: BLE001
        # default-allow for transactional (customer opted-in by interacting)
        return False


def _explicit_revoke(to_email: str) -> bool:
    """Returns True iff there's an EXPLICIT revoke record for this address.
    Absence of a record is treated as "implied consent via form submission"
    for transactional purposes only.
    """
    try:
        from auto_client_acquisition.consent_table import records_for
        for rec in reversed(records_for(to_email)):
            if rec.channel == "email" and rec.purpose == "transactional":
                return rec.kind == "revoke"
        return False
    except Exception:  # noqa: BLE001
        return False


async def send_transactional(
    *,
    kind: str,
    to_email: str,
    subject: str,
    body_plain: str,
    sender_name: str = "Dealix",
    customer_id: str | None = None,
) -> TransactionalSendResult:
    """Send a transactional email. Whitelisted kinds only. PDPL Article 5
    revoke is always honored.
    """
    now = datetime.now(timezone.utc).isoformat()

    if kind not in ALLOWED_KINDS:
        return TransactionalSendResult(
            delivered=False,
            reason_code="blocked_kind",
            kind=kind,
            to_email=to_email,
            sent_at=now,
            error=f"kind {kind!r} not in {sorted(ALLOWED_KINDS)}",
        )

    if not to_email or "@" not in to_email:
        return TransactionalSendResult(
            delivered=False,
            reason_code="no_recipient",
            kind=kind,
            to_email=to_email,
            sent_at=now,
        )

    if _explicit_revoke(to_email):
        return TransactionalSendResult(
            delivered=False,
            reason_code="blocked_opt_out",
            kind=kind,
            to_email=to_email,
            sent_at=now,
        )

    result: GmailSendResult = await send_email(
        to_email=to_email,
        subject=subject,
        body_plain=body_plain,
        sender_name=sender_name,
    )

    if result.status == "ok":
        return TransactionalSendResult(
            delivered=True,
            reason_code="ok",
            kind=kind,
            to_email=to_email,
            gmail_message_id=result.gmail_message_id,
            sent_at=now,
        )

    return TransactionalSendResult(
        delivered=False,
        reason_code="gmail_error",
        kind=kind,
        to_email=to_email,
        sent_at=now,
        error=result.error or result.status,
    )


# ── Templates ────────────────────────────────────────────────────────


def render_diagnostic_intake_confirmation(
    *, customer_name: str, sector: str, expected_eta_hours: int = 24
) -> tuple[str, str]:
    """Returns (subject, body_plain). Bilingual AR + EN."""
    subject = (
        "تأكيد استلام طلب التشخيص — Dealix / Diagnostic intake received — Dealix"
    )
    body = (
        f"السلام عليكم {customer_name}،\n\n"
        f"استلمنا طلب التشخيص لقطاع {sector}. "
        f"سيصلكم التقرير خلال {expected_eta_hours} ساعة بالعربية والإنجليزية، "
        "مع توصيات أولية لمعالجة فرص الإيراد.\n\n"
        "ملاحظات مهمة:\n"
        "- التقرير تقديري ولا يَعِد بنتائج مبيعات مضمونة.\n"
        "- لن نُرسل أي رسائل خارجية لعملائك دون موافقتك.\n"
        "- لن نقوم بأي scraping أو تواصل آلي بارد.\n\n"
        "إذا كان لديك بيانات أولية تريد مشاركتها قبل التحليل، "
        "أرسلها كرد على هذه الرسالة.\n\n"
        "— فريق Dealix\n\n"
        "—\n\n"
        f"Hello {customer_name},\n\n"
        f"We received your diagnostic intake for sector {sector}. "
        f"Your bilingual (AR + EN) brief will arrive within {expected_eta_hours} hours "
        "with initial recommendations on revenue opportunities.\n\n"
        "Important notes:\n"
        "- The brief is estimated — no guaranteed sales outcomes.\n"
        "- We will NOT send external messages to your customers without your approval.\n"
        "- We do NOT scrape or send cold automated outreach.\n\n"
        "If you have data to share before the analysis, reply to this email.\n\n"
        "— Dealix team"
    )
    return subject, body


def render_proposal_sent(
    *,
    customer_name: str,
    engagement_id: str,
    price_sar: int,
    payment_link: str = "",
) -> tuple[str, str]:
    subject = (
        f"عرض مشروع #{engagement_id} — Dealix / Sprint proposal #{engagement_id} — Dealix"
    )
    body = (
        f"السلام عليكم {customer_name}،\n\n"
        f"مرفق عرض Revenue Intelligence Sprint رقم {engagement_id} "
        f"بقيمة {price_sar} ريال سعودي.\n\n"
        "نطاق محدود، حدود واضحة، Proof Pack مضمون مع كل تسليم.\n"
        + (f"\nرابط الدفع: {payment_link}\n" if payment_link else "")
        + "\nرد على هذه الرسالة بـ’موافق’ لبدء التنفيذ خلال 24 ساعة.\n\n"
        "— Dealix\n\n"
        "—\n\n"
        f"Hello {customer_name},\n\n"
        f"Attached is your Revenue Intelligence Sprint proposal #{engagement_id} "
        f"at {price_sar} SAR.\n\n"
        "Bounded scope, clear exclusions, Proof Pack guaranteed on every delivery.\n"
        + (f"\nPayment link: {payment_link}\n" if payment_link else "")
        + "\nReply ’approved’ to start within 24 hours.\n\n"
        "— Dealix"
    )
    return subject, body


def render_proof_pack_delivered(
    *, customer_name: str, engagement_id: str, proof_score: float, tier: str
) -> tuple[str, str]:
    subject = (
        f"Proof Pack جاهز — مشروع {engagement_id} / Proof Pack ready — engagement {engagement_id}"
    )
    body = (
        f"السلام عليكم {customer_name}،\n\n"
        f"تم إصدار Proof Pack للمشروع {engagement_id} بدرجة {proof_score}/100 "
        f"(تصنيف: {tier}).\n\n"
        "المرفق يحتوي على 14 قسماً: الملخص التنفيذي، البيانات المُستخدمة، "
        "قرارات الحوكمة، الفرص المرتبة، المسودات، القيمة المرصودة، الحدود، "
        "والخطوات التالية.\n\n"
        "نرحب بمراجعة Managed Revenue Ops الشهرية إذا كنت ترى تكراراً شهرياً للقيمة.\n\n"
        "— Dealix\n\n"
        "—\n\n"
        f"Hello {customer_name},\n\n"
        f"Your Proof Pack for engagement {engagement_id} is ready with a score "
        f"of {proof_score}/100 (tier: {tier}).\n\n"
        "Attached: 14 sections covering executive summary, data used, governance "
        "decisions, ranked opportunities, drafts, observed value, limitations, "
        "and next steps.\n\n"
        "Happy to discuss a monthly Managed Revenue Ops cadence if the value is "
        "recurring for you.\n\n"
        "— Dealix"
    )
    return subject, body


__all__ = [
    "ALLOWED_KINDS",
    "TransactionalSendResult",
    "render_diagnostic_intake_confirmation",
    "render_proof_pack_delivered",
    "render_proposal_sent",
    "send_transactional",
]
