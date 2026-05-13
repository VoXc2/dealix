# Human-in-the-Loop Matrix

> "AI proposes, human approves." For every AI-touched action, this matrix
> defines whether a human must be in the loop and at which checkpoint.

## Matrix

| AI action | Risk | Human role | Approval required? | Approver |
|-----------|------|-----------|:------------------:|----------|
| Classify data | Low | Reviewer spot-checks ≥ 5% sample | No | n/a |
| Score / rank entities | Medium | Delivery Owner reviews top-N before delivery | Yes (before delivery) | Delivery Owner |
| Draft email / message | Medium | Human reviews each draft | Yes (per draft) | AE / CSM |
| Recommend next action | Medium | Human accepts/rejects per item | Yes | Delivery Owner |
| RAG answer (internal user) | Medium | Source check on first use of each doc | No (post-hoc audit) | n/a |
| RAG answer (customer-facing) | High | Source-grounded answer + citation | Yes (workflow gate) | HoCS |
| Update CRM stage | Medium | Owner approval per record | Yes | AE |
| Bulk CRM update | High | Approval per batch | Yes | AE + CRO |
| Send single email externally | High | Per-message approval | Yes | CSM |
| Bulk send (any channel) | Critical | Campaign approval + consent attestation | Yes | Head of CS + HoLegal |
| WhatsApp message | High | Consent + human approval per message | Yes | Head of CS |
| Publish marketing claim | Medium | Claim QA before publish | Yes | Marketing Lead |
| Use customer data in report (external) | High | Redaction + lawful basis | Yes | HoLegal |
| External API write | High | CTO approval per integration | Yes | CTO |
| Policy override | Critical | CEO only | Yes | CEO |
| Autonomous external action | Not allowed | n/a | BLOCKED | (no exception) |

## Mode hierarchy (most → least restrictive)

1. **Blocked** — forbidden; never permitted (e.g., autonomous external action, cold WhatsApp, scraping, guaranteed claims).
2. **Approval-only** — agent prepares; human approves per item before side-effect runs.
3. **Reviewed-before-delivery** — agent produces; human reviews before customer sees output.
4. **Audit-only** — agent acts; human reviews log post-hoc (low-risk internal actions only).

## Default for new agents

When a new agent is added (per `docs/product/AI_WORKFORCE_OPERATING_MODEL.md`), its default mode is **Approval-only** unless the AI Action Taxonomy clearly classifies it as Level 0–1 with no side-effect. Promotion to a less-restrictive mode requires:
- ≥ 30 days of stable behavior in Approval-only.
- Zero Hard Fails attributed to the agent.
- CTO + HoLegal co-sign.

## Why this matters

Agentic AI's biggest risk in 2026+ is autonomous actions that move beyond the human's permission scope. Dealix sells AI Operations explicitly because we keep the human in the loop. Customers buy Dealix because they trust the loop — remove the loop and we are commodity AI.

## Cross-links
- `docs/governance/RUNTIME_GOVERNANCE.md` — the 8 runtime checks
- `docs/governance/APPROVAL_MATRIX.md` — action × evidence → approver role
- `dealix/trust/approval_matrix.py` — code-side approval matrix
- `docs/product/AI_WORKFORCE_OPERATING_MODEL.md`
