"""Universal Diagnostic Factory — one canonical factory, 50 families, D0-D5, overlays."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"

LOCALE_AR = "ar"
LOCALE_EN = "en"
SUPPORTED_LOCALES = (LOCALE_AR, LOCALE_EN)

TRUTH_CLASS_PATTERN = "PATTERN"
TRUTH_CLASS_ESTIMATED = "ESTIMATED"
TRUTH_CLASS_UNKNOWN = "UNKNOWN"

ESTIMATE_LABEL_AR = "تقدير — ليس قياسًا مؤكدًا"
ESTIMATE_LABEL_EN = "ESTIMATED — not a measured fact"

class DiagnosticDepth(StrEnum):
    D0_SIGNAL_SCAN = "D0_signal_scan"
    D1_RAPID = "D1_rapid"
    D2_FUNCTIONAL = "D2_functional"
    D3_CROSS_FUNCTIONAL = "D3_cross_functional"
    D4_DEEP_EVIDENCE = "D4_deep_evidence"
    D5_CONTINUOUS = "D5_continuous"

# Founder policy: every diagnostic depth is genuinely free. Depth describes
# diagnostic scope/evidence intensity, never payment status.
FREE_DEPTHS: frozenset[DiagnosticDepth] = frozenset(DiagnosticDepth)

class DiagnosticFamily(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    family_id: str  # A01..A50
    name: str
    description: str
    depth: DiagnosticDepth = DiagnosticDepth.D1_RAPID
    sector_fit: list[str] = Field(default_factory=list)
    buyer_fit: list[str] = Field(default_factory=list)
    evidence_required: list[str] = Field(default_factory=list)
    economic_relevance: str = UNKNOWN

class SectorSurface(BaseModel):
    """A commercial surface a buyer names, mapped to one canonical sector pack.

    Surfaces are aliases, not new systems: many verticals share a canonical
    sector pack plus a primary family set. Pattern knowledge only.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    surface_id: str
    canonical_sector: str  # a canonical sector id, or "*" for size-only surfaces
    ar_name: str
    en_name: str
    primary_families: list[str] = Field(default_factory=list)
    company_size_hint: str = UNKNOWN

