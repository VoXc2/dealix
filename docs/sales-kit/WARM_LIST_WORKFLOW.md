# Warm List Workflow — تدفّق العمل على القائمة الدافئة

> Founder-only sales kit for the first revenue motion at Dealix. Twenty named personal contacts, five per day over four days. No cold outreach. No automation. Every reply is governed at the qualification gate before any draft is sent. Bilingual (AR + EN), no emojis, no model names.
>
> Cross-link: [FIRST_10_WARM_MESSAGES_AR_EN.md](../FIRST_10_WARM_MESSAGES_AR_EN.md), [OBJECTION_HANDLING_V6.md](../OBJECTION_HANDLING_V6.md), [03_commercial_mvp/DIAGNOSTIC_DELIVERY_SOP.md](../03_commercial_mvp/DIAGNOSTIC_DELIVERY_SOP.md), [ops/FIRST_CUSTOMER_ONBOARDING.md](../ops/FIRST_CUSTOMER_ONBOARDING.md).

---

## 1. Scope and constraints — النطاق والقيود

- **Audience / الجمهور:** 20 personal contacts the founder has met at least once, in person or by named introduction. No purchased lists. No scraped lists. No "I found you on LinkedIn" intros.
- **Channel / القناة:** WhatsApp or email — whichever the relationship already uses. Never both at once. Never a new channel for the first message.
- **Cadence / الإيقاع:** 5 contacts per day, 4 days. One outreach per contact. No automated follow-up. A second message only when the contact replies, or when an explicit follow-up window was agreed.
- **Constitutional gates / بوابات دستورية:** the contact must be a personal relationship (non-negotiable on cold WhatsApp does not apply to opted-in relationships, but consent is logged in the engagement record). Any draft the contact forwards to a third party is treated as a new intake and gated again.

---

## 2. The one-line ask — السطر الواحد

The founder sends one of the two language variants, matching the language the relationship uses. No paragraph. No deck. No calendar link.

**العربية:**

> أبني MVP لخدمة Revenue Intelligence لشركات B2B سعودية — أبحث عن 2–3 شركات يجربون تشخيصاً مجانياً + Sprint مدفوع 499 ريال. هل تعرف من يفيدك هذا؟

**English:**

> Building an MVP for a Revenue Intelligence service for Saudi B2B companies. Looking for 2 to 3 companies to run a free diagnostic and a paid 7-day 499 SAR sprint. Do you know anyone this would be useful for?

Rules around the ask:

- One question only. The contact picks the answer space.
- No pricing details beyond the 499 SAR figure. No deliverable list. No deck attached. The diagnostic page is offered only after a "yes, tell me more."
- No "circle back" follow-ups. If there is no reply in 7 days, the contact is left alone. Re-engagement only on a natural occasion (a published post they react to, a referral they make, an in-person meeting).

---

## 3. Daily plan — الخطة اليومية

| Day | Contacts | Founder hours | Outcome target |
|---|---|---|---|
| Day 1 | 5 | 60 minutes (send + log) | 5 messages sent. Engagement entries opened. |
| Day 2 | 5 | 60 minutes | 5 sent. 1–2 replies expected from Day 1 — handled per Section 4. |
| Day 3 | 5 | 60 minutes | 5 sent. Reply handling continues. |
| Day 4 | 5 | 60 minutes | All 20 sent. First qualification calls scheduled. |
| Day 5–7 | — | as scheduled | Qualification calls. Free diagnostics started for ACCEPT / DIAGNOSTIC_ONLY outcomes. |

Each contact is logged at send time, not at reply time, in `engagement_ledger` with `channel`, `language`, `timestamp`, `relationship_basis` (e.g., "met at Saudi Tech meetup, March 2025"). The relationship_basis is the consent record.

---

## 4. Reply handlers — معالجات الردود

Three reply patterns cover ~90 percent of responses. Each pattern carries a precise next message draft.

### 4.1 Interested — مهتم

**Signal:** the contact says "tell me more," asks who the diagnostic is for, mentions a specific company that might benefit, or asks for a call.

**Founder action:** within 24 hours, never sooner than 1 hour (to avoid looking automated), the founder replies with the qualifying message.

**Arabic draft:**

> شكراً. التشخيص المجاني خلال 24 ساعة، ثنائي اللغة، يُسلَّم باعتماد شخصي. السبرنت بعده خياري، 499 ريال، 7 أيام، يُسلِّم: 10 حسابات مُرتَّبة، مسوّدات ثنائية اللغة، سجل قرارات حوكمة، حزمة إثبات من 14 قسماً، وأصل واحد قابل لإعادة الاستخدام.
> هل أرسل لك رابط نموذج طلب التشخيص، أو ترتيب مكالمة 20 دقيقة لمعرفة هل يناسبكم؟

**English draft:**

> Thank you. The free diagnostic is delivered in 24 hours, bilingual, with my personal sign-off. The sprint after it is optional — 499 SAR, 7 days, delivering: 10 ranked accounts, bilingual drafts, a governance decisions log, a 14-section Proof Pack, and one reusable capital asset.
> Shall I send you the diagnostic intake link, or arrange a 20-minute call to check whether it fits?

The reply is followed by a qualification call only after the contact picks one. If they pick the intake link, the qualification is run on the submitted intake; see Section 5.

### 4.2 Not interested — غير مهتم

**Signal:** the contact says "not right now," "we have something internal," "stretched on budget," or any variant of decline.

