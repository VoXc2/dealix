# Commercial Gates (G1–G7)

> Canonical spec for the seven progress gates. A gate is **passed / not passed** —
> never a percentage, never a date. Each gate reads the Commercial Evidence
> State Machine ([CEL spec](COMMERCIAL_EVIDENCE_STATE_MACHINE.md)) and is
> evaluated by `auto_client_acquisition/commercial_os/gates.py`.

## Why gates exist

Gates stop the company from skipping ahead of its own evidence. You do not build
a platform before a workflow repeats; you do not claim revenue before an invoice
is paid; you do not call something repeatable until it has sold twice. Each gate
has one job: convert a *belief* into a *recorded fact*.

## The seven gates

| Gate | Name | Entry criteria (recorded facts) | Reads |
|------|------|----------------------------------|-------|
| **G1** | First Market Proof | 5 messages reach `sent` **and** the first reply or silence is classified | `commercial.sent` ×5 + `commercial.reply_classified` ≥1 |
| **G2** | Meeting Proof | At least one engagement reaches `used_in_meeting` | a `CEL5` event |
| **G3** | Pull Proof | At least one engagement reaches `scope_requested` or `pilot_intro_requested` | a `CEL6` event |
| **G4** | Revenue Proof | At least one engagement reaches `invoice_paid` | a `CEL7_confirmed` event |
| **G5** | Repeatability | The **same** offer reaches `invoice_paid` twice | `CEL7_confirmed` ×2 for one `offer_id` |
| **G6** | Retainer | A recurring monthly engagement is active | an active retainer engagement |
| **G7** | Platform Signal | The same manual workflow has repeated 3+ times | `friction_log` repeated-workflow signal ≥3 |

## Gate rules

- **Gates are ordered for the company, not for a single deal.** A single deal
  flows through CEL states; the company flows through gates. G4 (Revenue Proof)
  is passed the first time *any* deal is paid.
- **A gate, once passed, stays passed.** It records a historical fact.
- **G7 is the only trigger for building platform features.** Per company
  doctrine, no new feature is built unless a client explicitly asked, a workflow
  repeated 3+ times (G7), it removes a real risk, it speeds a paid delivery, or
  it opens a retainer. Otherwise: **No build.**

## Gate → action mapping

| Until passed | Company focus |
|--------------|---------------|
| G1 | Pick 5 warm contacts, draft, get founder approval, send, classify replies. |
| G2 | Convert interest into a real meeting where a Dealix artifact is used. |
| G3 | Earn pull — a scope or intro request from the prospect. |
| G4 | Turn a scope into an invoice, and an invoice into a payment. |
| G5 | Sell the *same* offer a second time before widening the catalog. |
| G6 | Convert a repeated engagement into a monthly retainer. |
| G7 | Only now: consider building a reusable platform module. |

## بالعربية — موجز

**البوابات السبع (G1–G7)** تحوّل القناعة إلى حقيقة مسجّلة: إثبات سوق، إثبات
اجتماع، إثبات جذب، إثبات إيراد، قابلية تكرار، ريتينر، ثم إشارة منصة. البوابة
تُقاس بـ«تم / لم يتم» فقط. **G7 وحدها** تأذن ببناء ميزة منصة جديدة — وفيما عدا
ذلك: لا تبنِ.
