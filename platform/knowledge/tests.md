# العربية

# اختبارات — طبقة المعرفة (الطبقة الرابعة)

> مواصفة حالات الاختبار ومعايير القبول لطبقة المعرفة والذاكرة. هذه مواصفة، لا كود.

## 1. النطاق

تغطي هذه المواصفة: الاستيعاب، التقطيع، التضمين، الاسترجاع الهجين، إعادة الترتيب، الاستشهادات، تتبّع نسب المصدر، وعزل المستأجرين.

## 2. حالات اختبار الاستيعاب

| # | الحالة | معيار القبول |
|---|---|---|
| ING-1 | استيعاب محتوى بلا `tenant_id` | يُرفض المحتوى ولا يُخزَّن في نطاق افتراضي. |
| ING-2 | استيعاب محتوى يحوي بيانات شخصيّة | تُحجَب البيانات قبل التخزين عبر `pii_redactor.py`. |
| ING-3 | استيعاب محتوى بلا أساس قانوني | يدخل قائمة مراجعة بشريّة، لا الفهرسة المباشرة. |
| ING-4 | استيعاب وحدة سليمة | تُختم بطابع زمني وحالة `fresh` وقيد تدقيق. |

## 3. حالات اختبار التقطيع والتضمين

| # | الحالة | معيار القبول |
|---|---|---|
| CHK-1 | تقطيع مستند فيه جدول | لا يُقطَع المقطع عبر منتصف الجدول. |
| CHK-2 | كل مقطع | يحمل `chunk_id` و `tenant_id` ومرجع الملف وبصمة محتوى. |
| EMB-1 | تضمين مقطع | يُعاد متّجه بطول 1536 من `text-embedding-3-small`. |
| EMB-2 | فشل واجهة التضمين | يُعاد متّجه صفري ويُسجَّل تحذير، دون تعطّل. |
| EMB-3 | تحديث مصدر | تُحدَّث المقاطع المتغيّرة فقط (مقارنة بصمات)، وتبقى البقيّة. |

## 4. حالات اختبار الاسترجاع والاستشهاد

| # | الحالة | معيار القبول |
|---|---|---|
| RET-1 | استعلام بلا `tenant_id` | يُرفض الاستعلام. |
| RET-2 | استعلام مستأجر A | لا تظهر أي نتيجة من مستأجر B. |
| RET-3 | مستخدم بلا صلاحيّة على مقطع | لا يظهر المقطع ولا يُكشف وجوده. |
| RET-4 | سؤال بلا أي مقطع مطابق | تُرجَع «أدلّة غير كافية» (`insufficient_evidence: true`). |
| RET-5 | تطابق دلالي ومعجمي | يدمج الاسترجاع الهجين القائمتين ويُزيل التكرار. |
| CIT-1 | إجابة بلا مصادر مُمرَّرة | إجابة فارغة و `insufficient_evidence: true`. |
| CIT-2 | إجابة بمصادر | كل استشهاد يحمل `id` ومقتطفًا داعمًا. |
| CIT-3 | استشهاد لا يدعم الادّعاء | يُرصَد كخطأ جودة في تقييم المعرفة. |

## 5. حالات اختبار النسب والحداثة

| # | الحالة | معيار القبول |
|---|---|---|
| LIN-1 | أي إجابة منتَجة | يمكن تتبّعها رجوعًا إلى ملفها الأصلي. |
| LIN-2 | تعديل مصدر | تظل الاستشهادات القديمة تشير إلى نسختها وقت الإنشاء. |
| FRS-1 | مصدر قديم | يُوسَم `aging` ثم `stale`، ولا يُحذف بصمت. |

## 6. معايير القبول الشاملة

- صفر حالات استرجاع عابرة للمستأجرين في كل المجموعة.
- 100% من الإجابات المهمّة تحمل استشهادًا أو تُرجِع «أدلّة غير كافية».
- نجاح تقييمات `knowledge_eval.py` و `evals/governance_eval.yaml` و `evals/arabic_quality_eval.yaml`.
- دقّة الاستشهاد ≥ 95% على مجموعة التقييم الثابتة.

روابط: `readiness.md` · `scorecard.yaml` · `citations.md`

---

# English

# Tests — Knowledge Layer (Layer 4)

> A specification of test cases and acceptance criteria for the knowledge and memory layer. This is a spec, not code.

## 1. Scope

This spec covers: ingestion, chunking, embedding, hybrid retrieval, reranking, citations, source lineage, and tenant isolation.

## 2. Ingestion test cases

| # | Case | Acceptance criterion |
|---|---|---|
| ING-1 | Ingest content without a `tenant_id` | Content is rejected and not stored under a default scope. |
| ING-2 | Ingest content containing personal data | Data is redacted before storage via `pii_redactor.py`. |
| ING-3 | Ingest content without a lawful basis | It enters a human review queue, not direct indexing. |
| ING-4 | Ingest a valid unit | It is stamped with a timestamp, `fresh` status, and an audit entry. |

## 3. Chunking and embedding test cases

| # | Case | Acceptance criterion |
|---|---|---|
| CHK-1 | Chunk a document containing a table | The chunk is not cut through the middle of the table. |
| CHK-2 | Every chunk | Carries a `chunk_id`, `tenant_id`, file reference, and content hash. |
| EMB-1 | Embed a chunk | A 1536-length vector from `text-embedding-3-small` is returned. |
| EMB-2 | Embedding API failure | A zero vector is returned and a warning logged, with no crash. |
| EMB-3 | Update a source | Only changed chunks are updated (hash comparison); the rest remain. |

## 4. Retrieval and citation test cases

| # | Case | Acceptance criterion |
|---|---|---|
| RET-1 | Query without a `tenant_id` | The query is rejected. |
| RET-2 | Query by tenant A | No result from tenant B appears. |
| RET-3 | User lacking permission on a chunk | The chunk does not appear and its existence is not revealed. |
| RET-4 | Question with no matching chunk | "Insufficient evidence" is returned (`insufficient_evidence: true`). |
| RET-5 | Semantic and lexical match | Hybrid retrieval merges the two lists and deduplicates. |
| CIT-1 | Answer with no sources passed | Empty answer and `insufficient_evidence: true`. |
| CIT-2 | Answer with sources | Every citation carries an `id` and a supporting excerpt. |
| CIT-3 | Citation that does not support the claim | Flagged as a quality defect in the knowledge eval. |

## 5. Lineage and freshness test cases

| # | Case | Acceptance criterion |
|---|---|---|
| LIN-1 | Any produced answer | Can be traced back to its origin file. |
| LIN-2 | A source is edited | Old citations still point to their version at creation time. |
| FRS-1 | An aging source | Is flagged `aging` then `stale`, and is never silently deleted. |

## 6. Overall acceptance criteria

- Zero cross-tenant retrieval incidents across the whole set.
- 100% of important answers carry a citation or return "insufficient evidence."
- `knowledge_eval.py`, `evals/governance_eval.yaml`, and `evals/arabic_quality_eval.yaml` pass.
- Citation accuracy >= 95% on the fixed eval set.

Links: `readiness.md` · `scorecard.yaml` · `citations.md`
