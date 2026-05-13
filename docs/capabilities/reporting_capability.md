# Capability Blueprint — Reporting Capability

> One of the 7 capabilities Dealix builds inside customers (per
> `docs/company/CAPABILITY_OPERATING_MODEL.md`). Mirrors the structure of
> `docs/capabilities/revenue_capability.md`. Concerns turning operational
> telemetry into executive summaries, proof packs, and weekly digests
> that the customer can actually act on — not "dashboards nobody opens".

## Business purpose
Give executives the truth in time to act. Replace Sunday-night Excel
rebuilds with a generated weekly summary, a monthly executive recap, and
a proof pack at every project closure. The Reporting Capability is the
loop that lets every other capability **compound** — a value not measured
is a value not retained.

> **Hard rule**: every output ends with a **next action** — no
> decorative outputs. If a recap doesn't tell the executive what to do
> next, it isn't shipped. This rule is enforced in
> `dealix/reporting/executive_report.py` (Proof Pack model) and in the
> Closure rule of `docs/company/VALUE_REALIZATION_SYSTEM.md`.

## Typical problems
- Weekly executive recap rebuilt by hand every Sunday night by a senior
  analyst — 4–6 hours, every week, forever.
- Multiple sources of truth: sales numbers from CRM, support numbers from
  inbox, ops numbers from sheets — no one composite view.
- Dashboards that "look pretty" but go unopened after week 2 because
  they don't recommend anything.
- Board pack assembled in PowerPoint at midnight; figures contradict
  last month's deck because nobody can explain the methodology.
- Project closure with no proof: "we did the work" — but no before/after
  numbers, no evidence, no next-value pointer.
- AR/EN gap: executives read in Arabic, analysts write in English; the
  monthly translation tax eats analyst capacity.
- No audit trail on the numbers themselves — when the CFO asks "where
  did this come from?", silence.

