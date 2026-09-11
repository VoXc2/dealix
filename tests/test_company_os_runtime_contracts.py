from pathlib import Path

from core.llm.openai_compat import LOCAL_OLLAMA_TIMEOUT_SECONDS, OpenAIClient

ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_loopback_ollama_gets_bounded_cpu_timeout_only_by_default() -> None:
    local = OpenAIClient(
        api_key="ollama-local",
        model="qwen3:4b-instruct-2507-q4_K_M",
        base_url="http://127.0.0.1:11434/v1",
    )
    remote = OpenAIClient(api_key="test", model="test")
    explicit = OpenAIClient(
        api_key="ollama-local",
        model="test",
        base_url="http://127.0.0.1:11434/v1",
        timeout=45,
    )

    assert local.timeout == LOCAL_OLLAMA_TIMEOUT_SECONDS == 180
    assert remote.timeout == 60
    assert explicit.timeout == 45


def test_sales_arena_runner_isolates_independent_challenges() -> None:
    text = _read("scripts/commercial/run_sales_arena.py")
    assert "async def _run_isolated_arena" in text
    assert "for challenge in DEFAULT_CHALLENGES:" in text
    assert "run_sales_arena(router=router, challenges=(challenge,))" in text
    assert "external_actions_performed=0" in text


def test_issue_bridge_installer_pins_one_canonical_source_and_preserves_state() -> None:
    text = _read("scripts/ops/install_dealix_vps_issue_bridge.sh")
    assert 'SOURCE_REF="${DEALIX_SOURCE_REF:-main}"' in text
    assert "ops/dealix-vps-self-hosted-control-20260820" not in text
    assert "?ref=${SOURCE_SHA}" in text
    assert text.count("?ref=${SOURCE_SHA}") == 2
    assert 'STATE_FILE="${STATE_DIR}/issue_bridge.json"' in text
    assert 'STATE_ACTION="preserved"' in text
    assert 'STATE_ACTION="bootstrapped"' in text
    assert 'Environment="OPENAI_BASE_URL=http://127.0.0.1:11434/v1"' in text
    assert 'Environment="OPENAI_API_KEY=ollama-local"' in text
    assert "secret_values_printed=false" in text
