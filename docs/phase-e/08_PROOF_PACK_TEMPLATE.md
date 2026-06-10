# Proof Pack — Template

A Proof Pack documents what actually happened during the 7-day Pilot
based on **real events the customer logged**. It is NEVER fabricated.
If there are no events, the pack is an **empty template**, not a fake
result.

## Required fields

| Field | Allowed values |
|---|---|
| `customer_handle` | placeholder (e.g. `Customer-Slot-A`) |
| `period_ar` / `period_en` | bilingual date range |
| `summary_ar` / `summary_en` | ≤ 5 lines each, FACTUAL only |
| `events[]` | list of recorded events from the ledger; empty if none |
| `decision` | `review_required` (default) / `customer_approved` |
| `audience` | `internal_only` (default) / `public_allowed` |
| `approval_status` | `approval_required` (default) |
| `signature` | HMAC if proof-ledger infra supports it |

## Hard rules

- ❌ NEVER include a metric the customer didn't supply
- ❌ NEVER include a testimonial without signed permission
- ❌ NEVER include a specific revenue claim without the customer
  having paid + signed off
- ❌ NEVER include `نضمن` / `guaranteed` / `blast` / `scrape`
- ❌ NEVER include the customer's real name unless `audience=public_allowed`
- ✅ Empty events list is honest — say so explicitly
- ✅ Mark every section "Draft / Internal" until the customer signs
  off
- ✅ Bilingual: Arabic primary, English secondary

## Empty pack template (when no events recorded)

```markdown
# Proof Pack — Customer-Slot-A

## Summary / الملخّص

**Arabic**: لم يتم تسجيل أحداث قابلة للتوثيق خلال هذه الفترة.
**English**: No verifiable events were recorded during this period.

## Events

(empty — see `docs/proof-events/` for the schema)

## Decision

`review_required`

## Audience

`internal_only`

## Approval status

`approval_required`
```

## Populated pack template (when events exist)

```markdown
# Proof Pack — Customer-Slot-A

## Summary / الملخّص

**Arabic**:
- 10 فرص تم اختيارها
- 5 رسائل تمت الموافقة عليها وأرسلت يدوياً
- 2 ردود إيجابية حتى الآن

**English**:
- 10 opportunities reviewed
- 5 approved drafts sent manually
- 2 positive replies so far

## Events

| Date | Event | Type | Audience | Source |
|---|---|---|---|---|
| 2026-MM-DD | Approved draft sent | message_sent_manual | internal_only | customer_log |
| 2026-MM-DD | Reply received | reply_received | internal_only | customer_log |

## Decision

`review_required`

## Audience

`internal_only` (no public mention until customer signs off)

## Approval status

`approval_required`
```

## How to generate

```bash
python scripts/dealix_proof_pack.py \
  --customer-handle "Customer-Slot-A" \
  --period-from 2026-MM-DD \
  --period-to 2026-MM-DD
```

The script reads from `docs/proof-events/<slot>.json` (or empty if no
events) and renders bilingual Markdown. Output is `internal_only` by
default.

## Publish-permission workflow

If the customer agrees to make the Proof Pack public:

1. Customer signs a permission email (kept by founder, NOT in repo)
2. Founder runs the proof-pack script with `--audience public_allowed`
3. Pack is shared on a controlled channel (LinkedIn post text approved
   by customer; case study approved by customer)
4. NEVER published without the signed permission email
