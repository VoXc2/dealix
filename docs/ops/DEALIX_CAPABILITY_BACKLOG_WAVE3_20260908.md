# Dealix Capability Backlog — Wave 3

Date: 2026-09-08 Asia/Riyadh

This is a **backlog**, not an install manifest. It extends the Internet Harvest without changing the canonical ranks 51-100 registry. Admission still requires measured gap -> duplication check -> license/security/data boundary -> isolated benchmark -> receipt -> ADOPT/REJECT/DEFER.

`AUTO_INSTALL=false`
`ACTIVE_BENCHMARKS_MAX=1`
`L5_EXECUTED=NONE`

## Performance / release confidence

### Locust — PILOT_AFTER_CURRENT_MAIN_PARITY
Repository: `locustio/locust`
- Python-native HTTP/other-protocol load testing.
- Potential Dealix use: quantify API/diagnostic/webhook capacity before a customer pilot or traffic increase.
- Duplication guard: do not run until functional/current-main release parity is stable; performance of a stale release is not decision-useful.
- Benchmark: one isolated API fixture / staging-equivalent route with conservative RPS and no third-party target.
- Acceptance: catches a measurable throughput/latency bottleneck and yields a reproducible capacity receipt.

### k6 — DEFER_LICENSE_AND_DUPLICATION_REVIEW
Repository: `grafana/k6`
- Modern load testing, but current repository licensing is AGPL-3.0.
- Compare against Locust only if JavaScript scripting / protocol coverage creates a measured advantage.
- Do not embed or redistribute before license posture is reviewed.

## API contract confidence

### Pact — PILOT_WHEN_REAL_CONSUMER_PROVIDER_BOUNDARY_EXISTS
Repository family: `pact-foundation/*`
- Consumer-driven contract testing for provider/consumer interaction compatibility.
- Use when Dealix has a real API consumer/provider boundary whose releases change independently.
- Do not add a permanent contract broker/service before a measured multi-service coordination need exists.

### Schemathesis — CANDIDATE_FOR_OPENAPI_FUZZ_ACCEPTANCE
Repository: `schemathesis/schemathesis`
- Candidate property/fuzz testing for OpenAPI/GraphQL APIs.
- Benchmark only on Dealix-owned local/test endpoints.
- Must add unique failures beyond current pytest/Hurl/hypothesis/API acceptance before admission.

## Data quality / evidence trust

### Soda Core — PILOT_ISOLATED
Repository: `sodadata/soda-core`
- Data quality + data-contract verification using YAML contracts across Postgres/DuckDB and other data sources.
- Strong potential for Proof/Economic pipelines where schema validity alone is insufficient.
- Duplication guard: Pandera remains cheap dataframe/schema baseline; Soda is admitted only for cross-database data-contract checks with unique value.
- No Soda Cloud upload by default; local/open-source path first.

### Great Expectations — DEFER_DUPLICATE
Repository: `great-expectations/great_expectations`
- Strong data quality/docs/profile ecosystem, but overlaps Pandera + Soda candidate scope.
- Do not admit until a specific requirement cannot be met more simply by the current stack.

## Runtime / host security

### Falco — DEFER_UNTIL_RUNTIME_THREAT_GAP
Repository: `falcosecurity/falco`
- Cloud-native runtime threat detection.
- Dealix currently gets more value from reducing attack surface, patching, secret hygiene, container/SBOM evidence and provider logs.
- Pilot only if a measured Linux/container runtime detection requirement appears that current controls cannot satisfy.
- Do not create another always-on security platform by default.

### Wazuh — DEFER_COMPLEXITY
Repository: `wazuh/wazuh`
- Broad host/SIEM/XDR capability, but operational footprint is material for current Dealix scale.
- Consider only if customer/compliance evidence or multi-host security operations creates a concrete requirement.

## Secret management

### Infisical — DEFER_DUPLICATE_SECRET_AUTHORITY
Repository: `Infisical/infisical` (formerly public mirrors may vary)
- Full secret-management platform can centralize/inject credentials.
- Dealix already uses provider secret stores and has ONE secret/identity authority rule.
- Do not introduce a new persistent secret authority merely because the tool exists.
- Re-evaluate only if rotation/audit/injection across multiple runtimes becomes a measured gap.

### SOPS — PILOT_FOR_ENCRYPTED_REPO_CONFIG_ONLY
Repository: `getsops/sops`
- Encrypts YAML/JSON/ENV/INI/binary files using KMS/age/PGP.
- Candidate only for non-runtime encrypted configuration artifacts where provider secret stores do not fit.
- Never commit plaintext secrets; never use SOPS as a reason to move existing Production secrets into Git.

## Policy-as-code

### Open Policy Agent / Conftest — DEFER_MEASURED_POLICY_GAP
Repository: `open-policy-agent/opa`, `open-policy-agent/conftest`
- General-purpose declarative policy engine / structured-config policy tests.
- Dealix already has deterministic Constitution/Truth Firewall/ChannelEligibility contracts in application code.
- Admit only for infrastructure/config policy checks that are materially simpler and more maintainable in Rego than current verifiers.
- Must never become a second commercial/consent/approval authority.

## Arabic / hard-document fallback

### Surya OCR — PILOT_ONLY_IF_DOCLING/MINERU/PADDLE_GAP
Repository: `LPAI-Org/Surya`
- OCR/layout/reading-order/table detection supporting 90+ languages with Arabic examples.
- It overlaps the current Docling -> MinerU/PaddleOCR hard-document ladder.
- Benchmark only on a labeled hard Arabic tender/forms corpus after first-line parsers miss acceptance thresholds.
- Model/runtime dependencies and license must be reviewed before commercial admission.

## Document transformation

### Pandoc — DEFER_LICENSE_AND_EXISTING_ARTIFACT_PIPELINE
Repository: `jgm/pandoc`
- Universal markup/document conversion with extensive reader/writer support.
- GPL-2.0+ and overlap with current DOCX/PDF/Gamma/Canva pipelines mean no default adoption.
- Pilot only if a repeatable document conversion gap remains unsolved by existing artifact tooling.

## Default decision

None of the above is installed by this backlog. Current priority order remains:
1. current-main Production parity / front door;
2. Probability Revenue Engine + real Market->Cash learning;
3. one bounded capability benchmark at a time;
4. only then deeper runtime/security/performance infrastructure when evidence demands it.
