#!/usr/bin/env python3
"""
Dealix Account Intelligence — shared library.

Single source of truth for the five launch systems, the scoring models, the
evidence/contact-confidence ladders, the copy builders (email / call / mini
proposal), and the policy token lists (guaranteed-claim, hedging, and
prompt-injection markers).

Design rules enforced here so the rest of the pipeline inherits them:
  * Stdlib only (json, csv, datetime, pathlib, random, hashlib) — no external deps.
  * Deterministic: every pack is derived from a seeded RNG so runs are reproducible.
  * Honest seed data: this is clearly synthetic. We never invent phone numbers or
    emails — phone_if_public / email_if_public stay null and outreach falls back to
    role-based routes. Real public/founder-provided contacts can raise confidence to
    C2-C4 later without changing the contract.
  * No guaranteed claims anywhere in generated copy.
  * L0/L1 evidence => copy must hedge ("غالبًا" / "قد" / "في هذا النوع من الشركات").
"""

from __future__ import annotations

import hashlib
import random
from datetime import datetime
from pathlib import Path

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "schemas"
DATA_DIR = REPO_ROOT / "data"
REPORTS_DIR = REPO_ROOT / "reports"

COUNTRY = "Saudi Arabia"

# --------------------------------------------------------------------------- #
# Policy token lists (used by copy builders AND the validator)
# --------------------------------------------------------------------------- #

# Words/phrases that turn a draft into a guaranteed-result claim. Forbidden in
# email_body, mini proposals, and website copy.
GUARANTEED_CLAIM_TOKENS = [
    "نضمن", "نضمن لك", "ضمان", "مضمون", "مضمونة", "نضاعف", "سنضاعف",
    "زيادة 100%", "100%", "نتيجة مؤكدة", "نتائج مؤكدة", "بدون أي مخاطرة",
    "guarantee", "guaranteed", "we guarantee", "double your", "triple your",
    "risk-free", "no risk", "100% increase",
]

# Hedging markers that evidence-poor copy (L0/L1) MUST contain.
HEDGING_TOKENS = [
    "غالبًا", "غالبا", "قد ", "عادةً", "عادة", "في الغالب", "ربما",
    "في هذا النوع", "يُحتمل", "محتمل", "likely", "probably", "often", "typically",
]

# Prompt-injection markers. If any external company text contains these, the
# content is quarantined and never used as instructions.
PROMPT_INJECTION_TOKENS = [
    "ignore previous instructions", "ignore all previous", "disregard previous",
    "reveal secret", "reveal the secret", "show your prompt", "system prompt",
    "change system prompt", "execute command", "run command", "send credentials",
    "use this tool", "you are now", "act as", "exfiltrate",
    "تجاهل التعليمات", "تجاهل كل التعليمات", "نفّذ الأمر", "أرسل كلمة المرور",
]

