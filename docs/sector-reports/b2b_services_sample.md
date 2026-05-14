# B2B Services Sample Sector Report

## تقرير قطاعي توضيحي — خدمات الأعمال (B2B)

> **SYNTHETIC + AGGREGATED.** This is a sample sector report for Saudi B2B services. All numbers are synthetic and aggregated for illustration. No real client data is referenced. K-anonymity ≥ 5 is enforced on every slice.
>
> **اصطناعي ومُجمَّع.** تقرير قطاعي توضيحي لخدمات الأعمال في المملكة العربية السعودية. كل الأرقام اصطناعية لأغراض التوضيح، ولا تستند إلى أي بيانات عملاء حقيقية.

---

## 1. Saudi B2B services landscape — مشهد خدمات الأعمال

Saudi B2B services covers a broad band of organizations selling expertise to other organizations: management consulting, marketing agencies, legal-adjacent advisory, IT integration, training providers, accounting and tax, design studios. Companies in this band are typically small-to-medium in headcount, depend on partner networks and inbound referrals, and rely heavily on individual operators rather than productized workflows.

In the synthetic model, the B2B services band shows the following structural features:

- Median headcount: 18 employees (synthetic).
- Median active client count: 12 (synthetic).
- Median age of "AI use inside operations": 14 months (synthetic).
- Share of organizations where AI use is **declared and documented**: 21% (synthetic).
- Share where AI use is **silent** (employees use AI tools individually with no record): 79% (synthetic).

The silent-use figure is the structurally important one. Where AI use is silent, no Source Passport exists, no workflow owner is named, no governance decision is recorded, and no Proof Pack closes the project. The entire six-stage equation collapses to "individual employee plus public chat tool".

في المعطيات الاصطناعية، تستخدم 79% من الشركات الذكاء الاصطناعي بصورة صامتة: استخدام فردي بلا توثيق وبلا قرار حوكمة. هذه هي الفجوة البنيوية الرئيسية.

---

## 2. Readiness score distribution — توزيع درجة الجاهزية

Across the synthetic B2B services subpopulation (300 organizations), the readiness score distribution is right-skewed. Most organizations cluster between 35 and 60. A small tail sits above 70.

| Score band | Maturity equivalent | Share of synthetic B2B services |
|------------|---------------------|---------------------------------|
| 0 – 29 | Siloed | 14% |
| 30 – 49 | Structured | 41% |
| 50 – 69 | AI-Assisted | 32% |
| 70 – 84 | Governed | 11% |
| 85 – 100 | Orchestrated | 2% |

Dimension averages for B2B services in the synthetic model:

| Dimension | Average score |
|-----------|---------------|
| Leadership alignment | 56 |
| Workflow clarity | 49 |
| Data readiness | 41 |
| Human capability | 52 |
| Governance maturity | 38 |

The pattern is the one observed across the full v1 benchmark: governance is the weakest link, data is the second weakest, leadership and workflow sit in the middle.

---

## 3. Top five friction patterns — أنماط الاحتكاك الخمسة

The synthetic dataset reveals five recurring friction patterns. Each is anonymized; none describes a real organization.

### 3.1 Silent personal-account AI use

A senior consultant pastes client briefs into a public chat tool from a personal account. The output is forwarded directly to the client without review, without source declaration, without a recorded decision. When the engagement closes, no Proof Pack exists; the work cannot be referenced internally or externally.

- **Frequency in synthetic data**: 64% of B2B services organizations show this pattern at least once per month.
- **Standards activated by remediation**: [SOURCE_PASSPORT_STANDARD.md](../23_standards/SOURCE_PASSPORT_STANDARD.md), [AGENT_CONTROL_STANDARD.md](../23_standards/AGENT_CONTROL_STANDARD.md).

### 3.2 Cold outreach via informal channels

A growth team sends WhatsApp messages to unverified numbers obtained from scraped public sources. The messages reference the recipient's company by name. No consent record exists; no opt-in path was offered.

- **Frequency in synthetic data**: 47% of organizations show this pattern.
- **Standards activated**: [RUNTIME_GOVERNANCE_STANDARD.md](../23_standards/RUNTIME_GOVERNANCE_STANDARD.md) — hard-blocks the channel.

### 3.3 Guaranteed-result language in proposals

Proposal drafts contain phrases like "we will close fifteen accounts in the first quarter" or "guaranteed ROI within ninety days". Claim safety checks would refuse such language, but no claim-safety check exists in most B2B services operations.

- **Frequency in synthetic data**: 38% of proposals reviewed in the synthetic dataset.
- **Standards activated**: [RUNTIME_GOVERNANCE_STANDARD.md](../23_standards/RUNTIME_GOVERNANCE_STANDARD.md) — `BLOCK` on guarantee language.

