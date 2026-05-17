# Revenue Ops Machine — Operator Reference — آلة عمليّات الإيراد — مرجع المُشغِّل

> Operator-facing reference for the governed online sales funnel under `auto_client_acquisition/revenue_ops_machine/`. Bilingual headings; English body is acceptable for operator detail. This doc describes how the machine is configured and operated — it is not customer-facing and contains no client data.
>
> Cross-link: [LINKEDIN_CADENCE_PLAN.md](./LINKEDIN_CADENCE_PLAN.md), [REVENUE_OPS_EMAIL_TEMPLATES.md](./REVENUE_OPS_EMAIL_TEMPLATES.md), landing page `/dealix-diagnostic`, Sample Proof Pack `/assets/proof/sample-proof-pack.html`, Proof Pack standard `docs/assets/proof_packs/proof_pack_template.md`.

---

## 1. What the machine is — ما هي الآلة

The Revenue Ops Machine is a governed 16-state online sales funnel. It routes an inbound lead from first contact to delivery, with a lead scorer at the front and a draft → gate → approval-queue flow at every external touchpoint. It does not send anything externally on its own. It routes leads onto the existing 5-rung offer ladder; it does not set prices.

The machine sells one focused offer to the market — the **Governed Revenue Ops Diagnostic** — which maps where revenue workflows, CRM/data quality, and AI usage create risk or missed value, and produces three practical decisions plus a Proof Pack. That offer maps onto the existing ladder rungs (Free Mini Diagnostic, or the 499 SAR Revenue Proof Sprint).

---

## 2. The 16-state funnel — قمع الإيراد بستّ عشرة حالة

### State diagram — مخطّط الحالات

```
                              visitor
                                 |
                          lead_captured
                                 |
                          [ A/B/C/D scorer ]
                       /         |          \
              qualified_A   qualified_B    nurture
                       \         |          /
                          meeting_booked
                                 |
                          meeting_done
                                 |
                          scope_requested
                                 |
                          scope_sent  ......... (scope approved in writing)
                                 |
                          invoice_sent
                                 |
                          invoice_paid
                                 |
                          delivery_started
                                 |
                          proof_pack_sent
                                 |
                          upsell_sprint
                                 |
                          retainer_candidate   [terminal — positive]

   closed_lost  <---- reachable from ANY non-terminal state above
                      [terminal — negative]
```

### State list — قائمة الحالات

| # | State | Meaning |
|---|---|---|
| 1 | `visitor` | Anonymous arrival on a landing page. No PII yet. |
| 2 | `lead_captured` | A form submission with consent recorded. |
| 3 | `qualified_A` | Scorer grade A — highest readiness. |
| 4 | `qualified_B` | Scorer grade B — minor clarification needed. |
| 5 | `nurture` | Grade C/D — not now; routed to a lighter rung or held. |
| 6 | `meeting_booked` | A diagnostic review time is confirmed. |
| 7 | `meeting_done` | The review call has happened. |
| 8 | `scope_requested` | The customer asked for a scope of work. |
| 9 | `scope_sent` | A scope draft has been delivered for written approval. |
| 10 | `invoice_sent` | An invoice has been sent — only after scope approval. |
| 11 | `invoice_paid` | Payment confirmed. |
| 12 | `delivery_started` | Diagnostic work has begun — only after payment. |
| 13 | `proof_pack_sent` | The 14-section Proof Pack has been delivered. |
| 14 | `upsell_sprint` | A next-step proposal — only after a Proof Pack exists. |
| 15 | `retainer_candidate` | The engagement shows recurring value (positive terminal). |
| 16 | `closed_lost` | Reachable from any non-terminal state (negative terminal). |

`retainer_candidate` and `closed_lost` are terminal. Every other state can transition to `closed_lost`.

---

## 3. The 5 hard ordering rules — القواعد الخمس الصارمة للترتيب

These are non-negotiable transition rules. The machine refuses an illegitimate transition before it happens.

1. **No invoice before scope.** `invoice_sent` is reachable only after `scope_sent` with a recorded written approval. — لا فاتورة قبل نطاق موافَق عليه كتابةً.
2. **No delivery before payment.** `delivery_started` is reachable only after `invoice_paid`. — لا تسليم قبل دفع.
3. **No proof pack before delivery.** `proof_pack_sent` is reachable only after `delivery_started`. — لا حزمة إثبات قبل بدء التسليم.
4. **No upsell before proof pack.** `upsell_sprint` is reachable only after `proof_pack_sent`. — لا ترقية قبل حزمة إثبات.
5. **No case study before written approval.** A delivered engagement becomes a public/anonymized case asset only with the customer's separate written approval. — لا دراسة حالة قبل موافقة مكتوبة.

A transition that violates any rule is rejected, logged, and surfaced to the operator. There is no override flag.

---

## 4. The A/B/C/D lead scorer — مُسجِّل العملاء A/B/C/D

Every `lead_captured` record is scored by a published, deterministic rule — not a gut feel.

### Scoring formula — معادلة التسجيل

