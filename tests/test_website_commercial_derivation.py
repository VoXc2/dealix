from dealix.commercial.economic_cell import Sector
from dealix.commercial.website_commercial_derivation import WebsiteCommercialDerivation


def test_every_sector_has_arabic_and_english_projection() -> None:
    pages = WebsiteCommercialDerivation().all_sector_pages()

    assert len(pages) == len(Sector) * 2 == 40
    assert len({(page.sector_id, page.locale) for page in pages}) == 40
    assert all(page.brand == "Dealix" for page in pages)
    assert all(page.page_kind == "DEALIX_SECTOR_APPLICATION" for page in pages)


def test_every_sector_page_uses_same_free_diagnostic_and_no_fake_proof() -> None:
    pages = WebsiteCommercialDerivation().all_sector_pages()

    assert all(page.diagnostic_price == "FREE" for page in pages)
    assert all(page.free_diagnostic_cta for page in pages)
    assert all(page.proof_claims == [] for page in pages)
    assert all(page.publish_authority is False for page in pages)


def test_content_queue_is_source_backed_draft_only() -> None:
    queue = WebsiteCommercialDerivation().content_queue_projection()

    assert queue
    assert {item["sector_id"] for item in queue} == {sector.value for sector in Sector}
    assert all(item["source_refs"] for item in queue)
    assert all(item["truth_status"] == "DRAFT_REQUIRES_SOURCE_VALIDATION" for item in queue)
    assert all(item["publish_authority"] is False for item in queue)
