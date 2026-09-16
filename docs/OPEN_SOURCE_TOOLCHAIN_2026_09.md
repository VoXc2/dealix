# Dealix Open-Source Capability Radar — 2026-09-16

## Executive decision

Dealix gains leverage from open-source software without creating a second Company Machine. Default order: **reuse → install CLI/library → isolated trial → adopt only after evidence**. Heavy services stay off by default; production mutation remains a separate governed action.

- Live GitHub repositories reviewed: **122**
- Strict OSS / OSI-compatible or manually verified OSS: **116**
- Open-core mixed repositories: **4**
- Source-available non-OSI exceptions: **2**
- Unresolved license reviews: **0**
- Archived repositories retained in current radar: **0**

## Founder / CEO rules

1. Production Trust and verified economic movement outrank adding infrastructure.
2. No second CRM, scheduler, model gateway, vector DB, observability authority, or agent fleet without a measured gap.
3. Prefer OSS CLI/library leverage before always-on services.
4. Canonical defaults: PostgreSQL+pgvector over Qdrant; current model router over LiteLLM; OpenTelemetry+Langfuse over Phoenix/Opik; Company scheduler over Temporal; HubSpot mirror over Twenty; Playwright over browser-agent abstractions.
5. `n8n` is an existing license exception, not strict OSS. Do not embed/resell/client-host it without license review; Node-RED is the Apache-2.0 escape hatch to assess.
6. HashiCorp Vault is BSL and MongoDB server is SSPL; strict-OSS candidates are OpenBao and PostgreSQL/JSONB. Valkey is the BSD Redis-compatible candidate.
7. New installs must not start services, expose ports, deploy, mutate DNS/DB/secrets, send/publish, or alter production authority.

## Reproducible server toolchain

- `mise` 2026.9.9: **48** checksum-locked Linux x64 CLI tools in `tooling/oss/mise.toml` + `mise.lock`.
- `uv tool`: **8** isolated Python CLIs in `tooling/oss/uv-tools.txt`.
- Existing runtime reused: Docker, Git/GitHub CLI, Python, Node, OpenCode, Ollama, cloudflared, Tailscale, PostgreSQL/pgvector, Caddy, n8n, etc.
- Bootstrap: `scripts/bootstrap_open_source_toolchain.sh`.
- Verification: `scripts/verify_open_source_toolchain.py --check-installed`.

## Priority next actions

1. **P0 Production Trust:** exact-current canary → backup/restore/rollback proof → accepted exact-SHA release → public Web/API SHA parity.
2. **P0 Disk:** preserve rollback assets, but avoid heavy services while `/` is near 90% utilization.
3. **P1 Supply chain:** Gitleaks + Semgrep + OSV-Scanner + Trivy + Syft + Cosign; Grype/TruffleHog as independent cross-checks.
4. **P1 API trust:** Hurl + Schemathesis on isolated canaries; k6/oha only against bounded test endpoints.
5. **P1 Agent eval/red-team:** Promptfoo / Inspect AI / Garak / PyRIT as test lanes only.
6. **P1 Revenue:** Market Radar → Free Diagnostic/content/drafts; research never becomes relationship/consent automatically.
7. **P2 Authorization:** OPA/OpenFGA only around concrete tenant/room gaps.
8. **P2 License escape paths:** Node-RED for workflow, OpenBao for secrets, Valkey for cache/queue.
9. **P2 Document intelligence:** MarkItDown first; Docling only if heavier parsing quality is justified.
10. **P3 Heavy stacks:** Grafana/Loki/Tempo/Prometheus, Keycloak, dbt, Great Expectations, OpenLineage remain on-demand.

## Current authority notes

- AutoGen is maintenance-mode; Microsoft Agent Framework is the current successor candidate, but Dealix Company Machine remains authority.
- Active PyRIT repository is `microsoft/PyRIT`; old `Azure/PyRIT` is archived.
- Grafana Alloy is the modern collector candidate; do not add Promtail.
- Phoenix is Elastic License 2.0 and remains HOLD; existing Langfuse/OTel is preferred.

