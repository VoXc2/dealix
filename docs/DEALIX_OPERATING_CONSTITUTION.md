# Dealix Operating Constitution

> **The single document that governs every decision.** If a feature,
> service, prompt, agent, dashboard, or sale doesn't pass these
> rules, it doesn't ship.

## Article 1 — The Final Definition

```
Dealix is a Saudi-first Self-Growing Company Operating System
that helps companies find better customers, sell smarter,
support faster, deliver with proof, manage financial truth,
and make better daily decisions across every role.
```

Dealix is NOT a chatbot, NOT a dashboard, NOT a CRM, NOT a marketing
agency, NOT an automation tool. It is an operating layer.

## Article 2 — The Golden Loop

```
Market Signal
  → Target Score
  → Offer Match
  → Growth/Sales/Support Action
  → Approval
  → Diagnostic
  → Pilot
  → Delivery
  → Support Insight
  → Proof Event
  → Finance Truth
  → Weekly Executive Decisions
  → Better Targeting
```

Any feature that doesn't serve this loop is **deferred**.

## Article 3 — The Four Laws

### Law 1: Every feature must serve one of four things

```
1. Bring a better opportunity
2. Convert opportunity to revenue
3. Deliver proven value
4. Improve the next decision
```

### Law 2: No growth without proof

```
No proof → no claim
No customer approval → no public case study
No payment/commitment → no revenue
No source → no metric
```

### Law 3: Autonomous Intelligence, Human-Approved Execution

The system analyzes, ranks, drafts, measures, learns autonomously.
External actions (send / charge / publish proof / use logo) require
explicit founder approval.

### Law 4: No V13 before commercial proof

V13 is forbidden until at least one of:
- payment_received
- written_commitment_received
- delivery_session with real customer
- proof_event from real customer

## Article 4 — Hard Gates (NEVER FLIP)

```
NO_LIVE_SEND
NO_LIVE_CHARGE
NO_COLD_WHATSAPP
NO_LINKEDIN_AUTOMATION
NO_SCRAPING
NO_FAKE_PROOF
NO_FAKE_REVENUE
NO_UNAPPROVED_TESTIMONIAL
```

These are immutable. Flipping any requires a dedicated PR + founder
review + safety sign-off.

## Article 5 — Action Modes (the only allowed values)

```
suggest_only
draft_only
approval_required
approved_manual
blocked
```

Any code that uses `auto_send`, `auto_charge`, `auto_scrape`,
`auto_dm`, or any unapproved live action is a **constitutional
violation** and must be reverted.

## Article 6 — The Three Interfaces

Dealix has exactly **3 interfaces**, no more:

1. **Founder Command Center** — for the operator
2. **Customer Company Portal** — for the client (no internals shown)
3. **Role Command Center** — for each role inside a client company
4. **Executive Weekly Brief** — single-page summary

## Article 7 — The Seven Layers

```
Layer 1: Market & Self-Growth (Growth Beast)
Layer 2: Company Service (Company Growth Beast + Phase E kit)
Layer 3: Revenue & Sales (RX revenue_pipeline + RevOps)
Layer 4: Delivery & Support (Delivery OS + Support OS + KB)
Layer 5: Proof & Learning (proof_ledger + proof_to_market)
Layer 6: Compliance & Governance (compliance_os_v12 action_policy)
Layer 7: Executive & Role Command (Executive OS + Role Command v125)
```

V12.5 ships ALL 7 layers as live code. See:
- `docs/BEAST_LEVEL_ARCHITECTURE.md`
- `docs/REVENUE_EXECUTION_OS.md`
- `docs/SECTOR_PLAYBOOKS.md`
- `docs/V12_1_TRIGGER_RULES.md`
- `docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md`

## Article 8 — Revenue Truth

```
Draft invoice ≠ revenue
Verbal interest ≠ revenue
Diagnostic delivered ≠ revenue
Written commitment = commitment (NOT revenue)
Payment evidence (Moyasar/bank) = revenue
```

