# العربية

# المعمارية — طبقة المعرفة (الطبقة الرابعة)

> هذا المستند يصف معمارية طبقة المعرفة والذاكرة في منصة Dealix: كيف تتحوّل ملفات المؤسسة ومحادثاتها وقراراتها إلى ذاكرة قابلة للاسترجاع مع مصدر لكل إجابة.

## 1. الغرض

الطبقة الرابعة تجعل Dealix «ذاكرة الشركة». الهدف أن يعرف النظام العملاء والسياسات والملفّات والعمليّات والقرارات والسياق، وأن يجيب على أي سؤال مهم مع استشهاد بمصدر حقيقي. القاعدة الحاكمة: «لا مصدر، لا إجابة».

هذه الطبقة لا تنشئ مزاعم جديدة ولا تضمن نتائج؛ هي تسترجع ما هو مُسجَّل بالفعل وتربطه بمصدره.

## 2. المكوّنات

- **بوّابة الاستيعاب (Ingestion):** تستقبل المستندات والمحادثات والأحداث، وتتحقق من ملكية المستأجر والصلاحيات قبل الفهرسة.
- **محرّك التقطيع (Chunking):** يقسّم المستندات إلى مقاطع دلاليّة بحجم متّسق مع حفظ الحدود البنيويّة.
- **خدمة التضمين (Embeddings):** تحوّل المقاطع إلى متّجهات عبر `core/memory/embedding_service.py`.
- **الاسترجاع الهجين (Hybrid Retrieval):** يدمج البحث الدلالي المتّجهي مع البحث المعجمي بالكلمات المفتاحيّة.
- **إعادة الترتيب (Reranking):** يرتّب النتائج المرشّحة حسب الصلة الفعليّة بالسؤال.
- **محرّك الاستشهادات (Citations):** يربط كل جملة في الإجابة بمقطع مصدر، عبر `auto_client_acquisition/knowledge_os/answer_with_citations.py`.
- **تتبّع نسب المصدر (Source Lineage):** يحفظ سلسلة الاشتقاق من الملف الأصلي إلى المقطع إلى الإجابة.
- **سجلّات الذاكرة:** ذاكرة تنظيميّة، ذاكرة العملاء، ذاكرة سير العمل، ذاكرة السياسات، ذاكرة تنفيذيّة.

## 3. تدفّق البيانات

1. يصل مستند أو محادثة إلى بوّابة الاستيعاب مع `tenant_id` ووسوم الصلاحيّة.
2. تتحقق البوّابة من أساس قانوني وملكيّة المستأجر، ثم تمرّر المحتوى للتقطيع.
3. تُقطَّع الوحدة إلى مقاطع، ويُحسب لكل مقطع متّجه تضمين وبصمة محتوى (hash).
4. تُخزَّن المقاطع مع نطاق المستأجر ووسوم الصلاحيّة وحالة الحداثة.
5. عند ورود سؤال، يُجرى استرجاع هجين مقيّد بصلاحيّات المستخدم ومستأجره.
6. تُعاد ترتيب النتائج، وتمرّر أعلى المقاطع لمحرّك الاستشهادات.
7. تُبنى الإجابة فقط من مقاطع لها مصدر؛ غياب المصدر يُرجِع «أدلّة غير كافية».
8. يُسجَّل أثر الاسترجاع كاملًا في تتبّع نسب المصدر.

## 4. ربط بالكود القائم

| المكوّن | المسار في المستودع |
|---|---|
| التضمين والبحث الدلالي | `core/memory/embedding_service.py` |
| الإجابة مع استشهادات | `auto_client_acquisition/knowledge_os/answer_with_citations.py` |
| تقييم سياسة المعرفة | `auto_client_acquisition/knowledge_os/knowledge_eval.py` |
| قاعدة «لا مصدر، لا إجابة» | `auto_client_acquisition/governance_os/rules/no_source_no_answer.yaml` |
| الذاكرة الاستراتيجيّة (ملفّات الدروس) | `auto_client_acquisition/intelligence_os/strategic_memory.py` |
| ذاكرة الإيرادات وتتبّع الأحداث | `auto_client_acquisition/revenue_memory/` |
| سياسة الاحتفاظ بالأحداث | `auto_client_acquisition/revenue_memory/retention.py` |
| دماغ العميل وحزمة السياق | `auto_client_acquisition/customer_brain/context_pack.py` |
| سجلّ الموافقات وحجب PII | `auto_client_acquisition/customer_data_plane/` |
| تقييم الجودة العربيّة | `evals/arabic_quality_eval.yaml` |

