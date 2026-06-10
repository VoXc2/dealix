# Dealix v7 — Revenue Factory Launch Board

> The single page the founder lives on. Manual outreach only.
> Bilingual. PDPL-compliant. **No automation.**

**Date opened:** 2026-05-05
**Owner:** Founder

---

## 1. Launch objective

Convert **3 paying Pilots within 21 days** through warm intros only,
proving the AI Workforce model and the 499 SAR price point before
flipping to the post-pilot pricing ladder (Decision Pack §S1).

## 2. ICP (Ideal Customer Profile)

| Dimension | Target |
|---|---|
| Geography | KSA (Riyadh / Jeddah / Dammam) |
| Vertical | B2B services, B2B SaaS, agencies, training/consulting |
| Headcount | 5–50 employees |
| Decision-maker | Founder is the buyer |
| Existing pipeline | ≥ 1 inbound channel (WA / email / LinkedIn warm) |
| Pain | Lost replies after peak hours, no Proof Pack, scattered follow-up |
| Budget | Discretionary 499 SAR for "growth experiment" |

If a prospect doesn't tick ≥ 5 boxes → defer to Diagnostic only.

## 3. First 10 Warm Prospects (placeholders only)

Founder fills these in a private note (NOT here — PDPL).

| # | Placeholder | Vertical | Source | Status | Next action |
|---|---|---|---|---|---|
| 1 | Prospect-1 | b2b_services | warm intro | not_contacted | book Diagnostic |
| 2 | Prospect-2 | b2b_saas | inbound | not_contacted | book Diagnostic |
| 3 | Prospect-3 | agency | warm intro | not_contacted | partner pitch |
| 4 | Prospect-4 | training | founder network | not_contacted | book Diagnostic |
| 5 | Prospect-5 | b2b_services | warm intro | not_contacted | book Diagnostic |
| 6 | Prospect-6 | local_services | inbound | not_contacted | book Diagnostic |
| 7 | Prospect-7 | b2b_saas | warm intro | not_contacted | book Diagnostic |
| 8 | Prospect-8 | agency | warm intro | not_contacted | partner pitch |
| 9 | Prospect-9 | training | founder network | not_contacted | book Diagnostic |
| 10 | Prospect-10 | b2b_services | inbound | not_contacted | book Diagnostic |

## 4. First 3 Diagnostics (live)

Tracked separately in `docs/FIRST_3_CUSTOMER_LOOP_BOARD.md`. Launch
board summary:

| Slot | Stage | Next action |
|---|---|---|
| A | not_started | book Diagnostic call |
| B | not_started | book Diagnostic call |
| C | not_started | book Diagnostic call |

## 5. Service ladder (price-locked)

| Rung | Service | Price | When to recommend |
|---|---|---|---|
| 0 | Free Diagnostic | 0 SAR | first call always |
| 1 | Growth Starter Pilot | 499 SAR | qualified prospect, 7-day commitment |
| 2 | Data to Revenue | 1,500–3,000 SAR | existing list/CRM, 14-day project |
| 3 | Executive Growth OS | 2,999 SAR/mo | post-Pilot upsell |
| 4 | Partnership Growth | 3,000–7,500 SAR | agency or sell-through |
| 5 | Compliance/Trust Pack | +30% | regulated buyer (banks, healthcare) |
| 6 | Custom Control Tower | TBD | enterprise (>200 employees) |

Locked until customer #5 paid. See `docs/PRICING_AND_PACKAGING_V6.md`.

## 6. Manual outreach rules

- ❌ NO LinkedIn DM automation tools
- ❌ NO mass WhatsApp (cold or warm)
- ❌ NO purchased / scraped contact lists
- ❌ NO bulk email tools
- ❌ NO posting AI-generated bulk content
- ✅ One-by-one manual sends, founder-typed
- ✅ 48-hour follow-up rule (one touch only)
- ✅ Bilingual (Arabic primary)

Templates: `docs/FIRST_10_WARM_MESSAGES_AR_EN.md` + `docs/V7_FIRST_10_WARM_OUTREACH_PACK.md`.

## 7. Daily founder routine (≤ 30 min)

1. Open the morning digest email (sent 7AM KSA via `daily_digest.yml`)
2. `make v5-status` — confirm all gates BLOCKED
3. Review pending approvals: `curl /api/v1/approvals/pending`
4. Move 1 prospect forward
5. Record any ProofEvent from yesterday's delivery

## 8. Weekly review routine (Monday, ≤ 60 min)

1. `curl /api/v1/executive-report/weekly` — read the bilingual report
2. Update the slot board (this file + `FIRST_3_CUSTOMER_LOOP_BOARD.md`)
3. Sign ≤ 2 of the 10 Decision Pack items
4. Capture any new objection in `docs/OBJECTION_HANDLING_V6.md`
5. Decide which prospect to move forward this week

## 9. Proof collection plan

- Every Pilot delivery day → record a `delivery_task_completed` ProofEvent
- Day 7 → `python scripts/dealix_proof_pack.py --customer-handle <slot>`
- Founder reviews + signs the Pack manually
- Customer signs publication consent (or doesn't — Pack stays internal)

## 10. Pricing learning plan

After each Pilot:
1. What price would the customer pay AGAIN if forced to choose?
2. What price would the customer recommend to a peer?
3. Would they pay 990 SAR if 499 retired?

These three answers feed Decision Pack §S1.

## 11. Risk register

| Risk | Likelihood | Severity | Mitigation |
|---|---|---|---|
| Production stays on stale build | high | medium | Founder triggers Railway redeploy |
| First Pilot fails to deliver | medium | high | Founder reviews each draft before send; SLA documented |
| Cost overrun on AI agents | low | medium | `cost_guard` enforces per-run budget |
| PII leak in proof pack | low | high | Redaction-on-write tested; export anonymizes by default |
| Forbidden phrase regresses into copy | low | high | Pre-commit hooks + CI test |
| Customer asks for cold outreach | medium | medium | Politely decline; offer Diagnostic + 90-day nurture |

## 12. Go / No-Go gates

| Gate | Required for | Status |
|---|---|---|
| Production redeploy complete | Founder dashboard URL works | ⏳ |
| Full pytest green | Every layer healthy | ✅ |
| Forbidden-claims sweep clean | Public copy honest | ✅ |
| First Pilot SLA documented | Customer expectations clear | ✅ (in YAML) |
| Phase E playbook reviewed by founder | Founder confidence | ✅ (doc exists) |

If all 5 gates pass → `OUTREACH_GO=yes` → begin warm intros.

— Revenue Factory Launch Board v1.0 · 2026-05-05 · Dealix
