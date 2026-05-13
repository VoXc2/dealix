---
title: Executive Operating Cadence — Weekly, Monthly, Quarterly, Annual
doc_id: W5.T30.exec-operating-cadence
owner: CEO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W0.T00, W4.T13, W5.T10, W5.T18, W5.T19, W5.T29]
kpi:
  metric: operating_cadence_attendance
  target: 95
  window: quarterly
rice:
  reach: 50
  impact: 2.0
  confidence: 0.9
  effort: 2
  score: 45
---

# Executive Operating Cadence

## 1. Context

A company executes its strategy through the rhythm of its meetings. The executive operating cadence at Dealix is the structured set of recurring decision events that translate the annual strategy into weekly action — and translate weekly signal back into annual strategy adjustments. Without this cadence, the team defaults to reactive mode: every Slack thread becomes a meeting, every dashboard spike becomes a fire drill, and the strategic frame erodes one ad-hoc decision at a time.

This document defines the canonical cadence: four weekly events (Monday Ops, Wednesday Pipeline, Friday Retro, and a daily standup nested inside each), the Monthly Business Review (anchored to the T13 KPI dashboard), the Quarterly Strategy Reset, and the Annual Board Cycle. Per meeting it specifies attendees, prep, decision rights, and output artifact. The intent is to make the operating system legible enough that anyone on the team can predict what gets discussed where, who decides what, and what comes out of a given event.

Cross-link: `docs/ops/DAILY_OPERATING_LOOP.md` defines the day-level rhythm that nests inside this cadence; this document defines the week / month / quarter / year scaffold that contains the daily loop.

## 2. Audience

- **CEO (owner)** — runs the operating cadence, chairs strategic events, owns the calendar.
- **HoP, HoCS, HoS, HoM, HoT, HoO, CFO/Finance lead** — the executive team. Standing attendees at weekly events; rotating ownership of agenda items.
- **CRO** — when filled, owns Wednesday Pipeline and is a co-chair of the Monthly Business Review with the CEO.
- **Board (independent + investor directors)** — Quarterly and Annual events.
- **Wider team (manager-level)** — receives the published outputs (decisions log, action items, KPI snapshots) within 24 hours of each event.

## 3. Decisions / Content

### 3.1 Weekly Cadence

Three executive meetings per week plus a 15-minute daily standup. Total weekly executive-time investment: approximately 4 hours per attendee, deliberately compact.

#### Monday Ops (60 minutes, 09:00 SA time)

- **Purpose**: convert weekly KPIs into the week's operating plan; surface and assign top-3 weekly priorities per function.
- **Attendees**: full exec team.
- **Prep** (by Sunday 18:00): each Head writes a 200-word weekly brief — what shipped last week, what's planned this week, top blockers, the one decision they need from the room. Briefs circulated in advance.
- **Agenda**: (5m) prior-week scorecard review; (30m) function-by-function read-out (5m each); (15m) cross-function coordination + blocker resolution; (10m) decisions and action items.
- **Decision rights**: tactical decisions binding on the week. Strategic decisions deferred to the Monthly Business Review.
- **Output**: published decisions log + action items list within 4 hours, in the shared ops channel.

#### Wednesday Pipeline (60 minutes, 14:00 SA time)

- **Purpose**: pipeline integrity, forecast accuracy, deal-by-deal coverage for the current quarter.
- **Attendees**: CEO, CRO (or HoS until CRO hired), HoCS, HoM, CFO, Sales managers.
- **Prep** (by Tuesday 18:00): updated HubSpot pipeline view; deals > SAR 500K with risk flags; updated forecast vs. plan.
- **Agenda**: (10m) forecast roll-up; (30m) deal-by-deal review of stage 3+ opportunities and Sovereign-segment pipeline; (10m) marketing-sourced pipeline health; (10m) actions.
- **Decision rights**: pipeline owner has commercial discretion within pre-approved discount/term ladders; deviations require CEO + CRO joint approval same-day.
- **Output**: forecast variance report + deal action items within 4 hours.

#### Friday Retro (45 minutes, 16:00 SA time)

