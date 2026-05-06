# Dealix Operating Constitution — Truth Audit

Single-page mapping: **Article → code/docs → status**. Updated with Constitution Closure PR (founder beast CC, customer portal, golden loop test).

| # | Topic | Status | Primary path |
|---|--------|--------|----------------|
| 1 | Final definition (Saudi self-growing Company OS) | LIVE-DOC | `docs/DEALIX_OPERATING_CONSTITUTION.md` |
| 2 | Golden loop (signal → … → better targeting) | LIVE-CODE-TESTED | `tests/test_golden_loop_integration.py` |
| 3 | Four laws (growth/revenue/delivery/proof + evidence + approval + market learning) | LIVE-CODE | Hard gates on routers; `revenue_pipeline.advance`; `revops` evidence |
| 4 | Hard gates immutable | LIVE-CODE | `tests/test_truth_labels_v11.py`, OS tests, `_HARD_GATES` on routers |
| 5 | Five action modes | LIVE-CODE | `auto_client_acquisition/full_ops/work_item.py` `ActionMode`; endpoints return modes |
| 6 | Three interfaces | PARTIAL→LIVE | Founder: `GET /api/v1/founder/beast-command-center`. Role: `/api/v1/role-command-v125/*`. Executive: `executive_os` / reporting. Customer: `GET /api/v1/customer-portal/{handle}` |
| 7 | Seven layers | LIVE-CODE | `growth_beast`, `company_growth_beast`, `revops`, `delivery_os`, `proof_to_market`, `compliance_os_v12`, `executive_os` (+ `full_ops` orchestration) |
| 8 | Revenue truth | LIVE-CODE | `auto_client_acquisition/revenue_pipeline/*`, `GET /api/v1/revenue-pipeline/summary`, `GET /api/v1/revops/finance-brief` |
| 9 | Offer ladder (499 pilot, etc.) | LIVE-DOC + CODE | `docs/COMPANY_SERVICE_LADDER.md`; `growth_beast.offer_intelligence.match_offer` |
|10 | Sector priority | LIVE-DOC | `docs/SECTOR_PLAYBOOKS.md` — runtime sector enforcement deferred (no auto-block by vertical without founder policy) |
|11 | Feature acceptance (8 questions) | LIVE-DOC | Constitution Article 11 — PR review process |
|12 | Service acceptance (ICP…blocked claims) | LIVE-DOC | Constitution Article 12 |
|13 | Build order A–G | LIVE-CODE | Phases A–G covered by verifiers + layers; **Phase H scale DEFERRED** until 3 paid pilots (`docs/V12_1_TRIGGER_RULES.md`) |
|14 | Nine roles daily brief | LIVE-CODE | `GET /api/v1/role-command-v125/today/{role}` |
|15 | Quality bar (verifiers) | LIVE-CODE | `scripts/v11_customer_closure_verify.sh`, `v12_full_ops_verify.sh`, `revenue_execution_verify.sh`, `beast_level_verify.sh` |
|16 | Final customer journey (7 outputs in 7 days) | LIVE-CODE-TESTED | Golden loop + portal fields mirror journey; real customer data follows revenue (Phase E) |
|17 | Strategic statement | LIVE-DOC | `docs/DEALIX_OPERATING_CONSTITUTION.md` Article 17 |

## Closure endpoints (this audit round)

- **Founder Beast Command Center:** `GET /api/v1/founder/beast-command-center`
- **Customer portal (8 fields):** `GET /api/v1/customer-portal/{customer_handle}`
- **Golden loop test:** `tests/test_golden_loop_integration.py`

## Deferred by design

- **Phase H — Scale** (3 sectors, retainers, partner diagnostic at scale): trigger = customer evidence per `V12_1_TRIGGER_RULES.md`.
- **Production git_sha match:** operational check `curl https://api.dealix.me/health` after Railway deploy.

## Verdict helper

After merge + deploy:

```bash
bash scripts/beast_level_verify.sh
```

Expect: `DEALIX_BEAST_LEVEL=PASS`, `GOLDEN_LOOP=pass`, `FOUNDER_BEAST_CC=pass`, `CUSTOMER_PORTAL=pass`.
