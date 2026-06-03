# نظام البنية والموثوقية (Infra & Reliability OS)

## المكدّس الفعلي
- الواجهة: React 19 + Vite + Tailwind/shadcn.
- الخلفية: Hono + tRPC (`api/`)، مصادقة Kimi OAuth + JWT (`jose`).
- البيانات: Drizzle ORM + MySQL (`db/`)، تخزين S3 (`@aws-sdk`).
- البناء: `vite build` + `esbuild api/boot.ts`؛ التشغيل: `node dist/boot.js`.

## مبادئ الموثوقية
- بيئات منفصلة (محلي/تجريبي/إنتاج) — انظر `ENVIRONMENT_POLICY_AR.md`.
- لا نشر إنتاج من فرع وكيل؛ اعتماد بشري (`DEPLOYMENT_APPROVAL_POLICY_AR.md`).
- أسرار خارج المستودع (`SECRETS_MANAGEMENT_POLICY_AR.md`).
- نسخ احتياطي + استرجاع (`BACKUP_AND_RECOVERY_AR.md`).
- كشف انحراف (`DRIFT_DETECTION_AR.md`) و SLO/SLA (`SLO_SLA_POLICY_AR.md`).

## نقاط الصحة (مقترحة)
- `/health` للخلفية (TBD — غير مطبّق بعد).
- فحص اتصال قاعدة البيانات عند الإقلاع.

## الحالة
🟡 مسودة تشغيلية. لا تغييرات إنتاج في هذا الإصدار. البنود المفتوحة في
`reports/infra/INFRA_GAP_AUDIT.md`.
