from pathlib import Path


def test_public_doctrine_does_not_expose_commercial_secrets():
    forbidden_terms = [
        "anchor_partner_pipeline",
        "admin_key",
        "client_data",
        "private_pricing",
        "investor_confidential",
        "localStorage",
        "secret",
        "password",
        "token",
    ]
    files = list(Path("open-doctrine").glob("*.md"))
    assert files, "open-doctrine/ must contain at least one .md file"
    for path in files:
        text = path.read_text()
        for term in forbidden_terms:
            assert term not in text, f"forbidden term {term!r} found in {path}"
