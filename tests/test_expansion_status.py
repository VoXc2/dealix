"""Commercial expansion status + warm enrich."""

from __future__ import annotations

from dealix.commercial_ops.expansion_status import build_expansion_status
from scripts.enrich_targeting_warm import enrich_warm_notes


def test_build_expansion_status_shape():
    blob = build_expansion_status(abm_top_n=3)
    assert blob["targeting"]["pool_rows"] >= 0
    assert "social" in blob
    assert blob["next_actions_ar"]


def test_enrich_warm_dry_run():
    blob = enrich_warm_notes(limit=5, dry_run=True)
    assert blob["dry_run"] is True
    assert "warm_tags_added" in blob
