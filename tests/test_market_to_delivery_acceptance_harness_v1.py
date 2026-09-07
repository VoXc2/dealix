from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACCEPT = ROOT / "scripts/commercial/accept_market_to_delivery_v1.sh"
POSTGRES = ROOT / "scripts/commercial/run_market_to_delivery_postgres_acceptance_v1.sh"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_source_acceptance_anchors_repo_root_and_python_imports():
    text = _text(ACCEPT)
    assert 'cd "$ROOT"' in text
    assert 'export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"' in text
    assert '-t "$ROOT"' in text
    assert "test_market_to_delivery_http.py" in text


def test_postgres_acceptance_anchors_repo_root_and_python_imports():
    text = _text(POSTGRES)
    assert 'cd "$ROOT"' in text
    assert 'export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"' in text
    assert 'verify_market_to_delivery_postgres_v1.py' in text
    assert '127.0.0.1' in text
    assert 'production_db=false' in text


def test_harness_does_not_weaken_material_effect_guards():
    source_text = _text(ACCEPT)
    postgres_text = _text(POSTGRES)
    assert 'LIVE_EXECUTION=false' in source_text
    assert 'PRODUCTION_READY=UNPROVEN' in source_text
    assert 'external_send=false' in postgres_text
    assert 'payment=false' in postgres_text
