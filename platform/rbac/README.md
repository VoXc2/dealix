# RBAC

## الأدوار المفعّلة للحلقة الحالية
- `viewer`
- `sales_rep`
- `sales_manager`
- `tenant_admin`

## القاعدة
تشغيل workflow المبيعات يتطلب:
- `workflow:run`
- `agent:run:sales_agent`

## نقطة ربط
- مصفوفة الصلاحيات في `auto_client_acquisition/foundation_core/enterprise_loop.py`
