# مصنع العروض المصغّرة (Mini Proposals)

عرض مصغّر واحد لكل حساب مؤهّل: محدد، مسعّر، ومغلق النطاق — ويحتاج اعتماد المؤسس
قبل الإرسال.

## المخرجات

- `data/proposals/mini_proposals.jsonl`
- `reports/proposals/MINI_PROPOSAL_QUEUE.md` (طابور)

## بنية العرض

| الحقل | المعنى |
| --- | --- |
| `title` | عنوان مرتبط بالاحتياج والقطاع |
| `core_system`, `sprint_id` | النظام والسبرنت |
| `starter_price_sar` | سعر مبدئي ثابت |
| `deliverables` | ≥ 2 مخرج واضح |
| `timeline_days` | مدة محددة |
| `required_inputs` | مدخلات مطلوبة من العميل |
| `open_scope` | **false دائمًا** (لا نطاق مفتوح) |
| `approval_required` | **true دائمًا** |
| `status` | draft / approved / sent / won / lost |

## بوابة العرض

يفشل العرض إذا: لا سعر، لا مخرجات، لا مدة، لا مدخلات، نطاق مفتوح، بلا اعتماد،
أو وجود وعد مضمون. التطبيق: `scripts/checks/check_proposal_gate.py`.

## القاعدة

```
لا عرض يُرسل آليًا. الاعتماد بشري. النطاق مغلق. لا ضمانات.
```
