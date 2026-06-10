# Phase E — GO / NO-GO truth labels

These labels are the **single source of truth** for what Dealix is
allowed to do today. Each label is a contract: tests assert the value
never silently changes. If you want to change one, change the test +
the label in the same PR.

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

## What each label means

| Label | Yes means | No means |
|---|---|---|
| `PRODUCTION_READY` | `/health` returns 200 with valid `git_sha`; smoke ≥ 27/28 | redeploy |
| `PHASE_E_GO` | Founder may begin warm intros today | wait for green |
| `FIRST_CUSTOMER_READY` | Diagnostic + draft message ready; Pilot quote-only | — |
| `PAID_PILOT_READY` | Manual / test-mode payment fallback works (no live charge) | — |
| `PAID_BETA_READY` | At least 1 customer signed + paid + delivered | block all "PAID_BETA" claims publicly |
| `REVENUE_LIVE` | Public claim of revenue is permitted | NO public revenue claims, NO public ROI claims |
| `LIVE_SEND_READY` | WhatsApp/email/LinkedIn live send authorized | DRAFT-ONLY content |
| `LIVE_CHARGE_READY` | Moyasar live charge enabled | TEST-MODE / MANUAL only |
| `LINKEDIN_AUTOMATION_READY` | Out-of-scope; will not be built | manual only |
| `COLD_WHATSAPP_READY` | Will never be enabled (PDPL + brand) | warm-intro-only forever |

## How to flip a label safely

1. Open a PR titled `chore(go-no-go): flip <LABEL> to <yes/no>`.
2. Edit this file.
3. Edit `tests/test_truth_labels_v11.py` to match.
4. Provide the evidence in the PR description: smoke result, signed
   customer agreement, etc.
5. NEVER flip `LIVE_SEND_READY` or `LIVE_CHARGE_READY` to yes without
   founder + safety review.
6. NEVER flip `COLD_WHATSAPP_READY` — that label is hard-pinned `never`.

## Bilingual summary

**Arabic**:
كل حالة من الاحتياجات أعلاه ينعكس في اختبار. الفلاج لا ينقلب صدفة. لا
نطلق رسائل حيّة، لا نسحب رسوم حيّة، ولا نرسل واتس بارد. كل خطوة عبر
موافقة المؤسس.

**English**:
Each truth label above is mirrored in a unit test. No live send, no
live charge, no cold WhatsApp. Every external action passes through
founder approval.
