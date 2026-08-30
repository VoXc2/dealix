"""Governed commercial drafts for War Room targets (never a send authority)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.paths import ICP_AGENCY_YAML, REPO_ROOT

OBJECTION_PATH = REPO_ROOT / "docs/commercial/operations/objection_engine_registry.yaml"

CTA_AR = "إذا يناسبكم، أجهز Mini Diagnostic مجاني ومحدد على واقعكم، وبعده نقرر هل تستحق Discovery."
CURRENT_POSITIONING_AR = (
    "Dealix تربط السياق والإشارات التجارية بأولوية واضحة، تنفيذ محكوم، وإثبات قابل للمراجعة فوق أدواتكم الحالية."
)
CURRENT_PATH_AR = "المسار إذا ظهر fit: Mini Diagnostic مجاني -> Discovery مؤهلة -> عرض مخصص؛ لا سعر أو التزام قبل Discovery."
LEGACY_COMMERCIAL_LITERALS = (
    "499",
    "7-day",
    "7 day",
    "10 leads",
    "pilot صغير",
)


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def _load_objections() -> list[dict[str, str]]:
    data = _load_yaml(OBJECTION_PATH)
    items = data.get("objections") or []
    out: list[dict[str, str]] = []
    for ob in items:
        if isinstance(ob, dict):
            out.append(
                {
                    "id": str(ob.get("id") or ""),
                    "response_draft_ar": str(ob.get("response_draft_ar") or "").strip(),
                }
            )
    return out


def _truth_safe_snippet(value: str) -> str:
    text = value.strip()
    lowered = text.lower()
    if any(literal.lower() in lowered for literal in LEGACY_COMMERCIAL_LITERALS):
        return ""
    return text


def _default_objection_snippet(objections: list[dict[str, str]]) -> str:
    for ob in objections:
        if ob.get("id") == "crm_exists" and ob.get("response_draft_ar"):
            return _truth_safe_snippet(ob["response_draft_ar"].split("\n")[0])
    return ""


def build_outreach_draft_ar(row: dict[str, str], *, icp: dict[str, Any], objection_snippet: str) -> str:
    # ``icp`` is retained for API compatibility only. Canonical commercial
    # wording is intentionally not sourced from historical ICP/pricing files.
    del icp
    company = (row.get("company") or "فريقكم").strip()
    pain = (row.get("pain_hypothesis") or "").strip()
    channel = (row.get("channel") or "linkedin_manual").strip()

    opener = f"مرحباً {company} —"
    if channel.startswith("email"):
        opener = f"الموضوع: تشخيص تشغيلي مختصر — {company}\n\nمرحباً،"

    safe_objection = _truth_safe_snippet(objection_snippet)
    lines = [
        opener,
        "",
        pain or "أراجع أين يتشتت السياق التجاري بين الأدوات، ومن يملك الإجراء التالي، وكيف تثبت النتيجة.",
        "",
        CURRENT_POSITIONING_AR,
        "",
        CURRENT_PATH_AR,
        "",
    ]
    if safe_objection:
        lines.append(safe_objection[:200])
        lines.append("")
    lines.extend(
        [
            CTA_AR,
            "",
            "— Dealix (مسودة داخلية — لا إرسال بدون أهلية القناة وصلاحية تنفيذ محددة)",
        ]
    )
    return "\n".join(lines).strip()


def attach_outreach_drafts(payload: dict[str, Any]) -> dict[str, Any]:
    """Mutate War Room payload targets with current-truth draft copy only."""
    icp = _load_yaml(ICP_AGENCY_YAML)
    objections = _load_objections()
    snippet = _default_objection_snippet(objections)

    targets = payload.get("targets") or {}
    items = list(targets.get("items") or [])
    for row in items:
        if isinstance(row, dict) and not (row.get("outreach_draft_ar") or "").strip():
            row["outreach_draft_ar"] = build_outreach_draft_ar(row, icp=icp, objection_snippet=snippet)

    follow = payload.get("follow_ups_due") or []
    for row in follow:
        if isinstance(row, dict) and not (row.get("outreach_draft_ar") or "").strip():
            row["outreach_draft_ar"] = build_outreach_draft_ar(row, icp=icp, objection_snippet=snippet)

    payload["outreach_policy_ar"] = (
        "مسودات داخلية فقط؛ target/status لا يساوي علاقة أو موافقة أو صلاحية إرسال. "
        "أي أثر خارجي يحتاج أهلية القناة، consent/suppression عند اللزوم، وصلاحية تنفيذ محددة قابلة للانتهاء."
    )
    payload["commercial_path_ar"] = CURRENT_PATH_AR
    return payload
