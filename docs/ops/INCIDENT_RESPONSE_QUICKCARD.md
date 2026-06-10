# Incident Response Quickcard — بطاقة استجابة سريعة

> One-pager for any compliance, data, or security incident at Dealix. Bilingual. No emojis. Designed to be printed and pinned next to the founder's workstation.
>
> Cross-link: [PDPL_BREACH_RUNBOOK.md](./PDPL_BREACH_RUNBOOK.md), [PDPL_BREACH_RESPONSE_PLAN.md](../PDPL_BREACH_RESPONSE_PLAN.md), [PDPL_DATA_SUBJECT_REQUEST_SOP.md](../PDPL_DATA_SUBJECT_REQUEST_SOP.md), [SECURITY_RUNBOOK.md](../SECURITY_RUNBOOK.md), [FIRST_CUSTOMER_ONBOARDING.md](./FIRST_CUSTOMER_ONBOARDING.md).

---

## 1. The five phases — المراحل الخمس

| # | Phase / المرحلة | Clock / الساعة | Owner |
|---|---|---|---|
| 1 | Detection / الكشف | T+0 | First person to observe |
| 2 | Triage / الفرز | within 4 hours of detection | Founder |
| 3 | Customer notification (PDPL Article 21) / إبلاغ العميل | within 72 hours of confirmation | Founder |
| 4 | Root cause + corrective action / السبب الجذري والتصحيح | within 14 days | Founder |
| 5 | Public changelog (anonymized) / تحديث علني بلا أسماء | by day 14 | Founder |

Each phase has one exit criterion. Do not advance to the next phase before its exit criterion is met. Do not skip phase 5 even when the incident was resolved silently — the public changelog is the audit trail that makes refusal credible.

---

## 2. Triage in 4 hours — الفرز خلال أربع ساعات

Within 4 hours of detection, the founder writes a triage note containing:

- **What we know / ما نعرفه:** observed facts only, no speculation.
- **What we suspect / ما نشك فيه:** explicit guesses, labeled as guesses.
- **Scope estimate / تقدير النطاق:** which engagements, which customers (anonymized in the note itself), which data classes.
- **PII involvement / وجود بيانات شخصية:** yes / no / unknown.
- **Containment action taken / إجراء الاحتواء:** what was switched off, locked down, rotated.

The triage note is stored in `friction_log` with `severity=incident`. It is the source document for the 72-hour notification.

---

## 3. Customer notification (PDPL Article 21) — إبلاغ العميل

Within 72 hours of confirming the incident, the customer receives a written notification with:

1. What happened, in plain bilingual language.
2. Which of their data was involved, in counts not names.
3. What we have already done about it.
4. What we are asking from them (often nothing).
5. The founder's direct contact for follow-up.

The 72-hour clock starts at confirmation, not at first suspicion. The triage note distinguishes the two timestamps explicitly. If suspicion lasts more than 24 hours without confirmation, the founder writes a "pre-notification" courtesy note to the affected customer, even when no PDPL clock has started — it costs trust to be silent during a long triage.

---

## 4. Three scenarios with concrete responses — ثلاث حالات

### 4.1 PII leak suspicion — اشتباه تسرّب بيانات شخصية

**Signal:** a log line contains PII (a name, a phone, an email) that should have been redacted. Or, an outbound message reaches a recipient who should not have received it.

**Immediate response:**

- Rotate any credential that might have been exposed. Even if not certain, rotate.
- Freeze the engagement workspace via `POST /api/v1/governance-os/freeze?engagement=<id>` — no new actions until cleared.
- Pull the audit chain for the affected data via `GET /api/v1/data-os/lineage?source_id=<id>`. Identify every downstream artifact carrying the source.
- Quantify the exposure: how many rows, how many people, what fields. Counts only, in the triage note.
- Customer notification within 72 hours per Section 3.
- `friction_log` entry with `incident_type=pii_leak_suspicion`. `capital_ledger` entry once the corrective action is implemented (the rule that prevents the same class of leak).

**SDAIA reporting threshold:** if PDPL Article 21 reporting thresholds are met, the founder files with SDAIA in parallel to customer notification, not after. Placeholder: `<SDAIA reporting portal URL and account>`.

### 4.2 Unauthorized external send blocked — محاولة إرسال خارجي مرفوضة

**Signal:** the governance runtime returned `BLOCK` on an outbound action that should have been authorized. Or, an internal user attempted to forward data flagged `external_use_allowed=false`.

**Immediate response:**

- This is a successful refusal, not a failure. The system did what it should. Treat as a near-miss, not a breach.
- `friction_log` entry within the same business day, `incident_type=unauthorized_external_send_blocked`.
- Review whether the requesting flow was misconfigured (e.g., a draft pipeline that asked for external dispatch when the passport disallowed). If yes, fix the upstream configuration and deposit the fix in `capital_ledger`.
- Customer notification is not required by PDPL for a blocked attempt, but the customer is informed at the next scheduled touchpoint. Transparency is the policy; silent near-misses become loud breaches later.
- Public changelog entry on the standard 14-day cadence, anonymized.

### 4.3 Customer requests data deletion — طلب حذف بيانات

**Signal:** the customer or one of their data subjects requests deletion under PDPL Articles 13 and 18.

**Immediate response:**

- Acknowledge receipt within 24 hours, in writing.
- Verify identity per [PDPL_DATA_SUBJECT_REQUEST_SOP.md](../PDPL_DATA_SUBJECT_REQUEST_SOP.md).
- Execute deletion within the statutory window. Endpoint: `POST /api/v1/data-os/delete?source_id=<id>` runs across the lineage chain produced in Section 4.1.
- Issue a deletion certificate to the customer, bilingual, with the lineage hash showing every artifact that was removed and every one that was anonymized in place (because anonymized data has no remaining identifier).
- `proof_ledger.deletion_executed`. `capital_ledger` if the deletion path produced a reusable tooling improvement.
- Public changelog entry: counts only, no customer identifier.

---

## 5. Friction log + capital ledger — التسجيل الإجباري

Every incident, including a successful refusal, must end with two entries:

- A `friction_log` entry describing what broke or almost broke, what changed in response, and what we are still uncertain about.
- A `capital_ledger` entry containing the reusable artifact produced by the response — a new rule, a new check, a new template, a new redaction pattern.

An incident that does not deposit a capital asset is an incident that has not finished. The founder reviews the open incidents weekly and chases any that have a `friction_log` entry but no matching `capital_ledger` entry.

---

## 6. Public changelog — السجل العلني

Within 14 days of incident closure, a public changelog entry is published on the company site and cross-posted to the founder's LinkedIn. The entry contains:

- A one-line description, anonymized.
- The phase 4 corrective action, named.
- The capital asset deposited.

No customer names. No founder excuses. No competitive comparisons. The public changelog is one of the eleven constitutional non-negotiables operating in plain sight.

---

## 7. Escalation contacts — جهات التصعيد

Fill these placeholders on the operating environment, never in this document committed to git.

- **Founder on-call / المؤسس المناوب:** `<phone>` — answers within 30 minutes during operating hours.
- **Legal advisor / المستشار القانوني:** `<advisor_contact>`.
- **SDAIA contact / الجهة الرقابية:** `<SDAIA point-of-contact name + email + portal URL>`.
- **ZATCA technical / الدعم الفني للفوترة:** `<ZATCA support channel>` — for incidents touching invoice integrity.
- **Cloud provider security / أمان مزود السحابة:** `<security contact for hosting provider>`.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
