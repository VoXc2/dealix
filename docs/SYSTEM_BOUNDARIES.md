# System Boundaries — Dealix

> **Last updated:** 2026-06-03 · **Owner:** Agent #35 (Final Integration) · **Version:** v1.0
> **Purpose:** for each system, what is in scope, out of scope, and what crosses into another system. Prevents duplicate work.

---

## 1) Enterprise Sales OS (Agent 29)

| | |
|---|---|
| **In scope** | ABM list, Tier-1/2/3, TAP, Stakeholder mapping, Buying Committee, Discovery, Mutual Action Plan, Executive Business Case, Pilot → Expansion, Deal Risk review, Procurement RFP/RFI |
| **Out of scope** | Day-to-day delivery inside the client (post-pilot). Code/configuration. UI/UX. Network/infra. |
| **Crosses into** | (a) **Delivery (legacy)** when pilot SOW is signed; (b) **Commercial OS** when ICP matches; (c) **AI Governance** when Sales Outreach Agent needs approval; (d) **Data Products** when sector_benchmarks inform ABM scoring; (e) **Legal** when MSA is needed. |

## 2) AI Agent Governance OS (Agent 30)

| | |
|---|---|
| **In scope** | Agent registry, A0-A5 autonomy levels, Permission lifecycle, Onboard/Offboard, Eval cadence, Retirement, Incident Response, Human approval boundaries, vendor agent policy |
| **Out of scope** | Code of individual agents (engineering). Model training/eval details (data_lead). Business logic of what agents do. |
| **Crosses into** | (a) **Security** when P1/P2 incident escalates; (b) **Responsible AI** for ethical use cases; (c) **Engineering** when new agent is registered; (d) **Data Products** for eval data; (e) **all operational systems** (Default-Deny gates every external_action). |

## 3) Data Products OS (Agent 31)

| | |
|---|---|
| **In scope** | Sector benchmarks, Message performance library, Objection intelligence, Offer performance model, Delivery patterns, Renewal triggers, Pricing sensitivity, Learning loop |
| **Out of scope** | Raw data ingestion (Data Governance). Real-time inference. PII handling (Security/Privacy). Sales motion design (Sales). |
| **Crosses into** | (a) **Sales/Offers** when benchmarks drive CTA/landing copy; (b) **CS/Delivery** when renewal triggers fire; (c) **Data Governance** for PII rules; (d) **AI Governance** for agent training data. |

## 4) Offer Landing Pages (Agent 33)

| | |
|---|---|
| **In scope** | 6 offer pages (Diagnostic, Followup, AI Starter, Full OS, Monthly, Custom), FAQ library, CTA library, Arabic-first content |
| **Out of scope** | Post-click onboarding (phase-e). Sales conversation (Sales legacy). Pricing decisions (founder). Brand design (marketing). |
| **Crosses into** | (a) **Sales/Commercial** when CTA → Calendly/WhatsApp; (b) **Phase-E** when user books; (c) **Data Products** when sector_benchmark informs best_offer; (d) **Enterprise Sales** when page targets enterprise segment. |

## 5) Integration Layer (Agent 35)

| | |
|---|---|
| **In scope** | Master index, system map, founder guides, daily/weekly rhythms, priority roadmap, file ownership, system boundaries, anti-duplication policy, integration reports |
| **Out of scope** | Creating new feature systems. Modifying legacy docs. Agent registry. |
| **Crosses into** | (a) **All systems** (cross-references); (b) **founder** for final decisions. |

---

## 6) Legacy Boundaries (Quick Ref)

| System | In scope | Out of scope |
|--------|---------|--------------|
| **Commercial** | ICP, Pricing, Proposals, Follow-up | Code, Delivery execution |
| **Enterprise** | Security, Privacy, Procurement, Support | Sales motion (→ Enterprise Sales) |
| **Enterprise Rollout** | Post-sale adoption inside client | Pre-sale (→ Enterprise Sales) |
| **Delivery** | SOW, SLA, handoff | Sales motion, pricing |
| **Governance** | A0-A5, Approval matrix | Specific agent code |
| **Security** | Prompt injection, keys, OWASP | Sales/marketing |
| **Responsible AI** | Ethics, AI literacy | Specific agent code |
| **Data Governance** | PII, quality, retention | Product use of data (→ Data Products) |
| **Finance** | Unit economics, CAC, pricing | Sales execution |
| **Legal** | DPA, MSA, PDPL | Sales motion |
| **Partnerships** | Channel, referral | Direct sales |
| **Product** | Code, features, evals | Sales/delivery |
| **Strategy** | Roadmap, OKRs | Tactical execution |

---

## 7) Crossings — How to Hand Off

| When | From → To | Handoff Artifact |
|------|-----------|------------------|
| Pilot signed | Enterprise Sales → Delivery | `mutual_action_plans.jsonl` |
| Pilot completed | Delivery → Data Products | `proofs/dealix_v1_proof_pack.json` |
| New agent | Engineering → AI Governance | `agent_registry.jsonl` |
| New data row | Delivery/Sales → Data Products | append to `data/data_products/*.jsonl` |
| CTA clicked | Offers → Sales | webhook → lead |
| Sector benchmark updated | Data Products → Sales/Offers | PR with `data-change` tag |
| Incident P0 | AI Governance → Founder | `data/ai_governance/agent_incidents.jsonl` |
| MSA needed | Sales → Legal | `docs/legal/ENTERPRISE_MSA_TEMPLATE.md` |

---

## 8) Disambiguation Rules

When two systems could claim ownership of a file/concept:

1. **Pre-sale vs Post-sale** → Enterprise Sales (pre) vs Rollout (post)
2. **Raw data vs Products** → Data Governance (raw) vs Data Products (products)
3. **Action gating vs Action execution** → AI Governance (gate) vs the system that executes
4. **Pricing rules vs Pricing decisions** → Sales/Commercial (rules) vs Founder (decisions)
5. **Public page vs Internal doc** → Offers (public) vs the system that owns content

---

## 9) Open Questions for Founder

1. هل هذه الحدود **حادة كفاية**، أم تحتاج `exception cases` إضافية؟
2. من يُقرّر **hand-offs** (الـ 8 في القسم 7) عند نزاع؟ — افتراضياً founder.
3. هل تريد **automated check** (CI) يفرض الـ boundaries (يصدّ PR يخالفها)؟
