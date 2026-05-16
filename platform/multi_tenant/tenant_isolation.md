# Tenant Isolation Contract

## مبدأ أساسي

لا يوجد أي كيان تشغيلي في Dealix بدون `tenant_id`.

## نطاق الإلزام

يجب أن يحمل `tenant_id`:

- workflow run
- agent context
- retrieval queries
- memory writes
- audit logs
- external actions

## ممنوعات (Explicit Deny)

- Shared memory بين عملاء مختلفين.
- Shared retrieval index بدون فصل صلاحيات.
- أي endpoint يسمح بالوصول لبيانات tenant آخر.

## ضوابط التنفيذ

1. **Data partitioning**
   - كل جدول تشغيلي يتضمن `tenant_id`.
   - يفضل row-level security عند الإمكان.

2. **Application guards**
   - لا يتم تنفيذ query أو command قبل حقن `tenant_id`.
   - أي absence لـ `tenant_id` = fail-fast.

3. **Retrieval guards**
   - filters إلزامية بالـ `tenant_id`.
   - permission-aware memory filtering قبل إرجاع النتائج.

4. **Auditability**
   - كل عملية وصول تسجل `tenant_id`, `actor_id`, `resource`, `action`.

## اختبارات القبول

- محاولة قراءة lead من tenant آخر يجب أن تفشل.
- محاولة retrieval خارج نطاق tenant يجب أن تعيد empty/denied.
- أي run بدون tenant context يجب أن يرفض قبل التنفيذ.
