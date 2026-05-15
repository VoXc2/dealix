"""Machine-readable index for docs/NN_* master layers ↔ implementation paths.

See docs/DEALIX_MASTER_LAYERS_MAP.md and docs/enterprise_architecture/SYSTEM_MAP.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DealixLayer:
    """One numbered layer in the Dealix constitution map."""

    folder: str
    title_ar: str
    primary_packages: tuple[str, ...]


# Order matches docs/00 … docs/36 README sequence.
MASTER_LAYERS: tuple[DealixLayer, ...] = (
    DealixLayer("00_constitution", "الأطروحة والدستور", ("revenue_memory", "institutional_control_os")),
    DealixLayer("01_category_creation", "صناعة الفئة", ("category_os",)),
    DealixLayer("02_strategy", "الهوية الاستراتيجية", ("strategy_os", "gtm_os")),
    DealixLayer("03_saudi_positioning", "التموضع السعودي", ("market_intelligence", "revenue_os")),
    DealixLayer("04_product_strategy", "استراتيجية المنتج", ("service_catalog", "commercial_engagements")),
    DealixLayer("05_client_os", "نظام تشغيل العميل", ("client_os",)),
    DealixLayer("06_data_os", "طبقة البيانات", ("data_os", "customer_data_plane")),
    DealixLayer("07_governance", "الحوكمة", ("governance_os", "compliance_trust_os")),
    DealixLayer("08_responsible_ai", "AI المسؤول", ("responsible_ai_os",)),
    DealixLayer("09_llm_gateway", "بوابة النماذج", ("llm_gateway_v10",)),
    DealixLayer("10_agents", "الوكلاء المحكومون", ("agentic_operations_os", "ai_workforce", "agent_governance")),
    DealixLayer("11_secure_runtime", "تشغيل آمن", ("tool_guardrail_gateway", "safe_send_gateway")),
    DealixLayer("12_auditability", "التدقيق والمساءلة", ("compliance_trust_os", "evidence_control_plane_os")),
    DealixLayer("13_evidence_control_plane", "سيطرة الأدلة", ("evidence_control_plane_os",)),
    DealixLayer("14_proof", "Proof OS", ("proof_architecture_os", "proof_ledger")),
    DealixLayer("15_value", "Value OS", ("value_capture_os", "proof_architecture_os")),
    DealixLayer("16_capital", "Capital OS", ("operating_finance_os", "board_decision_os")),
    DealixLayer("17_revenue_os", "Revenue OS", ("revenue_os", "revenue_pipeline")),
    DealixLayer("18_brain_os", "Company Brain", ("knowledge_os", "company_brain")),
    DealixLayer("19_workflow_os", "Workflow OS", ("delivery_os",)),
    DealixLayer("20_adoption", "التبني", ("adoption_os", "customer_success")),
    DealixLayer("21_operating_rhythm", "إيقاع التشغيل", ("operating_rhythm_os",)),
    DealixLayer("22_board_decision", "قرارات المجلس", ("board_decision_os",)),
    DealixLayer("23_intelligence", "الذكاء المركّب", ("intelligence_os", "intelligence_compounding_os")),
    DealixLayer("24_risk_resilience", "المخاطر والمرونة", ("risk_resilience_os",)),
    DealixLayer("25_compliance_trust", "الامتثال والثقة", ("compliance_trust_os", "compliance_os")),
    DealixLayer("26_human_amplified", "المنظمة المضخّمة بالبشر", ("personal_operator", "executive_command_center")),
    DealixLayer("27_value_capture", "التقاط القيمة", ("value_capture_os",)),
    DealixLayer("28_operating_finance", "المالية التشغيلية", ("operating_finance_os", "finance_os")),
    DealixLayer("29_enterprise_rollout", "دخول المؤسسات", ("enterprise_rollout_os", "enterprise_os")),
    DealixLayer("30_standards", "المعايير", ("standards_os",)),
    DealixLayer("31_certification", "الشهادات", ("ecosystem_os",)),
    DealixLayer("32_ecosystem", "النظام البيئي", ("ecosystem_os", "partnership_os")),
    DealixLayer("33_ventures", "مصنع المشاريع", ("endgame_os", "holding_os")),
    DealixLayer("34_market_power", "قوة السوق", ("market_power_os", "dominance_os")),
    DealixLayer("35_tests", "الاختبارات والحواجز", ("tests",)),
    DealixLayer("36_architecture", "المعمارية", ("api",)),
    # ── Institutional Intelligence Layer (SYSTEM 56–65) ──
    DealixLayer(
        "37_institutional_control_plane",
        "طبقة التحكم المؤسسية",
        ("institutional_control_os", "orchestrator"),
    ),
    DealixLayer(
        "38_agent_society",
        "مجتمع الوكلاء",
        ("agent_governance", "agentic_operations_os", "ai_workforce"),
    ),
    DealixLayer(
        "39_assurance_contracts",
        "عقود الضمان والأمان",
        ("governance_os", "secure_agent_runtime_os", "tool_guardrail_gateway"),
    ),
    DealixLayer(
        "40_memory_fabric",
        "نسيج الذاكرة المؤسسية",
        ("revenue_memory", "knowledge_os"),
    ),
    DealixLayer(
        "41_organizational_reasoning",
        "الاستدلال المؤسسي",
        ("intelligence_os", "intelligence_compounding_os", "meta_os"),
    ),
    DealixLayer(
        "42_resilience_chaos",
        "المرونة واختبار الفوضى",
        ("risk_resilience_os", "revenue_memory"),
    ),
    DealixLayer(
        "43_meta_governance",
        "الحوكمة الفوقية",
        ("meta_os", "governance_os"),
    ),
    DealixLayer(
        "44_institutional_value",
        "محرك القيمة المؤسسية",
        ("value_capture_os", "value_os", "proof_architecture_os"),
    ),
    DealixLayer(
        "45_institutional_learning",
        "محرك التعلم المؤسسي",
        ("learning_flywheel",),
    ),
    DealixLayer(
        "46_institutional_operating_core",
        "النواة التشغيلية المؤسسية",
        ("institutional_dependency_os",),
    ),
)

# Optional hints for cross-cutting concerns not tied to a single layer folder.
IMPLEMENTATION_HINTS: dict[str, tuple[str, ...]] = {
    "saudi_layer": ("revenue_os", "market_intelligence", "pipelines"),
    "revenue_memory": ("revenue_memory",),
}


def readme_path(repo_root: Path, folder: str) -> Path:
    return repo_root / "docs" / folder / "README.md"


def layer_by_folder(folder: str) -> DealixLayer | None:
    for layer in MASTER_LAYERS:
        if layer.folder == folder:
            return layer
    return None
