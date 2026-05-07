# Dealix — Operational Readiness Playbook (Wave 4 integrated)

**Date:** 2026-05-07
**Audience:** founder + CSM
**Status:** post-Wave-4 integration upgrade

---

## 0. Daily verification

```bash
# 30-second health check
bash scripts/integration_upgrade_verify.sh
bash scripts/full_ops_10_layer_verify.sh
bash scripts/customer_experience_audit.sh
```

Acceptance:
- `INTEGRATION_UPGRADE=PASS`
- `DEALIX_FULL_OPS_10_LAYER_VERDICT=PASS`
- `CUSTOMER_EXPERIENCE_AUDIT=PASS`

If any FAIL — stop, investigate, do NOT push to production.

---

## 1. Run all tests

```bash
python3 -m compileall api auto_client_acquisition db scripts
python3 -m pytest -q --no-cov
```

Wave 3 + Wave 4 baseline: 60 + 132 = 192+ tests must pass.

---

## 2. Read the Full-Ops Score

```bash
curl -s http://localhost:8000/api/v1/full-ops-radar/score | jq .
```

Look at `readiness_label`:
- **Full Ops Ready (90-100)** — every layer green; you can sell aggressively
- **Customer Ready with Manual Ops (75-89)** — most layers green; manual ops fill gaps
- **Diagnostic Only (60-74)** — only do diagnostics, no Sprint or Partner yet
- **Internal Only (<60)** — internal use only, do NOT sell

Interpret `breakdown` to see which layer is missing weight.

---

## 3. Use the Weakness Radar

```bash
curl -s "http://localhost:8000/api/v1/full-ops-radar/weaknesses?customer_handle=acme" | jq .
```

Each weakness has:
- `severity` (low / medium / high / critical)
- `blocker` (true/false)
- `reason_ar` + `reason_en`
- `fix_ar` + `fix_en`
- `owner_role` (founder / csm_or_founder / system)

Critical + blocker=true items must be addressed before customer-facing actions.

---

## 4. Demo the Executive Command Center

For a prospect:
- Browser → `https://dealix.me/executive-command-center.html` (DEMO state)
- After they sign up: `?org=<handle>` (PRE-LAUNCH)
- After they activate: `?org=<handle>&access=<token>` (LIVE)

Show the founder how all 15 sections compose into one screen:
1. Executive summary
2. Full-Ops Score
3. Today's 3 Decisions
4. Revenue Radar
5. Sales Pipeline
6. Growth Radar
7. Partnership Radar
8. Support Inbox
9. Delivery Operations
10. Finance State
11. Proof Ledger
12. Risk & Compliance
13. Pending Approvals
14. WhatsApp Decision Preview
15. Degraded Sections (if any)

---

## 5. Demo the Customer Portal

```
https://dealix.me/customer-portal.html             → DEMO
https://dealix.me/customer-portal.html?org=acme    → PRE-LAUNCH
https://dealix.me/customer-portal.html?org=acme&access=<token>  → LIVE
```

Walk the customer through:
- 8 sections (constitutional)
- enriched_view: ops_summary + sequences + radar_today + digest_weekly + digest_monthly + service_status_for_customer + (Wave 4) full_ops_score + weaknesses_summary + next_3_decisions + support_summary + payment_state + proof_summary + approval_summary + executive_command_link

---

## 6. Use the WhatsApp Decision Bot internally

The bot is internal-admin only. It NEVER sends to customers.

```bash
# Today's status
curl -s -X POST http://localhost:8000/api/v1/whatsapp-decision/brief \
  -H 'Content-Type: application/json' \
  -d '{"customer_handle": "acme"}' | jq .

# Parse a Saudi command
curl -s -X POST http://localhost:8000/api/v1/whatsapp-decision/command \
  -H 'Content-Type: application/json' \
  -d '{"text": "وش أهم 3 قرارات؟"}' | jq .
```

Supported commands:
- وش الوضع اليوم؟
- وش أهم 3 قرارات؟
- وش الصفقات المتأخرة؟
- وش الدعم المفتوح؟
- وش المخاطر؟
- جهز رد للعميل
- اعتمد الرد
- صعّد التذكرة
- أعطني التقرير الأسبوعي

The bot blocks any unsafe command (broadcast, cold WhatsApp, purchased lists) with an Arabic explanation.

---

## 7. First real customer

