"""Partner-distribution radar — static catalog of partner categories.

This is a CATALOG, not a discovery tool. It lists the
**categories of partners** Dealix should approach, with a typed
record per category carrying:

  - the strategic fit reason
  - the recommended offer (revenue share, co-deliver, referral, etc.)
  - the manual warm message draft (Arabic + English secondary)
  - the safety boundary (no scraping, no auto-DM)

Founder picks specific partners from each category from their own
network — Dealix never scrapes any directory. The drafts go
through the existing ``safe_publishing_gate`` before being shown
to the founder for approval.

What this module is NOT:
  - a partner directory we crawl
  - a scraper of LinkedIn / Crunchbase / etc.
  - an auto-outreach engine
  - a tracking system (that lives in the main CRM if/when one exists)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.self_growth_os.safe_publishing_gate import check_text
from auto_client_acquisition.self_growth_os.schemas import (
    ApprovalStatus,
    Language,
    RiskLevel,
    ServiceBundle,
)


@dataclass(frozen=True)
class PartnerCategory:
    """One partner category — a class of partners, not a specific one."""

    category_id: str
    name_ar: str
    name_en: str
    fit_reason_ar: str
    fit_reason_en: str
    recommended_offer_ar: str
    recommended_offer_en: str
    warm_intro_draft_ar: str
    warm_intro_draft_en: str
    co_branded_proof_idea: str
    risk_notes: str
    next_step: str
    service_bundle: ServiceBundle = ServiceBundle.PARTNERSHIP_GROWTH

    def to_dict(self) -> dict[str, Any]:
        return {
            "category_id": self.category_id,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "fit_reason_ar": self.fit_reason_ar,
            "fit_reason_en": self.fit_reason_en,
            "recommended_offer_ar": self.recommended_offer_ar,
            "recommended_offer_en": self.recommended_offer_en,
            "warm_intro_draft_ar": self.warm_intro_draft_ar,
            "warm_intro_draft_en": self.warm_intro_draft_en,
            "co_branded_proof_idea": self.co_branded_proof_idea,
            "risk_notes": self.risk_notes,
            "next_step": self.next_step,
            "service_bundle": self.service_bundle.value,
        }


# Hand-curated catalog. Each entry is grounded in
# docs/STRATEGIC_MASTER_PLAN_2026.md Part VII Channel 3.
CATALOG: tuple[PartnerCategory, ...] = (
    PartnerCategory(
        category_id="b2b_marketing_agency",
        name_ar="وكالة تسويق B2B سعوديّة",
        name_en="Saudi B2B marketing agency",
        fit_reason_ar=(
            "تبيع لشركات B2B سعوديّة — نفس عملاء Dealix. تكمّل خدمتها "
            "بـ Revenue Execution OS بدل بناء أداة داخليّة."
        ),
        fit_reason_en=(
            "Sells to Saudi B2B companies — same buyer Dealix targets. "
            "Adds Revenue Execution OS to its stack without building one."
        ),
        recommended_offer_ar=(
            "حصّة ٣٠٪ من إيراد السنة الأولى للعميل المحوَّل. تخفيض ٢٠٪ "
            "السنة الثانية. وكالة معتمَدة بشعار Dealix Partner."
        ),
        recommended_offer_en=(
            "30% of Year-1 revenue for referred customers; 20% in Year 2. "
            "Certified-partner badge."
        ),
        warm_intro_draft_ar=(
            "السلام عليكم [اسم]، شفت شغلكم على [حملة/شريك ظاهر]. عندنا "
            "Dealix — Revenue Execution OS عربي يكمّل خدمتكم بدون منافسة. "
            "ممكن نأخذ ٢٠ دقيقة الأسبوع الجاي نشرح كيف نشتغل سوا؟"
        ),
        warm_intro_draft_en=(
            "Hi [name], saw your work with [visible client]. We built "
            "Dealix — an Arabic Revenue Execution OS that complements "
            "your service without overlap. Could we grab 20 minutes "
            "next week?"
        ),
        co_branded_proof_idea=(
            "Proof Pack مشترك بعلامتيكم: عدد فرص محدّدة + رسائل عربيّة "
            "+ خطّة متابعة. مدفوع من العميل عبر الوكالة، Dealix يسلّم."
        ),
        risk_notes=(
            "تجنّب أيّ بند exclusivity حتى أوّل ٣ proofs مُسلَّمة. "
            "لا يوجد نشر آلي أو cold outreach تحت أيّ شعار."
        ),
        next_step="founder_warm_intro_then_20min_call",
    ),
    PartnerCategory(
        category_id="performance_marketing_agency",
        name_ar="وكالة أداء (Paid Media)",
        name_en="Performance / paid-media agency",
        fit_reason_ar=(
            "يصرفون على Paid Ads لكن النتائج تتسرّب لأنّ الردّ على "
            "leads بطيء. Dealix يحمي ROI الإعلانات."
        ),
        fit_reason_en=(
            "Spend big on paid ads but lose leads to slow follow-up. "
            "Dealix protects their ad ROI."
        ),
        recommended_offer_ar=(
            "حصّة ٢٥٪ سنة أولى. Dealix يدخل كأداة follow-up ضمن "
            "تقاريرهم الشهريّة."
        ),
        recommended_offer_en=(
            "25% Y1 share. Dealix slots in as the follow-up tool in "
            "their monthly client reports."
        ),
        warm_intro_draft_ar=(
            "[اسم]، عميلكم بيدفع SAR على إعلانات؛ ٤٠٪ من leads تروح "
            "للمنافس اللي يردّ خلال ساعة. عندنا حلّ عربي ساعة الردّ "
            "فيه ٤٥ ثانية، شراكة ٢٥٪ Y1. ١٥ دقيقة؟"
        ),
        warm_intro_draft_en=(
            "[name], your client pays for ads but ~40% of leads go to "
            "whoever replies within 1 hour. We close that to 45s in "
            "Arabic. 25% Y1 partnership. 15 min?"
        ),
        co_branded_proof_idea=(
            "تقرير مشترك يربط cost-per-lead لـ paid → first-touch SLA "
            "→ معدل التحويل عبر Dealix."
        ),
        risk_notes=(
            "الوكالة تظلّ مالكة لعلاقة العميل. Dealix لا يتواصل مع "
            "العميل النهائي بدون إذن مكتوب."
        ),
        next_step="founder_warm_intro_then_15min_call",
    ),
    PartnerCategory(
        category_id="sales_consultant",
        name_ar="مستشار مبيعات/تدريب فرق",
        name_en="Sales consultant / sales-training firm",
        fit_reason_ar=(
            "يدرّبون فرق المبيعات السعوديّة لكن أدوات التنفيذ يدويّة. "
            "Dealix يحوّل تدريبهم إلى loop تشغيلي."
        ),
        fit_reason_en=(
            "Train Saudi sales teams but execution tooling is manual. "
            "Dealix turns their training into an operational loop."
        ),
        recommended_offer_ar=(
            "Referral fee ثابت ١,٠٠٠–٢,٠٠٠ ريال لكلّ pilot يُغلق + "
            "خصم ٢٠٪ على Executive Growth OS لعملائهم الحاليّين."
        ),
        recommended_offer_en=(
            "Flat referral fee 1,000-2,000 SAR per closed pilot + "
            "20% discount on Executive Growth OS for their existing book."
        ),
        warm_intro_draft_ar=(
            "[اسم]، تدريبكم ممتاز لكن المتدرّبين يرجعون لـ CRM ضعيف. "
            "Dealix يخلّي التدريب يصير تشغيل يومي. ١٥ دقيقة لشرح؟"
        ),
        warm_intro_draft_en=(
            "[name], your training is great but trainees go back to a "
            "weak CRM. Dealix turns the training into daily ops. "
            "15-min walk-through?"
        ),
        co_branded_proof_idea=(
            "محتوى مشترك: 'كيف يبدو يوم مندوب مبيعات سعودي مع Dealix' "
            "— المستشار يضيفه لمنهجه."
        ),
        risk_notes=(
            "لا حصريّة. لا يلتزم المستشار بكميّة عملاء معيّنة. "
            "العمولة تُدفع فقط على Pilot مُغلَق + مدفوع."
        ),
        next_step="founder_intro_then_demo",
    ),
    PartnerCategory(
        category_id="crm_implementer",
        name_ar="شريك تنفيذ CRM (HubSpot/Salesforce)",
        name_en="CRM implementer (HubSpot/Salesforce)",
        fit_reason_ar=(
            "ينصبون CRM لكن العميل ما يستخدمه. Dealix يكمّل بطبقة "
            "تنفيذ تجعل CRM قيّماً."
        ),
        fit_reason_en=(
            "Set up CRM, but client adoption is low. Dealix complements "
            "with an execution layer that makes the CRM stick."
        ),
        recommended_offer_ar=(
            "حصّة ٢٠٪ Y1 + سعر مرجعي للعملاء الذين يربطون Dealix بـ CRM موجود."
        ),
        recommended_offer_en=(
            "20% Y1 share + reference pricing for customers linking "
            "Dealix to an existing CRM."
        ),
        warm_intro_draft_ar=(
            "[اسم]، نشتغل تكامل عربي مع HubSpot — Dealix يكتب الردود "
            "والمتابعات بالعربي ويحدّث CRM. شراكة على عملاء KSA. ٢٠ دقيقة؟"
        ),
        warm_intro_draft_en=(
            "[name], we built an Arabic execution layer that talks to "
            "HubSpot — drafts replies, updates CRM, all bilingual. "
            "Partner on KSA accounts? 20 min?"
        ),
        co_branded_proof_idea=(
            "Case study: 'CRM adoption rises from 30% to 80% when "
            "Dealix handles the Arabic execution.'"
        ),
        risk_notes=(
            "لا يوجد بيع مفترض إلى عملائهم بدون استجابة العميل أوّلاً."
        ),
        next_step="technical_walkthrough_call",
    ),
    PartnerCategory(
        category_id="software_house",
        name_ar="بيت برمجيّات سعودي",
        name_en="Saudi software house / dev shop",
        fit_reason_ar=(
            "يبني MVPs لعملاء B2B لكن يعجز عن مكوّن sales/growth. "
            "Dealix يصير المكوّن الجاهز لهم."
        ),
        fit_reason_en=(
            "Build MVPs for B2B clients but lack a sales/growth "
            "component. Dealix becomes their drop-in piece."
        ),
        recommended_offer_ar=(
            "Reseller pricing: ٢٥٪ خصم على Executive Growth OS عند "
            "تضمين Dealix في عقد المشروع."
        ),
        recommended_offer_en=(
            "Reseller pricing: 25% off Executive Growth OS when Dealix "
            "is bundled in their project contract."
        ),
        warm_intro_draft_ar=(
            "[اسم]، شفت [مشروع منشور]. لمّا تبني MVP، عميلكم بيحتاج "
            "طبقة sales تخلّيه يبيع. Dealix جاهز للتضمين بدون بناء "
            "من الصفر. ٢٠ دقيقة؟"
        ),
        warm_intro_draft_en=(
            "[name], saw [public project]. When you ship an MVP, the "
            "client still needs a sales layer. Dealix slots in. 20 min?"
        ),
        co_branded_proof_idea=(
            "Proof Pack مشترك: 'من MVP إلى أوّل ١٠ عملاء في ٣٠ يوم.'"
        ),
        risk_notes="لا تعديلات منتج خاصّة لكلّ شريك — معماريّة موحَّدة.",
        next_step="founder_intro_then_30min_demo",
    ),
    PartnerCategory(
        category_id="accounting_firm",
        name_ar="مكتب محاسبة معتمَد (ZATCA)",
        name_en="Certified accounting firm (ZATCA)",
        fit_reason_ar=(
            "يخدمون SMEs سعوديّة. عملاؤهم يحتاجون نموّ بيع، "
            "والمكتب يحتاج خدمات إضافيّة لرفع الـ ARPU."
        ),
        fit_reason_en=(
            "Serve Saudi SMEs. Their clients need sales growth; the "
            "firm wants higher ARPU services to offer."
        ),
        recommended_offer_ar=(
            "Referral ثابت ١,٠٠٠ ريال لكلّ pilot + بادج 'Dealix-ready'."
        ),
        recommended_offer_en=(
            "Flat 1,000 SAR per closed pilot referral + 'Dealix-ready' badge."
        ),
        warm_intro_draft_ar=(
            "[اسم]، عملاؤكم يطلبون نموّ مبيعات وأنتم تركّزون على المالي. "
            "نقدر نتشارك. ١٥ دقيقة؟"
        ),
        warm_intro_draft_en=(
            "[name], your clients ask for sales growth while you focus "
            "on financials. Could partner up. 15 min?"
        ),
        co_branded_proof_idea=(
            "ندوة مشتركة: 'كيف يحقّق صاحب SME سعودي نموّاً قابلاً للتفعيل "
            "بفاتورة ZATCA + Dealix.'"
        ),
        risk_notes="لا مشاركة بيانات عميل بين المكتب وDealix بدون موافقة كتابيّة.",
        next_step="webinar_co_host_then_intros",
    ),
    PartnerCategory(
        category_id="founder_community",
        name_ar="مجتمع مؤسّسين خليجي",
        name_en="Gulf founder community",
        fit_reason_ar=(
            "أفضل قناة warm intro. مؤسّسون يثقون ببعضهم أكثر من أيّ "
            "إعلان. Dealix يكسب ولاء المؤسس قبل ما يكسب عقد."
        ),
        fit_reason_en=(
            "Best warm-intro channel. Founders trust each other more "
            "than any ad. Dealix wins founder loyalty before contracts."
        ),
        recommended_offer_ar=(
            "Diagnostic مجاني لأعضاء المجتمع + خصم ٢٠٪ على Pilot لأوّل ٥ أعضاء."
        ),
        recommended_offer_en=(
            "Free Diagnostic for community members + 20% off Pilot for first 5."
        ),
        warm_intro_draft_ar=(
            "للمجتمع: 'أهديكم Diagnostic مجاني عربي حول إيراد شركتكم. "
            "مدّة ٢٠ دقيقة، نتيجة فعليّة، بدون شروط.'"
        ),
        warm_intro_draft_en=(
            "Community post: 'Free 20-min Arabic Revenue Diagnostic. "
            "Real output. No strings.'"
        ),
        co_branded_proof_idea="جلسة chat مع مؤسس + Proof Pack منشور بإذن صريح.",
        risk_notes="لا spam في المجتمع — منشور واحد كلّ ٤-٦ أسابيع كحدّ أقصى.",
        next_step="single_founder_post_then_inbound_only",
    ),
    PartnerCategory(
        category_id="hr_recruitment",
        name_ar="شركة توظيف/HR",
        name_en="HR / recruitment firm",
        fit_reason_ar=(
            "العملاء يطلبون منهم 'مندوبي مبيعات' — وحلّ Dealix يقدر "
            "يقلّل عدد الموظّفين المطلوبين، فيتّحوّل التوظيف لتدريب + "
            "تنفيذ."
        ),
        fit_reason_en=(
            "Clients ask them for 'sales reps' — Dealix can reduce "
            "headcount needed; recruiting shifts to training + execution."
        ),
        recommended_offer_ar=(
            "Referral عند تحويل عميل توظيف إلى عميل Dealix: ١٥٪ "
            "Y1، أو ٣,٠٠٠ ريال ثابتة لكلّ Pilot."
        ),
        recommended_offer_en=(
            "Referral 15% Y1 or flat 3,000 SAR per Pilot when "
            "redirecting a hiring request to Dealix."
        ),
        warm_intro_draft_ar=(
            "[اسم]، عميل طلب منكم ٥ مندوبي مبيعات؟ ممكن يحقّق نفس "
            "النتيجة بفريقين + Dealix. ٢٠ دقيقة؟"
        ),
        warm_intro_draft_en=(
            "[name], a client asked for 5 sales reps? They might hit "
            "the same result with 2 reps + Dealix. 20 min?"
        ),
        co_branded_proof_idea=(
            "محتوى: 'متى تحتاج توظيف، ومتى يكفي توظيف ٢ + Dealix.'"
        ),
        risk_notes="لا تنافس مباشر — الشركة تظلّ مَن تقترح الحلّ على عميلها.",
        next_step="founder_intro_then_compare_call",
    ),
)


def list_categories() -> list[dict[str, Any]]:
    """Return all catalog entries as plain dicts."""
    return [c.to_dict() for c in CATALOG]


def get_category(category_id: str) -> dict[str, Any]:
    """Return one category by id, or raise KeyError."""
    for c in CATALOG:
        if c.category_id == category_id:
            return c.to_dict()
    raise KeyError(f"unknown partner category: {category_id}")


def safe_drafts() -> dict[str, Any]:
    """Run every warm-intro draft (AR + EN) through the safe-publishing
    gate and return aggregated results. Use this before any draft is
    shown to the founder for final approval.

    The gate result is added inline to each entry; nothing is sent.
    """
    results: list[dict[str, Any]] = []
    for c in CATALOG:
        ar = check_text(c.warm_intro_draft_ar, language=Language.AR)
        en = check_text(c.warm_intro_draft_en, language=Language.EN)
        results.append({
            "category_id": c.category_id,
            "ar_decision": ar.decision,
            "ar_forbidden_tokens": ar.forbidden_tokens_found,
            "en_decision": en.decision,
            "en_forbidden_tokens": en.forbidden_tokens_found,
        })
    safe_count = sum(
        1 for r in results
        if r["ar_decision"] == "allowed_draft" and r["en_decision"] == "allowed_draft"
    )
    return {
        "total": len(results),
        "all_safe": safe_count == len(results),
        "safe_count": safe_count,
        "results": results,
    }


def summary() -> dict[str, Any]:
    """High-level summary for the API."""
    return {
        "schema_version": 1,
        "categories_total": len(CATALOG),
        "approval_status_default": ApprovalStatus.APPROVAL_REQUIRED.value,
        "risk_level_default": RiskLevel.LOW.value,
        "service_bundle": ServiceBundle.PARTNERSHIP_GROWTH.value,
        "boundary": {
            "no_scraping": True,
            "no_auto_dm": True,
            "no_cold_outreach": True,
            "approval_required_for_external_send": True,
            "drafts_only_until_founder_approves": True,
        },
        "categories": [
            {"category_id": c.category_id, "name_ar": c.name_ar, "name_en": c.name_en}
            for c in CATALOG
        ],
    }
