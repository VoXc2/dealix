# Refund SOP — Dealix

**Status:** DRAFT — clauses require lawyer review before customer #1
**Owner:** Sami (founder) · Finance reviews monthly
**Last updated:** 2026-05-07
**Companion docs:** `docs/ops/MANUAL_PAYMENT_SOP.md` · `docs/INVOICING_ZATCA_READINESS.md` · `dealix/payments/moyasar.py` · `scripts/dealix_payment_confirmation_stub.py` · Plan §23.5.6

> **Why this doc exists:** Without a refund SOP written before customer #1, the first unhappy customer either causes panic or breeds resentment. With it, every refund is calm, fast, documented, and good-for-reputation.

---

## 1. Refund commitments by offer

Offer ladder and prices: `docs/OFFER_LADDER_AND_PRICING.md` (Governed Revenue & AI Ops).

### 7-Day Governed Revenue & AI Ops Diagnostic (4,999 / 9,999 / 15,000 / 25,000 SAR)

- **Window:** 14 calendar days from `payment_confirmed` state
- **Coverage:** 100% refund if delivery did not match the documented spec
- **Mechanism:** same channel as payment (bank transfer ↔ bank transfer; Moyasar card ↔ Moyasar reverse)
- **Turnaround:** 3-5 business days bank transfer · 2 business days Moyasar live
- **Ledger entry:** `dealix_payment_confirmation_stub.py --action refund --evidence-note "..."`

### Revenue Intelligence Sprint (25,000 SAR+, scoped)

- **Window:** per the signed scope of work
- **Coverage:** refund applies if delivery did not match the agreed scope; no guaranteed outcomes — Dealix delivers evidenced opportunities and a proof pack
- **Mechanism:** refunded via original payment channel

### Governed Ops Retainer (4,999–35,000 SAR/month, scoped)

- **Window:** any month, on 30-day notice
- **Coverage:** pro-rata refund of unused months absent Dealix fault
- **Note:** no guaranteed revenue or KPI outcomes — the retainer delivers a monthly governed decision rhythm plus a proof pack
- **Mechanism:** prorated by completed days, refunded via original payment channel
- **Turnaround:** 5-7 business days

---

## 2. Refund triggers (when customer can claim)

### Automatic eligibility (no founder discretion needed)

- Diagnostic customer requests refund within 14 days where delivery did not match spec
- Retainer customer cancels on 30-day notice (pro-rata for unused months)

### Founder-discretion eligibility

- Diagnostic customer requests refund after Day 14 with a real complaint (rare; default is no, but log + escalate)
- Retainer customer wants to exit mid-month (default is pro-rata for unused days)
- Customer reports a service breakdown that wasn't fixed within 24h SLA

### Not eligible

- Customer "changed mind" after Day 14 of the Diagnostic without a service issue
- Customer demands a guaranteed revenue or KPI outcome (Dealix sells evidenced opportunities, not guarantees)
- Customer demands Dealix automate something blocked by hard gates (NO_LIVE_SEND, NO_COLD_WHATSAPP, etc.) — refund not applicable; explain gates

---

## 3. Refund process — step by step

### When customer requests refund

**Step 1 — receive request (any channel)**
- Founder acknowledges within 4 hours: «استلمت طلبك. خلال يوم أرتب لك المبلغ.»
- DO NOT argue. DO NOT ask "why" repeatedly. Listen, log.

**Step 2 — verify eligibility (within 24 hours)**
- Open `docs/wave6/live/payment_state.json` for that customer
- Check: payment_confirmed date · days elapsed · SKU type
- Determine: Diagnostic within 14 days with spec mismatch? → AUTO-APPROVE
- Retainer cancellation on notice? → compute pro-rata for unused days
- Founder discretion? → write decision + reason in `docs/wave6/live/refund_log.jsonl` (gitignored)

**Step 3 — execute refund (within 24-72 hours of approval)**
- Bank transfer payments: re-transfer to customer's account, screenshot receipt
- Moyasar card payments: log into Moyasar dashboard → Refund button → enter amount + reason
- Record txn ID in `docs/wave6/live/refund_log.jsonl`

**Step 4 — update payment state machine**
```bash
python3 scripts/dealix_payment_confirmation_stub.py \
  --action refund \
  --customer-handle <handle> \
  --evidence-note "Refund issued via <channel>, txn <id>, reason: <short>"
```

This sets `is_revenue=False`, `state=refunded`. The `confirmed_revenue_sar` aggregator subtracts this customer's amount.

