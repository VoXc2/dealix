# Identity

## الهدف
إلزام كل تشغيل بهوية واضحة:
- `user_id`
- `user_role`
- `tenant_id`

## مبدأ
لا توجد عمليات مجهولة داخل workflow المؤسسي.

## نقطة ربط
- `EnterpriseLoopRequest` داخل `auto_client_acquisition/foundation_core/enterprise_loop.py`
