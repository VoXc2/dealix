# العربية

# الاستشهادات — طبقة المعرفة (الطبقة الرابعة)

> كيف يربط Dealix كل إجابة بمصدر حقيقي، ولماذا غياب المصدر يعني «أدلّة غير كافية» لا إجابة مُختلَقة.

## 1. الغرض

محرّك الاستشهادات هو ضامن قاعدة «لا مصدر، لا إجابة». مسؤوليّته أن يربط ما تُرجِعه طبقة المعرفة بمقاطع مصدر صريحة، وأن يرفض إنتاج إجابة لا تستند إلى مصدر.

## 2. سلوك المحرّك

كما هو معرّف في `auto_client_acquisition/knowledge_os/answer_with_citations.py`:

- إذا لم تُمرَّر أي مصادر، يُرجِع المحرّك إجابة فارغة مع `insufficient_evidence: true`.
- إذا تُمرَّرت مصادر، يبني كل استشهاد من `id` المصدر ومقتطف نصّي منه.
- السلوك حتميّ (deterministic) عند هذه الحدود: لا توليد بلا مصدر.

## 3. شكل الاستشهاد

كل استشهاد يحمل:

- `id` المقطع المصدر.
- مقتطف نصّي يدعم الجزء المقابل من الإجابة.
- مرجعًا للملف الأصلي عبر تتبّع نسب المصدر.
- حالة حداثة المصدر، حتى يرى القارئ إن كان الدليل حديثًا أو قديمًا.

## 4. دقّة الاستشهاد

- كل جملة تحمل ادّعاءً يجب أن تشير إلى مقطع مصدر يدعمها فعلًا.
- يُقيَّم تطابق الاستشهاد مع الادّعاء عبر `auto_client_acquisition/knowledge_os/knowledge_eval.py` و `evals/governance_eval.yaml`.
- استشهاد لا يدعم الادّعاء يُعد خطأ جودة، لا تفصيلًا تجميليًّا.

## 5. الحوكمة

- لا تُعرَض إجابة على المستخدم بحالة `insufficient_evidence: true` كأنها إجابة مؤكَّدة.
- القيمة التقديريّة تُوسَم صراحةً، ولا تُقدَّم كقيمة مُتحقَّقة.
- لا تُختلَق أرقام مبيعات أو معدّلات تحويل؛ يُذكر فقط ما يدعمه مصدر.
- كل إجابة مع استشهاداتها تُسجَّل في تتبّع نسب المصدر.

روابط: `reranking.md` · `source_lineage.md` · `readiness.md`

---

# English

# Citations — Knowledge Layer (Layer 4)

> How Dealix binds every answer to a real source, and why the absence of a source means "insufficient evidence" rather than a fabricated answer.

## 1. Purpose

The citations engine is the guarantor of the "no source, no answer" rule. Its job is to bind whatever the knowledge layer returns to explicit source chunks, and to refuse to produce an answer that rests on no source.

## 2. Engine behavior

As defined in `auto_client_acquisition/knowledge_os/answer_with_citations.py`:

- If no sources are passed, the engine returns an empty answer with `insufficient_evidence: true`.
- If sources are passed, it builds each citation from the source `id` and a text excerpt from it.
- Behavior is deterministic at these boundaries: no generation without a source.

## 3. Citation shape

Every citation carries:

- The `id` of the source chunk.
- A text excerpt that supports the corresponding part of the answer.
- A reference to the origin file via source lineage.
- The source freshness status, so the reader sees whether the evidence is recent or aging.

## 4. Citation accuracy

- Every sentence carrying a claim must point to a source chunk that genuinely supports it.
- Citation-to-claim alignment is assessed via `auto_client_acquisition/knowledge_os/knowledge_eval.py` and `evals/governance_eval.yaml`.
- A citation that does not support its claim is a quality defect, not a cosmetic detail.

## 5. Governance

- An answer with `insufficient_evidence: true` is not shown to the user as a confirmed answer.
- Estimated values are labeled explicitly and are not presented as verified values.
- Sales numbers and conversion rates are not fabricated; only what a source supports is stated.
- Every answer and its citations are recorded in source lineage.

Links: `reranking.md` · `source_lineage.md` · `readiness.md`
