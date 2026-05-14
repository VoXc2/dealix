# Partner Covenant

## ميثاق الشريك

> The six commitments every Dealix Delivery Partner accepts before issuing a single deliverable under the Dealix brand.

A Dealix Delivery Partner is any agency, consultancy, freelancer collective, or in-house team authorized to ship work as "Dealix" or "Dealix Governed". This document is the operating contract attached to that authorization. It is short by design; the depth lives in the standards it references.

شريك التسليم لدى Dealix هو أي جهة مُخوَّلة بإصدار تسليمات تحت اسم Dealix. هذا الميثاق هو العقد التشغيلي المرتبط بهذا التخويل.

---

## 1. The six commitments — الالتزامات الستة

### 1.1 No unsafe automation — لا أتمتة غير آمنة

The partner will not use, build, or ship any of the following on behalf of a Dealix client:

- Web scraping of personal or contact data.
- Cold WhatsApp outreach to numbers without prior opt-in or a clear lawful basis.
- LinkedIn automation, including connection sending bots, scraping, or scheduled bulk publishing.
- Bulk outreach campaigns that bypass channel-specific consent rules.

These items are hard-blocked in the runtime; attempting them inside Dealix tooling fails closed. The partner agrees not to attempt the same outside Dealix tooling on Dealix engagements.

### 1.2 No guaranteed claims — لا ضمانات

The partner will not make any of the following claims to a client, in writing or otherwise:

- Guaranteed sales numbers, conversion rates, or revenue outcomes.
- ROI presented as fact rather than as an estimated or observed range.
- "We will close X deals" language under any framing.

Claim safety is enforced by the runtime governance layer. Any output containing guarantee language is blocked at the boundary, regardless of who drafted it.

### 1.3 Proof Pack required on every delivery — حزمة إثبات لكل تسليم

The partner will produce a Proof Pack at the close of every engagement, conforming to [PROOF_PACK_STANDARD.md](../23_standards/PROOF_PACK_STANDARD.md).

- The Proof Pack must score at least 70 to ship the engagement.
- The Proof Pack must score at least 80 to pitch a retainer extension on the same client.
- Engagements that fail to meet 70 trigger a remediation cycle before invoice.

### 1.4 QA review accepted — قبول مراجعة الجودة

The partner accepts the Dealix QA rubric on all deliverables shipped under the Dealix brand. QA review covers:

- Source Passport coverage on every output.
- Governance status on every external-bound output.
- Bilingual completeness where the engagement is bilingual.
- Doctrine compliance: the eleven non-negotiables (no scraping, no cold WhatsApp, no LinkedIn automation, no fake claims, no guaranteed sales, no PII in logs, no source-less answers, no external action without approval, no agent without identity, no project without Proof Pack, no project without Capital Asset).

QA may request revisions. The partner accepts up to two QA cycles per engagement at no extra cost to the client.

### 1.5 Governance rules accepted — قبول قواعد الحوكمة

The partner agrees that every external-bound output produced on a Dealix engagement passes through the runtime governance decision, conforming to [RUNTIME_GOVERNANCE_STANDARD.md](../23_standards/RUNTIME_GOVERNANCE_STANDARD.md).

- The seven decision values are not negotiable.
- A `BLOCK` decision is final until its underlying condition is changed.
- A `REQUIRE_APPROVAL` decision requires a named approver, in writing, before the action proceeds.

The partner may not route around the governance decision via personal accounts, side channels, or out-of-band tools.

### 1.6 Audit rights accepted — قبول حق التدقيق

Dealix may audit any partner-delivered engagement under the following conditions:

- **Quarterly cycle** — a sample of partner engagements is selected each quarter for routine audit.
- **Incident-triggered** — any complaint, doctrine violation report, or operational anomaly may trigger an immediate audit.
- **Scope** — Source Passports, governance decisions, Proof Packs, and the audit chain emitted by `auditability_os`.
- **Notice** — quarterly audits are announced; incident audits may be immediate.

The partner agrees to provide read access to the audit chain for the engagement under review. Personal information is excluded from the audit scope; only counts, hashes, and metadata are inspected.

---

## 2. Strikes and suspension — العقوبات والتعليق

A partner accumulates strikes for violations of the covenant. Strikes are recorded against the partner identity, not against individual operators.

| Strike trigger | Severity |
|----------------|----------|
| Late Proof Pack on a closed engagement | one strike |
| QA cycle exceeded without remediation | one strike |
| Source Passport missing on a shipped output | two strikes |
| Cold outreach via a hard-blocked channel | immediate suspension |
| Guarantee claim shipped to a client | immediate suspension |
| PII exported outside the agreed scope | immediate suspension |
| Any doctrine violation (eleven non-negotiables) | immediate suspension |

Composition:

- Three strikes within ninety days → suspension for at least sixty days, with a re-onboarding cycle required before reinstatement.
- Any "immediate suspension" item → the partner's authorization is revoked the same day; reinstatement is at Dealix's sole discretion.

ثلاث مخالفات خلال تسعين يوماً تؤدي إلى تعليق لا يقل عن ستين يوماً. مخالفة من قائمة الخطوط الحمراء تؤدي إلى تعليق فوري.

---

## 3. Referral program — برنامج الإحالة

A partner who refers a paying client receives 5,000 SAR per closed deal, payable after the client's first invoice clears and the engagement's first Proof Pack is filed.

- Referral records and payouts are tracked in `api/routers/referral_program.py`.
- A referral is invalid if the referred client was already in Dealix's active pipeline.
- A referral payout is forfeited if the engagement triggers an immediate-suspension item within the first ninety days.

تُدفَع مكافأة الإحالة بمقدار خمسة آلاف ريال سعودي لكل صفقة مغلقة، بعد تحصيل أول فاتورة وإصدار حزمة الإثبات الأولى.

---

## 4. Cross-references — مراجع متقاطعة

- [DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md](../23_standards/DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md).
- [SOURCE_PASSPORT_STANDARD.md](../23_standards/SOURCE_PASSPORT_STANDARD.md).
- [RUNTIME_GOVERNANCE_STANDARD.md](../23_standards/RUNTIME_GOVERNANCE_STANDARD.md).
- [PROOF_PACK_STANDARD.md](../23_standards/PROOF_PACK_STANDARD.md).
- [AGENT_CONTROL_STANDARD.md](../23_standards/AGENT_CONTROL_STANDARD.md).

---

## 5. Disclaimer — إخلاء مسؤولية

This covenant is operational, not a substitute for the underlying Partner Legal Agreement. In any conflict between this covenant and the signed agreement, the signed agreement controls. This covenant does not by itself create a legal partnership, joint venture, or employment relationship.

هذا الميثاق وثيقة تشغيلية ولا يُغني عن اتفاقية الشراكة القانونية الموقَّعة. عند أي تعارض، تُعتمَد الاتفاقية الموقَّعة. لا يُنشئ هذا الميثاق وحده شراكة قانونية ولا علاقة عمل.
