# قالب Task Brief — تحديد المهمة بدقة

## لماذا Brief مهم؟

"برومبت واحد محدد يُغني عن 5 رسائل توضيحية"
كل رسالة توضيحية = توكنز إضافية + وقت ضائع.

## القالب

```markdown
## Context
[السياق الضروري فقط — جملة أو اثنتان]

## Goal
[ماذا يجب أن يحدث؟ — جملة واحدة محددة]

## Files
- `path/to/file.py`: [لماذا هذا الملف؟]
- `path/to/other.py`: [لماذا هذا الملف؟]

## Constraints
- [قيد تقني 1]
- [قيد تقني 2]

## Done When
- [ ] [معيار 1 — قابل للقياس]
- [ ] [معيار 2 — قابل للقياس]

## Style
No explanations. Code only. Minimal output.
```

---

## مثال: إضافة Validation

**قبل (مُكلف):**
```
أضف validation للإيميل في نموذج إنشاء المستخدم
```
← يُنتج 5 رسائل توضيحية على الأقل

**بعد (فعّال):**
```markdown
## Context
نموذج إنشاء المستخدم في `api/schemas/user.py` لا يتحقق من صحة الإيميل.

## Goal
أضف Pydantic validator للإيميل يرفض الصيغ غير الصحيحة.

## Files
- `api/schemas/user.py`: Pydantic schema للمستخدم (السطر 15-40)

## Constraints
- Pydantic v2 syntax (model_validator, field_validator)
- رسالة الخطأ بالعربية والإنجليزية

## Done When
- [ ] validator يرفض "notanemail"
- [ ] validator يقبل "user@domain.com"
- [ ] رسالة خطأ موجودة بالعربية

## Style
No explanations. Code only.
```

---

## مثال: إصلاح Bug

```markdown
## Context
`GET /api/v1/deals/{id}` يُعيد 500 عندما deal_id غير موجود.

## Goal
أعيد 404 مع رسالة واضحة بدلاً من 500.

## Files
- `api/routes/deals.py`: دالة get_deal (السطر 45-67)

## Constraints
- استخدم HTTPException من fastapi
- رسالة الخطأ: `{"detail": "Deal not found", "code": "DEAL_NOT_FOUND"}`

## Done When
- [ ] GET /api/v1/deals/99999 يُعيد 404 (ليس 500)
- [ ] response body يحتوي على "code": "DEAL_NOT_FOUND"

## Style
No explanations. Only the changed function.
```
