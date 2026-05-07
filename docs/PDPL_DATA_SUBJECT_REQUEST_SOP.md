# PDPL Data Subject Request (DSAR) SOP — Dealix

**Status:** DRAFT — must be lawyer-reviewed (per `LEGAL_ENGAGEMENT.md` deliverable L5) before customer #4
**Owner:** Sami (founder) · acts as DPO until DPO appointed (Wave 8+)
**Last updated:** 2026-05-07
**Companion docs:** `docs/PRIVACY_PDPL_READINESS.md` · `docs/DPA_PILOT_TEMPLATE.md` · `docs/LEGAL_ENGAGEMENT.md` · `landing/privacy.html` · Plan §23.5.5

> **Why this doc exists:** Saudi PDPL grants data subjects rights to access, correct, delete, restrict processing, and port their data. Failure to respond within statutory deadlines = enforcement action (48 SDAIA decisions issued 2025-2026, fines up to 5,000,000 SAR per breach).
>
> Dealix MUST have this SOP before customer #4 — manually-handled DSARs work for customers 1-3 but not at scale.

---

## 1. PDPL data subject rights (per nDMO + Articles 16-22 PDPL)

| Right | What it means | Statutory window |
|---|---|---|
| **Right to access** | Subject can request copy of their personal data Dealix processes | 30 days |
| **Right to correction** | Subject can request correction of inaccurate data | 30 days |
| **Right to erasure** | Subject can request deletion (subject to legal retention) | 30 days |
| **Right to restriction** | Subject can request processing be paused | 30 days |
| **Right to portability** | Subject can request data in structured, machine-readable format | 30 days |
| **Right to object** | Subject can object to processing for marketing | immediate stop |
| **Right not to be subject to automated decision-making** | Subject can request human review of automated decisions | 30 days |

> **Critical:** SDAIA enforcement window is 5 days for response when SDAIA itself initiates investigation. Statutory 30-day window is for direct subject requests.

---

## 2. Who is the "data subject"?

In Dealix's model:

- **Controller customer's end-users** (e.g., real-estate office's own clients whose data is processed by Dealix) → Dealix is **Processor**
- **Direct prospects / leads to Dealix** (people Dealix's pipelines have processed) → Dealix is **Controller**
- **Dealix's paying customers themselves** → Dealix is **Controller** for the customer-relationship data, **Processor** for the customer's customer data

**Routing rule:**

| Request from | Route to | Dealix role |
|---|---|---|
| End-user of customer's business | Customer (Controller) — Dealix supports as Processor | Processor (assist) |
| Dealix's prospect / lead | Founder direct | Controller (own response) |
| Dealix's paying customer | Founder direct | Controller (own response) |

If end-user contacts Dealix directly, redirect them to the Controller (customer) within 5 days, cc customer.

---

## 3. Receiving a DSAR — channels

Dealix accepts DSARs through:

1. Email: privacy@dealix.me (primary)
2. WhatsApp: founder's number (acceptable in Saudi context; must escalate to email for record)
3. Postal mail: company registered address (rare)
4. Online form on `dealix.me/privacy.html#dsar` (TO BE BUILT — Wave 8 backlog)

**Never refuse a DSAR for using the wrong channel.** Acknowledge any channel within 24 hours, redirect to email for documentation.

---

## 4. Step-by-step procedure

### Step 1 — receive + acknowledge (within 24h)

Founder receives DSAR. Logs in `docs/wave6/live/dsar_log.jsonl` (gitignored):

```json
{
  "dsar_id": "dsar_<timestamp>",
  "received_at": "ISO date",
  "received_via": "email | whatsapp | postal | form",
  "data_subject_identity": "<verified name + Saudi ID hash if provided>",
  "data_subject_role": "end_user | prospect | paying_customer",
  "request_type": "access | correction | erasure | restriction | portability | object | automated_decision_review",
  "scope": "<what data is requested>",
  "statutory_deadline": "received_at + 30 days",
  "status": "received",
  "notes": "..."
}
```

Send acknowledgement (within 24h):

> **AR (template):**
>
> «شكراً [الاسم]. استلمت طلبك حسب نظام حماية البيانات الشخصيّة (PDPL). سأتحقّق من هويّتك خلال ٧ أيّام، ثم أرد عليك خلال ٣٠ يوم من تاريخ استلام الطلب الكامل ([تاريخ]). لو احتجت معلومات إضافيّة لتسريع العمليّة، سأتواصل معك. شكرًا لثقتك.»

### Step 2 — verify identity (within 7 days)

Verify the requester is who they claim to be. Acceptable proof:

- Saudi national ID number (last 4 digits matching record + name match)
- Email matching record on file
- Sectorally-appropriate identity proof (e.g., real-estate office's CR number)

**Do NOT** ask for full government ID scan unless absolutely necessary (PDPL data minimization). Use the minimum proof needed.

If identity cannot be verified after 14 days → reply explaining the verification gap. Do NOT release data without verification.

### Step 3 — determine scope + retrieve data (within 14 days of verification)

For **access / portability requests**: collect all personal data Dealix has on the subject across:

- `auto_client_acquisition/lead_inbox.py` JSONL records
- `crm_v10` Account / Contact tables
- `proof_ledger` events tagged with subject ID
- `support_inbox` ticket history
- `customer_brain` snapshots
- Any audit logs in `observability_v10`
- `payment_ops` payment confirmations (for paying customers)

For **correction requests**: identify the inaccurate field + confirm correction with subject before applying.

For **erasure requests**: check legal retention obligations:
- ZATCA invoice retention: 6-10 years for paying customers
- Audit log retention: 5 years (PDPL operational)
- If retention obligation conflicts with deletion → explain to subject, partial-delete what's possible

For **portability**: export in JSON or CSV, machine-readable.

### Step 4 — respond to subject (within 30 days total)

Send via email (or original channel if subject prefers):

```
الموضوع: ردّ على طلب حقوق البيانات الشخصيّة — رقم الطلب [dsar_id]

[الاسم]،

استلمت طلبك بتاريخ [تاريخ الاستلام].

نوع الطلب: [وصول / تصحيح / حذف / تقييد / نقل]

النتيجة:
- [إذا الوصول/النقل]: مرفق ملف JSON يحتوي على كل بياناتك الشخصيّة المعالجة لدى Dealix.
- [إذا التصحيح]: تمّ تصحيح الحقل [اسم الحقل] من [القيمة القديمة] إلى [القيمة الجديدة].
- [إذا الحذف]: تمّ حذف بياناتك من [الأنظمة]. ما لم نتمكّن من حذفه: [القائمة] لأسباب قانونيّة (مثل التزامات ZATCA).
- [إذا التقييد]: تمّ إيقاف معالجة بياناتك في الأنظمة المذكورة.

إذا كان لديك أيّ سؤال، تواصل معي على هذا البريد.

سامي [اسم العائلة]
المؤسّس وقائد حماية البيانات (DPO acting)
Dealix
```

### Step 5 — document closure

Update DSAR log entry:

```json
{
  "responded_at": "ISO date",
  "response_method": "email + json export",
  "data_provided": {...},
  "data_redacted": [...],
  "retention_blocked": [...],
  "status": "completed"
}
```

If subject disputes the response → escalate per §6.

---

## 5. Special cases

### 5.1 Subject requests deletion of data Dealix processes for a customer (Processor role)

Dealix:
1. Acknowledges receipt within 24h
2. Forwards request to Controller customer within 5 days (with subject's consent)
3. Coordinates with customer on response
4. Customer is the primary respondent; Dealix supports

### 5.2 Bulk DSAR (10+ subjects in single request)

Likely an audit / regulatory action.
1. Notify lawyer immediately (within 4 hours)
2. Verify the requester's authority (regulator? customer's lawyer?)
3. Respond within statutory window with lawyer-drafted response

### 5.3 SDAIA inquiry

5-day response window (NOT 30). Drop everything:
1. Notify lawyer within 1 hour
2. Document inquiry in DSAR log
3. Respond per lawyer guidance only
4. Never destroy or modify data after SDAIA inquiry received (evidence preservation)

### 5.4 Data breach affecting subject's data

PDPL Article 21: notify affected subjects + SDAIA within 72 hours of becoming aware.
- Notify lawyer immediately
- Pause all processing of affected data
- Run breach response plan (TO BE BUILT — `LEGAL_ENGAGEMENT.md` deliverable L6)

---

## 6. Escalation paths

| Trigger | Escalate to | Within |
|---|---|---|
| Subject disputes response | Lawyer | 5 business days |
| Bulk DSAR (10+ subjects) | Lawyer | 4 hours |
| SDAIA inquiry | Lawyer + advisor | 1 hour |
| Suspected data breach | Lawyer + Cybersecurity insurance (when bound) | immediate |
| Cross-border data transfer question | Lawyer | 5 business days |

---

## 7. Wave 7 vs Wave 8 automation

### Wave 7 (current) — manual DSAR

- Founder personally handles each DSAR
- Manual data export from each storage location
- Logged in JSONL, no automated handler

### Wave 8+ trigger to automate

When any of these fires, automate DSAR handling:

- 3rd DSAR in 30 days
- Customer asks "do you have a DSAR portal?"
- Lawyer recommends formal automation

Future automation will include:
- `/api/v1/pdpl/dsar/submit` endpoint (per `landing/privacy.html#dsar` form)
- Automated identity verification + audit logging
- Automated data aggregation from across modules
- Lawyer-attested response template

This is **NOT in Wave 7 scope** — manual is acceptable for customers 1-3 per Plan §23.5.5.

---

## 8. Hard rules

- ❌ Never delete data after SDAIA inquiry received
- ❌ Never release data without identity verification
- ❌ Never miss the 30-day window without lawyer-attested extension request
- ❌ Never release data of one subject to another (verify carefully)
- ❌ Never charge a fee for a DSAR (PDPL prohibits)
- ❌ Never refuse a request for using "wrong channel" — redirect, don't refuse
- ✅ Always log every DSAR in `dsar_log.jsonl` same day
- ✅ Always notify lawyer for §5 special cases
- ✅ Always send acknowledgement within 24h
- ✅ Always respect data minimization (don't ask for more proof than needed)

---

## 9. Lawyer review checkpoints

Before customer #4, lawyer must review:

- [ ] §1 enumerated rights — confirm completeness vs PDPL articles
- [ ] §3 channels — confirm `privacy@dealix.me` + WhatsApp acceptability
- [ ] §4 step-by-step — confirm 30-day window calculation
- [ ] §5.3 SDAIA inquiry handling — confirm 5-day response framing
- [ ] §6 escalation paths
- [ ] Communication templates (Saudi-Arabic + English)

> **Disclaimer:** This SOP is NOT legal advice. Lawyer review per `LEGAL_ENGAGEMENT.md` deliverable L5 is required before customer #4.
