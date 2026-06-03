# Dealix — Escalation Policy / سياسة التصعيد

> **Authoritative.** When Support OS hands off to a human; what
> SLAs apply; what the founder must do on receipt.

## Mandatory escalation categories (V12)

| Category | Reason | SLA |
|---|---|---|
| `payment` | every payment-related issue | P0 (≤ 60 min) |
| `refund` | refund request | P0 (≤ 60 min) |
| `privacy_pdpl` | data rights / consent withdrawal | P0 (≤ 60 min) |
| `angry_customer` | frustration / threat / complaint | P0 (≤ 60 min) |
| `security_incident` | leak / breach / unauthorized access | P0 (≤ 15 min) |
| `system_outage` | service down | P0 (≤ 15 min) |
| `customer_asks_for_guarantee` | "guarantee" / "نضمن" | P0 (≤ 60 min) |
| `customer_asks_for_cold_whatsapp` | "cold WhatsApp" / "واتساب بارد" | P0 (blocked + escalated) |
| `customer_asks_for_scraping` | "scrape" / "سحب بيانات تنافسي" | P0 (blocked + escalated) |
| `legal` | lawyer / lawsuit / "قضيّة" / "محامي" | P0 (≤ 60 min) |

## Arabic — العربيّة

أي رسالة في الفئات أعلاه:
- لا تُجاب آليّاً.
- تُسجَّل كـ ticket P0.
- يُخطَّر المؤسس فوريّاً.
- يُحضَّر مسوّدة ردّ بـ `action_mode = approval_required`.
- المؤسس يعتمد المسوّدة قبل الإرسال اليدوي.

## English

Any message in the categories above:
- Is NEVER auto-answered.
- Is logged as a P0 ticket.
- Triggers immediate founder notification.
- Gets a draft response prepared with
  `action_mode = approval_required`.
- The founder reviews + approves before any manual send.

## Non-escalation flow (P1–P3)

For categories outside the mandatory-escalation list:
- P1 (technical_issue, billing): same-day response, draft via
  `responder.py`, founder approves before send.
- P2 (onboarding, connector_setup, unknown): 24-hour response.
- P3 (upgrade_question, diagnostic_question, proof_pack_question):
  48-hour response.

## On-call expectation (V12 honest state)

Single founder. P0 acknowledged within 60 minutes during business
hours (8AM–10PM KSA). Outside business hours: escalation queued for
next morning unless explicit emergency contact path was agreed.

## Founder receipt action checklist

When a P0 escalation arrives:
1. Read the redacted message (no PII — only `evidence_id`).
2. Open the customer record from your private vault.
3. Read the suggested draft from Support OS.
4. Edit if needed.
5. Reply manually via the original channel.
6. Record the resolution in the ticket.
7. Log a `proof_event` if it has business significance.
