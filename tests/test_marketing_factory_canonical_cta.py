from pathlib import Path

from dealix.marketing_factory.schemas import CalendarSlotRecord

ROOT = Path(__file__).resolve().parents[1]


def test_marketing_factory_defaults_to_canonical_free_diagnostic_cta() -> None:
    record = CalendarSlotRecord(id="cal_test", scheduled_date="2026-09-12", channel="linkedin", title_ar="test", body_draft_ar="test")
    assert record.cta_path == "/book"
    assert "المجاني" in record.cta_label_ar


def test_marketing_factory_seed_and_store_do_not_reintroduce_legacy_diagnostic_route() -> None:
    for relative in ("dealix/marketing_factory/store.py", "dealix/marketing_factory/content_calendar.seed.yaml"):
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "/dealix-diagnostic" not in text
        assert "/book" in text
