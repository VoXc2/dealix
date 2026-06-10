# Dealix — OWASP API Security Action Plan

خطة تنفيذية لتحويل مخاطر OWASP API Security Top 10 إلى gates قابلة للفحص داخل Dealix.

## الهدف

حماية API وواجهات التشغيل من المخاطر الأعلى أثرًا: صلاحيات خاطئة، كسر الهوية، تسريب بيانات، استهلاك زائد للموارد، SSRF، وسوء إعدادات الأمان.

## 1) Authorization & object access

| Gate | المطلوب | Evidence |
|---|---|---|
| Tenant isolation | كل endpoint يقرأ tenant/customer من auth context وليس من body فقط | اختبارات unit/integration |
| Admin boundary | `/api/v1/admin/*` يتطلب `ADMIN_API_KEYS` أو RBAC لاحقًا | middleware test |
| Object ownership | لا يمكن الوصول إلى مورد بغير المالك | negative tests |

## 2) Authentication

- لا يتم تشغيل الإنتاج بدون `API_KEYS` و `ADMIN_API_KEYS`.
- لا يتم قبول placeholder secrets في production.
- أي JWT أو session لاحقًا يجب أن يحتوي expiry وissuer وaudience.

## 3) Resource consumption

- استخدم rate limiting لكل surfaces الحساسة.
- اجعل healthcheck سريعًا ولا يعتمد على خدمات خارجية إلا في deep mode.
- أي endpoint يستخدم LLM أو enrichment يجب أن يكون له timeout/retry/budget.

## 4) Sensitive data exposure

- ممنوع secrets داخل `NEXT_PUBLIC_*`.
- ممنوع إرجاع provider tokens أو raw customer payloads في public endpoints.
- logs يجب أن تستخدم redaction للـ keys والبريد وأرقام الهاتف عند الحاجة.

## 5) SSRF and external fetches

- أي crawler/enrichment يجب أن يمنع private IP ranges.
- لا تقبل URLs داخلية من المستخدم بدون validation.
- ضع allowlist للمزودين المعروفين عند الإمكان.

## 6) Security configuration

- Security headers للواجهات.
- CORS محدود بالدومينات الفعلية.
- Railway healthcheck `/healthz` لكل خدمة.
- API deep health متاح للمراقبة، وليس بديلًا عن liveness.

## 7) Inventory and documentation

- `docs/architecture/API_MAP.md` هو خريطة الأسطح.
- أي endpoint جديد يجب أن يضيف ownership، auth class، وrisk class.
- أي public claim يجب أن يمر عبر no-overclaim register.

## 8) CI gates المطلوبة

```bash
python scripts/check_env_contract.py
python scripts/verify_railway_surfaces.py
python scripts/verify_founder_operating_system.py
python scripts/check_openapi_contract.py
pytest -q
```

## 9) تنفيذ قريب المدى

- [ ] إضافة negative authorization tests لأهم endpoints التجارية.
- [ ] إضافة audit log coverage لاستخدام admin routes.
- [ ] إضافة SSRF guard مركزي لأي URL fetch.
- [ ] إضافة API risk-class map لكل router.
- [ ] إضافة security evidence snapshot مع كل release.
