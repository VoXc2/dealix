#!/usr/bin/env python3
"""Generate constitution, auditability, enterprise trust, and evidence bridge docs.

Run: py -3 scripts/generate_holding_vision_docs.py
"""

from __future__ import annotations

import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SEE = "\n## روابط\n\n- [DEALIX_EXECUTION_WAVES_AR.md](../strategic/DEALIX_EXECUTION_WAVES_AR.md)\n- [docs/00_foundation/](../00_foundation/) — طبقة دستور موازية مرقمة\n"


def md(title: str, role: str, bullets: list[str]) -> str:
    b = "\n".join(f"- {x}" for x in bullets)
    return textwrap.dedent(
        f"""# {title}

## الدور

{role}

## نقاط تشغيلية

{b}
{SEE}
""",
    ).strip() + "\n"


def write_pack(folder: str, title: str, files: list[tuple[str, str, str, list[str]]]) -> None:
    d = REPO / "docs" / folder
    d.mkdir(parents=True, exist_ok=True)
    rows = []
    for fname, t, role, bl in files:
        (d / fname).write_text(md(t, role, bl), encoding="utf-8")
        rows.append(f"| [{fname}]({fname}) | {t} |")
    readme = (
        textwrap.dedent(
            f"""# {title}

| ملف | موضوع |
|------|--------|
{chr(10).join(rows)}
""",
        ).strip()
        + SEE
        + "\n"
    )
    (d / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    write_pack(
        "00_constitution",
        "الدستور — Dealix كشركة تشغيل محكومة",
        [
            ("DEALIX_CONSTITUTION.md", "دستور Dealix", "من نحن قبل أي كود أو عرض.", ["Saudi Governed AI Operations Holding path"]),
            ("NON_NEGOTIABLES.md", "غير قابل للتفاوض", "حدود أمان وثقة.", ["No scraping / cold WA / LI automation / fake proof"]),
            ("WHAT_DEALIX_REFUSES.md", "ما نرفضه", "فلتر مبيعات وثقافة.", []),
            ("GOOD_REVENUE_BAD_REVENUE.md", "إيراد جيد وسيئ", "حماية التركيز.", []),
            ("OPERATING_EQUATION.md", "معادلة التشغيل", "Data + Workflow + AI + Governance + Proof.", []),
        ],
    )
    write_pack(
        "15_auditability",
        "Auditability — سلسلة أدلة ومساءلة",
        [
            ("AUDITABILITY_OS.md", "نظام التدقيق", "No compliance claim without evidence.", []),
            ("EVIDENCE_CHAIN.md", "سلسلة الأدلة", "Source → AI → Policy → Decision → Output → Proof.", []),
            ("ACCOUNTABILITY_MODEL.md", "نموذج المساءلة", "مالك + موافق + راعي عميل.", []),
            ("POLICY_CHECKABILITY.md", "قابلية فحص السياسات", "كل قاعدة قابلة للاختبار.", []),
            ("RESPONSIBILITY_ATTRIBUTION.md", "نسبة المسؤولية", "Actor → artifact.", []),
            ("AUDIT_METRICS.md", "مقاييس التدقيق", "تغطية سجلات وقرارات.", []),
        ],
    )
    write_pack(
        "enterprise_trust",
        "Enterprise Trust Data Room",
        [
            ("ENTERPRISE_TRUST_DATA_ROOM.md", "غرفة الثقة", "مكان واحد لكل أدلة المشتريات.", []),
            ("TRUST_PACK_INDEX.md", "فهرس Trust Pack", "روابط موحدة.", []),
            ("AUDIT_SUMMARIES.md", "ملخصات تدقيق", "", []),
            ("COMPLIANCE_REPORTS.md", "تقارير امتثال", "", []),
            ("INCIDENT_LOG_TEMPLATE.md", "قالب سجل حوادث", "", []),
        ],
    )
    d16 = REPO / "docs" / "16_evidence_control_plane"
    d16.mkdir(parents=True, exist_ok=True)
    (d16 / "EVIDENCE_TO_PRODUCTIZATION.md").write_text(
        md(
            "من الأدلة إلى التمنتج",
            "ربط Evidence Graph بإشارات منتج (modules, playbooks, pricing).",
            ["كل حلقة أدلة قوية تولّد candidate لـmodule أو معيار", "لا productization بدون Proof متكرر"],
        ),
        encoding="utf-8",
    )
    (d16 / "README.md").write_text(
        textwrap.dedent(
            """# Evidence Control Plane — جسر المستوى 4

| ملف | موضوع |
|------|--------|
| [EVIDENCE_TO_PRODUCTIZATION.md](EVIDENCE_TO_PRODUCTIZATION.md) | أدلة → منتج |

## ملاحظة

الوثائق التفصيلية الأساسية موجودة في [docs/15_evidence_control_plane/](../15_evidence_control_plane/).
هذا المجلد يكمّل مسار **Productization** دون تكرار الملفات الكاملة.
"""
        ).strip()
        + SEE
        + "\n",
        encoding="utf-8",
    )
    print("wrote docs/00_constitution, docs/15_auditability, docs/enterprise_trust, docs/16_evidence_control_plane")


if __name__ == "__main__":
    main()
