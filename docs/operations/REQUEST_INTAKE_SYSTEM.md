# Request Intake System

> Every inbound request — sales lead, existing-customer ask, feature
> idea, partnership offer — flows through the same classification gate
> before any action is taken. No "let me just do this quickly" allowed.

## The 7 request types

1. **Sales opportunity** — net-new prospect; route to Qualification Score.
2. **Existing client request** — within or outside scope; route to Change Request System.
3. **Feature request** — engineer or customer idea; route to Feature Prioritization.
4. **Governance request** — security/compliance/audit ask; route to HoLegal + Governance OS.
5. **Support issue** — bug/regression/incident; route to engineering on-call.
6. **Partnership opportunity** — agency / consultant / channel; route to partner program.
7. **Custom enterprise request** — multi-pillar, multi-team; route to Enterprise Decision gate.

## Intake form (every inbound fills this)

```markdown
# Request Intake — <slug>
- Source: who asked + channel (email / WhatsApp / call / referral)
- Type: <one of the 7 above>
- Urgency: Low / Medium / High
- Revenue potential (next 90 days): SAR __
- Risk level: Low / Medium / High
- Existing Sellable-service match: Lead Intel / AI Quick Win / Company Brain / none
- Forbidden-action requested? yes / no (which?)
- Decision-maker named: yes / no
- Data / process available: yes / no / unknown

## Decision (one of)
- Route to Sellable service → quote SOW
- Offer paid Diagnostic
- Reject (Decision Rule violated)
- Add to backlog (feature / governance / partnership)
- Escalate to CEO (high-value / high-risk)

## Owner of next action
- Name: __
- Deadline: __
```

## Routing matrix

| Type | Default route | Owner | SLA |
|------|---------------|-------|-----|
| Sales opportunity | Qualification Score → Discovery call | CRO / SDR | ≤ 5 business days |
| Existing client | Change Request System | HoCS | ≤ 2 business days |
| Feature request | Feature Prioritization Score | HoP | monthly review |
| Governance | Approval Matrix | HoLegal | ≤ 1 business day |
| Support | Engineering on-call | CTO | SLO per tier |
| Partnership | Partner Program qualification | CRO | ≤ 7 business days |
| Custom enterprise | Enterprise Decision gate | CEO + CTO + HoLegal | ≤ 14 business days |

## Auto-rejections (capture politely, do not pursue)

- Cold WhatsApp / SMS / LinkedIn automation requests.
- Guaranteed-outcome contracts.
- Requests to "white-label and resell" without partner agreement.
- Requests with no decision-maker AND no budget AND no data.

## Anti-pattern blocked

The founder receiving a WhatsApp at 11pm saying "اشتغل هذا الشي بسرعة لي" → the intake form says: classify first, decide next morning. No "yes" via WhatsApp.

## Owner & cadence
- **Owner**: CEO owns the process; CRO + HoCS execute.
- **Cadence**: daily triage 15 minutes; weekly intake-volume review.

## Cross-links
- `docs/sales/QUALIFICATION_SCORE.md`
- `docs/sales/CLIENT_SELECTION_DECISION.md` *(if added)*
- `docs/delivery/CHANGE_REQUEST_PROCESS.md`
- `docs/product/FEATURE_PRIORITIZATION.md`
- `docs/governance/APPROVAL_MATRIX.md`
- `docs/enterprise/ENTERPRISE_DECISION.md`
