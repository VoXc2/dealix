# Dealix Full Ops — Architecture Blueprint / مخطط معمارية العمليات الكاملة

> Status: living document · Owner: engineering · Companion to
> `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md` and `docs/COMMERCIAL_WIRING_MAP.md`.

## Context / السياق

**EN.** The founder set out a complete "Full Ops Platform" vision: a public growth
site, a founder ops console, a customer workspace, partner and affiliate portals,
sales/support/marketing/delivery autopilots, an agent orchestrator, and a
governance OS where **every action carries a source, a risk level, an approval
rule, an evidence event, and a KPI**. This document does one job: it maps that
vision onto the repository as it actually exists, so the team builds against
reality instead of re-imagining systems that already ship.

The headline finding from a full repo survey: **most of the vision is already
built** — under different names. Dealix already has the 9 canonical OS modules,
an agent orchestrator, an approval center, evidence/proof ledgers, 156 FastAPI
routers, 442 tests, and the 11 non-negotiables enforced by passing doctrine
tests. The genuine gaps are narrow: config-as-code, the 5-portal frontend, and a
set of partially-built specialist OS modules.

**AR.** وضع المؤسس رؤية كاملة لمنصة عمليات شاملة: موقع نمو عام، كونسول عمليات
للمؤسس، مساحة عمل للعميل، بوابات للشركاء والمسوّقين، وأنظمة تشغيل آلي للمبيعات
والدعم والتسويق والتسليم، ومنسّق وكلاء، ونظام حوكمة حيث **لكل إجراء مصدر ومستوى
خطر وقاعدة موافقة وحدث إثبات ومؤشر أداء**. هذه الوثيقة تربط تلك الرؤية بالمستودع
كما هو فعلياً. النتيجة الأساسية: **معظم الرؤية مبني مسبقاً** تحت أسماء مختلفة.

---

## 1. Vision → Reality map / خريطة الرؤية إلى الواقع

Each vision component and the **existing** module/router that already provides it.
"New this cycle" marks what was scaffolded in the Full Ops architecture pass.

| Vision component | Where it lives today | State |
|---|---|---|
| Public Growth Site | `frontend/src/app/[locale]/{dealix-diagnostic,risk-score,proof-pack,partners,affiliate,support}` + static `landing/*.html` | Route skeleton new this cycle; landing pages live |
| Founder Ops Console | `frontend/src/app/[locale]/ops/*` + existing `dashboard`, `pipeline`, `approvals`, `agents`, `analytics` | Route skeleton new this cycle; core pages live |
| Customer Workspace | `frontend/src/app/[locale]/customer` + `customer-portal`; backend `customer_brain`, `customer_success_os`, `customer_inbox_v10` | Skeleton new; backend live |
| Partner Portal | `frontend/src/app/[locale]/partner/dashboard`; backend partnership skeleton | Skeleton new; backend partial |
| Affiliate Portal | `frontend/src/app/[locale]/affiliate/dashboard` | Skeleton new; backend gap |
| Sales Autopilot | `auto_client_acquisition/sales_os/`, `dealix/intelligence/lead_scorer.py`, `revenue_os/`, `api/routers/sales_os.py` | Live |
| Support Autopilot | `customer_inbox_v10`, `customer_success_os`, `api/routers/customer_inbox_v10.py` | Live; knowledge OS partial |
| Marketing Factory | `autonomous_growth/`, growth modules, `api/routers/campaigns.py` | Partial |
| Delivery Factory | `auto_client_acquisition/delivery_os/`, `delivery_factory/`, `proof_ledger/` | Live |
| Billing Ops | `dealix/payments/` (Moyasar), `dealix/registers/` (ZATCA), `api/routers/payment_ops.py` | Live |
| Approval Center | `auto_client_acquisition/approval_center/`, `governance_os/approval_matrix.py`, `api/routers/approval_center.py` | Live |
| Evidence Ledger | `auto_client_acquisition/evidence_control_plane_os/`, `proof_ledger/` | Live |
| Agent Orchestrator | `auto_client_acquisition/orchestrator/runtime.py`, `agent_mesh_os/`, `agent_governance/`, `platform_core/agent_runtime.py` | Live |
| Governance OS | `governance_os/`, `safe_send_gateway/doctrine.py`, `platform_core/governance.py`, **`policy_config/`** | Live; config-as-code new this cycle |
| 14 operational ledgers | `docs/ledgers/`, `dealix/contracts/`, value/proof/capital stores | Live |
| 11 non-negotiables | `tests/test_no_*.py`, `tests/test_v7_*.py`, `safe_send_gateway/doctrine.py` | Enforced by passing tests |

The 9 canonical OS modules — `data_os`, `governance_os`, `proof_os`, `value_os`,
`capital_os`, `adoption_os`, `friction_log`, `client_os`, `sales_os` — all exist
under `auto_client_acquisition/` and are covered by tests.

---

## 2. The governance contract / عقد الحوكمة

**EN.** Every action in Dealix must satisfy five questions before it runs. This
is not aspirational — it is enforced by code and by passing tests.

1. **Source** — where did the input come from? (`data_os` source attribution)
2. **Risk level** — low / medium / high? (`policy_config/approval_policy.yaml` →
   `governance_os/approval_matrix.py`)
3. **Approval rule** — does a human approve first? (`approval_center/`,
   `safe_send_gateway/doctrine.py`)
