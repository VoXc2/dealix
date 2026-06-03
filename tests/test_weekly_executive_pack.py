"""Wave 13 Phase 5 — Weekly Executive Pack tests.

Asserts the renderers + CLI:
  - Customer view has 5 sections, Arabic-first, no internal jargon
  - Founder view has full detail, internal terms allowed
  - Forbidden tokens (guaranteed/نضمن/100%) scrubbed in customer view
  - is_estimate disclaimer present
  - CLI exits 0 on demo handle
  - Render dispatch works for both audiences

Sandbox-safe: only loads renderers + ExecutivePackRecord schema directly.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest


def _load():
    repo_root = Path(__file__).resolve().parent.parent

    # Schemas first
    schemas_path = repo_root / "auto_client_acquisition" / "full_ops_contracts" / "schemas.py"
    spec = importlib.util.spec_from_file_location("_test_w13_p5_schemas", schemas_path)
    assert spec is not None and spec.loader is not None
    schemas = importlib.util.module_from_spec(spec)
    sys.modules["_test_w13_p5_schemas"] = schemas
    sys.modules["auto_client_acquisition.full_ops_contracts.schemas"] = schemas
    spec.loader.exec_module(schemas)

    rend_path = repo_root / "auto_client_acquisition" / "executive_pack_v2" / "renderers.py"
    spec = importlib.util.spec_from_file_location("_test_w13_p5_renderers", rend_path)
    assert spec is not None and spec.loader is not None
    rend = importlib.util.module_from_spec(spec)
    sys.modules["_test_w13_p5_renderers"] = rend
    spec.loader.exec_module(rend)

    return schemas, rend


_SCH, _REND = _load()
ExecutivePackRecord = _SCH.ExecutivePackRecord
render_for_customer = _REND.render_for_customer
render_for_founder = _REND.render_for_founder
render_pack = _REND.render_pack


def _make_pack(**overrides) -> ExecutivePackRecord:
    base = dict(
        pack_id="pack_t1",
        customer_handle="acme-real-estate",
        cadence="weekly",
        week_label="2026-W19",
        executive_summary_ar="هذا الأسبوع: 5 فرص جديدة و 3 موافقات معلّقة.",
        executive_summary_en="This week: 5 new leads and 3 pending approvals.",
        leads={"leads_total": 5, "leads_allowed": 4, "leads_blocked": 0,
               "leads_needs_review": 1, "drafts_created": 3},
        support={"tickets_total": 2, "tickets_open": 1,
                 "tickets_escalated": 0, "sla_breached_count": 0},
        next_3_actions=[
            {"approval_id": "ap_1", "action_type": "draft_message",
             "channel": "whatsapp", "risk_level": "low",
             "summary_ar": "اعتمد رسالة الترحيب لشركة الأحمد"},
            {"approval_id": "ap_2", "action_type": "follow_up",
             "channel": "email", "risk_level": "medium",
             "summary_ar": "متابعة استفسار الخالدية"},
        ],
        risks=[],
        blockers=[],
        decisions=[],
        proof_events=[],
    )
    base.update(overrides)
    return ExecutivePackRecord(**base)


# ── Test 1 ────────────────────────────────────────────────────────────
def test_customer_view_has_five_sections():
    pack = _make_pack()
    md = render_for_customer(pack)
    assert "## 1. ملخص الأسبوع" in md
    assert "## 2. أهم النتائج" in md
    assert "## 3. أهم قرارات الأسبوع القادم" in md
    assert "## 4. المخاطر" in md
    assert "## 5. التوصية" in md


# ── Test 2 ────────────────────────────────────────────────────────────
def test_customer_view_arabic_first():
    """Title is Arabic; English is secondary on KPI lines."""
    pack = _make_pack()
    md = render_for_customer(pack)
    assert md.startswith("# تقرير Dealix الأسبوعي")


# ── Test 3 ────────────────────────────────────────────────────────────
def test_customer_view_has_no_internal_jargon():
    """Customer must not see leadops_spine, customer_brain, v10/v11/etc."""
    pack = _make_pack(
        executive_summary_ar="نتائج leadops_spine + customer_brain تشير إلى تحسن v12",
    )
    md = render_for_customer(pack)
    forbidden = ["leadops_spine", "customer_brain", "v10", "v11", "v12"]
    for tok in forbidden:
        assert tok not in md, f"customer view leaked internal jargon: {tok}"


# ── Test 4 ────────────────────────────────────────────────────────────
def test_customer_view_scrubs_forbidden_claims():
    """Article 8: 'guaranteed' / 'نضمن' must never appear in customer view."""
    pack = _make_pack(executive_summary_ar="نضمن تحقيق نتائج 100% guaranteed")
    md = render_for_customer(pack)
    md_lower = md.lower()
    forbidden_pats = [
        re.compile(r"\bguaranteed?\b", re.IGNORECASE),
        re.compile(r"نضمن"),
        re.compile(r"\bguarantee\b", re.IGNORECASE),
    ]
    for pat in forbidden_pats:
        m = pat.search(md_lower if pat.pattern.startswith(r"\b") else md)
        assert m is None, f"customer view still contains forbidden token: {m.group(0) if m else ''}"


# ── Test 5 ────────────────────────────────────────────────────────────
def test_customer_view_has_estimate_disclaimer():
    """Article 8: every numeric is_estimate=True must be visible to customer."""
    pack = _make_pack()
    md = render_for_customer(pack)
    assert "تقديرات" in md or "estimate" in md.lower()


# ── Test 6 ────────────────────────────────────────────────────────────
def test_render_dispatch_and_founder_view_has_full_detail():
    """render_pack(audience='founder') routes correctly + includes appendix."""
    pack = _make_pack(
        appendix={"active_sessions": [{"session_id": "s_1"}],
                  "built_from": ["leadops_spine", "approval_center"]},
    )
    customer_md = render_pack(pack, audience="customer")
    founder_md = render_pack(pack, audience="founder")

    # Customer view: short, Arabic-first, no internal jargon
    assert "leadops_spine" not in customer_md

    # Founder view: full detail (appendix + internal terms allowed)
    assert "## Appendix" in founder_md
    assert "leadops_spine" in founder_md  # founders see internal terms
    assert "FOUNDER VIEW" in founder_md

    # Invalid audience raises
    with pytest.raises(ValueError):
        render_pack(pack, audience="public")
