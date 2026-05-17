# Dealix Revenue Autopilot — أوتوبايلوت الإيراد

> Doctrine + code map for the governed funnel that turns content and
> outbound into paid diagnostics. Source of truth for the
> `auto_client_acquisition/revenue_autopilot/` package and the
> `/api/v1/revenue-autopilot` router.

> وثيقة الدوكترين وخريطة الكود للقمع المحكوم الذي يحوّل المحتوى والتواصل
> إلى تشخيصات مدفوعة.

---

## 1. Purpose & doctrine — الغرض والدوكترين

Dealix is a **Governed Revenue & AI Operations Company** — not an AI
agency, not a chatbot, not an early SaaS. The Revenue Autopilot is the
machine that proves the market pays for governed revenue and AI
operations. It rests on four pillars:

- **Founder-led trust** — trust comes from the founder.
- **Proof-led funnel** — proof comes before the call.
- **Automated revenue ops** — operation comes from automation.
- **Disciplined approval system** — governance comes from approvals.

Dealix لا تحتاج مزايا أكثر الآن؛ تحتاج ماكينة تثبت أن السوق يدفع مقابل
التشغيل المحكوم للإيراد والذكاء الاصطناعي.

---

## 2. The three governance tiers — درجات الحوكمة الثلاث

| Tier | What it does | الوصف |
|---|---|---|
| **Autopilot** | Internal steps run fully automated — capture, score, log, persist. | الخطوات الداخلية تُؤتمت بالكامل. |
| **Copilot** | Produces a draft or a recommendation for the founder. | يولّد مسودة أو توصية. |
| **Founder Approval** | External / sensitive actions are queued in the Approval Command Center — never auto-executed. | الأفعال الخارجية تُوضع في قائمة الموافقة، ولا تُنفَّذ تلقائيًا. |

Internal steps automate 100%. Every external send, final invoice send,
case-study publish, final diagnosis, and agent action requires founder
approval.

---

## 3. Offer model — نموذج العرض

Dealix sells **one front-door offer** — the 7-Day Governed Revenue & AI
Ops Diagnostic — with two evidence-led follow-ons. Canonical registry:
`auto_client_acquisition/service_catalog/registry.py`.

| `service_id` | Offer | Price (SAR) | Journey stage |
|---|---|---|---|
| `diagnostic_starter_4999` | 7-Day Diagnostic — Starter | 4,999 | `diagnostic` |
| `diagnostic_standard_9999` | 7-Day Diagnostic — Standard | 9,999 | `diagnostic` |
| `diagnostic_executive_15000` | 7-Day Diagnostic — Executive | 15,000 | `diagnostic` |
| `revenue_intelligence_sprint` | Revenue Intelligence Sprint | per scope | `sprint` |
| `governed_ops_retainer` | Governed Ops Retainer | per scope / month | `retainer` |

Path: **Diagnostic → Revenue Intelligence Sprint → Governed Ops Retainer.**

The diagnostic surfaces where revenue leaks, where CRM/data is not ready,
where AI or automation is ungoverned, and the first executable decisions
with evidence.

---

## 4. Lead-score point system — نظام نقاط تقييم العميل

Implemented deterministically in
`auto_client_acquisition/revenue_autopilot/lead_scorer.py`.

| Signal | Points |
|---|---|
| Decision maker | +3 |
| B2B company | +3 |
| Has CRM / revenue workflow | +3 |
| Uses or plans AI | +3 |
| Saudi / GCC | +2 |
| Urgency within 30 days | +2 |
| Budget 5k+ SAR | +2 |
| No company | −3 |
| Student / job seeker | −3 |
| Vague curiosity only | −2 |

| Total points | Tier |
|---|---|
| 12+ | `qualified_A` |
| 8–11 | `qualified_B` |
| 5–7 | `nurture` |
| below 5 | `closed_lost` |

---

## 5. Funnel stages + hard rules — مراحل القمع والقواعد الصلبة

Stage model + transitions: `revenue_autopilot/funnel.py`.

```
new_lead → qualified_A | qualified_B | nurture | partner_candidate
qualified_A/B → meeting_booked → meeting_done
  → scope_requested → scope_sent → invoice_sent → invoice_paid
  → delivery_started → proof_pack_sent
  → sprint_candidate | retainer_candidate
(any active stage → closed_lost)
```

