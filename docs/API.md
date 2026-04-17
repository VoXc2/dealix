# Dealix — توثيق REST API

> **الإصدار:** v1.0.0 · **آخر تحديث:** 2025  
> **الروابط ذات الصلة:** [البنية المعمارية](../ARCHITECTURE.md) · [دليل النشر](./DEPLOYMENT.md)  
> **OpenAPI Interactive Docs:** `GET /docs` (Swagger UI) · `GET /redoc` (ReDoc)

---

## نظرة عامة

يُعدّ Dealix API واجهة REST كاملة تتيح للتطبيقات الأمامية والتكاملات الخارجية التفاعل مع منصة المبيعات. يلتزم التصميم بمبادئ:
- **REST** — موارد واضحة، أفعال HTTP قياسية
- **RFC 7807** — صيغة موحّدة لأخطاء `Problem Details`
- **Cursor-based Pagination** — للأداء الثابت مع قواعد البيانات الكبيرة
- **Idempotency** — آمن التكرار على جميع العمليات المُعدِّلة
- **Versioning** — URI-based (`/api/v1/`, `/api/v2/`)

**Base URL:**
```
Production:  https://api.dealix.sa/api/v1
Staging:     https://api.staging.dealix.sa/api/v1
Development: http://localhost:8000/api/v1
```

---

## المصادقة — Authentication

### نموذج JWT

يستخدم Dealix API مصادقة JWT (JSON Web Tokens) بنموذج access/refresh token:

```
Access Token:  صالح 15 دقيقة
Refresh Token: صالح 7 أيام (single-use مع rotation)
```

**تضمين الـ Token في الطلبات:**
```http
Authorization: Bearer <access_token>
```

**حمولة JWT (Payload):**
```json
{
  "sub": "user_uuid",
  "tenant_id": "tenant_uuid",
  "role": "admin | agent | viewer",
  "exp": 1735000000,
  "iat": 1734999100
}
```

### POST /api/v1/auth/login

تسجيل الدخول والحصول على tokens.

**الطلب:**
```http
POST /api/v1/auth/login
Content-Type: application/json
```
```json
{
  "email": "user@company.sa",
  "password": "••••••••"
}
```

**الاستجابة الناجحة (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900
}
```

**استجابة الخطأ (401 Unauthorized):**
```json
{
  "type": "https://dealix.sa/errors/authentication-failed",
  "title": "فشل المصادقة",
  "status": 401,
  "detail": "البريد الإلكتروني أو كلمة المرور غير صحيحة",
  "instance": "/api/v1/auth/login"
}
```

### POST /api/v1/auth/refresh

تجديد access token باستخدام refresh token.

**الطلب:**
```http
POST /api/v1/auth/refresh
Content-Type: application/json
```
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**الاستجابة الناجحة (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900
}
```

> **ملاحظة:** الـ refresh token القديم يُبطَل فور إصدار الجديد (token rotation).

---

## تحديد المعدل — Rate Limiting

| الفئة | الحد |
|-------|------|
| طلبات عامة | 100 طلب / دقيقة لكل tenant |
| نقاط Auth | 10 طلبات / دقيقة لكل IP |
| إرسال Outreach | 50 رسالة / دقيقة لكل tenant |
| استدعاءات LLM | 20 طلب / دقيقة لكل tenant |

