# دورة حياة أصل وثائقي في Dealix

**الغرض:** كل وثيقة تمر بحالة واضحة من الإنشاء إلى الإيقاف أو الأرشفة، بما يتوافق مع [DOCS_ARCHIVE_POLICY_AR.md](DOCS_ARCHIVE_POLICY_AR.md).

## مراحل الدورة

```text
Draft → Active → Canonical | Supporting
  → Partner-safe | Client-facing | Investor-safe (عند الحاجة)
  → Reviewed (cadence)
  → Updated | Deprecated
  → Archived
```

| المرحلة | المعنى |
|---------|--------|
| **Draft** | فكرة أو مسودة؛ غير معتمدة للعروض الخارجية. |
| **Active** | مستخدمة داخليًا أو في تسليم محدود. |
| **Canonical** | المصدر المعتمد للمجال؛ مسجّل في [DOCS_CANONICAL_REGISTRY_AR.md](DOCS_CANONICAL_REGISTRY_AR.md). |
| **Supporting** | تكمّل canonical ولا تُروَّج كمرجع أول. |
| **External-safe** | وسم فرعي: وثيقة رُاجعت للاستخدام مع شريك/عميل/مستثمر حسب [DOCS_PUBLICATION_BOUNDARY_AR.md](DOCS_PUBLICATION_BOUNDARY_AR.md). |
| **Reviewed** | مرت بمراجعة وفق [DOCS_REVIEW_CADENCE_AR.md](DOCS_REVIEW_CADENCE_AR.md). |
| **Deprecated** | لا تُستخدم في حركة تجارية جديدة؛ يُفضّل إشارة للبديل. |
| **Archived** | للحفظ التاريخي؛ لا عروض جديدة تعتمد عليها. |

## انتقالات مقبولة

- من **Draft** إلى **Active** بقرار مالك الوثيقة (أو المؤسس للأصول الحاكمة).
- من **Active** إلى **Canonical** بإدخال صف في السجل المعتمد وربط من المحور.
- **Deprecated** يتبعه إما تحديث أو **Archived** دون حذف إلزامي من المستودع في هذه المرحلة.

## المالك والمسؤولية

كل أصل **CANONICAL** يجب أن يكون له **مالك** (فريق أو دور) مسجّل في تقرير المراجعة الشهرية حتى يُضاف حقل رسمي لاحقًا.
