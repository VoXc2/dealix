"""Every proposal maps to the product catalog."""
from _util import decide, load_jsonl, valid_product_ids, DATA


def test_proposal_without_catalog_mapping_is_rejected():
    assert decide({"type": "proposal", "product_id": "mystery_product"}) == "reject"
    assert decide({"type": "proposal", "product_id": None}) == "reject"


def test_proposal_with_valid_product_is_allowed():
    a_valid_id = sorted(valid_product_ids())[0]
    assert decide({"type": "proposal", "product_id": a_valid_id}) == "allow"


def test_catalog_is_non_empty():
    assert len(valid_product_ids()) >= 4, "catalog should expose the known SKUs + ladder"


def test_committed_proposals_map_to_catalog():
    ids = valid_product_ids()
    proposals = load_jsonl(DATA / "proposals" / "proposals.jsonl")
    assert proposals, "expected seed proposals"
    for p in proposals:
        assert p.get("product_id") in ids, f"proposal {p.get('id')} not mapped to catalog"
        # No final price without founder approval
        pr = p.get("price_range_sar") or {}
        if pr.get("is_final"):
            assert p.get("founder_approved") is True, f"proposal {p.get('id')} final price without approval"


def test_proof_pack_pilot_maps_to_catalog():
    ids = valid_product_ids()
    for pp in load_jsonl(DATA / "proof_packs" / "proof_packs.jsonl"):
        assert pp.get("recommended_pilot_product_id") in ids
