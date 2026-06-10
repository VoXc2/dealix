# Wave 17 — Day 1 Launch Kit (Founder Playbook)

> Wave 17 §35.2.8 — the founder's single-page reference for receiving
> the first real Saudi B2B customer. ≤45 minutes total daily execution.
> Everything else is "look up if needed."
>
> **Use this kit when:** you've signed DPA, DNS records are live,
> Moyasar KYC done (or bank transfer fallback ready), and you're ready
> to start sending warm-intro WhatsApp messages.

## The morning ritual (≤10 minutes)

### 7:30 AM — Run readiness check (1 min)

```bash
bash scripts/dealix_market_launch_ready_verify.sh
```

Expected verdict: `MARKET_LAUNCH_READY=PASS` (or `PARTIAL` with known
founder actions). If `BLOCKED` → resolve before continuing.

### 7:35 AM — Run founder daily brief (1 min)

```bash
python3 scripts/dealix_founder_daily_brief.py --auto-source
```

Read the 5 sections:
1. **Bottleneck Radar** — what's blocking revenue today?
2. **Service Catalog** — 7 offerings priced + KPI committed
3. **Article 13 Status** — `X / 3` paid customers
4. **Hard Gates** — all 8 immutable
5. **Today's Single Action** — ONE sentence; do that.

### 7:40 AM — Send 5 warm-intro WhatsApp messages (5 min)

Open `docs/FIRST_10_WARM_MESSAGES_AR_EN.md` → copy 5 messages tailored
to specific people in your network. Send via personal WhatsApp.

**NEVER** automate. **NEVER** copy-paste blast. Each message:
- Mentions the person by name
- References shared context (event / mutual contact / sector)
- Asks ONE question (book a 30-min diagnostic, OR share `/services.html`)
- Daily cap: 5 messages (Article 4 NO_BLAST)

Log each one:
```bash
python3 scripts/dealix_first10_warm_intros.py add
# (interactive prompt — fills warm_intros.jsonl)
```

### 7:50 AM — Open `/founder-leads.html` (3 min)

URL: `https://dealix.me/founder-leads.html?access=dealix-founder-2026`

Review yesterday's replies + plan today's follow-ups. Use the founder
rules (Wave 7.7) to auto-approve safe messages; everything else
manually approves on `/decisions.html`.

## Throughout the day (≤30 min total)

### Replies arrive

Respond within 30 min business hours. Use templates from
`docs/FIRST_CUSTOMER_SCRIPT_PACK_AR_EN.md` (Wave 11). Log each reply:

```bash
python3 scripts/dealix_first10_warm_intros.py mark-replied
```

### Demo booked?

Send Calendly link. When demo happens:
- Use `docs/WAVE6_REAL_DEMO_RUNBOOK_AR_EN.md` (15-min bilingual)
- After demo: `python3 scripts/dealix_demo_outcome.py`

### Demo → Sprint conversion?

```bash
python3 scripts/dealix_pilot_brief.py \
    --company "Acme Real Estate" \
    --sector real_estate --amount-sar 499
```

Send brief via WhatsApp. Customer pays via bank transfer → log it:

```bash
# Step 1: invoice intent (customer commits)
python3 scripts/dealix_payment_confirmation_stub.py \
    --action invoice-intent-created \
    --customer-handle acme-real-estate

# Step 2: evidence received (customer sends bank screenshot)
python3 scripts/dealix_payment_confirmation_stub.py \
    --action evidence-received \
    --customer-handle acme-real-estate \
    --evidence-note "bank-transfer screenshot received via WhatsApp"

# Step 3: confirm (after you verify the transfer hit your account)
python3 scripts/dealix_payment_confirmation_stub.py \
    --action confirm \
    --customer-handle acme-real-estate
```

🎯 **Article 13 trigger:** `confirmed_revenue_sar` increments only AFTER
step 3. The Founder Daily Brief will reflect this tomorrow.

### Kick off Sprint:

```bash
python3 scripts/dealix_delivery_kickoff.py \
    --company "Acme Real Estate" \
    --service 7_day_revenue_proof_sprint \
    --payment-state-file docs/wave6/live/payment_state.json
```

## The evening shutdown (≤5 minutes)

### 6:00 PM — Mark decisions complete

Open `/decisions.html?access=dealix-founder-2026` → mark approved
messages as sent.

### 6:03 PM — Check artifact enforcer

