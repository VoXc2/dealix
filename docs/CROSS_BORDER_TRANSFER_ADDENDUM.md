# Cross-Border Data Transfer Addendum — Dealix

**Version:** 1.0 (founder-self-execution per `LEGAL_FOUNDER_SELF_EXECUTION.md`)
**Effective:** 2026-05-07
**Status:** annex to `docs/DPA_DEALIX_FULL.md` §7
**Companion:** `landing/subprocessors.html` · `docs/SUPPLIER_MASTER_LIST.md`

> **Saudi PDPL restricts cross-border transfer of personal data**. This addendum lists every Dealix subprocessor outside KSA + the legal safeguards in place. Customer accepts these transfers by signing DPA + this addendum.

---

## ١. الإطار القانوني · Legal framework

### Saudi PDPL principles for cross-border transfer

PDPL principles allow cross-border transfer when:

1. The recipient country has **adequate protection** as determined by SDAIA
2. There are **appropriate safeguards** (Standard Contractual Clauses or equivalent)
3. The data subject has given **explicit consent** to the specific transfer
4. The transfer is **necessary for performance of contract** with the data subject
5. The transfer protects a **vital interest** of the data subject

Dealix's transfers rely primarily on **(2) appropriate safeguards** + **(4) contract performance**.

---

## 2. Subprocessors outside KSA

| Subprocessor | Country | Service | Legal basis | Safeguard |
|---|---|---|---|---|
| **Anthropic PBC** | USA | LLM inference (Claude) | Contract performance | Anthropic's DPA + their SCCs |
| **Groq Inc.** | USA | LLM inference (Llama 3.3) | Contract performance | Groq's TOS + DPA |
| **Google LLC** | USA | Gemini API (when activated) | Contract performance | Google Cloud DPA + EU SCCs |
| **OpenAI Inc.** | USA | LLM fallback (when activated) | Contract performance | OpenAI's API DPA |
| **Hunter.io / Émojics SAS** | France | Email enrichment | Contract performance | EU GDPR + IAB DPA |
| **Railway Corp.** | USA | Hosting / Postgres | Contract performance | Railway's DPA + SOC 2 |
| **Cloudflare Inc.** | USA | DNS + CDN | Contract performance + legitimate interest (security) | Cloudflare's DPA + EU SCCs |
| **GitHub Inc.** | USA | Source code + landing pages | Legitimate interest | GitHub's DPA |
| **Meta Platforms** | USA / Ireland | WhatsApp Business API | Contract performance | Meta WhatsApp Business DPA |
| **Supabase Inc.** | USA | Postgres (when activated) | Contract performance | Supabase's DPA |

---

## 3. Subprocessors inside KSA

| Subprocessor | Service | Notes |
|---|---|---|
| **Moyasar** | Payment processing | Saudi-licensed PSP; data stays in KSA |

---

## 4. Per-subprocessor safeguard details

### Anthropic (Claude API)

- **Data sent:** prompts containing customer's lead text, draft requests, narrative briefs (PII-redacted before send via `tool_guardrail_gateway`)
- **Data NOT sent:** customer payment info, full conversation logs
- **Data retention by Anthropic:** per their policy (typically 30 days for abuse monitoring; Zero Data Retention available for enterprise tier)
- **Sub-subprocessors:** Amazon AWS (US), Google Cloud (US, EU)
- **Safeguard mechanism:** Anthropic Commercial Terms + Data Protection Agreement
- **Customer right:** request specific Zero Data Retention via `privacy@dealix.me`

### Groq

- **Data sent:** classification prompts (intent detection, BANT scoring)
- **Data NOT sent:** payment info, sensitive PII
- **Data retention:** per Groq's TOS
- **Safeguard:** Groq Cloud Terms + Privacy Policy

### Google Gemini (when activated)

- **Data sent:** research-context prompts (sector intel, market signals)
- **Data NOT sent:** customer payment info
- **Data retention:** per Google's API policy (no storage on Vertex AI standard tier)
- **Safeguard:** Google Cloud Customer Agreement + EU SCCs

### OpenAI (fallback)

- **Data sent:** only when primary providers fail; same content rules
- **Data NOT sent:** payment info
- **Data retention:** per OpenAI API policy (zero retention in opt-out)
- **Safeguard:** OpenAI API Data Processing Addendum

### Hunter.io

- **Data sent:** company domain + email pattern (when HUNTER_API_KEY active)
- **Data NOT sent:** any PII, message content
- **Data retention:** Hunter caches domain data; can be deleted on request
- **Safeguard:** EU GDPR jurisdiction + Hunter's Privacy Policy

### Railway (hosting)

- **Data hosted:** all Dealix Postgres data, including customer PII
- **Data location:** US data centers (configurable to EU on enterprise tier)
- **Encryption:** at rest (AES-256) + in transit (TLS 1.3)
- **Backup:** 30-day retention, daily snapshots
- **Safeguard:** Railway Data Processing Addendum + SOC 2 attestation
- **Future option:** migrate to KSA-resident hosting when Article 13 unlock for compliance scaling