- **Purpose**: weekly retrospective; what worked, what didn't, what we are changing. Operational learning loop.
- **Attendees**: full exec team.
- **Prep**: no formal prep; show up honest.
- **Agenda**: (10m) wins reel; (15m) misses and root-cause hypotheses; (10m) one structural change for next week; (10m) team mood / signal-from-the-floor read.
- **Decision rights**: changes to operating practices binding the following week; bigger structural changes deferred to Monthly Business Review.
- **Output**: a single page — three wins, three misses, one structural change — published to the company-wide channel.

#### Daily Standup (15 minutes, 09:00 SA time, Tue/Wed/Thu)

- Nested inside the daily operating loop (`docs/ops/DAILY_OPERATING_LOOP.md`). Asynchronous on most days; synchronous on launch / incident weeks.

### 3.2 Monthly Business Review (MBR)

- **Cadence**: first Wednesday of each month, 09:00–12:00 SA time, in-person preferred.
- **Purpose**: strategic monthly review — translate the T13 KPI dashboard (cross-link: `BUSINESS_KPI_DASHBOARD_SPEC.md`) into structural decisions for the coming month. The MBR is where weekly operational noise resolves into monthly strategic signal.
- **Attendees**: full exec team; CFO presents financials; HoP presents product velocity; HoCS presents NRR / churn; HoS presents pipeline; HoT presents trust posture; HoO presents operational health.
- **Prep** (by the prior Friday 17:00): T13 dashboard snapshot frozen; each Head writes a 1-page MBR memo covering (a) prior month's actuals vs. plan, (b) variance explanation, (c) the single most material decision needed this month, (d) the single biggest risk for the next 90 days.
- **Agenda** (3 hours): (15m) CEO framing; (30m) financials; (45m) function read-outs (8m each); (45m) the three biggest decisions of the month, debated and decided; (30m) risk and dependency review; (15m) wrap and action items.
- **Decision rights**: monthly structural decisions binding on the function; commercial commitments > SAR 1M require CEO sign-off in the room.
- **Output**: MBR pack (decisions, actions, owners, deadlines) + dashboard snapshot published within 24 hours.

### 3.3 Quarterly Strategy Reset (QSR)

- **Cadence**: 1.5-day off-site at the end of each quarter (Mar, Jun, Sep, Dec).
- **Purpose**: validate or revise the strategic frame; reset OKRs; re-plan the coming quarter end-to-end.
- **Attendees**: exec team; selected manager-level attendees by invitation; occasional board observer.
- **Prep**: 5-page strategic memo from each function (4-week prep window); CEO writes a 10-page "state of the company" memo.
- **Agenda** (Day 1: 09:00–18:00): (60m) CEO state-of-the-company; (90m) prior-quarter OKR review; (90m) market and competitive update; (90m) function strategy debates; (90m) integrated planning workshop. (Day 2: 09:00–14:00): (90m) commit to next-quarter OKRs; (90m) cross-function alignment; (60m) communication plan for the rest of the company; (60m) wrap.
- **Decision rights**: strategic decisions binding for the quarter. Any deviation during the quarter requires CEO sign-off and is logged for the next QSR.
- **Output**: published "Quarterly Strategy Pack" within 5 business days — OKRs, function plans, resource allocation, risk register.

### 3.4 Annual Board Cycle

- **Cadence**: four formal board meetings per calendar year (Feb, May, Aug, Nov) + one annual strategy review (typically October).
- **Purpose**: governance, strategic oversight, capital decisions, succession planning.
- **Attendees**: full board, CEO, CFO; other Heads as agenda dictates.
- **Prep**: board pack circulated 7 calendar days in advance — financials, KPI dashboard, strategic update, three discussion topics, one decision item.
- **Agenda** (typical board meeting, 3 hours): (15m) CEO update; (45m) financials and forecast; (60m) deep-dive on one strategic topic; (30m) governance / committee reports; (30m) executive session (board only).
- **Decision rights**: per the company's governance documents — typically annual budget approval, executive compensation, major contracts > board-approved threshold, equity actions, succession.
- **Output**: board minutes within 10 business days; CEO summary published to exec team within 48 hours of each board meeting.

