# Quality Standard v1 — Master · Operating Blueprint

**Layer:** Master · Operating Blueprint
**Owner:** QA Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [QUALITY_STANDARD_V1_AR.md](./QUALITY_STANDARD_V1_AR.md)

## Context
This is the Dealix v1 quality bar that every delivery must clear before
it ships to a client and before it is filed in the Proof Ledger. It
operationalizes the rules in `docs/DEALIX_OPERATING_CONSTITUTION.md`,
hardens the AI observability practices in
`docs/AI_OBSERVABILITY_AND_EVALS.md` and `docs/EVALS_RUNBOOK.md`, and is
the gate referenced by the 90-Day Plan's Phase-1 acceptance test in
`docs/company/NEXT_90_DAYS_EXECUTION_PLAN.md`. Hard fails route directly
to the incident process in `docs/ops/INCIDENT_RUNBOOK.md`.

## Score model (out of 100)

| Area | Weight |
|---|---:|
| Business impact | 20 |
| Data quality | 15 |
| AI output quality | 15 |
| Arabic / English quality | 10 |
| Compliance | 15 |
| Reusability | 15 |
| Upsell potential | 10 |
| **Total** | **100** |

Each area is scored 0–100 by the reviewer, then weighted to produce the
overall score. Scores are recorded in the delivery's QA log and
attached to the Proof Pack.

## Pass rule
A delivery passes only if **all three** conditions hold:
1. Overall weighted score **≥ 85**.
2. Compliance area score = **100** (no exceptions).
3. No critical unresolved risk flagged in the reviewer checklist.

## Hard fails (any one fails the entire delivery, regardless of score)
- PII appears in logs, prompts, or reports.
- Any AI output makes a **guaranteed** claim (revenue, results, time
  saved) without a stated baseline and source.
- A knowledge / RAG answer is delivered **without** a cited source.
- An external action (email, post, message, API call) was taken
  **without** an explicit, logged approval.
- Use of any forbidden tool: cold WhatsApp, LinkedIn automation,
  unauthorized scraping, prospect-data purchased from prohibited
  sources.

Any hard fail triggers the incident process and a 24-hour client
communication, even if the client has not noticed.

## Score interpretation
- **85–100** — Ready for client delivery + Proof Pack filed.
- **70–84** — Rework required. Reviewer must document specific gaps in
  the QA log; delivery date held until rework re-scores ≥ 85.
- **< 70** — Do not deliver. Restart QA cycle from "Data" upward; the
  delivery is treated as if it has not been built yet.

## Reviewer checklist (5 areas, ~30 items)

### Business (5 items)
- [ ] Outcome is stated in one sentence.
- [ ] At least one metric is defined and measurable.
- [ ] Next action for the client is listed.
- [ ] Executive summary is present (≤ 5 bullets).
- [ ] SAR / dollar impact stated where reasonable, or marked "indicative".

### Data (5 items)
- [ ] Source dataset registered with name, owner, location.
- [ ] Freshness noted (date of last sync or export).
- [ ] Sample QA passed on a documented row count.
- [ ] Duplicates detected and handled with documented rule.
- [ ] PII fields flagged; minimization rule applied.

### AI (5 items)
- [ ] Prompt is versioned and committed.
- [ ] Output schema is enforced (JSON / structured fields).
- [ ] Claims check passed (no guarantees, no unsourced numbers).
- [ ] Arabic tone check passed (register matches the client's audience).
- [ ] RAG citations present for any factual answer; "I do not know" used
      when source is missing.

### Compliance (5 items)
- [ ] Governance check (`governance_os.policy_check`) logged.
- [ ] Approvals captured for every external action.
- [ ] Lawful basis verified for any PII processed (PDPL-aware).
- [ ] Consent reviewed and stored where applicable.
- [ ] Audit event written with `audit_event_id`.

### Reusability (5 items)
- [ ] Template extracted (prompt, schema, or playbook section).
- [ ] Playbook entry added or updated.
- [ ] Capital ledger entry created for any new reusable asset.
- [ ] Feature candidate logged in the product backlog (if any).
- [ ] Proof Pack drafted with anonymization rule applied.

### Optional sixth pass (auditor only)
- [ ] Spot-check 2 random outputs against original source data.
- [ ] Replay one approval chain end-to-end.
- [ ] Confirm no PII in any log line attached to this delivery.

## Roles
- **Reviewer** — runs the checklist, scores each area, signs the QA log.
- **QA Lead** — owns this standard, resolves disputes, approves edge
  cases.
- **CEO** — final escalation for any "Hard fail → ship anyway" request
  (rarely granted, always logged).

## Cadence
- Per delivery (every time).
- Weekly aggregate review on Wednesday (QA day in the weekly rhythm).
- Quarterly recalibration of weights based on aggregate scores and
  client feedback.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Delivery artefacts (data, prompts, outputs, logs) | QA score + pass/fail + gap list | Reviewer | Per delivery |
| Hard-fail flag | Incident ticket + 24-hour client comms | QA Lead | On fail |
| Quarterly score aggregate | Updated weights / new checklist items | QA Lead + CEO | Quarterly |
| Approved exception | Logged CEO sign-off | CEO | Rare |

## Metrics
- **Pass rate** — % of deliveries passing v1. Target: ≥ 95% from day 30.
- **Mean overall score** — Target: ≥ 88 trailing 30-day average.
- **Hard-fail count** — Target: 0 per quarter.
- **Rework cycles** — Target: median ≤ 1 per failing delivery.

## Related
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — eval signals feeding this standard.
- `docs/EVALS_RUNBOOK.md` — how to run the eval suite the reviewer references.
- `docs/ops/INCIDENT_RUNBOOK.md` — incident process for hard fails.
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — constitutional rules this standard enforces.
- `docs/company/DEALIX_MASTER_OPERATING_BLUEPRINT.md` — blueprint that makes this standard mandatory.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
