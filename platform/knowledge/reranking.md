# العربية

# إعادة الترتيب — طبقة المعرفة (الطبقة الرابعة)

> كيف تُرتَّب المقاطع المرشّحة حسب الصلة الفعليّة بالسؤال قبل بناء الإجابة.

## 1. الغرض

إعادة الترتيب هي المرحلة التي تلي الاسترجاع الهجين. الاسترجاع يُحضِر مجموعة مرشّحة واسعة؛ إعادة الترتيب تختار منها الأعلى صلة فعليّة بالسؤال، فتقلّل الضوضاء التي تصل إلى محرّك الاستشهادات.

## 2. لماذا مرحلة منفصلة

- الاسترجاع الأوّلي مُحسَّن للسرعة والاستدعاء الواسع.
- إعادة الترتيب مُحسَّنة للدقّة على عدد صغير من المرشّحين.
- فصل المرحلتين يرفع دقّة الإجابة دون إبطاء الاسترجاع الأوّلي.

## 3. إشارات الترتيب

تُرتَّب المقاطع حسب مزيج من:

- درجة التشابه الدلالي من خدمة التضمين.
- قوّة التطابق المعجمي مع كلمات السؤال.
- حالة الحداثة: المقطع `fresh` يُفضَّل على `stale` عند تساوي الصلة.
- نوع المصدر: السياسة المعتمدة تُفضَّل على المسوّدة عند تساوي الصلة.

## 4. حدّ القطع

- يُمرَّر للاستشهادات عدد محدود من المقاطع الأعلى ترتيبًا فقط.
- إذا كانت درجة كل المرشّحين دون حدّ الثقة، تُرجِع الطبقة «أدلّة غير كافية» بدل إجابة ضعيفة.
- لا يُرفع مقطع `stale` فوق حدّ القطع لمجرّد ندرة البدائل دون إعلام بحالته.

## 5. الحوكمة

- إعادة الترتيب لا تُنشئ محتوى ولا تُعيد صياغته؛ تُرتّب فقط.
- يُسجَّل ترتيب المقاطع النهائي في تتبّع نسب المصدر، فيمكن مراجعة لماذا اختير مقطع.
- لا تُرتَّب مقاطع من خارج نطاق المستأجر أو خارج صلاحيّة المستخدم؛ هذه مُرشَّحة قبل الوصول لهذه المرحلة.

روابط: `hybrid_retrieval.md` · `citations.md` · `source_lineage.md`

---

# English

# Reranking — Knowledge Layer (Layer 4)

> How candidate chunks are ordered by actual relevance to the question before the answer is built.

## 1. Purpose

Reranking is the stage that follows hybrid retrieval. Retrieval brings a broad candidate set; reranking selects from it the chunks with the highest actual relevance to the question, reducing the noise that reaches the citations engine.

## 2. Why a separate stage

- Initial retrieval is optimized for speed and broad recall.
- Reranking is optimized for precision over a small candidate set.
- Separating the two raises answer precision without slowing initial retrieval.

## 3. Ranking signals

Chunks are ordered by a combination of:

- The semantic similarity score from the embedding service.
- The strength of lexical match against the question's terms.
- Freshness status: a `fresh` chunk is preferred over a `stale` one at equal relevance.
- Source type: an approved policy is preferred over a draft at equal relevance.

## 4. Cutoff threshold

- Only a limited number of top-ranked chunks pass to citations.
- If every candidate scores below the confidence threshold, the layer returns "insufficient evidence" rather than a weak answer.
- A `stale` chunk is not lifted above the cutoff merely due to a scarcity of alternatives without surfacing its status.

## 5. Governance

- Reranking creates no content and does not rephrase it; it only orders.
- The final chunk order is recorded in source lineage, so the reason a chunk was chosen can be reviewed.
- Chunks outside the tenant scope or the user's permission are not reranked; they are filtered before this stage.

Links: `hybrid_retrieval.md` · `citations.md` · `source_lineage.md`
