# PDPL Breach Response Plan — Dealix

**Version:** 1.0 (founder-self-execution per `LEGAL_FOUNDER_SELF_EXECUTION.md`)
**Effective:** 2026-05-07
**Owner:** Sami (founder) — acting Data Protection Officer (DPO) until appointed
**Companion:** `docs/DPA_DEALIX_FULL.md` §5.6 · `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md` · `docs/LEGAL_ENGAGEMENT.md`

> **Saudi PDPL requires breach notification to SDAIA + affected individuals within 72 hours of detection.** This SOP defines who, what, and how — fast, accurate, regulator-ready.

---

## 1. What is a "personal data breach"

Per Saudi PDPL principles, a breach occurs when there is:

- Unauthorized **access** to personal data (someone accessed who shouldn't)
- Unauthorized **disclosure** (data leaked outside Dealix's systems)
- **Loss** of personal data (deleted without recovery, or lost on a stolen device)
- **Alteration** without authorization (data tampered with)
- **Destruction** of data without authorization

**Examples we've simulated to prepare:**

- Customer Postgres database accessed via leaked credentials
- WhatsApp conversation log emailed to wrong customer
- Subprocessor (Anthropic / Hunter / Moyasar) suffers a breach affecting our data
- Employee's laptop with cached customer data stolen
- Misconfigured S3 bucket allows public read

---

## 2. Detection — how we find breaches

### Automated detection (active 24/7)

| Source | Trigger | Routing |
|---|---|---|
| Audit log anomalies | Unusual query patterns / failed auth bursts | Real-time alert to Sami's WhatsApp + email |
| Subprocessor notifications | Anthropic/Groq/Railway/etc. breach disclosure | Public RSS + their security advisory |
| User reports | Customer / public reports a leak | privacy@dealix.me + WhatsApp founder |
| External research | Security researcher contacts us | privacy@dealix.me |
| GitHub secret scanning | API key leak in commit | Repo-level alert blocks merge |
| Cloudflare WAF | DDoS / unusual traffic | Cloudflare dashboard |

### Manual detection

- Founder's daily review of audit_log
- Weekly Friday review (per `SALES_OPS_SOP.md` §10) audits anomalies

---

## 3. The 72-hour clock

PDPL window: **72 hours from awareness** (NOT from incident occurrence).

```
Hour 0   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ AWARENESS
Hour 1   Triage + initial classification (Sami + lawyer)
Hour 4   Containment in progress
Hour 8   Forensics started; affected scope known
Hour 24  Customer notification drafted (if customer-impacting)
Hour 48  SDAIA notification draft ready (if regulator-required)
Hour 72  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ DEADLINE
```

If we miss 72h: SDAIA inquiry likely + escalating fines.

---

## 4. Response procedure — step by step

### Phase 1 — Triage (within 1 hour of awareness)

**Sami runs:**

1. Open `data/breach_response/<timestamp>.md` (gitignored — never commit incident details)
2. Log: time of awareness · how detected · initial scope · who knows
3. Phone the lawyer immediately (per `LEGAL_ENGAGEMENT.md`)
4. Determine: is this a real breach OR a false alarm?

**Decision tree:**

- **False alarm** → close with documentation, no further action
- **Confirmed breach with personal data** → continue to Phase 2
- **Suspected but unconfirmed** → continue to Phase 2 in parallel with confirmation

### Phase 2 — Containment (within 4 hours)

1. **Stop the bleeding:**
   - Rotate all secrets that may be compromised
   - Disable affected user accounts
   - Block compromised IP / kill suspicious session
   - Pull affected service from Railway if necessary
2. **Preserve evidence:**
   - Snapshot affected logs BEFORE remediation
   - Save to `/data/breach_response/<timestamp>/evidence/` (gitignored)
   - Hash + timestamp every evidence file
3. **No data destruction** without lawyer approval (preserve for forensics)

### Phase 3 — Forensics (within 24 hours)

1. **What was accessed?**
   - Query audit_log for the suspicious correlation_id
   - Cross-reference with consent_table + customer records
2. **What was exfiltrated?**
   - Network logs from Railway / Cloudflare
   - Subprocessor logs (Anthropic / Groq / etc. may help if they were involved)
3. **Who is affected?**
   - Generate list of `customer_handle` + `data_subject_id` impacted
4. **What's the harm potential?**
   - Identity theft risk?
   - Financial fraud risk?
   - Reputational harm?
   - PDPL "high risk" classification?

### Phase 4 — Notification (within 72 hours)

#### To SDAIA (regulator)

**When required:** any breach with risk of harm to data subjects.

**Channel:** SDAIA portal at sdaia.gov.sa (or by phone + written confirmation if portal down).

**Content (template):**

```
Subject: PDPL Breach Notification — [Dealix entity name] — [Date]

1. Identity of controller / processor
   - Name: Dealix [legal entity]
   - CR: [if registered]
   - DPO contact: privacy@dealix.me, +966[Sami phone]

2. Date and time of incident
   - Awareness: [ISO timestamp]
   - Estimated start: [ISO timestamp]
   - Detection method: [from §2]

3. Nature of breach
   - Type: [unauthorized access | disclosure | loss | alteration | destruction]
   - Categories of data affected: [identification | contact | business context | etc.]
   - Approximate number of data subjects affected: [N]
   - Approximate number of personal data records: [N]

4. Likely consequences
   - [Summary of risk to individuals]

5. Containment measures taken
   - [List from Phase 2]

6. Notification to affected individuals
   - [Plan + timeline]

7. Contact for further information
   - privacy@dealix.me + Sami phone

8. Attachments
   - Evidence summary (high level, no PII)
   - Audit log excerpts (redacted)
```

#### To affected data subjects

**When required:** breach is "likely to result in high risk to rights and freedoms" of subjects.

**Channel:** the channel through which they originally consented (email / WhatsApp).

**Content (template — Saudi-Arabic):**

```
الموضوع: إخطار مهمّ بشأن خصوصيّتك

عزيزي/تي [الاسم]،

يؤسفنا إبلاغك أنّنا اكتشفنا حادثة أمنيّة بتاريخ [تاريخ] أدّت إلى:
[وصف مختصر للحادثة]

البيانات الشخصيّة المتأثّرة:
[قائمة]

الإجراءات التي اتّخذناها:
١. [إجراء ١]
٢. [إجراء ٢]
٣. [إجراء ٣]

ما يجب أن تفعله أنت:
[توصيات حسب طبيعة الخرق — مثل تغيير كلمات السرّ، مراقبة كشف الحساب، إلخ]

لو كان لديك أيّ سؤال:
- privacy@dealix.me
- WhatsApp: [Sami's number]

نعتذر بشدّة، ونلتزم بالشفافيّة الكاملة.
[توقيع المؤسس]
```

### Phase 5 — Post-incident (within 7 days)

1. **Root cause analysis (RCA):**
   - 5-Whys to find the underlying cause
   - Document in `data/breach_response/<timestamp>/rca.md`
2. **Remediation plan:**
   - Code/process changes
   - Training updates
   - Subprocessor evaluation
3. **Update this SOP** if process gaps identified
4. **Notify lawyer + insurance** of resolution
5. **Customer transparency:** if multi-customer breach, publish anonymized post-mortem (within 30 days)

---

## 5. Decision tree — is this a breach?

```
Is unauthorized party accessing data NOW?
├── YES → CONTAIN IMMEDIATELY (Phase 2)
└── NO
    └── Was data accessed/disclosed/lost in past?
        ├── YES → Phase 1 triage
        └── NO
            └── Unauthorized configuration change?
                ├── YES → Phase 1 triage
                └── NO → Likely false alarm; document and close
```

---

## 6. Severity classification

| Level | Criteria | Notification scope |
|---|---|---|
| **Critical** | >100 subjects affected; sensitive data; or financial/identity risk | SDAIA + all subjects + public disclosure |
| **High** | 10-100 subjects OR moderate risk | SDAIA + affected subjects |
| **Medium** | <10 subjects, low harm potential | SDAIA only (some cases) + affected subjects |
| **Low / informational** | Internal-only, no subjects affected | Document; no external notification |

---

## 7. Escalation paths

| Trigger | Escalate to | Within |
|---|---|---|
| Suspected breach (any) | Lawyer | 1 hour |
| Confirmed breach (any) | Cybersecurity insurance broker (when bound) | 1 hour |
| Subprocessor breach affecting Dealix data | Subprocessor's incident team | Same hour |
| SDAIA inquiry response | Lawyer | Immediately |
| Media inquiry | Lawyer + drafting team | Before any statement |

---

## 8. Communication rules

- **Speed > polish:** notify within 72h even if forensics incomplete
- **Honesty > spin:** never minimize the breach
- **Saudi-Arabic primary:** all customer notifications bilingual
- **Single-source-of-truth:** one designated spokesperson (Sami) + lawyer review of all external statements
- **Internal silence on social:** no social media commentary until lawyer-approved statement
- **Legal hold:** preserve all logs + emails related to incident

---

## 9. Subprocessor breach — special procedure

If a subprocessor (Anthropic, Groq, Hunter, etc.) suffers a breach affecting our data:

1. Subprocessor notifies Dealix (per their DPA)
2. Sami evaluates: did our customers' data get affected?
3. If yes: treat as Dealix breach for §3-§6 purposes
4. Preserve subprocessor's notification + their forensics report
5. Include subprocessor's actions in our notification to SDAIA + customers
6. Decide: should we replace this subprocessor?

---

## 10. Insurance + financial planning

- **Cybersecurity insurance:** target bind by month 4 (per Wave 7 §23.5.5)
- Coverage: PDPL fine reimbursement + breach response costs (legal, forensics, notification, credit monitoring)
- Premium estimate: 2,500-5,000 SAR/year for first year (low-volume tier)
- Without insurance: founder personal liability for first year

---

## 11. Drills — practice the response

**Quarterly drill:** simulate a breach scenario, run through Phase 1-4 (without actually notifying). Document timing + gaps.

**Drill #1 (quarter 1):** lost laptop with cached customer data
**Drill #2 (quarter 2):** Anthropic API key leaked publicly
**Drill #3 (quarter 3):** Customer Postgres unauthorized access
**Drill #4 (quarter 4):** Subprocessor breach disclosure

After each drill: update this SOP if process gaps.

---

## 12. Hard rules

- ❌ Never delete logs after suspicious activity (preserves evidence)
- ❌ Never skip lawyer phone call in Phase 1
- ❌ Never miss 72h window even if "investigation incomplete"
- ❌ Never make external statement without lawyer review
- ❌ Never apologize in writing without lawyer review (admission of liability)
- ✅ Always document timeline immediately (memory fades)
- ✅ Always isolate evidence in `data/breach_response/<timestamp>/`
- ✅ Always notify customer + SDAIA bilingual
- ✅ Always run RCA within 7 days
- ✅ Always update this SOP if drill reveals gaps

---

## 13. Founder personal commitment

I, Sami [last name], commit to:
- Treating any breach as the most urgent thing in my calendar
- Honesty with customers — even when it costs us the contract
- Lawyer-first counsel before any external statement
- Insurance bind by month 4 of operations
- Quarterly drills to keep this SOP fresh

**Signed:** _____________________ **Date:** _____________________

---

## English summary

**PDPL window:** 72 hours from awareness to notify SDAIA + affected subjects.

**Phases:**
1. Triage (1h) — call lawyer, classify
2. Contain (4h) — stop the bleeding, preserve evidence
3. Forensics (24h) — what was accessed, who's affected, what's the harm
4. Notify (72h) — SDAIA via portal + subjects via their original consent channel
5. Post-incident (7d) — RCA, remediation, update this SOP

**Severity tiers:** Critical (>100 subjects + sensitive) · High (10-100) · Medium (<10) · Low (internal only).

**Escalation:** lawyer within 1h on any suspected breach. Insurance when bound. SDAIA via portal.

**Comms rules:** Speed > polish. Honesty > spin. Bilingual notifications. Single spokesperson. Legal hold on logs.

**Drills:** quarterly simulations to keep response sharp.

**Insurance:** target month 4 bind, 2.5-5K SAR/year.

This SOP is founder-self-executable. Lawyer review parallel-tracked within 90 days.