4. **Evidence event** — what immutable record is written? (`evidence_control_plane_os/`,
   `proof_ledger/`)
5. **KPI** — which metric does it move? (`value_os/`, `reports/`)

On top sit the **11 non-negotiables** (verbatim, from `tests/test_trust_pack.py`):
no scraping · no cold WhatsApp · no LinkedIn automation · no fake/un-sourced
claims · no guaranteed sales outcomes · no PII in logs · no source-less knowledge
answers · no external action without approval · no agent without identity · no
project without Proof Pack · no project without Capital Asset.

**AR.** كل إجراء في Dealix يجب أن يجيب على خمسة أسئلة قبل تنفيذه — المصدر،
مستوى الخطر، قاعدة الموافقة، حدث الإثبات، ومؤشر الأداء — وفوقها الـ11 خطاً أحمر
لا يُتجاوز، وكلها مفروضة باختبارات ناجحة.

---

## 3. Config-as-code (shipped this cycle) / الإعدادات كشفرة

Governance routing was hardcoded in Python; it is now policy-driven. YAML defaults
are byte-equivalent to the prior literals, so behaviour is unchanged — config
makes governance editable and auditable, never weaker.

| File (`auto_client_acquisition/policy_config/`) | Drives | Consumer |
|---|---|---|
| `approval_policy.yaml` | action → (risk, route) | `governance_os/approval_matrix.py` |
| `claim_policy.yaml` | doctrine reasons + claim keyword guards | `safe_send_gateway/doctrine.py`, `claim_guard.py` |
| `lead_scoring.yaml` | heuristic weights + tiers | `dealix/intelligence/lead_scorer.py` |
| `stage_transitions.yaml` | lead-lifecycle stage graph + required evidence | `stage_guard.py` |

Loader: `policy_config/loader.py` (`load_policy(name)`, cached, `DEALIX_POLICY_DIR`
override). YAML ships in the wheel via `[tool.setuptools.package-data]`.

The doctrine guards stay **Python-authoritative**: config may add codes or reword
reasons; removing a base code hard-fails (`doctrine_codes_missing:*`). Config can
tighten a non-negotiable, never remove it.

---

## 4. Real gap list / قائمة الفجوات الفعلية

What is genuinely not built (vs. imagined as missing):

- **Config-as-code** — 4 policy files shipped this cycle; still hardcoded:
  `agent_permissions.yaml`, `affiliate_rules.yaml`, `partner_rules.yaml`,
  `support_intents.yaml`, `no_build_rules.yaml`.
- **5-portal frontend** — route skeleton shipped this cycle; real portal UI,
  multi-tenant workspace isolation, and role-based routing are not built.
- **Specialist OS modules** — knowledge OS, market power OS, partnership OS are
  skeletons; affiliate/commission engine is a gap.
- **Analytics / BI** — no data warehouse, no self-service dashboards, no cohort
  or funnel tooling.
- **Model ops** — model selection hardcoded; no prompt versioning or A/B testing.

---

## 5. V1–V4 roadmap / خارطة الطريق

Mapped to `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md`. Each phase ships against
existing modules — no new folder taxonomy required.

**V1 — 14 days (Days 0–14).** Public diagnostic + risk-score pages wired to
`leads` API and `lead_scorer`; founder console (`ops/founder`, `ops/sales`,
`ops/approvals`, `ops/evidence`) wired to live routers; partner/affiliate intake
forms. Gate: first paid pilot (499 SAR).

**V2 — 30 days.** Marketing console + campaign engine; support classifier wired
to `customer_inbox_v10`; scope + invoice draft generators; Proof Pack shell.
Gate: 2 pilots completed, 1 proof event.

**V3 — 90 days.** Customer/partner/affiliate portal UIs; agent orchestrator
extensions; governance dashboard; commission + payout engine; delivery
automation. Gate: 10 customers, 3 retainers (per the 90-day plan).

**V4 — post paid-proof.** Multi-tenant client workspace, benchmark engine,
decision-passport builder, GCC Governed AI Ops index.

---

## 6. Module layout decision / قرار بنية الوحدات

The vision proposed a flat layout (`dealix/growth/`, `dealix/sales/`,
`dealix/support/`…). The repo already has the canonical
`auto_client_acquisition/*_os/` layout — 183 modules and 442 tests depend on it.

**Decision: keep the canonical layout.** The vision's flat names are a *conceptual
map*, not folders to create. Refactoring 183 modules and updating 442 tests +
imports to a new scheme would break a production codebase for cosmetic reasons,
with no functional gain. New work uses the existing `*_os/` packages; new
config lives in `auto_client_acquisition/policy_config/`.

---

## 7. Frontend portal map / خريطة بوابات الواجهة

Five portals under `frontend/src/app/[locale]/` (next-intl, AR default + EN):

- **Public growth**: `dealix-diagnostic`, `risk-score`, `proof-pack`, `partners`,
  `affiliate`, `support`
- **Founder ops**: `ops/{founder,sales,marketing,support,partners,affiliates,approvals,evidence}`
- **Customer workspace**: `customer`
- **Partner portal**: `partner/dashboard`
- **Affiliate portal**: `affiliate/dashboard`

Each route is real and navigable; pages render `PortalPlaceholder` via the
`makePortalPage` factory with its scheduled V-phase. Copy lives in the `portals`
namespace of `frontend/messages/{ar,en}.json`.

---

## Footer

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
