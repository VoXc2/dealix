"""Offer and pitch generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .catalog import OFFERS_OUT_DIR, TEMPLATES_DIR, load_service_catalog
from .kpis import kpis_for_service
from .playbooks import playbook_for_service
from .pricing import get_service_pricing, parse_service_id
from .risk import risk_for_service


def _render_template(template_path: Path, payload: dict[str, str]) -> str:
    text = template_path.read_text(encoding="utf-8")
    for key, value in payload.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def _lookup_engine_summary(engine: str) -> dict[str, Any]:
    catalog = load_service_catalog()
    for line in catalog["service_lines"]:
        mapped_engine = line["line_id"].upper()
        if mapped_engine == engine:
            return line
    # Manual overlays used for sellable service naming.
    overlays = {
        "CUSTOMER_PORTAL": {
            "line_outcome_ar": "تجربة عميل واضحة مع خطط أسبوعية واعتمادات ومخرجات قابلة للقياس."
        },
        "SECURITY": {
            "line_outcome_ar": "تحكم أمني تشغيلي يرفع الثقة ويقلل مخاطر الوصول والبيانات."
        },
        "OBSERVABILITY": {
            "line_outcome_ar": "رؤية تشغيلية دقيقة للتكلفة، الأداء، المخاطر، وأثر القرار."
        },
    }
    if engine in overlays:
        return overlays[engine]
    raise ValueError(f"No engine summary found for {engine}")


def generate_offer(
    service_id: str,
    segment: str,
    lang: str = "ar",
    output_dir: Path | None = None,
) -> dict[str, Path]:
    engine, tier = parse_service_id(service_id)
    pricing = get_service_pricing(service_id, segment)
    kpis = kpis_for_service(service_id)
    playbook = playbook_for_service(service_id)
    risks = risk_for_service(service_id)
    summary = _lookup_engine_summary(engine)

    target_dir = output_dir or OFFERS_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{service_id.lower()}_{segment}"

    risks_text = "\n".join(
        f"- {r['risk']} (severity: {r['severity']}) — mitigation: {r['mitigation']}"
        for r in risks
    ) or "- لا توجد مخاطر مسجلة."

    payload = {
        "service_id": service_id,
        "segment": segment,
        "tier": tier,
        "problem": summary.get("line_outcome_ar", ""),
        "decision": playbook["decision_gate"],
        "scope": "\n".join(f"- {item}" for item in playbook["implementation_steps"]),
        "out_of_scope": "\n".join(f"- {item}" for item in playbook["out_of_scope"]),
        "duration_days": str(playbook["delivery_window_days"]),
        "setup_fee_sar": str(pricing["setup_fee_sar"]),
        "monthly_retainer_sar": str(pricing["monthly_retainer_sar"]),
        "minimum_contract_months": str(pricing["minimum_contract_months"]),
        "kpis": "\n".join(f"- {item}" for item in kpis["business_kpis"]),
        "requirements": "\n".join(f"- {item}" for item in pricing["requires"]),
        "risks": risks_text,
        "stopping_conditions": "\n".join(
            f"- {item}" for item in playbook["stopping_conditions"]
        ),
        "next_step": playbook["next_step"],
        "acceptance_criteria": "\n".join(
            f"- {item}" for item in playbook["acceptance_criteria"]
        ),
    }

    offer_template = TEMPLATES_DIR / ("offer_ar.md" if lang == "ar" else "offer_en.md")
    sow_template = TEMPLATES_DIR / "sow_ar.md"
    risk_template = TEMPLATES_DIR / "executive_summary_ar.md"

    offer_out = target_dir / f"{stem}_offer.md"
    sow_out = target_dir / f"{stem}_sow.md"
    risk_out = target_dir / f"{stem}_risk_register.md"

    offer_out.write_text(_render_template(offer_template, payload), encoding="utf-8")
    sow_out.write_text(_render_template(sow_template, payload), encoding="utf-8")
    risk_out.write_text(_render_template(risk_template, payload), encoding="utf-8")

    return {
        "offer": offer_out,
        "sow": sow_out,
        "risk_register": risk_out,
    }


def build_pitch(service_id: str, lang: str = "ar") -> str:
    engine, tier = parse_service_id(service_id)
    summary = _lookup_engine_summary(engine)
    if lang == "ar":
        return (
            f"{service_id}: هذا العرض ({tier}) يحل مشكلة \"{summary['line_outcome_ar']}\" "
            "عبر قرار واضح، تنفيذ منضبط، وإثبات أثر قابل للقياس مع حوكمة كاملة."
        )
    return (
        f"{service_id}: This {tier} offer solves a measurable business pain with "
        "decision clarity, governed execution, and proof-led outcomes."
    )
