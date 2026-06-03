"""Governed first-touch outreach snippets for War Room P0 targets (no send)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.paths import ICP_AGENCY_YAML, REPO_ROOT

OBJECTION_PATH = REPO_ROOT / "docs/commercial/operations/objection_engine_registry.yaml"

CTA_AR = "هل يناسبكم Risk Score مجاني أو Sample Proof Pack على 10 leads عندكم؟"


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


def _default_objection_snippet(objections: list[dict[str, str]]) -> str:
    for ob in objections:
        if ob.get("id") == "crm_exists" and ob.get("response_draft_ar"):
            return ob["response_draft_ar"].split("\n")[0].strip()
    return ""


def build_outreach_draft_ar(row: dict[str, str], *, icp: dict[str, Any], objection_snippet: str) -> str:
    company = (row.get("company") or "فريقكم").strip()
    pain = (row.get("pain_hypothesis") or "").strip()
    core = str(icp.get("core_message_ar") or "").strip().replace("\n", " ")
    motion = (row.get("motion") or icp.get("motion") or "A").strip()
    channel = (row.get("channel") or "linkedin_manual").strip()

    opener = f"مرحباً {company} —"
    if channel.startswith("email"):
        opener = f"الموضوع: متابعة ما بعد الحملة — {company}\n\nمرحباً،"

    lines = [
        opener,
        "",
        pain or "بعد الحملة، السؤال عادة: من رد؟ من يتابع؟ وهل عندكم دليل؟",
        "",
    ]
    if core:
        lines.append(core[:280])
        lines.append("")
    if objection_snippet:
        lines.append(objection_snippet[:200])
        lines.append("")
    lines.extend(
        [
            f"Motion {motion} — نبدأ بـ pilot صغير (10 leads) بدون أتمتة إرسال.",
            CTA_AR,
            "",
            "— سامي · Dealix (مسودة — موافقة قبل أي إرسال)",
        ]
    )
    return "\n".join(lines).strip()


def attach_outreach_drafts(payload: dict[str, Any]) -> dict[str, Any]:
    """Mutate war_room payload targets with outreach_draft_ar per item."""
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

    payload["outreach_policy_ar"] = "مسودات لمسة أولى فقط — لا إرسال LinkedIn/WhatsApp آلي."
    return payload