### Cloudflare

- **Data passed-through:** HTTP requests (cached briefly, no Postgres data)
- **Data location:** distributed edge (closest is Frankfurt, then East US)
- **Safeguard:** Cloudflare DPA + EU SCCs

### GitHub

- **Data hosted:** source code + public landing pages (no customer PII in code)
- **Safeguard:** GitHub DPA + Microsoft Cloud Privacy Statement

### Meta WhatsApp Business

- **Data sent/received:** WhatsApp messages between customer's contacts and Dealix
- **Data location:** distributed Meta infrastructure
- **Safeguard:** Meta WhatsApp Business API Terms + Meta Privacy Policy

### Supabase (when activated)

- **Data hosted:** if used, Postgres alternative for specific workflows
- **Data location:** US (configurable to other regions)
- **Safeguard:** Supabase DPA

---

## 5. Customer's choices

The Customer (Controller) has the following choices regarding cross-border transfers:

| Choice | Effect |
|---|---|
| **Accept all** | Default — service operates with all subprocessors |
| **Reject specific** | Some functionality degraded (e.g., reject Anthropic → fallback to Groq for all narrative tasks, lower quality) |
| **Reject all non-KSA** | Service NOT VIABLE in current architecture (Anthropic/Groq are infrastructure-critical) — discuss alternative |

To exercise:
- Email privacy@dealix.me
- Specify which subprocessor(s)
- We respond within 7 business days with impact + alternatives

---

## 6. Notification of subprocessor changes

- **30-day advance notice** for adding any new subprocessor outside KSA
- **Customer right to object** within 30 days (with effect: service degrades or contract early-termination)
- **Channel:** email to designated contact + update on `landing/subprocessors.html`

---

## 7. Data localization requests

If Customer requires KSA-resident processing for specific data categories:

- **Discuss at contract signing** — additional retainer required
- **Available today:** payment data (Moyasar — KSA-resident)
- **Available with effort:** Postgres on KSA-region (would require Railway enterprise migration; cost ~5K-10K SAR/year additional)
- **NOT available:** LLM inference (no Saudi-resident Claude/Llama equivalents at acceptable quality)

---

## 8. Onward transfers (sub-subprocessors)

Each subprocessor has its own sub-subprocessor list (e.g., Anthropic uses AWS + Google Cloud as infrastructure providers). Dealix's contractual reach extends one level (the direct subprocessor); we rely on the subprocessor's own DPA chain to govern further transfers.

Customer's right: ask for any subprocessor's full sub-subprocessor list (we forward the request).

---

## 9. Government access requests

If a foreign government compels a subprocessor to disclose data:

- The subprocessor's standard DPA governs the response (typically: minimal disclosure + customer notification when permitted)
- Dealix is notified per its DPA with the subprocessor
- Customer is notified by Dealix within reasonable time (subject to legal restrictions on the disclosure)

---

## 10. Customer signature

The Customer hereby:

- **Acknowledges** the cross-border transfers described in §2
- **Accepts** the safeguards described in §4 as appropriate
- **Confirms** they have legal basis from data subjects to permit these transfers (or will obtain it before sending us PII)
- **Agrees** to the notification procedure in §6

| | Customer | Dealix |
|---|---|---|
| Signed | _____________________ | _____________________ |
| Name | _____________________ | Sami [last name] |
| Title | _____________________ | Founder |
| Date | _____________________ | _____________________ |

---

## English summary

**Subprocessors outside KSA:** Anthropic (US), Groq (US), Google (US), OpenAI (US), Hunter (FR), Railway (US), Cloudflare (US/global), GitHub (US), Meta WhatsApp (US/IE), Supabase (US, when activated).

**Subprocessors inside KSA:** Moyasar (payment).

**Legal basis for transfers:** Contract performance (primary) + appropriate safeguards (Standard Contractual Clauses or each subprocessor's own DPA).

**PII protection before transfer:** `tool_guardrail_gateway` redacts PII before sending to LLM providers; payment data never sent to LLM providers.

**Customer choice:** accept all (default) · reject specific (degrades service) · reject all non-KSA (not viable in current arch).

**Subprocessor changes:** 30-day notice + customer right to object.

**KSA-resident hosting:** available for payment data today; Postgres would need Railway enterprise migration (additional cost).

**Government access:** subprocessor's DPA governs response; customer notified when permitted.

**Saudi PDPL Article 29 alignment:** transfers rely on appropriate safeguards (#2) + contract performance (#4) per the spirit of the law. Lawyer review will validate exact article applicability.

This addendum is signed alongside DPA + Privacy Policy + Terms of Service. Customer accepts upfront before service begins.
