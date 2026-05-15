# العربية

# التقطيع — طبقة المعرفة (الطبقة الرابعة)

> كيف تُقسَّم المستندات والمحادثات إلى مقاطع دلاليّة قابلة للفهرسة، مع حفظ الحدود البنيويّة ونسب المصدر.

## 1. الغرض

محرّك التقطيع يحوّل وحدة المحتوى المستوعَبة إلى مقاطع متّسقة الحجم تصلح للتضمين والاسترجاع. الهدف أن يكون كل مقطع كبيرًا بما يكفي ليحمل معنى مكتملًا، وصغيرًا بما يكفي ليُسترجَع بدقّة، ومرتبطًا دائمًا بالملف الأصلي وموضعه فيه.

## 2. مبادئ التقطيع

- **احترام البنية:** لا يُقطَع المقطع عبر منتصف جدول أو بند تعاقدي أو فقرة سياسة.
- **حجم متّسق:** المقطع المستهدف بين 200 و 500 كلمة، مع تداخل محدود بين المقاطع المتجاورة لحفظ السياق.
- **حدود دلاليّة:** يُفضَّل القطع عند العناوين والفقرات وعناصر القوائم.
- **اللغة العربيّة:** يحترم المقطع اتجاه النص واكتمال الجملة العربيّة؛ تُقيَّم الجودة عبر `evals/arabic_quality_eval.yaml`.

## 3. بيانات المقطع المرافقة

كل مقطع يُختم بـ:

- `chunk_id` فريد و `tenant_id` ثابت.
- مرجع للملف الأصلي وموضع المقطع داخله (صفحة أو فقرة أو إزاحة).
- بصمة محتوى (hash) لكشف التغيير.
- وسوم الصلاحيّة الموروثة من المصدر.
- حالة الحداثة الموروثة (`fresh` / `aging` / `stale`).

## 4. تحديث المقاطع دون كسر النظام

عند تعديل المصدر تُعاد معالجة المقاطع المتأثّرة فقط: تُقارَن بصمات المحتوى، فتُحدَّث المقاطع المتغيّرة وتبقى البقيّة. المعرّفات السابقة تبقى صالحة للتتبّع التاريخي، فلا تنكسر الاستشهادات القديمة.

## 5. الحوكمة

- لا يُنشأ مقطع بلا مرجع لملفه الأصلي؛ مقطع بلا نسب يُرفض.
- وسوم الصلاحيّة وحالة الحداثة تُورَّث من المصدر، ولا تُخفَّض يدويًّا دون قيد تدقيق.
- إعادة التقطيع عمليّة قابلة للتدقيق ومسجّلة في تتبّع نسب المصدر.

روابط: `ingestion.md` · `embeddings.md` · `source_lineage.md`

---

# English

# Chunking — Knowledge Layer (Layer 4)

> How documents and conversations are split into indexable semantic chunks while preserving structural boundaries and source lineage.

## 1. Purpose

The chunking engine turns an ingested content unit into consistently sized chunks suitable for embedding and retrieval. The goal: each chunk is large enough to carry a complete meaning, small enough to be retrieved precisely, and always bound to its origin file and position within it.

## 2. Chunking principles

- **Respect structure:** A chunk is never cut through the middle of a table, a contract clause, or a policy paragraph.
- **Consistent size:** Target chunk size is 200–500 words, with limited overlap between adjacent chunks to preserve context.
- **Semantic boundaries:** Cuts are preferred at headings, paragraphs, and list items.
- **Arabic text:** Chunks respect text direction and Arabic sentence completeness; quality is assessed via `evals/arabic_quality_eval.yaml`.

## 3. Chunk-accompanying metadata

Every chunk is stamped with:

- A unique `chunk_id` and an immutable `tenant_id`.
- A reference to the origin file and the chunk's position within it (page, paragraph, or offset).
- A content hash for change detection.
- Permission tags inherited from the source.
- Inherited freshness status (`fresh` / `aging` / `stale`).

## 4. Updating chunks without breaking the system

When a source is edited, only the affected chunks are reprocessed: content hashes are compared, changed chunks are updated, and the rest remain. Prior identifiers stay valid for historical tracing, so old citations do not break.

## 5. Governance

- No chunk is created without a reference to its origin file; a chunk without lineage is rejected.
- Permission tags and freshness status are inherited from the source and are not manually downgraded without an audit entry.
- Re-chunking is an auditable operation recorded in source lineage.

Links: `ingestion.md` · `embeddings.md` · `source_lineage.md`
