# Enterprise Master Services Agreement (MSA) — Template

> **Purpose:** boilerplate MSA for customers > 50 employees signing R7 (Enterprise PMO) or large R5 (Bespoke AI) contracts.
> **NOT for SMB:** standard Terms of Service (`landing/terms.html`) covers customers under R1–R4.
> **Disclaimer:** this is a STARTING POINT. ALL enterprise contracts must be reviewed by Saudi legal counsel (e.g., Tamimi & Co, Clyde & Co Riyadh) before signature. Dealix accepts no liability for use without qualified legal review.

---

## 1. Parties

**Service Provider:** Dealix [official entity name to be inserted], a [legal form] registered in the Kingdom of Saudi Arabia under Commercial Registration No. {CR_NUMBER}, with registered address at {ADDRESS}, Riyadh, Saudi Arabia.

**Customer:** [Customer legal entity name], with Commercial Registration No. {CUSTOMER_CR}, with registered address at {CUSTOMER_ADDRESS}.

## 2. Services Description

Dealix shall provide the following services to Customer:

- [ ] R1 Managed Pilot (7-day)
- [ ] R2 SaaS Subscription (specify tier: Starter / Growth / Scale)
- [ ] R3 Lead-as-a-Service (specify model: Per-Reply / Per-Demo / Flat-Rate)
- [ ] R4 Sector Intelligence Reports (specify cadence)
- [ ] R5 Bespoke AI Service Setup (specify scope in Annex A)
- [ ] R7 Enterprise PMO (specify scope in Annex B)

Detailed scope: see Annex A and Annex B.

## 3. Service Levels

- **Uptime SLA:** 99.5% monthly (excluding scheduled maintenance windows announced ≥ 48h in advance)
- **First-response SLA:** business-hours support (Sun–Thu 09:00–17:00 AST), 4-hour first response
- **Critical incident SLA:** P0 incidents (data breach, full outage) — 30-minute first response, 24/7
- **PDPL request response SLA:** within 30 days per Art. 13–14
- **Failed-month remedy:** if uptime falls below 99.0% in any calendar month, Customer receives a 25% credit on next month's subscription

## 4. Fees and Payment

- Recurring fee: {AMOUNT} SAR per month, payable monthly in advance via {METHOD: Moyasar / bank transfer}
- One-time setup fee: {AMOUNT} SAR, payable upon signature
- Metered LaaS fees: per `docs/business/PRICING_AND_PACKAGES.md` Tier 5 (Per-Reply 25 SAR, Per-Demo 150 SAR)
- All fees exclude VAT (15% Saudi VAT applied per ZATCA Phase 2 invoice)
- Late payment: 30-day grace period, then 1.5% monthly interest per Saudi commercial law

## 5. Term and Termination

- **Initial term:** 12 months from Effective Date
- **Renewal:** automatic 12-month renewals unless either party gives 60-days written notice
- **Termination for cause:** either party may terminate immediately on material breach uncured within 30 days of written notice
- **Termination for convenience:** Customer may terminate with 90-days written notice, prorated refund of any prepaid services
- **Effect of termination:** Customer data exported within 30 days per PDPL Art. 14; Dealix retains required records per Art. 18 (5 years) but no further processing

## 6. Data Protection (PDPL Compliance)

This section is the centerpiece of any Saudi enterprise contract.

### 6.1 Roles

- Customer is the **Data Controller** of end-customer personal data
- Dealix is the **Data Processor** acting on Customer's documented instructions

### 6.2 Processor Obligations

