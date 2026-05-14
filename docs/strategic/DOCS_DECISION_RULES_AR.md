# قواعد قرار الوثائق — Dealix

## لماذا توجد هذه القواعد؟

لأن Dealix لا تحتاج **المزيد من الملفات**؛ تحتاج **أصولًا** قابلة للبيع والتسليم والحوكمة والترخيص، مُفعّلة عبر [EXTERNAL_PACK_REGISTRY_AR.md](EXTERNAL_PACK_REGISTRY_AR.md) و [data/docs_asset_usage_log.json](../../data/docs_asset_usage_log.json).

## إنشاء وثيقة جديدة

يُسمح فقط إذا كانت الوثيقة تخدم **واحدًا** من:

- **sell** — عرض أو إغلاق  
- **deliver** — تسليم Sprint / Retainer  
- **govern** — حوكمة، سياسة، سجل canonical  
- **prove** — Proof، أدلة، QA  
- **train** — تمكين مشغّل أو أكاديمية مقيدة  
- **license** — ترخيص IP أو شريك  
- **fund** — استثمار / use of funds / diligence  
- **archive** — أرشفة، queue، توثيق مصير  

**السؤال الحاكم:** *Will this change help us sell, deliver, govern, prove, train, license, fund, or archive?* — إذا لا، **لا تُنشَأ**.

## تحديث وثيقة

يُسمح إذا كان التحديث:

- يجعلها **canonical** أكثر  
- يقلل الالتباس والتكرار  
- يربطها **بعرض أو اختبار أو API**  
- يجعلها **أأمن خارجيًا** ([DOCS_PUBLICATION_BOUNDARY_AR.md](DOCS_PUBLICATION_BOUNDARY_AR.md))  
- يحسّن **التسليم أو البيع**  

## منع الوثيقة

لا تُنشأ وثيقة إذا:

- تكرّر ملفًا **canonical** بلا قيمة مضافة  
- **لا جمهور** واضح لها  
- **لا مالك** (انظر [HOLDING_VALUE_REGISTRY_AR.md](HOLDING_VALUE_REGISTRY_AR.md))  
- **لا تصنيف نشر** لها عند أي استخدام خارجي محتمل  
- **لا ترتبط** بعرض أو تشغيل أو ثقة  

## أرشفة

- تبدأ بـ **LEGACY** أو **DEPRECATED** في السياسة والسجل، لا بنقل المجلد فورًا.  
- لا نقل قبل مراجعة الروابط والاختبارات ([ARCHIVE_REVIEW_QUEUE_AR.md](ARCHIVE_REVIEW_QUEUE_AR.md)).  

## النشر الخارجي

ممنوع إرسال أي وثيقة خارجية بدون:

- **Publication boundary** مسجّل  
- **حزمة خارجية معتمدة** أو موافقة المؤسس ([EXTERNAL_PACK_REGISTRY_AR.md](EXTERNAL_PACK_REGISTRY_AR.md))  
- **عدم وجود أسرار**  
- **عدم وجود ادّعاءات تنظيمية مبالغ فيها**  

بعد الإرسال: أضف عنصرًا في `data/docs_asset_usage_log.json` → `entries` (*No usage, no commercial evidence*).

## الحزم المعتمدة للإرسال

استخدم فقط الحزم المعرفة في [EXTERNAL_PACK_REGISTRY_AR.md](EXTERNAL_PACK_REGISTRY_AR.md).
