# Wave 15 — Customer Ops Polish · Evidence Table

> **Wave 15 scope:** convert Wave 13 + Wave 14 backend into founder-
> usable daily tooling + static-frontend integration + E2E coverage.
> Three new CLIs + one new static JSON + one new E2E test file. Zero
> new business logic (Article 11). All 8 hard gates preserved.
>
> **Article 4** (8 hard gates immutable): each new CLI prints to stdout
> or writes gitignored files; NEVER auto-sends. Verifier asserts no
> live actions.
>
> **Article 8** (no fake claims): every numeric carries `is_estimate=True`.
> Founder Daily Brief honestly reports `article_13_trigger_remaining`.
>
> **Article 11** (no duplication): all 3 CLIs compose existing modules
> (`service_catalog`, `bottleneck_radar`, `expansion_engine`). The
> static JSON is a deterministic export of the registry — not a parallel
> truth.

## Verdict

```
DEALIX_WAVE15_CUSTOMER_OPS_VERDICT=PASS
Total: 16 · PASS: 15 · FAIL: 0 · SANDBOX_SKIP: 1
```

Single command: `bash scripts/dealix_wave15_customer_ops_verify.sh`.

## Evidence rows (7-column schema)

| # | Layer | Required | Actual | Test path / Verifier line | Hard gate preserved | Status |
|---|---|---|---|---|---|---|
| 1 | Service Catalog JSON exporter | Registry → `landing/assets/data/services-catalog.json`, idempotent + `--check` mode | `scripts/dealix_export_service_catalog_json.py` (~110 LOC) | `SERVICE_CATALOG_JSON_EXPORTER=PASS` + 2 schema checks | Article 11 (single source of truth) | PASS |
| 2 | Service Catalog static JSON | 7 offerings + 8 hard gates + Article 8/11 declarations | `landing/assets/data/services-catalog.json` (291 lines) | `SERVICE_CATALOG_JSON_HAS_7_OFFERINGS=PASS` + `SERVICE_CATALOG_JSON_HAS_8_HARD_GATES=PASS` | All 8 enumerated | PASS |
| 3 | Bottleneck Radar standalone CLI | 3 output formats (md, json, one-line) + bilingual | `scripts/dealix_bottleneck_radar.py` (~130 LOC) | `BOTTLENECK_RADAR_CLI_MD/JSON/ONE_LINE=PASS` (3 checks) | Article 8 (is_estimate=True in JSON) | PASS |
| 4 | Founder Daily Brief CLI | Composes Bottleneck + Service Catalog + Article 13 status into single bilingual brief | `scripts/dealix_founder_daily_brief.py` (~210 LOC) | `FOUNDER_DAILY_BRIEF_MD=PASS` + 2 schema checks | Article 4 (NEVER auto-sends — stdout/file only) + Article 8 (article_13_trigger_remaining honest) | PASS |
| 5 | E2E customer journey integration test | 13 tests covering catalog + passport + lifecycle + bottleneck + expansion + hard gates + Article 8 + Article 13 | `tests/test_wave15_customer_journey_e2e.py` (~315 LOC, 13 tests) | `WAVE15_CUSTOMER_JOURNEY_E2E=PASS` | All 8 hard gates verified per step | PASS |
| 6 | Wave 13 regression | Wave 13 master verifier still PASS (17/17) | unchanged | `WAVE13_REGRESSION=PASS` | All 8 immutable | PASS |
| 7 | Wave 14 regression | Wave 14 verifier still PASS (19/20 + 1 SANDBOX_SKIP) | unchanged | `WAVE14_REGRESSION=PASS` | All 8 immutable | PASS |
| 8 | Article 4 lockdown (linkedin_scraper) | git-ls-files-wide scan + Wave 15 docs allowlisted | extended `tests/test_no_linkedin_scraper_string_anywhere.py` allowlist | `NO_LINKEDIN_SCRAPER_STRING=PASS` | NO_LINKEDIN_AUTO + NO_SCRAPING | PASS |
| 9 | Article 8 forbidden claims | No `نضمن` / `guaranteed` / `blast` / `scraping` in any landing/ HTML | unchanged | `FORBIDDEN_CLAIMS_LINT=PASS` | NO_FAKE_REVENUE + NO_FAKE_PROOF | PASS |
| 10 | Constitution closure (16 invariants) | Beast CC + Portal + Golden Loop healthy | sandbox-skip via `pyotp` cascade (Wave 11 §31) | `CONSTITUTION_CLOSURE=SANDBOX_SKIP` | n/a sandbox | SANDBOX_SKIP (prod PASS) |

## Phase-by-phase breakdown

### Phase A — Compile sanity (1 check)

- `COMPILEALL_WAVE15_SCRIPTS` — all 3 new CLIs compile cleanly

### Phase B — Service Catalog JSON (3 checks)

- `SERVICE_CATALOG_JSON_EXPORTER` — `--check` mode verifies on-disk JSON matches registry
- `SERVICE_CATALOG_JSON_HAS_7_OFFERINGS` — count assertion
- `SERVICE_CATALOG_JSON_HAS_8_HARD_GATES` — Article 4 enumeration

### Phase C — Bottleneck Radar CLI (3 checks)

- `BOTTLENECK_RADAR_CLI_MD` — markdown format
- `BOTTLENECK_RADAR_CLI_JSON` — JSON format + `is_estimate=True` invariant
- `BOTTLENECK_RADAR_CLI_ONE_LINE` — single-line summary

### Phase D — Founder Daily Brief CLI (3 checks)

- `FOUNDER_DAILY_BRIEF_MD` — markdown contains Article 13 section
- `FOUNDER_DAILY_BRIEF_HARD_GATES_LISTED` — JSON has all 8 gates
- `FOUNDER_DAILY_BRIEF_ARTICLE_13_REMAINING_3_WHEN_ZERO_PAID` — Article 8 honesty

### Phase E — E2E (1 check, 13 sub-tests)

- `WAVE15_CUSTOMER_JOURNEY_E2E` — `tests/test_wave15_customer_journey_e2e.py`
  1. Service catalog 7 offerings + valid action_modes
  2. Decision Passport validates owner + action_mode
  3. Decision Passport blocks cold_whatsapp channel
  4. Service Session lifecycle state machine valid
  5. Bottleneck Radar empty state = `clear`
  6. Bottleneck Radar 5+ items = `critical` + bilingual action
  7. Expansion Readiness Score returns bounded float
  8. Expansion ready when proof mature
  9. All 8 hard gates present in every offering
  10. No forbidden action_modes in catalog
  11. No guarantee language in KPI commitments
  12. Service Catalog JSON in sync with registry
  13. Article 13 gate logic in daily brief

### Phase F — Wave 13/14 regression (2 checks)

- `WAVE13_REGRESSION` — Wave 13 verifier 17/17 PASS
- `WAVE14_REGRESSION` — Wave 14 verifier 19/20 PASS + 1 SANDBOX_SKIP

### Phase G — Article 4 + 8 invariants (3 checks)

- `NO_LINKEDIN_SCRAPER_STRING` — git-wide scan
- `FORBIDDEN_CLAIMS_LINT` — landing HTML scan
- `CONSTITUTION_CLOSURE` — SANDBOX_SKIP (production curl smoke validates)

## Files added in Wave 15

**New scripts (3, ~450 LOC):**
- `scripts/dealix_export_service_catalog_json.py` (~110 LOC) — registry → JSON
- `scripts/dealix_bottleneck_radar.py` (~130 LOC) — 3-format CLI
- `scripts/dealix_founder_daily_brief.py` (~210 LOC) — composite morning brief

**New verifier (1):**
- `scripts/dealix_wave15_customer_ops_verify.sh` (~140 LOC, 16 checks)

**New static data (1):**
- `landing/assets/data/services-catalog.json` (291 lines, generated from registry)

**New test (1, ~315 LOC, 13 tests):**
- `tests/test_wave15_customer_journey_e2e.py` — E2E integration walking Wave 13 + 14 modules

**New docs (1):**
- `docs/WAVE15_EVIDENCE_TABLE.md` (this file)

**Modified:**
- `tests/test_no_linkedin_scraper_string_anywhere.py` — extend allowlist for Wave 15 docs

## Constitution compliance audit

| Article | How preserved |
|---|---|
| **Article 3** (no V13/V14 architecture before paid pilots) | Wave 15 is pure tooling + tests. Zero new business logic. |
| **Article 4** (8 hard gates immutable) | Founder daily brief NEVER auto-sends; explicit `_HARD_GATES` tuple printed every run. Verifier asserts list is 8 items. |
| **Article 6** (8-section portal contract) | Untouched. |
| **Article 8** (no fake claims) | Every CLI marks `is_estimate=True` in JSON output. Article 13 status honestly reports `remaining`. |
| **Article 11** (no features beyond required) | All 3 CLIs COMPOSE existing modules (`service_catalog.registry`, `bottleneck_radar.computer`, `expansion_engine.readiness_score`). |
| **Article 13** (3 paid pilots gate) | Daily Brief surfaces `article_13_trigger_remaining` — never claims trigger fired without 3 confirmed paid. |

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

## How to use Wave 15 deliverables

```bash
# 1. Regenerate Service Catalog JSON when registry changes:
python3 scripts/dealix_export_service_catalog_json.py

# 2. Verify on-disk JSON matches registry (CI-friendly):
python3 scripts/dealix_export_service_catalog_json.py --check

# 3. Morning Bottleneck Radar (paste counts from layer modules):
python3 scripts/dealix_bottleneck_radar.py \
    --blocking-approvals 3 --pending-payments 1 \
    --overdue-followups 5 --format md

# 4. Consolidated founder daily brief (THE morning ritual):
python3 scripts/dealix_founder_daily_brief.py \
    --blocking-approvals 2 --pending-payments 1 \
    --paid-customers 0

# 5. Write brief to gitignored file (for cron):
python3 scripts/dealix_founder_daily_brief.py \
    --paid-customers 0 \
    --out data/founder_briefs/$(date +%Y-%m-%d).md

# 6. Full Wave 15 verification:
bash scripts/dealix_wave15_customer_ops_verify.sh
```

## Next founder action

> _"Add `python3 scripts/dealix_founder_daily_brief.py --paid-customers <N>` to your morning ritual at 8 AM KSA. The output is copy-paste-able into WhatsApp. Track `paid_customers_count` manually as you close pilots. Once Article 13 trigger fires (3 paid), the brief automatically pivots to 'run customer signal synthesis'."_
