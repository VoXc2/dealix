# Mini Proposal System — العرض المصغّر (صفحة واحدة)

**الهدف:** بعد البريد أو المكالمة، يجهّز النظام عرضًا من صفحة واحدة لكل شركة: لماذا هذا النظام، الألم الحالي، أول سبرنت، المخرجات، المدة، سعر مبدئي، المدخلات المطلوبة، أول دليل متوقع، والخطوة التالية.

> كل عرض **يتطلب موافقة المؤسس قبل الإرسال** (`approval_required = true`). ولا توجد وعود عائد مضمونة في أي عرض.

- **Schema:** [`schemas/mini_proposal.schema.json`](../../schemas/mini_proposal.schema.json)
- **البيانات:** [`data/acquisition/mini_proposals.jsonl`](../../data/acquisition/mini_proposals.jsonl)
- **الطابور:** [`reports/acquisition/MINI_PROPOSAL_QUEUE.md`](../../reports/acquisition/MINI_PROPOSAL_QUEUE.md)

---

## 1. البنية

```txt
Title · Recommended System · Why this system · Current likely pain
First sprint · Deliverables · Timeline · Starter price
Required inputs · Expected first proof · Next step · Approval required
```

## 2. السبرنت والسعر المبدئي لكل نظام

| النظام | السبرنت | السعر المبدئي |
|--------|---------|----------------|
| Revenue Operating System | 7-Day Revenue Operating Sprint | تبدأ من 4,500 ريال |
| Executive Command OS | 7-Day Executive Command Sprint | تبدأ من 4,000 ريال |
| Follow-up Recovery OS | 7-Day Follow-up Recovery Sprint | تبدأ من 3,500 ريال |
| WhatsApp Client OS | 7-Day WhatsApp Client Sprint | تبدأ من 3,500 ريال |
| Proposal & Proof OS | 7-Day Proposal & Proof Sprint | تبدأ من 3,000 ريال |

> السعر **مبدئي** ونقطة بداية للنقاش — التسعير النهائي قرار المؤسس ولا يُؤتمت.

## 3. مثال (مولّد فعليًا)

```txt
Title: 7-Day Follow-up Recovery Sprint — Growth Labs SA
Recommended system: Follow-up Recovery OS
Why: النظام يبني طابور متابعة ونموذج حالات ورسائل جاهزة حسب حالة العميل…
Current likely pain: غياب نظام متابعة موحد بعد أول تواصل
First sprint: نبني follow-up queue ونموذج حالات ورسائل متابعة حسب حالة العميل وإيقاع تذكير.
Deliverables: Follow-up Queue · Lead Status Model · Follow-up Message Set · Reminder Rhythm · Recovery Report · Escalation Rules
Timeline: 7 أيام
Starter price: تبدأ من 3,500 ريال
Expected first proof: قائمة أولية بالفرص القابلة للاسترجاع التي توقفت متابعتها.
Next step: مكالمة 20 دقيقة لفهم مصادر الاستفسارات وقنوات المتابعة.
Approval required: true
```

---

## 4. قواعد صارمة

- الفحص **C04** يضمن وجود `deliverables` و`starter_price_sar > 0` لكل عرض.
- الفحص **C06** يمنع أي مصطلح وعد/ضمان في نص العرض.
- الفحص **C08** يضمن `approval_required = true`.
- `required_inputs` في العرض = نفس مدخلات التسليم، فيعرف العميل مسبقًا ما سيُطلب منه.