## 5. الحدود والقيود

- لا استرجاع عابر للمستأجرين تحت أي ظرف.
- الاسترجاع يحترم صلاحيّات المستخدم، لا صلاحيّات الفريق فقط.
- لا يُكتسح موقع خارجي ولا تُستخرج بيانات بلا أساس قانوني.
- المصادر القديمة تُعلَّم بحالة حداثة، ولا تُحذف بصمت.

روابط: `ingestion.md` · `hybrid_retrieval.md` · `citations.md` · `source_lineage.md` · `readiness.md`

---

# English

# Architecture — Knowledge Layer (Layer 4)

> This document describes the knowledge and memory architecture of the Dealix platform: how an organization's files, conversations, and decisions become retrievable memory, with a source behind every answer.

## 1. Purpose

Layer 4 makes Dealix "the company's memory." The goal is a system that knows customers, policies, files, operations, decisions, and context, and answers any important question with a citation to a real source. The governing rule is "no source, no answer."

This layer creates no new claims and guarantees no outcomes. It retrieves what is already recorded and binds it to its origin.

## 2. Components

- **Ingestion gateway:** Receives documents, conversations, and events; checks tenant ownership and permissions before indexing.
- **Chunking engine:** Splits documents into consistently sized semantic chunks while preserving structural boundaries.
- **Embedding service:** Converts chunks into vectors via `core/memory/embedding_service.py`.
- **Hybrid retrieval:** Combines vector semantic search with lexical keyword search.
- **Reranking:** Orders candidate results by actual relevance to the question.
- **Citations engine:** Binds every answer sentence to a source chunk via `auto_client_acquisition/knowledge_os/answer_with_citations.py`.
- **Source lineage:** Records the derivation chain from the original file, to the chunk, to the answer.
- **Memory stores:** Organizational, customer, workflow, policy, and executive memory.

## 3. Data flow

1. A document or conversation arrives at the ingestion gateway with a `tenant_id` and permission tags.
2. The gateway checks lawful basis and tenant ownership, then passes content to chunking.
3. The unit is split into chunks; each chunk gets an embedding vector and a content hash.
4. Chunks are stored with tenant scope, permission tags, and a freshness status.
5. On an incoming question, hybrid retrieval runs, scoped to the user's permissions and tenant.
6. Results are reranked, and the top chunks pass to the citations engine.
7. The answer is built only from chunks that have a source; absence of a source returns "insufficient evidence."
8. The full retrieval trace is recorded in source lineage.

## 4. Mapping to existing code

| Component | Repository path |
|---|---|
| Embedding and semantic search | `core/memory/embedding_service.py` |
| Answer with citations | `auto_client_acquisition/knowledge_os/answer_with_citations.py` |
| Knowledge policy eval | `auto_client_acquisition/knowledge_os/knowledge_eval.py` |
| "No source, no answer" rule | `auto_client_acquisition/governance_os/rules/no_source_no_answer.yaml` |
| Strategic memory (lesson files) | `auto_client_acquisition/intelligence_os/strategic_memory.py` |
| Revenue memory and event tracing | `auto_client_acquisition/revenue_memory/` |
| Event retention policy | `auto_client_acquisition/revenue_memory/retention.py` |
| Customer brain and context pack | `auto_client_acquisition/customer_brain/context_pack.py` |
| Consent registry and PII redaction | `auto_client_acquisition/customer_data_plane/` |
| Arabic quality eval | `evals/arabic_quality_eval.yaml` |

## 5. Boundaries and constraints

- No cross-tenant retrieval under any condition.
- Retrieval respects per-user permissions, not just team-level permissions.
- No external site is scraped and no data is extracted without lawful basis.
- Stale sources are flagged with a freshness status and are never silently deleted.

Links: `ingestion.md` · `hybrid_retrieval.md` · `citations.md` · `source_lineage.md` · `readiness.md`
