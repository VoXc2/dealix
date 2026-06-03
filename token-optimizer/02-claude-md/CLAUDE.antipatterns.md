# أمثلة على ما يجب تجنبه في CLAUDE.md

## ❌ أنتيباترن 1: تاريخ المشروع

```markdown
## Project History
In January 2024 we started with a monolith...
We migrated to microservices in March...
The CTO decided to use FastAPI because...
[200 سطر من التاريخ]
```

**المشكلة**: هذه معلومات تاريخية، لا تساعد Claude في مهمته الحالية.
**الحل**: احذفها. ضعها في `docs/HISTORY.md` إذا أردت.

---

## ❌ أنتيباترن 2: وثائق API كاملة

```markdown
## API Endpoints
POST /api/v1/users - creates user
  - body: {name: string, email: string, ...}
  - returns: {id: int, name: string, ...}
GET /api/v1/users/{id} - gets user
  - params: id (int)
  - returns: {id: int, ...}
[100 نقطة نهاية أخرى]
```

**المشكلة**: Claude يمكنه قراءة ملفات الـ routes مباشرة.
**الحل**: `- api/routes/: all FastAPI endpoints` — سطر واحد يكفي.

---

## ❌ أنتيباترن 3: أمثلة كود في CLAUDE.md

```markdown
## How to Create a New Endpoint
```python
from fastapi import APIRouter
router = APIRouter()

@router.get("/example")
async def example():
    return {"status": "ok"}
```
Always import APIRouter from fastapi...
[50 سطر من الشرح]
```

**المشكلة**: Claude يعرف FastAPI. هذا يُكلف 300+ توكن لا فائدة منها.
**الحل**: `3. All endpoints use APIRouter. See api/routes/ for examples.`

---

## ❌ أنتيباترن 4: محضر الاجتماعات

```markdown
## Recent Decisions
2024-03-15: Team decided to use Redis for caching
2024-03-20: CTO approved migration to PostgreSQL
2024-04-01: Decision to add Arabic support
```

**المشكلة**: هذه قرارات تاريخية لا تؤثر على كيفية كتابة الكود اليوم.
**الحل**: احذفها تماماً. ضعها في `docs/decisions/`.

---

## ❌ أنتيباترن 5: Schema قاعدة البيانات الكاملة

```markdown
## Database Schema
Table: users
  - id: integer primary key
  - name: varchar(255)
  - email: varchar(255) unique
  - created_at: timestamp
  ...
[300 سطر من الـ schema]
```

**المشكلة**: 300 سطر = 1,500+ توكن على **كل** رسالة.
**الحل**: ضعها في `skills/database.md` وحمّلها فقط عند مهام DB.

---

## المقارنة المباشرة

| الوضع | حجم CLAUDE.md | توكن/رسالة | 100 رسالة |
|-------|---------------|------------|-----------|
| قبل التحسين | 5,000 توكن | 5,000 | 500,000 توكن |
| بعد التحسين | 400 توكن | 400 | 40,000 توكن |
| **التوفير** | | **4,600 توكن** | **460,000 توكن** |
