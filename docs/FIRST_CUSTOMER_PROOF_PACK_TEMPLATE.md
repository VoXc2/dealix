# First Customer Proof Pack — Template

> Day 7 deliverable. Single document, ≤ 4 pages, Arabic-first.
> Estimates are clearly labeled as estimates. No invented outcomes.

## Header

```
Dealix Proof Pack — Pilot Week 1

Client:           [Company name]
Service:          7-Day Growth Proof Sprint
Period:           [start ISO date] → [end ISO date]
Prepared by:      Sami / Dealix
Generated at:     [ISO timestamp]
Customer ID:      [from /api/v1/payments/mark-paid response]
Deal ID:          [from /api/v1/deals]
```

## 1. Executive Summary

```
- What we worked on:
  [1-2 sentences in Arabic — concrete + bounded]

- Main finding:
  [1 sentence — the most important learning from this week]

- Recommended next step:
  [Continue Pilot / Executive Growth OS / Data to Revenue / Partnership Growth / Stop]
```

## 2. What was created

```
- Opportunities created:           10
- Drafts created (AR + EN):        6
- Follow-up angles planned:        3
- Meeting / call scripts:          [N or "n/a"]
- Partner suggestions:             [N or "n/a"]
```

## 3. What was protected

```
- Unsafe channels avoided:
  [list — e.g. "blocked cold WhatsApp on 4 numbers from purchased list"]

- Cold WhatsApp blocked:
  [count + the operator decision id(s) from /api/v1/compliance/check-outreach]

- Contacts marked needs_review:
  [count + reason]

- Claims avoided:
  [list — e.g. "no 'نضمن' in any draft, all verified by sweep"]

- Approval points enforced:
  [list — e.g. "every outbound was draft-only, founder approves before send"]
```

## 4. Revenue impact estimate (clearly labeled)

```
⚠ This section is an ESTIMATE. Outcomes depend on the customer's
  execution, market conditions, and which drafts are actually sent.
  Dealix does not guarantee revenue.

- Potential pipeline:
  [SAR range — e.g. 50,000 - 150,000 SAR — تقدير]

- Confidence:
  [low / medium / high — with reason]

- Assumptions:
  - [assumption 1 — e.g. "20% reply rate on warm LinkedIn DMs"]
  - [assumption 2 — e.g. "30% of replies convert to a meeting"]
  - [assumption 3 — e.g. "10% of meetings convert to a deal at customer's average size"]

- What is estimated vs proven:
  - PROVEN: opportunities count (10), drafts count (6), risks blocked (N)
  - ESTIMATED: pipeline value, conversion rates
```

## 5. Open approvals

```
- Messages awaiting your approval before send: [N]
- Follow-ups awaiting approval:                [N]
- Channels awaiting approval (e.g. switch from LinkedIn to email): [N]

Each open approval lives in /api/v1/admin/approvals/pending until you decide.
```

## 6. Next 7-day plan

```
Step 1: [concrete next action — e.g. "approve the top 3 LinkedIn drafts and send manually"]
Step 2: [concrete next action]
Step 3: [concrete next action]
```

## 7. Upgrade recommendation

Pick exactly one:

```
□ Continue Pilot (another 7 days at 499 SAR — same bundle, new ICP)
□ Upgrade to Executive Growth OS (2,999 SAR/month — daily role briefs + weekly proof packs)
□ Run Data to Revenue (1,500 SAR — clean a list and score contactability)
□ Run Partnership Growth (3,000-7,500 SAR — agency channel build)
□ Stop / not a fit (and that's OK — say thank you)
```

Justify the choice in 2-3 lines.

## Hard rules

| Rule | Detail |
| --- | --- |
| Estimates labeled `تقدير` / `estimate` | Never bare numbers without the label |
| No "نضمن" / "guaranteed" anywhere | Pre-send sweep enforced |
| `What was created` and `What was protected` both populated | If protected = 0, that's a flag — re-check compliance/check-outreach was actually run |
| Next 7-day plan has 3 concrete steps | Vague language = customer won't act |
| Upgrade recommendation = exactly one option | Multiple options confuse the customer |
| Day 7 hard delivery | If late → upsell window closes |

## How to render

Three options today:

1. **Markdown only** (current default — paste into LinkedIn DM or email).
2. **`POST /api/v1/customers/{customer_id}/proof-pack`** returns a Markdown
   case-study template with testimonial + referral asks. Combine with this
   doc's structure.
3. **`POST /api/v1/command-center/proof-pack`** returns a graded version
   with activity_summary + pipeline_impact + benchmark_comparison.
   Use the grade for the upgrade recommendation logic
   (grade ≥ B → recommend Executive Growth OS).

HMAC-signed PDF rendering is BACKLOG — Markdown delivery is fine for
the first 3-5 customers.

## Definition of done

- [ ] All 7 sections populated
- [ ] Estimates labeled as estimates
- [ ] At least one "what was protected" entry (else re-check compliance ran)
- [ ] Exactly one upgrade recommendation
- [ ] Sent on day 7 (not day 8)
- [ ] Board row → `proof_pack_sent`
