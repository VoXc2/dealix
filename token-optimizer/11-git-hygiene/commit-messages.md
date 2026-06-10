# رسائل Commit الواضحة: توفير رسائل توضيحية لاحقاً

## لماذا رسائل Commit تؤثر على التوكنز؟

رسائل commit غير واضحة تجعل Claude يطرح أسئلة:
- "ما هذا الـ commit؟"
- "لماذا تغيّر هذا؟"
- "ما علاقة هذا التغيير بمهمتنا؟"

كل سؤال = توكنز إضافية.

---

## صيغة Commit المثالية

```
[type]: [وصف موجز باللغة الإنجليزية]

[body اختياري - لماذا؟ ليس ماذا؟]
```

### أنواع (type)
| النوع | المعنى |
|-------|--------|
| `feat` | ميزة جديدة |
| `fix` | إصلاح bug |
| `refactor` | إعادة هيكلة بدون تغيير وظيفي |
| `test` | إضافة/تعديل اختبارات |
| `docs` | تحديث توثيق |
| `chore` | تحديثات صيانة |
| `perf` | تحسين أداء |
| `security` | إصلاح ثغرة أمنية |

---

## أمثلة

```bash
# ❌ غير مفيد
git commit -m "fix bug"
git commit -m "update clients"
git commit -m "changes"

# ✅ مفيد
git commit -m "fix: return 404 instead of 500 when client not found"
git commit -m "feat: add CSV export endpoint for clients list"
git commit -m "refactor: extract client scoring logic to ClientScorer class"
git commit -m "perf: add index on clients.sector reduces query time 80%"
git commit -m "security: validate file extension before upload to prevent LFI"
```

---

## Commit Template لـ Dealix

```bash
# إعداد template
cat > ~/.gitmessage << 'EOF'
# [feat|fix|refactor|test|docs|chore|perf|security]: [وصف]
# 
# لماذا (ليس ماذا):
#
# Breaking changes:
# Related issue:
EOF

git config --global commit.template ~/.gitmessage
```

---

## قاعدة الـ PR الواحدة

```
كل PR = commit واحد أو commits مترابطة تحل مشكلة واحدة

❌ PR تحتوي:
- feat: add export
- fix: bug in auth
- refactor: update models

✅ PR تحتوي:
- feat: add client CSV export endpoint
- test: add export endpoint tests
- docs: document export endpoint in API spec
```

هذا يجعل مراجعة Claude للـ PR أسرع وأدق بتوكنز أقل.
