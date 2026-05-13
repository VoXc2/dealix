# Dealix Customer Operating System

> The client should not buy a Sprint or a report. The client should feel that Dealix has become an **operating layer** inside their company — measuring, governing, proving, and recommending the next decision every month.

Twelfth strategic layer. Typed surfaces live in `auto_client_acquisition/client_os/`.

## 1. Client OS shape

```
Client OS =
  Capability Score
+ Data Readiness
+ Governance Status
+ Workflows
+ Drafts / Outputs
+ Approvals
+ Proof Timeline
+ Value Dashboard
+ Next Actions
```

The client sees: my capabilities, my ready data, my risks, what was built, what needs approval, what's been proven, what's the next decision.

## 2. Modules (seven panels)

1. Capability Dashboard (7 capability axes × 0–5 maturity).
2. Data Readiness Panel (sources, passport status, quality, duplicates, missing fields, PII flags, allowed use).
3. Governance Panel (allow/draft/approval/redaction/blocked counts, audit events).
4. Workflow Panel (owner, inputs, AI step, approval path, QA, proof metric, cadence).
5. Draft Pack (never auto-sent: emails, LinkedIn drafts, WhatsApp draft with consent only, call script, follow-up plan).
6. Proof Timeline (proof events, value events, blocked risks, before/after, confirmed vs. estimated).
7. Next Actions (Continue / Expand / Pause, linked to retainer or upsell).

## 3. Three-stage workspace

- **Stage 1 — after Sprint:** Proof Pack, Top Opportunities, Draft Pack, Next Action Plan.
- **Stage 2 — Retainer:** Monthly Dashboard, Proof Timeline, Approval Center, Value Report, Governance Log.
- **Stage 3 — large account:** Client Workspace, Role-based approvals, Audit exports, Executive reports, Multi-workflow view.

Rule: don't build the full Client OS before retainer pull. The client must pull, not Dealix push.

## 4. Client Health Score — 7 dimensions, total 100

| Dimension | Weight |
| --- | ---: |
| Clear owner | 15 |
| Data readiness | 15 |
| Stakeholder engagement | 15 |
| Proof strength | 20 |
| Governance alignment | 15 |
| Monthly workflow need | 10 |
| Expansion potential | 10 |

Tiers: 85+ expand aggressively, 70–84 offer retainer, 55–69 continue carefully, <55 pause or diagnostic only.

## 5. Operating cadence

- Weekly: data update, output review, draft approval, proof events, risk flags.
- Monthly: value report, proof summary, capability score update, next actions, expansion recommendation.
- Quarterly: capability review, governance review, workflow maturity, retainer scope, strategic roadmap.

Rule: retainer without cadence = weak support contract.

## 6. Monthly Value Report — 8 sections

What was done, what changed, what value was observed, what is estimated, what risks were blocked, what needs approval, what capability improved, what should happen next.

## 7. Trust layer per output

Each output exposes: source status, governance status, PII status, approval status, QA status, proof linkage. No invisible agents. No unowned agents. No external action without approval. No agent output without audit.

## 8. Agent Transparency Card

Every output that touched an agent shows the card — agent, task, autonomy_level, human_owner, external_action_allowed, approval_required, audit_event.

## 9. Saudi Client OS

Arabic executive summaries, English appendix optional, Saudi business tone, city/region fields, sector taxonomy, PDPL-aware language, WhatsApp consent status, relationship status.

## 10. Expansion engine

Every panel surfaces a next commercial move:

- Weak data readiness → Data Readiness Retainer.
- High governance risk → Monthly Governance.
- Draft Pack used → Monthly RevOps OS.
- Knowledge gaps → Company Brain.
- Repeated reports → Executive Reporting Automation.

Rule: the workspace reveals the next commercial move, not just the work.

## 11. MVP

Client profile, capability score, data readiness score, lead/workflow table, governance status, draft pack, proof pack, next actions. **Not** in MVP: SSO, complex RBAC, billing, marketplace, partner portal, white-label.

## 12. Data model (16 entities)

`Client → Workspace → Projects → DataSources (each with SourcePassport) → Datasets → Workflows → Outputs → Drafts → Approvals → AuditEvents → ProofEvents → ValueEvents → NextActions → RetainerRecommendations`.

## 13. Adoption metrics

workspace active clients, monthly active stakeholders, drafts reviewed, approvals completed, proof views, next actions accepted, retainer conversions, expansion clicks, governance decisions viewed. The strongest signal: **client asks for a continuous dashboard**.

## 14. Monetization in three stages

Stage 1: included with retainer. Stage 2: Workspace fee (Workspace, Approval Center, Governance Log, Value Dashboard). Stage 3: Enterprise (Audit exports, role permissions, AI Control Plane, executive dashboards). Don't impose a platform fee before the client sees continuation value.

## 15. The closing sentence

> Dealix wins when every client lives inside an operating system: capabilities measured, data governed, outputs approvable, value proven, and next step explicit — the bridge from a single project to a retainer to a platform.