# 50 families catalog (condensed, covers spec)
FAMILIES: list[DiagnosticFamily] = [
    DiagnosticFamily(family_id="A01", name="Executive/Strategy", description="priorities, business model, decision architecture", depth=DiagnosticDepth.D1_RAPID, buyer_fit=["ceo","founder"]),
    DiagnosticFamily(family_id="A02", name="Business Model", description="revenue streams, value prop, segments", depth=DiagnosticDepth.D1_RAPID),
    DiagnosticFamily(family_id="A03", name="Financial Performance", description="revenue, margin, cash conversion", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["cfo"]),
    DiagnosticFamily(family_id="A04", name="Cash/Collections", description="DSO, overdue, collection", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["cfo"]),
    DiagnosticFamily(family_id="A05", name="Revenue Leakage", description="missed leads, stale, unquoted", depth=DiagnosticDepth.D1_RAPID, sector_fit=["technology_saas_si","professional_services"]),
    DiagnosticFamily(family_id="A06", name="Sales OS", description="ICP, qualification, pipeline", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["sales_director"]),
    DiagnosticFamily(family_id="A07", name="Marketing/Demand", description="positioning, SEO, AI search, CAC", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["marketing_director"]),
    DiagnosticFamily(family_id="A08", name="Customer Experience", description="onboarding, support, churn", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A09", name="Customer Service", description="ticket inflow, routing, automation", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A10", name="Operations", description="throughput, bottlenecks, exceptions", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["coo","operations_director"]),
    DiagnosticFamily(family_id="A11", name="Business Process", description="process inventory, owner, KPI, waste", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A12", name="Automation Opportunity", description="DETERMINISTIC vs AGENTIC classification, frequency*minutes", depth=DiagnosticDepth.D1_RAPID),
    DiagnosticFamily(family_id="A13", name="AI Readiness", description="use cases, data, governance, economics", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["cio","cto"]),
    DiagnosticFamily(family_id="A14", name="AI Governance", description="inventory, risk, oversight, third parties", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["ciso","cdo"]),
    DiagnosticFamily(family_id="A15", name="Agentic AI Readiness", description="authority, tool permissions, auditability", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A16", name="AI Economics", description="tokens, cost per accepted result", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A17", name="Cybersecurity", description="governance, identity, monitoring, suppliers", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["ciso"]),
    DiagnosticFamily(family_id="A18", name="Data", description="source, quality, lineage, governance", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["cdo","cio"]),
    DiagnosticFamily(family_id="A19", name="Document Intelligence", description="extraction, approvals, search, versioning", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A20", name="Knowledge Mgmt", description="sources, freshness, conversion", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A21", name="IT Landscape", description="ERP/CRM/HR, SaaS sprawl", depth=DiagnosticDepth.D1_RAPID, buyer_fit=["cio"]),
    DiagnosticFamily(family_id="A22", name="Integration", description="SYSTEM→DATA→EVENT→ACTION mapping", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A23", name="Cloud/Infra", description="availability, cost, backup, vendor lock-in", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A24", name="Software Engineering", description="CI/CD, test, debt, incidents", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["cto"]),
    DiagnosticFamily(family_id="A25", name="Procurement", description="request→pay, supplier performance", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["procurement_director"]),
    DiagnosticFamily(family_id="A26", name="Supply Chain", description="demand, inventory, fulfillment", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A27", name="Inventory", description="accuracy, stockouts, replenishment", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A28", name="Project Delivery", description="scope, schedule, change, billing", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["project_director"]),
    DiagnosticFamily(family_id="A29", name="Construction/EPC Commercial", description="RFI, variations, claims, payment", depth=DiagnosticDepth.D2_FUNCTIONAL, sector_fit=["construction_epc"]),
    DiagnosticFamily(family_id="A30", name="Contract", description="obligations, milestones, SLA, risk", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A31", name="Workforce/HR Ops", description="hiring, role clarity, productivity", depth=DiagnosticDepth.D2_FUNCTIONAL, buyer_fit=["hr_director"]),
    DiagnosticFamily(family_id="A32", name="Quality", description="defects, rework, root cause", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A33", name="Risk/Control", description="risks, controls, owners, gaps", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A34", name="Vendor/Third-Party", description="criticality, concentration, cyber", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A35", name="Partner/Channel", description="fit, incentives, economics", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A36", name="B2G/Procurement Readiness", description="CR, Jadeer, tender fit, partner needs", depth=DiagnosticDepth.D2_FUNCTIONAL, sector_fit=["government_b2g"]),
    DiagnosticFamily(family_id="A37", name="Fatoora Technical Ops", description="ERP/invoice, XML, API, exception, observability", depth=DiagnosticDepth.D2_FUNCTIONAL, sector_fit=["finance_fintech_insurance"]),
    DiagnosticFamily(family_id="A38", name="Website/Digital Front Door", description="performance, trust, conversion, SEO", depth=DiagnosticDepth.D1_RAPID),
    DiagnosticFamily(family_id="A39", name="SEO/AI Search", description="crawlability, structured, AI visibility", depth=DiagnosticDepth.D1_RAPID, buyer_fit=["marketing_director"]),
    DiagnosticFamily(family_id="A40", name="Communication Ops", description="inbound, routing, consent, CRM", depth=DiagnosticDepth.D1_RAPID),
    DiagnosticFamily(family_id="A41", name="Meeting-to-Action", description="capture, decisions, owner, follow-up", depth=DiagnosticDepth.D1_RAPID),
    DiagnosticFamily(family_id="A42", name="Executive Reporting", description="KPIs, latency, actionability", depth=DiagnosticDepth.D1_RAPID, buyer_fit=["ceo"]),
    DiagnosticFamily(family_id="A43", name="Analytics", description="metric defs, funnels, attribution", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A44", name="Compliance Ops", description="obligations, evidence, escalation", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A45", name="Business Continuity", description="critical processes, backup, RTO/RPO", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A46", name="Facility/Field Ops", description="work orders, dispatch, SLAs", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A47", name="Asset Maintenance", description="register, preventive, downtime", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A48", name="Fraud/Anomaly", description="duplicate, control gaps, approval anomalies", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A49", name="Service Delivery", description="intake, fulfillment, QA, profitability", depth=DiagnosticDepth.D2_FUNCTIONAL),
    DiagnosticFamily(family_id="A50", name="Company OS", description="TRUTH, PRIORITY, PEOPLE, PROCESS, SYSTEMS, DATA, AI, AUTHORITY, PROOF, ECONOMICS", depth=DiagnosticDepth.D3_CROSS_FUNCTIONAL, buyer_fit=["ceo"]),
]

# Arabic-first family names. Internal pattern knowledge, not customer facts.
FAMILY_AR: dict[str, str] = {
    "A01": "الإدارة والاستراتيجية",
    "A02": "نموذج العمل",
    "A03": "الأداء المالي",
    "A04": "النقد والتحصيل",
    "A05": "تسرّب الإيراد",
    "A06": "نظام المبيعات",
    "A07": "التسويق والطلب",
    "A08": "تجربة العميل",
    "A09": "خدمة العملاء",
    "A10": "العمليات",
    "A11": "العمليات الإدارية",
    "A12": "فرص الأتمتة",
    "A13": "جاهزية الذكاء الاصطناعي",
    "A14": "حوكمة الذكاء الاصطناعي",
    "A15": "جاهزية الوكلاء الأذكياء",
    "A16": "اقتصاديات الذكاء الاصطناعي",
    "A17": "الأمن السيبراني",
    "A18": "البيانات",
    "A19": "ذكاء المستندات",
    "A20": "إدارة المعرفة",
    "A21": "الأنظمة التقنية",
    "A22": "التكامل بين الأنظمة",
    "A23": "السحابة والبنية التحتية",
    "A24": "هندسة البرمجيات",
    "A25": "المشتريات",
    "A26": "سلسلة التوريد",
    "A27": "المخزون",
    "A28": "تسليم المشاريع",
    "A29": "الجانب التجاري للإنشاءات",
    "A30": "العقود",
    "A31": "عمليات القوى العاملة",
    "A32": "الجودة",
    "A33": "المخاطر والضوابط",
    "A34": "الموردون والأطراف الثالثة",
    "A35": "الشراكات والقنوات",
    "A36": "جاهزية القطاع الحكومي",
    "A37": "عمليات فاتورة الإلكترونية",
    "A38": "الواجهة الرقمية والموقع",
    "A39": "تحسين محركات البحث والبحث الذكي",
    "A40": "عمليات التواصل",
    "A41": "من الاجتماع إلى التنفيذ",
    "A42": "تقارير الإدارة",
    "A43": "التحليلات",
    "A44": "عمليات الالتزام",
    "A45": "استمرارية الأعمال",
    "A46": "عمليات المرافق والميدان",
    "A47": "صيانة الأصول",
    "A48": "الاحتيال والشذوذ",
    "A49": "تسليم الخدمات",
    "A50": "نظام تشغيل الشركة",
}

# 30 requested commercial surfaces -> canonical sector packs. Expandable: add a
# surface here (or extend SECTOR_INTEL) instead of building a parallel system.
SECTOR_SURFACES: list[SectorSurface] = [
    SectorSurface(surface_id="logistics", canonical_sector="logistics_supply_chain", ar_name="الخدمات اللوجستية", en_name="Logistics", primary_families=["A10", "A12", "A26", "A27", "A46"]),
    SectorSurface(surface_id="ports_marine", canonical_sector="logistics_supply_chain", ar_name="الموانئ والبحري", en_name="Ports & Marine", primary_families=["A10", "A26", "A28", "A46"]),
    SectorSurface(surface_id="construction", canonical_sector="construction_epc", ar_name="المقاولات والإنشاءات", en_name="Construction/EPC", primary_families=["A28", "A29", "A30", "A04"]),
    SectorSurface(surface_id="real_estate", canonical_sector="real_estate_proptech", ar_name="العقار", en_name="Real Estate", primary_families=["A05", "A08", "A28", "A46"]),
    SectorSurface(surface_id="retail", canonical_sector="retail_commerce_ecommerce", ar_name="التجزئة", en_name="Retail", primary_families=["A05", "A08", "A09", "A27"]),
    SectorSurface(surface_id="ecommerce", canonical_sector="retail_commerce_ecommerce", ar_name="التجارة الإلكترونية", en_name="E-commerce", primary_families=["A05", "A07", "A08", "A27", "A38"]),
    SectorSurface(surface_id="hospitality", canonical_sector="tourism_hospitality", ar_name="الضيافة والفنادق", en_name="Hospitality", primary_families=["A08", "A09", "A10", "A46"]),
    SectorSurface(surface_id="restaurants", canonical_sector="tourism_hospitality", ar_name="المطاعم", en_name="Restaurants", primary_families=["A08", "A09", "A10", "A27"]),
    SectorSurface(surface_id="healthcare_operations", canonical_sector="healthcare", ar_name="العمليات الصحية", en_name="Healthcare Operations", primary_families=["A08", "A09", "A18", "A44"]),
    SectorSurface(surface_id="clinics", canonical_sector="healthcare", ar_name="العيادات", en_name="Clinics", primary_families=["A08", "A09", "A40", "A44"]),
    SectorSurface(surface_id="manufacturing", canonical_sector="industrial_manufacturing", ar_name="التصنيع", en_name="Manufacturing", primary_families=["A10", "A27", "A32", "A47"]),
    SectorSurface(surface_id="industrial", canonical_sector="industrial_manufacturing", ar_name="القطاع الصناعي", en_name="Industrial", primary_families=["A10", "A11", "A32", "A47"]),
    SectorSurface(surface_id="automotive", canonical_sector="mobility_automotive", ar_name="السيارات والتنقل", en_name="Automotive/Mobility", primary_families=["A05", "A25", "A27", "A46"]),
    SectorSurface(surface_id="education", canonical_sector="education_training", ar_name="التعليم والتدريب", en_name="Education", primary_families=["A05", "A08", "A31", "A49"]),
    SectorSurface(surface_id="hr_recruitment", canonical_sector="professional_services", ar_name="الموارد البشرية والتوظيف", en_name="HR & Recruitment", primary_families=["A31", "A11", "A12", "A49"]),
    SectorSurface(surface_id="professional_services", canonical_sector="professional_services", ar_name="الخدمات المهنية", en_name="Professional Services", primary_families=["A05", "A06", "A28", "A49"]),
    SectorSurface(surface_id="accounting", canonical_sector="professional_services", ar_name="المحاسبة", en_name="Accounting", primary_families=["A03", "A04", "A11", "A12"]),
    SectorSurface(surface_id="finance_operations", canonical_sector="finance_fintech_insurance", ar_name="العمليات المالية", en_name="Finance Operations", primary_families=["A03", "A04", "A37", "A48"]),
    SectorSurface(surface_id="legal_operations", canonical_sector="professional_services", ar_name="العمليات القانونية", en_name="Legal Operations", primary_families=["A19", "A30", "A44", "A11"]),
    SectorSurface(surface_id="insurance_operations", canonical_sector="finance_fintech_insurance", ar_name="عمليات التأمين", en_name="Insurance Operations", primary_families=["A08", "A19", "A30", "A48"]),
    SectorSurface(surface_id="facilities", canonical_sector="real_estate_proptech", ar_name="إدارة المرافق", en_name="Facilities Management", primary_families=["A46", "A47", "A25", "A10"]),
    SectorSurface(surface_id="maintenance", canonical_sector="real_estate_proptech", ar_name="الصيانة", en_name="Maintenance", primary_families=["A46", "A47", "A32", "A10"]),
    SectorSurface(surface_id="field_services", canonical_sector="logistics_supply_chain", ar_name="الخدمات الميدانية", en_name="Field Services", primary_families=["A46", "A47", "A40", "A10"]),
    SectorSurface(surface_id="procurement", canonical_sector="export_import_rhq", ar_name="المشتريات", en_name="Procurement", primary_families=["A25", "A30", "A34", "A48"]),
    SectorSurface(surface_id="warehousing", canonical_sector="logistics_supply_chain", ar_name="المستودعات", en_name="Warehousing", primary_families=["A26", "A27", "A10", "A47"]),
    SectorSurface(surface_id="distribution", canonical_sector="logistics_supply_chain", ar_name="التوزيع", en_name="Distribution", primary_families=["A26", "A27", "A06", "A35"]),
    SectorSurface(surface_id="customer_service", canonical_sector="retail_commerce_ecommerce", ar_name="خدمة العملاء", en_name="Customer Service", primary_families=["A08", "A09", "A40", "A12"]),
    SectorSurface(surface_id="marketing", canonical_sector="telecom_media_marketing", ar_name="التسويق", en_name="Marketing", primary_families=["A07", "A39", "A38", "A43"]),
    SectorSurface(surface_id="technology_saas", canonical_sector="technology_saas_si", ar_name="التقنية وSaaS", en_name="Technology/SaaS", primary_families=["A05", "A13", "A24", "A38"]),
    SectorSurface(surface_id="sme", canonical_sector="*", ar_name="المنشآت الصغيرة والمتوسطة", en_name="SMEs", primary_families=["A01", "A05", "A11", "A12", "A38"], company_size_hint="sme"),
    SectorSurface(surface_id="enterprise_operations", canonical_sector="*", ar_name="عمليات المؤسسات الكبرى", en_name="Enterprise Operations", primary_families=["A50", "A11", "A18", "A43"], company_size_hint="enterprise"),
]

class UniversalDiagnosticFactory:
    """One canonical factory — composes diagnostics dynamically."""

    def __init__(self) -> None:
        self.families = {f.family_id: f for f in FAMILIES}

    def resolve_surface(self, surface_id: str) -> SectorSurface | None:
        """Resolve a buyer-facing surface alias to its canonical sector pack."""
        key = (surface_id or "").strip().lower().replace("-", "_")
        for surface in SECTOR_SURFACES:
            if surface.surface_id == key:
                return surface
        return None

    def family_name(self, fam: DiagnosticFamily, locale: str = LOCALE_AR) -> str:
        if locale == LOCALE_AR:
            return FAMILY_AR.get(fam.family_id, fam.name)
        return fam.name

    def is_free(self, depth: DiagnosticDepth) -> bool:
        """D0-D2 are genuinely free; deeper depths need qualified discovery."""
        return depth in FREE_DEPTHS

    def compose(self, sector: str, company_size: str, buyer_role: str, problem: str, depth: DiagnosticDepth = DiagnosticDepth.D1_RAPID) -> list[DiagnosticFamily]:
        # Adaptive: filter by sector/buyer/problem relevance — token-based, inclusive
        surface = self.resolve_surface(sector)
        canonical_sector = surface.canonical_sector if surface else sector
        if canonical_sector == "*":
            canonical_sector = "professional_services"
            if surface and surface.company_size_hint != UNKNOWN:
                company_size = surface.company_size_hint
        surface_primary = set(surface.primary_families) if surface else set()
        selected: list[DiagnosticFamily] = []
        problem_tokens = set(problem.lower().replace("-", "_").split("_")) if problem != UNKNOWN else set()
        sector_l = canonical_sector.lower()
        buyer_l = buyer_role.lower()
        for f in FAMILIES:
            # Depth filter (allow equal or shallower)
            if f.depth.value > depth.value and depth != DiagnosticDepth.D0_SIGNAL_SCAN:
                continue
            score = 0
            # Surface primary families — the strongest signal for a named surface
            if f.family_id in surface_primary:
                score += 4
            # Sector overlay — bonus, not strict
            if f.sector_fit and sector_l in [s.lower() for s in f.sector_fit]:
                score += 3
            elif f.sector_fit and sector_l not in [s.lower() for s in f.sector_fit]:
                # Keep if core or problem matches
                pass
            # Buyer overlay
            if f.buyer_fit and buyer_l in [b.lower() for b in f.buyer_fit]:
                score += 2
            # Problem relevance — token overlap
            desc_l = (f.description + " " + f.name).lower()
            if problem_tokens and any(tok in desc_l for tok in problem_tokens if len(tok) > 2):
                score += 2
                selected.append(f)
                continue
            # Include core families for D1
            if f.family_id in ("A01","A05","A11","A12","A38"):
                selected.append(f)
                continue
            if f.family_id in ("A03","A04","A10") and buyer_l in ("cfo","coo"):
                selected.append(f)
                continue
            if score >= 2:
                selected.append(f)
                continue
        # Deduplicate, limit to 12 max for focus
        seen = set()
        result = []
        for f in selected:
            if f.family_id not in seen:
                result.append(f)
                seen.add(f.family_id)
                if len(result) >= 12:
                    break
        # Guarantee the surface's primary families are present (depth-bounded).
        if surface:
            for fid in surface.primary_families:
                fam = self.families.get(fid)
                if fam is None or fid in seen:
                    continue
                if fam.depth.value > depth.value and depth != DiagnosticDepth.D0_SIGNAL_SCAN:
                    continue
                result.insert(0, fam)
                seen.add(fid)
            result = result[:12]
        return result or [self.families["A01"], self.families["A11"]]

    def compose_for_surface(
        self,
        surface_id: str,
        buyer_role: str = "ceo",
        problem: str = UNKNOWN,
        depth: DiagnosticDepth = DiagnosticDepth.D1_RAPID,
        company_size: str = UNKNOWN,
    ) -> tuple[SectorSurface | None, list[DiagnosticFamily]]:
        """Compose a diagnostic from a buyer-facing surface name (alias-safe)."""
        surface = self.resolve_surface(surface_id)
        if company_size == UNKNOWN:
            company_size = surface.company_size_hint if surface and surface.company_size_hint != UNKNOWN else "sme"
        families = self.compose(surface_id, company_size, buyer_role, problem, depth)
        return surface, families

    def surface_coverage(self) -> dict[str, list[str]]:
        """Canonical sector -> commercial surfaces it serves (coverage map)."""
        covered: dict[str, list[str]] = {}
        for surface in SECTOR_SURFACES:
            covered.setdefault(surface.canonical_sector, []).append(surface.surface_id)
        return covered

    def generate_questions(self, fam: DiagnosticFamily, evidence: dict[str, Any] | None = None, locale: str = LOCALE_AR) -> list[dict[str, Any]]:
        # Adaptive questions — only those that change decision. Arabic-first, EN parity.
        locale = locale if locale in SUPPORTED_LOCALES else LOCALE_AR
        name_ar = FAMILY_AR.get(fam.family_id, fam.name)
        text_ar_q1 = f"هل يمكن تزويدنا بمُخرَج نظام فعلي (تصدير أو تقرير) يوضح «{name_ar}» خلال آخر 90 يومًا؟"
        text_ar_q2 = f"كم مرة يتكرر العمل اليدوي أو التأخير في «{name_ar}» شهريًا؟ (رقم تقديري)"
        text_en_q1 = f"Can you provide a real system export (report or file) covering '{fam.name}' from the last 90 days?"
        text_en_q2 = f"How many manual or delayed events per month in '{fam.name}'? (estimate)"
        base = [
            {
                "question_id": f"{fam.family_id}_Q1",
                "question_text": text_ar_q1 if locale == LOCALE_AR else text_en_q1,
                "text_ar": text_ar_q1,
                "text_en": text_en_q1,
                "reason": "evidence_needed",
                "evidence_needed": "system_export",
                "economic_relevance": "high",
                "answer_type": "text",
                "branch_condition": "if manual_steps>5",
                "truth_class": TRUTH_CLASS_PATTERN,
            },
            {
                "question_id": f"{fam.family_id}_Q2",
                "question_text": text_ar_q2 if locale == LOCALE_AR else text_en_q2,
                "text_ar": text_ar_q2,
                "text_en": text_en_q2,
                "reason": "confidence_impact",
                "evidence_needed": "interview",
                "economic_relevance": "medium",
                "answer_type": "number",
                "branch_condition": "if delay>7",
                "truth_class": TRUTH_CLASS_ESTIMATED,
            },
        ]
        if evidence:
            for q in base:
                q["evidence_state"] = "PRESENT" if evidence.get(q["evidence_needed"]) else "MISSING"
        return base

    def economic_leakage(self, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        # Translate findings to leakage types. Numbers are only used when the
        # caller supplies a basis; nothing is invented here.
        leakage: list[dict[str, Any]] = []
        for f in findings:
            if "manual" not in f.get("finding", "").lower():
                continue
            frequency = f.get("annual_frequency", UNKNOWN)
            time_per_event = f.get("time_per_event", UNKNOWN)
            basis = f.get("estimate_basis", UNKNOWN)
            has_basis = frequency != UNKNOWN and time_per_event != UNKNOWN and basis != UNKNOWN
            leakage.append({
                "type": "MANUAL_LABOR",
                "finding": f["finding"],
                "evidence": f.get("evidence", UNKNOWN),
                "confidence": f.get("confidence", "WEAK_EVIDENCE"),
                "annual_frequency": frequency,
                "time_per_event": time_per_event,
                "annual_hours": f.get("annual_hours", UNKNOWN),
                "truth_class": TRUTH_CLASS_ESTIMATED if has_basis else TRUTH_CLASS_UNKNOWN,
                "estimate_label_ar": ESTIMATE_LABEL_AR if has_basis else UNKNOWN,
                "estimate_label_en": ESTIMATE_LABEL_EN if has_basis else UNKNOWN,
                "estimate_basis": basis,
                "is_measured_fact": False,
            })
        return leakage

    def value_estimate(self, leakage: list[dict[str, Any]], hourly_cost_sar: Any = UNKNOWN) -> dict[str, Any]:
        """Range estimate, only with a caller-supplied cost basis.

        Never invents hourly cost, frequency, or ROI. UNKNOWN otherwise.
        """
        unknown = {
            "value_range_sar": UNKNOWN,
            "truth_class": TRUTH_CLASS_UNKNOWN,
            "estimate_label_ar": UNKNOWN,
            "estimate_label_en": UNKNOWN,
            "estimate_basis": UNKNOWN,
            "is_measured_fact": False,
        }
        if hourly_cost_sar == UNKNOWN or not leakage:
            return unknown
        try:
            hourly = float(hourly_cost_sar)
        except (TypeError, ValueError):
            return unknown
        low = high = 0.0
        for item in leakage:
            if item.get("truth_class") != TRUTH_CLASS_ESTIMATED:
                continue
            try:
                annual_hours = float(item.get("annual_hours", UNKNOWN))
            except (TypeError, ValueError):
                continue
            low += annual_hours * hourly * 0.8
            high += annual_hours * hourly * 1.2
        if high <= 0:
            return unknown
        return {
            "value_range_sar": {"low": round(low), "high": round(high)},
            "truth_class": TRUTH_CLASS_ESTIMATED,
            "estimate_label_ar": ESTIMATE_LABEL_AR,
            "estimate_label_en": ESTIMATE_LABEL_EN,
            "estimate_basis": "caller_supplied_hourly_cost_sar",
            "is_measured_fact": False,
        }

    def to_proposal(self, families: list[DiagnosticFamily], economic_leakage: list[dict[str, Any]]) -> dict[str, Any]:
        has_estimates = any(item.get("truth_class") == TRUTH_CLASS_ESTIMATED for item in economic_leakage)
        return {
            "families": [f.family_id for f in families],
            "leakage": economic_leakage,
            "next_step": "discovery" if economic_leakage else "signal_scan",
            "evidence_confidence": "MODERATE_EVIDENCE" if economic_leakage else "HYPOTHESIS",
            "truth_class": TRUTH_CLASS_ESTIMATED if has_estimates else TRUTH_CLASS_PATTERN,
            "estimate_labels": {"ar": ESTIMATE_LABEL_AR, "en": ESTIMATE_LABEL_EN} if has_estimates else {},
            "free_depths": [d.value for d in FREE_DEPTHS],
        }

__all__ = [
    "UniversalDiagnosticFactory",
    "DiagnosticDepth",
    "DiagnosticFamily",
    "FAMILIES",
    "FAMILY_AR",
    "SECTOR_SURFACES",
    "SectorSurface",
    "FREE_DEPTHS",
    "SUPPORTED_LOCALES",
    "LOCALE_AR",
    "LOCALE_EN",
    "TRUTH_CLASS_PATTERN",
    "TRUTH_CLASS_ESTIMATED",
    "TRUTH_CLASS_UNKNOWN",
    "ESTIMATE_LABEL_AR",
    "ESTIMATE_LABEL_EN",
    "UNKNOWN",
]
