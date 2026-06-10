# Dealix Strategic Opportunities

This roadmap ranks opportunities by impact, execution risk, and value for Saudi B2B customers.

## P0 — Convert readiness into revenue

| Opportunity | Why it matters | First implementation |
|---|---|---|
| Live demo request loop | Converts website traffic into founder pipeline. | Verify demo endpoint, inbox/CRM routing, response SLA, and Arabic/English fields. |
| Production smoke evidence | Builds operator confidence before campaigns. | Keep Production Smoke workflow recent and attach reports to release notes. |
| Clear checkout readiness | Prevents paid traffic waste. | Verify pricing copy, payment provider mode, callback URL, and webhook secret. |
| Public status route | Gives operators and prospects a simple confidence surface. | Maintain `/status`, API health link, and runbooks. |

## P1 — Enterprise pilot readiness

| Opportunity | Why it matters | First implementation |
|---|---|---|
| Proof Pack for every pilot | Enterprise buyers need traceability. | Connect customer outcome, source evidence, approval status, and owner. |
| No-overclaim evidence flow | Keeps marketing aligned with implementation. | Review `dealix/registers/no_overclaim.yaml` before changing public copy. |
| API contract baseline | Protects dashboards and integrations. | Commit `docs/architecture/openapi.json` once stable and review breaking changes. |
| Admin/auth matrix | Reduces risk in enterprise settings. | Document admin/customer/public route boundaries and tests. |

## P2 — Scale and defensibility

| Opportunity | Why it matters | First implementation |
|---|---|---|
| Agency partner kit | Enables white-label or implementation partners. | Create onboarding, SLA, brand rules, escalation, and sandbox demo kit. |
| Saudi sector playbooks | Improves outbound relevance. | Build playbooks for clinics, logistics, legal, professional services, SaaS, and agencies. |
| Cost-aware AI routing | Protects margin. | Track provider spend, fallback behavior, cache hit rate, and approval class. |
| Bilingual trust center | Reduces sales friction. | Publish concise security, privacy, approval, and compliance answers. |

## P3 — Platform moat

| Opportunity | Why it matters | First implementation |
|---|---|---|
| Benchmark and eval dashboard | Proves AI quality over time. | Add eval set, scoring rubric, and regression trend. |
| Customer health engine | Drives retention and expansion. | Track onboarding progress, usage signals, value events, and risk flags. |
| Marketplace-ready service catalog | Simplifies purchasing. | Standardize packages, outcomes, evidence, pricing, and handoff process. |
| Audit-ready release manifest | Supports enterprise procurement. | Use `make release-manifest` and `make dependency-inventory` for release evidence. |

## What not to do yet

- Do not add heavy dependencies without a clear path to revenue, safety, or reliability.
- Do not automate high-stakes outbound commitments without approval gates.
- Do not publish broad compliance or security claims without evidence.
- Do not start paid traffic until demo, checkout, health, and rollback are verified.

## Arabic summary

أفضل الفرص الآن: تحويل الجاهزية إلى مبيعات، إثبات الديمو والدفع، توثيق الادعاءات، تثبيت API contract، ثم بناء playbooks سعودية وشراكات. لا تضف مكتبات ثقيلة بدون عائد واضح أو دليل تشغيل.
