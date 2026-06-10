# Dealix — Executive Decision Pack v1

> One-page operational sign-off. Ten decisions, fourteen-day action
> plan, explicit budget envelope, and a Go/No-Go gate. Read in 5
> minutes; sign at the bottom.
>
> **Date:** 2026-05-04
> **Branch:** `claude/service-activation-console-IA2JK` @ `1b8725d`
> **Strategic context:** `docs/STRATEGIC_MASTER_PLAN_2026.md`
> **Closure verdict:** `FIRST_CUSTOMER_READY_DIAGNOSTIC_ONLY`
> **Reviewer:** Sami Assiri (Founder)
> **Author:** Dealix Strategic Plan System

---

## I. The Ten Decisions to Authorize

Each decision has: **the ask**, **the rationale**, **the cost**,
**the risk**, **three options**. Select an option per row by ticking
in §V.

### 🟡 PERIMETER (B-series — unblock the page surface)

**B1 — `roi.html:152` "نضمن استرجاع 100%" refund wording**
- Rationale: Refund guarantee is legitimate, but `نضمن` is on the
  forbidden-claims list. The test surfaced it as `REVIEW_PENDING`.
- Cost of approval: 0 (keep) / 30 min (rephrase)
- Risk of inaction: forbidden-claims sweep stays at "REVIEW_PENDING"
- **Options:** ☐ Keep as-is + APPROVED ☐ Rephrase to "نلتزم باسترجاع 100%" ☐ Drop the refund line entirely

**B2 — `academy.html` "Cold Email Pro — Saudi" course title**
- Rationale: Course teaches cold email, but Dealix's product policy
  forbids cold outreach. Mixed signal to AI engines + buyers.
- Cost of approval: 0 (keep + policy note) / 1 hr (rename to
  "Email Outreach Pro" or drop the course)
- Risk of inaction: brand-honesty erosion; AI may surface contradiction
- **Options:** ☐ Keep + add policy note ☐ Rename to "Email Outreach Pro — Saudi" ☐ Drop the course entirely

**B3 — Next 1–3 pages to author full OG/canonical/twitter:card copy**
- Rationale: 21 advisory SEO gaps; founder picks priority pages
- Cost: 30 min/page (Claude drafts, founder approves)
- Risk: AI engines under-cite Dealix pages without OG
- **Options:** ☐ `pricing.html` + `trust-center.html` + `marketers.html` ☐ Pick a different set ☐ Defer for one more cycle

**B4 — Search/keyword data source**
- Rationale: Phase 4 (search radar) blocks on this. Without a real
  source, every keyword is invented = forbidden.
- Cost: 0 (manually-curated) / ~250 SAR/mo (Ahrefs Lite or SEMrush)
- Risk: low signal on what to write
- **Options:** ☐ Google Search Console (free, KSA-anchor) ☐ Manually-curated lists ☐ Paid tool (Ahrefs/SEMrush)

**B5 — Authorize Phase D (7 safety tests)**
- Rationale: Closure cells `OPERATOR_SAFETY_AR/EN`, `LIVE_GATES_SAFE`
  are `not_runnable` until tests exist. Tests are pure additions
  against existing safety modules.
- Cost: ~3 hours of Claude time
- Risk of inaction: `not_runnable` stays in every closure verdict
- **Options:** ☐ Authorize all 7 ☐ Authorize 3 most critical
  (`test_live_gates_default_false.py`, `test_safe_action_gateway.py`,
  `test_whatsapp_policy.py`) ☐ Defer

### 🟢 STRATEGY (S-series — surfaced by the strategic master plan)

