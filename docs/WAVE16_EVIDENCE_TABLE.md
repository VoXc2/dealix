# Wave 16 — Auto-Source + Content · Evidence Table

> **Wave 16 scope:** convert Wave 15 daily-brief CLI from manual flags
> to live module reads + add 2 new founder CLIs (artifact enforcer +
> case study builder) + new customer-facing landing page (sector
> benchmark) + 16-test E2E coverage. Zero new business logic
> (Article 11). All 8 hard gates preserved.
>
> **Article 4** (8 hard gates immutable): every new CLI is read-only OR
> writes to gitignored files only; NEVER auto-publishes, NEVER
> auto-sends. Verifier asserts no live actions.
>
> **Article 8** (no fake claims): `query_layer_counts()` returns 0
> honestly when modules empty. Case Study Builder REFUSES to fabricate
> when no events meet publish gate.
>
> **Article 11** (no duplication): all 3 CLIs + 1 module compose
> existing layer code. Sector Benchmark page references real data
> sources by file path.

## Verdict

```
DEALIX_WAVE16_AUTO_SOURCE_VERDICT=PASS
Total: 16 · PASS: 15 · FAIL: 0 · SANDBOX_SKIP: 1
```

Single command: `bash scripts/dealix_wave16_auto_source_verify.sh`.

## Evidence rows (7-column schema)

| # | Layer | Required | Actual | Test path / Verifier line | Hard gate preserved | Status |
|---|---|---|---|---|---|---|
| 1 | `founder_brief` auto-source module | Pure-read helper that queries 5 layer modules + paid customers; returns LayerCounts dataclass | `auto_client_acquisition/founder_brief/__init__.py` (~190 LOC) | `FOUNDER_BRIEF_AUTO_SOURCE=PASS` (4 sub-tests) | Article 8 (returns 0 honestly when empty) | PASS |
| 2 | `--auto-source` flag in daily brief | Replaces 6 manual flags with single live query | extension to `scripts/dealix_founder_daily_brief.py` | `DAILY_BRIEF_AUTO_SOURCE_FLAG=PASS` | CLI flags still override (max-with) | PASS |
| 3 | Daily Artifact Enforcer CLI | Lists active service sessions with 2+ days no artifact; 3 formats (md/json/one-line) + `--strict` mode | `scripts/dealix_artifact_enforcer.py` (~165 LOC) | `ARTIFACT_ENFORCER_CLI=PASS` (3 sub-tests) + `ARTIFACT_ENFORCER_ONE_LINE=PASS` | Article 4 (read-only — never auto-closes); Article 8 (no fake_proof — surface from orchestrator only) | PASS |
| 4 | Case Study auto-generator CLI | Takes proof events JSONL + builds bilingual case study draft via existing `case_study_engine.builder` | `scripts/dealix_case_study_builder.py` (~210 LOC) + `--demo` mode | `CASE_STUDY_DEMO_MODE=PASS` (4 sub-tests) + `CASE_STUDY_DEMO_BUILDS=PASS` | Article 4 (NEVER auto-publishes — draft_only); Article 8 (REFUSES when 0 publishable, exit 1) | PASS |
| 5 | Sector Benchmark landing page | 6 Saudi B2B sectors × signals + recommended angles + bilingual + Article 8 declarations | `landing/sector-benchmark.html` (~310 lines, 6 `data-sector-id` cards) | `SECTOR_BENCHMARK_HTML=PASS` (4 sub-tests) | NO_BLAST + NO_COLD_WHATSAPP + NO_SCRAPING (in negation context, allowlisted) | PASS |
| 6 | Forbidden claims linter (sector-benchmark allowlist) | `tests/test_landing_forbidden_claims.py` ALLOWLIST extended for Wave 16 negations | `tests/test_landing_forbidden_claims.py` 3 entries: blast/cold/scraping NEGATION | `FORBIDDEN_CLAIMS_LINT=PASS` | All 8 gates honored | PASS |
| 7 | linkedin_scraper lockdown | git-ls-files-wide scan + Wave 16 docs allowlist | extended `tests/test_no_linkedin_scraper_string_anywhere.py` | `NO_LINKEDIN_SCRAPER_STRING=PASS` | NO_LINKEDIN_AUTO + NO_SCRAPING immutable | PASS |
| 8 | NO_WAVE16_CLI_LIVE_SEND invariant | Idempotent read-test on auto-source helper | `tests/test_wave16_auto_source_and_content.py` test_no_wave16_cli_attempts_live_send | `NO_WAVE16_CLI_LIVE_SEND=PASS` | Article 4 enforced | PASS |
| 9 | Wave 13 regression | Wave 13 master verifier still PASS (17/17) | unchanged | `WAVE13_REGRESSION=PASS` | All 8 immutable | PASS |
| 10 | Wave 14 regression | Wave 14 verifier still PASS (19/20 + 1 SANDBOX_SKIP) | unchanged | `WAVE14_REGRESSION=PASS` | All 8 immutable | PASS |
| 11 | Wave 15 regression | Wave 15 verifier still PASS (15/16 + 1 SANDBOX_SKIP) | unchanged | `WAVE15_REGRESSION=PASS` | All 8 immutable | PASS |
| 12 | Constitution closure | Beast CC + Portal + Golden Loop healthy | sandbox-skip via `pyotp` cascade (Wave 11 §31) | `CONSTITUTION_CLOSURE=SANDBOX_SKIP` | n/a sandbox | SANDBOX_SKIP (prod PASS) |