**Step 5 — close-out communication**
- Send customer: "تم تحويل المبلغ. ستصلك خلال 3-5 أيّام عمل. شاكر لك على ثقتك."
- Offer: "لو احتجت تجربة Dealix مرّة ثانية بعد 90 يوم، احتفظت لك بنفس السعر الأوّل."
- DO NOT ghost. DO NOT apologize 10 times. Be calm and grown.

**Step 6 — internal post-mortem**
- Within 1 week, write 1-page reflection: What signal did we miss in the diagnostic call? Was the ICP wrong? Was the value-narrative wrong? Append to `docs/V14_CUSTOMER_SIGNAL_SYNTHESIS.md`.

---

## 4. Refund log — what to record

Append-only JSONL at `docs/wave6/live/refund_log.jsonl`:

```json
{
  "refund_id": "rf_<timestamp>",
  "customer_handle": "...",
  "sku": "sprint_499 | partner_12000",
  "original_payment_confirmed_at": "ISO date",
  "refund_requested_at": "ISO date",
  "refund_executed_at": "ISO date",
  "amount_sar": 499.00,
  "amount_halalah": 49900,
  "channel": "bank_transfer | moyasar_card",
  "txn_id": "...",
  "eligibility_path": "auto_within_14 | founder_discretion | partner_kpi_unmet",
  "reason_short": "...",
  "reason_full": "...",
  "post_mortem_doc_link": "..."
}
```

Same gitignore protection as other live data.

---

## 5. Communication templates (Saudi Arabic)

### When a Diagnostic customer requests a refund within 14 days

> «شكراً على تواصلك [الاسم]. استلمت الطلب.
> سأحوّل لك المبلغ المدفوع لشريحة التشخيص خلال ٣ أيام عمل بأمر الله.
> هل تفضّل التحويل على نفس الـ IBAN اللي حوّلت منه أوّل مرّة، أو IBAN ثاني؟»

### When a Retainer customer wants to exit

> «وصلتني الرسالة [الاسم]. أقدّر صراحتك.
> أتحرّك على الفور:
> - أوقف الفوترة لشهر ٣ و٤
> - أرتّب مبلغ الشهر الباقي مدفوع مسبقاً ([X]) أرجعه لك خلال ٥-٧ أيّام
> - أرسل لك Proof Pack الجزئي للـ ٦ أسابيع اللي اشتغلناها (ملك لك للأبد)
> هل في شيء غيره أقدر أساعدك فيه؟»

### When customer demands feature blocked by hard gate

> «أتفهّم وش تطلب [الاسم]. لكن Dealix فيه قواعد ثابتة في الكود (٨ بوّابات أمان) — هذي ما نقدر نطفّيها لأي عميل.
> السبب: حماية لك من غرامة PDPL، حماية لرقمك من banned، حماية لسمعتك.
> اللي نقدر نسوّيه: نجهّز draft، أنت ترسل بضغطة. هذا اللي ضمن السياسة.
> لو هذا ما يكفي، أفهم — وأقدر أرتّب لك استرجاع كامل خلال ٧ أيّام.»

---

## 6. Refund metrics to track

In monthly Friday review (per `SALES_OPS_SOP.md` §10):

- Refund count by offer
- Refund rate as % of paid customers
- Days-to-refund average
- Top reason (categorize: ICP-mismatch · expectations-mismatch · service-breakdown · other)

**Healthy targets:**
- Diagnostic refund rate: <10% (if higher → ICP problem)
- Retainer refund rate: <5% (if higher → onboarding/CS problem)
- Days-to-refund: <5 average

**Warning signs:**
- Same reason 3+ times → fix the upstream cause (pitch, onboarding, KPI definition)
- Founder argues with customer in refund chat → STOP, re-read this doc

---

## 7. Hard rules

- ❌ Never delay a Sprint refund past Day 14 — eats trust
- ❌ Never charge a "processing fee" on refunds — Saudi B2B trust signal
- ❌ Never refund without recording in refund_log.jsonl — finance ground truth
- ❌ Never tweet/share/discuss a refund publicly — even if customer is wrong
- ✅ Always cc yourself on the refund confirmation message
- ✅ Always offer to keep the relationship warm for future ("احتفظت لك بنفس السعر بعد 90 يوم")
- ✅ Always update `confirmed_revenue_sar` via CLI — keep ground truth honest

> **Lawyer review checkpoint:** §1 refund commitments + §3 mechanism + §5 communication templates → must be reviewed by lawyer (per Wave 7 §23.5.5 deliverable L4) before customer #1. Specifically: confirm ZATCA refund handling for VAT (refund must NOT include VAT once collected; treat refund as supply reversal, refile VAT in next quarter).
