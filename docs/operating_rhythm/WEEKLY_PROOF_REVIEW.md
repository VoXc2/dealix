# Weekly Proof Review — مراجعة الإثبات أسبوعيًا

**Proof هو الوقود التجاري.** إن لم تُراجعه أسبوعيًا، يصبح ملفًا يُنسى.

## أسئلة المراجعة

- ما **Proof Packs** التي خرجت؟
- ما **متوسط Proof Score**؟
- أي proof **ضعيف**؟
- أي proof **يصلح للمبيعات**؟
- أي proof **يفتح retainer**؟
- أي proof **يكشف feature**؟

## قرارات تشغيلية (مرجعية)

| الشرط | القرار |
|--------|--------|
| Proof Score ≥ 85 | مرشح لملخص case-safe |
| Proof Score ≥ 80 **و** adoption ≥ 70 | توصية retainer |
| Proof Score < 70 | تحسين تسليم مطلوب |
| نمط proof متكرر | مرشح benchmark |

## الربط بالكود

- `auto_client_acquisition/proof_architecture_os/proof_score.py` — النطاقات والعتبات.
- `auto_client_acquisition/operating_rhythm_os/proof_review.py` — دمج proof + adoption للتوصية الأسبوعية.