## Files added in Wave 16

**New module (1 dir, ~190 LOC):**
- `auto_client_acquisition/founder_brief/__init__.py` — `LayerCounts` dataclass + `query_layer_counts()` composing 5 layer modules

**New CLIs (2 scripts, ~375 LOC):**
- `scripts/dealix_artifact_enforcer.py` (~165 LOC) — 3-format CLI for overdue session detection
- `scripts/dealix_case_study_builder.py` (~210 LOC) — proof events → bilingual case study draft

**New verifier (1, ~125 LOC, 16 checks):**
- `scripts/dealix_wave16_auto_source_verify.sh`

**New static page (1, ~310 lines):**
- `landing/sector-benchmark.html` — 6 Saudi B2B sectors with signals + angles

**New test (1, ~250 LOC, 16 tests):**
- `tests/test_wave16_auto_source_and_content.py`

**New docs (1):**
- `docs/WAVE16_EVIDENCE_TABLE.md` (this file)

**Modified:**
- `scripts/dealix_founder_daily_brief.py` — added `--auto-source` flag + `query_layer_counts` import
- `tests/test_landing_forbidden_claims.py` — extended ALLOWLIST for sector-benchmark.html negations
- `tests/test_no_linkedin_scraper_string_anywhere.py` — extended allowlist for Wave 16 docs

## Phase-by-phase breakdown

### Phase A — Compile sanity (2 checks)

- `COMPILEALL_WAVE16_MODULES` — `founder_brief/` package compiles
- `COMPILEALL_WAVE16_SCRIPTS` — both new CLIs compile

### Phase B — Auto-source for daily brief (2 checks)

- `FOUNDER_BRIEF_AUTO_SOURCE` — 4 sub-tests on `query_layer_counts()`
- `DAILY_BRIEF_AUTO_SOURCE_FLAG` — `--auto-source` produces JSON with `is_estimate=True`

### Phase C — Artifact Enforcer CLI (2 checks)

- `ARTIFACT_ENFORCER_CLI` — 3 sub-tests (empty state, one-line format, JSON has is_estimate)
- `ARTIFACT_ENFORCER_ONE_LINE` — single-line output contains `artifact_enforcer`

### Phase D — Case Study Builder (2 checks)

- `CASE_STUDY_DEMO_MODE` — 4 sub-tests (demo, JSON, refusal, usage error)
- `CASE_STUDY_DEMO_BUILDS` — JSON output has `candidate` field

### Phase E — Sector Benchmark page (1 check, 4 sub-tests)

- `SECTOR_BENCHMARK_HTML` — exists, 6 sectors, bilingual, declares is_estimate

### Phase F — Article 4 + 8 cross-cutting (3 checks)

