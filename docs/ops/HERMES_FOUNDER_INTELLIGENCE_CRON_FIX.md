# Hermes Founder Intelligence — Context Overflow Fix (2026-09-14)

## Failure

- Cron: `Dealix Founder Intelligence` (`34d8d39ce69f`, `0 8 * * *`, model `dealix-auto` via `http://127.0.0.1:11999/v1`)
- Error: `HTTP 502: {"error":{"code":400,"message":"request (14488 tokens) exceeds the available context size (8192 tokens), try increasing it","type":"exceed_context_size_error","n_prompt_tokens":14488,"n_ctx":8192}}` (`agent.log:4549`)
- Compression: `tokens=~14,517 model=dealix-auto` → `no_progress` → `Context length exceeded: 9,081 tokens. Cannot compress further.`

## Root cause

1. **Hard 8K bound is canonical** — `harden_dealix_local_ai_8k.sh` enforces `OLLAMA_CONTEXT_LENGTH=8192` + `DEALIX_LOCAL_NUM_CTX=8192` + `ollama rm dealix-qwen3-4b-64k` on a 16 Gi node (`MemoryMax=8G` for ollama, 512 M for router). Previous 64k/32k attempts were reverted (`20-context.conf.bak-20260911T001731-64k` → `8192`, `zzzz-dealix-context-32k.conf` → `8192`). Raising needs L5 + RAM proof.

2. **Packet was un-bounded** — `dealix_founder_evidence_packet.sh` emitted `head -c 12000`×3 + `head -c 12000`×2 + `head -c 16000`×4 + `cat` 6 receipts unbounded → `32082` chars live (`31766` in replay) → `~7941` tok. Plus Hermes overhead (SOUL `10339` + workdir `AGENTS.md` `587` + skills index ~`8000` + `file` tools ~`3600` + cron hint + skill body `2364` + router `SYSTEM_PREFIX`) = `14488` prompt tok → `>8192`. Single-message prompt cannot be compressed (`messages=1`).

3. **Config mismatch** — `~/.hermes/config.yaml` advertises `model.context_length: 64000` / `context_length_cache.yaml:64000` while the actual server caps at `8192`. Hermes threshold `54400` (85% of 64k) never fires before the `502` at `8192`. Even at `8192`, `CONTEXT_FILE_MAX_CHARS` floor `20000` keeps `AGENTS.md` at `20k` — no help.

Dominant field: `reports/probability_revenue_engine/2026-09-14.json` `15418` chars (`3855` tok, 48% of packet). Truncating it alone still leaves `>8192`.

## Fix — L0-L4 bounded (no restart)

Distill the packet to the seven required outputs (`TRUTH/MONEY/REAL_RELATIONSHIPS/TOP_OPPORTUNITY/APPROVAL_NEEDED/BEST_SAFE_L0-L4_ACTION/LEARNING`):

- `founder_os_truth`: `head -c 1800`×2 + `head -n 22` for `FOUNDER_DAILY_COMMAND.md` (was `12000`×3)
- `opportunity-summary` / `approval-queue`: `jq -c` distilled to 2 records (`1100`/`900` cap, was `12000`)
- `today_self_operating_company`: only `daily/$TODAY.md` first 30 lines (`+` no `approvals/proof` 16000×2); `probability_revenue_engine` top-3 distilled `1300` (was `15418` full)
- `latest_company_receipts`: dropped (was 6×`cat` unbounded; not decision-critical)
- Removed `production_api_meta` curl (1200–2000) — `LATEST_TRUTH` already carries freeze/economy

Result: `6044` chars `~1511` tok (was `32082` `~7941`) — `81%` reduction. EST prompt `~19800` chars `~4955` tok (base `13777` from `old 45543-31766` + `6044`) vs `8192` → margin `~3237` tok. Live packet at `/home/dealix/.hermes/scripts/dealix_founder_evidence_packet.sh` (backup `.bak-20260914-*`).

Verification: `python3 -c "len(open('/home/dealix/.hermes/scripts/dealix_founder_evidence_packet.sh').read())"` + replay `| wc -c` + `chars/4` vs `8192`.

## L5 — richer context (requires approval)

Increasing `n_ctx` restores detail but risks OOM on 15 Gi (`ollama 8G`, router 512 M; llama-server `-c 8192 -b 1024 --context-shift`). Passage requires founder action-bound approval (ACTION_HASH per `APPROVAL_FINGERPRINT_CONTRACT.md`) and RAM headroom proof.

Exact diff if approved for 16384 (conservative) or 32768:

```diff
# /etc/systemd/system/ollama.service.d/zzzzz-dealix-8k-guard.conf
-Environment="OLLAMA_CONTEXT_LENGTH=8192"
+Environment="OLLAMA_CONTEXT_LENGTH=16384"
# /etc/systemd/system/dealix-llm-router.service.d/zzzzz-dealix-local-ai-8k.conf
-Environment=DEALIX_LOCAL_NUM_CTX=8192
+Environment=DEALIX_LOCAL_NUM_CTX=16384
# /opt/dealix/ai-router/router.py (fallback default)
-    "8192",
+    "16384",
```

Then `systemctl daemon-reload && systemctl restart ollama && systemctl restart dealix-llm-router` and re-verify `systemctl show ollama --property=Environment` + `curl /api/ps` `context_length` + `curl /v1/chat/completions` 14k prompt returns 200. Update `scripts/ops/harden_dealix_local_ai_8k.sh` + `tests/test_local_ai_8k_hardener_contract.py` (currently assert `8192`) and `~/.hermes/config.yaml` `model.context_length: 16384` (and `context_length_cache.yaml`). Keep `OLLAMA_MAX_LOADED_MODELS=1 NUM_PARALLEL=1` and watch `free -h` (`available` stays `>4G`).

## Files

- Live: `/home/dealix/.hermes/scripts/dealix_founder_evidence_packet.sh` (now bounded)
- Canonical bounded template: `scripts/ops/dealix_founder_evidence_packet.distilled.sh` (this repo)
- Proof: `agent.log:4549` `502` + `12088`→`6044` `wc -c` + `ps` `context_length 8192`