```bash
# Create the leadops record
curl -X POST http://localhost:8000/api/v1/leadops/run -d '{...}'

# Build the brain
curl -X POST http://localhost:8000/api/v1/customers/{handle}/brain/build

# Start a service session
curl -X POST http://localhost:8000/api/v1/service-sessions/start -d '{...}'

# Receive payment (manual evidence first)
curl -X POST http://localhost:8000/api/v1/payment-ops/manual-evidence -d '{...}'
curl -X POST http://localhost:8000/api/v1/payment-ops/confirm -d '{...}'

# Kickoff delivery
curl -X POST http://localhost:8000/api/v1/payment-ops/{id}/kickoff-delivery

# Record proof events as work completes
curl -X POST http://localhost:8000/api/v1/proof-ledger/events -d '{...}'

# At end: build case study (only after consent signed)
curl -X POST http://localhost:8000/api/v1/case-study/build -d '{...}'
```

---

## 8. What stays MANUAL

- Every external send (WhatsApp / Email / LinkedIn / call)
- Payment confirmation (founder uploads evidence + flips state)
- Case study consent signature (customer signs explicitly)
- LinkedIn outreach (NO automation, never)
- Customer escalations (founder reviews each P0 ticket personally)

---

## 9. What must NEVER be automated yet

- WhatsApp customer outbound (NO_LIVE_SEND gate)
- Gmail live send (NO_LIVE_SEND gate)
- LinkedIn anything (NO_LINKEDIN_AUTO gate)
- Moyasar live charge (NO_LIVE_CHARGE gate)
- Scraping (NO_SCRAPING gate)
- Cold WhatsApp (NO_COLD_WHATSAPP gate)
- Fake proof events (NO_FAKE_PROOF gate)
- Fake testimonials (Article 8)

---

## 10. When to consider next integrations

Use this decision matrix per integration:

| Integration | Trigger condition | What it adds | Priority |
|---|---|---|---|
| **HubSpot** | Customer requests CRM sync | Bidirectional contact + deal sync | Low — only if asked |
| **Google Sheets** | Founder needs custom reports | Live data export to sheets | Medium |
| **Chatwoot** | First Partner customer needs full support inbox | Self-hosted shared inbox | Medium |
| **Langfuse** | LLM costs exceed 500 SAR/month or quality drops | Trace + cost + eval observability | High when triggered |
| **Qdrant** | After 5+ paid customers (semantic memory needed) | Vector search across brain + proof | Low until then |
| **OpenTelemetry** | Need cross-system distributed traces | Standard traces/metrics/logs | Low until SLA matters |
| **Cal.com** | Founder calendar overflow | Per-customer kickoff scheduling | Medium |
| **Moyasar live** | First confirmed paid pilot | Live charge path (DEALIX_MOYASAR_MODE=live env) | High when first pilot signs |

DO NOT pre-install any of these. Each requires:
1. A named customer with a real need
2. A test that proves the integration works
3. A rollback plan

---

## 11. GO / NO-GO checklist (customer-facing launch)

Before sending the URL to a real prospect:

### MUST be GREEN:
- [ ] `bash scripts/integration_upgrade_verify.sh` → INTEGRATION_UPGRADE=PASS
- [ ] `bash scripts/full_ops_10_layer_verify.sh` → DEALIX_FULL_OPS_10_LAYER_VERDICT=PASS
- [ ] `bash scripts/customer_experience_audit.sh` → CUSTOMER_EXPERIENCE_AUDIT=PASS
- [ ] `python3 -m pytest -q --no-cov` → 0 failures
- [ ] Manual smoke at `/customer-portal.html` (DEMO + signed-up + LIVE)
- [ ] Manual smoke at `/executive-command-center.html` (DEMO + signed-up + LIVE)
- [ ] Full-Ops Score ≥ 90 → readiness label is "Full Ops Ready"

### MUST be MANUAL:
- [ ] Founder ready to handle WhatsApp inbound personally
- [ ] Moyasar bank-transfer instructions ready (live charge OFF)
- [ ] First customer's diagnostic call scheduled

### NO-GO (do not launch if any true):
- [ ] Any `critical` weakness from Weakness Radar
- [ ] `customer-portal.html` shows DEMO when org=ACTIVE
- [ ] Forbidden token detected in any customer-facing page
- [ ] Any internal term leaked to customer
- [ ] Any test failure

---

## 12. Emergency contacts

- Production prod: `https://api.dealix.me/`
- Health: `GET /api/v1/health`
- Master verifier: `bash scripts/integration_upgrade_verify.sh`
- Rollback: `git revert <last-commit>` then `git push`