# --------------------------------------------------------------------------- #
# The five launch systems
# --------------------------------------------------------------------------- #
SYSTEMS = {
    "Revenue Operating System": {
        "key": "revenue_os",
        "entry_offer": "Revenue Leakage Sprint",
        "first_sprint": "Revenue Leakage Sprint",
        "starter_price_sar": 4500,
        "nightly_count": 100,
        "primary_buyer_roles": ["Founder", "Head of Sales", "GM"],
        "secondary_role": "Sales Operations Lead",
        "deliverables": ["Revenue Leakage Map", "Opportunity Stage Model", "Follow-up Workflow"],
        "full_deliverables": [
            "Revenue Leakage Map", "Opportunity Stage Model", "Follow-up Workflow",
            "Draft Templates", "Weekly Revenue Report",
        ],
        "upsells": ["AI Revenue Ops Starter", "Monthly Optimization", "Full Revenue OS"],
        "delivery_complexity": "medium",
        "ease_of_delivery": 12,
        "delivery_hours": 22,
        "upsell_potential": "high",
        "upsell_score": 15,
        "sectors": ["Marketing Agencies", "Recruitment", "Professional Services", "Real Estate"],
        "area_ar": "خط الإيرادات والمتابعة",
        "surface_ar": "عدد العملاء المحتملين",
    },
    "Executive Command OS": {
        "key": "executive_command_os",
        "entry_offer": "Daily Command Sprint",
        "first_sprint": "Daily Command Sprint",
        "starter_price_sar": 5500,
        "nightly_count": 70,
        "primary_buyer_roles": ["Founder", "CEO", "GM"],
        "secondary_role": "Executive Assistant",
        "deliverables": ["KPI Map", "Daily Command Report", "Risk/Priority Matrix"],
        "full_deliverables": [
            "KPI Map", "Daily Command Report", "Risk/Priority Matrix",
            "Decision Log", "Executive Action Board",
        ],
        "upsells": ["Executive Dashboard", "Finance OS", "Delivery & Operations OS"],
        "delivery_complexity": "medium",
        "ease_of_delivery": 16,
        "delivery_hours": 20,
        "upsell_potential": "high",
        "upsell_score": 14,
        "sectors": ["Professional Services", "Logistics", "Clinics", "Marketing Agencies"],
        "area_ar": "قرارات الإدارة اليومية",
        "surface_ar": "كثرة التقارير",
    },
    "Follow-up Recovery OS": {
        "key": "followup_recovery_os",
        "entry_offer": "7-Day Follow-up Recovery Sprint",
        "first_sprint": "7-Day Follow-up Recovery Sprint",
        "starter_price_sar": 3500,
        "nightly_count": 90,
        "primary_buyer_roles": ["Sales Manager", "Marketing Manager", "Founder"],
        "secondary_role": "Customer Service Lead",
        "deliverables": ["Follow-up Queue", "Lead Status Model", "Recovery Report"],
        "full_deliverables": [
            "Follow-up Queue", "Lead Status Model", "Message Set",
            "Recovery Report", "Escalation Rules",
        ],
        "upsells": ["Revenue OS", "WhatsApp Client OS", "Monthly Follow-up Optimization"],
        "delivery_complexity": "low",
        "ease_of_delivery": 18,
        "delivery_hours": 14,
        "upsell_potential": "medium",
        "upsell_score": 11,
        "sectors": ["Training Companies", "Real Estate", "Clinics", "Marketing Agencies", "Recruitment"],
        "area_ar": "متابعة العملاء المحتملين",
        "surface_ar": "عدد الاستفسارات",
    },
    "WhatsApp Client OS": {
        "key": "whatsapp_client_os",
        "entry_offer": "WhatsApp Flow Sprint",
        "first_sprint": "WhatsApp Flow Sprint",
        "starter_price_sar": 4500,
        "nightly_count": 70,
        "primary_buyer_roles": ["Operations", "Customer Service", "Founder"],
        "secondary_role": "Marketing Manager",
        "deliverables": ["WhatsApp Flow Map", "Readiness Scan", "Human Handoff Policy"],
        "full_deliverables": [
            "WhatsApp Flow Map", "Readiness Scan", "Action Cards",
            "Human Handoff Policy", "Secure Portal Handoff",
        ],
        "upsells": ["Client Portal", "Support Quality OS", "Customer Success OS"],
        "delivery_complexity": "high",
        "ease_of_delivery": 10,
        "delivery_hours": 26,
        "upsell_potential": "medium",
        "upsell_score": 12,
        "sectors": ["Clinics", "Real Estate", "Training Companies", "Recruitment"],
        "area_ar": "محادثات العملاء عبر واتساب",
        "surface_ar": "سرعة الرد",
    },
    "Proposal & Proof OS": {
        "key": "proposal_proof_os",
        "entry_offer": "Proposal & Proof Sprint",
        "first_sprint": "Proposal & Proof Sprint",
        "starter_price_sar": 3000,
        "nightly_count": 70,
        "primary_buyer_roles": ["Founder", "Partner", "BD", "Sales Lead"],
        "secondary_role": "Proposal Writer",
        "deliverables": ["Proposal Template", "Proof Pack Template", "Next-step Card"],
        "full_deliverables": [
            "Proposal Template", "Proof Pack Template", "Scope / Out-of-scope",
            "Risk & Assumption Block", "Next-step Card",
        ],
        "upsells": ["Proof Library", "Sales Enablement OS", "Revenue OS"],
        "delivery_complexity": "low",
        "ease_of_delivery": 20,
        "delivery_hours": 10,
        "upsell_potential": "medium",
        "upsell_score": 10,
        "sectors": ["Professional Services", "Marketing Agencies", "Training Companies"],
        "area_ar": "إعداد العروض وإثبات القيمة",
        "surface_ar": "عدد العروض المرسلة",
    },
}

