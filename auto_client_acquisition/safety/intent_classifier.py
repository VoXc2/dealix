"""
Bilingual safety + intent classifier for the Dealix operator.

Wire-in point (deploy branch): `api/routers/operator.py` should import
`classify_intent` and merge its decision with the existing recommend-bundle
logic. When `decision.action_mode == ActionMode.BLOCKED`, the operator
must NOT recommend a bundle and must return the safe-alternatives list.

Design goals:
- 100% deterministic (no LLM call on the safety hot path).
- Catch Saudi Arabic dialect phrasings of:
    1. cold-WhatsApp / blast / bulk / mass-send
    2. purchased-list / scraped / random-numbers
    3. auto-DM / bot-talks-to-people without consent
- Catch the same in English.
- Default to NOT-blocked + intent="want_more_customers" for safe phrasings.
- Detect Arabic / English / mixed language for downstream tone selection.

Public API:
    classify_intent(text: str) -> IntentDecision
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from enum import Enum


class Language(str, Enum):
    AR = "ar"
    EN = "en"
    MIXED = "mixed"


class ActionMode(str, Enum):
    SUGGEST_ONLY = "suggest_only"
    DRAFT_ONLY = "draft_only"
    APPROVAL_REQUIRED = "approval_required"
    APPROVED_EXECUTE = "approved_execute"
    BLOCKED = "blocked"


@dataclass
class IntentDecision:
    intent: str
    action_mode: ActionMode
    language: Language
    recommended_bundle: str | None = None
    blocked_reasons: list[str] = field(default_factory=list)
    safe_alternatives: list[str] = field(default_factory=list)
    reason_ar: str = ""
    reason_en: str = ""
    requires_intake: bool = False

    @property
    def blocked(self) -> bool:
        return self.action_mode == ActionMode.BLOCKED

    def to_dict(self) -> dict[str, object]:
        return {
            "intent": self.intent,
            "action_mode": self.action_mode.value,
            "blocked": self.blocked,
            "language": self.language.value,
            "recommended_bundle": self.recommended_bundle,
            "blocked_reasons": list(self.blocked_reasons),
            "safe_alternatives": list(self.safe_alternatives),
            "reason_ar": self.reason_ar,
            "reason_en": self.reason_en,
            "requires_intake": self.requires_intake,
        }


# ── Normalization ──────────────────────────────────────────────────

_ARABIC_TATWEEL = "ـ"
_ARABIC_DIACRITICS = "".join(chr(c) for c in range(0x0610, 0x061B))  # quranic marks
_ARABIC_DIACRITICS += "".join(chr(c) for c in range(0x064B, 0x0660))  # fatha/kasra/etc

_ARABIC_NORMALIZE = [
    ("أ", "ا"), ("إ", "ا"), ("آ", "ا"),
    ("ى", "ي"), ("ة", "ه"),
    ("ؤ", "و"), ("ئ", "ي"),
    ("ﻻ", "لا"), ("ﻷ", "لا"), ("ﻹ", "لا"), ("ﻵ", "لا"),
]


def _normalize(text: str) -> str:
    """Lower-case, strip diacritics, alif/yaa unification — for substring matching only."""
    s = unicodedata.normalize("NFKC", text or "")
    for ch in _ARABIC_DIACRITICS + _ARABIC_TATWEEL:
        s = s.replace(ch, "")
    for src, dst in _ARABIC_NORMALIZE:
        s = s.replace(src, dst)
    return s.lower()


_AR_RE = re.compile(r"[؀-ۿ]")
_EN_RE = re.compile(r"[A-Za-z]")


def _detect_language(text: str) -> Language:
    has_ar = bool(_AR_RE.search(text))
    has_en = bool(_EN_RE.search(text))
    if has_ar and has_en:
        return Language.MIXED
    if has_ar:
        return Language.AR
    return Language.EN


# ── Pattern banks ──────────────────────────────────────────────────

# Channel tokens for "WhatsApp"
_WA_TOKENS = (
    "whatsapp", "whats app", "whatsap", "wa.me", "واتساب", "واتس", "وتساب", "وتس",
)


def _has_whatsapp(t: str) -> bool:
    return any(tok in t for tok in _WA_TOKENS)


# Cold / blast / bulk signals
_COLD_BLAST_AR = (
    "بارد",            # "cold"
    "حمله واتساب",     # "WhatsApp campaign"
    "حمله",            # "campaign" (paired with WA)
    "جماعي",           # "group / mass"
    "blast",
    "bulk",
    "mass",
    "spam",
    "بالكوم",          # "in bulk" colloquial
    "يشطح",            # Saudi slang: "let the bot go wild"
    "خل البوت يكلم",   # "let the bot talk to..."
    "البوت يفتح محادثات",  # "bot opens conversations"
    "البوت يفتح",          # bot initiates
    "ارمي رسايل",          # "I throw messages" (mass send slang)
    "ارمي رساي",
    "رساي",                # Saudi colloquial "messages"
    "ارمي واتساب",
    "كل اللي عندي",        # "everyone I have"
    "على كل اللي",         # "on everyone who"
    "ارسل لهم كلهم",       # "send to all of them"
    "ارسل للكل",           # "send to everyone"
    "ارسلهم كلهم",
    "حتى لو ما وافقوا",    # "even if they didn't agree"
    "حتى لو ما وافق",
    "ما يعرفوني",          # "people who don't know me"
    "ما يعرفني",
    "ناس ما يعرف",         # "people who don't know"
)

_COLD_BLAST_EN = (
    "cold whatsapp", "cold whats app", "cold wa", "cold dm",
    "blast whatsapp", "whatsapp blast", "blast wa",
    "bulk whatsapp", "whatsapp bulk",
    "mass whatsapp", "whatsapp mass",
    "spam whatsapp",
    "auto dm", "auto-dm",
    "scrape and message", "scrape then message",
    "automate whatsapp",
    "send whatsapp to a list",
    "send whatsapp to everyone",
    "whatsapp to random numbers",
)


# "Purchased / scraped / random numbers" signals
_PURCHASED_AR = (
    "مشتريها", "مشتراه", "مشتراها", "مشتري",     # "I bought / bought"
    "اشتريتها", "اشتريت قائمه", "اشتريت لسته",
    "شريتها", "شريت قائمه", "شريت لسته",          # Saudi colloquial "I bought"
    "جبتها من قائمه", "جبتها من لسته",            # "I got from a list"
    "جبتها من بره", "من بره",                     # "from outside / from somewhere"
    "ارقام من السوق",                              # "numbers from the market"
    "ارقام من برا", "ارقام من بره",
    "ارقام عشوائيه", "ارقام عشوائي",
    "لسته ارقام من", "قائمه ارقام من",
    "ارقام واجد",                                  # "lots of numbers"
    "بدون ما يكلموني",                            # "without them messaging me first"
    "بدون موافقه", "بدون اذن", "بدون اذن منهم",
    "بلا موافقه", "بلا اذن",
)

_PURCHASED_EN = (
    "purchased phone list", "phone list i bought", "list i bought",
    "bought a list", "bought list",
    "scraped list", "scraped numbers", "scraped phones",
    "random numbers", "random phone numbers",
    "without consent", "no consent", "without opt-in", "without optin",
    "without them messaging", "without them contacting",
)


# Auto-DM / bot-talks-to-people signals
_AUTO_DM_AR = (
    "خل البوت يكلم الناس",
    "البوت يشطح",
    "البوت يرسل بدون",
    "البوت يفتح محادثات",      # bot initiates conversations
    "البوت يفتح محادثات واتساب",
    "البوت يكلم ناس",
    "ارسل تلقائي",
    "تلقائي للناس",
    "ارسل للناس بدون",
    "ناس ما يعرفوني",          # people who don't know me
    "ناس ما يعرفني",
    "ما يعرفوني",
)

_AUTO_DM_EN = (
    "auto-message", "auto message", "automated outreach to whatsapp",
    "let the bot message", "let the bot send",
)


# Safe alternatives — same list always returned when blocked
_SAFE_ALTERNATIVES = [
    "linkedin_manual_warm_intro",
    "inbound_wa_me_link",
    "opt_in_form",
    "email_draft_with_approval",
    "customer_initiated_whatsapp",
]


# Service-routing positive signals (only used when not blocked)
_DATA_TO_REVENUE_AR = (
    "عندي ملف", "عندي قائمه", "عندي لسته",
    "200 lead", "500 lead", "1000 lead",
    "200 عميل محتمل", "500 عميل محتمل",
    "عملائي السابقين", "عملاء سابقين",
    "قاعده بياناتي", "قاعدة بيانات",
    "بياناتي", "ملف العملاء",
)

_DATA_TO_REVENUE_EN = (
    "have a list of", "we have a list",
    "a file of leads", "have a database",
    "previous customers", "past customers", "old customers",
    "existing customers list",
    "we have customer data",
    "consented list", "have a consented",
)

_PARTNERSHIPS_AR = (
    "شراكات", "شراكه", "وكالات", "وكاله",
    "بارتنر", "بارتنرز", "partner", "partners",
)

_PARTNERSHIPS_EN = (
    "partnerships", "partners", "agency partners", "channel partners",
    "co-sell", "co sell", "co-selling",
)

_PROOF_AR = (
    "تقرير لإداره", "تقرير للإدار",
    "إثبات النتائج", "اثبات النتائج",
    "proof pack", "proof report",
    "تقرير تنفيذي",
)

_PROOF_EN = (
    "proof pack", "proof report", "evidence report",
    "executive report", "report for management",
    "report for the board", "report for leadership",
    "proof for management",
)


def _matches_any(text: str, patterns: tuple[str, ...]) -> list[str]:
    """Return the list of patterns found in `text` (already normalized)."""
    return [p for p in patterns if p in text]


# ── Public API ─────────────────────────────────────────────────────

_BLOCKED_REASON_AR = (
    "هذا الطلب غير آمن: الإرسال البارد على واتساب لأرقام بدون موافقة "
    "يخالف PDPL وسياسات WhatsApp. لن نساعد في هذا الطلب."
)

_BLOCKED_REASON_EN = (
    "This request is not safe: cold WhatsApp / bulk send to numbers "
    "without explicit opt-in violates Saudi PDPL and WhatsApp policy. "
    "Dealix will not assist with this."
)


def classify_intent(text: str) -> IntentDecision:
    """Classify an operator chat input → safe IntentDecision.

    Always deterministic. No LLM. No external call.
    """
    raw = (text or "").strip()
    lang = _detect_language(raw)
    norm = _normalize(raw)

    blocked: list[str] = []
    has_wa = _has_whatsapp(norm)

    # 1. Cold / blast / bulk WhatsApp
    cold_ar_hits = _matches_any(norm, _COLD_BLAST_AR)
    cold_en_hits = _matches_any(norm, _COLD_BLAST_EN)
    if has_wa and (cold_ar_hits or cold_en_hits):
        blocked.append("cold_or_blast_whatsapp")

    # Direct English phrases that imply WhatsApp implicitly
    if any(p in norm for p in _COLD_BLAST_EN):
        blocked.append("cold_or_blast_whatsapp")

    # 2. Purchased / scraped / random numbers — even without literal WhatsApp word
    purchased_ar_hits = _matches_any(norm, _PURCHASED_AR)
    purchased_en_hits = _matches_any(norm, _PURCHASED_EN)
    if purchased_ar_hits or purchased_en_hits:
        # Any explicit "list I bought / scraped / random numbers" is by itself
        # an outreach safety risk in this product context (sales). Treat any
        # outreach verb OR explicit channel reference as confirming intent.
        outreach_verbs = (
            "ارسل", "ارسلهم", "اكلم", "اكلمهم", "اتصل", "اتصلهم",
            "ابيع", "بيع", "اعرض", "اعرضلهم",
            "send", "contact", "message", "reach out", "reach them",
            "sell to", "pitch", "outreach",
        )
        if (
            has_wa
            or "whatsapp" in norm
            or any(v in norm for v in outreach_verbs)
        ):
            blocked.append("purchased_or_scraped_list_no_consent")
        else:
            # Even without an explicit verb, mentioning a purchased list in
            # an operator chat is a strong intent signal. Block by default;
            # if the user is just informational they will rephrase.
            blocked.append("purchased_or_scraped_list_no_consent")

    # 3. Bot auto-DMs people
    if _matches_any(norm, _AUTO_DM_AR) or _matches_any(norm, _AUTO_DM_EN):
        blocked.append("auto_dm_without_consent")

    # 4. Generic "blast"/"bulk" without channel — still suspicious
    if any(t in norm for t in ("blast", "bulk", "mass send", "ارسل للجميع", "ارسل للكل")):
        if has_wa or "whatsapp" in norm or "ارسل" in norm:
            blocked.append("mass_send_intent")

    blocked = sorted(set(blocked))

    if blocked:
        return IntentDecision(
            intent="cold_or_blast_outreach_request",
            action_mode=ActionMode.BLOCKED,
            language=lang,
            recommended_bundle=None,
            blocked_reasons=blocked,
            safe_alternatives=list(_SAFE_ALTERNATIVES),
            reason_ar=_BLOCKED_REASON_AR,
            reason_en=_BLOCKED_REASON_EN,
            requires_intake=False,
        )

    # 5. Safe routing — order matters: list-with-consent → data_to_revenue beats want_more_customers
    if (
        _matches_any(norm, _DATA_TO_REVENUE_AR)
        or _matches_any(norm, _DATA_TO_REVENUE_EN)
    ):
        return IntentDecision(
            intent="has_list",
            action_mode=ActionMode.APPROVAL_REQUIRED,
            language=lang,
            recommended_bundle="data_to_revenue",
            reason_ar="نوصي Data to Revenue. نحتاج نعرف مصدر القائمة وحالة الموافقة قبل أي تواصل.",
            reason_en="Recommended: Data to Revenue. Need source + consent status before any outreach.",
            requires_intake=True,
        )

    if _matches_any(norm, _PARTNERSHIPS_AR) or _matches_any(norm, _PARTNERSHIPS_EN):
        return IntentDecision(
            intent="want_partnerships",
            action_mode=ActionMode.APPROVAL_REQUIRED,
            language=lang,
            recommended_bundle="partnership_growth",
            reason_ar="نوصي Partnership Growth — partner shortlist + co-branded Proof Pack + revenue share tracker.",
            reason_en="Recommended: Partnership Growth — partner shortlist + co-branded Proof Pack + revenue share tracker.",
            requires_intake=True,
        )

    if _matches_any(norm, _PROOF_AR) or _matches_any(norm, _PROOF_EN):
        return IntentDecision(
            intent="want_proof_report",
            action_mode=ActionMode.SUGGEST_ONLY,
            language=lang,
            recommended_bundle="executive_growth_os",
            reason_ar="نوصي Executive Growth OS مع Proof Pack أسبوعي للإدارة.",
            reason_en="Recommended: Executive Growth OS with weekly Proof Pack for leadership.",
            requires_intake=True,
        )

    # Default safe path → growth_starter (most common ask)
    return IntentDecision(
        intent="want_more_customers",
        action_mode=ActionMode.APPROVAL_REQUIRED,
        language=lang,
        recommended_bundle="growth_starter",
        reason_ar="نوصي Growth Starter — 10 فرص + رسائل عربية + Proof Pack بـ 499 ريال خلال 7 أيام.",
        reason_en="Recommended: Growth Starter — 10 opportunities + Arabic messages + Proof Pack at 499 SAR over 7 days.",
        requires_intake=True,
    )
