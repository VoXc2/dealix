"""V12 Phase 5 — Knowledge base presence + content tests."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
KB_DIR = REPO_ROOT / "docs" / "knowledge-base"


_REQUIRED_FILES = (
    "support_faq_ar.md",
    "support_faq_en.md",
    "pricing_policy_ar_en.md",
    "payment_policy_ar_en.md",
    "privacy_pdpl_ar_en.md",
    "service_delivery_ar_en.md",
    "escalation_policy_ar_en.md",
)


def test_all_7_kb_files_exist() -> None:
    for name in _REQUIRED_FILES:
        path = KB_DIR / name
        assert path.exists(), f"missing knowledge-base file: {name}"


def test_each_kb_file_has_substantive_content() -> None:
    for name in _REQUIRED_FILES:
        path = KB_DIR / name
        content = path.read_text(encoding="utf-8")
        assert len(content) >= 500, f"{name} too short: {len(content)} chars"


def test_kb_files_are_bilingual_or_clearly_labeled() -> None:
    """Each KB file is either Arabic-only, English-only, or bilingual.
    Files with `_ar_en` in the name MUST contain both Arabic and
    English content. AR-only / EN-only files explicitly don't need
    to mix.
    """
    arabic_chars = "ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي".split()
    for name in _REQUIRED_FILES:
        content = (KB_DIR / name).read_text(encoding="utf-8")
        if name.endswith("_ar_en.md"):
            assert any(ch in content for ch in arabic_chars), (
                f"{name} marked _ar_en but has no Arabic content"
            )
            assert any(c.isalpha() and c.isascii() for c in content), (
                f"{name} marked _ar_en but has no English content"
            )


def test_escalation_policy_lists_all_mandatory_categories() -> None:
    text = (KB_DIR / "escalation_policy_ar_en.md").read_text(encoding="utf-8")
    required = [
        "payment", "refund", "privacy_pdpl", "angry_customer",
        "security_incident", "system_outage",
        "customer_asks_for_guarantee", "customer_asks_for_cold_whatsapp",
    ]
    for cat in required:
        assert cat in text, f"escalation policy missing category: {cat}"


def test_no_promotional_claims_in_kb() -> None:
    """KB files actively REJECT guaranteed-revenue claims, so phrases
    like "no guarantee" / "don't guarantee" are expected. We block
    only **promotional** assertions: a claim that Dealix DOES
    guarantee something. The Arabic 'نضمن لكم' is a promotional form
    that must NEVER appear; English needs context-sensitive detection.
    """
    forbidden_arabic = ("نضمن لكم",)
    forbidden_english_promo = (
        "we guarantee ",
        "we will guarantee",
        "guaranteed roi for you",
        "guaranteed leads to you",
        "blast to all",
        "we'll scrape",
        "will scrape every",
    )
    for name in _REQUIRED_FILES:
        original = (KB_DIR / name).read_text(encoding="utf-8")
        for p in forbidden_arabic:
            assert p not in original, f"{name} contains forbidden Arabic: {p}"
        lower = original.lower()
        for p in forbidden_english_promo:
            assert p not in lower, f"{name} contains promotional claim: {p}"
