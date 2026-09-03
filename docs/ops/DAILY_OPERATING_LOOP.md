# Dealix — Daily Operating Loop

**Purpose:** run one governed company loop every day while keeping internal automation active and external authority human-controlled.  
**Cadence:** agents may work continuously on internal, reversible tasks; external effects remain approval-first.  
**Canonical objective:** verified economic movement per founder minute, cost, and risk.

## Non-negotiable operating law

`Research ≠ relationship` · `public contact ≠ consent` · `engagement ≠ buyer intent` · `draft ≠ sent` · `quote ≠ invoice` · `invoice ≠ payment` · `synthetic ≠ customer proof`

No automated LinkedIn scraping, browser bot, connection/message automation, cold WhatsApp, mass email, public publishing, payment, or production mutation.

## Morning — truth and priority

### 1. Trust gate

Check the live repository before acting:

- confirm current `main` SHA;
- list open PRs and exact head SHAs;
- inspect current reviews, unresolved threads, and hosted job steps;
- classify `steps=[]`, `runner_id=0`, quota, and billing failures as infrastructure non-evidence;
- run the available sovereign verifier against the exact intended SHA;
- record local verification, hosted CI, and production acceptance as separate axes:
  - `LOCAL_VERIFIED` when the exact-head local verifier passes;
  - `REMOTE_CI_GREEN` only when hosted jobs actually execute and pass;
  - `REMOTE_CI_EXECUTION_PLANE_BLOCKED` when hosted jobs are unavailable/non-executing;
  - `PRODUCTION_VERIFIED` only after SHA parity, front-door health, and required consecutive smokes are evidenced;
  - `PRODUCTION_UNKNOWN` when production evidence is absent or stale.
- use `LOCAL_VERIFIED_REMOTE_CI_BLOCKED` only when local verification passed and remote CI itself is unavailable; never use it merely because production acceptance is pending;
- reserve composite `PASS` for the complete applicable acceptance packet, with no hidden UNKNOWN axis.

Never convert `UNKNOWN` to `PASS`. Record exact-head local verification separately from remote CI and production. Every L5 approval packet must include the canonical `ACTION_HASH` bound to action type, target, environment, and payload, plus expiry. Any SHA, payload, target, environment, or evidence change invalidates the approval.

### 2. Production gate

Using the canonical Railway owner, verify and record:

`deployment status → deployed SHA → runtime /version SHA → /health → /healthz → /ar → public front door`

Require three consecutive smoke passes before a readiness claim. If direct evidence is unavailable, mark production readiness `UNKNOWN`; do not infer an outage or success from a stale notification.

### 3. Revenue command

Open the existing canonical commercial/Company Brain command surface. For every active account, expose one line only:

`company | current stage | consent_state | evidence | pain/economic impact | one next action | due | blocker | expiry`

Prioritize the nearest verified stage movement. Do not optimize lead counts or signal volume.

## Midday — evidence to conversation

### Market Radar

Convert source-bound signals into:

`signal → evidence → hypothesis → next evidence action`

Use official/public research to prepare founder conversation cards. Event or directory presence never becomes a contact, consent, partner, customer, opportunity, quote, revenue, or proof record.

### Founder-led interactions

The founder records each real interaction:

`WHO → COMPANY → ROLE → REAL PAIN → CURRENT TOOL → BUSINESS IMPACT → DECISION OWNER → DATA ACCESS → PILOT WILLINGNESS → FOLLOW-UP PERMISSION → NEXT STEP`

Use native/manual channel actions and the channel's own permissions. Dealix prepares research, copy, questions, and drafts; it does not impersonate the founder or automate restricted channel behavior.

### Canonical commercial progression

Use the existing opportunity state machine exactly; do not invent compressed aliases or insert evidence milestones into the commercial taxonomy:

1. `research` — `warm_intro_selected` or `message_drafted`; source-bound research/draft only
2. `qualify` — `founder_sent_manually` or `replied`; do not infer economic qualification beyond the recorded event/evidence
3. `approval` — `diagnostic_requested` or `diagnostic_delivered`; canonical diagnostic/pre-commitment mapping, not an L5 action approval record
4. `conversation` — `pilot_offered`; offer/discovery mapping only
5. `pilot` — `commitment_received`; bounded pilot commitment mapping
6. `proof` — `payment_received`; payment milestone mapping; payment evidence still comes from Finance OS
7. `commercial` — `delivery_started`, `delivered`, or `proof_pack_delivered`; delivery/proof-pack mapping
8. `won` — `upsell_offered` or `closed_won`; customer validation and expansion/referral/productization remain evidence attributes
9. `lost | parked` — `closed_lost` or explicit pause; terminal or explicitly paused outcome

Real interaction, known contact, diagnostic, quote, invoice, payment, delivery, customer validation, and expansion/referral/productization are evidence attributes within this machine—not new stage values. Consent remains a separate axis and must never store commercial milestones:

`UNKNOWN | CONSENTED | OPTED_OUT | SUPPRESSED | EXPIRED`

If evidence is missing, keep the account at its current stage. A public contact, event badge, draft, generated message, quote marker, invoice marker, paid-pilot marker, or synthetic record cannot promote it.

## Afternoon — bounded delivery preparation

For a qualified request, route to exactly one of the four canonical offers:

- Revenue Command Pilot
- Company Brain & Governed AI Sprint
- Saudi Market Access Sprint
- Partner Implementation & Proof

The Free Mini Diagnostic is the entry point into the existing `DIAGNOSTIC` path, not a fifth offer.

Prepare the smallest reversible pilot packet:

`baseline | problem | owner | data boundary | approved actions | success measure | exclusions | duration | price/scope draft | proof plan | rollback`

No public fixed pricing, guarantees, checkout, or payment claim is created by a draft.

## Delivery and proof

For each accepted/paid pilot, maintain:

`Baseline → Approved Action → Execution Receipt → Outcome → Customer Validation → Economic Interpretation → Limitation → Decision`

Payment requires payment evidence. Customer outcome requires customer-linked evidence. Proof requires resolvable, time-valid, non-synthetic evidence for the same company.

## Evening — one founder digest

Return only:

- **MONEY:** verified payments, commercial stage movement, blocked money;
- **DECISIONS:** 2–5 action-bound approvals, if any;
- **RISKS:** trust, production, consent, security, or delivery blockers;
- **APPROVALS:** exact packets awaiting founder action;
- **NEXT_ACTION:** one highest-leverage action per active account.

Append founder minutes, time-to-evidence, and the reason for every blocked or stopped item.

## Continuous internal work

Agents may continue 24/7 with:

- source-bound research and freshness checks;
- evidence normalization and deduplication;
- draft diagnostics, discovery briefs, proposals, proof packs, and content;
- tests, static checks, dependency analysis, and sovereign verification;
- queue hygiene, expiry detection, and blocker escalation;
- measured learning events.

They may not self-upgrade their authority, invent evidence, create a parallel owner, or cross the L5 boundary.

## Stop rules

Stop or downgrade work when it has no verified movement toward Trust, Revenue, Proof, Founder-Time Saving, or Cost Reduction after two reviews. Reject new tools unless they show:

`measured gap → isolated pilot → measurable benefit → rollback/disable path`

## Weekly review

Review the single scorecard:

`exact-head acceptance | SHA parity | real interactions | qualified problems | diagnostics | discoveries | customer-specific quotes | verified payments | accepted proof packs | expansions/referrals | founder minutes per stage movement | time-to-evidence`

Choose one repeated, material, evidence-backed learning event for the engineering backlog. Everything else remains queued, paused, or rejected.
