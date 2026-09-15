from pathlib import Path


CONTENT_FACTORY = Path("scripts/launch/content_factory_dry_run.py")


def test_dry_run_does_not_reintroduce_unsupported_legacy_claims() -> None:
    text = CONTENT_FACTORY.read_text(encoding="utf-8")
    forbidden = (
        "60% من مشاريع العقارات",
        "4 من كل 10 فقط",
        "200,000 و 500,000 ريال",
        "80% من الصفقات تحتاج 5-8",
        "نتائج واضحة خلال 30 يوماً",
    )
    assert not any(claim in text for claim in forbidden)


def test_dry_run_preserves_truth_and_authority_boundaries() -> None:
    text = CONTENT_FACTORY.read_text(encoding="utf-8")
    assert "تشخيص مجاني" in text
    assert "بعد اكتشاف مؤهل فقط" in text
    assert "بلا وعود بنتائج أو مدة ثابتة" in text
    assert "مسودة داخلية فقط" in text
    assert "دليلاً على وجود علاقة أو موافقة" in text
