# أوامر Pipe لتصفية المحتوى قبل إرساله لـ Claude

## المبدأ

بدلاً من إرسال الملف كاملاً، استخدم pipe لإرسال ما يحتاجه Claude فقط.

---

## Python Files

```bash
# أسماء الدوال والـ classes فقط
grep -n "^class\|^def\|^async def\|^    def\|^    async def" api/routes/clients.py

# فقط الـ imports
grep -n "^import\|^from" core/models/client.py

# فقط الـ endpoints (FastAPI)
grep -n "@router\.\|@app\." api/routes/clients.py

# دالة محددة فقط
sed -n '/^async def create_client/,/^async def\|^def\|^class/p' api/routes/clients.py | head -50

# فقط الأسطر التي تحتوي على TODO
grep -n "TODO\|FIXME\|HACK\|XXX" api/routes/clients.py
```

---

## Logs

```bash
# آخر 100 سطر
tail -100 logs/app.log

# أسطر الخطأ فقط
grep "ERROR\|CRITICAL\|Exception\|Traceback" logs/app.log | tail -50

# خطأ محدد
grep -n "ValueError\|KeyError" logs/app.log | tail -20

# لوج من وقت محدد
grep "2026-05-30" logs/app.log | tail -100
```

---

## JSON Files

```bash
# هيكل JSON بدون القيم
python3 -c "import json,sys; d=json.load(sys.stdin); print(list(d.keys()))" < config.json

# مفاتيح nested
python3 -c "
import json, sys
def print_keys(d, prefix=''):
    for k,v in d.items():
        print(f'{prefix}{k}: {type(v).__name__}')
        if isinstance(v, dict):
            print_keys(v, prefix + '  ')
json_str = sys.stdin.read()
print_keys(json.loads(json_str))
" < data/config.json
```

---

## Database Schema

```bash
# عرض هيكل جدول محدد فقط
psql $DATABASE_URL -c "\d clients"

# أسماء الجداول فقط
psql $DATABASE_URL -c "\dt"

# فقط الـ indexes
psql $DATABASE_URL -c "\di"
```

---

## Git

```bash
# الملفات المتغيرة فقط (بدون محتوى)
git diff --name-only

# تغييرات ملف محدد فقط
git diff HEAD api/routes/clients.py

# ملخص آخر 5 commits
git log --oneline -5

# من غيّر سطراً محدداً
git blame -L 45,60 api/routes/clients.py
```

---

## هيكل المشروع

```bash
# هيكل 3 مستويات
tree -L 3 --gitignore -I "__pycache__|node_modules|.git|*.pyc"

# ملفات Python فقط
find . -name "*.py" | grep -v "__pycache__\|.venv\|.git" | sort

# ملفات أكبر من 100 سطر
find . -name "*.py" -exec awk 'END{if(NR>100)print NR, FILENAME}' {} \; | sort -rn | head -20
```

---

## Tests

```bash
# أسماء test functions فقط
grep -n "def test_" tests/test_clients.py

# فشل آخر تشغيل فقط
pytest tests/ --tb=no -q 2>&1 | tail -20

# coverage summary فقط
pytest tests/ --cov=api --cov-report=term-missing 2>&1 | grep -E "TOTAL|MISS"
```
