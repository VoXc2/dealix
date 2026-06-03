# Mini Proposal Queue
*Date: 2026-06-03 | Source: data/proposals/mini_proposals.jsonl*

> العروض المختصرة الجاهزة. كلها **مسودات** بـ `approval_required = true` — لا إرسال قبل اعتماد المؤسس.

---

## 1. الطابور

| العرض | الشركة | النظام | السعر (SAR) | المدة | المخرجات | الحالة |
|------|--------|--------|------:|------|:-------:|--------|
| MP-001 | Madar | Revenue Operating System | 4,500 | 5–7 أيام | 4 | draft |
| MP-002 | Tadreeb Plus | Follow-up Recovery OS | 3,500 | 7 أيام | 4 | draft |
| MP-003 | Noor Clinics | WhatsApp Client OS | 4,500 | 5–7 أيام | 4 | draft |
| MP-004 | Rased | Proposal & Proof OS | 3,000 | 5 أيام | 4 | draft |
| MP-005 | BinaaPro | Proposal & Proof OS | 3,000 | 5–7 أيام | 4 | draft |

**إجمالي القيمة الافتتاحية:** 18,500 SAR (إن اعتُمدت وأُغلقت جميعًا).

---

## 2. أول دليل قيمة متوقع (Expected First Proof)

| العرض | أول دليل |
|------|---------|
| MP-001 | خريطة تسرب الفرص خلال الأيام الأولى |
| MP-002 | قائمة متابعة تُظهر التسجيلات القابلة للاسترجاع |
| MP-003 | خريطة تدفق واضحة لرحلة الحجز مع نقاط التحويل البشري |
| MP-004 | قالب عرض موحّد جاهز للعرض القادم |
| MP-005 | قالب عرض فني + بلوك مخاطر جاهزان |

---

## 3. بوابة الجودة (مُجتازة)

```
✅ starter_price_sar > 0 لكل عرض
✅ approval_required = true لكل عرض
✅ ≥ 3 deliverables لكل عرض
✅ expected_first_proof موجود
✅ لا ادعاءات مضمونة (الفاحص يتجاهل النفي مثل "لا نضمن")
```

التفصيل: `docs/proposals/MINI_PROPOSAL_FACTORY_AR.md` + `PROPOSAL_APPROVAL_GATE_AR.md`.

---

*Mini Proposal Queue | Generated: 2026-06-03 | كل عرض مسودة*
