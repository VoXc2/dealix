# Dealix Governed AI Operations Standard

## معيار عمليات الذكاء الاصطناعي المحوكمة

> Open Standard, version 1.0. Anyone may implement this standard inside their organization, with their own tools, vendors, and teams. Only delivery branded as "Dealix" or "Dealix Governed" requires a partnership with Dealix.

This document defines the operating equation, required artifacts, maturity model, and adoption rules for running AI inside a Saudi B2B operation in a way that is auditable, governable, and safe by default. It is intended to be quoted, adapted, and implemented openly across sectors.

---

## 1. Why this standard exists — لماذا هذا المعيار

In most Saudi B2B operations today, AI usage is silent: a few employees paste customer data into public chat tools, a few managers receive AI-generated drafts and forward them without review, and a few projects quietly automate outreach without a record. None of this is malicious. All of it is ungoverned.

A governed AI operation does the opposite. Every input has an owner. Every workflow has a step. Every AI run leaves a trace. Every external-bound output passes through a governance decision. Every project closes with a Proof Pack. Every team operates on a known cadence.

This standard names the six stages that turn raw AI usage into governed AI operations, and the artifacts each stage must produce.

في معظم عمليات الأعمال السعودية اليوم، استخدام الذكاء الاصطناعي صامت: يلصق الموظفون بيانات العملاء في أدوات عامة، ويمرر المدراء مسودات لم تُراجَع، وتُؤتمَت قنوات تواصل دون سجل. هذا المعيار يحوّل ذلك الاستخدام الصامت إلى عمليات محوكمة بست مراحل واضحة، لكل مرحلة منها أثر يمكن مراجعته.

---

## 2. The six-stage operating equation — معادلة التشغيل بست مراحل

```
Data  →  Workflow  →  AI  →  Governance  →  Proof  →  Cadence
بيانات  →  مسار عمل  →  ذكاء اصطناعي  →  حوكمة  →  إثبات  →  إيقاع
```

Each stage transforms the previous one. No stage may be skipped. No stage may be merged into another. The minimum required artifact for each stage is named below.

### Stage 1 — Data

Every byte of input that touches an AI run must carry a Source Passport. The Source Passport names the source, its type, its owner, the allowed use, whether it contains PII, its sensitivity, whether AI may access it, whether it may leave the organization, and its retention policy.

- Required artifact: **Source Passport** per dataset, file, channel, or feed.
- Reference spec: [SOURCE_PASSPORT_STANDARD.md](SOURCE_PASSPORT_STANDARD.md).
- Failure mode: data used without a passport must be blocked at the workflow boundary.

### Stage 2 — Workflow

Every AI-assisted activity must be expressed as a named workflow with a named owner. "The AI handles it" is not a workflow. A workflow lists its steps, inputs (with passport references), outputs, and the human accountable for the result. The workflow owner is a person, not a team and not a tool.

- Required artifact: **Workflow Owner record** (name, role, scope, escalation path).
- Failure mode: ungoverned ad-hoc AI use; treat as Stage 0.

### Stage 3 — AI

Every model invocation must be logged: which workflow called it, which sources it read, which tools it could touch, which output it produced, and how long it ran. This is not a research log; it is an operational ledger.

- Required artifact: **AI Run Ledger entry** per invocation.
- Reference: agent identity is governed by [AGENT_CONTROL_STANDARD.md](AGENT_CONTROL_STANDARD.md).
- Failure mode: silent AI usage; immediate remediation required.

### Stage 4 — Governance

Every output that leaves the workflow must pass a governance decision. The decision is one of seven values: `ALLOW`, `ALLOW_WITH_REVIEW`, `DRAFT_ONLY`, `REQUIRE_APPROVAL`, `REDACT`, `BLOCK`, `ESCALATE`. The decision is deterministic, recorded, and never inferred after the fact.

- Required artifact: **Governance Decision record** per external-bound output.
- Reference spec: [RUNTIME_GOVERNANCE_STANDARD.md](RUNTIME_GOVERNANCE_STANDARD.md).
- Failure mode: any output shipped without a recorded decision is a doctrine violation.

### Stage 5 — Proof

