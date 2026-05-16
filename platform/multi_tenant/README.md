# Multi-Tenant System

## قاعدة إلزامية
كل طلب تشغيلي يجب أن يحمل `tenant_id`.

## ضوابط
- لا يوجد تنفيذ بدون tenant context.
- لا يوجد مشاركة بيانات بين tenants.
- كل أثر تشغيلي (audit/metrics) مربوط بـ `tenant_id`.

## نقطة ربط
- `auto_client_acquisition/foundation_core/enterprise_loop.py` (request contract)
