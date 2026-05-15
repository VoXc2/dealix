# العربية

# تتبّع نسب المصدر — طبقة المعرفة (الطبقة الرابعة)

> كيف يُتيح Dealix تتبّع أي إجابة رجوعًا إلى الملف الذي جاءت منه، عبر سلسلة اشتقاق كاملة قابلة للتدقيق.

## 1. الغرض

تتبّع نسب المصدر يحفظ سلسلة الاشتقاق: من الملف الأصلي، إلى المقطع، إلى المتّجه، إلى نتيجة الاسترجاع، إلى الاستشهاد في الإجابة. الهدف أن يستطيع أي مدقّق أن يسأل «من أين جاءت هذه الإجابة؟» ويحصل على جواب دقيق.

## 2. سلسلة الاشتقاق

1. **الملف الأصلي:** المستند أو المحادثة أو الحدث المستوعَب، مع `tenant_id` ووقت الاستيعاب.
2. **المقطع:** `chunk_id` وموضعه في الملف وبصمة محتواه.
3. **المتّجه:** سجلّ التضمين المرتبط، مع اسم النموذج.
4. **نتيجة الاسترجاع:** السؤال ودرجة الصلة وترتيب المقطع.
5. **الاستشهاد:** الإجابة النهائيّة والمقاطع التي بُنيت منها.

## 3. أين تُسجَّل النسب

- أحداث الأعمال وأثرها في سجلّ الأحداث `auto_client_acquisition/revenue_memory/` (انظر `event_store.py` و `audit.py`).
- إعادة التشغيل والإسقاطات عبر `auto_client_acquisition/revenue_memory/replay.py` و `projections.py`.
- الخطّ الزمني للحساب عبر `auto_client_acquisition/revenue_memory/timeline.py`.
- قيود التدقيق للإجراءات الحسّاسة عبر `auto_client_acquisition/revenue_memory/audit.py`.

## 4. تحديث مصدر دون كسر التتبّع

- عند تعديل ملف، تُنشأ نسخة مصدر جديدة وتبقى النسخة السابقة مرجعًا تاريخيًّا.
- الاستشهادات القديمة تظل تشير إلى النسخة التي بُنيت منها وقتها، فلا تنكسر سجلّات سابقة.
- يُسجَّل التغيير كحدث، فيظهر في الخطّ الزمني للمصدر.

## 5. حالة الحداثة

كل مصدر يحمل حالة: `fresh` (حديث)، `aging` (يتقادم)، `stale` (قديم). تنتقل الحالة وفق سياسة الاحتفاظ، وتظهر بجانب كل استشهاد، ولا يُحذف مصدر بصمت.

## 6. الحوكمة

- لا تُقبَل إجابة بلا سلسلة نسب كاملة قابلة للتتبّع.
- التتبّع مقيّد بالمستأجر؛ لا يكشف مدقّق مستأجرٍ نسبَ مستأجرٍ آخر.
- حذف مصدر إجراء مُصنَّف يتطلب موافقة موثَّقة، ويترك أثرًا في سجلّ التدقيق.

روابط: `architecture.md` · `citations.md` · `readiness.md` · `../../memory/organizational_memory/retention_policy.md`

---

# English

# Source Lineage — Knowledge Layer (Layer 4)

> How Dealix lets any answer be traced back to the file it came from, through a complete, auditable derivation chain.

## 1. Purpose

Source lineage records the derivation chain: from the origin file, to the chunk, to the vector, to the retrieval result, to the citation in the answer. The goal: any auditor can ask "where did this answer come from?" and get a precise answer.

## 2. Derivation chain

1. **Origin file:** The ingested document, conversation, or event, with its `tenant_id` and ingestion time.
2. **Chunk:** A `chunk_id`, its position in the file, and its content hash.
3. **Vector:** The associated embedding record, with the model name.
4. **Retrieval result:** The question, the relevance score, and the chunk rank.
5. **Citation:** The final answer and the chunks it was built from.

## 3. Where lineage is recorded

- Business events and their trace in the event store `auto_client_acquisition/revenue_memory/` (see `event_store.py` and `audit.py`).
- Replay and projections via `auto_client_acquisition/revenue_memory/replay.py` and `projections.py`.
- The account timeline via `auto_client_acquisition/revenue_memory/timeline.py`.
- Audit entries for sensitive actions via `auto_client_acquisition/revenue_memory/audit.py`.

## 4. Updating a source without breaking tracing

- When a file is edited, a new source version is created and the prior version remains a historical reference.
- Old citations still point to the version they were built from, so prior records do not break.
- The change is recorded as an event and appears on the source timeline.

## 5. Freshness status

Every source carries a status: `fresh`, `aging`, or `stale`. The status transitions per the retention policy, appears next to each citation, and a source is never silently deleted.

## 6. Governance

- An answer without a complete, traceable lineage chain is not accepted.
- Tracing is scoped to the tenant; an auditor of one tenant cannot see the lineage of another.
- Deleting a source is a classified action requiring documented approval and leaves an audit trail.

Links: `architecture.md` · `citations.md` · `readiness.md` · `../../memory/organizational_memory/retention_policy.md`
