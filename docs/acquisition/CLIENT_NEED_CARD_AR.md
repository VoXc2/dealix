# Client Need Card — دليل النظام

**الهدف:** يترجم وضع الشركة إلى **حاجة محددة** + النظام الذي يلبّيها + **المدخلات المطلوبة** للبدء + مقياس نجاح واضح. هذا الكرت هو الجسر بين «بحثنا عن الشركة» و«جهّزنا لها عرضًا وتسليمًا».

- **Schema:** [`schemas/client_need_card.schema.json`](../../schemas/client_need_card.schema.json)
- **البيانات:** [`data/acquisition/client_need_cards.jsonl`](../../data/acquisition/client_need_cards.jsonl)
- **المولّد:** [`scripts/generate_acquisition_packs.py`](../../scripts/generate_acquisition_packs.py)

---

## 1. الحقول

| الحقل | المعنى |
|------|--------|
| `card_id` | معرّف الكرت (CNC-001 …) |
| `company`, `sector` | الشركة والقطاع |
| `recommended_system` | النظام المقترح |
| `current_state` | الوضع الحالي المرجّح |
| `pain_hypothesis` | فرضية الألم (وليست حقيقة مؤكدة) |
| `desired_outcome` | النتيجة المرغوبة |
| `success_metric` | كيف نعرف أننا نجحنا |
| `required_inputs` | المدخلات اللازمة للبدء (نفس مدخلات التسليم) |
| `decision_maker_target` | الدور المستهدف |
| `urgency` | low / medium / high (تُشتق من score) |
| `evidence_level` | مستوى الدليل |
| `next_action` | الخطوة التالية |

> **لماذا مهم؟** `required_inputs` هنا = نفس المدخلات التي يطلبها التسليم لاحقًا. فإذا انتقلت الشركة من «مهتم» إلى «عميل»، نكون قد عرفنا مسبقًا ما نحتاج لجمعه — ولا يبدأ التسليم قبل اكتمالها (انظر [بوابات القبول](../delivery/DELIVERY_ACCEPTANCE_GATES_AR.md)).

---

## 2. مثال (مولّد فعليًا)

```txt
Card: CNC (Follow-up Recovery OS)
Company: SkillUp Arabia
Pain hypothesis: انخفاض نسبة تحول الاستفسارات إلى تسجيلات
Desired outcome: طابور متابعة واضح، ورسائل جاهزة حسب حالة كل عميل، وإيقاع متابعة ثابت.
Success metric: وجود طابور متابعة، ولكل فرصة رسالة مناسبة، وإيقاع متابعة واضح، وتقرير أسبوعي.
Required inputs: قائمة leads أو محادثات · آخر تواصل · حالة كل lead · قنوات المتابعة · أمثلة ردود العملاء
Decision maker target: Training Manager
Urgency: medium
```

---

## 3. قواعد صارمة

- `pain_hypothesis` **فرضية** لا تُقدَّم للعميل كحقيقة مؤكدة.
- `success_metric` لازم يكون **قابلًا للملاحظة** (ليس وعدًا برقم عائد).
- `required_inputs` لا تكون فارغة (يفرضه الفحص C11 على Schema).