### 3.5 Decision-Rights Hierarchy

The cadence implies a hierarchy of decision rights, which makes the system self-consistent:

| Time horizon | Decision type | Forum | Final authority |
|--------------|---------------|-------|-----------------|
| Day | Operational | Daily standup / direct exec | Function Head |
| Week | Tactical (binding ≤ 1 week) | Monday Ops / Wednesday Pipeline / Friday Retro | Function Head w/ CEO awareness |
| Month | Structural (binding the month) | Monthly Business Review | CEO with exec team alignment |
| Quarter | Strategic OKRs and plans | Quarterly Strategy Reset | CEO with exec team commitment |
| Year | Capital, governance, succession | Board Cycle | Board |

A decision belongs in the lowest-cost forum that is decision-capable. Escalation up the hierarchy is for genuine strategic questions, not for offloading discomfort.

### 3.6 Anti-Patterns

- **Meeting drift** — discussions spilling outside the agenda; mitigated by published agendas and a hard-stop discipline.
- **Status-only meetings** — Monday Ops becoming a series of status updates with no decisions. The 30-minute readout cap forces compression.
- **Founder default mode** — CEO answering every operational question that should be answered by a Head. The decision-rights hierarchy is enforced.
- **Decisionless MBRs** — the MBR exists to make decisions; if none emerge, the prep was insufficient.
- **Quarterly reset that doesn't reset** — QSR producing the same OKRs as the prior quarter without genuine debate. The 5-page strategic memo per function is the antidote.

## 4. KPIs / Acceptance

| Metric | Target | Window |
|--------|--------|--------|
| Operating-cadence attendance | ≥ 95% | quarterly |
| Decisions per Monthly Business Review | ≥ 3 logged | per MBR |
| Action-item closure rate | ≥ 90% by next equivalent event | per event |
| MBR pack published within 24h | 100% | per MBR |
| Quarterly Strategy Pack published within 5 business days | 100% | per quarter |
| Board pack circulated ≥ 7 days in advance | 100% | per board meeting |
| Decision-rights breaches (escalation up the hierarchy inappropriately) | ≤ 1 per quarter | quarterly |

## 5. Dependencies

- Docs: W4.T13 (KPI dashboard — drives MBR), W5.T10 (CS framework — informs CSR read-outs), W5.T18 (pilot framework — informs Wednesday pipeline), W5.T19 (expansion playbook — informs MBR commercial review), W5.T29 (launch checklist — overrides the cadence during launch week with the launch-room cadence).
- Code: dashboard rollups for KPI snapshots; HubSpot for pipeline review; shared decisions-log in the ops channel.
- People: CEO, CFO, all functional Heads, Board.

## 6. Cross-links

- Daily loop: `docs/ops/DAILY_OPERATING_LOOP.md`
- KPI dashboard: `BUSINESS_KPI_DASHBOARD_SPEC.md`
- Master plan: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- ICP: `docs/go-to-market/icp_saudi.md`
- Lead engine: `docs/product/saudi_lead_engine.md`
- Pricing: `docs/pricing/pricing_packages_sa.md`
- CS framework: `docs/customer-success/cs_framework.md`
- Pilot framework: `docs/delivery/pilot_framework.md`
- Expansion playbook: `docs/customer-success/expansion_playbook.md`
- Launch checklist: `docs/product/launch_checklist.md`
- Executive decision pack: `EXECUTIVE_DECISION_PACK.md`
- Founder escalation: `FOUNDER_DECISION_ESCALATION.md`

## 7. Owner & Review Cadence

- **Owner**: CEO.
- **Review**: cadence structure reviewed at each Quarterly Strategy Reset; weekly meeting formats reviewed at the Friday Retro on the last Friday of each quarter.
- **Escalation**: any standing meeting cancelled more than once per quarter → CEO review; structural changes to the cadence (new meeting, removed meeting, changed decision rights) → quarterly review only.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CEO | Initial cadence: 3 weekly meetings + daily standup, Monthly Business Review, Quarterly Strategy Reset, Annual Board Cycle, decision-rights hierarchy |
