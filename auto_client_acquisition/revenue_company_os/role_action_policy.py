"""
Role Action Policy — pure-data table mapping (role, action_path) → allowed?

The policy implements the "blocked actions per role" lists from the vision
document. Adding a new constraint is a one-line edit to BLOCK_RULES.

Used by api/middleware.RoleActionGuardMiddleware. Opt-in via the
X-Dealix-Role request header — without that header the policy is bypassed
(public/unauthenticated endpoints stay open).

Match semantics:
  - rule path matches request path exactly OR is a prefix ending with "/"
  - method "*" matches any method; otherwise exact match
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BlockRule:
    role: str
    method: str  # "POST" | "GET" | ... | "*"
    path: str    # exact path OR prefix ending with "/"
    reason_ar: str


# ── Block rules ───────────────────────────────────────────────────
# Each tuple says: this role MUST NOT perform this action.
BLOCK_RULES: tuple[BlockRule, ...] = (
    # Sales cannot trigger live charge or recreate tables.
    BlockRule("sales_manager", "POST", "/api/v1/payments/charge",
              "البيع لا يستطيع تشغيل live charge — يحتاج موافقة CEO + Compliance."),
    BlockRule("sales_manager", "POST", "/api/v1/admin/recreate-tables",
              "البيع لا يصل إلى عمليات الـ admin."),

    # Growth cannot send WhatsApp/Email without compliance review.
    BlockRule("growth_manager", "POST", "/api/v1/whatsapp/brief/send-internal",
              "النمو لا يرسل WhatsApp مباشرة — يمر بـ Compliance."),
    BlockRule("growth_manager", "POST", "/api/v1/email/send",
              "النمو لا يرسل بريد مباشر — يمر بـ Compliance."),
    BlockRule("growth_manager", "POST", "/api/v1/calls/dial-live",
              "النمو لا يبدأ مكالمات حية."),

    # Customer Success cannot change pricing or live-action gates.
    BlockRule("customer_success", "POST", "/api/v1/services/",
              "CS لا يعدّل الـ Service Tower أو الأسعار."),
    BlockRule("customer_success", "POST", "/api/v1/admin/",
              "CS لا يصل إلى الـ admin."),

    # Compliance cannot bypass the gates (read-only role for live actions).
    BlockRule("compliance", "POST", "/api/v1/payments/charge",
              "Compliance لا يدفع نيابةً — دور التحقق فقط."),
    BlockRule("compliance", "POST", "/api/v1/whatsapp/brief/send-internal",
              "Compliance لا ينفّذ outbound."),
    BlockRule("compliance", "POST", "/api/v1/calls/dial-live",
              "Compliance لا يبدأ مكالمات حية."),

    # RevOps cannot send outbound directly (read/observe + reroute only).
    BlockRule("revops", "POST", "/api/v1/whatsapp/brief/send-internal",
              "RevOps لا يرسل outbound — يقرأ ويعيد التوجيه."),
    BlockRule("revops", "POST", "/api/v1/calls/dial-live",
              "RevOps لا يبدأ مكالمات حية."),

    # Finance cannot edit lead/customer records (audit + reconcile only).
    BlockRule("finance", "POST", "/api/v1/leads/",
              "المالية لا تعدّل leads — قراءة فقط."),
    BlockRule("finance", "POST", "/api/v1/customers/",
              "المالية لا تعدّل customers — قراءة فقط."),

    # Agency partners cannot read other partners' data.
    BlockRule("agency_partner", "GET", "/api/v1/admin/",
              "الشريك لا يصل إلى admin."),
    BlockRule("agency_partner", "POST", "/api/v1/admin/",
              "الشريك لا يصل إلى admin."),
)


def _matches(rule: BlockRule, method: str, path: str) -> bool:
    if rule.method != "*" and rule.method.upper() != method.upper():
        return False
    if rule.path.endswith("/"):
        return path.startswith(rule.path)
    return path == rule.path


def evaluate(role: str | None, method: str, path: str) -> tuple[bool, str | None]:
    """Decide whether (role, method, path) is allowed by the policy.

    Returns (allowed, reason_if_blocked).

    Behavior:
      - role is None or empty → always allowed (public/unauthed endpoints)
      - any matching BlockRule → (False, reason_ar)
      - no matching rule → (True, None)
    """
    if not role:
        return True, None
    role = role.strip().lower()
    if not role:
        return True, None
    for rule in BLOCK_RULES:
        if rule.role == role and _matches(rule, method, path):
            return False, rule.reason_ar
    return True, None


def list_blocked_for(role: str) -> list[dict[str, str]]:
    """Return the policy table filtered for a given role — used by UI hints."""
    role = (role or "").strip().lower()
    return [
        {"method": r.method, "path": r.path, "reason_ar": r.reason_ar}
        for r in BLOCK_RULES if r.role == role
    ]