**Hard rules** (enforced by the forward-only transition map):

- No `invoice_sent` without `scope_sent`.
- No `delivery_started` without `invoice_paid`.
- No revenue counted before `invoice_paid` (`is_revenue_countable`).

---

## 6. The 10 automations — الأتمتة العشر

Hooks in `revenue_autopilot/automations.py`. Each mutates the funnel
stage, logs an append-only evidence event, produces **drafts only**, and
routes external actions through the Approval Command Center.

| # | Automation | Tier | Outputs | Approval routed |
|---|---|---|---|---|
| 1 | `lead_capture` | Autopilot + Copilot | Score, assign tier, first-response draft | First-response email |
| 2 | `qualified_lead` | Copilot | Booking email + meeting brief | Booking email |
| 3 | `proof_pack_request` | Autopilot + Copilot | Log request, 2-day follow-up | Follow-up task |
| 4 | `meeting_booked` | Copilot | Pre-call brief + 5 discovery questions | — (internal) |
| 5 | `meeting_done` | Autopilot | Route to `scope_requested` or `nurture` | — (internal) |
| 6 | `scope_requested` | Copilot | Scope doc + invoice draft, tier recommendation | Scope send + invoice |
| 7 | `invoice_paid` | Autopilot + Copilot | Open delivery, onboarding form | Onboarding email |
| 8 | `delivery` | Copilot | Diagnostic workplan + proof pack draft | — (internal) |
| 9 | `proof_pack_sent` | Founder Approval | Final proof pack send, upsell recommendation | Follow-up task |
| 10 | `retainer_sprint_upsell` | Copilot | Sprint + retainer proposal drafts | Both proposals |

Automation 1 runs at lead capture (`POST /lead`). Automations 2–10 run
via `POST /engagements/{id}/automations/{automation_name}`.

---

## 7. Approval-queue policy — سياسة قائمة الموافقة

Automated 100% (no approval): lead capture, scoring, CRM record creation,
meeting brief, follow-up drafts, scope drafts, invoice drafts, onboarding
checklist, proof pack drafts, nurture reminders, evidence logging.

**Never auto-executed — founder approval required:** cold external send,
final invoice send, security/compliance claims, case-study publishing,
final diagnostic conclusion, agent action.

Approvals are created via `approval_center.create_approval` and surface in
`GET /api/v1/revenue-autopilot/engagements/{id}` as `pending_approvals`.

---

## 8. Code map — خريطة الكود

| File | Responsibility |
|---|---|
| `revenue_autopilot/lead_scorer.py` | Deterministic point-system scorer |
| `revenue_autopilot/funnel.py` | Stage model + forward-only transition rules |
| `revenue_autopilot/records.py` | Engagement, evidence, draft, transition schemas |
| `revenue_autopilot/automations.py` | The 10 automation hooks |
| `revenue_autopilot/orchestrator.py` | Engagement lifecycle + JSONL persistence |
| `api/routers/revenue_autopilot.py` | `/api/v1/revenue-autopilot` router |
| `service_catalog/registry.py` | The 5-offering registry |

Persistence: in-memory index + append-only `data/revenue_autopilot.jsonl`
+ operational stream mirror (same pattern as `leadops_spine`).

---

## 9. Non-negotiables alignment — التوافق مع الثوابت

The Revenue Autopilot honors the 11 non-negotiables
(`docs/00_constitution/NON_NEGOTIABLES.md`):

- **`no_live_send` / `no_live_charge`** — automations produce drafts only;
  external sends and invoices are queued, never executed.
- **`no_unbounded_agents`** — every automation has an explicit scope,
  named funnel transition, and evidence event.
- **`no_unaudited_changes`** — every stage move and action is recorded as
  a `StageTransition` or `EvidenceEvent`.
- **`no_unverified_outcomes`** — revenue is countable only at
  `invoice_paid` or later.
- **`no_hidden_pricing`** — all tiers and prices live in the registry.
- **`no_cold_whatsapp` / `no_scraping`** — the autopilot never originates
  cold outbound; it drafts for founder-led, warm channels only.

Tested by `tests/test_revenue_autopilot_*.py`.
