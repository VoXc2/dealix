# PROPOSAL — Paid Diagnostic Tiers / مقترح تسعير التشخيص المدفوع

> 🚫 **THIS IS A PROPOSAL — NOT LIVE PRICING.**
> This document does **not** change the offer ladder. Live pricing remains as
> defined in `docs/OFFER_LADDER_AND_PRICING.md` and
> `auto_client_acquisition/service_catalog/registry.py`. Adopting the tiers
> below requires an explicit founder decision plus the evidence described in
> "Adoption gate".
>
> 🚫 **هذا مقترح — وليس تسعيراً حياً.** لا يغيّر هذا المستند سلّم العروض.
> التسعير الحي يبقى كما في `docs/OFFER_LADDER_AND_PRICING.md`.

---

## العربية

### السياق

استراتيجية Revenue OS تقترح **عرضاً ملكياً واحداً** بمدخل واحد:
**7-Day Governed Revenue & AI Ops Diagnostic** — تشخيص مدفوع، بأربع شرائح.

### الشرائح المقترحة

| الشريحة | السعر المقترح |
|---|---|
| Starter | 4,999 SAR |
| Standard | 9,999 SAR |
| Executive | 15,000 SAR |
| Enterprise Diagnostic | 25,000 SAR |

المسار بعد التشخيص: Diagnostic → Revenue Intelligence Sprint → Governed Ops
Retainer.

### التعارض مع الدوكترين الحالي

| البند | الحالي (نافذ) | المقترح |
|---|---|---|
| التشخيص | **مجاني** (Rung 0) | مدفوع 4,999–25,000 SAR |
| الـ Sprint | **499 SAR** (مقفول) | غير متأثر |

`docs/OFFER_LADDER_AND_PRICING.md` ينص صراحةً: **لا تغييرات سعرية بدون ≥ 3
pilots مدفوعة**، و Rung 1 (499 SAR) مقفول حتى تثبته 3 pilots.

### بوابة التبنّي (Adoption gate)

لا يصبح هذا التسعير حياً إلا بعد:

1. **قرار مؤسس صريح** موثّق.
2. **≥ 3 تشخيصات مدفوعة** أثبتت استعداد السوق للدفع عند هذا المستوى.
3. تحديث `docs/OFFER_LADDER_AND_PRICING.md` و `service_catalog/registry.py`
   معاً (السلّم يفرض ترتيباً سعرياً تصاعدياً على مستوى الـ registry).
4. اجتياز اختبارات الدوكترين — لا سعر مخفي (`no_hidden_pricing`).

> ملاحظة استراتيجية: تسعير 4,999+ يستبعد عميل «automation رخيص» ويستهدف عميل
> «governed operations» — وهذا متّسق مع التموضع. لكن قفل التسعير في المستودع
> موجود تحديداً لمنع التسعير بلا دليل. القرار للمؤسس.

---

## English

### Context

The Revenue OS strategy proposes a **single royal offer** with one entry:
the **7-Day Governed Revenue & AI Ops Diagnostic** — a paid diagnostic with
four tiers.

### Proposed tiers

| Tier | Proposed price |
|---|---|
| Starter | 4,999 SAR |
| Standard | 9,999 SAR |
| Executive | 15,000 SAR |
| Enterprise Diagnostic | 25,000 SAR |

Post-diagnostic path: Diagnostic → Revenue Intelligence Sprint → Governed Ops
Retainer.

### Conflict with current doctrine

| Item | Current (live) | Proposed |
|---|---|---|
| Diagnostic | **Free** (Rung 0) | Paid 4,999–25,000 SAR |
| Sprint | **499 SAR** (locked) | Unaffected |

`docs/OFFER_LADDER_AND_PRICING.md` explicitly states: **no price changes
without ≥ 3 paid pilots**, and Rung 1 (499 SAR) is locked until 3 pilots
validate it.

### Adoption gate

This pricing only goes live after:

1. An explicit, documented **founder decision**.
2. **≥ 3 paid diagnostics** proving the market will pay at this level.
3. Updating `docs/OFFER_LADDER_AND_PRICING.md` and
   `service_catalog/registry.py` together (the ladder enforces an ascending
   price constraint at the registry level).
4. Passing doctrine tests — no hidden pricing (`no_hidden_pricing`).

> Strategic note: 4,999+ pricing screens out the "cheap automation" buyer and
> targets the "governed operations" buyer — consistent with positioning. But
> the repo's pricing lock exists precisely to prevent pricing without evidence.
> The decision is the founder's.
