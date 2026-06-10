# 01 — .claudeignore: استبعاد الملفات غير الضرورية

## لماذا هذا الأهم؟

بدون `.claudeignore`، قد يقرأ Claude آلاف الملفات المُولَّدة تلقائياً أثناء الاستكشاف،
مما يُحرق توكنز على محتوى لا قيمة له. مثال حقيقي:

- **قبل**: 11,000 توكن عند بدء الجلسة
- **بعد**: 800 توكن فقط ← توفير **93%**

## كيف يعمل؟

نفس صياغة `.gitignore` تماماً. Claude يحترم هذا الملف ولا يقرأ أي ملف مذكور فيه.

## الملفات في هذا المجلد

| الملف | الوصف |
|-------|--------|
| `.claudeignore.dealix` | ملف جاهز مخصص لمشروع Dealix |
| `.claudeignore.python` | قالب لمشاريع Python عامة |
| `.claudeignore.node` | قالب لمشاريع Node.js/React |
| `.claudeignore.fullstack` | قالب للمشاريع الكاملة (Python + Node) |
| `patterns-explained.md` | شرح كل نمط وسبب استبعاده |
| `savings-calculator.md` | حساب التوفير المتوقع لكل نمط |

## التطبيق الفوري

```bash
# لمشروع Dealix (Python + FastAPI + React)
cp token-optimizer/01-claudeignore/.claudeignore.dealix .claudeignore

# تحقق أن الملف شُغِّل
cat .claudeignore
```

## مصادر التوفير

| النمط | حجم البيانات النموذجية | التوكنز المُهدرة |
|-------|----------------------|-----------------|
| `node_modules/` | 200-500 MB | 100,000+ |
| `__pycache__/` | 10-50 MB | 10,000+ |
| `dist/ + build/` | 50-200 MB | 50,000+ |
| `*.lock` | 500KB-5MB | 5,000+ |
| `coverage/` | 10-100 MB | 20,000+ |
| `*.log` | 1-500 MB | 50,000+ |
