# DesignOps Skill Catalog

The 15 skills DesignOps OS ships with. Every skill produces an artifact
whose manifest defaults to `safe_to_send=False`. Inputs/outputs are typed
dicts; "Approval" is the human gate before the artifact leaves the founder's
machine.

| # | Skill name | Mode | Scenario | Inputs | Outputs | Approval | Forbidden tokens |
|---|---|---|---|---|---|---|---|
| 1 | `mini_diagnostic` | bilingual | First call after warm intro | `customer_handle`, `pain_points[]` | md + html | founder review | guaranteed, best, #1, free forever, risk-free, 100%, instant, certified |
| 2 | `full_diagnostic` | bilingual | Paid diagnostic deliverable | `customer_handle`, `findings[]`, `next_steps[]` | md + html | founder review | (same 8) |
| 3 | `proposal_page` | bilingual | Scope + price + next step | `tier_id`, `scope[]`, `customer_handle` | md + html | founder review | (same 8) |
| 4 | `pricing_reference` | EN | Internal pricing card | `tier_id` | md | founder-only (never sent to customer) | guaranteed, best, #1 |
| 5 | `invoice_draft` | bilingual | Moyasar-ready draft | `tier_id`, `customer_email`, `amount_sar` | json (handed to admin CLI) | founder + `--allow-live-charge` (which still does not exist) | (same 8) |
| 6 | `proof_pack` | bilingual | Day-7 evidence bundle | `proof_events[]`, `customer_handle` | md + html | founder review | (same 8) |
| 7 | `executive_weekly_pack` | EN | Founder weekly review | `kpis{}`, `wins[]`, `risks[]` | md + html | founder-only | guaranteed, best |
| 8 | `objection_handler` | bilingual | Reply to a known objection | `objection_id` | md | founder review | (same 8) |
| 9 | `warm_intro_message` | bilingual | First-touch DM template | `prospect_handle`, `referrer` | md | founder review | guaranteed, best, #1, free forever, instant |
| 10 | `pilot_recap` | bilingual | End-of-pilot summary | `customer_handle`, `outcomes[]`, `decision_ask` | md + html | founder review | (same 8) |
| 11 | `landing_block` | bilingual | One landing-page section | `block_id`, `copy_ar`, `copy_en` | html | founder review | guaranteed, best, #1, certified, 100% |
| 12 | `case_card` | bilingual | One-pager (anonymized) | `engagement_id` | md + html | founder review (anonymization required) | guaranteed, best, real customer name |
| 13 | `rfp_one_pager` | EN | Bid response | `rfp_id`, `scope[]`, `price_sar` | md + html | founder review | guaranteed, certified, 100% |
| 14 | `internal_decision_pack` | EN | Founder decision memo | `decision_id`, `options[]` | md | founder-only | (none — internal) |
| 15 | `ops_runbook_card` | EN | Recurring-task checklist | `runbook_id`, `steps[]` | md | founder-only | (none — internal) |

## Field notes
- **Mode** — `bilingual` means AR + EN side-by-side; `EN` means English-only
  (founder-only artifacts).
- **Approval** — the founder review banner is rendered into both md and html
  outputs. The banner cannot be removed by a generator; only the founder can
  flip the manifest's `safe_to_send` flag.
- **Forbidden tokens** — see `DESIGNOPS_ARTIFACT_SAFETY.md` for the canonical
  list and bilingual rephrasing examples. "(same 8)" expands to:
  `guaranteed`, `best`, `#1`, `free forever`, `risk-free`, `100%`, `instant`,
  `certified`.

## Coming next (not yet implemented — defer until requested)
| Idea | Why defer |
|---|---|
| `arabic_legal_addendum` | Needs Saudi-counsel review of template language. |
| `roi_calculator_card` | Numbers must be tied to `proof_ledger`, not estimated. |
| `partner_co_branded_pack` | Requires a partner-distribution agreement on file. |
| `multi_customer_aggregate_report` | Needs PDPL-aligned anonymization spec first. |
| `pdf_pack_renderer` | PDF emission deferred (see exporter `NotImplementedError`). |
| `pptx_investor_one_pager` | PPTX emission deferred. |
| `customer_health_score_card` | Needs an agreed scoring model + audit trail. |

These are intentionally not built. Each requires a founder decision before
adding it to the registry.