SYSTEM_NAMES = list(SYSTEMS.keys())

# --------------------------------------------------------------------------- #
# Sectors → subsectors, pains, decision-maker roles, ability-to-pay bias
# --------------------------------------------------------------------------- #
SECTORS = {
    "Marketing Agencies": {
        "subsectors": ["Performance Marketing", "Branding Studio", "Social Media Agency", "Full-service Agency"],
        "decision_maker": "Founder / CEO",
        "ability_bias": "medium",
        "pains": [
            "بطء متابعة العملاء المحتملين بعد أول رد",
            "غياب صورة واضحة عن مراحل الصفقة",
            "اعتماد المتابعة على اجتهاد الفريق بدون نظام",
            "صعوبة إثبات النتائج للعملاء",
        ],
        "model_hint": "خدمات تسويقية بعقود شهرية ومشاريع",
        "services": ["إدارة حملات", "تصميم", "محتوى", "إدارة حسابات"],
    },
    "Training Companies": {
        "subsectors": ["Corporate Training", "Professional Courses", "Online Academy", "Bootcamps"],
        "decision_maker": "CEO / Head of Sales",
        "ability_bias": "medium",
        "pains": [
            "ضياع استفسارات التسجيل عبر واتساب بدون متابعة",
            "فجوة بين الاستفسار والتسجيل الفعلي",
            "تكرار نفس الأسئلة بدون نظام رد منظم",
            "حملات موسمية تنتهي بدون متابعة منهجية",
        ],
        "model_hint": "برامج تدريبية بالتسجيل والدُفعات",
        "services": ["دورات", "برامج شركات", "شهادات", "ورش"],
    },
    "Clinics": {
        "subsectors": ["Dental", "Dermatology", "General Practice", "Aesthetic"],
        "decision_maker": "Operations Manager / Owner",
        "ability_bias": "high",
        "pains": [
            "استفسارات واتساب كثيرة بدون رد منظم",
            "مواعيد تضيع بسبب بطء التأكيد",
            "غياب متابعة بعد أول استفسار",
            "صعوبة قياس مصدر الحجوزات",
        ],
        "model_hint": "خدمات طبية بالمواعيد والحجوزات",
        "services": ["حجوزات", "استشارات", "متابعة مرضى"],
    },
    "Real Estate": {
        "subsectors": ["Brokerage", "Developer", "Property Management", "Off-plan Sales"],
        "decision_maker": "Sales Manager / Owner",
        "ability_bias": "high",
        "pains": [
            "عملاء محتملون كثر بدون متابعة منظمة",
            "بطء الرد على استفسارات الوحدات",
            "غياب نظام لترتيب أولوية العملاء",
            "تشتت قنوات التواصل بين الفريق",
        ],
        "model_hint": "بيع/تأجير عقارات بعمولات ودورات بيع طويلة",
        "services": ["وساطة", "تطوير", "إدارة أملاك"],
    },
    "Professional Services": {
        "subsectors": ["Consulting", "Legal", "Accounting", "Engineering"],
        "decision_maker": "Partner / Managing Director",
        "ability_bias": "high",
        "pains": [
            "عروض تُكتب من الصفر في كل مرة",
            "غياب إثبات قيمة منظم في العروض",
            "صفقات تتعطل في مرحلة العرض",
            "صعوبة رؤية المدير لحالة الأعمال يوميًا",
        ],
        "model_hint": "خدمات مهنية بمشاريع وعقود استشارية",
        "services": ["استشارات", "عقود", "مشاريع", "تقارير"],
    },
    "Recruitment": {
        "subsectors": ["Staffing", "Executive Search", "HR Outsourcing", "Talent Tech"],
        "decision_maker": "Founder / BD Lead",
        "ability_bias": "medium",
        "pains": [
            "متابعة العملاء والمرشحين بدون نظام موحد",
            "ضياع طلبات التوظيف بين القنوات",
            "بطء تحويل الطلب إلى عقد",
            "غياب رؤية واضحة لمراحل الصفقة",
        ],
        "model_hint": "توظيف بعمولات وعقود خدمة",
        "services": ["توظيف", "بحث تنفيذي", "خدمات موارد بشرية"],
    },
    "Logistics": {
        "subsectors": ["Last-mile Delivery", "Freight", "Warehousing", "3PL"],
        "decision_maker": "Operations Director / GM",
        "ability_bias": "high",
        "pains": [
            "غياب لوحة قرار يومية للإدارة",
            "تشتت المؤشرات التشغيلية",
            "بطء رصد المخاطر التشغيلية",
            "صعوبة ترتيب الأولويات اليومية",
        ],
        "model_hint": "خدمات لوجستية بعقود تشغيل",
        "services": ["توصيل", "شحن", "تخزين", "تشغيل"],
    },
}

