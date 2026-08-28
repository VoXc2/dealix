"""Negotiation & Persuasion Engine.

Bilingual objection handling, persuasion maps, deal strategy, and scripts for
Saudi B2B sales.

COMMERCIAL SAFETY CONTRACT
--------------------------
This compatibility engine is *not* price, commitment, or outcome authority.
It mirrors the current Dealix commercial path and produces negotiation support
that remains subject to the canonical Business Model, active first-launch gate,
and approval/evidence controls.

Current customer path:
    Free Mini Diagnostic
    -> qualified discovery
    -> customer-specific quote
    -> Revenue Command Pilot — 30 days
    -> Proof Pack
    -> Stop / Expand / Redesign

Named price, discount, contract, tender, payment/refund, public claim, and other
commercial commitments require their specific approval/evidence gates. The
engine must not invent ROI, customer outcomes, competitor results, or a public
fixed Pilot price.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Literal

from intelligence.bilingual import BilingualBlock, BilingualRenderer, BilingualText, LanguageCode


COMMERCIAL_PATH = (
    "Free Mini Diagnostic -> Qualified Discovery -> Customer-Specific Quote -> "
    "Revenue Command Pilot — 30 days -> Proof Pack -> Stop/Expand/Redesign"
)
COMMERCIAL_AUTHORITY = "canonical_business_model_and_active_first_launch_gate"
QUOTE_AUTHORITY = "founder_approved_named_customer_quote_after_qualified_discovery"


class ObjectionCategory(str, Enum):
    PRICE = "price"
    TIMING = "timing"
    COMPETITION = "competition"
    TRUST = "trust"
    SCOPE = "scope"
    AUTHORITY = "authority"
    RISK = "risk"


@dataclass(frozen=True)
class Objection:
    objection_id: str
    category: ObjectionCategory
    trigger_phrase: BilingualText
    response: BilingualBlock
    evidence_refs: list[str]
    requires_price_reference: bool = False
    price_sku: str | None = None

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "objection_id": self.objection_id,
            "category": self.category.value,
            "trigger_phrase": BilingualRenderer.filter_text(self.trigger_phrase, lang),
            "response": BilingualRenderer.filter_block(self.response, lang),
            "evidence_refs": self.evidence_refs,
            "requires_price_reference": self.requires_price_reference,
            "price_sku": self.price_sku,
            "commercial_authority": COMMERCIAL_AUTHORITY,
            "commitment_allowed": False,
        }


@dataclass(frozen=True)
class StakeholderInfluence:
    name: str
    role: str
    influence_level: Literal["decision_maker", "influencer", "gatekeeper", "blocker"]
    key_concern: BilingualText

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "influence_level": self.influence_level,
            "key_concern": BilingualRenderer.filter_text(self.key_concern, lang),
        }


@dataclass(frozen=True)
class PersuasionMap:
    deal_id: str
    stakeholders: list[StakeholderInfluence]
    value_props: list[BilingualText]
    risk_reversals: list[BilingualText]
    recommended_sequence: list[str]

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "deal_id": self.deal_id,
            "stakeholders": [s.to_dict(lang) for s in self.stakeholders],
            "value_props": [BilingualRenderer.filter_text(v, lang) for v in self.value_props],
            "risk_reversals": [BilingualRenderer.filter_text(r, lang) for r in self.risk_reversals],
            "recommended_sequence": self.recommended_sequence,
            "commercial_authority": COMMERCIAL_AUTHORITY,
        }


@dataclass(frozen=True)
class DealStrategy:
    deal_id: str
    company_name: str
    sector: str
    strategy_type: Literal["challenger", "consultative", "relationship", "value"]
    win_themes: list[BilingualText]
    talking_points: list[BilingualBlock]
    objection_playbook: list[Objection]
    pricing_anchor: dict[str, Any]
    close_timeline_days: int
    confidence_percent: float

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "deal_id": self.deal_id,
            "company_name": self.company_name,
            "sector": self.sector,
            "strategy_type": self.strategy_type,
            "win_themes": [BilingualRenderer.filter_text(w, lang) for w in self.win_themes],
            "talking_points": [BilingualRenderer.filter_block(t, lang) for t in self.talking_points],
            "objection_playbook": [o.to_dict(lang) for o in self.objection_playbook],
            "pricing_anchor": self.pricing_anchor,
            "close_timeline_days": self.close_timeline_days,
            "confidence_percent": self.confidence_percent,
            "commercial_authority": COMMERCIAL_AUTHORITY,
            "execution_allowed": False,
            "approval_required_for_commitment": True,
        }


class NegotiationEngine:
    """Bilingual negotiation support that never authorizes a commitment."""

    def __init__(self) -> None:
        self._objection_library = self._build_objection_library()

    @staticmethod
    def _authority_payload() -> dict[str, Any]:
        return {
            "commercial_path": COMMERCIAL_PATH,
            "authority": COMMERCIAL_AUTHORITY,
            "quote_authority": QUOTE_AUTHORITY,
            "public_fixed_pilot_price_allowed": False,
            "invented_roi_or_outcome_claims_allowed": False,
            "execution_allowed": False,
        }

    def _build_objection_library(self) -> dict[ObjectionCategory, list[Objection]]:
        return {
            ObjectionCategory.PRICE: [
                Objection(
                    objection_id="price-01",
                    category=ObjectionCategory.PRICE,
                    trigger_phrase=BilingualRenderer.bt(
                        en="Your service is expensive",
                        ar="خدمتكم غالية",
                    ),
                    response=BilingualBlock(
                        title=BilingualRenderer.bt(en="Clarify value and scope", ar="توضيح القيمة والنطاق"),
                        body=BilingualRenderer.bt(
                            en=(
                                "That is fair to examine. Rather than defend a generic price, we should first "
                                "confirm the problem, baseline, required scope, and success evidence. If the "
                                "opportunity qualifies after discovery, Dealix prepares a customer-specific "
                                "quote for approval; there is no public fixed Pilot price."
                            ),
                            ar=(
                                "من الطبيعي مراجعة التكلفة. بدل الدفاع عن سعر عام، نثبت أولاً المشكلة وخط "
                                "الأساس والنطاق المطلوب ودليل النجاح. إذا تأهلت الفرصة بعد الاستكشاف، تُجهّز "
                                "Dealix عرضًا خاصًا بالعميل للموافقة؛ ولا يوجد سعر عام ثابت للبرنامج التجريبي."
                            ),
                        ),
                    ),
                    evidence_refs=["COMMERCIAL_IDENTITY.md", "docs/DEALIX_BUSINESS_MODEL.md"],
                ),
            ],
            ObjectionCategory.TIMING: [
                Objection(
                    objection_id="timing-01",
                    category=ObjectionCategory.TIMING,
                    trigger_phrase=BilingualRenderer.bt(
                        en="We will look at this next quarter",
                        ar="سننظر في هذا الربع القادم",
                    ),
                    response=BilingualBlock(
                        title=BilingualRenderer.bt(en="Test whether delay matters", ar="اختبار أثر التأجيل"),
                        body=BilingualRenderer.bt(
                            en=(
                                "We should not assume delay is costly without your data. A Free Mini Diagnostic "
                                "can document the current workflow, the evidence gap, and whether there is a "
                                "measurable reason to act now or defer."
                            ),
                            ar=(
                                "لا ينبغي أن نفترض أن التأجيل مكلف من دون بياناتكم. يمكن للتشخيص المصغر المجاني "
                                "توثيق سير العمل الحالي وفجوة الأدلة وتحديد ما إذا كان هناك سبب قابل للقياس "
                                "للتحرك الآن أو التأجيل."
                            ),
                        ),
                    ),
                    evidence_refs=["free_mini_diagnostic", "proof_requirements"],
                ),
            ],
            ObjectionCategory.COMPETITION: [
                Objection(
                    objection_id="competition-01",
                    category=ObjectionCategory.COMPETITION,
                    trigger_phrase=BilingualRenderer.bt(
                        en="We are already using a CRM/AI tool",
                        ar="نستخدم بالفعل أداة CRM/AI",
                    ),
                    response=BilingualBlock(
                        title=BilingualRenderer.bt(en="Complement before replace", ar="التكامل قبل الاستبدال"),
                        body=BilingualRenderer.bt(
                            en=(
                                "Dealix is not positioned as a generic CRM replacement. The relevant question is "
                                "whether your current stack already gives you governed opportunity decisions, "
                                "approval control, and source-bound proof. The Diagnostic can test that gap first."
                            ),
                            ar=(
                                "Dealix ليست بديلًا عامًا لنظام CRM. السؤال هو هل توفر منظومتكم الحالية قرارات "
                                "فرص محكومة وموافقات مضبوطة وإثباتًا مرتبطًا بالمصدر. يمكن للتشخيص اختبار هذه "
                                "الفجوة أولاً."
                            ),
                        ),
                    ),
                    evidence_refs=["COMMERCIAL_IDENTITY.md", "integration_map"],
                ),
            ],
            ObjectionCategory.TRUST: [
                Objection(
                    objection_id="trust-01",
                    category=ObjectionCategory.TRUST,
                    trigger_phrase=BilingualRenderer.bt(
                        en="How do we know this will work for us?",
                        ar="كيف نعرف أن هذا سينجح معنا؟",
                    ),
                    response=BilingualBlock(
                        title=BilingualRenderer.bt(en="Evidence before commitment", ar="الأدلة قبل الالتزام"),
                        body=BilingualRenderer.bt(
                            en=(
                                "We do not promise an outcome before evidence. We start with a Free Mini "
                                "Diagnostic. If the problem, owner, lawful data, baseline, and proof path qualify, "
                                "the next paid motion is a customer-specific 30-day Revenue Command Pilot with "
                                "defined acceptance criteria, weekly proof, and a final Stop/Expand/Redesign review."
                            ),
                            ar=(
                                "لا نعد بنتيجة قبل وجود دليل. نبدأ بتشخيص مصغر مجاني. إذا تأهلت المشكلة والمالك "
                                "والبيانات النظامية وخط الأساس ومسار الإثبات، فالخطوة المدفوعة التالية هي برنامج "
                                "Revenue Command لمدة 30 يومًا بنطاق خاص بالعميل ومعايير قبول وإثبات أسبوعي "
                                "ومراجعة نهائية للتوقف أو التوسع أو إعادة التصميم."
                            ),
                        ),
                    ),
                    evidence_refs=["docs/DEALIX_BUSINESS_MODEL.md", "COMMERCIAL_IDENTITY.md"],
                ),
            ],
            ObjectionCategory.SCOPE: [
                Objection(
                    objection_id="scope-01",
                    category=ObjectionCategory.SCOPE,
                    trigger_phrase=BilingualRenderer.bt(
                        en="This is more than we need right now",
                        ar="هذا أكثر مما نحتاجه الآن",
                    ),
                    response=BilingualBlock(
                        title=BilingualRenderer.bt(en="Start with one verified problem", ar="ابدأ بمشكلة واحدة مثبتة"),
                        body=BilingualRenderer.bt(
                            en=(
                                "Then we should reduce the scope. The entry step is the Free Mini Diagnostic: "
                                "one credible operational or revenue leak, the missing evidence, and a Pilot "
                                "hypothesis — not a company-wide transformation."
                            ),
                            ar=(
                                "إذن نقلل النطاق. خطوة الدخول هي التشخيص المصغر المجاني: مشكلة تشغيلية أو "
                                "إيرادية واحدة موثوقة، وفجوة الأدلة، وفرضية برنامج تجريبي — وليس تحولًا شاملاً "
                                "للشركة."
                            ),
                        ),
                    ),
                    evidence_refs=["free_mini_diagnostic", "docs/DEALIX_BUSINESS_MODEL.md"],
                ),
            ],
            ObjectionCategory.AUTHORITY: [
                Objection(
                    objection_id="authority-01",
                    category=ObjectionCategory.AUTHORITY,
                    trigger_phrase=BilingualRenderer.bt(
                        en="I need to check with my manager/CEO",
                        ar="أحتاج للتشاور مع مديري/الرئيس",
                    ),
                    response=BilingualBlock(
                        title=BilingualRenderer.bt(en="Make the decision defensible", ar="اجعل القرار قابلًا للدفاع"),
                        body=BilingualRenderer.bt(
                            en=(
                                "We can prepare a one-page decision brief that separates observed facts, "
                                "hypotheses, required evidence, scope, risks, and the next approval. It remains a "
                                "draft until the applicable external-send and commercial gates permit delivery."
                            ),
                            ar=(
                                "يمكننا إعداد ملخص قرار من صفحة واحدة يفصل الحقائق المرصودة والفرضيات والأدلة "
                                "المطلوبة والنطاق والمخاطر والموافقة التالية. ويبقى مسودة حتى تسمح بوابات الإرسال "
                                "والالتزام التجاري المطبقة بإرساله."
                            ),
                        ),
                    ),
                    evidence_refs=["buying_group", "approval_center"],
                ),
            ],
            ObjectionCategory.RISK: [
                Objection(
                    objection_id="risk-01",
                    category=ObjectionCategory.RISK,
                    trigger_phrase=BilingualRenderer.bt(
                        en="What if we do not see results?",
                        ar="ماذا لو لم نر نتائج؟",
                    ),
                    response=BilingualBlock(
                        title=BilingualRenderer.bt(en="Define evidence and stop rules", ar="حدد الأدلة وقواعد التوقف"),
                        body=BilingualRenderer.bt(
                            en=(
                                "The Pilot should define baseline, owner, data boundary, acceptance criteria, and "
                                "proof cadence before work starts. The final review is evidence-based: Stop, "
                                "Expand, or Redesign. We do not guarantee a commercial outcome."
                            ),
                            ar=(
                                "يجب أن يحدد البرنامج التجريبي خط الأساس والمالك وحدود البيانات ومعايير القبول "
                                "ودورية الإثبات قبل بدء العمل. وتكون المراجعة النهائية مبنية على الأدلة: توقف أو "
                                "توسع أو إعادة تصميم. ولا نضمن نتيجة تجارية."
                            ),
                        ),
                    ),
                    evidence_refs=["proof_pack", "acceptance_criteria"],
                ),
            ],
        }

    def list_objections(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return BilingualRenderer.wrap(
            {
                "categories": [c.value for c in ObjectionCategory],
                "objections": [
                    objection.to_dict(lang)
                    for category in self._objection_library.values()
                    for objection in category
                ],
                "authority": self._authority_payload(),
            },
            lang,
        )

    def handle_objection(
        self,
        category: str,
        context: dict[str, Any] | None = None,
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        context = context or {}
        try:
            objection_category = ObjectionCategory(category.lower())
        except ValueError:
            objection_category = ObjectionCategory.TRUST
        selected = self._objection_library[objection_category][0]
        return BilingualRenderer.wrap(
            {
                "objection": selected.to_dict(lang),
                "context": context,
                "authority": self._authority_payload(),
            },
            lang,
        )

    def build_persuasion_map(
        self,
        deal_id: str,
        stakeholders: list[dict[str, Any]],
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        stakeholder_objs = [
            StakeholderInfluence(
                name=stakeholder.get("name", "Unknown"),
                role=stakeholder.get("role", "Stakeholder"),
                influence_level=stakeholder.get("influence_level", "influencer"),
                key_concern=BilingualRenderer.bt(
                    en=stakeholder.get("key_concern_en", "Business outcome"),
                    ar=stakeholder.get("key_concern_ar", "النتيجة التجارية"),
                ),
            )
            for stakeholder in stakeholders
        ]
        value_props = [
            BilingualRenderer.bt(
                en="Turn evidence into governed revenue decisions",
                ar="تحويل الأدلة إلى قرارات إيراد محكومة",
            ),
            BilingualRenderer.bt(
                en="Keep critical external commitments approval-gated",
                ar="إبقاء الالتزامات الخارجية الحرجة خاضعة للموافقة",
            ),
            BilingualRenderer.bt(
                en="Build source-bound Proof Packs for executive decisions",
                ar="بناء حزم إثبات مرتبطة بالمصدر للقرارات التنفيذية",
            ),
        ]
        risk_reversals = [
            BilingualRenderer.bt(
                en="Diagnostic before paid scope",
                ar="تشخيص قبل النطاق المدفوع",
            ),
            BilingualRenderer.bt(
                en="Evidence-based Stop / Expand / Redesign decision",
                ar="قرار توقف أو توسع أو إعادة تصميم مبني على الأدلة",
            ),
        ]
        persuasion_map = PersuasionMap(
            deal_id=deal_id,
            stakeholders=stakeholder_objs,
            value_props=value_props,
            risk_reversals=risk_reversals,
            recommended_sequence=[
                "Map the buying group and decision criteria",
                "Separate observed facts from hypotheses",
                "Run or complete the Free Mini Diagnostic",
                "Confirm qualification, baseline, owner, lawful data, and proof path",
                "Prepare a customer-specific 30-day Pilot scope and quote for approval",
                "Proceed only through the applicable approval and external-action gates",
            ],
        )
        return BilingualRenderer.wrap(
            {
                "persuasion_map": persuasion_map.to_dict(lang),
                "authority": self._authority_payload(),
            },
            lang,
        )

    def generate_deal_strategy(
        self,
        company_name: str,
        sector: str,
        city: str,
        package_sku: str,
        budget_hint: float | None = None,
        employees: int = 50,
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        """Generate a non-committing strategy draft.

        ``package_sku`` and ``budget_hint`` are treated as context only. They do
        not authorize pricing. Numeric price/ROI output is intentionally absent.
        """
        del budget_hint

        strategy_type: Literal["challenger", "consultative", "relationship", "value"] = "consultative"
        if employees <= 50:
            strategy_type = "relationship"

        win_themes = [
            BilingualRenderer.bt(en="Evidence before commitment", ar="الأدلة قبل الالتزام"),
            BilingualRenderer.bt(en="Saudi-first operating context", ar="سياق تشغيلي سعودي أولاً"),
            BilingualRenderer.bt(en="Approval-gated critical commitments", ar="التزامات حرجة خاضعة للموافقة"),
        ]
        talking_points = [
            BilingualBlock(
                title=BilingualRenderer.bt(en="Why now", ar="لماذا الآن"),
                body=BilingualRenderer.bt(
                    en=(
                        f"For {company_name}, the question is whether a specific measurable revenue or "
                        f"operating problem exists in the current {sector} workflow in {city}. The Diagnostic "
                        "should establish that from source-bound evidence rather than market assumptions."
                    ),
                    ar=(
                        f"بالنسبة إلى {company_name}، السؤال هو هل توجد مشكلة إيرادية أو تشغيلية محددة وقابلة "
                        f"للقياس في سير عمل {sector} الحالي في {city}. يجب أن يثبت التشخيص ذلك بأدلة مرتبطة "
                        "بالمصدر بدل افتراضات السوق."
                    ),
                ),
            ),
            BilingualBlock(
                title=BilingualRenderer.bt(en="Why Dealix", ar="لماذا Dealix"),
                body=BilingualRenderer.bt(
                    en=(
                        "Dealix combines governed company context, opportunity intelligence, approval-first "
                        "action control, outcome evidence, and executive command. Fit must be proven for the "
                        "customer rather than assumed."
                    ),
                    ar=(
                        "تجمع Dealix سياق الشركة المحكوم وذكاء الفرص والتحكم في الإجراءات بالموافقة أولاً "
                        "وأدلة النتائج والقيادة التنفيذية. ويجب إثبات الملاءمة للعميل بدل افتراضها."
                    ),
                ),
            ),
            BilingualBlock(
                title=BilingualRenderer.bt(en="Commercial next step", ar="الخطوة التجارية التالية"),
                body=BilingualRenderer.bt(
                    en=(
                        "The entry step is the Free Mini Diagnostic. After qualified discovery and the active "
                        "launch gate, Dealix may prepare a customer-specific 30-day Revenue Command Pilot scope "
                        "and quote for approval. No public fixed Pilot price is authorized."
                    ),
                    ar=(
                        "خطوة الدخول هي التشخيص المصغر المجاني. بعد الاستكشاف المؤهل واجتياز بوابة الإطلاق "
                        "يمكن لـDealix إعداد نطاق وعرض خاص بالعميل لبرنامج Revenue Command لمدة 30 يومًا "
                        "للموافقة. ولا يوجد سعر عام ثابت معتمد للبرنامج التجريبي."
                    ),
                ),
            ),
        ]
        playbook = [
            self._objection_library[ObjectionCategory.PRICE][0],
            self._objection_library[ObjectionCategory.TIMING][0],
            self._objection_library[ObjectionCategory.TRUST][0],
        ]
        pricing_anchor = {
            "requested_package_context": package_sku,
            "commercial_mode": "quote_only_after_qualified_discovery",
            "quote_authority": QUOTE_AUTHORITY,
            "base_price_sar": None,
            "adjusted_price_sar": None,
            "roi_estimate_percent": None,
            "payment_terms": None,
            "approval_required": True,
            "execution_allowed": False,
        }
        strategy = DealStrategy(
            deal_id=f"deal-{company_name.lower().replace(' ', '-')}",
            company_name=company_name,
            sector=sector,
            strategy_type=strategy_type,
            win_themes=win_themes,
            talking_points=talking_points,
            objection_playbook=playbook,
            pricing_anchor=pricing_anchor,
            close_timeline_days=30,
            confidence_percent=50.0,
        )
        return BilingualRenderer.wrap(
            {
                "deal_strategy": strategy.to_dict(lang),
                "authority": self._authority_payload(),
            },
            lang,
        )

    def get_script(
        self,
        scenario: str,
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        scripts: dict[str, list[BilingualBlock]] = {
            "discovery_call": [
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Opening", ar="المقدمة"),
                    body=BilingualRenderer.bt(
                        en=(
                            "Thank you for the time. Before discussing a solution, I would like to understand "
                            "the workflow, the accountable owner, the evidence you already have, and what a "
                            "measurable improvement would mean for your team."
                        ),
                        ar=(
                            "شكرًا لوقتكم. قبل مناقشة الحل، أود فهم سير العمل والمالك المسؤول والأدلة المتاحة "
                            "لديكم وما الذي يعنيه تحسن قابل للقياس لفريقكم."
                        ),
                    ),
                ),
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Evidence probe", ar="استكشاف الأدلة"),
                    body=BilingualRenderer.bt(
                        en=(
                            "Where does the current process create the most uncertainty or leakage, and what "
                            "source could establish the baseline?"
                        ),
                        ar=(
                            "أين يخلق المسار الحالي أكبر قدر من عدم اليقين أو التسرب، وما المصدر الذي يمكنه "
                            "إثبات خط الأساس؟"
                        ),
                    ),
                ),
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Value bridge", ar="جسر القيمة"),
                    body=BilingualRenderer.bt(
                        en=(
                            "Dealix is a Saudi-first AI Business Operating System. The first commercial wedge is "
                            "Revenue + Proof + Command: governed decisions, approval-controlled actions, and "
                            "source-bound evidence rather than blind automation."
                        ),
                        ar=(
                            "Dealix هو نظام تشغيل أعمال بالذكاء الاصطناعي للشركات السعودية. والمدخل التجاري "
                            "الأول هو الإيرادات والإثبات والقيادة: قرارات محكومة وإجراءات مضبوطة بالموافقة "
                            "وأدلة مرتبطة بالمصدر بدل الأتمتة العمياء."
                        ),
                    ),
                ),
            ],
            "objection_price": [
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Acknowledge", ar="الإقرار"),
                    body=BilingualRenderer.bt(
                        en="Budget discipline matters. We should compare scope and evidence, not defend a generic price.",
                        ar="انضباط الميزانية مهم. يجب أن نقارن النطاق والأدلة بدل الدفاع عن سعر عام.",
                    ),
                ),
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Clarify", ar="التوضيح"),
                    body=BilingualRenderer.bt(
                        en=(
                            "What outcome or operating problem would make a paid 30-day Pilot worth considering, "
                            "and what evidence would your team need to defend that decision internally?"
                        ),
                        ar=(
                            "ما النتيجة أو المشكلة التشغيلية التي تجعل التفكير في برنامج مدفوع لمدة 30 يومًا "
                            "منطقيًا، وما الأدلة التي يحتاجها فريقكم للدفاع عن القرار داخليًا؟"
                        ),
                    ),
                ),
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Next step", ar="الخطوة التالية"),
                    body=BilingualRenderer.bt(
                        en=(
                            "Complete the Free Mini Diagnostic first. If the opportunity qualifies, prepare a "
                            "customer-specific scope and quote for the required approval."
                        ),
                        ar=(
                            "نُكمل التشخيص المصغر المجاني أولاً. إذا تأهلت الفرصة، نُعد نطاقًا وعرضًا خاصًا "
                            "بالعميل للموافقة المطلوبة."
                        ),
                    ),
                ),
            ],
            "closing": [
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Confirm evidence", ar="تأكيد الأدلة"),
                    body=BilingualRenderer.bt(
                        en=(
                            "Before any commitment, confirm the problem, decision owner, lawful data, baseline, "
                            "proof path, budget/timing discussion, and applicable approval gates."
                        ),
                        ar=(
                            "قبل أي التزام، نؤكد المشكلة وصاحب القرار والبيانات النظامية وخط الأساس ومسار "
                            "الإثبات ومناقشة الميزانية والتوقيت وبوابات الموافقة المطبقة."
                        ),
                    ),
                ),
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Commercial next step", ar="الخطوة التجارية التالية"),
                    body=BilingualRenderer.bt(
                        en=(
                            "If qualification and the active launch gate pass, prepare the named-customer 30-day "
                            "Pilot scope, acceptance criteria, proof cadence, exclusions, and quote for approval. "
                            "Do not send or commit until the relevant external-action gate permits it."
                        ),
                        ar=(
                            "إذا اجتاز التأهيل وبوابة الإطلاق الفعالة، نُعد نطاق البرنامج التجريبي الخاص بالعميل "
                            "لمدة 30 يومًا ومعايير القبول ودورية الإثبات والاستثناءات والعرض للموافقة. ولا يتم "
                            "الإرسال أو الالتزام حتى تسمح بوابة الإجراء الخارجي ذات الصلة."
                        ),
                    ),
                ),
            ],
        }
        blocks = scripts.get(scenario, scripts["discovery_call"])
        return BilingualRenderer.wrap(
            {
                "scenario": scenario,
                "blocks": [BilingualRenderer.filter_block(block, lang) for block in blocks],
                "authority": self._authority_payload(),
            },
            lang,
        )