```bash
python3 scripts/dealix_artifact_enforcer.py --strict --format one-line
```

If any active session is 2+ days without artifact → schedule tomorrow's
delivery.

### 6:05 PM — Queue tomorrow's first 5 warm intros

Open `docs/FIRST_10_WARM_MESSAGES_AR_EN.md` → pick 5 names from the
remaining pool. Pre-draft the messages tonight; send tomorrow morning.

## The weekly review (Friday 4 PM, 30 min)

### Weekly Executive Pack

```bash
python3 scripts/dealix_weekly_executive_pack.py
```

Read for each active customer. Share customer-facing version manually.

### Funnel review

```bash
python3 scripts/dealix_first3_board.py  # or first10_warm_intros.py list
```

Count: intros sent → replies received → demos booked → Sprints closed.

**Target (Week 1):** 25 intros → 10 replies → 4 demos → 1 paid Sprint.

## The pre-launch founder checklist

Before sending the FIRST warm-intro WhatsApp, confirm:

- [ ] **DPA self-execution signed** — `data/wave11/founder_legal_signature.txt` exists
- [ ] **SDAIA registration started** — track in `docs/LEGAL_ENGAGEMENT.md`
- [ ] **DNS records live** — `bash scripts/dealix_dns_verify.py` returns `ready_for_transactional` or better
- [ ] **Bank account ready** — IBAN documented in `docs/MOYASAR_LIVE_CUTOVER.md` (for bank transfer fallback)
- [ ] **Calendly link** — embedded in WhatsApp message templates
- [ ] **Customer portal access token pattern** — `docs/integrations/CUSTOMER_PORTAL_TOKEN_SETUP.md`
- [ ] **5 warm-intro names selected** — listed in `data/wave11/warm_intros.jsonl` (or paper notebook)
- [ ] **`MARKET_LAUNCH_READY=PASS` or PARTIAL** — `bash scripts/dealix_market_launch_ready_verify.sh`

## Hard rules (NEVER violate)

| Rule | Why | What happens if violated |
|---|---|---|
| **No cold WhatsApp** | Article 4 NO_COLD_WHATSAPP | PDPL fine + WhatsApp ban |
| **No more than 5 warm-intros/day** | Article 4 NO_BLAST | Relationship-burning, looks like spam |
| **No live auto-send** | Article 4 NO_LIVE_SEND | safe_send_gateway raises SendBlocked |
| **No live auto-charge** | Article 4 NO_LIVE_CHARGE | Moyasar mode=sandbox until launch |
| **No fake testimonials / proof** | Article 8 NO_FAKE_PROOF | Lose trust + SDAIA risk |
| **No "نضمن" / "guaranteed"** | Article 8 NO_FAKE_REVENUE | Legal liability |
| **No scraping LinkedIn** | Article 4 NO_LINKEDIN_AUTO | Account ban + ToS violation |
| **No publishing case study without signed consent** | Article 4 NO_FAKE_PROOF | Customer relationship destroyed |

## When you receive your first paid customer

1. **Pop the cork** — this is the Article 13 trigger.
2. Run `python3 scripts/dealix_payment_confirmation_stub.py --action confirm`
3. Run `python3 scripts/dealix_delivery_kickoff.py` — Sprint begins.
4. **Day 7 of Sprint:** customer signs consent → run `python3 scripts/dealix_case_study_builder.py --customer-handle <handle> --events <proof_events.jsonl>`
5. **After 3 paid customers:** run `python3 scripts/dealix_customer_signal_synthesis.py` → decide Wave 18 path (Deepen / Expand / Scale).

## Emergency contacts

- **PDPL data-subject request:** see `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`
- **Breach response:** see `docs/PDPL_BREACH_RESPONSE_PLAN.md`
- **Refund:** see `docs/REFUND_SOP.md` (100% within 14 days for Sprint)
- **Lawyer:** see `docs/LEGAL_ENGAGEMENT.md`

## The single most important sentence

> _"After Wave 17, the engineering is ready. The only remaining gate to first paid customer is YOU sending 5 WhatsApp messages and replying within 30 minutes. No more code. No more architecture. The constraint is execution."_

---

_Wave 17 §35.2.8 · Constitution Articles 3, 4, 8, 11, 13 preserved._
_Generated by `scripts/dealix_market_launch_ready_verify.sh` when verdict=PASS._