**Founder action:** thank them, log it, never push. The relationship is the asset; the deal is a moment.

**Arabic draft:**

> شكراً على الصراحة، يفيدني سماعها مبكراً. أبقي اسمكم في قائمة المتابعة العامة — لا رسائل آلية، فقط حين تصدر دراسة حالة قطاعية تخصكم.
> إن خطر لكم شخص قد يفيده، أُقدّر إحالته. (الإحالة المُغلقة لها مكافأة معلنة، 5,000 ريال لكل صفقة مُغلقة).

**English draft:**

> Thank you for the directness — it helps. I will keep you on the general radar — no automated follow-ups, only when a sector case study you might care about is published.
> If someone you know might benefit, I would be grateful for an intro. (Our referral program pays 5,000 SAR per closed deal, transparently.)

`friction_log` entry: reason captured anonymously (sector, size, decline reason), no personal name carried beyond the engagement entry.

### 4.3 Asks more info — يطلب تفاصيل

**Signal:** the contact wants the deliverable list, the pricing breakdown, a sample Proof Pack, references, or the methodology document.

**Founder action:** send one short reply with up to two links, never an attachment, never a sales deck. Pick the link that matches the question they asked.

**Arabic draft:**

> سؤال وجيه. أرفقُ مرجعين:
> 1) معيار حزمة الإثبات (14 قسماً + معادلة الدرجة): <link to PROOF_PACK_STANDARD>.
> 2) جواز المصدر (لماذا كل بيان يحمل بطاقة): <link to LINKEDIN_POST_002>.
> إن أردت 20 دقيقة لاحقاً للحديث على حالة محددة، أرشّح أن ترسل عميلاً واحداً تفكر فيه، وأحضّر تشخيصاً مصغّراً قبل المكالمة.

**English draft:**

> Good question. Two references:
> 1) Proof Pack standard (14 sections + score formula): <link to PROOF_PACK_STANDARD>.
> 2) Source Passport explainer: <link to LINKEDIN_POST_002>.
> If you want a 20-minute call later, I suggest you nominate one customer in mind, and I prepare a micro-diagnostic before the call.

A second back-and-forth is acceptable. A third without progress to either a call or an intake form is itself a signal — log as `low_intent` and leave the door open.

---

## 5. Qualification gate — بوابة التأهيل

Every reply that crosses into "tell me more" triggers a qualification call (20 minutes) and a structured intake. After the call, the founder runs the qualifying endpoint:

```
POST /api/v1/service-setup/qualify
{
  "engagement_id": "<eng_id>",
  "intake": {
    "sector": "<insurance | saas | logistics | education | retail | other>",
    "company_size": "<1-10 | 11-50 | 51-200 | 201+>",
    "primary_problem": "<short string>",
    "data_ownership_declared": true,
    "decision_authority": "founder | head_of_sales | head_of_data | other",
    "consent_to_diagnostic": true
  },
  "founder_notes": "<text>"
}
```

The endpoint returns one of five decisions. Each maps to a precise next action:

| Decision | Meaning | Next step |
|---|---|---|
| `ACCEPT` | Fits the productized offer. Data ownership is clear. Decision-maker is on the call. | Send the Free Diagnostic intake link. 24-hour clock starts on submission. Engagement moves to `diagnostic_in_progress`. |
| `DIAGNOSTIC_ONLY` | Fits, but only at the diagnostic tier. Risk of misalignment past the diagnostic; do not pitch the sprint yet. | Run the Free Diagnostic. At delivery, the recommendation field decides whether to invite to a sprint. |
| `REFRAME` | Genuine intent, wrong frame. Customer is asking for a service we do not offer (e.g., full-funnel marketing), but the underlying need fits something we do (e.g., data quality). | Reply with a 3-line reframe note. Re-run the qualify endpoint with the new framing. |
| `REJECT` | Outside the productized scope. Examples: cold outreach automation, LinkedIn automation, guaranteed sales, scraped-list enrichment. | Polite refusal, with the constitutional clause cited briefly. `friction_log` entry. No follow-up. |
| `REFER_OUT` | Need is legitimate but better served by a partner. | Make the intro to the partner. Record in `referral_ledger` with `direction=outbound`. No fee taken on outbound referrals unless a written reciprocal exists. |

The decision is logged in `proof_ledger` as `event=qualify_decision`. The five decisions are the complete set; the founder does not invent a sixth one.

---

## 6. Daily wrap — الإغلاق اليومي

At the end of each outreach day, the founder writes a one-paragraph wrap in `friction_log`:

- How many messages sent, replies received, replies converted to qualification calls.
- The single biggest objection of the day, verbatim and anonymized.
- One change to the script or the offer for tomorrow — or no change, with a reason.

The wrap is two minutes of writing. The compound effect across four days is the founder's first sector pattern asset, deposited at the end of week one in `capital_ledger`.

---

## 7. What this workflow refuses — ما يرفضه هذا التدفّق

- **No automated sends.** Every message is typed by the founder.
- **No "spray and pray."** Twenty contacts is the universe for week one. Twenty-one requires a new approval.
- **No pricing negotiation in chat.** Pricing is fixed at 499 SAR for the sprint, 0 SAR for the diagnostic. Negotiation happens only on the Managed Ops / Custom AI tiers and only in a scheduled call.
- **No deck before a call.** No PDF before a question. No automated calendar link as the first reply.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
