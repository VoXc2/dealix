# Self-Growth OS Package — Honest Scope

> Where ``auto_client_acquisition/self_growth_os/`` is at, what it
> does today, what it does NOT do (and why), and the explicit
> ship-when trigger for every deferred module.
>
> Pairs with ``docs/SELF_GROWTH_OS_SCOPE.md`` (sibling document
> tracking the broader 23-phase prompt) and
> ``docs/STRATEGIC_MASTER_PLAN_2026.md`` Part V.B.

## What's real (6 modules, all tested)

| Module | What it does | Wraps | Tests |
|---|---|---|---|
| `schemas.py` | Typed records used across the package: `ServiceActivationCheck`, `SafePublishingResult`, `ToolCapability`, `EvidenceRecord` + enums (`Language`, `RiskLevel`, `ApprovalStatus`, `ServiceBundle`, `PublishingDecision`). Default `approval_status=approval_required`. `extra="forbid"` to catch typo bugs. | Pydantic v2 | `tests/test_self_growth_os_package.py::test_schemas_*` |
| `safe_publishing_gate.py` | Runtime safe-publishing gate over ANY draft string. Returns typed `SafePublishingResult` with decision (`allowed_draft` / `needs_review` / `blocked`), forbidden tokens found, sample excerpts. Same vocabulary as the YAML validator + perimeter test. Never modifies input. | `scripts/verify_service_readiness_matrix.py`, `tests/test_landing_forbidden_claims.py` | `test_safe_publishing_gate_*` |
| `service_activation_matrix.py` | Read-only access to `docs/registry/SERVICE_READINESS_MATRIX.yaml`. Functions: `counts()`, `check_service(id)`, `check_all()`, `candidates_for_promotion()`. Honest signal: `eight_gate_block_present` is True only when the YAML actually carries a `gates:` mapping. | `docs/registry/SERVICE_READINESS_MATRIX.yaml` | `test_service_matrix_*` |
| `seo_technical_auditor.py` | Read-only access to `docs/SEO_AUDIT_REPORT.json`. Functions: `summary()`, `pages_with_required_gaps()`, `pages_with_advisory_gaps()`, `gap_count()`, `is_perimeter_clean()`. | `scripts/seo_audit.py` | `test_seo_auditor_*` |
| `tool_registry.py` | Optional-tooling registry. 15 entries (pyyaml, fastapi, anthropic, openai, lxml, …). Each row says installed/missing + required_for_core + install_hint. Defensive against C-extension panics. Never installs. | `requirements.txt` (informational only) | `test_tool_registry_*` |
| `evidence_collector.py` | In-process append-only buffer of typed events. `record()`, `all_events()`, `clear()`, `write_jsonl()`, `language_breakdown()`. Seed of the future ProofEvent ledger. | (none yet) | `test_evidence_collector_*` |

