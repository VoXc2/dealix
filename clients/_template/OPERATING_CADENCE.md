# Operating Cadence — <CLIENT_NAME>

**Layer:** Client Template · Operational Kit
**Owner:** CSM Lead — <OWNER_NAME>
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [OPERATING_CADENCE_AR.md](./OPERATING_CADENCE_AR.md)

## Context
Operating cadence is the **heartbeat** of the engagement. Without an
agreed daily/weekly/monthly rhythm, every Dealix engagement drifts
into chaotic Slack threads and lost evidence. This template locks
the rhythm in writing on day 1 and mirrors the company-side rhythm
described in `docs/V14_FOUNDER_DAILY_OPS.md` and
`docs/meetings/OPERATING_REVIEW_PACK.md`, so the client engagement is
readable from a single ops review.

## Header
- **Client:** `<CLIENT_NAME>`
- **Primary CSM:** `<OWNER_NAME>`
- **Sprint / retainer:** `<sprint or retainer name>`
- **Time zone:** `<Asia/Riyadh>`
- **Working week:** Sun–Thu
- **Comms primary:** `<Slack / Teams / WhatsApp Business>` (no PII)
- **Comms async ticketing:** `<Linear / Jira / Notion>` queue
- **Approval channel:** dedicated review thread, screenshot in proof folder

## Daily — 15 min standup (Sun–Thu, 09:30 Riyadh)
**Attendees:** Delivery Lead + 1 capability owner (Dealix), 1 client
operator. CSM async.

Agenda:
1. **Workflow queue** — what's in run, what's blocked.
2. **Approvals** — items waiting for HITL or client sign-off.
3. **Urgent issues** — incidents, failed runs, data outages
   (escalation per `docs/INCIDENT_RUNBOOK.md`).
4. **Top one** — single most important task for the next 24h.

Output: short note in the daily channel + ticket updates. No slide,
no document.

## Weekly — 45 min review (Wednesday, 14:00 Riyadh)
**Attendees:** Full Dealix pod + client owner + capability owner.

Agenda:
1. **Progress against sprint plan** — what shipped, what slipped, why.
2. **Quality / QA issues** — eval failures, HITL exceptions,
   data quality alerts (`docs/EVALS_RUNBOOK.md`).
3. **Top 3 actions** — for the coming week, named owners, dates.
4. **Blockers** — what does the client need to unblock by Friday?
5. **Risks** — anything new on the risk register.

Output: weekly review note pinned in the engagement folder; one row
appended to the engagement journal.

## Monthly — 90 min review (last Wednesday, 14:00 Riyadh)
**Attendees:** Dealix Account Director + CSM + Delivery Lead, client
owner, client sponsor (CEO or COO).

Agenda:
1. **Proof update** — value delivered this month, evidence linked.
2. **Capability scorecard update** — re-score addressed capabilities,
   commit to `CAPABILITY_SCORECARD.md`.
3. **Roadmap update** — adjust 30/60/90 in `CAPABILITY_ROADMAP.md`.
4. **Backlog grooming** — `CAPABILITY_BACKLOG.md` reprioritized.
5. **Retainer review** — health, satisfaction, expansion signals from
   `EXPANSION_MAP.md`.
6. **Risks + governance** — incidents, audits, PDPL items.
7. **Decisions** — written, owners, dates, in monthly minutes.

Output: monthly memo (PDF-friendly) + signed proof appendix.

## Quarterly — Business Review (90 min + 30 min exec)
**Attendees:** Dealix Account Director + Capability Owner + CSO,
client sponsor + CFO (if applicable).

Agenda:
1. Quarter recap: value, level moves, sprints delivered.
2. Next quarter capability focus and sprint commit.
3. Pricing / tier review and forward roadmap.
4. Reference / case-study willingness.

Output: QBR pack archived under the client folder + updated 12-month
view in `CAPABILITY_ROADMAP.md`.

## Escalation paths
- **Operational incident** (eval failure, data outage):
  on-call Dealix engineer within 30 min;
  `docs/INCIDENT_RUNBOOK.md`.
- **PDPL / breach signal:** privacy officer within 1 hour;
  `docs/ops/PDPL_BREACH_RUNBOOK.md`.
- **Commercial issue** (scope, billing): Account Director within 4 hours.
- **Strategic concern** (relationship, exec mismatch): CSO within 24h.

## Comms hygiene rules
- No PII or contract figures in chat — link to the private workspace.
- All decisions logged in writing within 24h.
- All approvals captured (screenshot or signed message) into the
  proof folder before any production run.
- Sensitive data movement follows `docs/DATA_RETENTION_POLICY.md`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Workflow queue | Daily standup note | Delivery Lead | Daily |
| Sprint plan, evals | Weekly review note | CSM Lead | Weekly |
| Proof pack, scorecard | Monthly memo | Account Director | Monthly |
| QBR pack | Quarterly capability commitment | CSO + client sponsor | Quarterly |

## Metrics
- **Cadence adherence** — % of scheduled standups / reviews held.
- **Decision latency** — hours from issue raised to decision logged.
- **Approval lead time** — hours from request to client sign-off
  (target ≤ 24h for non-prod).
- **Incident MTTR** — minutes from incident to mitigation.

## How to fill this
1. Agree the schedule on the kickoff call; lock recurring invites.
2. Confirm the comms channel, the ticketing queue, and the proof
   folder location at day 1.
3. Pre-populate the first week's standups and the first month's
   review dates.
4. Re-confirm in writing every quarter; cadence drift is the leading
   cause of churn.

## Related
- `docs/meetings/OPERATING_REVIEW_PACK.md` — company review pack
- `docs/V14_FOUNDER_DAILY_OPS.md` — founder daily loop
- `docs/INCIDENT_RUNBOOK.md` — incident handling
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