**Positive signals — إشارات إيجابيّة:**

| Signal | Points |
|---|---|
| Decision maker is present | +3 |
| Company uses a CRM | +3 |
| Has AI / revenue-automation usage | +3 |
| GCC B2B activity | +2 |
| Urgency within 30 days | +2 |
| Budget 5,000+ SAR | +2 |

**Negative signals — إشارات سلبيّة:**

| Signal | Points |
|---|---|
| Student / jobseeker | -3 |
| No operating company | -3 |
| Vague curiosity (no defined problem) | -2 |

### Grade thresholds — عتبات التصنيف

| Total score | Grade |
|---|---|
| `>= 10` | A |
| `6 – 9` | B |
| `3 – 5` | C |
| `< 3` | D |

### Grade → route mapping — ربط التصنيف بالمسار

| Grade | Funnel state | Route |
|---|---|---|
| A | `qualified_A` | Direct to a diagnostic review; suggest the 499 SAR Revenue Proof Sprint rung. |
| B | `qualified_B` | Diagnostic review after minor clarification; rung suggested on the call. |
| C | `nurture` | Routed to the Free Mini Diagnostic rung; revisit later. |
| D | `nurture` | Held or referred to a better-fit path; no offer pushed now. |

The scorer is transparent on purpose: it protects both sides. The machine never routes a not-ready lead to a high rung. See `LINKEDIN_POST_013.md` for the customer-facing explanation.

---

## 5. The 6 ops systems — أنظمة التشغيل الستّة

Each ops system owns one funnel touchpoint and produces one artifact. Each artifact is a draft until the founder approves it. The matching customer-facing copy lives in `REVENUE_OPS_EMAIL_TEMPLATES.md`.

| # | Ops system | Funnel touchpoint | Produces |
|---|---|---|---|
| 1 | Lead follow-up | `lead_captured` → graded | A bilingual follow-up draft matched to the lead's grade and rung. |
| 2 | Booking invite | `qualified_A/B` → `meeting_booked` | A booking-invite draft with prep checklist. |
| 3 | Meeting brief (internal) | `meeting_booked` → `meeting_done` | An internal-only brief — grade, signals, target decision. Never sent externally. |
| 4 | Scope cover note | `scope_requested` → `scope_sent` | A scope-of-work draft plus cover note; states deliverables, exclusions, rung price. |
| 5 | Invoice cover note | `scope_sent` (approved) → `invoice_sent` | An invoice cover-note draft reflecting the signed scope exactly. |
| 6 | Proof-pack delivery note | `delivery_started` → `proof_pack_sent` | A delivery-note draft accompanying the 14-section Proof Pack. |

A seventh touchpoint — the sprint upsell note (`proof_pack_sent` → `upsell_sprint`) — is produced only when the Proof Pack shows value recurs. It is not a standing ops system; it fires conditionally.

The Proof Pack itself has 14 sections: executive_summary, problem, inputs, source_passports, work_completed, outputs, quality_scores, governance_decisions, blocked_risks, value_metrics, limitations, recommended_next_step, capital_assets_created, appendices. See the Sample Proof Pack at `/assets/proof/sample-proof-pack.html`.

---

## 6. The draft → gate → approval-queue flow — مسار المسوّدة ← البوّابة ← طابور الاعتماد

Nothing the machine produces is sent externally automatically. Every message, scope, invoice, and Proof Pack moves through three steps:

```
   [ machine produces artifact ]
                |
            DRAFT  ......... artifact exists, marked draft_only, not yet visible externally
                |
            GATE   ......... governance check: ordering rules, PII redaction, scope/price
                |             consistency. A failed gate stops the artifact here and logs why.
                |
   APPROVAL QUEUE  ......... the artifact waits for the founder. The founder edits, approves,
                |             or rejects. Rejection returns it to draft with a note.
                |
            SEND   ......... only an approved artifact is sent. The send is logged with the
                              approver, timestamp, and the gate result it cleared.
```

Operator notes:

- The gate enforces the 5 hard ordering rules. An artifact for an out-of-order state never reaches the queue.
- PII is redacted at the gate before an artifact is shown in any internal review surface beyond the founder.
- No artifact carries a guaranteed sales number, conversion rate, or ROI claim. The gate flags guarantee-language for the founder to remove.
- The approval queue is the single choke point. If the founder is unavailable, artifacts wait — they do not auto-release.
- The public landing form (`/dealix-diagnostic`) posts to the public endpoint `/api/v1/public/demo-request`. Admin-only capture routes are never exposed on a public page.

---

## 7. What the machine never does — ما لا تفعله الآلة أبداً

- No scraping, no cold WhatsApp automation, no LinkedIn automation, no bulk outreach.
- No external send without explicit founder approval in the queue.
- No promised sales numbers, conversion rates, or ROI as fact — only estimated, evidenced opportunities.
- No invoice before a signed scope; no delivery before payment; no proof pack before delivery; no upsell before a proof pack; no case study before written approval.
- No new prices invented. The machine routes leads onto the unchanged 5-rung ladder.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