**Headers المُعادة:**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1735000060
Retry-After: 23   (عند تجاوز الحد — 429 Too Many Requests)
```

---

## Idempotency

جميع نقاط الطرفية المُعدِّلة (POST، PUT، PATCH) **تشترط** مفتاح idempotency.

**Header المطلوب:**
```http
X-Idempotency-Key: <uuid-v4>
```

**السلوك:**
- الطلب الأول: يُنفَّذ ويُحفَظ النتيجة لمدة **24 ساعة**
- الطلبات اللاحقة بنفس المفتاح: يُعاد نفس الرد دون إعادة التنفيذ
- مفتاح مختلف = طلب جديد مستقل

**مثال:**
```http
POST /api/v1/leads
X-Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
```

إذا فُقد الاتصال وأعاد العميل الطلب بنفس المفتاح، لن يُنشأ الرصاص مرتين.

---

## صيغة الأخطاء — RFC 7807 Problem Details

جميع الأخطاء تتبع [RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807):

```json
{
  "type": "https://dealix.sa/errors/<error-code>",
  "title": "وصف مختصر للخطأ بالعربية",
  "status": 422,
  "detail": "شرح تفصيلي للمشكلة وكيفية حلها",
  "instance": "/api/v1/leads",
  "errors": [
    {
      "field": "company_name",
      "message": "اسم الشركة مطلوب"
    }
  ]
}
```

**رموز HTTP المستخدمة:**

| الرمز | المعنى |
|-------|--------|
| 200 | نجاح |
| 201 | إنشاء ناجح |
| 202 | مقبول للمعالجة (Async) |
| 400 | طلب غير صالح |
| 401 | غير مصادَق |
| 403 | غير مصرَّح (tenant mismatch) |
| 404 | المورد غير موجود |
| 409 | تعارض (idempotency أو تكرار) |
| 422 | بيانات غير صالحة |
| 429 | تجاوز حد الطلبات |
| 500 | خطأ داخلي في الخادم |
| 503 | الخدمة غير متاحة مؤقتاً |

---

## نقاط الطرفية الرئيسية — Endpoints

### الرصاص — Leads

#### GET /api/v1/leads

استرجاع قائمة الرصاص للـ tenant الحالي.

```http
GET /api/v1/leads?status=new&limit=20&cursor=<cursor_token>
Authorization: Bearer <token>
```

**Query Parameters:**

| المعامل | النوع | الوصف |
|---------|-------|-------|
| `status` | string | `new`, `qualified`, `contacted`, `closed`, `lost` |
| `limit` | integer | عدد النتائج (افتراضي: 20، أقصى: 100) |
| `cursor` | string | مؤشر الصفحة التالية (cursor-based pagination) |
| `search` | string | بحث نصي في الاسم والشركة |
| `score_min` | integer | أدنى درجة تأهيل (0-100) |

**الاستجابة (200 OK):**
```json
{
  "data": [
    {
      "id": "lead_uuid",
      "company_name": "شركة المثال للتقنية",
      "contact_name": "محمد عبدالله",
      "contact_phone": "+966501234567",
      "status": "new",
      "qualification_score": null,
      "created_at": "2025-01-15T10:30:00Z",
      "tenant_id": "tenant_uuid"
    }
  ],
  "pagination": {
    "next_cursor": "eyJpZCI6InVzZXJfMTIzIn0=",
    "has_more": true,
    "total_count": 247
  }
}
```

#### POST /api/v1/leads

إنشاء رصاص جديد.

```http
POST /api/v1/leads
Authorization: Bearer <token>
X-Idempotency-Key: <uuid-v4>
Content-Type: application/json
```

```json
{
  "company_name": "شركة الأفق للتجارة",
  "contact_name": "سارة المالكي",
  "contact_phone": "+966509876543",
  "contact_email": "sara@ufuq.sa",
  "industry": "retail",
  "company_size": "50-200",
  "notes": "تبحث عن حلول CRM متكاملة"
}
```

**الاستجابة (201 Created):**
```json
{
  "id": "lead_uuid",
  "status": "new",
  "created_at": "2025-01-15T11:00:00Z"
}
```

#### POST /api/v1/leads/{id}/qualify

تشغيل Qualifier Agent على رصاص محدد.

```http
POST /api/v1/leads/{id}/qualify
Authorization: Bearer <token>
X-Idempotency-Key: <uuid-v4>
```

**الاستجابة (202 Accepted — معالجة غير متزامنة):**
```json
{
  "task_id": "task_uuid",
  "status": "queued",
  "estimated_seconds": 15,
  "poll_url": "/api/v1/tasks/task_uuid"
}
```

**نتيجة المهمة (عند polling):**
```json
{
  "task_id": "task_uuid",
  "status": "completed",
  "result": {
    "qualification_score": 78,
    "qualification_tier": "B",
    "reasoning": "الشركة تستوفي معايير الحجم والقطاع. نقطة ضعف: عدم وضوح الميزانية.",
    "recommended_action": "تواصل أولي عبر واتساب",
    "next_agent": "outreach"
  }
}
```

### التواصل — Outreach

#### POST /api/v1/outreach/send

إرسال رسالة تواصل عبر WhatsApp.

```http
POST /api/v1/outreach/send
Authorization: Bearer <token>
X-Idempotency-Key: <uuid-v4>
Content-Type: application/json
```

```json
{
  "lead_id": "lead_uuid",
  "channel": "whatsapp",
  "template_id": "initial_contact_v2",
  "personalization": {
    "contact_name": "أبو عبدالله",
    "company_name": "شركة الأفق",
    "pain_point": "إدارة العملاء"
  }
}
```

**الاستجابة (202 Accepted):**
```json
{
  "message_id": "msg_uuid",
  "task_id": "task_uuid",
  "status": "queued",
  "compliance_check": "pending"
}
```

> **ملاحظة:** كل رسالة تمر عبر Compliance Agent قبل الإرسال الفعلي. إذا رفضت Compliance Agent، يُعاد خطأ `403` مع سبب مفصّل.

### التحليلات — Analytics

#### GET /api/v1/analytics/funnel

استرجاع مقاييس قمع المبيعات.

```http
GET /api/v1/analytics/funnel?period=last_30_days
Authorization: Bearer <token>
```

**الاستجابة (200 OK):**
```json
{
  "period": "last_30_days",
  "generated_at": "2025-01-15T12:00:00Z",
  "funnel": {
    "total_leads": 150,
    "qualified": 89,
    "contacted": 67,
    "interested": 34,
    "closed_won": 12,
    "closed_lost": 22
  },
  "conversion_rates": {
    "lead_to_qualified": "59.3%",
    "qualified_to_contacted": "75.3%",
    "contacted_to_closed_won": "17.9%"
  },
  "cache_ttl_seconds": 900
}
```

> **تحذير Truth Registry:** مقاييس الأداء المعروضة هنا تعكس بيانات قاعدة البيانات الحالية. أي ادّعاء بمستوى تحويل محدد يجب أن يستند إلى 30 يوماً من البيانات الفعلية.

---

## Webhooks

### WhatsApp Inbound

استقبال الرسائل الواردة من WhatsApp Business API.

```
POST /api/v1/webhooks/whatsapp
```

**الحمولة (يُرسلها Meta):**
```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "id": "whatsapp_business_account_id",
    "changes": [{
      "value": {
        "messaging_product": "whatsapp",
        "contacts": [{"wa_id": "966501234567"}],
        "messages": [{
          "id": "wamid.xxx",
          "from": "966501234567",
          "timestamp": "1735000000",
          "type": "text",
          "text": {"body": "نعم، أنا مهتم"}
        }]
      }
    }]
  }]
}
```

**التحقق (Verification Challenge):**
```
GET /api/v1/webhooks/whatsapp?hub.mode=subscribe&hub.verify_token=<token>&hub.challenge=<challenge>
```

### ZATCA Callbacks

استقبال ردود ZATCA على الفواتير الإلكترونية.

```
POST /api/v1/webhooks/zatca
X-ZATCA-Signature: <hmac-signature>
```

---

## Pagination — الترقيم

يستخدم Dealix API **Cursor-based Pagination** بدلاً من الترقيم بالصفحات (offset/page) لضمان الأداء الثابت.

**طلب الصفحة الأولى:**
```http
GET /api/v1/leads?limit=20
```

**طلب الصفحة التالية:**
```http
GET /api/v1/leads?limit=20&cursor=eyJpZCI6ImxlYWRfdXVpZCJ9
```

**هيكل الاستجابة:**
```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6ImxlYWRfdXVpZCJ9",
    "has_more": true,
    "total_count": 247
  }
}
```

> **ملاحظة:** `total_count` تقريبي لأسباب الأداء في الجداول الكبيرة.

---

## إستراتيجية الإصدار — Versioning

يتبع Dealix API الإصدار عبر URI Path:

```
/api/v1/  ← الإصدار الحالي المستقر
/api/v2/  ← التالي (عند الإفصاح)
```

**سياسة التغييرات:**
- **تغييرات متوافقة** (Backward-compatible): إضافة حقول، endpoints جديدة — بدون رفع الإصدار
- **تغييرات كاسرة** (Breaking changes): حذف حقول، تغيير schemas — يستلزم إصداراً جديداً
- فترة دعم الإصدار القديم بعد إطلاق الجديد: **6 أشهر** مع إشعار مسبق

---

## المهام غير المتزامنة — Async Tasks

بعض العمليات (تأهيل الرصاص، إرسال رسائل) تُنفَّذ بصورة غير متزامنة عبر Celery.

**نمط Polling:**
```http
# 1. إرسال الطلب → 202 Accepted
POST /api/v1/leads/{id}/qualify
→ { "task_id": "task_uuid", "poll_url": "/api/v1/tasks/task_uuid" }

# 2. الاستعلام عن الحالة
GET /api/v1/tasks/task_uuid
→ { "status": "pending | running | completed | failed" }

# 3. عند الاكتمال
→ { "status": "completed", "result": {...} }
```

**حالات المهام:**

| الحالة | المعنى |
|--------|--------|
| `queued` | في الانتظار |
| `running` | قيد التنفيذ |
| `completed` | اكتملت بنجاح |
| `failed` | فشلت مع رسالة خطأ |
| `retrying` | تُعاد المحاولة تلقائياً |

---

## الروابط والمراجع

- [البنية المعمارية](../ARCHITECTURE.md) — وصف الوكلاء والطبقات
- [دليل النشر](./DEPLOYMENT.md) — إعداد البيئات
- [RFC 7807 — Problem Details](https://datatracker.ietf.org/doc/html/rfc7807)
- [WhatsApp Business API Docs](https://developers.facebook.com/docs/whatsapp)
- Swagger UI التفاعلي: `/docs`
- ReDoc: `/redoc`
