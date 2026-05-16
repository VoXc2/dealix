# Governed Revenue Ops — Repositioning Metrics

Small, honest metric set for the Governed Revenue Ops repositioning. **All
values start at 0.** No real customer, send, invoice, or Proof Pack exists yet —
metrics move only on real, approved activity. We never invent metrics.

| Metric | Value | Definition |
|--------|-------|------------|
| `sent_count` | 0 | Outreach messages actually sent (after approval) |
| `reply_count` | 0 | Replies received |
| `meeting_count` | 0 | Meetings held |
| `diagnostic_scope_requested` | 0 | Diagnostic scopes a prospect requested |
| `invoice_sent` | 0 | Invoices sent (engagement state `invoice_sent`) |
| `invoice_paid` | 0 | Invoices paid (engagement state `invoice_paid`) |
| `proof_pack_created` | 0 | Proof Packs created (score >= 70) |
| `retainer_opportunity` | 0 | Retainer opportunities identified |

**Rules:**
- A metric increments only on a real event with an evidence trail.
- `sent_count` increments only after a draft passes the approval center.
- `invoice_*` metrics track the engagement state machine — never a UI charge.
- No metric here implies a paid customer outcome; none exists yet.

Source of truth for live counts: the `/api/v1/revenue-ops` evidence trail and
the Founder Command Center screen.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
