"""Marketing loop sovereign tests — draft-only, evidence-linked, no auto-publish."""
from __future__ import annotations

from dealix.company_os.marketing_loop import (
    draft_content,
    identify_content_gaps,
    prioritize_gaps,
    run_daily_marketing_loop,
)


def test_marketing_loop_identifies_gaps_all_sectors():
    gaps = identify_content_gaps()
    assert len(gaps) >= 6  # at least 6 sectors × 3 themes bounded
    for gap in gaps:
        assert gap.sector
        assert gap.theme
        assert gap.evidence_ref.startswith("sector:")
        assert gap.priority > 0


def test_marketing_loop_prioritizes_economically():
    gaps = identify_content_gaps()
    top3 = prioritize_gaps(gaps, top_n=3)
    assert len(top3) == 3
    # ZATCA/PDPL should be top (highest priority numbers)
    assert top3[0].priority >= top3[1].priority >= top3[2].priority
    assert any("zatca" in g.theme for g in top3)  # most urgent must be in top3


def test_marketing_loop_drafts_are_bilingual_and_evidence_linked():
    gaps = identify_content_gaps()
    draft = draft_content(gaps[0], tenant_id="dealix")
    assert draft.title_ar and draft.title_en
    assert draft.body_ar and draft.body_en
    assert draft.cta_ar and draft.cta_en
    assert draft.evidence_ids
    assert draft.approval_required is True
    assert draft.external_published is False
    assert draft.id.startswith("mkt-")


def test_marketing_loop_daily_cycle_is_safe_and_bounded():
    receipt = run_daily_marketing_loop(tenant_id="dealix", top_n=3)
    assert receipt["tenant_id"] == "dealix"
    assert len(receipt["gaps"]) == 3
    assert len(receipt["drafts"]) == 3
    assert len(receipt["distribution_prep"]) == 3
    # All drafts must require approval and not be auto-published
    for d in receipt["drafts"]:
        assert d["approval_required"] is True
        assert d["external_published"] is False
        assert d["evidence_ids"]
        assert d["title_ar"] and d["title_en"]
    # QA must pass
    assert receipt["qa"]["passed"] is True
    assert receipt["qa"]["failures"] == []
    assert receipt["verdict"] == "PASS"
    # Distribution is prep only, never published
    for prep in receipt["distribution_prep"]:
        assert prep["publish_status"] == "draft_ready_needs_approval"
        assert "utm_campaign" in prep
        assert "dealix_" in prep["utm_campaign"]


def test_marketing_loop_tenant_isolation():
    r1 = run_daily_marketing_loop(tenant_id="tenant_alpha", top_n=2)
    r2 = run_daily_marketing_loop(tenant_id="tenant_beta", top_n=2)
    # Different tenant → different draft ids (hash includes tenant)
    ids1 = {d["id"] for d in r1["drafts"]}
    ids2 = {d["id"] for d in r2["drafts"]}
    assert ids1.isdisjoint(ids2)
    assert r1["tenant_id"] == "tenant_alpha"
    assert r2["tenant_id"] == "tenant_beta"