- `FORBIDDEN_CLAIMS_LINT` — landing forbidden tokens audit
- `NO_LINKEDIN_SCRAPER_STRING` — git-wide scan
- `NO_WAVE16_CLI_LIVE_SEND` — idempotency check on auto-source

### Phase G — Wave 13/14/15 regression (3 checks)

- `WAVE13_REGRESSION` — Wave 13 verifier 17/17 PASS
- `WAVE14_REGRESSION` — Wave 14 verifier 19/20 PASS + 1 SANDBOX_SKIP
- `WAVE15_REGRESSION` — Wave 15 verifier 15/16 PASS + 1 SANDBOX_SKIP

### Phase H — Constitution (1 check, sandbox-aware)

- `CONSTITUTION_CLOSURE` — SANDBOX_SKIP (production curl smoke validates)

## Constitution compliance audit

| Article | How preserved |
|---|---|
| **Article 3** (no V13/V14 architecture before paid pilots) | Wave 16 is pure tooling + content + tests. Zero new business logic. |
| **Article 4** (8 hard gates immutable) | All 3 new CLIs are read-only OR draft_only. Verifier asserts. Hard gates listed in every output JSON. |
| **Article 6** (8-section portal contract) | Untouched. |
| **Article 8** (no fake claims) | `query_layer_counts()` returns 0 honestly when empty. Case Study Builder REFUSES (exit 1) when no publishable events. Sector Benchmark declares `is_estimate=True` per card. |
| **Article 11** (no features beyond required) | `founder_brief` composes existing modules; CLIs wrap `case_study_engine.builder` + `service_sessions.orchestrator`; landing page references `sector_pulse.py` truth registry. |
| **Article 13** (3 paid pilots gate) | Daily brief still tracks `paid_customers_count`; `--auto-source` reads live count from `payment_ops`. |

## Hard gates audit (Article 4 immutable)

```
NO_LIVE_SEND=immutable
NO_LIVE_CHARGE=immutable
NO_COLD_WHATSAPP=immutable
NO_LINKEDIN_AUTO=immutable
NO_SCRAPING=immutable
NO_FAKE_PROOF=immutable
NO_FAKE_REVENUE=immutable
NO_BLAST=immutable
```

## How to use Wave 16 deliverables

```bash
# 1. Morning founder brief — automatic from live module state:
python3 scripts/dealix_founder_daily_brief.py --auto-source

# 2. Founder brief with manual override (CLI flags take max with live):
python3 scripts/dealix_founder_daily_brief.py --auto-source --paid-customers 1

# 3. Daily artifact check (cron-friendly with --strict):
python3 scripts/dealix_artifact_enforcer.py --strict --format one-line

# 4. Case Study builder demo (sandbox-safe):
python3 scripts/dealix_case_study_builder.py --demo \
    --customer-handle acme-real-estate --sector real_estate

# 5. Case Study from real proof events JSONL:
python3 scripts/dealix_case_study_builder.py \
    --customer-handle acme-real-estate \
    --sector real_estate \
    --events data/customers/acme-real-estate/proof_events.jsonl

# 6. Full Wave 16 verification:
bash scripts/dealix_wave16_auto_source_verify.sh
```

## Customer-facing artifacts (post-Wave 16)

| Page | URL | What it shows |
|---|---|---|
| Service Catalog | `/services.html` | 7 priced offerings (Wave 14) |
| Sector Benchmark | `/sector-benchmark.html` | 6 Saudi sectors × signals × angles (Wave 16) |
| Customer Portal | `/customer-portal.html` | Per-customer 9-section view |
| Case Study (template) | `/case-study.html` | 1 example case study |
| Diagnostic | `/diagnostic.html` | Free intake form |
| Sprint signup | `/start.html` | 499 SAR Sprint signup |

## Next founder action

> _"Add `python3 scripts/dealix_founder_daily_brief.py --auto-source --out data/founder_briefs/$(date +%Y-%m-%d).md` to your morning ritual at 8 AM KSA via Railway cron. Share `https://dealix.me/sector-benchmark.html` with prospects when their sector matches a recommended angle."_
