from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROWTH = ROOT / "scripts/commercial/run_autonomous_growth_daily.py"
SELECTOR = ROOT / "scripts/commercial/run_probability_revenue_engine_v1.py"


def test_growth_remains_canonical_company_os_adapter():
    text = GROWTH.read_text(encoding="utf-8")
    assert "run_self_operating_company_os.py" in text
    assert "run_probability_revenue_engine_v1.py" in text
    assert "AUTONOMOUS_GROWTH=DELEGATED_TO_CANONICAL_COMPANY_OS_WITH_PROBABILITY_RANKING" in text


def test_probability_selector_is_read_only_and_truth_first():
    text = SELECTOR.read_text(encoding="utf-8")
    assert "UNKNOWN_NOT_EVIDENCE_BACKED" not in text or "unknown_probability_policy" in text
    assert "external_send_authority" in text
    assert "STOP_SUPPRESSED" in text
    assert "PROBABILITY_UNKNOWN_RESEARCH_ONLY" in text
    assert "deep_wip_candidate" in text


def test_growth_does_not_gain_send_or_material_mutation_primitives():
    text = GROWTH.read_text(encoding="utf-8")
    forbidden = [
        "requests.post(",
        "httpx.post(",
        "send_message(",
        "send_email(",
        "merge_pull_request",
        "railway up",
        "cloudflare",
        "alembic upgrade",
    ]
    for token in forbidden:
        assert token not in text