SECTOR_NAMES = list(SECTORS.keys())

CITIES = [
    "Riyadh", "Jeddah", "Dammam", "Khobar", "Mecca", "Medina", "Tabuk",
    "Abha", "Buraydah", "Hail", "Jubail", "Yanbu", "Taif", "Najran", "Qassim",
]

# Synthetic (clearly fictional) company-name word banks. Seed data only.
NAME_PREFIX = [
    "Nova", "Peak", "Bright", "Atlas", "Vertex", "Orbit", "Pulse", "Summit",
    "Zenith", "Falcon", "Cedar", "Dunes", "Najd", "Tuwaiq", "Sahary", "Rua",
    "Mada", "Ufuq", "Qimam", "Masar", "Tamayuz", "Ru'ya", "Ittiqan", "Manarah",
]
NAME_SUFFIX_BY_SECTOR = {
    "Marketing Agencies": ["Agency", "Studio", "Media", "Collective"],
    "Training Companies": ["Academy", "Training", "Institute", "Learning"],
    "Clinics": ["Clinic", "Medical", "Care", "Health"],
    "Real Estate": ["Real Estate", "Properties", "Realty", "Development"],
    "Professional Services": ["Consulting", "Partners", "Advisory", "Group"],
    "Recruitment": ["Talent", "Recruitment", "Staffing", "HR"],
    "Logistics": ["Logistics", "Freight", "Supply", "Transport"],
}

# --------------------------------------------------------------------------- #
# Evidence & contact ladders (sub-scores)
# --------------------------------------------------------------------------- #
EVIDENCE_LEVELS = ["L0", "L1", "L2", "L3", "L4"]
EVIDENCE_PAIN_CLARITY = {"L0": 8, "L1": 14, "L2": 20, "L3": 23, "L4": 25}
EVIDENCE_TOP100_SCORE = {"L0": 2, "L1": 4, "L2": 6, "L3": 8, "L4": 10}

CONTACT_LEVELS = ["C0", "C1", "C2", "C3", "C4"]
CONTACT_TOP100_SCORE = {"C0": 4, "C1": 10, "C2": 15, "C3": 18, "C4": 20}
CONTACT_CASH_SCORE = {"C0": 3, "C1": 8, "C2": 12, "C3": 14, "C4": 15}

ABILITY_TOP100 = {"low": 5, "medium": 10, "high": 15}
ABILITY_CASH = {"low": 9, "medium": 17, "high": 25}
URGENCY_CASH = {"low": 8, "medium": 16, "high": 25}
RISK_LOW_SCORE = {"low": 10, "medium": 6, "high": 0}
UPSELL_HINT = {"low": 6, "medium": 11, "high": 15}


def _hedge_ok(text: str) -> bool:
    return any(tok in text for tok in HEDGING_TOKENS)


