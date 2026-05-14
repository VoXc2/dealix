"""Wave 19 Recovery — GCC Expansion + Open Doctrine tests.

Enforce that the GCC expansion narrative preserves the Saudi-first
beachhead discipline, and that the open doctrine repository does not
leak commercial secrets.
"""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_gcc_expansion_preserves_saudi_beachhead():
    p = REPO_ROOT / "docs/gcc-expansion/GCC_EXPANSION_THESIS.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "Saudi-first commercially" in text
    assert "Saudi Arabia remains the commercial beachhead" in text
    assert "not launching broadly across the GCC before Invoice #1" in text


def test_gcc_country_priority_and_gtm_sequence_exist():
    priority = REPO_ROOT / "docs/gcc-expansion/GCC_COUNTRY_PRIORITY_MAP.md"
    gtm = REPO_ROOT / "docs/gcc-expansion/GCC_GO_TO_MARKET_SEQUENCE.md"
    assert priority.exists()
    assert gtm.exists()
    priority_text = priority.read_text(encoding="utf-8")
    gtm_text = gtm.read_text(encoding="utf-8")
    assert "Beachhead" in priority_text
    assert "Saudi Arabia" in priority_text
    assert "United Arab Emirates" in priority_text
    assert "Step 1" in gtm_text
    assert "anchor partner" in gtm_text.lower()


def test_open_doctrine_exists():
    readme = REPO_ROOT / "open-doctrine/README.md"
    eleven = REPO_ROOT / "open-doctrine/11_NON_NEGOTIABLES.md"
    mapping = REPO_ROOT / "open-doctrine/CONTROL_MAPPING.md"
    assert readme.exists()
    assert eleven.exists()
    assert mapping.exists()
    readme_text = readme.read_text(encoding="utf-8")
    eleven_text = eleven.read_text(encoding="utf-8")
    assert "Governed AI Operations Doctrine" in readme_text
    assert "Source Passport" in eleven_text
    assert "No Unsafe Growth" in eleven_text


def test_public_doctrine_does_not_expose_commercial_secrets():
    forbidden_terms = [
        "anchor_partner_pipeline",
        "admin_key",
        "client_data",
        "private_pricing",
        "investor_confidential",
        "localStorage",
        "password",
        "token",
    ]
    files = list((REPO_ROOT / "open-doctrine").glob("*.md"))
    assert files, "open-doctrine markdown files missing"
    for path in files:
        text = path.read_text(encoding="utf-8")
        for term in forbidden_terms:
            assert term not in text, f"{term} leaked into public doctrine {path.name}"