Enforced by `auto_client_acquisition/revops/payment_confirmation.py`
(evidence required, ≥ 5 chars).

## Article 9 — The 5-Rung Service Ladder

```
Rung 0: Mini Diagnostic       (free / token)
Rung 1: 7-Day Growth Proof    499 SAR
Rung 2: 30-Day Operating      recommended_draft
Rung 3: Monthly Operating     recommended_draft
Rung 4: Partner Co-Branded    after 3 paid pilots
```

Each rung unlocks ONLY on real evidence from the rung below
(see `docs/COMPANY_SERVICE_LADDER.md`).

## Article 10 — Sector Priority

```
Tier 1 (start here):     Marketing agencies, B2B services, Consulting
Tier 2 (after proof):    SaaS, Ecommerce, Real estate, Local services
Tier 3 (after maturity): Healthcare, Education, Logistics, Industrial
```

Codified in `docs/SECTOR_PLAYBOOKS.md`.

## Article 11 — Feature Acceptance Test

Any new feature must answer **YES** to all 8:

```
1. Does it serve growth, revenue, delivery, or proof?
2. Does it have a clear owner role?
3. Does it have a metric?
4. Does it produce proof events?
5. Does it have an action mode?
6. Does it have a risk policy?
7. Does it appear in a command center?
8. Does it improve a daily decision?
```

If any answer is **no**, do not build it.

## Article 12 — Service Acceptance Test

Any new service must include all 12:

```
ICP
Pain
Offer
Inputs
Workflow
Deliverables
Proof
Price
Margin
Support scope
Upsell path
Blocked claims
```

If any field is missing, the service is not ready to sell.

## Article 13 — The Build Order (cannot skip)

```
A. Production Truth          ✅ V11/V12 verifiers PASS
B. Revenue Truth             ✅ RX + RevOps shipped
C. Growth Beast              ✅ V12.5 shipped
D. Company Growth Beast      ✅ V12.5 shipped
E. Role Command              ✅ V12.5 shipped (9 roles)
F. Proof-to-Market           ✅ V12.5 shipped
G. First Revenue (founder)   ⏳ Day 1 Launch Kit ready
H. Scale (after 3 pilots)    deferred
```

## Article 14 — The 9 Roles Daily Brief

Each role gets exactly 3 decisions per day. No more.

```
CEO              → top 3 business decisions
Growth           → segment + content + experiment
Sales            → top 3 deals + objection + offer
Support          → P0 escalations + KB gaps
Customer Success → at-risk + upsell-ready + check-in
Delivery         → today's deliverable + missing inputs
Finance          → cash + commitments + margin
Compliance       → blocked + escalated + consent
Operations       → verifier + incidents + SLA
```

Endpoint: `GET /api/v1/role-command-v125/today/{role}`

## Article 15 — Quality Bar

```
FULL_PYTEST=PASS
V11_VERIFIER=PASS
V12_FULL_OPS_VERIFY=PASS
DEALIX_REVENUE_EXECUTION=PASS
DEALIX_BEAST_LEVEL=PASS
NO_LIVE_*=blocked
NO_FAKE_*=blocked
ARABIC_PRIMARY=pass
```

Anything below this bar is treated as a regression and blocks deploy.

## Article 16 — The Final Test

> "Every company entering Dealix exits within 7 days with:
> 1. A clear diagnostic
> 2. An actionable plan
> 3. Ready messages
> 4. Delivery checklist
> 5. Real Proof Pack
> 6. Executive report
> 7. Clear next decision"

If a company exits with only a dashboard → **system failure**.
If they exit with clarity + execution + proof + decision → **system success**.

## Article 17 — The Strategic Statement

```
Dealix becomes the strongest possible company when its goal is
not "build more features" but "operate one self-sustaining loop":
target → sell → serve → prove → learn → target better.
```

---

This Constitution overrides any prior plan, prompt, or aspiration
that contradicts it. When in doubt, return to Article 1.
