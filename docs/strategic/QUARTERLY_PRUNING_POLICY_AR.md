# سياسة التشذيب الربع سنوية (Quarterly Pruning)

**الغرض:** الحد من الضوضاء بمرور الوقت **دون** كسر الروابط أو حذف متهور.

## القاعدة — أول 90 يومًا

- **لا حذف** جماعي.  
- **لا نقل** جماعي لمجلدات `docs/`.  
- **لا إعادة ترقيم**.  
- **تصنيف فقط** (LEGACY / SUPPORTING / DEPRECATED) عبر [ARCHIVE_REVIEW_QUEUE_AR.md](ARCHIVE_REVIEW_QUEUE_AR.md).

## بعد 90 يومًا

يُسمح **بالنقل** المحدود فقط إذا:

1. الملف أو المجلد مصنَّف **LEGACY** أو **DEPRECATED** صراحةً.  
2. **لا** يعتمد عليه [HOLDING_DOCS_HUB_AR.md](HOLDING_DOCS_HUB_AR.md) أو [DOCS_CANONICAL_REGISTRY_AR.md](DOCS_CANONICAL_REGISTRY_AR.md) كمصدر معتمد.  
3. **لا توجد روابط مكسورة** (فحص يدوي أو سكربت لاحقًا).  
4. **الاختبارات PASS** (`pytest` بما فيها حوكمة الوثائق).  
5. لقطة [**docs_top_level_snapshot.json**](_generated/docs_top_level_snapshot.json) مُحدَّثة.

## الحذف

**Delete almost never** — الحذف الفعلي قرار نادر وبعد توثيق وسجل.

مرجع: [DOCS_ARCHIVE_POLICY_AR.md](DOCS_ARCHIVE_POLICY_AR.md).