Dealix shall:
1. Process personal data only on Customer's documented instructions
2. Ensure all personnel are bound by confidentiality
3. Implement security measures appropriate to risk (see Annex C: Security Measures)
4. Engage sub-processors only with Customer's prior written consent (current list: `landing/sub-processors.html`)
5. Assist Customer with data subject requests (Art. 13–14) at no additional charge
6. Notify Customer of any personal data breach within **24 hours** of discovery (Dealix's tighter SLA than the 72-hour SDAIA mandate)
7. At termination, delete or return all personal data per Customer's election

### 6.3 Cross-Border Transfers

- Dealix uses Anthropic (US) and OpenAI (US) as LLM sub-processors
- Backups stored in AWS me-south-1 (Bahrain — within GCC, no cross-border transfer)
- All cross-border transfers are subject to SDAIA-approved Standard Contractual Clauses or equivalent

### 6.4 Audit Rights

Customer (or its DPO) may audit Dealix's PDPL compliance:
- Up to once per year, with 30-days notice
- Limited to documents/processes relevant to processing of Customer's data
- Dealix accepts certifications by reputable third parties (e.g., ISO 27001 once obtained) in lieu of on-site audit

## 7. Intellectual Property

- Dealix retains all IP in the Service software, models, and infrastructure
- Customer retains all IP in Customer Data
- Dealix grants Customer a non-exclusive, non-transferable license to use the Service during the Term
- Customer grants Dealix a limited license to process Customer Data solely to provide the Service
- Anonymized, aggregated insights derived from Customer Data may be used by Dealix for product improvement (Customer may opt out)

## 8. Indemnification

- Dealix indemnifies Customer against third-party IP infringement claims arising from Customer's use of the Service per these terms
- Customer indemnifies Dealix against third-party claims arising from Customer's data, content, or unauthorized use
- Indemnification cap: 12 months of fees paid (gross negligence and willful misconduct excluded from cap)

## 9. Limitation of Liability

- Aggregate liability cap: 12 months of fees paid prior to the incident
- Excluded: gross negligence, willful misconduct, breach of confidentiality, breach of Section 6 (Data Protection)
- No indirect, consequential, or punitive damages

## 10. Governing Law and Dispute Resolution

- **Governing law:** Laws of the Kingdom of Saudi Arabia
- **Jurisdiction:** courts of Riyadh
- **First-line dispute resolution:** 30-day good-faith negotiation between executives
- **Arbitration (optional):** SCCA (Saudi Center for Commercial Arbitration), Riyadh seat, Arabic + English language, 1 arbitrator

## 11. General Provisions

- **Entire agreement:** this MSA + Annexes supersedes all prior agreements
- **Amendments:** in writing, signed by both parties
- **Force majeure:** standard exceptions (war, pandemic, government action) suspend performance obligations
- **Assignment:** neither party may assign without written consent, except in change of control of the other party
- **Notices:** to legal addresses listed above, by registered mail or email with read receipt
- **Severability:** if any provision is invalid, the rest survives
- **Counterparts:** electronic signature acceptable; both parties retain copies

---

## Annexes

### Annex A — Bespoke AI Service Scope (R5)
[To be filled per contract]

### Annex B — Enterprise PMO Scope (R7)
[To be filled per contract]

### Annex C — Security Measures
[Standard list: encryption at rest + transit, access controls, MFA, audit logging, incident response, vulnerability scanning, regular pen-tests]

### Annex D — Sub-Processors List
- Anthropic (LLM inference, US)
- OpenAI (LLM inference, US)
- Moyasar (payments, KSA)
- Meta (WhatsApp Business Cloud, US/EU/regional CDN)
- Resend or SendGrid (transactional email, US)
- AWS me-south-1 (backups, Bahrain)
- Google Cloud (Maps API, US)
- Hunter.io (email enrichment, France)
- Firecrawl (content extraction, US)
- Wappalyzer (tech fingerprint, US)

### Annex E — PDPL Compliance Plan
- Reference: `integrations/pdpl.py` artifacts
- DPO contact: per `docs/legal/DPO_APPOINTMENT_TEMPLATE.md`

### Annex F — Service-Level Agreement Details
[Defines incident severities, response times, credit calculations]

### Annex G — Pricing Schedule
[Detailed pricing, payment terms, currency, escalation clauses]

---

## Signature Block

**For Dealix:**
Name: ________________________________
Title: ________________________________
Signature: ____________________________
Date: ________________________________

**For Customer:**
Name: ________________________________
Title: ________________________________
Signature: ____________________________
Date: ________________________________

---

## Reviewer Notes (Internal — Strip Before Sending)

Before sending this template to a customer:

- [ ] Replace ALL `{PLACEHOLDER}` values
- [ ] Verify ALL Annexes are populated with customer-specific content
- [ ] Have Saudi legal counsel review (mandatory)
- [ ] Confirm pricing matches `api/routers/pricing.py` PLANS dict
- [ ] Confirm sub-processors list matches current `landing/sub-processors.html`
- [ ] Confirm SLA matches current operational capacity (don't promise what you can't deliver)
- [ ] Have customer's legal review and negotiate
- [ ] Counter-sign only after CTO and DPO approvals