## Full reviewed registry

| # | Project | Category | Decision | Install | License class | License | Stars |
|---:|---|---|---|---|---|---|---:|
| 1 | [Docker Engine](https://github.com/moby/moby) | runtime | ADOPT | existing | OSI_SPDX | Apache-2.0 | 72101 |
| 2 | [Git](https://github.com/git/git) | sdlc | ADOPT | existing | MANUAL_OSS | GPL-2.0-only | 63175 |
| 3 | [GitHub CLI](https://github.com/cli/cli) | sdlc | ADOPT | existing | OSI_SPDX | MIT | 46290 |
| 4 | [Python](https://github.com/python/cpython) | runtime | ADOPT | existing | MANUAL_OSS | PSF-2.0 | 77187 |
| 5 | [Node.js](https://github.com/nodejs/node) | runtime | ADOPT | existing | MANUAL_OSS | MIT | 121967 |
| 6 | [npm](https://github.com/npm/cli) | sdlc | ADOPT | existing | MANUAL_OSS | Artistic-2.0 | 10117 |
| 7 | [uv](https://github.com/astral-sh/uv) | python_tooling | ADOPT | mise | OSI_SPDX | Apache-2.0 | 89862 |
| 8 | [OpenCode](https://github.com/anomalyco/opencode) | coding_agents | ADOPT | existing | OSI_SPDX | MIT | 207721 |
| 9 | [Ollama](https://github.com/ollama/ollama) | local_ai | ADOPT | existing | OSI_SPDX | MIT | 181101 |
| 10 | [n8n](https://github.com/n8n-io/n8n) | automation | EXISTING_LICENSE_EXCEPTION | existing | SOURCE_AVAILABLE_NON_OSI | Sustainable Use License 1.0 | 204473 |
| 11 | [cloudflared](https://github.com/cloudflare/cloudflared) | edge | ADOPT | existing | OSI_SPDX | Apache-2.0 | 15627 |
| 12 | [Tailscale](https://github.com/tailscale/tailscale) | networking | ADOPT | existing | OSI_SPDX | BSD-3-Clause | 36521 |
| 13 | [PostgreSQL](https://github.com/postgres/postgres) | data | ADOPT | existing | MANUAL_OSS | PostgreSQL | 22115 |
| 14 | [pgvector](https://github.com/pgvector/pgvector) | data | ADOPT | existing | MANUAL_OSS | PostgreSQL | 23023 |
| 15 | [Caddy](https://github.com/caddyserver/caddy) | edge | ADOPT | existing | OSI_SPDX | Apache-2.0 | 75771 |
| 16 | [Sentry Python SDK](https://github.com/getsentry/sentry-python) | observability | ADOPT | existing | OSI_SPDX | MIT | 2203 |
| 17 | [OpenTelemetry Python](https://github.com/open-telemetry/opentelemetry-python) | observability | ADOPT | existing | OSI_SPDX | Apache-2.0 | 2633 |
| 18 | [Langfuse](https://github.com/langfuse/langfuse) | llm_observability | ADOPT | existing | OPEN_CORE_MIXED | MIT core + enterprise directories | 34668 |
| 19 | [PostHog](https://github.com/PostHog/posthog) | product_analytics | ADOPT | existing | OPEN_CORE_MIXED | MIT core + enterprise directory | 39814 |
| 20 | [Playwright](https://github.com/microsoft/playwright) | browser_testing | ADOPT | existing | OSI_SPDX | Apache-2.0 | 96197 |
| 21 | [Redis](https://github.com/redis/redis) | data | ADOPT | existing | MIXED_WITH_OSI_AGPL_OPTION | AGPL-3.0 OR RSALv2 OR SSPLv1 (Redis 8+) | 76375 |
| 22 | [FastAPI](https://github.com/fastapi/fastapi) | api | ADOPT | existing | OSI_SPDX | MIT | 102355 |
| 23 | [Pydantic](https://github.com/pydantic/pydantic) | contracts | ADOPT | existing | OSI_SPDX | MIT | 28778 |
| 24 | [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) | data | ADOPT | existing | OSI_SPDX | MIT | 12158 |
| 25 | [Alembic](https://github.com/sqlalchemy/alembic) | data | ADOPT | existing | OSI_SPDX | MIT | 4397 |
| 26 | [pytest](https://github.com/pytest-dev/pytest) | testing | ADOPT | existing | OSI_SPDX | MIT | 14505 |
| 27 | [Ruff](https://github.com/astral-sh/ruff) | sdlc | ADOPT | mise | OSI_SPDX | MIT | 49645 |
| 28 | [Black](https://github.com/psf/black) | sdlc | ADOPT | mise | OSI_SPDX | MIT | 41843 |
| 29 | [mypy](https://github.com/python/mypy) | sdlc | ADOPT | existing | MANUAL_OSS | MIT | 20641 |
| 30 | [pre-commit](https://github.com/pre-commit/pre-commit) | sdlc | ADOPT | mise | OSI_SPDX | MIT | 15574 |
| 31 | [detect-secrets](https://github.com/Yelp/detect-secrets) | security | ADOPT | existing | OSI_SPDX | Apache-2.0 | 4635 |
| 32 | [Bandit](https://github.com/PyCQA/bandit) | security | ADOPT | existing | OSI_SPDX | Apache-2.0 | 8264 |
| 33 | [mise](https://github.com/jdx/mise) | toolchain | ADOPT | existing | OSI_SPDX | MIT | 33966 |
| 34 | [actionlint](https://github.com/rhysd/actionlint) | sdlc | ADOPT | mise | OSI_SPDX | MIT | 4226 |
| 35 | [age](https://github.com/FiloSottile/age) | security | ADOPT | mise | OSI_SPDX | BSD-3-Clause | 23593 |
| 36 | [bat](https://github.com/sharkdp/bat) | developer_ux | TRIAL | mise | OSI_SPDX | Apache-2.0 | 60466 |
| 37 | [bottom](https://github.com/ClementTsang/bottom) | server_ops | TRIAL | mise | OSI_SPDX | MIT | 14024 |
| 38 | [Checkov](https://github.com/bridgecrewio/checkov) | security | TRIAL | mise | OSI_SPDX | Apache-2.0 | 9002 |
| 39 | [Conftest](https://github.com/open-policy-agent/conftest) | policy | ADOPT | mise | MANUAL_OSS | Apache-2.0 | 3261 |
| 40 | [Cosign](https://github.com/sigstore/cosign) | supply_chain | ADOPT | mise | OSI_SPDX | Apache-2.0 | 6304 |
| 41 | [CycloneDX CLI](https://github.com/CycloneDX/cyclonedx-cli) | supply_chain | TRIAL | mise | OSI_SPDX | Apache-2.0 | 542 |
| 42 | [git-delta](https://github.com/dandavison/delta) | developer_ux | TRIAL | mise | OSI_SPDX | MIT | 32197 |
| 43 | [direnv](https://github.com/direnv/direnv) | developer_ux | TRIAL | mise | OSI_SPDX | MIT | 15447 |
| 44 | [DuckDB](https://github.com/duckdb/duckdb) | analytics | ADOPT | mise | OSI_SPDX | MIT | 41293 |
| 45 | [duf](https://github.com/muesli/duf) | server_ops | ADOPT | mise | MANUAL_OSS | MIT | 15300 |
| 46 | [dust](https://github.com/bootandy/dust) | server_ops | ADOPT | mise | OSI_SPDX | Apache-2.0 | 12266 |
| 47 | [eza](https://github.com/eza-community/eza) | developer_ux | TRIAL | mise | OSI_SPDX | EUPL-1.2 | 23287 |
| 48 | [fd](https://github.com/sharkdp/fd) | sdlc | ADOPT | mise | OSI_SPDX | Apache-2.0 | 44429 |
| 49 | [fzf](https://github.com/junegunn/fzf) | developer_ux | TRIAL | mise | OSI_SPDX | MIT | 82999 |
| 50 | [Gitleaks](https://github.com/gitleaks/gitleaks) | security | ADOPT | mise | OSI_SPDX | MIT | 29337 |
| 51 | [Grype](https://github.com/anchore/grype) | security | TRIAL | mise | OSI_SPDX | Apache-2.0 | 12890 |
| 52 | [Hadolint](https://github.com/hadolint/hadolint) | sdlc | ADOPT | mise | OSI_SPDX | GPL-3.0 | 12408 |
| 53 | [Hurl](https://github.com/Orange-OpenSource/hurl) | testing | ADOPT | mise | OSI_SPDX | Apache-2.0 | 19195 |
| 54 | [Hyperfine](https://github.com/sharkdp/hyperfine) | performance | TRIAL | mise | OSI_SPDX | Apache-2.0 | 28869 |
| 55 | [just](https://github.com/casey/just) | task_runner | ADOPT | mise | OSI_SPDX | CC0-1.0 | 35808 |
| 56 | [jq](https://github.com/jqlang/jq) | sdlc | ADOPT | mise | MANUAL_OSS | MIT | 35608 |
| 57 | [k6](https://github.com/grafana/k6) | performance | ADOPT | mise | OSI_SPDX | AGPL-3.0 | 31497 |
| 58 | [Lychee](https://github.com/lycheeverse/lychee) | web_quality | ADOPT | mise | OSI_SPDX | Apache-2.0 | 3917 |
| 59 | [oha](https://github.com/hatoo/oha) | performance | TRIAL | mise | OSI_SPDX | MIT | 10547 |
| 60 | [OSV-Scanner](https://github.com/google/osv-scanner) | security | ADOPT | mise | OSI_SPDX | Apache-2.0 | 11034 |
| 61 | [rclone](https://github.com/rclone/rclone) | backup | ADOPT | mise | OSI_SPDX | MIT | 59775 |
| 62 | [restic](https://github.com/restic/restic) | backup | ADOPT | mise | OSI_SPDX | BSD-2-Clause | 36066 |
| 63 | [ripgrep](https://github.com/BurntSushi/ripgrep) | sdlc | ADOPT | mise | OSI_SPDX | Unlicense | 68303 |
| 64 | [Semgrep CE](https://github.com/semgrep/semgrep) | security | ADOPT | uv-tool | OSI_SPDX | LGPL-2.1 | 16658 |
| 65 | [ShellCheck](https://github.com/koalaman/shellcheck) | sdlc | ADOPT | mise | OSI_SPDX | GPL-3.0 | 40041 |
| 66 | [shfmt](https://github.com/mvdan/sh) | sdlc | ADOPT | mise | OSI_SPDX | BSD-3-Clause | 9059 |
| 67 | [SOPS](https://github.com/getsops/sops) | security | ADOPT | mise | OSI_SPDX | MPL-2.0 | 23136 |
| 68 | [Syft](https://github.com/anchore/syft) | supply_chain | ADOPT | mise | OSI_SPDX | Apache-2.0 | 9567 |
| 69 | [Taplo](https://github.com/tamasfe/taplo) | sdlc | ADOPT | mise | OSI_SPDX | MIT | 2391 |
| 70 | [Task](https://github.com/go-task/task) | task_runner | ASSESS | mise | OSI_SPDX | MIT | 16148 |
| 71 | [tokei](https://github.com/XAMPPRocky/tokei) | developer_metrics | ASSESS | on-demand | MANUAL_OSS | Apache-2.0 OR MIT | 14910 |
| 72 | [Trivy](https://github.com/aquasecurity/trivy) | security | ADOPT | mise | OSI_SPDX | Apache-2.0 | 37934 |
| 73 | [TruffleHog](https://github.com/trufflesecurity/trufflehog) | security | TRIAL | mise | OSI_SPDX | AGPL-3.0 | 27943 |
| 74 | [Vale](https://github.com/vale-cli/vale) | content_quality | TRIAL | mise | OSI_SPDX | MIT | 6109 |
| 75 | [watchexec](https://github.com/watchexec/watchexec) | developer_ux | TRIAL | mise | OSI_SPDX | Apache-2.0 | 7187 |
| 76 | [xh](https://github.com/ducaale/xh) | api_dev | TRIAL | mise | OSI_SPDX | MIT | 8075 |
| 77 | [yamllint](https://github.com/adrienverge/yamllint) | sdlc | ADOPT | uv-tool | OSI_SPDX | GPL-3.0 | 3460 |
| 78 | [yq](https://github.com/mikefarah/yq) | sdlc | ADOPT | mise | OSI_SPDX | MIT | 15964 |
| 79 | [zizmor](https://github.com/zizmorcore/zizmor) | security | ADOPT | mise | OSI_SPDX | MIT | 6518 |
| 80 | [zoxide](https://github.com/ajeetdsouza/zoxide) | developer_ux | TRIAL | mise | OSI_SPDX | MIT | 39491 |
| 81 | [Schemathesis](https://github.com/schemathesis/schemathesis) | api_testing | TRIAL | uv-tool | OSI_SPDX | MIT | 3601 |
| 82 | [MCP Python SDK v2](https://github.com/modelcontextprotocol/python-sdk) | agent_protocol | TRIAL | uv-tool | OSI_SPDX | MIT | 24307 |
| 83 | [PydanticAI](https://github.com/pydantic/pydantic-ai) | agent_framework | TRIAL | uvx | OSI_SPDX | MIT | 19972 |
| 84 | [LangGraph](https://github.com/langchain-ai/langgraph) | agent_framework | ASSESS | uvx | OSI_SPDX | MIT | 41727 |
| 85 | [DSPy](https://github.com/stanfordnlp/dspy) | llm_optimization | ASSESS | uvx | OSI_SPDX | MIT | 38054 |
| 86 | [LiteLLM](https://github.com/BerriAI/litellm) | llm_gateway | HOLD | none | OPEN_CORE_MIXED | MIT core + enterprise directory | 58840 |
| 87 | [promptfoo](https://github.com/promptfoo/promptfoo) | llm_eval | TRIAL | npm | OSI_SPDX | MIT | 25155 |
| 88 | [DeepEval](https://github.com/confident-ai/deepeval) | llm_eval | ASSESS | uvx | OSI_SPDX | Apache-2.0 | 18286 |
| 89 | [Ragas](https://github.com/vibrantlabsai/ragas) | rag_eval | ASSESS | uvx | OSI_SPDX | Apache-2.0 | 15746 |
| 90 | [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) | llm_eval | TRIAL | uvx | OSI_SPDX | MIT | 2781 |
| 91 | [Garak](https://github.com/NVIDIA/garak) | llm_security | TRIAL | uvx | OSI_SPDX | Apache-2.0 | 9261 |
| 92 | [PyRIT](https://github.com/microsoft/PyRIT) | llm_security | TRIAL | on-demand | OSI_SPDX | MIT | 4477 |
| 93 | [Phoenix](https://github.com/Arize-ai/phoenix) | llm_observability | HOLD | none | SOURCE_AVAILABLE_NON_OSI | Elastic License 2.0 | 11478 |
| 94 | [Opik](https://github.com/comet-ml/opik) | llm_observability | HOLD | none | OSI_SPDX | Apache-2.0 | 22050 |
| 95 | [Grafana Alloy](https://github.com/grafana/alloy) | observability | ASSESS | none | OSI_SPDX | Apache-2.0 | 3539 |
| 96 | [Prometheus](https://github.com/prometheus/prometheus) | observability | ASSESS | compose_profile | OSI_SPDX | Apache-2.0 | 66085 |
| 97 | [Loki](https://github.com/grafana/loki) | observability | ASSESS | compose_profile | OSI_SPDX | AGPL-3.0 | 28895 |
| 98 | [Tempo](https://github.com/grafana/tempo) | observability | ASSESS | compose_profile | OSI_SPDX | AGPL-3.0 | 5475 |
| 99 | [Grafana](https://github.com/grafana/grafana) | observability | ASSESS | compose_profile | OSI_SPDX | AGPL-3.0 | 76767 |
| 100 | [Qdrant](https://github.com/qdrant/qdrant) | vector_db | HOLD | none | OSI_SPDX | Apache-2.0 | 34585 |
| 101 | [Meilisearch](https://github.com/meilisearch/meilisearch) | search | ASSESS | none | MANUAL_OSS | MIT | 59301 |
| 102 | [MarkItDown](https://github.com/microsoft/markitdown) | document_processing | TRIAL | uv-tool | OSI_SPDX | MIT | 184513 |
| 103 | [Docling](https://github.com/docling-project/docling) | document_processing | ASSESS | none | OSI_SPDX | MIT | 66470 |
| 104 | [Crawl4AI](https://github.com/unclecode/crawl4ai) | web_intelligence | TRIAL | uvx | OSI_SPDX | Apache-2.0 | 83623 |
| 105 | [Firecrawl](https://github.com/firecrawl/firecrawl) | web_intelligence | ASSESS | none | OSI_SPDX | AGPL-3.0 | 180970 |
| 106 | [browser-use](https://github.com/browser-use/browser-use) | browser_automation | ASSESS | none | OSI_SPDX | MIT | 114753 |
| 107 | [Temporal](https://github.com/temporalio/temporal) | workflow_engine | HOLD | none | OSI_SPDX | MIT | 23079 |
| 108 | [Twenty](https://github.com/twentyhq/twenty) | crm | HOLD | none | OPEN_CORE_MIXED | AGPL-3.0 core + enterprise-marked files | 56853 |
| 109 | [Vaultwarden](https://github.com/dani-garcia/vaultwarden) | secrets_ui | ASSESS | none | OSI_SPDX | AGPL-3.0 | 67731 |
| 110 | [OpenFGA](https://github.com/openfga/openfga) | authorization | TRIAL | none | OSI_SPDX | Apache-2.0 | 5780 |
| 111 | [OPA](https://github.com/open-policy-agent/opa) | policy | TRIAL | none | OSI_SPDX | Apache-2.0 | 12238 |
| 112 | [Keycloak](https://github.com/keycloak/keycloak) | identity | ASSESS | none | OSI_SPDX | Apache-2.0 | 36795 |
| 113 | [dbt Core](https://github.com/dbt-labs/dbt) | analytics_engineering | ASSESS | none | OSI_SPDX | Apache-2.0 | 13834 |
| 114 | [Great Expectations](https://github.com/fivetran/great_expectations) | data_quality | ASSESS | none | OSI_SPDX | Apache-2.0 | 11796 |
| 115 | [OpenLineage](https://github.com/OpenLineage/OpenLineage) | data_lineage | ASSESS | none | OSI_SPDX | Apache-2.0 | 2658 |
| 116 | [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | agent_framework | ASSESS | on-demand | OSI_SPDX | MIT | 13540 |
| 117 | [pip-audit](https://github.com/pypa/pip-audit) | security | ADOPT | uv-tool | OSI_SPDX | Apache-2.0 | 1363 |
| 118 | [pgcli](https://github.com/dbcli/pgcli) | data_ops | TRIAL | uv-tool | OSI_SPDX | BSD-3-Clause | 13388 |
| 119 | [Node-RED](https://github.com/node-red/node-red) | workflow_automation | ASSESS | on-demand | OSI_SPDX | Apache-2.0 | 23655 |
| 120 | [OpenBao](https://github.com/openbao/openbao) | secrets_management | TRIAL | on-demand | OSI_SPDX | MPL-2.0 | 7372 |
| 121 | [Valkey](https://github.com/valkey-io/valkey) | data_cache | ASSESS | on-demand | OSI_SPDX | BSD-3-Clause | 27208 |
| 122 | [OpenTofu](https://github.com/opentofu/opentofu) | infrastructure_as_code | ASSESS | on-demand | OSI_SPDX | MPL-2.0 | 30188 |

## Reproducible usage

```bash
./scripts/bootstrap_open_source_toolchain.sh
./scripts/verify_open_source_toolchain.py --check-installed
./tooling/oss/run trivy --version
./tooling/oss/run gitleaks version
```

These commands do not start always-on services or mutate production.
