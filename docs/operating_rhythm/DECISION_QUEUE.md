# Decision Queue — قائمة قرارات، لا مهام فقط

Dealix تحتاج **قائمة قرارات** منفصلة عن قائمة المهام: كل عنصر له نوع، هدف، أدلة، مالك، موعد، وحالة.

## حقل القرار (مرجع JSON)

```json
{
  "decision_id": "DEC-001",
  "type": "BUILD | SCALE | KILL | HOLD | OFFER_RETAINER | RAISE_PRICE",
  "target": "Approval Center MVP",
  "evidence": ["approval friction repeated across 4 clients"],
  "owner": "Product Owner",
  "deadline": "this_week",
  "decision_status": "pending"
}
```

## أنواع القرارات (قابلة للتوسيع)

Build، Scale، Kill، Hold، Raise price، Offer retainer، Reject revenue، Create playbook، Create benchmark، Create standard، Create venture candidate — والتصنيف الفعلي في الكود: `operating_rhythm_os.decision_queue`.

## القواعد

- **كل قرار بلا evidence → مؤجل** (لا يُسجّل كـ«جاهز للتنفيذ»).
- **كل evidence متكرر بلا قرار → هدر** — يجب أن يتحول إلى قرار في الأسبوع التالي.

## الكود

`auto_client_acquisition/operating_rhythm_os/decision_queue.py`