**S1 — Pilot retirement at customer #6 → Growth Starter at 990 SAR**
- Rationale: 499 SAR is a CAC, not a profit product. Cap at 5 paid pilots.
- Cost: 0 (price change applies *after* customer #5)
- Risk of inaction: Dealix becomes a 499-SAR-only company forever
- **Options:** ☐ Approve cap at customer #5 ☐ Cap at customer #10 ☐ No cap until Q4 2026

**S2 — Authorize agency partner outreach (5 names, 30% Y1 rev share)**
- Rationale: Channel 3 in the strategic plan; compounding distribution
- Cost: ~4 founder hours + 3 hours Claude (drafts)
- Risk of inaction: distribution stays founder-bottlenecked
- **Options:** ☐ Authorize 5 names ☐ Authorize 2 names (test first) ☐ Defer to month 4

**S3 — Outcome-rider experiment after first Executive Growth OS month-3**
- Rationale: 10% bonus on proven uplift over baseline. Aligns
  incentives without "guaranteed revenue" claim.
- Cost: 0 until first Executive customer hits month 3
- Risk: pricing complexity if mishandled
- **Options:** ☐ Approve for month-3 trigger ☐ Defer until 3 Executive customers ☐ Decline (keep flat pricing)

**S4 — Compliance-tier premium (+30% for DPO-shareable PDPL audit)**
- Rationale: Procurement/compliance teams have budget; marketing teams don't.
- Cost: 1 day Claude work to wire `cross_border_restriction` +
  `audit_trail` into a single export endpoint
- Risk: low; pure upsell
- **Options:** ☐ Approve as add-on SKU ☐ Bundle into Executive Growth OS Plus ☐ Defer

**S5 — First service to flip Live (recommendation: `lead_intake_whatsapp`)**
- Rationale: Validates the 8-gate process publicly. Currently Partial;
  needs OTel traces + abuse-boundary test (~6 hours of Claude work).
- Cost: 6 hours Claude + founder approval at the gate
- Risk: low; reversible (can flip back to Partial)
- **Options:** ☐ `lead_intake_whatsapp` ☐ `consent_required_send` ☐ `audit_trail` ☐ Defer (no Live until first paid customer)

---

## II. Fourteen-Day Action Plan (compressed from 90-day Part VI)

Each row: **#**, **action**, **owner**, **exit criterion**, **deadline**.

| # | Action | Owner | Exit Criterion | Deadline |
|---|---|---|---|---|
| 1 | Sign this Decision Pack (§V) | Founder | Signature block filled | Day 1 |
| 2 | Open PR `claude/service-activation-console-IA2JK` → main | Founder or Claude | PR exists, CI green | Day 2 |
| 3 | Merge to main + Railway redeploy | Founder | `/health` reports real `git_sha` | Day 3 |
| 4 | Verify all 3 self-growth endpoints reachable on prod | Claude | 200 OK across `status`, `service-activation`, `seo/audit` | Day 3 |
| 5 | Apply B1 + B2 decisions (rephrase or APPROVE) | Founder + Claude | `tests/test_landing_forbidden_claims.py` updated | Day 4 |
| 6 | Apply B3 (1–3 pages get full OG copy) | Claude | `tests/test_seo_audit.py` ADVISORY_EXEMPT shrinks by 1–3 | Day 5 |
| 7 | Author Phase D tests if B5 = Approve | Claude | Test count rises 32 → 35–39 (3 or 7 tests added) | Day 6 |
| 8 | Pick 5 warm-intro target companies | Founder | Names + contact channels in shared doc | Day 7 |
| 9 | Draft bilingual Diagnostic intake form | Claude | Form pasted in chat or Notion | Day 8 |
| 10 | Send 5 manual warm intros (founder's own channels) | Founder | 5 sent | Day 9 |
| 11 | Build first ProofEvent ledger table (V.B #1 of strategy) | Claude | Migration shipped + table reachable via API | Day 10 |
| 12 | Run free Diagnostic on 1–2 respondents | Founder + Claude | Diagnostic doc delivered to ≥1 prospect | Day 12 |
| 13 | Convert 1 to Growth Starter Pilot 499 SAR | Founder | Verbal + written commit | Day 14 |
| 14 | If S2 = Approve: send 5 agency partner pitches | Founder | 5 sent | Day 14 |

**End-of-14-day target:** 1 paid pilot (or written commit) + branch
deployed + at least 3 closure cells flipped from `not_runnable` to `pass`.

---

## III. Budget Envelope (this 14-day window)

| Item | Range | Notes |
|---|---:|---|
| Railway hosting (current) | 0 SAR | already paid |
| LLM API spend (Groq + Anthropic test calls) | < 50 SAR | rate-limited; multi-provider router falls back |
| Domain renewals / cert | 0 SAR | not due |
| Search tool (B4 if paid option) | 0–250 SAR | only if Ahrefs Lite chosen |
| Ad spend | 0 SAR | NOT authorized this window |
| Founder time (delivery + sales) | ~30 hrs | the only real cost |
| Claude time (this window's Phase C/D/F1 work) | covered | already in plan |

**Hard cap:** 300 SAR cash + 30 founder hours over 14 days. Anything
above this requires a separate authorization.

---

## IV. Go / No-Go Gate (Day 14 review)

Apply the rules from `docs/STRATEGIC_MASTER_PLAN_2026.md` Part X.

**GO (continue 90-day plan):** any of these is true on Day 14:
- ≥1 paid Pilot (Moyasar invoice paid OR written commit)
- ≥1 active prospect in Diagnostic delivery (delivered, awaiting decision)
- ≥1 agency partner intro call scheduled

**HOLD (extend 14-day window by 7 days):** all of:
- Branch deployed + endpoints green
- ≥3 warm intros responded
- 0 PDPL violations / 0 unsafe live actions

**NO-GO (re-plan):** any of these:
- Production deploy failed and not recoverable in Day-15 fix window
- Any `*_ALLOW_LIVE_*` flag flipped to True without explicit founder
  ticket
- Any safety test went from `pass` to `fail` (real regression)
- Customer concentration risk: a single warm intro is now >60% of
  expected first-month revenue

---

## V. Approval Block

**To authorize this Decision Pack, fill below and commit (or reply
to chat with the same content).**

```
B1 — roi.html refund wording:        ☐ Keep+APPROVED  ☐ Rephrase  ☐ Drop
B2 — academy "Cold Email Pro":       ☐ Keep+note       ☐ Rename    ☐ Drop
B3 — pages for full OG copy:         ☐ pricing+trust+marketers   ☐ other: ____   ☐ Defer
B4 — search/keyword data source:     ☐ GSC (free)      ☐ Manual    ☐ Paid tool
B5 — Phase D safety tests:           ☐ All 7           ☐ 3 critical only  ☐ Defer
S1 — Pilot retirement cap:           ☐ At customer #5  ☐ At customer #10  ☐ No cap
S2 — Agency partner outreach:        ☐ 5 names         ☐ 2 names   ☐ Defer
S3 — Outcome rider:                  ☐ Approve         ☐ Defer     ☐ Decline
S4 — Compliance premium (+30%):      ☐ Add-on SKU      ☐ Bundle    ☐ Defer
S5 — First service to flip Live:     ☐ lead_intake_whatsapp   ☐ consent_required_send   ☐ audit_trail   ☐ Defer

Budget envelope acknowledged:        ☐ Yes (≤ 300 SAR + 30 founder hours / 14 days)

14-day plan acknowledged:            ☐ Yes (rows 1–14 in §II)

Go/No-Go gate acknowledged:          ☐ Yes

Hard rules re-acknowledged
(Part XI of strategic master plan): ☐ Yes
```

**Signed:** _______________________  **Date:** _____________

**Sami Assiri, Founder**

---

## VI. What Happens Immediately Upon Sign-Off

The instant this is signed (committed with selections filled):

1. Claude opens a PR with this Decision Pack as its body, plus the
   branch's 5 commits as its diff.
2. Per the **B1+B2** selections, Claude updates
   `tests/test_landing_forbidden_claims.py` (changes `REVIEW_PENDING`
   reasons or rephrases the strings — depending on selection).
3. Per **B3**, Claude adds canonical/OG/twitter:card to the chosen
   1–3 pages and shrinks `ADVISORY_EXEMPT` correspondingly.
4. Per **B5**, Claude authors the Phase D tests (3 or 7 depending
   on selection) — strictly *xfail* where a runtime safety check is
   missing rather than fake-green.
5. Claude builds the ProofEvent ledger table (action #11).
6. Per **S2**, Claude drafts 5 partner-pitch emails (Arabic + English
   secondary), waiting for founder approval before sending.
7. Per **S5**, Claude opens a sub-issue: "Flip `lead_intake_whatsapp`
   to Live — checklist of remaining 8-gate tasks."

Anything **not** authorized stays untouched. No silent action.

---

## VII. What Stays NOT Authorized (no matter what is selected above)

Even with full sign-off, the following remain blocked until separate
written authorization:

- ❌ Flipping `whatsapp_allow_live_send=True`
- ❌ Adding `MOYASAR_ALLOW_LIVE_CHARGE` (or any `*_ALLOW_LIVE_*` flag)
- ❌ Sending any external message (email/WhatsApp/SMS) on a customer's behalf
- ❌ Charging any card automatically (manual Moyasar invoice link only)
- ❌ Scraping any source / cold-WhatsApping / LinkedIn DM automation
- ❌ Publishing customer names without written consent
- ❌ Marking any service Live in the YAML without an explicit `gates:`
  block AND on-disk tests AND founder approval at the gate
- ❌ Generating low-value AI pages at scale
- ❌ Changing pricing beyond the S1 cap (no other price moves)

---

## VIII. Tracking

When this is signed and applied, the closure verdict block in
`docs/MASTER_CLOSURE_EVIDENCE_TABLE.md` will update as follows
(projected):

| Cell | Today | After 14 days |
|---|---|---|
| `DEALIX_MASTER_VERDICT` | `FIRST_CUSTOMER_READY_DIAGNOSTIC_ONLY` | `FIRST_CUSTOMER_READY_REALISTIC` if pilot lands; same otherwise |
| `PROD_GIT_SHA` | `unknown` | `<real commit SHA>` |
| `OPERATOR_SAFETY_AR/EN` | `not_runnable` | `pass` (3 or 7 tests) or `xfail` w/ TODO |
| `LIVE_GATES_SAFE` | `pass` | `pass` (re-asserted by `test_live_gates_default_false.py`) |
| `OUTREACH_GO` | `no` | `manual_warm_only` |
| `FIRST_CUSTOMER_SCOPE` | `diagnostic_only` | `diagnostic_or_first_pilot` |
| `BLOCKERS` | 4 listed | reduced to ≤1 |

End of pack.
