# Brain OS — المعرفة الداخلية (Company Brain)

## الهدف في المخطط

`brain_os/` — في الريبو يُنفَّذ أساسًا كـ **`knowledge_os`**.

## قواعد Company Brain

- **No source-less answers** — بلا سجل مصدر لا إجابة ادّعائية.
- إذا الأدلة غير كافية → **insufficient evidence**.
- كل إجابة لها **استشهادات** أو مستوى ثقة معلن.
- فجوات المعرفة تتحول إلى **مهام**.

## المخرجات المستهدفة

سجل المصادر، إجابات موثّقة، تقرير فجوات، معدل نقص الأدلة، حزمة إثبات معرفي.

## التنفيذ في الريبو

- `auto_client_acquisition/knowledge_os/` — مثل `answer_with_citations.py`, `knowledge_eval.py`.
- سجل المصادر في المنتج: `docs/ledgers/SOURCE_REGISTRY.md` ووحدات `revenue_os/source_registry.py` حيث ينطبق.

## روابط

- [TRUST_OS.md](TRUST_OS.md) — [STANDARDS_OS.md](STANDARDS_OS.md)