## API surface added (all read-only except publishing/check)

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/self-growth/status` | Guardrail summary + which sub-payloads exist |
| GET | `/api/v1/self-growth/service-activation` | Full matrix JSON (existing) |
| GET | `/api/v1/self-growth/service-activation/{id}` | Typed `ServiceActivationCheck` for one service |
| GET | `/api/v1/self-growth/service-activation-candidates` | Partial/Pilot services ranked for promotion |
| GET | `/api/v1/self-growth/seo/audit` | Full SEO audit report (existing) |
| GET | `/api/v1/self-growth/seo/audit/summary` | Compact SEO summary + advisory-gap histogram |
| GET | `/api/v1/self-growth/tooling` | Tool-registry audit |
| POST | `/api/v1/self-growth/publishing/check` | Run safe-publishing gate over a draft string |

`POST /publishing/check` is the only non-GET endpoint and **NEVER stores
the input or sends anything**. It runs the regex and returns the result.

## What's NOT here (and why)

The original Self-Growth OS prompts asked for 22+ modules. We
intentionally shipped only the 6 above. The remaining 16 are
deferred — each with a documented ship-when trigger.

| Deferred module | Why deferred | Ship-when trigger |
|---|---|---|
| `search_radar.py` | Inventing search volume violates "no fake data" hard rule | Founder picks a real source: GSC / Bing Webmaster / Ahrefs API / curated list (decision B4) |
| `keyword_intent_radar.py` | Same reason — depends on real search data | After search_radar |
| `geo_aio_radar.py` | A real GEO playbook needs baseline AI citation data we don't have yet | After 1 week of recording how Perplexity/ChatGPT describe Dealix |
| `content_brief_generator.py` | Briefs without keyword/intent data are unanchored | After search_radar + keyword_intent_radar |
| `content_draft_engine.py` | Draft engine without runtime approval queue is unsafe; engine output must go through `dealix.governance.approvals.ApprovalGate` (Redis) | After founder defines the review channel (Notion? GitHub PRs? CLI?) |
| `content_quality_gate.py` | 70% covered by `safe_publishing_gate.py` (this branch) + the perimeter sweeps; full version needs human-calibrated scoring | After ≥10 founder-reviewed drafts exist as training |
| `landing_page_opportunity_engine.py` | Roadmap of 23 pages exceeds founder calendar bandwidth | Founder picks the next 1–3 pages |
| `internal_linking_planner.py` | Useful only when catalog grows past ~10 pages with shared concepts | When a new page lands and link-graph audit is needed |
| `distribution_planner.py` | Distribution surface — same risk as draft engine; publishing without approval queue = unsafe | After `content_draft_engine` ships |
| `social_draft_engine.py` | Same as above | Same |
| `partner_distribution_radar.py` | Already partially documented in `docs/partners/`; new code without a partner CRM duplicates state | When partner outreach starts (after first 3 paid pilots) |
| `community_signal_radar.py` | "Do not scrape automatically" — a community radar is just a manual log file until ingestion path is decided | When founder picks log location (Notion/GitHub Issues/...) |
| `proof_snippet_engine.py` | Requires real `ProofEvent` rows; none exist yet | After first paid pilot generates real ProofEvent JSON |
| `daily_growth_loop.py` | The personal-operator daily brief already exists at `/api/v1/personal-operator/daily-brief`. A parallel CLI fragments founder workflow | If founder explicitly wants a CLI in addition to the API |
| `weekly_growth_scorecard.py` | Same as above | After founder runs daily brief 4 weeks and lists missing fields |
| `self_improvement_loop.py` | Highest-value phase, but requires search/intent/draft engines real first | Build when those 3 are landed and have ≥2 weeks of data |

## Hard guarantees of every module here

- **Draft-only by default.** No external send / charge / scrape.
- **`approval_required` is the default `approval_status`** on every record that represents an external action.
- **Arabic-primary, English-secondary** — every text-bearing record carries a `language` enum and the `Language.AR` default reflects this.
- **Never claim guaranteed revenue / ranking / proof.** The `safe_publishing_gate` enforces this at runtime; the YAML validator enforces it in source.
- **Never log PII.** `evidence_collector` warns callers; the schemas don't capture customer PII fields by default.
- **No new live-action env flags.** All 4 `*_ALLOW_LIVE_*` variables remain off by default; `tests/test_live_gates_default_false.py` enforces this.

## Where it plugs in

```
                ┌──────────────────────────────────────────┐
                │  docs/registry/SERVICE_READINESS_MATRIX  │
                │              .yaml (32 services)         │
                └──────────────┬───────────────────────────┘
                               │
                               │ read-only via
                               ▼
              ┌──────────────────────────────────────────┐
              │ self_growth_os.service_activation_matrix │
              └──────────────┬───────────────────────────┘
                             │
                             │  ServiceActivationCheck
                             ▼
              ┌──────────────────────────────────────────┐
              │     api/routers/self_growth.py           │
              │  /service-activation/{id}                │
              │  /service-activation-candidates          │
              └──────────────────────────────────────────┘

         Drafts in (any source)
                │
                ▼
   self_growth_os.safe_publishing_gate.check_text()
                │
                ▼
   SafePublishingResult { decision, forbidden_tokens, … }
                │
                ▼
   POST /api/v1/self-growth/publishing/check
                │
                ▼
   (caller decides whether to send to ApprovalGate /
    rephrase / reject — this gate never stores anything)
```

## Test counts (after this commit)

```
105 passed in the new-bundle pytest run
  2 skipped (CompanyBrain — module not yet implemented)
  3 xfailed (free-form Arabic + English safety classifier on the
              personal-operator route — explicit bug tickets, never
              fake-green)
```

## What would unlock the next module

If exactly one decision is made next, the highest-leverage one is
**B4** (pick a search/keyword data source). That single choice
unlocks `search_radar`, `keyword_intent_radar`, and
`content_brief_generator` — three modules that today are blocked
on "do not invent search volume."
