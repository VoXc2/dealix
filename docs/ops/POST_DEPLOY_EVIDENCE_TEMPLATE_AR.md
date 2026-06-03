# Dealix — قالب إثبات ما بعد النشر

استخدم هذا القالب بعد كل Redeploy أو Hotfix حتى يكون القرار مبنيًا على دليل.

## 1) معلومات النشر

- التاريخ والوقت:
- الشخص المنفذ:
- الخدمات المتأثرة:
  - [ ] API
  - [ ] frontend
  - [ ] apps/web
- آخر commit منشور:
- رابط Railway deployment:

## 2) فحوصات الصحة

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/ready
curl -fsS 'https://api.dealix.me/healthz?deep=1'
curl -fsS https://dealix.me/healthz
```

ضع النتائج هنا:

```text

```

## 3) فحوصات الريبو

```bash
python scripts/verify_railway_surfaces.py
python scripts/founder_launch_final_check.py
```

ضع النتائج هنا:

```text

```

## 4) فحوصات CI

- CI:
- Security:
- Production Smoke:
- Railway build logs:
- Railway deploy logs:

## 5) القرار

- [ ] جاهز للإنتاج
- [ ] جاهز مع ملاحظة غير حرجة
- [ ] غير جاهز — يحتاج إصلاح

## 6) الملاحظات والمتابعة

- Root cause إن وجد:
- الإجراء التالي:
- Issue/PR للمتابعة:
