"""
Sprint templates — deterministic, rule-based generators for the 7-Day
Growth Proof Sprint. Each function takes the Company Brain + sprint context
and returns the day's output dict. No LLM, no I/O — pure logic.

The Brain is a dict like:
    {
        "company_name": "Acme",
        "sector": "B2B SaaS",
        "city": "Riyadh",
        "offer_ar": "خدمات استشارية",
        "ideal_customer_ar": "شركات 10-50 موظف",
        "approved_channels": ["linkedin_manual", "email_draft"],
        "blocked_channels": ["cold_whatsapp"],
        "tone_ar": "professional_saudi_arabic",
        "average_deal_value_sar": 5000.0,
    }
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(tzinfo=None).isoformat()


def _safe_brain(brain: dict[str, Any] | None) -> dict[str, Any]:
    b = dict(brain or {})
    b.setdefault("company_name", "العميل")
    b.setdefault("sector", "B2B")
    b.setdefault("city", "السعودية")
    b.setdefault("offer_ar", "خدمات الشركة")
    b.setdefault("ideal_customer_ar", "شركات سعودية 10-50 موظف")
    b.setdefault("tone_ar", "professional_saudi_arabic")
    b.setdefault("approved_channels", ["linkedin_manual", "email_draft"])
    b.setdefault("blocked_channels", ["cold_whatsapp", "linkedin_auto_dm"])
    b.setdefault("average_deal_value_sar", 5000.0)
    return b


# ── Day 1: Mini Diagnostic ────────────────────────────────────────


def generate_diagnostic(brain: dict[str, Any]) -> dict[str, Any]:
    """Day 1 — Mini Diagnostic. Picks best segment + 3 quick-win opps + 1 risk."""
    b = _safe_brain(brain)
    segments = [
        f"{b['ideal_customer_ar']} في {b['city']}",
        "وكالات تسويق B2B في الرياض",
        f"شركات {b['sector']} المتوسعة (Series A/B)",
    ]
    why_segment = (
        f"هذه الشريحة مطابقة لـ ICP والـ {b['city']} يخفّض احتكاك المتابعة، "
        "ولأنها تنفق فعلاً ميزانية على المشاكل التي يحلها عرضكم."
    )
    quick_wins = [
        {
            "title_ar": f"{b['company_name']} — تحسين CTA على الصفحة الرئيسية",
            "why": "الـ CTA الحالي عام؛ الشركات السعودية تستجيب أسرع للـ CTAs محددة (مثلاً 'احجز Diagnostic 30 دقيقة').",
            "expected_lift_ar": "تحويل 8% → 14%",
        },
        {
            "title_ar": "Outreach مُركّز على شريحة واحدة",
            "why": f"الجمع بين قطاعات متعددة يقلل الـ reply rate. التركيز على {segments[0]} يضاعف معدل الردود.",
            "expected_lift_ar": "reply rate 4% → 10%",
        },
        {
            "title_ar": "Proof Pack أسبوعي للقيادة",
            "why": "العميل يبقى لو شاف الأثر. Proof Pack أسبوعي يخفّض churn بشكل ملموس.",
            "expected_lift_ar": "retention +15%",
        },
    ]
    return {
        "day": 1,
        "kind": "diagnostic",
        "generated_at": _now_iso(),
        "company": b["company_name"],
        "best_segment_ar": segments[0],
        "alternative_segments_ar": segments[1:],
        "why_segment_ar": why_segment,
        "quick_wins": quick_wins,
        "safe_channel_ar": "LinkedIn manual + Email opt-in form",
        "risk_to_avoid_ar": (
            "تجنّب أي outreach للأرقام المشتراة أو القوائم بدون opt-in موثق — "
            "غرامة PDPL تصل لـ 5 مليون SAR."
        ),
        "next_step_ar": "غداً: Opportunity Pack — 10 فرص محددة بالاسم.",
    }


# ── Day 2: Opportunity Pack ───────────────────────────────────────


def generate_opportunity_pack(brain: dict[str, Any]) -> dict[str, Any]:
    """Day 2 — 10 named opportunities with why-now + contactability + channel."""
    b = _safe_brain(brain)
    sector = b["sector"]
    city = b["city"]

    # Deterministic 10-row template — replace placeholders with seed contacts
    # the founder fills in. Pure structure; no fabricated names.
    opportunities = []
    for i in range(1, 11):
        risk = "low" if i <= 7 else "medium"
        channel = "linkedin_manual" if i % 2 == 1 else "email_draft"
        opportunities.append({
            "n": i,
            "company_placeholder_ar": f"شركة {i} في {city} ({sector})",
            "person_placeholder_ar": "[المؤسس / VP Sales — أكمل من LinkedIn 1st-degree]",
            "why_now_ar": (
                "نشاط حديث على LinkedIn (post / hire / funding) يشير إلى نقطة دخول."
                if i % 2 == 1
                else "إعلان توسع أو تعيين Sales — توقيت مناسب لاقتراح Pilot."
            ),
            "contactability_ar": "1st-degree (warm)" if i <= 6 else "2nd-degree via referral",
            "recommended_channel_ar": channel,
            "risk_status_ar": risk,
            "expected_value_sar": float(b["average_deal_value_sar"] * (1.0 if i <= 5 else 0.7)),
        })

    return {
        "day": 2,
        "kind": "opportunity_pack",
        "generated_at": _now_iso(),
        "company": b["company_name"],
        "segment_ar": f"{b['ideal_customer_ar']} في {city}",
        "count": len(opportunities),
        "opportunities": opportunities,
        "approved_channels": list(b["approved_channels"]),
        "blocked_channels": list(b["blocked_channels"]),
        "next_step_ar": "غداً: Message Pack — 6 رسائل عربية + 3 follow-ups + 2 ردود اعتراض.",
    }


# ── Day 3: Message Pack ───────────────────────────────────────────


def generate_message_pack(brain: dict[str, Any]) -> dict[str, Any]:
    """Day 3 — 6 personalized first messages + 3 follow-ups + 2 objection responses."""
    b = _safe_brain(brain)
    company = b["company_name"]
    offer = b["offer_ar"]

    # 6 first-message templates — deterministic, Saudi-tone
    first_messages = [
        f"أ. [الاسم]، شفت آخر post لك عن [موضوع محدد] — تعليق صادق من جملة. "
        f"أبني {company}: {offer}. ١٥ دقيقة هذا الأسبوع لأشاركك فكرة سريعة؟",

        f"السلام عليكم [الاسم]. لاحظت توسعكم في [قطاع/مدينة]. "
        f"عندي زاوية ربما تفيدكم في {offer} — هل تتفضّل بـ ١٠ دقائق؟",

        f"[الاسم]، أحتاج رأيك (مش بيع). أبني خدمة {offer} للشركات الشبيهة بكم. "
        "أيش أكثر شي يضايقكم في pipeline حاليًا؟",

        f"أ. [الاسم]، استخدمت {company} وسائل عمل مشابهة. "
        f"عندي Diagnostic مجاني (٢٤ ساعة). تتفضّل بتجربته؟",

        f"السلام [الاسم]. شفت [أحد منشوراتهم]. "
        f"أعمل في {b['sector']} وعندي سؤال محدد — هل تفضّل LinkedIn DM أو Email؟",

        f"[الاسم]، {company} جاي يخدم {b['ideal_customer_ar']}. "
        "هل ميزانية النمو في الـ Q الحالي مفتوحة؟ سؤال صادق.",
    ]

    follow_ups = [
        f"[الاسم]، أردت تذكيرك فقط — أعرف أن الأسبوع مزدحم. لو ما يناسب، تمام، أنا مش بيع.",
        f"عرض بديل: 1-page summary أرسله لتقرأه وقت فاضي بدلاً من اجتماع. مفيد؟",
        f"إذا التوقيت سيء حاليًا، خلني أعرف وأرجع لك بعد ٣ أسابيع.",
    ]

    objection_responses = [
        {
            "objection_ar": "السعر مرتفع",
            "response_ar": (
                f"فهمت. كم تكلف خسارة صفقة واحدة بسبب متابعة منسية؟ "
                f"Pilot 499 SAR لأسبوع — تشوف Proof قبل أي التزام أكبر."
            ),
        },
        {
            "objection_ar": "ميزانيتنا مستهلكة",
            "response_ar": (
                "499 SAR من بطاقة شخصية، تحت threshold الـ approval. "
                "ابدأ غدًا، رد في 30 يوم."
            ),
        },
    ]

    return {
        "day": 3,
        "kind": "message_pack",
        "generated_at": _now_iso(),
        "company": company,
        "tone_ar": b["tone_ar"],
        "first_messages_ar": first_messages,
        "follow_ups_ar": follow_ups,
        "objection_responses": objection_responses,
        "approval_required": True,
        "blocked_phrases_ar": list(b.get("forbidden_claims") or ["نضمن", "guaranteed"]),
        "next_step_ar": "غداً: Meeting/Call Plan — سكربت + agenda + قائمة أسئلة + close plan.",
    }


# ── Day 4: Meeting / Call Plan ────────────────────────────────────


def generate_meeting_prep(brain: dict[str, Any]) -> dict[str, Any]:
    """Day 4 — Call script + meeting agenda + discovery questions + close plan."""
    b = _safe_brain(brain)
    return {
        "day": 4,
        "kind": "meeting_prep",
        "generated_at": _now_iso(),
        "company": b["company_name"],
        "call_script_intro_ar": (
            f"السلام عليكم [الاسم]، معك [اسمك] من {b['company_name']}. "
            f"شكرًا للوقت. سأبقى في حدود ١٥ دقيقة."
        ),
        "meeting_agenda": [
            {"minutes": 5, "topic_ar": "Discovery — أكبر تحدي حالي في pipeline؟"},
            {"minutes": 5, "topic_ar": f"كيف يحل {b['offer_ar']} هذا التحدي تحديدًا"},
            {"minutes": 5, "topic_ar": "Pilot 499 SAR — لو مناسب، نبدأ غدًا"},
        ],
        "discovery_questions_ar": [
            "ما حجم القائمة الحالية؟ كم متوسط الـ reply rate؟",
            "ما أكثر شي يضايقكم في الـ pipeline اليوم؟ (متابعات منسية؟ leads ضعيفة؟ تقارير؟)",
            "كم شخص في فريق المبيعات حاليًا؟",
            "ما أكبر صفقة فقدتموها هذه السنة؟ ولماذا؟",
            "من يقرر الميزانية على شيء بحجم 499 SAR؟ 2,999 SAR/شهر؟",
        ],
        "close_plan_ar": [
            "إذا 'نعم': أرسل intake form + رابط Moyasar في WhatsApp — ١٠ دقائق.",
            "إذا 'أحتاج أراجع': اطلب يوم محدد للمتابعة + أرسل 1-page summary.",
            "إذا 'السعر/التوقيت': اعرض Free Diagnostic بدلاً.",
        ],
        "next_step_ar": "غداً: Pipeline Review — من ردّ، من يحتاج follow-up، من high-intent.",
    }


# ── Day 5: Pipeline Review ────────────────────────────────────────


def generate_pipeline_review(brain: dict[str, Any], prospects_data: list[dict] | None = None) -> dict[str, Any]:
    """Day 5 — Categorize all touched prospects into buckets."""
    b = _safe_brain(brain)
    rows = list(prospects_data or [])

    replied = [p for p in rows if p.get("status") == "replied"]
    no_reply = [p for p in rows if p.get("status") == "messaged" and not p.get("last_reply_at")]
    high_intent = [p for p in rows if p.get("status") in ("meeting_booked", "pilot_offered")]
    blocked = [p for p in rows if p.get("blocked_channels")]

    return {
        "day": 5,
        "kind": "pipeline_review",
        "generated_at": _now_iso(),
        "company": b["company_name"],
        "summary": {
            "total_touched": len(rows),
            "replied": len(replied),
            "no_reply": len(no_reply),
            "high_intent": len(high_intent),
            "blocked": len(blocked),
        },
        "replied_list": [{"id": p.get("id"), "company": p.get("company")} for p in replied[:10]],
        "follow_up_due": [
            {"id": p.get("id"), "company": p.get("company"), "stale_hours": p.get("stale_hours", 0)}
            for p in no_reply[:10]
        ],
        "high_intent_list": [
            {"id": p.get("id"), "company": p.get("company"), "stage": p.get("status")}
            for p in high_intent[:10]
        ],
        "blocked_list": [
            {"id": p.get("id"), "reason_ar": p.get("risk_reason") or "channel policy"}
            for p in blocked[:10]
        ],
        "next_step_ar": "غداً: Proof Pack Draft — ما تم إنجازه، ما حُمي، ما ينتظر، الأثر المالي.",
    }


# ── Day 6: Proof Pack Draft ───────────────────────────────────────


def generate_proof_draft(brain: dict[str, Any], counts: dict[str, int] | None = None,
                        risks_blocked: list | None = None,
                        revenue_impact_sar: float = 0.0) -> dict[str, Any]:
    """Day 6 — Draft of the final Proof Pack. The customer reviews this
    before Day 7 Final + upsell."""
    b = _safe_brain(brain)
    counts = counts or {}
    risks = list(risks_blocked or [])
    return {
        "day": 6,
        "kind": "proof_draft",
        "generated_at": _now_iso(),
        "company": b["company_name"],
        "what_was_created": [
            {"unit": "opportunity_created", "count": counts.get("opportunity_created", 0)},
            {"unit": "draft_created", "count": counts.get("draft_created", 0)},
            {"unit": "meeting_drafted", "count": counts.get("meeting_drafted", 0)},
            {"unit": "followup_created", "count": counts.get("followup_created", 0)},
        ],
        "what_was_protected": [
            {
                "label_ar": (r.get("label_ar") if isinstance(r, dict) else str(r)),
                "risk_level": (r.get("risk_level") if isinstance(r, dict) else "low"),
            }
            for r in risks[:10]
        ],
        "what_is_pending": {
            "approvals": counts.get("pending_approvals", 0),
            "next_actions": counts.get("pending_next_actions", 0),
        },
        "expected_revenue_impact_sar": round(float(revenue_impact_sar), 2),
        "next_step_ar": "غداً: Final Proof Pack + offer Growth OS الشهري.",
    }


# ── Day 7: Final Proof + Upsell ───────────────────────────────────


def generate_close_out(brain: dict[str, Any], proof_draft: dict[str, Any] | None = None,
                      pack_url: str | None = None) -> dict[str, Any]:
    """Day 7 — Final Proof Pack delivered + upsell to Growth OS."""
    b = _safe_brain(brain)
    draft = proof_draft or {}
    return {
        "day": 7,
        "kind": "close_out",
        "generated_at": _now_iso(),
        "company": b["company_name"],
        "proof_pack_url": pack_url or "—",
        "proof_summary_ar": (
            f"خلال ٧ أيام: سلّمنا تشخيص + ١٠ فرص + ٦ رسائل + خطة مكالمة + "
            f"مراجعة pipeline. الأثر المالي التقديري: "
            f"{draft.get('expected_revenue_impact_sar', 0):,.0f} SAR."
        ),
        "upsell": {
            "service_id": "executive_growth_os",
            "name_ar": "Executive Growth OS",
            "price_label": "2,999 SAR / شهر شامل الضريبة",
            "annual_label": "29,888 SAR / سنوي (وفّر 17%)",
            "included_ar": [
                "كل ما حصلت عليه في الـ Pilot — لكن مستمر",
                "4 daily-ops windows أوتوماتيكية",
                "Role briefs لـ 9 أدوار (CEO/Sales/Growth/...)",
                "Self-Growth weekly experiments",
                "Proof Pack أسبوعي مع HMAC",
                "دعم خلال 4 ساعات",
            ],
            "next_step_ar": (
                "هل نبدأ الشهر الأول الآن؟ نفس الـ Mada، نفس الفاتورة، "
                "تجديد تلقائي شهري — إلغاء بضغطة."
            ),
        },
        "alternative_ar": (
            "لو حابب تتوقف هنا — تمام، شكراً للثقة. "
            "Proof Pack ملكك، استخدمه كما تشاء."
        ),
    }
