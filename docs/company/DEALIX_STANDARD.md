# The Dealix Standard

Dealix delivers AI Operations through eight standards:

1. **Data Ready**
2. **Process Clear**
3. **Human Approved**
4. **Source Grounded**
5. **Quality Scored**
6. **Governance Checked**
7. **Proof Delivered**
8. **Expansion Planned**

**No client delivery is complete unless all eight standards are satisfied** (document any exception in `clients/<client>/governance_events.md` with founder approval).

Canonical links: [`DEALIX_OPERATING_KERNEL.md`](DEALIX_OPERATING_KERNEL.md) · [`EVIDENCE_SYSTEM.md`](EVIDENCE_SYSTEM.md) · [`COMPOUNDING_SYSTEM.md`](COMPOUNDING_SYSTEM.md).

---

## 1. Data Ready

AI implementation does not start without understanding the data.

**Questions**

- What is the **source** of the data?
- Does it contain **PII**? Under what lawful basis?
- Is it **complete enough** for the promised output?
- Is there **duplication** or conflicting records?
- Is use **permitted** (license, export, consent, contract)?
- Do we know the **purpose** of processing (proportionality)?

**If unclear:** run a Data Readiness / Lead Intelligence intake; do not promise full automation first.

---

## 2. Process Clear

Do not automate what you cannot explain on one page.

**Questions**

- Who **starts** the process?
- What are **inputs** and **outputs**?
- Who **reviews** and who **approves**?
- What are **failure modes** and fallbacks?
- What **KPI** proves the workflow works?

Use: `docs/assets/templates/workflow_map_template.md`, service delivery checklists.

---

## 3. Human Approved

Any **external** or **sensitive** action requires explicit human approval.

**Examples**

- Sending email or messages on behalf of the client
- WhatsApp (draft-only; no cold automation)
- Publishing claims about results or ROI
- Using PII in models, reports, or demos
- Sharing a report that still contains client-identifiable fields

See: `docs/governance/APPROVAL_MATRIX.md`.

---

## 4. Source Grounded

For knowledge and client-facing reports: **no unsupported statements**.

```text
No source = no answer
```

Company Brain and research-style outputs must cite client-approved sources or return **insufficient evidence**.

---

## 5. Quality Scored

Every client-facing output has a **QA score** before delivery targets (see `docs/quality/OUTPUT_QA_SCORECARD.md` and service QA checklists).

---

## 6. Governance Checked

Every output passes: **PII** · **claims** · **outbound policy** · **source attribution** · **approvals** · **auditability**.

Scripts: `scripts/verify_governance_rules.py`, `scripts/verify_ai_output_quality.py`.

---

## 7. Proof Delivered

Every project ends with a **Proof Pack**: what was done, on what data, with what risks, and what the client should do next.

Templates: `docs/templates/proof_pack.md`, `clients/<client>/06_proof_pack.md`.

---

## 8. Expansion Planned

Every project ends with a clear **next step** toward **self-use**, **pilot extension**, **retainer**, or **enterprise** packaging — captured in `07_next_steps.md` and `POST_PROJECT_REVIEW.md` (retainer opportunity).