def has_guaranteed_claim(text: str) -> bool:
    low = text.lower()
    return any(tok.lower() in low for tok in GUARANTEED_CLAIM_TOKENS)


def has_injection_marker(text: str) -> bool:
    low = text.lower()
    return any(tok.lower() in low for tok in PROMPT_INJECTION_TOKENS)


# --------------------------------------------------------------------------- #
# Copy builders
# --------------------------------------------------------------------------- #
def build_email(pack: dict) -> tuple[str, str]:
    """Build an evidence-aware Arabic outreach email that satisfies the gate:
    company context, likely pain, ONE system, first sprint, exactly 3 deliverables,
    one CTA, hedged language for L0/L1, no guaranteed claims."""
    sys = SYSTEMS[pack["recommended_system"]]
    company = pack["company_name"]
    sector_ar = pack["sector"]
    city = pack["city"]
    role = pack["likely_decision_maker_role"].split("/")[0].strip()
    pains = pack["_pain_list"][:3]
    deliverables = sys["deliverables"][:3]

    subject = f"فكرة لتحسين {sys['area_ar']} في {company}"

    if pack["evidence_level"] in ("L0", "L1"):
        context = (
            f"راجعت حضور {company} ضمن قطاع {sector_ar} في {city}، "
            f"وفي هذا النوع من الشركات غالبًا لا يكون التحدي في {sys['surface_ar']} فقط، "
            f"بل في تنظيم {sys['area_ar']}."
        )
        pain_intro = "وغالبًا تظهر التحديات في:"
    else:
        context = (
            f"راجعت {pack['signal_source']} الخاص بـ{company}، ولاحظت {pack['buying_signal']}."
        )
        pain_intro = "ويبدو أن أبرز نقاط التحسين هي:"

    body_lines = [
        f"السلام عليكم {role} في {company}،",
        "",
        context,
        "",
        pain_intro,
        f"- {pains[0]}",
        f"- {pains[1] if len(pains) > 1 else pains[0]}",
        f"- {pains[2] if len(pains) > 2 else pains[0]}",
        "",
        f"لذلك أعتقد أن أنسب نظام لكم من Dealix هو: {pack['recommended_system']}.",
        f"نبدأ بـ{sys['first_sprint']}، ومخرجه خلال أيام يكون:",
        f"- {deliverables[0]}",
        f"- {deliverables[1]}",
        f"- {deliverables[2]}",
        "",
        "إذا مناسب، أرسل لكم Mini Proposal من صفحة واحدة يوضح التصور والسعر الافتتاحي والمتطلبات.",
    ]
    return subject, "\n".join(body_lines)


def build_call(pack: dict) -> tuple[str, list[str], list[dict]]:
    sys = SYSTEMS[pack["recommended_system"]]
    pain_short = pack["_pain_list"][0]
    opener = (
        f"السلام عليكم، معك فريق Dealix. أرسلنا لكم رسالة مختصرة بخصوص {pack['recommended_system']}. "
        f"الفكرة ليست مشروعًا ضخمًا من البداية، بل {sys['first_sprint']} صغير يوضح هل {pain_short} "
        f"عندكم يستحق التنظيم أو لا. سؤالي السريع: هل {sys['area_ar']} عندكم يمشي بنظام واضح، "
        f"أو يعتمد غالبًا على اجتهاد الفريق؟"
    )
    questions = [
        f"كيف تتعاملون حاليًا مع {sys['area_ar']}؟",
        f"ما حجم التأثير لو تحسّن {pain_short} عندكم؟",
        "من المسؤول عن هذا الجانب اليوم، ومن يقرر تجربة أداة جديدة؟",
    ]
    objections = [
        {"objection": "عندنا فريق يكفي", "response": f"ممتاز، {sys['first_sprint']} يدعم فريقكم ولا يستبدله، ويعطيهم نظامًا أوضح."},
        {"objection": "مشغولين حاليًا", "response": "لذلك نبدأ بمخرج صغير خلال أيام بدون التزام طويل."},
        {"objection": "كم السعر؟", "response": f"السعر الافتتاحي للـSprint يبدأ من {sys['starter_price_sar']} ريال، وأرسل لكم Mini Proposal يوضح التفاصيل."},
    ]
    return opener, questions, objections


def build_mini_proposal_fields(pack: dict) -> dict:
    sys = SYSTEMS[pack["recommended_system"]]
    company = pack["company_name"]
    if pack["evidence_level"] in ("L0", "L1"):
        public_signal = f"إشارة قطاعية: شركات {pack['sector']} في {pack['city']} غالبًا تواجه {pack['_pain_list'][0]}."
    else:
        public_signal = f"{pack['signal_source']}: {pack['buying_signal']}."
    return {
        "title": f"Mini Proposal — {pack['recommended_system']} لـ{company}",
        "recommended_system": pack["recommended_system"],
        "public_signal": public_signal,
        "likely_pain": pack["likely_pain"],
        "why_this_system": pack["why_this_system"],
        "first_sprint": sys["first_sprint"],
        "deliverables": list(sys["full_deliverables"]),
        "timeline": "3 إلى 5 أيام عمل",
        "starter_price_sar": sys["starter_price_sar"],
        "required_inputs": pack["required_inputs"],
        "expected_first_proof": pack["proof_angle"],
        "risks_assumptions": [
            "النتائج تعتمد على جودة المدخلات المقدمة من العميل.",
            "Sprint تشخيصي أولًا؛ لا نعد بأرقام مضمونة.",
        ],
        "next_step": "مراجعة المؤسس واعتماد الإرسال، ثم جلسة مدخلات قصيرة.",
        "approval_required": True,
    }


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #
def compute_account_score(pack: dict) -> tuple[int, dict]:
    """Top-100 ranking score, out of 100."""
    sys = SYSTEMS[pack["recommended_system"]]
    # system fit: primary sector for this system => 20, otherwise 15/10
    if pack["sector"] in sys["sectors"][:2]:
        fit = 20
    elif pack["sector"] in sys["sectors"]:
        fit = 17
    else:
        fit = 11
    breakdown = {
        "pain_clarity": EVIDENCE_PAIN_CLARITY[pack["evidence_level"]],
        "contact_availability": CONTACT_TOP100_SCORE[pack["contact_confidence"]],
        "system_fit": fit,
        "ability_to_pay_signal": ABILITY_TOP100[pack["ability_to_pay"]],
        "evidence_level": EVIDENCE_TOP100_SCORE[pack["evidence_level"]],
        "low_risk": RISK_LOW_SCORE[pack["risk_level"]],
    }
    return sum(breakdown.values()), breakdown


def compute_cash_priority(pack: dict) -> tuple[int, dict]:
    """Cash Priority Score, out of 100."""
    sys = SYSTEMS[pack["recommended_system"]]
    breakdown = {
        "ability_to_pay": ABILITY_CASH[pack["ability_to_pay"]],
        "urgency": URGENCY_CASH[pack["urgency"]],
        "ease_of_delivery": sys["ease_of_delivery"],
        "upsell_potential": sys["upsell_score"],
        "contact_availability": CONTACT_CASH_SCORE[pack["contact_confidence"]],
    }
    return sum(breakdown.values()), breakdown


def account_bucket(score: int) -> str:
    if score >= 85:
        return "top_priority"
    if score >= 75:
        return "approval_queue"
    if score >= 65:
        return "more_research"
    return "reject_nurture"


def top100_exclusions(pack: dict) -> list[str]:
    """Hard exclusions that keep an account out of the Top-100 queue."""
    reasons = []
    if not pack.get("recommended_system"):
        reasons.append("no_recommended_system")
    if not pack.get("best_contact_route"):
        reasons.append("no_contact_route")
    if pack.get("risk_level") == "high":
        reasons.append("risk_high")
    if not pack.get("evidence_level"):
        reasons.append("missing_evidence_level")
    if pack.get("do_not_contact") or pack.get("status") == "suppressed":
        reasons.append("suppression_do_not_contact")
    if has_guaranteed_claim(pack.get("email_body", "")):
        reasons.append("guaranteed_claim_in_email")
    # pain stated as fact without evidence (L0/L1 must hedge)
    if pack.get("evidence_level") in ("L0", "L1") and not _hedge_ok(pack.get("likely_pain", "")):
        reasons.append("pain_as_fact_without_evidence")
    return reasons


