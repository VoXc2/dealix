# 11 — Git Hygiene: نظافة Git وGitHub

## لماذا Git يؤثر على التوكنز؟

عندما يستكشف Claude المشروع، يمكنه قراءة ملفات `git log` و `git diff` الطويلة.
ضخامة الـ repository تعني:
- بحث أطول = توكنز أكثر
- ملفات مُتتبَّعة غير ضرورية تزيد الضجيج
- PR diffs ضخمة تُصعّب المراجعة

## الملفات في هذا المجلد

| الملف | الوصف |
|-------|--------|
| `gitignore-for-claude.md` | أنماط .gitignore تُفيد Claude أيضاً |
| `git-commands-for-claude.md` | أوامر git لإعطاء Claude معلومات دقيقة |
| `pr-workflow.md` | سير عمل PR يقلل توكنز المراجعة |
| `commit-messages.md` | رسائل commit واضحة توفر رسائل توضيحية |

## أهم التقنيات

### 1. .gitignore = .claudeignore (غالباً)
معظم ما يُستبعد من git يجب استبعاده من Claude أيضاً.
انسخ .claudeignore بناءً على .gitignore.

### 2. إعطاء Claude diff محدد بدلاً من طلب قراءة الملفات
```bash
# ❌ مُكلف
"اقرأ الملفات واخبرني بالتغييرات"

# ✅ فعّال
git diff HEAD~1 api/routes/clients.py  # ثم أعطه للـ Claude
```

### 3. تلخيص git log
```bash
# إعطاء Claude ملخص commits محدد
git log --oneline -10
```

### 4. PR صغيرة ومحددة
PR صغيرة = review أسرع = توكنز أقل في المراجعة.

## قاعدة الـ PR المثالية

```
PR = تغيير واحد منطقي
PR < 300 سطر متغيّر
PR = ملف tests مرتبط
PR = رسالة واضحة تشرح "لماذا"
```