### 3.4 PII in operational logs

Engagement teams paste full email addresses, phone numbers, and decision-maker names into internal chat logs, ticketing systems, and analytics dashboards. The logs are retained beyond the engagement's lifetime. No retention policy is applied.

- **Frequency in synthetic data**: 58% of organizations.
- **Standards activated**: [SOURCE_PASSPORT_STANDARD.md](../23_standards/SOURCE_PASSPORT_STANDARD.md) — retention policy enforcement.

### 3.5 Workflow ownership ambiguity

When asked "who owns the lead-prep workflow", the synthetic organization gives three different answers from three different operators. The workflow exists in practice but not on paper. Hand-offs are ad hoc. Quality varies operator-to-operator.

- **Frequency in synthetic data**: 71% of organizations.
- **Standards activated**: [DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md](../23_standards/DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md) — Stage 2 Workflow Owner artifact.

---

## 4. Recommended next steps — الخطوات التالية الموصى بها

For a B2B services organization assessing itself against this report, the recommended sequence is:

1. **List your ten most-used data sources** and assign each a Source Passport. Budget: half a day.
2. **Name a Workflow Owner for each AI-assisted workflow** in writing. Budget: one day.
3. **Adopt the seven-decision governance vocabulary on paper** before tooling. Every external-bound output gets a one-line decision tag. Budget: one team workshop.
4. **Close your next engagement with a Proof Pack** conforming to the fourteen-section schema. Budget: half a day at engagement close.
5. **Publish your operating cadence** — daily standup, weekly review, monthly Proof Pack assembly — and run it for sixty days.

After sixty days of consistent execution on these five items, an organization typically moves one maturity level in the framework, in the synthetic model.

بعد ستين يوماً من الالتزام بالخطوات الخمس، تنتقل الشركة عادةً مستوى نضج واحداً في الإطار وفق النموذج الاصطناعي.

---

## 5. Methodology — المنهجية

- **Synthetic and aggregated data only.** No real client data contributed to the numbers in this report.
- **Subpopulation**: 300 synthetic B2B services organizations sampled from the v1 benchmark dataset, with parameters disclosed in [SAUDI_AI_OPERATIONS_READINESS_REPORT_v1.md](../41_benchmarks/SAUDI_AI_OPERATIONS_READINESS_REPORT_v1.md) section 8.
- **K-anonymity ≥ 5** on every cell. No slice in this report falls below the threshold.
- **No naming.** No organization is named, characterized, or identifiable.
- **No claims.** Numbers are illustrative of the framework. They are not measurements of any real population.

---

## 6. Limitations — حدود التقرير

- The synthetic model encodes qualitative priors. Real-world distributions may differ in magnitude.
- The B2B services band is broad. A single subsector (e.g. management consulting) may differ materially from another (e.g. design studios). v2 will model subsectors where the synthetic sample supports it.
- The five friction patterns are recurring patterns in the synthetic model, not the only patterns. Sector-specific friction (regulatory exposure, channel restrictions, language requirements) is not fully modeled in v1.
- This report does not measure compliance with the Saudi Personal Data Protection Law or sectoral regulation.

---

## 7. Cross-references — مراجع متقاطعة

- [SAUDI_AI_OPERATIONS_READINESS_REPORT_v1.md](../41_benchmarks/SAUDI_AI_OPERATIONS_READINESS_REPORT_v1.md).
- [DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md](../23_standards/DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md).
- [SOURCE_PASSPORT_STANDARD.md](../23_standards/SOURCE_PASSPORT_STANDARD.md).
- [RUNTIME_GOVERNANCE_STANDARD.md](../23_standards/RUNTIME_GOVERNANCE_STANDARD.md).
- [PROOF_PACK_STANDARD.md](../23_standards/PROOF_PACK_STANDARD.md).
- [AGENT_CONTROL_STANDARD.md](../23_standards/AGENT_CONTROL_STANDARD.md).
- [PARTNER_COVENANT.md](../40_partners/PARTNER_COVENANT.md).

---

## 8. Disclaimer — إخلاء مسؤولية

This is a sample sector report. The data is synthetic and aggregated; the numbers illustrate the framework rather than measure any real organization or population. Decisions made on the basis of this report should be paired with first-party assessment of the operating context.

هذا تقرير قطاعي توضيحي. البيانات اصطناعية ومُجمَّعة. الأرقام توضّح الإطار ولا تقيس أي جهة أو سوق حقيقي. أي قرار يُبنى عليه يجب أن يُسنَد بتقييم ذاتي مباشر.
