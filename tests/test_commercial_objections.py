"""Objection registry matching for meeting briefs."""

from dealix.commercial_ops.objections import match_objections


def test_match_objections_crm_label():
    hits = match_objections("عندنا CRM و hubspot", limit=3)
    assert any(h.get("id") == "crm_exists" for h in hits)


def test_match_objections_price():
    hits = match_objections("السعر عالي جداً", limit=3)
    assert any(h.get("id") == "price_high" for h in hits)
