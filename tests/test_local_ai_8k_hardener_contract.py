from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HARDENER=ROOT/'scripts/ops/harden_dealix_local_ai_8k.sh'

def test_hardener_owns_final_ollama_and_router_overrides():
    text=HARDENER.read_text(encoding='utf-8')
    assert 'zzzzz-dealix-8k-guard.conf' in text
    assert 'zzzzz-dealix-local-ai-8k.conf' in text
    assert 'Environment=DEALIX_LOCAL_MODEL=$MODEL' in text
    assert 'Environment=DEALIX_LOCAL_NUM_CTX=8192' in text
    assert 'systemctl restart dealix-llm-router.service' in text
    assert 'OLLAMA_8K_GUARD=FAIL router_health' in text
    assert 'http://127.0.0.1:11999/healthz' in text

def test_hardener_keeps_cpu_node_bounded_and_warm():
    text=HARDENER.read_text(encoding='utf-8')
    assert 'OLLAMA_CONTEXT_LENGTH=8192' in text
    assert 'OLLAMA_MAX_LOADED_MODELS=1' in text
    assert 'OLLAMA_NUM_PARALLEL=1' in text
    assert 'OLLAMA_KEEP_ALIVE=15m' in text
    assert 'ollama rm "$LEGACY_MODEL"' in text
