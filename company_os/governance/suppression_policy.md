# Suppression & Do-Not-Contact Policy

> Resolves Launch No-Go Blocker #5 (missing suppression / do-not-contact).
> Enforced before ANY outreach is queued, drafted, or sent.

---

## Principle

No prospect on the suppression list is ever contacted by any channel, by a human
or by an agent. Suppression is checked **before** an account enters the outreach
queue and **again** before a founder approves a send.

## Suppression list

- File: `company_os/revenue/suppression_list.csv`
- Columns: `domain, company, reason, added_by, added_date, channel`
- `channel` = `all` (default), `email`, `whatsapp`, or `call`
- Matching is by **domain** first, then by normalized company name.

## What MUST be suppressed

| # | Condition | Channel |
|---|-----------|---------|
| 1 | Explicit unsubscribe / "do not contact" request | all |
| 2 | Hard bounce or spam complaint | email |
| 3 | Existing client (handled by delivery, not outreach) | all |
| 4 | Active deal already in pipeline (avoid double-touch) | all |
| 5 | Competitor / partner explicitly excluded by founder | all |
| 6 | Any contact obtained without a verifiable public source | all |

## Unsubscribe handling

- Every marketing email includes a working unsubscribe path (list-unsubscribe
  header + visible link) per bulk-sender norms.
- An unsubscribe request is added to the suppression list within 24 hours and is
  honored permanently.

## Enforcement points

1. **Account Pack build** — drop any account whose domain is on the list.
2. **Outreach queue** — re-check before drafts are generated.
3. **Founder approval** — the Daily Super Command must show `suppression: clean`
   for every send candidate, or the candidate is removed.

## Hard rules

- Suppression is **append-only**; entries are never silently removed.
- No purchased lists. No scraped personal emails/phones. Public, role-based
  routing only (see `data_handling_checklist.md` and `agent_permissions.md`).
- Removing someone from suppression requires founder sign-off + a logged reason.

---

*Version: 1.0 | Owner: Founder | Enforced: YES*
