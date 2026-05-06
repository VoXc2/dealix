# Revenue Execution OS — V12 mapped to first paid customer

> Single doc that converts the existing V12 9-OS stack into a daily
> revenue routine. Every stage cites the V12 file/endpoint that
> implements it. NO new modules.

## The full lead → revenue flow

```
Warm intro
  └→ Consent-aware intake
      └→ Mini Diagnostic
          └→ Founder approval
              └→ Pilot offer (499 SAR)
                  └→ Manual payment OR written commitment
                      └→ Delivery session (7 days)
                          └→ Support handling
                              └→ Proof events (real, never fabricated)
                                  └→ Proof Pack (internal_only by default)
                                      └→ Customer review call
                                          └→ Upsell OR referral
                                              └→ Weekly learning
                                                  └→ V12.1 trigger (only if real revenue)
```

## Per-stage mapping (V12 modules → revenue stage)

| # | Stage | Owner | V12 module / endpoint | Action mode | Done condition | Failure / escalation |
|---|---|---|---|---|---|---|
| 1 | Warm intro selection | founder | `scripts/dealix_first10_warm_intros.py` (RX, NEW) | `suggest_only` | 10 placeholders in `docs/phase-e/live/` | None — re-pick |
| 2 | Consent intake | founder | `auto_client_acquisition/customer_data_plane/consent_registry.py` | `approval_required` | consent recorded | escalate if customer asks delete/export |
| 3 | Mini Diagnostic | founder | `scripts/dealix_diagnostic.py` (V11) | `draft_only` | bilingual MD generated | `insufficient_evidence` → flag |
| 4 | Founder approval | founder | manual review of draft | `approval_required` | founder edits + approves | reject → re-draft |
| 5 | Pilot offer | founder | `docs/phase-e/05_PILOT_499_OFFER.md` (V11) + `dealix_invoice.py --dry-run` | `draft_only` | offer copy in customer's hands | escalate if guarantee request |
| 6 | Payment / commitment | founder | `dealix_invoice.py` (test-mode) OR bank transfer | `approved_manual` | funds confirmed OR signed commitment | NEVER mark paid without evidence |
| 7 | Delivery session | founder | `POST /api/v1/delivery-os/create-session` (V12) | `approval_required` | session in `in_progress` | block if registry missing |
| 8 | Day-1 opportunities | founder | `POST /api/v1/growth-os/daily-plan` (V12) | `draft_only` | 10 ranked sent to customer | re-rank if no fit |
| 9 | Day-2 message drafts | founder | `POST /api/v1/growth-os/outreach-draft` (V12) | `draft_only` | drafts approved | block any cold-channel request |
| 10 | Day-3 manual sends | founder | manual via WhatsApp/email | `approved_manual` | logged in customer's notes | NEVER auto-send |
| 11 | Day-4 follow-up plan | founder | derived from `customer_inbox_v10` SLA | `draft_only` | calendar in customer's hands | — |
| 12 | Day-5 risk note | founder | `POST /api/v1/customer-data/action-check` per planned action | per V12 `action_policy` | risk note ≤ 3 items | block if PDPL hit |
| 13 | Inbound support | founder | `POST /api/v1/support-os/classify` + `/draft-response` (V12) | `draft_only` or `approval_required` | reply approved + sent | mandatory escalate: refund/payment/privacy/angry/security/guarantee/cold-WhatsApp |
| 14 | Proof events | founder | `dealix_proof_pack.py` (V11) — log JSONL | `approved_manual` | event in `docs/proof-events/<slot>.json` | NEVER fabricate |
| 15 | Day-6 Proof Pack draft | founder | `dealix_proof_pack.py` | `approval_required` | draft Markdown, `audience: internal_only` | empty pack ≠ failure (honest) |
| 16 | Day-7 review call | founder | manual 30-min | manual | feedback recorded | refund decision per `payment_policy_ar_en.md` |
| 17 | Upsell decision | founder | `POST /api/v1/sales-os/objection-response` + `/meeting-prep` (V12) | `suggest_only` | next step chosen | no white-label before 3 paid pilots |
| 18 | Health score | founder | `POST /api/v1/customer-success-os/health-score` (V12) | `suggest_only` | 0–100 + band | unknown stays unknown |
| 19 | Partnership ask | founder | `POST /api/v1/partnership-os/fit-score` (V12) | `draft_only` | partner motion picked | no revenue-share without referral data |
| 20 | Weekly learning | founder | `GET /api/v1/self-improvement-os/weekly-learning` (V12) | `suggest_only` | 3 backlog items | no auto-PR |
| 21 | Daily founder routine | founder | `GET /api/v1/full-ops/daily-command-center` (V12) | read-only | top-3 decisions seen | re-run if degraded |

## The single morning command (replaces 9 dashboards)

```bash
python scripts/dealix_phase_e_today.py
curl -s https://api.dealix.me/api/v1/full-ops/daily-command-center | jq '.today_top_3_decisions, .next_best_actions'
```

## Truth-label gates (cannot be silently flipped)

From `docs/phase-e/00_GO_NO_GO.md` (V11 — locked by `tests/test_truth_labels_v11.py`):

```
PRODUCTION_READY = yes
PHASE_E_GO = yes
FIRST_CUSTOMER_READY = yes_for_warm_intro_and_diagnostic
PAID_PILOT_READY = yes_manual_payment_only
PAID_BETA_READY = no_until_payment_or_written_commitment
REVENUE_LIVE = no_until_real_money_or_signed_commitment
LIVE_SEND_READY = no
LIVE_CHARGE_READY = no
LINKEDIN_AUTOMATION_READY = no
COLD_WHATSAPP_READY = never
```

## Revenue truth (V12 + RX)

A pipeline stage advances ONLY on real evidence:

| Stage | Required evidence | Counts as revenue? |
|---|---|---|
| `warm_intro_selected` | placeholder slot picked | no |
| `message_drafted` | draft in `dealix_diagnostic` output | no |
| `founder_sent_manually` | founder confirms send | no |
| `replied` | screenshot in founder's vault | no |
| `diagnostic_delivered` | bilingual MD shared | no |
| `pilot_offered` | offer copy sent | no |
| `commitment_received` | signed/written email from customer | **partial** (counts toward `commitment` not `revenue`) |
| `payment_received` | Moyasar dashboard OR bank statement | **YES** |
| `delivery_started` | `delivery-os/create-session` returns `in_progress` | — |
| `delivered` | day-7 outputs sent | — |
| `proof_pack_delivered` | pack sent + customer ack | — |
| `closed_won` | invoice fully reconciled + customer renews/upsells | — |
| `closed_lost` | refund issued OR customer goes silent ≥ 14 days | — |

**`REVENUE_LIVE`** flips from `no_until_real_money_or_signed_commitment` to `yes` ONLY when at least one customer reaches `payment_received` AND the founder approves the flip in a dedicated PR.

## What this doc forbids

- ❌ Counting a draft invoice as revenue
- ❌ Counting a verbal "yes" without written confirmation as commitment
- ❌ Skipping diagnostic and going straight to pilot
- ❌ Skipping pilot and going straight to "custom engagement"
- ❌ Public mention of customer name without signed permission
- ❌ Building V13 before at least 1 customer reaches `payment_received`
