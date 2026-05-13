---
title: Change Request Process — Form, Approval, Pricing Rules
doc_id: W6.T36.change-request
owner: HoCS
status: draft
last_reviewed: 2026-05-13
audience: [internal, customer]
language: en
ar_companion: none
related: [W6.T36, W5.T18]
kpi:
  metric: change_request_turnaround_hours
  target: 48
  window: per_request
rice:
  reach: 0
  impact: 2
  confidence: 0.85
  effort: 0.5
  score: delivery-operating
---

# Change Request Process

## 1. Context

Once a project is in motion, the only legitimate path to add work is a written
Change Request (CR). The CR turns a verbal "can you also..." into a costed,
approved, scheduled increment — protecting the timebox of the original scope
and the margin on the project.

## 2. Audience

CSM (CR owner per project), customer's day-to-day owner (requester),
customer's economic buyer (approver on the buyer side), HoCS (approver on the
Dealix side for non-trivial CRs).

## 3. The Form

A change request is a 1-page document with seven fields. Stored in the
customer's project folder; emailed as PDF to the buyer for signature.

| Field | What goes in it |
|-------|-----------------|
| CR-ID | `CR-<project_id>-<seq>` |
| Title (AR / EN) | One line, action verb (e.g., "Add WhatsApp channel to outreach flow") |
| Requested by | Customer name + role + date |
| Business reason | Why the customer needs it; impact if not done |
| Scope delta | What is being added / removed / changed; data sources affected |
| Effort & timing | Engineer-days; calendar days; whether it shifts Day N |
| Pricing | SAR amount + whether absorbed / billed / credited |

## 4. Pricing Rules

| Size of CR | Default treatment |
|------------|------------------|
| < 4 engineer-hours, in-line with current Sprint pillar | Absorbed; logged in change ledger; no price change |
| 4–16 engineer-hours | Billed at SAR 1,250 / hour, fixed quote, paid Net-15 |
| > 16 engineer-hours OR shifts Day N OR adds an integration | Treated as a paid scope extension (mini-SOW); minimum SAR 12K |
| Adds a new OS module / vertical / language | Promoted to a separate Sprint or Pilot; **not** a CR |

The pricing column is set by the CSM and reviewed by HoCS before the CR
goes to the customer. No verbal commitments.

## 5. Approval Workflow

```
Day-to-day owner (request)
      ↓
CSM drafts CR (effort + price + timing)
      ↓
HoCS sign-off (Dealix side) — within 24h
      ↓
Economic buyer sign-off (Customer side) — within 48h
      ↓
CR added to the project plan; engineer scheduled; ledger entry created
```

A CR is **not started** until it is countersigned. "We'll start now and sort
out the paperwork later" is forbidden — it is the path back to scope creep.

## 6. Anti-Patterns

- **Free-ladders**: stacking "small" absorbed CRs that together exceed the absorb threshold.
- **Verbal CRs**: agreeing in a Slack thread without writing it down.
- **No-deadline CRs**: signing without dating the new Day N.
- **CR as discount lever**: customer pushing for free scope in exchange for case-study consent. Refer to Trust + AE.

## 7. Cross-links

- Scope control: [`SCOPE_CONTROL.md`](SCOPE_CONTROL.md)
- Lifecycle: [`DELIVERY_LIFECYCLE.md`](DELIVERY_LIFECYCLE.md)
- Pricing reference: [`../pricing/pricing_packages_sa.md`](../pricing/pricing_packages_sa.md)
- Approval matrix code: `dealix/trust/approval_matrix.py`

## 8. Owner & Review Cadence

- **Owner**: HoCS.
- **Review**: refresh price ladder when the canonical pricing doc changes.

## 9. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoCS | Initial CR form + pricing rules + approval workflow |
