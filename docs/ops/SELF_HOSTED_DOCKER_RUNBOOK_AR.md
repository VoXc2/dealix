# Dealix — Self-hosted Docker Runbook

## هل أقدر أشغل Dealix على نفس السيرفر؟

نعم، تقدر تشغله على VPS أو dedicated server باستخدام Docker Compose. الريبو الآن يحتوي stack إنتاجي يشغل:

- API
- frontend
- apps/web اختياري
- Postgres
- PgBouncer
- Redis
- Caddy reverse proxy مع TLS

## متى يكون مناسب؟

مناسب إذا تريد:

- تحكم كامل بالسيرفر.
- تكلفة ثابتة أقل من منصات managed.
- تطوير ونشر من أي مكان باستخدام SSH/GitHub keys.
- تشغيل قاعدة البيانات والواجهة والـ API على نفس الجهاز كبداية.

غير مناسب إذا:

- لا تريد إدارة backups/security updates.
- لا تريد تحمل مسؤولية scaling/monitoring.
- تحتاج high availability من اليوم الأول.

## أقل مواصفات مقترحة

### بداية حقيقية

- 4 vCPU
- 8 GB RAM
- 80 GB SSD
- Ubuntu 22.04/24.04

### ضغط أعلى

- 8 vCPU
- 16 GB RAM
- 160 GB SSD
- backups خارج السيرفر

### مهم

إذا زاد الضغط، افصل قاعدة البيانات إلى managed Postgres أو سيرفر مستقل. API والواجهات أسهل في التوسعة من قاعدة البيانات.

## الملفات المضافة

- `docker-compose.prod.yml`
- `.env.prod.example`
- `ops/caddy/Caddyfile`
- `scripts/server_bootstrap_ubuntu.sh`
- `scripts/server_deploy.sh`
- `scripts/server_backup.sh`
- `scripts/server_healthcheck.sh`

## أول إعداد للسيرفر

على Ubuntu server جديد:

```bash
sudo bash scripts/server_bootstrap_ubuntu.sh
```

بعدها:

```bash
sudo -iu dealix
cd /srv/dealix
git clone git@github.com:VoXc2/dealix.git .
cp .env.prod.example .env.prod
nano .env.prod
```

عبئ القيم الحقيقية، خصوصًا:

```text
APP_SECRET_KEY
JWT_SECRET_KEY
API_KEYS
ADMIN_API_KEYS
POSTGRES_PASSWORD
REDIS_PASSWORD
DEALIX_DOMAIN
DEALIX_API_DOMAIN
NEXT_PUBLIC_API_URL
NEXT_PUBLIC_SITE_URL
```

## النشر

```bash
bash scripts/server_deploy.sh
```

## فحص الصحة

```bash
bash scripts/server_healthcheck.sh
```

فحص خارجي:

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/ready
curl -fsS https://dealix.me/healthz
```

## النسخ الاحتياطي

```bash
bash scripts/server_backup.sh
```

يفضل وضع cron:

```cron
0 2 * * * cd /srv/dealix && bash scripts/server_backup.sh >> /srv/dealix/logs/backup.log 2>&1
```

## التطوير من أي مكان

### طريقة آمنة

1. استخدم GitHub SSH key على جهازك.
2. اشتغل محليًا على branch.
3. push إلى GitHub.
4. SSH للسيرفر.
5. pull ثم deploy.

```bash
git pull --ff-only
bash scripts/server_deploy.sh
```

### لا تعمل

- لا تفتح Docker socket للإنترنت.
- لا ترفع `.env.prod` إلى GitHub.
- لا تشغل editor كـ root داخل السيرفر إلا للضرورة.

## تحمل الضغط

الـ stack يستخدم PgBouncer لتقليل ضغط اتصالات Postgres، وRedis مع memory policy، وCaddy كـ reverse proxy. لكن الضغط الحقيقي يعتمد على:

- عدد الطلبات.
- endpoints التي تستخدم LLM أو enrichment.
- حجم قاعدة البيانات.
- عدد العمال workers.
- سرعة مزودي API الخارجيين.

## التوسعة

### المرحلة 1

كل شيء على نفس السيرفر.

### المرحلة 2

افصل Postgres إلى managed database.

### المرحلة 3

شغل أكثر من API container خلف Caddy أو load balancer.

### المرحلة 4

انقل jobs/queues إلى workers منفصلين.

## أوامر مفيدة

```bash
docker compose --env-file .env.prod -f docker-compose.prod.yml ps
docker compose --env-file .env.prod -f docker-compose.prod.yml logs -f api
docker compose --env-file .env.prod -f docker-compose.prod.yml restart api
docker stats
```

## قرار المؤسس

ابدأ بسيرفر واحد قوي، لكن لا تعتمد عليه وحده بدون backups. إذا بدأ عندك عملاء مدفوعين وtraffic ثابت، افصل قاعدة البيانات وأضف monitoring خارجي.
