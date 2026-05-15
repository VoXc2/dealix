# DPO (Data Protection Officer) Appointment Kit

> **Trigger:** first enterprise customer touch OR Dealix processes data for > 5 customers > 1 year. PDPL doesn't mandate DPO for SMB-scale processing, but Saudi enterprise customers will ask.
> **Cost estimate:** 20–40K SAR per year for part-time external DPO via specialized firm; 8–15K/mo for full-time if internal hire.

---

## Why a DPO?

Personal Data Protection Law (PDPL) Article 32 says:

> "Controllers processing significant volumes of personal data shall designate a Data Protection Officer..."

Dealix qualifies as a "Controller" when handling end-customer data (B2B + their leads' PII). Once we cross ~5 active enterprise customers, we're at the threshold.

## DPO Responsibilities (per PDPL Art. 32–34)

1. Advise on PDPL compliance for new product features
2. Monitor data protection impact assessments (DPIAs)
3. Cooperate with SDAIA (the Saudi Data Authority)
4. Be the point of contact for data subjects (PDPL Art. 13, 14 requests)
5. Maintain Record of Processing Activities (ROPA) — `integrations/pdpl.py` already produces these
6. Review breach notifications before 72-hour SDAIA submission (Art. 21)

## DPO Selection Criteria

The DPO **must** have:
- Legal background OR security/compliance training
- Saudi PDPL specialty (NOT just GDPR transposed)
- Independence from the engineering and sales orgs
- Direct line to founder (cannot be founder's manager or report)
- Ability to escalate to SDAIA on the Controller's behalf

The DPO **should** ideally have:
- Arabic + English fluency
- Prior experience with Saudi banking/healthcare data (highest standards)
- Familiarity with SDAIA's Personal Data Protection portal

## Appointment Path

### Path A: External Part-Time DPO (recommended for customers 5–30)

Cost: 20–40K SAR/year. Engaged via specialized firm:

- **Tamimi & Co** — premium, full-service legal+DPO bundle
- **Al Sharif Law** — boutique with PDPL specialty
- **DPO-as-a-Service** firms (search "خدمات DPO السعودية")

Template engagement letter: `docs/legal/DPO_ENGAGEMENT_LETTER.md` (TO BE WRITTEN when first contract negotiated)

### Path B: Internal Full-Time DPO (customer 30+)

Cost: 8–15K SAR/month + benefits. Job title: "Privacy Counsel / DPO".

Interview rubric: `docs/legal/DPO_INTERVIEW_RUBRIC.md` (TO BE WRITTEN when hiring path activates)

### Path C: Hybrid (Founder + External Advisor)

For SMB-only customer base (< 5 enterprise), founder remains the named DPO with an external advisor on retainer for monthly review. Cheaper (~5K SAR/month) but founder time-tax is real.

## SDAIA Registration

Once a DPO is appointed:

1. Go to https://www.sdaia.gov.sa/en/SDAIA/about/Pages/PersonalDataProtection.aspx
2. Submit "Controller Registration" form with:
   - Dealix's CR number (Commercial Registration)
   - DPO name + contact email + Saudi phone
   - Categories of personal data processed (PII, communications, lead enrichment)
   - Cross-border transfer disclosures (Anthropic/OpenAI in US, S3 me-south-1)
3. SDAIA confirms within 14 business days
4. Public-facing DPO contact published at `dealix.me/privacy#dpo`

## Public-Facing Disclosure (post-appointment)

Add to `landing/privacy-policy.html`:

```html
<section id="dpo">
  <h2>Data Protection Officer</h2>
  <p>You may contact our DPO directly for any data protection question
     or to exercise your PDPL rights (access, erasure, portability):</p>
  <p>
    <strong>{DPO Full Name}</strong><br>
    Email: dpo@dealix.me<br>
    Phone: +966 5X XXX XXXX<br>
    Address: {Dealix Saudi address}
  </p>
  <p>SDAIA-registered: Controller ID {SDAIA_REG_ID}</p>
</section>
```

## Pre-Appointment Checklist

Before appointing a DPO:

- [ ] Map all personal data flows (use `integrations/pdpl.py:build_data_export()` output as starting point)
- [ ] Identify all cross-border transfers (LLM providers + backups)
- [ ] Document retention policy (currently 5 years for audit logs — `integrations/pdpl.py:build_monthly_audit_report`)
- [ ] Identify high-risk processing (any AI inference on PII = high-risk per SDAIA)
- [ ] Prepare DPO budget (20-40K SAR/yr if external)
- [ ] Verify CR number is current with MCI

## Ongoing DPO Engagement Cadence

Once appointed:

- Monthly: review month's audit logs + breach reports (if any)
- Quarterly: privacy impact assessment of new features
- Annually: full ROPA refresh + SDAIA filing update
- Ad-hoc: every customer DPIA request (enterprise customers will ask)

## Cost Justification

Internal calculation for when DPO becomes cheaper than founder time:

- Founder hours/month on PDPL questions: estimated 8h
- Founder hourly value at current revenue: ~500 SAR/hour
- Monthly founder PDPL cost: ~4,000 SAR
- External DPO cost: ~3,000 SAR/month (part-time)

Break-even: **founder hits 6+ PDPL hours/month**. With 3+ enterprise customers, this happens reliably.

## SDAIA Audit Preparation

If SDAIA audits (random ~ every 24 months or post-incident):

1. ROPA must be current within 30 days (see `integrations/pdpl.py:build_monthly_audit_report`)
2. Breach log accessible (`integrations/pdpl.py:build_breach_notification` history)
3. DPO contact public and reachable within 1 business day
4. Consent records for every data subject (Art. 5 consent flows)
5. Cross-border transfer impact assessment

DPO leads the audit response. Founder is available for high-level questions only.

---

## Status

**Current:** No DPO appointed. Founder is the de-facto DPO contact.
**Next milestone:** First enterprise customer signs → activate Path A appointment within 30 days.