Every project closes with a Proof Pack: a fourteen-section artifact that consolidates inputs, sources, outputs, governance decisions, observed value, limitations, and the recommended next step. The Proof Pack carries a numeric score and a tier classification that determines how it may be referenced.

- Required artifact: **Proof Pack** at every project close.
- Reference spec: [PROOF_PACK_STANDARD.md](PROOF_PACK_STANDARD.md).
- Failure mode: project closure without a Proof Pack is forbidden.

### Stage 6 — Cadence

Operations live in time. A governed AI operation runs on a published rhythm: daily standup, weekly review, monthly Proof Pack assembly, quarterly capability review. The cadence is written down. The cadence is followed.

- Required artifact: **Operating Rhythm document** (frequency, owners, agenda, decision log).
- Failure mode: heroic one-off effort without a repeating loop; not governed operations.

---

## 3. Maturity levels — مستويات النضج

A team is classified into one of five maturity levels based on which stages they consistently execute. The level is a description, not a judgment; most Saudi B2B operations today sit at Level 1 or Level 2.

| Level | Name | Description |
|-------|------|-------------|
| 1 | **Siloed** | AI usage is individual, undeclared, and untracked. No passports, no workflows, no decisions. |
| 2 | **Structured** | Workflows exist on paper. Owners are named. AI usage is still mostly ad hoc. |
| 3 | **AI-Assisted** | AI is embedded inside named workflows. Logs exist but governance is informal. |
| 4 | **Governed** | All six stages are present. Every external output has a recorded governance decision. Proof Packs close every project. |
| 5 | **Orchestrated** | Multiple governed workflows interlock under a shared cadence; capital assets compound; partners run under the same standard. |

A team can move up one level per quarter under realistic conditions. Skipping levels is possible but rarely durable.

| المستوى | الاسم | الوصف |
|---------|-------|-------|
| 1 | **مشتّت** | استخدام فردي غير معلن وغير مُتتبَّع. |
| 2 | **منظَّم** | مسارات عمل مكتوبة وأصحاب مسؤولين، لكن استخدام الذكاء عشوائي. |
| 3 | **مُعان بالذكاء** | الذكاء الاصطناعي داخل المسارات، مع سجلات أولية. |
| 4 | **محوكَم** | المراحل الست كلها موجودة، وكل مخرج خارجي يحمل قرار حوكمة. |
| 5 | **منسَّق** | عدة مسارات محوكمة تعمل تحت إيقاع واحد وأصول رأسمالية مشتركة. |

---

## 4. The eleven non-negotiables — الخطوط الحمراء الإحدى عشرة

Conformance with this standard requires conformance with eleven hard rules. These are not preferences; they are the line that separates governed operations from ungoverned ones. The runtime enforces all of them at machine speed; the partner covenant binds humans to them.

1. No scraping of personal or contact data.
2. No cold WhatsApp outreach without prior opt-in or a clear lawful basis.
3. No LinkedIn automation: no connection bots, no scraping, no bulk publishing.
4. No fake claims: no fabricated testimonials, no invented case studies, no impersonation.
5. No guaranteed sales numbers, conversion rates, or ROI presented as fact.
6. No PII in logs, dashboards, or analytics stores.
7. No source-less answers: every output traces to a Source Passport.
8. No external action without an approval path appropriate to the action.
9. No agent without an Agent Card identity.
10. No project without a Proof Pack at close.
11. No project without at least one Capital Asset created.

A violation of any of the eleven by a partner triggers immediate suspension under the Partner Covenant. A violation by an internal team triggers a runtime fault and a friction-log entry. There is no exception path.

أي مخالفة لأي بند من البنود الإحدى عشرة تستوجب توقفاً فورياً ومراجعة. لا توجد استثناءات.

---

## 5. Adoption and licensing — التبني والترخيص

This standard is published openly. Any organization, vendor, consultancy, or in-house team may implement it. Adoption does not require permission, payment, or registration.

The following are explicitly permitted:

- Quoting any section verbatim with attribution.
- Implementing the six stages using any tools, models, or vendors.
- Translating, extending, or adapting the standard for a specific sector.
- Teaching the standard inside a paid program.

The following require a written partnership with Dealix:

