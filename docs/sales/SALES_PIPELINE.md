# Dealix Sales Pipeline — stages and exit criteria

```
Lead → Qualified → Discovery Scheduled → Discovery Done → Proposal Sent → Verbal Yes → Paid → Delivery Started → Proof Delivered → Retainer Offered → Retainer Won
```

## Lead

**Exit criteria**

- Company identified
- Contact path exists (email, intro, or inbound)

## Qualified

**Exit criteria**

- Fits ICP
- Clear pain signal
- Likely budget range discussed or inferable
- Owner / champion identified

## Discovery Scheduled

**Exit criteria**

- Time confirmed
- Pre-read or intake link sent (if applicable)

## Discovery Done

**Exit criteria**

- Problem and success metric articulated
- Data / process reality confirmed (what exists today)
- Decision-maker and approval path known
- Governance constraints understood (no auto-external comms, etc.)

## Proposal Sent

**Exit criteria**

- Service / sprint selected
- Scope, timeline, and price in writing
- Success metric and deliverables listed

## Verbal Yes

**Exit criteria**

- Client confirms intent to proceed (subject to contract / invoice)

## Paid

**Exit criteria**

- Invoice paid or agreement signed per your policy

## Delivery Started

**Exit criteria**

- Kickoff done; client responsibilities and timeline active

## Proof Delivered

**Exit criteria**

- Client received proof pack (or equivalent deliverable bundle)
- Review call completed; feedback captured

## Retainer Offered

**Exit criteria**

- Next step and monthly value articulated
- Clear packaged offer (scope, cadence, price band)

## Retainer Won

**Exit criteria**

- Retainer agreement active; first operating cycle scheduled

## Sales Room (per opportunity) — غرفة الصفقة (لكل فرصة)

Every opportunity carries one **deal room** — a single record that holds the full
truth of that opportunity. No opportunity moves through the stages above without a
deal room behind it. كل فرصة لها غرفة صفقة واحدة — سجل واحد يحمل كامل الحقيقة عن
تلك الفرصة. لا تتحرّك أي فرصة عبر المراحل أعلاه بدون غرفة صفقة خلفها.

### Deal room fields — حقول غرفة الصفقة

- **Company / الشركة** — the account name and segment.
- **Buyer / المشتري** — the named person and their role / approval authority.
- **Segment / القطاع** — the ICP segment this account belongs to.
- **Pain / الألم** — the problem in the buyer's own words.
- **Source / المصدر** — how the opportunity started (inbound, intro, founder-led).
- **Proof sent / الإثبات المُرسَل** — which assets were sent and when.
- **Demo date / تاريخ العرض** — scheduled or held.
- **Objections / الاعتراضات** — recorded as raised, not paraphrased away.
- **Scope / النطاق** — the offer and scope discussed (figures from
  [`../COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) only).
- **Invoice / الفاتورة** — sent / paid status; value logged only when paid.
- **Decision criteria / معايير القرار** — what the buyer needs to decide yes.
- **Next action / الإجراء التالي** — the single next step, with an owner.
- **Evidence / الدليل** — the recorded proof for the current stage.

### Decision states — حالات قرار الفرصة

At any review, an opportunity sits in exactly one state:

- **Advance / تقدّم** — evidence supports moving to the next stage.
- **Nurture / رعاية** — real but not ready; keep the door open, no push.
- **Partner route / مسار شريك** — better served through a partner; hand off.
- **Close lost / إغلاق خاسر** — log the reason, anonymized; relationship stays.
- **Ask referral / طلب إحالة** — closed or nurturing, but worth a referral ask.

### Three rules — القواعد الثلاث

> **No opportunity without a next action. No next action without a date. No stage
> without evidence.**
> **لا فرصة بدون next action، ولا next action بدون تاريخ، ولا مرحلة بدون evidence.**

These rules gate every stage transition above. A deal room that fails any of the
three is not allowed to advance — it is marked and reviewed, not moved.

See also: `docs/sales/QUALIFICATION_SCORE.md`, `docs/company/SERVICE_REGISTRY.md`, `docs/sales/PROPOSAL_SYSTEM.md`.
