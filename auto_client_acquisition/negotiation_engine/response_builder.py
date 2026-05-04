"""
Response Builder — produces an Arabic suggested reply per objection class.

Outputs are *suggestions*; every reply must be reviewed + approved by a
human before going out (approval-first, no auto-send).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SuggestedResponse:
    objection_class: str
    response_ar: str
    next_step_ar: str
    proof_based: bool
    risk_note_ar: str | None = None


# Each response is anchored on PROOF (not promises) and pushes toward the
# 499 Pilot when applicable — matching the company's commercial wedge.
_RESPONSES: dict[str, SuggestedResponse] = {
    "price": SuggestedResponse(
        objection_class="price",
        response_ar=(
            "السعر يبدو مرتفعاً قبل ما تشوف Proof. نبدأ بـ Pilot 499 ريال لمدة 7 أيام: "
            "10 فرص + رسائل عربية + Proof Pack. إذا أقنعك الـ Proof نكمل شهرياً، "
            "وإذا لا تتوقف بدون التزام طويل."
        ),
        next_step_ar="أرسل عرض Pilot 499 + رابط intake الآمن.",
        proof_based=True,
        risk_note_ar="لا نعرض خصومات قبل أول Proof Pack — تكسر السعر التشغيلي.",
    ),
    "timing": SuggestedResponse(
        objection_class="timing",
        response_ar=(
            "أتفهم أن التوقيت مهم. خلّينا نبدأ بـ Free Diagnostic مجاني (24 ساعة) "
            "حتى نوثّق فرصكم وقتاً يناسبكم؛ هذا ما يلزم وقتاً تشغيلياً منكم، "
            "ونحتفظ بالنتيجة لما تكون جاهز للـ Pilot."
        ),
        next_step_ar="ابعث رابط Free Diagnostic + احجز callback بعد 30 يوماً.",
        proof_based=True,
    ),
    "trust": SuggestedResponse(
        objection_class="trust",
        response_ar=(
            "هذا اعتراض صحي. لذلك ما نطلب اشتراك مباشر — نطلب 499 لمدة 7 أيام، "
            "ونسلّم Proof Pack حقيقي بأرقام (فرص، رسائل، مخاطر تم منعها). "
            "بعدها أنت من يقرر."
        ),
        next_step_ar="شارك Proof Pack sample + اطلب reference call.",
        proof_based=True,
    ),
    "already_have_agency": SuggestedResponse(
        objection_class="already_have_agency",
        response_ar=(
            "ممتاز — Dealix مكمّل لوكالتك وليس بديلاً. نشغّل لكم Pilot على عميل واحد "
            "مع Co-branded Proof Pack باسمكم. Revenue share متتبع إذا اخترتم "
            "Agency Partner Program."
        ),
        next_step_ar="حوّله لـ Agency Partner Pilot على عميل واحد.",
        proof_based=True,
        risk_note_ar="لا تدخل في exclusivity مبكر، ولا تتعهد revenue share بدون referral متتبع.",
    ),
    "need_team_approval": SuggestedResponse(
        objection_class="need_team_approval",
        response_ar=(
            "أرسلك Proof Pack sample + نسخة 30 ثانية للمجلس + رابط Free Diagnostic "
            "حتى تشاركه معهم بدون التزام."
        ),
        next_step_ar="جهّز deck مختصر + Proof sample + احجز اجتماع للفريق خلال أسبوع.",
        proof_based=True,
    ),
    "not_priority": SuggestedResponse(
        objection_class="not_priority",
        response_ar=(
            "مفهوم. أحتفظ بـ Diagnostic مجاني لكم، وأرجع لكم بعد 30 يوماً مع شريحة "
            "محدّثة. لا outbound في هذه الفترة — نحترم وقتكم."
        ),
        next_step_ar="جدول follow-up بعد 30 يوماً + سجّل reason='not_priority'.",
        proof_based=False,
    ),
    "send_details": SuggestedResponse(
        objection_class="send_details",
        response_ar=(
            "أرسل لكم 3 ملفات: (1) Proof Pack sample، (2) Pilot 499 توضيح، "
            "(3) Free Diagnostic intake. إذا أعجبتكم العينة نبدأ خلال 24 ساعة."
        ),
        next_step_ar="أرسل deck + Proof sample + رابط intake.",
        proof_based=True,
    ),
    "want_guarantee": SuggestedResponse(
        objection_class="want_guarantee",
        response_ar=(
            "Dealix لا يضمن نتائج محددة — نضمن Proof Pack بأرقام حقيقية (فرص، رسائل، "
            "مخاطر تم منعها، أثر تقديري على الإيراد). الضمان الحقيقي هو الشفافية، "
            "وليس وعد رقم."
        ),
        next_step_ar="حوّله لـ Pilot 499 + اشرح Proof Pack as deliverable.",
        proof_based=True,
        risk_note_ar="لا تستخدم 'نضمن' أو 'guaranteed' في أي رد — يكسر forbidden_claims_audit.",
    ),
}


def build_response(objection_class: str) -> SuggestedResponse | None:
    return _RESPONSES.get(objection_class)


def all_responses() -> tuple[SuggestedResponse, ...]:
    return tuple(_RESPONSES.values())
