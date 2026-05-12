# PDPL Breach Runbook — Data Breach Response

> **Authority:** Saudi PDPL (Personal Data Protection Law) + SDAIA implementing regulations.
> **Scope:** Any incident affecting confidentiality, integrity, or availability of personal data processed by Dealix (employees, prospects, customers, partners, end-users of customer products).
> **Owner:** DPO (Data Protection Officer). Backup: Founder/CEO.

---

## 1. Trigger criteria — what counts as a breach

A breach is **any** of:

- Unauthorised access to a database, S3 bucket, repo, or 1Password vault containing personal data.
- Personal data exfiltrated by a malicious party (confirmed or strongly suspected).
- Personal data emailed/sent to the wrong recipient (>10 records, or any record marked S2+).
- Lost/stolen device with non-encrypted dump of personal data.
- Public exposure of personal data via misconfigured endpoint, log line, error page, repo commit, or screenshot.
- Ransomware / destructive malware on a system processing personal data.

If unsure → **escalate as a breach**. Better to over-report internally than under-report.

---

## 2. Severity tiers

| Tier | Definition | Examples | SDAIA notification? |
|------|------------|----------|---------------------|
| **B1 — Critical** | Sensitive data (national ID, health, financial credentials), > 100 subjects, or any cross-border leak | DB dump leaked, sk_live key public | **Yes — within 72 hours** |
| **B2 — High** | Contact data (name+phone+email), 10–100 subjects, contained internally | Misdirected bulk email | **Yes — within 72 hours** |
| **B3 — Moderate** | Single subject, low sensitivity, contained | Wrong recipient on a single message | Internal only; log it |
| **B4 — Near miss** | Detected before exposure (e.g. blocked by gitleaks) | Pre-commit hook caught key | Internal only; log it |

---

## 3. The clock — 72-hour timeline (PDPL Art. 20)

The clock starts at **moment of awareness** (T₀), not at moment of breach. Every action below is logged with a UTC timestamp in `docs/ops/breach_log/<incident-id>.md`.

| T+ | Action | Owner |
|----|--------|-------|
| **T+0 → T+1h** | Contain — revoke compromised keys, block IPs, rotate secrets, isolate hosts. | On-call eng |
| **T+0 → T+2h** | Notify DPO + Founder + CTO. Open incident channel in Slack `#sec-incident-<id>`. | First responder |
| **T+0 → T+4h** | Preserve forensic evidence — DB snapshot, logs, S3 access logs, Sentry events. | Eng |
| **T+0 → T+12h** | Assess scope — affected subjects, data categories, geography. Fill `breach_assessment.md`. | DPO + Eng |
| **T+0 → T+24h** | Determine severity tier (B1/B2/B3/B4) and SDAIA notification requirement. | DPO + legal |
| **T+24h → T+48h** | Draft notification to SDAIA (B1/B2 only). Use template `breach_notify_sdaia_TEMPLATE.md`. | DPO + legal |
| **T+24h → T+72h** | Draft notification to affected data subjects (if high risk to their rights). | DPO + comms |
| **T+72h (B1/B2)** | **Submit SDAIA notification.** | DPO |
| **T+72h** | Initial public statement on status.dealix.sa (if customer-visible) | Comms |
| **T+7d** | Subject notifications mailed/SMS'd (if high risk). | Comms |
| **T+14d** | Internal post-mortem published (`docs/ops/breach_postmortem/<id>.md`). | DPO + Eng lead |
| **T+30d** | Corrective controls implemented + verified. Close incident. | All |

---

## 4. Containment playbook (T+0 → T+1h)

```bash
# Step 1 — revoke any compromised API key
# (1Password vault → mark key as compromised, generate new, push to Railway)

# Step 2 — rotate ALL of these if a Postgres breach is suspected:
#   APP_SECRET_KEY, JWT_SECRET_KEY, API_KEYS, ADMIN_API_KEYS,
#   MOYASAR_WEBHOOK_SECRET, all webhook HMAC secrets,
#   GMAIL_REFRESH_TOKEN, WHATSAPP_ACCESS_TOKEN

# Step 3 — block exfiltration paths
# - disable affected user accounts (DB level)
# - revoke Railway tokens at https://railway.app/account/tokens
# - revoke GitHub PATs

# Step 4 — preserve evidence (DO NOT delete anything yet)
pg_dump --format=custom --no-owner "${DATABASE_URL}" > /forensics/dealix-T0-$(date -u +%Y%m%dT%H%M%SZ).pgdump

# Step 5 — set MAINTENANCE_MODE=1 in Railway if data is still being actively exfiltrated
```

---

## 5. SDAIA notification — required content (per PDPL implementing regs)

Use the template `docs/ops/breach_notify_sdaia_TEMPLATE.md`. Required fields:

1. **Nature of the breach** — confidentiality / integrity / availability
2. **Categories of data subjects** (e.g. customers, employees, prospects) — and approximate count
3. **Categories of personal data** (e.g. name, phone, email, national ID, payment data)
4. **Likely consequences** for affected subjects
5. **Measures taken or proposed** to address the breach and mitigate adverse effects
6. **Contact point** (DPO name, email, phone)

Channels:
- SDAIA portal (when configured): https://sdaia.gov.sa/
- Email backup: `dpo@sdaia.gov.sa` (confirm address with legal at time of incident)

---

## 6. Subject notification — when required

Notify affected data subjects **without undue delay** if the breach is **likely to result in a high risk** to their rights and freedoms.

A notification is **not required** if any of the following applies (PDPL Art. 20):
- Data was encrypted with strong cryptography and key was not compromised.
- Subsequent measures eliminated the risk (e.g. ransomware reverted from backup with no exfiltration).
- Notification would require disproportionate effort — in which case a **public communication** (status page) is used instead.

**Template:** `docs/ops/breach_notify_subject_TEMPLATE_AR.md` (Arabic) and `..._EN.md`.

---

## 7. Internal log — required artefacts

For every incident, even B4 near-misses, create:

```
docs/ops/breach_log/
└── 2026-MM-DD-<short-slug>/
    ├── timeline.md              # T+0 actions with timestamps
    ├── assessment.md            # severity + scope + affected subjects
    ├── communications/          # all internal + external messages sent
    ├── evidence/                # exported logs, screenshots (no PII in repo!)
    ├── notification_sdaia.md    # if applicable
    ├── notification_subjects.md # if applicable
    └── postmortem.md            # T+14d
```

**Do not commit PII to the repo.** Evidence files with PII live in a private encrypted vault.

---

## 8. Drills — twice per year

- **April + October**: tabletop exercise with founder, CTO, DPO, legal. Simulate a B1 breach, walk through the 72-hour clock.
- Record drill in `docs/ops/breach_drill_log.md`.

---

## 9. Quick reference — escalation contacts

| Role | Name | Channel | SLA |
|------|------|---------|-----|
| DPO | _to fill_ | _email/phone_ | 1 hour |
| Founder/CEO | Sami Assiri | _phone_ | 1 hour |
| CTO / Eng lead | _to fill_ | _phone_ | 30 min |
| Legal counsel | _to fill_ | _email_ | 4 hours |
| Cyber insurance | _to fill_ | _phone_ | 24 hours |
| SDAIA hotline | _confirm_ | _portal_ | 72 hours |

**Fill these in pre-launch — empty rows are a launch blocker.**
