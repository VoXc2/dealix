# Dealix — Payment Policy / سياسة الدفع

> **Authoritative.** Single source of truth for payment behavior.
> Refer Support OS payment + refund + billing categories to this
> file.

## Canonical state

```
LIVE_CHARGE_READY = no
PAYMENT_DEFAULT_MODE = test_or_manual
ALLOW_LIVE_FLAG = none (no MOYASAR_ALLOW_LIVE_CHARGE env var exists)
ENTRY_OFFER = 7-Day Governed Revenue & AI Ops Diagnostic
ENTRY_OFFER_TIERS_SAR = 4,999 / 9,999 / 15,000 / 25,000 (see docs/OFFER_LADDER_AND_PRICING.md)
REFUND_WINDOW_DAYS = 7
```

## Arabic — العربيّة

### كيف يعمل الدفع؟

- نُصدر فاتورة Moyasar في وضع التجربة، أو نوفّر تحويل بنكي يدويّ.
- لا يوجد خصم تلقائي، ولا اشتراك متجدّد.
- المؤسس يعتمد كل دفعة قبل الإقرار بأن العميل دفع.
- لا نخزّن بيانات بطاقات بنكيّة — Moyasar يستضيف الدفع.

### الاسترجاع

- سياسة الاسترجاع موثّقة في `docs/REFUND_SOP.md`. الاسترجاع يُطبَّق إذا
  لم يطابق التسليم المواصفات الموثّقة للعرض.
- الاسترجاع يديره المؤسس يدويّاً (Moyasar refund أو حوالة بنكيّة
  معاكسة).

### المفتاح الحيّ

`sk_live_*` مرفوض في CLI ما لم يُمرَّر `--allow-live` يدويّاً.
هذا قرار حماية، ليس خياراً تشغيليّاً.

## English

### How payments work

- We issue a Moyasar test-mode invoice, or provide manual bank
  transfer details.
- No auto-charge, no recurring subscription.
- The founder confirms every payment before marking the customer
  as paid.
- We do NOT store card data — Moyasar hosts the checkout.

### Refunds

- Refund policy is documented in `docs/REFUND_SOP.md`. A refund
  applies if delivery did not match the documented spec for the offer.
- Refunds are processed manually by the founder (Moyasar refund or
  reverse bank transfer).

### Live key behavior

`sk_live_*` is REJECTED by the CLI unless `--allow-live` is passed
manually each time. This is a safety decision, not a configuration
option.

## Refund triggers (mandatory escalation)

If a customer mentions any of:
- "refund" / "استرجاع" / "استرداد" / "money back"
- "I want my money back" / "أبغى فلوسي"

Support OS escalates **immediately** to the founder; no automated
reply is sent.
