# V12 — Full-Ops 9-OS Architecture

V12 turns Dealix from "production live" → "Full-Ops platform with 9 cooperating operating systems" — without flipping any live gate, scraping, fabricating proof, or rebuilding what exists.

## The 9 OSes

For each OS the table below answers: **what the founder gets, who serves it inside Dealix, what's in vs out, and how status is honestly reported (live | partial | target)**.

| # | OS | Status | Backing module | V12 router | What ships in V12 | What stays target |
|---|---|---|---|---|---|---|
| 1 | **Growth OS** | partial → ✅ wrapper | `growth_v10` | `/api/v1/growth-os` | segment hints, channel safety, Arabic outreach drafts (draft_only), experiment scaffolding | full keyword radar, automated A/B |
| 2 | **Sales OS** | partial → ✅ wrapper | `crm_v10` + `email/reply_classifier` | `/api/v1/sales-os` | lead score, qualification, objection draft, meeting prep, no-guarantee posture | live deal-room collab, full forecast |
| 3 | **Support OS** | minimal → ✅ NEW | NEW `support_os/` | `/api/v1/support-os` | Arabic Saudi classifier (12 cats), P0–P3 SLA, knowledge-base answers, escalation triggers, draft_only responses | bulk dashboard, CSAT loop, team assignment |
| 4 | **Customer Success OS** | partial → ✅ wrapper | `customer_success` | `/api/v1/customer-success-os` | health score (0–100), weekly check-in draft, renewal-risk hint | onboarding workflow engine |
| 5 | **Delivery OS** | partial → ✅ wrapper + checklist | `delivery_factory` | `/api/v1/delivery-os` | service session schema, deliverable checklist, SLA tracker stub | full multi-tenant delivery board |
| 6 | **Partnership OS** | minimal → ✅ NEW | NEW `partnership_os/` | `/api/v1/partnership-os` | partner profile, fit score (0–100), motion picker, manual referral log | white-label, revenue share automation |
| 7 | **Compliance OS** | partial → ✅ action policy | `compliance_os` + NEW `compliance_os_v12/action_policy` | extended `/api/v1/customer-data-plane/action-check` | structured action × consent matrix, escalation for delete/export | DSR dashboard UI, SDAIA exports |
| 8 | **Executive OS** | partial → ✅ wrapper + daily-brief | `executive_reporting` | `/api/v1/executive-os` | top-3 daily decisions, weekly pack, risk summary, no-fake-forecast posture | board-pack PDF, multi-period KPIs |
| 9 | **Self-Improvement OS** | partial → ✅ wrapper + prompt-quality stub | `self_growth_os` | `/api/v1/self-improvement-os` | weekly learning summary, prompt quality stub (suggest_only), service gap hints | full A/B prompt evolution |

## Cross-cutting layers

| Layer | Files | Purpose |
|---|---|---|
| **Unified WorkItem** | `auto_client_acquisition/full_ops/{work_item,work_queue,prioritizer,adapters}.py` | Translator over `AgentTask` + `ApprovalRequest` + `JourneyAdvanceRequest`; one type for the daily command center |
| **Daily Command Center** | extended `api/routers/founder.py` + new `api/routers/full_ops.py` | Single endpoint `GET /api/v1/full-ops/daily-command-center` returning all 5 active OS queues + top-3 decisions + blocked actions |
| **Knowledge base** | `docs/knowledge-base/*.md` (7 files) | Source of truth for Support OS answers; bilingual; bilingual escalation policy |
| **Verifier** | `scripts/v12_full_ops_verify.sh` | 11 checks: compileall, V12 tests, V11 verifier re-run, forbidden claims, secret scan, status endpoints, smoke samples |

## Per-OS contract (canonical)

Every OS exposes (at minimum):
- `GET /status` → `{service, status, version, degraded, checks, hard_gates, next_action_ar/en}`
- one or more action endpoints returning `WorkItem`(s) with `action_mode` ∈ {`suggest_only`, `draft_only`, `approval_required`, `approved_manual`, `blocked`}
- `200` always — `degraded=true` + `degraded_sections=[...]` when a sub-component is unavailable; never `5xx`

## Hard rules per OS

| Rule | Growth | Sales | Support | CS | Delivery | Partner | Compliance | Executive | Self-Improvement |
|---|---|---|---|---|---|---|---|---|---|
| no live send | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| no live charge | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| no scraping | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| no cold WhatsApp | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| no fake proof | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| no LinkedIn auto | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| approval-first | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Arabic primary | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Owner mapping

For now (single founder), every OS owner = founder. Once team grows:
- Growth OS / Sales OS → Growth lead
- Support OS / CS OS → Support lead
- Delivery OS → Delivery lead
- Partnership OS / Executive OS → Founder
- Compliance OS → DPO (when hired)
- Self-Improvement OS → Engineering lead

## Bilingual one-liner

**Arabic**: 9 أنظمة تشغيل تتعاون داخل منصة واحدة، كل خطوة خارجية بموافقة المؤسس، كل بيانات حقيقية، لا ادّعاءات مضمونة، لا إرسال حيّ، لا خصم حيّ.

**English**: 9 cooperating operating systems on one platform; every external action passes through founder approval; real data only; no guaranteed claims; no live send; no live charge.
