"""Support ticket classify + deterministic draft replies (approval-first)."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.revenue_ops_autopilot.knowledge import load_knowledge_articles, score_article_match
from dealix.revenue_ops_autopilot.policies import kb_auto_reply_allowed
from dealix.revenue_ops_autopilot.schemas import ApprovalNeed


@dataclass
class SupportSignals:
    intent: str
    priority: str
    risk_level: str
    suggested_response_ar: str
    kb_source_ids: list[str]
    approval_need: ApprovalNeed
    kb_auto_allow: bool
    escalation_reason_ar: str | None


_INTENT_WEIGHTS: list[tuple[str, tuple[str, ...]]] = [
    (
        "faq_general",
        (
            "ما هي خدمة",
            "ماهي خدمة",
            "خدمة تشخيص",
            "ما التشخيص",
            "what is diagnostic",
            "what is the diagnostic",
        ),
    ),
    ("pricing_question", ("سعر", "price", "سار", "ريال", "رسوم", "تكلف")),
    ("proof_pack_question", ("proof pack", "دليل", "إثبات", "عرض تجريبي")),
    ("billing_question", ("فاتورة", "invoice", "دفع", "payment", "moyasar", "stripe")),
    ("technical_issue", ("bug", "error", "خطأ", "تسجيل", "login")),
    ("data_privacy", ("pdpl", "privacy", "حذف", "بيانات", "privacy")),
    ("security_question", ("security", "iso", "pen test", "أمن", "SOC")),
    ("refund_or_discount", ("refund", "خصم", "discount", "استرداد")),
    ("partnership", ("partner", "شراكة", "referral", "agency")),
]


def classify_intent(message_lc: str) -> str:
    for intent, needles in _INTENT_WEIGHTS:
        if any(n.lower() in message_lc for n in needles):
            return intent

    vague = ("help", "hi", "hello", "مساعدة")
    if any(v in message_lc for v in vague):
        return "generic"

    return "unknown"


def _financial_guarantee_red_flag(message_raw: str) -> tuple[bool, str | None]:
    """Misleading ROI / autonomy claims — escalate, never auto-send (Assurance playbook)."""

    mlc = message_raw.lower()

    arabic_triggers = (
        "هل تضمنون",
        "تضمنون لنا",
        "تضمن لنا",
        "ضمان نمو",
        "ضمان الإيراد",
        "ضمان تحقيق",
        "زاد الإيراد 30",
        "زيادة الإيراد 30",
        "30٪ للإيراد",
        "نمو الإيراد مضمون",
        "مضمونة لكم",
        "كل مبيعاتك تلقائياً بدون تدخل",
        "تلقائي بالكامل دون موافقتكم",
        "تلقائي بالكامل دون موافقتك",
    )

    latin_triggers = (
        ("guarantee", "30%"),
        ("guarantee", "revenue"),
        ("guarantee", "growth"),
        ("guarantee", "roi"),
        ("guaranteed", "revenue"),
        ("guaranteed", "return"),
        ("promise", "roi"),
        ("will increase revenue", ""),
        ("fully automate", "sales"),
    )

    if any(t in message_raw for t in arabic_triggers):
        return True, "arabic_financial_or_autonomy_guarantee"

    if "dealix تضمن" in message_raw or "dealix guarantee" in mlc:
        return True, "brand_level_guarantee_claim"

    for a, b in latin_triggers:
        if a in mlc and (not b or b in mlc):
            return True, "latin_financial_claim"

    return False, None


def _priority_for(intent: str) -> str:
    if intent == "unsupported_financial_claim":
        return "p0"
    if intent in {"billing_question", "refund_or_discount", "technical_issue"}:
        return "p2"
    if intent in {"data_privacy", "security_question"}:
        return "p1"
    return "p3"


def _risk_for(intent: str) -> str:
    if intent == "unsupported_financial_claim":
        return "critical"
    if intent in {"data_privacy", "security_question", "refund_or_discount"}:
        return "high"
    if intent == "pricing_question":
        return "medium"
    return "low"


def analyze_support(message: str) -> SupportSignals:
    mlc = message.lower()

    red, code = _financial_guarantee_red_flag(message)
    intent = classify_intent(mlc)

    priority = _priority_for(intent)
    risk_level = _risk_for(intent)

    if red:
        intent = "unsupported_financial_claim"
        priority = _priority_for(intent)
        risk_level = _risk_for(intent)

    kb_hits = []
    arts = load_knowledge_articles()
    for art in arts:
        s = score_article_match(mlc, art)
        if s > 0:
            kb_hits.append((s, art))
    kb_hits.sort(key=lambda x: -x[0])
    top = [a for _, a in kb_hits[:2]]
    kb_ids = [str(a["id"]) for a in top if a.get("id")]

    if red:
        top = []
        kb_ids = []
        draft = (
            "⚠ مسودة وقائية: السؤال يتضمن وعداً أو ضماناً مالياً أو تبعاً غير مصرح له "
            "بموجب سياسة Dealix. لا نقدّم تعهدات آلية خارج قاعدة المعرفة المعتمدة. "
            f"رمز المراجعة: {code}"
        )
    elif top:
        best = top[0]
        body = str(best.get("answer_ar") or best.get("answer_en") or "")
        sources_line = ", ".join(kb_ids) if kb_ids else "kb"
        draft = (
            f"مسودة آلية للمراجعة — المصدر الداخلي: {sources_line}\n\n{body.strip()}"
        )
        if intent in {"unknown", "generic"}:
            draft += (
                "\n\nملاحظة: لم نستطع تصنيف دقيق — أحتاج موافقتك لتوسيع الإجابة خارج قاعدة المعرفة."
            )
    else:
        kb_ids = []
        draft = (
            "مسودة: لا توجد مقالة معتمدة تطابق السؤال بثقة؛ نصعّده للمراجعة اليدوية قبل أي رد خارجي."
        )

    escalation = None
    approval_need: ApprovalNeed = "founder_review"

    kb_auto_allow = (
        not red
        and intent != "unsupported_financial_claim"
        and risk_level == "low"
        and bool(top)
        and kb_auto_reply_allowed(intent=intent, risk_level=risk_level)
        and str(top[0].get("risk_level", "low")).lower() == "low"
    )

    if intent == "unsupported_financial_claim":
        escalation = (
            "مخاطرة حرجة — وعد أو ضمان تجاري أو تبعات أتمتة غير مصرح لها؛ "
            "يُرفض أي رد تلقائي ويُنشأ علم امتثال."
        )
        approval_need = "blocked_escalation"
        kb_auto_allow = False
    elif risk_level == "critical":
        escalation = "مخاطرة حرجة — حظر الإرسال التلقائي وإحالة المراجعة للمؤسس فورًا."
        approval_need = "blocked_escalation"
        kb_auto_allow = False
    elif risk_level == "high":
        escalation = (
            "مخاطرة عالية — يتوقف أي رد خارجي إلى موافقة بشرية."
        )
        approval_need = "blocked_escalation"
        kb_auto_allow = False
    elif intent in {"pricing_question"}:
        escalation = (
            "سؤال تسعير — نعرض النطاق فقط؛ أي التزام سعر يحتاج موافقة أساس الأسعار."
        )
        kb_auto_allow = False

    return SupportSignals(
        intent=intent,
        priority=priority,
        risk_level=risk_level,
        suggested_response_ar=draft.strip(),
        kb_source_ids=kb_ids,
        approval_need=approval_need,
        kb_auto_allow=kb_auto_allow,
        escalation_reason_ar=escalation,
    )