# --------------------------------------------------------------------------- #
# Deterministic pack generation
# --------------------------------------------------------------------------- #
def _rng_for(seed: int, salt: str) -> random.Random:
    h = hashlib.sha256(f"{seed}:{salt}".encode("utf-8")).hexdigest()
    return random.Random(int(h[:16], 16))


def _weighted(rng: random.Random, choices: list, weights: list):
    return rng.choices(choices, weights=weights, k=1)[0]


def _slug(name: str) -> str:
    return name.lower().replace(" ", "").replace("'", "").replace("&", "and")


def generate_packs(seed: int = 20260603, run_date: str | None = None) -> list[dict]:
    """Generate the full nightly set across all systems using the configured
    nightly distribution (Revenue 100, Follow-up 90, Executive 70, WhatsApp 70,
    Proposal 70 = 400)."""
    run_date = run_date or datetime.now().strftime("%Y-%m-%d")
    # Deterministic: derived from run_date so same (seed, run_date) => byte-identical
    # data. Wall-clock time lives only in the human-facing report footers.
    generated_at = f"{run_date}T00:00:00+03:00"
    packs: list[dict] = []
    used_names: set[str] = set()
    counter = 0

    for system_name, sys in SYSTEMS.items():
        for i in range(sys["nightly_count"]):
            counter += 1
            rng = _rng_for(seed, f"{sys['key']}:{i}")

            sector = rng.choice(sys["sectors"])
            sec = SECTORS[sector]
            subsector = rng.choice(sec["subsectors"])
            city = rng.choice(CITIES)

            # synthetic, unique fictional company name
            for _ in range(50):
                prefix = rng.choice(NAME_PREFIX)
                suffix = rng.choice(NAME_SUFFIX_BY_SECTOR[sector])
                name = f"{prefix} {suffix}"
                if name not in used_names:
                    used_names.add(name)
                    break
            else:
                name = f"{prefix} {suffix} {counter}"
                used_names.add(name)

            website = f"www.{_slug(prefix + suffix)}.sa"

            evidence = _weighted(rng, EVIDENCE_LEVELS, [28, 44, 20, 6, 2])
            contact_conf = _weighted(rng, ["C0", "C1"], [42, 58])  # seed has no confirmed/published contacts
            risk = _weighted(rng, ["low", "medium", "high"], [68, 27, 5])
            ability = sec["ability_bias"]
            ability = _weighted(rng, ["low", "medium", "high"],
                                {"low": [50, 35, 15], "medium": [20, 55, 25], "high": [10, 35, 55]}[ability])
            urgency = _weighted(rng, ["low", "medium", "high"], [30, 45, 25])

            pains = rng.sample(sec["pains"], k=min(3, len(sec["pains"])))
            likely_pain_core = pains[0]
            # L0/L1 must hedge in the likely_pain string itself
            if evidence in ("L0", "L1"):
                likely_pain = f"غالبًا: {likely_pain_core}"
            else:
                likely_pain = f"بحسب {SECTORS[sector]['model_hint']}: {likely_pain_core}"

            missing_contact = contact_conf == "C0"
            best_route = "role_based_outreach" if contact_conf == "C0" else \
                _weighted(rng, ["contact_form", "public_social"], [60, 40])

            # buying signal / source depend on evidence
            if evidence in ("L0", "L1"):
                buying_signal = f"نمط قطاعي محتمل في {sector}"
                signal_source = "تحليل قطاعي عام" if evidence == "L0" else "الموقع الرسمي"
            elif evidence == "L2":
                buying_signal = "صفحة خدمات تشير إلى توسّع في الطلب"
                signal_source = "صفحة الخدمات/التواصل العامة"
            elif evidence == "L3":
                buying_signal = "أكثر من مصدر عام يشير إلى نمو الفريق"
                signal_source = "مصادر عامة متعددة متوافقة"
            else:
                buying_signal = "بيانات زوّدنا بها العميل عن تحدي المتابعة"
                signal_source = "بيانات من العميل/المؤسس"

            do_not_contact = False
            status = "researched"
            # exercise the suppression path on a small, deterministic subset
            if counter % 140 == 0:
                do_not_contact = True
                status = "suppressed"

            pack = {
                "pack_id": f"AP-{counter:06d}",
                "generated_at": generated_at,
                "run_date": run_date,
                "company_name": name,
                "website": website,
                "country": COUNTRY,
                "city": city,
                "sector": sector,
                "subsector": subsector,
                "services_detected": list(sec["services"]),
                "business_model_hint": sec["model_hint"],
                "public_contact_channels": ([] if contact_conf == "C0" else [best_route]),
                "phone_if_public": None,
                "email_if_public": None,
                "contact_page_url": None,
                "social_links": [],
                "google_business_hint": None,
                "likely_decision_maker_role": sec["decision_maker"],
                "secondary_contact_role": sys["secondary_role"],
                "best_contact_route": best_route,
                "contact_confidence": contact_conf,
                "buying_signal": buying_signal,
                "signal_source": signal_source,
                "likely_pain": likely_pain,
                "recommended_system": system_name,
                "why_this_system": (
                    f"يعالج {sys['area_ar']} مباشرةً، وهو أنسب نظام لـ{sector} في هذه المرحلة."
                ),
                "first_sprint_offer": sys["first_sprint"],
                "proof_angle": f"أول مخرج ملموس: {sys['deliverables'][0]} خلال أيام.",
                "delivery_pack": list(sys["full_deliverables"]),
                "required_inputs": [
                    "وصف مختصر للوضع الحالي",
                    "عينة من قنوات التواصل/الاستفسارات",
                    "تحديد المسؤول ومقياس النجاح",
                ],
                "acceptance_criteria": [
                    f"تسليم {sys['deliverables'][0]} ومراجعته مع العميل",
                    "اتفاق على مقياس نجاح واحد واضح",
                    "خطة خطوة تالية معتمدة",
                ],
                "risk_level": risk,
                "evidence_level": evidence,
                "ability_to_pay": ability,
                "urgency": urgency,
                "owner": "founder",
                "do_not_contact": do_not_contact,
                "missing_contact": missing_contact,
                "status": status,
                # internal helper (not part of schema; stripped before write)
                "_pain_list": pains,
            }

            # copy
            subject, body = build_email(pack)
            pack["email_subject"] = subject
            pack["email_body"] = body
            opener, questions, objections = build_call(pack)
            pack["call_opener"] = opener
            pack["call_questions"] = questions
            pack["expected_objections"] = objections
            pack["mini_proposal_title"] = f"Mini Proposal — {system_name} لـ{name}"
            pack["mini_proposal_angle"] = (
                f"تشخيص سريع لـ{sys['area_ar']} ثم أول مخرج ملموس عبر {sys['first_sprint']}."
            )

            # scores
            acc_score, acc_breakdown = compute_account_score(pack)
            cash_score, cash_breakdown = compute_cash_priority(pack)
            pack["account_score"] = acc_score
            pack["account_score_breakdown"] = acc_breakdown
            pack["cash_priority_score"] = cash_score
            pack["cash_priority_breakdown"] = cash_breakdown

            # next action
            if do_not_contact:
                pack["next_action"] = "suppress_do_not_contact"
            elif missing_contact:
                pack["next_action"] = "verify_public_contact"
            elif acc_score >= 85:
                pack["next_action"] = "queue_email_for_founder_approval"
            elif acc_score >= 75:
                pack["next_action"] = "review_in_approval_queue"
            elif acc_score >= 65:
                pack["next_action"] = "more_research_or_rewrite"
            else:
                pack["next_action"] = "nurture"

            packs.append(pack)

    return packs


def strip_internal(pack: dict) -> dict:
    """Remove helper keys (prefixed with _) before serialising to the contract."""
    return {k: v for k, v in pack.items() if not k.startswith("_")}
