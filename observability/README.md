# Observability

Operational visibility across workflows and agents:

- traces and spans
- failure and retry visibility
- policy violation telemetry
- incident tracking hooks

## Omega5 execution contract (extends, does not replace)

Canonical in-process contract: `auto_client_acquisition/observability_v10`
(`TraceRecordV10` + `record_v10_trace` + `contract_trace_hook`), surfaced at
`GET/POST /api/v1/observability-v10/*` and the `agent-observability` shim at
`/api/v1/agent-observability/*`. One buffer, one redaction path — no second
stack.

Every execution record carries (all optional except trace/correlation identity,
backward compatible): `trace_id`, `case_id`/`job_id`, `owner`/`agent_id`
(logical agent), `effect_class`/`authority`, `model_name` +
`model_provider_class` (class only, never secrets), `tool_name`/`action_name`,
`verifier`, `result`, `latency_ms`/`cost_known_state`/`estimated_cost_usd`,
`evidence_refs`, `release_sha`. Semantic fields are OpenTelemetry-compatible.

Redaction is mandatory and fail-closed: `redacted_payload` never stores raw
prompts, tool args/results, PII, or secrets. Denied keys coerce to `HOLD`
(`trace_schema.coerce_denied_payload_keys`, re-applied in `buffer.py`);
unknown sensitivity => omit/HOLD.

Deterministic receipt schema: `schemas/execution_receipt.schema.json`
(machine-checkable, no payloads).

## Optional exporters (all disabled by default, no services deployed)

- OTEL: `observability_adapters/otel_adapter.py` — active only when
  `OTEL_EXPORTER_OTLP_ENDPOINT` is set; contract-hook span export additionally
  gated by `OTEL_CONTRACT_TRACE_EXPORT=1` (`core/config/settings.py`).
- Langfuse: `observability_adapters/langfuse_adapter.py` — active only when
  `LANGFUSE_SECRET_KEY` + `LANGFUSE_PUBLIC_KEY` are set; metadata filtered
  for sensitive keys, never raw prompts/responses.
- OpenObserve: `observability_adapters/openobserve_adapter.py` — active only
  when `OPENOBSERVE_ENABLED=1` + `OPENOBSERVE_URL`/`ORG`/`STREAM`/`TOKEN` are
  set; payload pre-scrubbed via `RedactionFilter`.
- Local optional profile: `docker-compose.observability.yml`
  (`--profile observability` only) + `ops/observability/otelcol.config.yaml`
  (logging exporter only). Default `docker compose up` starts nothing new.

## Supply-chain evidence (fail-closed, presence-aware)

Isolated-lab contract: `config/oss/supply_chain_lab_v1.json` (verified by
`scripts/ops/verify_supply_chain_lab_v1.py`); evidence runner
`scripts/ops/run_supply_chain_evidence_v1.sh` uses lab binaries only.
Policy: `docs/ops/SBOM_AND_SUPPLY_CHAIN_POLICY.md`; CI surfaces:
`.github/workflows/docker-build.yml` (Trivy + SBOM, non-PR),
`repository-hardening.yml` (Trivy), `.trivyignore.yaml`; local SBOM:
`scripts/generate_sbom.py` (evidence only, CycloneDX).

Presence-aware gate (no installs, no sign/push):
`scripts/ops/verify_supply_chain_gates_v1.py` reports per-tool
`AVAILABLE | NOT_AVAILABLE | HOLD` for `osv-scanner`, `trivy`, `syft`,
`cosign` (+ SBOM artifact + manifest/policy presence). Missing scanners =>
`HOLD`, never `PASS`. Cosign counts only with explicit
`COSIGN_IDENTITY` + (`COSIGN_DIGEST` or `COSIGN_DIGEST_FILE`) evidence.
Exit `0` = PASS, `2` = HOLD (block promotion), `1` = script error.
