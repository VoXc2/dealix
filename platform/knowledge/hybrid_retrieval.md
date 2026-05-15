# العربية

# الاسترجاع الهجين — طبقة المعرفة (الطبقة الرابعة)

> كيف يجمع Dealix بين البحث الدلالي والبحث المعجمي، ويحترم صلاحيّات المستخدم، ويمنع الاسترجاع العابر للمستأجرين.

## 1. الغرض

الاسترجاع الهجين يجد المقاطع الأكثر صلة بسؤال المستخدم. يدمج طريقتين: البحث الدلالي بالمتّجهات الذي يلتقط المعنى، والبحث المعجمي بالكلمات المفتاحيّة الذي يلتقط المصطلحات الدقيقة وأسماء الأعلام والأرقام.

## 2. لماذا الهجين

- البحث الدلالي وحده قد يفوّت تطابقًا حرفيًّا مهمًّا (رقم عقد، اسم منتج).
- البحث المعجمي وحده يفوّت إعادة الصياغة والمرادفات.
- الدمج يرفع الاستدعاء (recall) دون خفض الدقّة (precision) بشكل ملموس.

## 3. تدفّق الاسترجاع

1. يصل السؤال مع هويّة المستخدم و `tenant_id`.
2. يُجرى البحث الدلالي عبر `core/memory/embedding_service.py` (دوال `search_accounts` و `search_conversations`)، مقيّدًا بـ `tenant_id`.
3. يُجرى البحث المعجمي على نفس المجموعة المقيّدة بالمستأجر.
4. تُدمَج قائمتا المرشّحين وتُزال التكرارات.
5. **ترشيح الصلاحيّات:** تُحذف أي مقاطع لا يملك المستخدم صلاحيّة عليها، بناءً على وسوم الصلاحيّة لا على المستأجر فقط.
6. تُمرَّر القائمة المرشّحة إلى إعادة الترتيب.

## 4. الاسترجاع المدرك للصلاحيّات

- الترشيح يتم على مستوى المستخدم: لا يكفي أن يكون المقطع داخل المستأجر، بل يجب أن يملك المستخدم صلاحيّة قراءته.
- مقطع بلا وسم صلاحيّة واضح يُعامَل كمقيَّد، لا كمفتوح.
- لا يُكشف في النتائج وجود مقاطع محجوبة عن المستخدم.

## 5. منع الاسترجاع العابر للمستأجرين

- كل استعلام يحمل `tenant_id` إلزاميًّا؛ استعلام بلا مستأجر يُرفض.
- لا تُدمَج نتائج من مستأجرين مختلفين في أي حالة.
- يُسجَّل كل استرجاع كحدث قابل للتدقيق مع المستأجر والمستخدم.

## 6. الحوكمة

- إذا لم تُرجِع المرحلة أي مقطع، تُرجِع طبقة المعرفة «أدلّة غير كافية» وفق `auto_client_acquisition/governance_os/rules/no_source_no_answer.yaml`.
- لا يُولِّد الاسترجاع محتوى؛ يُرتّب ما هو مُسجَّل فقط.

روابط: `embeddings.md` · `reranking.md` · `citations.md` · `readiness.md`

---

# English

# Hybrid Retrieval — Knowledge Layer (Layer 4)

> How Dealix combines semantic and lexical search, respects user permissions, and prevents cross-tenant retrieval.

## 1. Purpose

Hybrid retrieval finds the chunks most relevant to a user's question. It combines two methods: vector semantic search that captures meaning, and lexical keyword search that captures exact terms, proper nouns, and numbers.

## 2. Why hybrid

- Semantic search alone can miss an important literal match (a contract number, a product name).
- Lexical search alone misses paraphrasing and synonyms.
- The combination raises recall without a material drop in precision.

## 3. Retrieval flow

1. The question arrives with the user identity and a `tenant_id`.
2. Semantic search runs via `core/memory/embedding_service.py` (`search_accounts` and `search_conversations`), scoped by `tenant_id`.
3. Lexical search runs over the same tenant-scoped set.
4. The two candidate lists are merged and deduplicated.
5. **Permission filtering:** Any chunks the user lacks permission for are dropped, based on permission tags, not just the tenant.
6. The candidate list passes to reranking.

## 4. Permission-aware retrieval

- Filtering happens at the user level: it is not enough for a chunk to be inside the tenant; the user must hold permission to read it.
- A chunk without a clear permission tag is treated as restricted, not open.
- Results do not reveal the existence of chunks hidden from the user.

## 5. Preventing cross-tenant retrieval

- Every query carries a mandatory `tenant_id`; a query without a tenant is rejected.
- Results from different tenants are never merged, under any condition.
- Every retrieval is recorded as an auditable event with the tenant and user.

## 6. Governance

- If the stage returns no chunk, the knowledge layer returns "insufficient evidence" per `auto_client_acquisition/governance_os/rules/no_source_no_answer.yaml`.
- Retrieval generates no content; it only orders what is recorded.

Links: `embeddings.md` · `reranking.md` · `citations.md` · `readiness.md`
