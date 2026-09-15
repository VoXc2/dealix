from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_root_commercial_entry_aliases_redirect_to_book() -> None:
    config = (ROOT / "apps/web/next.config.js").read_text(encoding="utf-8")
    for source in ("/diagnostic-sprint", "/intake"):
        rule = f'{{ source: "{source}", destination: "/book", permanent: true }}'
        assert rule in config