- Branding a delivery as "Dealix Governed" or using the Dealix mark in client-facing artifacts.
- Issuing a Proof Pack under the Dealix tier classification as if it were Dealix-certified.
- Operating as a Dealix Delivery Partner under the [Partner Covenant](../40_partners/PARTNER_COVENANT.md).

Dealix gates only its brand and its delivery. The method is open.

هذا المعيار مفتوح. يحق لأي جهة تطبيقه. اسم "Dealix" والتسليم المُعتمَد من Dealix هو ما يتطلب شراكة مكتوبة.

---

## 6. How to start — كيف تبدأ

Implementation does not require a six-month transformation program. A team can begin Stage 1 in a single afternoon.

- **Week one** — list the ten most-used data sources in the organization and issue a Source Passport for each. Stage 1 begins to take shape.
- **Week two** — write down the three most-used AI-affected workflows. Name an owner per workflow. Stage 2 begins.
- **Week three** — adopt the seven-decision governance vocabulary on paper. Every external-bound output gets a one-line decision tag before it ships. Stage 4 begins.
- **Week four** — close the next engagement with a Proof Pack using the fourteen-section schema. Stage 5 begins.
- **Week five and beyond** — publish the operating cadence. Stage 6 begins. The full equation is now running, however lightly.

The standard does not require any specific tool, model, vendor, or platform. It is a description of what governed operations look like; the implementation belongs to the adopting organization.

التطبيق لا يحتاج برنامج تحوّل طويل. خلال خمسة أسابيع يمكن إقامة المراحل الست بصورة أولية. الأدوات والموردون اختيار الجهة المتبنّية.

---

## 7. Conformance — المطابقة

An implementation is conformant with this standard when it satisfies, at minimum:

- Every data source used by an AI workflow has a Source Passport that validates against the schema in [SOURCE_PASSPORT_STANDARD.md](SOURCE_PASSPORT_STANDARD.md).
- Every workflow that calls a model produces an AI Run Ledger entry that names the workflow, the inputs (by passport id), the model invocation, and the outputs.
- Every external-bound output carries a `governance_status` value drawn from the seven decision values defined in [RUNTIME_GOVERNANCE_STANDARD.md](RUNTIME_GOVERNANCE_STANDARD.md).
- Every project closes with a Proof Pack conforming to [PROOF_PACK_STANDARD.md](PROOF_PACK_STANDARD.md), with at least one Capital Asset deposited.
- Every agent that takes an action has an Agent Card conforming to [AGENT_CONTROL_STANDARD.md](AGENT_CONTROL_STANDARD.md), with a named kill-switch owner.

Conformance is a property of the operation, not of any specific tool. Two implementations using entirely different stacks may both be conformant.

---

## 8. Cross-references — مراجع متقاطعة

- [SOURCE_PASSPORT_STANDARD.md](SOURCE_PASSPORT_STANDARD.md) — data layer spec.
- [RUNTIME_GOVERNANCE_STANDARD.md](RUNTIME_GOVERNANCE_STANDARD.md) — seven-decision runtime spec.
- [PROOF_PACK_STANDARD.md](PROOF_PACK_STANDARD.md) — fourteen-section closure artifact.
- [AGENT_CONTROL_STANDARD.md](AGENT_CONTROL_STANDARD.md) — agent identity, autonomy, kill switch.
- [Partner Covenant](../40_partners/PARTNER_COVENANT.md) — partner commitments.
- [Saudi AI Operations Readiness Report v1](../41_benchmarks/SAUDI_AI_OPERATIONS_READINESS_REPORT_v1.md) — benchmark.

---

## 9. Disclaimer — إخلاء مسؤولية

This standard is descriptive, not regulatory. It does not replace the Saudi Personal Data Protection Law, sectoral regulations, or contractual obligations. It is intended to make AI-assisted operations safer and more auditable by default. Organizations remain responsible for their own legal, regulatory, and contractual posture.

هذا المعيار توصيفي وليس تنظيمياً. لا يحل محل نظام حماية البيانات الشخصية ولا الالتزامات التعاقدية. تبقى كل جهة مسؤولة عن وضعها القانوني والتنظيمي.
