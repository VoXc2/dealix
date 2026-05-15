# العربية

Owner: مالك تقييم الاسترجaع — مهندس RAG الرئيسي (RAG Lead Engineer)

## الغرض

يقيس هذا المستند جودة طبقة الاسترجاع (RAG) في منصة دياليكس: هل يجلب النظام الوثائق الصحيحة، وهل تستند إجابات الوكيل فعلياً إلى ما تم جلبه. الهدف من الطبقة الثامنة هو التوقف عن خداع النفس — قياس الجودة بدل افتراضها.

## مقاييس الاسترجاع

| المقياس | التعريف | لماذا يهم |
|---|---|---|
| الاستدعاء عند 5 (recall@5) | نسبة الوثائق ذات الصلة الموجودة ضمن أفضل 5 نتائج | يكشف فقدان مصادر ضرورية |
| الدقة عند 5 (precision@5) | نسبة النتائج الخمس التي كانت فعلاً ذات صلة | يكشف الضجيج الذي يربك الوكيل |
| MRR (متوسط الرتبة العكسية) | جودة ترتيب أول نتيجة صحيحة | يقيس قرب الإجابة الصحيحة من القمة |
| الاستناد (groundedness) | نسبة الحقائق في الإجابة التي تتبع وثيقة مُسترجَعة | المقياس المركزي ضد الهلوسة |
| معدل الامتناع الصحيح | نسبة الاستعلامات بلا مصدر التي امتنع فيها الوكيل عن الإجابة | يكافئ قول «لا أعرف» بدل الاختلاق |
| زمن الاسترجاع p95 | المئين 95 لزمن جلب الوثائق | إشارة تشغيلية للجاهزية |

## كيفية القياس

- مجموعة البيانات الذهبية: `evals/retrieval/dataset.jsonl` تحتوي على 8–12 استعلاماً بمعرّفات وثائق مرجعية مُتحقَّقة يدوياً.
- يُشغَّل التقييم عبر حزمة CI الموجودة `scripts/run_evals.py` ضمن `.github/workflows/ci.yml`.
- تُقارن المخرجات بالحدود في `evals/retrieval/thresholds.yaml`.
- الاستناد يُقيَّم باسترجاع كل حقيقة في الإجابة وإثبات ورودها في وثيقة مُسترجَعة؛ أي حقيقة بلا مصدر تُعدّ هلوسة.

## ربط المراقبة

- يُسجَّل لكل استعلام: معرّفات الوثائق المُسترجَعة، الدرجات، قرار الامتناع.
- تُصدَّر المقاييس المجمّعة إلى تقرير تقييم لكل إصدار.
- انخفاض الاستدعاء أو الاستناد دون الحد يرفع تنبيه انحدار قبل الدمج.

## السلوك عند نتيجة فارغة

إذا لم يُرجع الاستعلام أي وثيقة ذات صلة، يجب على الوكيل التصريح بعدم وجود مصدر مستند، ولا يجوز توليد إجابة من الذاكرة البارامترية.

## روابط ذات صلة

- `evals/retrieval/thresholds.yaml`
- `evals/hallucination/rubric.md`
- `evals/readiness.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Retrieval Eval Owner — RAG Lead Engineer

## Purpose

This document measures the quality of the retrieval (RAG) layer in the Dealix platform: does the system fetch the correct documents, and are agent answers actually grounded in what was fetched. The goal of Layer 8 is to stop fooling yourself — measure quality instead of assuming it.

## Retrieval metrics

| Metric | Definition | Why it matters |
|---|---|---|
| recall@5 | Share of relevant documents present in the top 5 results | Detects missing required sources |
| precision@5 | Share of the top 5 results that were actually relevant | Detects noise that confuses the agent |
| MRR (mean reciprocal rank) | Ranking quality of the first correct result | Measures how near the correct answer sits to the top |
| Groundedness | Share of facts in the answer that trace to a retrieved document | The central anti-hallucination metric |
| Correct abstention rate | Share of no-source queries where the agent declined to answer | Rewards saying "I don't know" over fabricating |
| Retrieval latency p95 | 95th percentile of document fetch time | Operational readiness signal |

## How it is measured

- Golden dataset: `evals/retrieval/dataset.jsonl` holds 8-12 queries with manually verified reference document IDs.
- The eval runs through the existing CI bundle `scripts/run_evals.py` inside `.github/workflows/ci.yml`.
- Outputs are compared against the thresholds in `evals/retrieval/thresholds.yaml`.
- Groundedness is scored by tracing each fact in the answer and proving it appears in a retrieved document; any unsourced fact counts as a hallucination.

## Observability hooks

- For every query, the retrieved document IDs, scores, and abstention decision are logged.
- Aggregated metrics are exported to an eval report per release.
- A drop in recall or groundedness below threshold raises a regression alert before merge.

## Behavior on an empty result

If a query returns no relevant document, the agent must state that it has no grounded source and must not generate an answer from parametric memory.

## Related links

- `evals/retrieval/thresholds.yaml`
- `evals/hallucination/rubric.md`
- `evals/readiness.md`

Estimated value is not Verified value.