## Required inputs from customer
- Source systems for data (CRM / inbox / sheets / form / webhook).
- The 5–10 metrics the executive actually cares about (or co-create on
  Day 1 from the customer's strategy doc).
- Cadence (weekly + monthly are default; quarterly optional).
- Named recipients per output (who reads what).
- Tone-of-voice guide for executive prose (or use Dealix bilingual default).
- Bilingual preference (AR / EN / both) per recipient.
- Baseline data for each metric — without baselines there's no before/after.

## AI functions that build this capability
- Telemetry aggregation across modules (data_os / revenue_os /
  customer_os / operations_os / knowledge_os) into a single
  `reporting_os` view.
- Executive recap generation (`dealix/reporting/executive_report.py`) —
  weekly summary + monthly executive recap, with **a next action per
  section**, no exceptions.
- Proof Pack model (`dealix/reporting/proof_pack.py`) — every project
  closure produces before/after numbers, evidence files, value-category
  tag, and a next-value opportunity (per
  `docs/company/VALUE_REALIZATION_SYSTEM.md`).
- Bilingual prose generation (AR / EN side-by-side, never silent
  translation between the two).
- Trend analysis: deltas vs. last week / last month / baseline.
- Anomaly surfacing: flag the 2–3 things that changed materially this
  week so the executive isn't hunting.
- Source attribution per metric — every figure cites the underlying
  query/dataset for audit.

## Governance controls (binding)
- **Every output ends with a next action** — no decorative outputs.
  Enforced in the template and the QA checklist.
- **Source citation per metric** — figures without a verifiable source
  are quarantined to `research-only` and flagged in the header
  (per `docs/governance/RUNTIME_GOVERNANCE.md` Check 1).
- **No forbidden claims** in executive prose ("نضمن / guarantee /
  best in / 100%") — scanner runs before render
  (per `docs/governance/FORBIDDEN_ACTIONS.md` §3.1).
- **No PII in shipped outputs** — PII detector runs on the rendered
  recap before delivery (per `docs/governance/PII_REDACTION_POLICY.md`).
- **Audit log append** for every output generated, sent, and read
  (per `docs/governance/AUDIT_LOG_POLICY.md`).
- **Proof event write** at every project stage closure
  (per `docs/governance/RUNTIME_GOVERNANCE.md` Check 8).
- **External-share approval** — sending an output outside the customer's
  perimeter (e.g., to a board observer or investor) requires Level-5
  approval per the Approval Matrix.

## KPIs (measured before/after)
- Analyst hours per week spent assembling outputs (target: down 80%+).
- Cycle time from period-end to delivery (Sunday night → Monday
  9 a.m. for the weekly; month-end → Day-3 for the monthly).
- Read rate (% of named recipients who open within 48h).
- Next-action completion rate (the headline — were the recommended
  actions actually taken).
- Proof-Pack-per-project coverage (target: 100% of closed projects).
- Audit completeness — every figure traceable to a source query.
- AR/EN parity (every output ships in the recipient's preferred language).

## Maturity ladder (per `docs/company/CAPABILITY_OPERATING_MODEL.md`)
- **Level 0** — no recaps; executives ask in Slack and get a guess.
- **Level 1** — manual weekly recap assembled in Excel every Sunday.
- **Level 2** — template documented; one analyst owns it; metrics
  defined.
- **Level 3** — generated weekly summary + monthly executive recap,
  every output ends with a next action (Executive Reporting Automation).
- **Level 4** — Proof Pack at every closure + bilingual + audit trail
  + anomaly surfacing (Monthly AI Ops, reporting-focused variant).
- **Level 5** — Reporting OS: continuous KPI feed, board pack on demand,
  customer team self-serves, SAMA/NCA/ZATCA-ready evidence on request.

## Dealix services that build / advance this capability
| Service | Lifts capability from → to | Indicative price |
|---------|----------------------------|------------------|
| Executive Reporting Automation | L1 → L3 | SAR 12,000–40,000 setup + SAR 5,000–15,000 / mo |
| Monthly AI Ops (reporting variant) | L3 → L4–L5 | SAR 15,000–60,000 / mo |

Status note: Executive Reporting Automation is **Designed / Phase 2** in
`docs/company/SERVICE_REGISTRY.md`. Until promotion to Sellable, executive
recaps ship as a component of every Sellable Sprint (Lead Intelligence
Sprint, AI Quick Win Sprint, Company Brain Sprint each end with an
executive recap + Proof Pack). Monthly AI Ops is the retainer home for
ongoing cadence — activated **only after** a Sellable Sprint has been
delivered.

## Agents involved (per `docs/product/AI_AGENT_INVENTORY.md`)
- **ReportingAgent** — autonomy level 2, MVP. Pulls from
  `reporting/executive_report` and `proof_pack`. Generates weekly +
  monthly recaps + project Proof Packs. Always ends with a next-action
  section.
- **ComplianceGuardAgent** — mandatory gate. Runs PII / claims / source
  checks on every render before delivery.
- (Cross-cutting) **DataQualityAgent** upstream — Reporting Capability
  refuses to render numbers from `research-only` data.

## Proof types produced
- **Quality Proof** — every figure cited to a source query; audit-
  complete; AR/EN parity. This is the headline alongside Time.
- **Time Proof** — analyst hours saved per week; cycle-time from period-
  end to delivery.
- **Risk Proof** — PII scrubs, forbidden-claim blocks, external-share
  approvals logged.
- **Revenue Proof (indirect)** — next-action completion rate; the
  Reporting Capability's job is to turn telemetry into pipeline-moving
  decisions.
- **Knowledge Proof** — every Proof Pack feeds the Value Ledger and the
  capability roadmap (per `docs/company/VALUE_REALIZATION_SYSTEM.md`).

## Saudi-specific notes
- **Bilingual by default** — executive outputs ship AR/EN side-by-side;
  Arabic-first for Saudi boards and family-office recipients, English
  for international investors and KPMG/Deloitte-style auditors.
- **ZATCA-relevant figures** (VAT, invoicing volumes) cite the
  customer's tenant data only; Dealix is the pipeline, never the
  controller (per `docs/governance/PDPL_DATA_RULES.md`).
- **Sector regulators** — when SAMA / NCA / SDAIA / ZATCA inherit the
  audit log, the source-attribution layer is exportable as the
  underlying evidence; figures are reproducible from queries.
- **Saudi calendar** — Hijri date stamps optional alongside Gregorian
  on the monthly executive recap.
- **Kingdom Residency** option pins all telemetry processing to
  Kingdom-eligible regions (Enterprise plan).

## Cross-links
- `docs/services/ai_quick_win_sprint/report_template.md`
- `docs/services/ai_quick_win_sprint/proof_pack_template.md`
- `docs/company/CAPABILITY_OPERATING_MODEL.md`
- `docs/company/AI_CAPABILITY_FACTORY.md`
- `docs/company/CAPABILITY_PACKAGES.md`
- `docs/company/VALUE_REALIZATION_SYSTEM.md`
- `docs/product/AI_AGENT_INVENTORY.md`
- `docs/product/WORKFLOW_RUNTIME_DESIGN.md`
- `docs/governance/RUNTIME_GOVERNANCE.md`
- `docs/governance/AUDIT_LOG_POLICY.md`
- `docs/governance/FORBIDDEN_ACTIONS.md`
- `docs/governance/PII_REDACTION_POLICY.md`