# AI and Automation Tooling Backlog

## Purpose
Track useful tools and libraries that may help Dealix without adding them blindly.

Every tool must pass the Vendor and Tool Adoption Policy before production use.

## Priority categories

| Category | Why it matters |
|---|---|
| LLM observability | Trace prompts, outputs, cost, quality, and incidents |
| Evaluation | Test AI outputs before release |
| RAG and retrieval | Improve source-grounded answers |
| Security testing | Detect prompt injection, leaks, and unsafe outputs |
| CRM automation | Improve account and opportunity workflows |
| Data quality | Keep account, KPI, and customer data reliable |
| Analytics | Help founder see decisions, not vanity metrics |
| Workflow automation | Reduce manual handoffs and execution delay |

## Candidate tool register

| Tool or category | Possible use | Risk | Decision |
|---|---|---|---|
| Langfuse | LLM traces, evals, prompt observability | Medium | Already listed as active dependency |
| OpenTelemetry | Vendor-neutral observability | Medium | Evaluate |
| Great Expectations | Data quality checks | Medium | Evaluate |
| Evidently AI | ML and data drift monitoring | Medium | Evaluate |
| Ragas | RAG evaluation | Medium | Evaluate |
| DeepEval | LLM evaluation | Medium | Evaluate |
| Garak | LLM vulnerability testing | High | Review before use |
| OWASP LLM test cases | AI security review reference | Medium | Reference |
| Prefect or Dagster | Workflow orchestration | Medium | Evaluate only if jobs grow |
| n8n | Internal workflow automation | Medium | Evaluate data handling first |
| PostHog | Product analytics | Medium | Evaluate if privacy controls fit |
| Metabase | Internal dashboards | Medium | Evaluate |
| Superset | Analytics dashboards | Medium | Evaluate |
| Sentry | Error tracking | Medium | Evaluate |
| Semgrep | Static analysis | Medium | Evaluate alongside CodeQL |
| TruffleHog | Secret scanning | Medium | Evaluate if GitHub scanning is insufficient |

## Adoption workflow

1. Add candidate here.
2. Create AI risk review or security review issue if relevant.
3. Document data used.
4. Estimate cost and operating owner.
5. Test in isolated environment.
6. Record decision.
7. Add to AI Tool Registry only after approval.

## Do not add directly

Avoid adding these without review:

- Tools that send customer data externally.
- Tools that automate outbound customer communication.
- Tools that scrape or enrich personal data.
- Tools with unclear license.
- Tools with unclear data retention.
- Tools that duplicate existing capabilities.
