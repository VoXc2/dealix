# أوامر Git لإعطاء Claude معلومات دقيقة ومضغوطة

## بدلاً من "اقرأ المشروع وافهمه"

### إعطاء خريطة التغييرات الأخيرة
```bash
# آخر 10 commits مع الملفات المتغيرة
git log --oneline -10 --stat | head -50

# ملخص التغييرات منذ main
git diff main --stat

# الملفات المتغيرة فقط (بدون محتوى)
git diff main --name-only
```

### إعطاء Claude diff محدد
```bash
# تغييرات ملف واحد فقط
git diff HEAD api/routes/clients.py

# تغييرات PR محددة
git diff origin/main...HEAD -- api/

# diff بأسلوب موجز
git diff --stat origin/main...HEAD
```

### استعراض المشاركين
```bash
# من عمل على ملف معين
git log --oneline --follow api/routes/clients.py | head -10

# آخر من غيّر سطراً معيناً
git blame -L 45,60 api/routes/clients.py
```

---

## إعداد git لتسريع العمل مع Claude

### alias مفيدة للإعداد
```bash
# أضف هذه aliases لـ ~/.gitconfig
git config --global alias.sum "log --oneline -10"
git config --global alias.changes "diff --stat origin/main...HEAD"
git config --global alias.files "diff --name-only origin/main...HEAD"
```

### استخدام مع Claude
```
# عوضاً عن "ما الملفات المتغيرة في هذا الـ PR؟"
# أعطِ Claude:
git diff --name-only origin/main...HEAD

# عوضاً عن "اشرح لي التغييرات"
# أعطِ Claude:
git diff origin/main...HEAD --stat
```

---

## تقليل ضجيج git log

```bash
# log نظيف بدون merge commits
git log --oneline --no-merges -15

# log مع التفاصيل المهمة فقط
git log --format="%h %as %s" -10
# المخرجات: abc1234 2026-05-30 Add client export endpoint
```

---

## إعداد .gitattributes لتحسين Diffs

```gitattributes
# .gitattributes — يُحسّن قراءة Claude للـ diffs

# ملفات generated تعامَل كـ binary (لا تظهر في diff)
*.lock binary
package-lock.json binary
pnpm-lock.yaml binary

# تعريف languages للملفات
*.py linguist-language=Python
*.ts linguist-language=TypeScript
```

---

## PR Review Workflow مع Claude

```bash
# 1. احصل على قائمة الملفات المتغيرة
git diff origin/main...HEAD --name-only

# 2. أعطِ Claude:
"راجع هذه الـ PR. الملفات المتغيرة:
[الملفات من الأمر السابق]

التغييرات:
$(git diff origin/main...HEAD --stat)

ركّز على: الأمان، الأداء، العلاقات بين الملفات.
لا شرح للكود الجيد. مشاكل فقط."
```
