# 07 — التوسّع والتعلّم / Expansion & Learning (Layer 7)

بعد التسليم لا تقل «شكراً» وتتوقف. حوّل العميل إلى أحد أربعة مسارات.
After delivery, don't just say "thanks". Route the customer into one of four paths.

## العربية

### المسارات الأربعة بعد التسليم

1. Revenue Sprint
2. Governed Ops Retainer
3. Partner referral
4. Case study / anonymous proof asset

### قواعد الترقية (Upsell)

```
workflow واضح + قرار عاجل        → Sprint
مراجعة شهرية / متابعة مستمرة      → Retainer
لا ميزانية الآن                  → nurture
أعجبته الفكرة وله شبكة            → referral
```

### مراجعة CEO الأسبوعية (الجمعة)

```
pipeline report   ·  blockers          ·  conversion rates
next best actions ·  no-build warning
كم lead؟ كم meeting؟ كم scope؟ كم invoice؟ كم paid؟
أفضل ICP؟  أسوأ channel؟  الاعتراض المتكرر؟
ما الذي يجب قتله؟  ما الذي يجب مضاعفته؟
```

### حلقة التعلّم

كل اعتراض → objections library. كل رسالة ناجحة → قالب. كل ICP رابح → تركيز.

### الربط بالنظام

- تتبّع التبنّي: `auto_client_acquisition/adoption_os/`.
- جدولة التجديد: `auto_client_acquisition/payment_ops/renewal_scheduler.py`
  (تجديد تلقائي بعد 3 دورات مؤكدة).
- التقارير الشهرية: `auto_client_acquisition/client_os/`.
- ⚠️ نشر case study يتطلب موافقة العميل + دليل (`no_fake_proof`).

---

## English

### The four post-delivery paths

1. Revenue Sprint
2. Governed Ops Retainer
3. Partner referral
4. Case study / anonymous proof asset

### Upsell rules

```
clear workflow + urgent decision   → Sprint
monthly review / ongoing follow-up → Retainer
no budget now                      → nurture
liked the idea and has a network   → referral
```

### Weekly CEO review (Friday)

```
pipeline report   ·  blockers          ·  conversion rates
next best actions ·  no-build warning
How many leads? meetings? scopes? invoices? paid?
Best ICP?  worst channel?  recurring objection?
What to kill?  what to double down on?
```

### The learning loop

Every objection → objections library. Every winning message → a template.
Every winning ICP → focus.

### How it connects to the system

- Adoption tracking: `auto_client_acquisition/adoption_os/`.
- Renewal scheduling: `auto_client_acquisition/payment_ops/renewal_scheduler.py`
  (auto-renewal after 3 confirmed cycles).
- Monthly reports: `auto_client_acquisition/client_os/`.
- ⚠️ Publishing a case study requires client approval + evidence (`no_fake_proof`).
