# شرح كل Hook وتأثيره على التوكنز

## SessionStart Hooks

### حقن Branch الحالي
```json
{
  "type": "command",
  "command": "git branch --show-current"
}
```
**الفائدة**: Claude يعرف الـ branch بدون أن تسأله.
**التوكنز المُوفرة**: 50-200 توكن (رسائل التوضيح)

---

## PreToolUse Hooks

### تحذير قبل قراءة ملف كبير
```json
{
  "matcher": {"tool": "Read", "fileSize": ">50000"},
  "type": "warn",
  "message": "File is large. Read specific line ranges."
}
```
**الفائدة**: يُنبّه Claude لقراءة نطاق محدد بدل الملف كله.
**التوكنز المُوفرة**: 5,000-50,000 توكن لكل قراءة ملف ضخم

### تحذير قبل find واسع النطاق
```json
{
  "matcher": {"tool": "Bash", "pattern": "find .* -name"},
  "type": "inject",
  "message": "Limit find to 50 results maximum."
}
```
**الفائدة**: يمنع find من إرجاع آلاف النتائج.
**التوكنز المُوفرة**: 2,000-20,000 توكن

---

## PostToolUse Hooks

### قطع مخرجات bash الطويلة
```json
{
  "matcher": {"tool": "Bash"},
  "type": "pipe",
  "command": "head -200"
}
```
**الفائدة**: أي bash command لا يُعيد أكثر من 200 سطر.
**التوكنز المُوفرة**: 60-90% على الأوامر الصاخبة (مثل `docker logs`, `pip list`, `npm install`)

### تحديد حجم أقصى بالحروف
```json
{
  "matcher": {"outputSize": ">10000"},
  "type": "truncate",
  "max_chars": 10000
}
```
**الفائدة**: ضمان عدم تجاوز مخرجات أي أداة 10,000 حرف.

---

## أمثلة توفير حقيقية

| الأمر | بدون Hook | مع Hook | التوفير |
|-------|-----------|---------|---------|
| `docker logs app` | 50,000 توكن | 1,000 توكن | 98% |
| `pip list` | 3,000 توكن | 200 توكن | 93% |
| `npm install` | 20,000 توكن | 500 توكن | 97% |
| `find . -name *.py` | 5,000 توكن | 250 توكن | 95% |
| `git log --oneline` | 10,000 توكن | 500 توكن | 95% |

---

## كيفية التفعيل

أضف محتوى `hooks.optimized.json` إلى `.claude/settings.json`:

```bash
# إذا لم يكن .claude/settings.json موجوداً
cp token-optimizer/07-hooks/hooks.optimized.json .claude/settings.json

# إذا كان موجوداً، أدمج الـ hooks يدوياً
```
