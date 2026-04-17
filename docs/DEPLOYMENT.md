# Dealix — دليل النشر والتشغيل

> **الإصدار:** 1.0.0 · **آخر تحديث:** 2025  
> **الروابط ذات الصلة:** [البنية المعمارية](../ARCHITECTURE.md) · [API Reference](./API.md)

---

## المتطلبات الأساسية

### أدوات مطلوبة

| الأداة | الإصدار الأدنى | الغرض |
|--------|---------------|-------|
| Docker | 24.0+ | تشغيل الحاويات |
| Docker Compose | v2.20+ | التطوير المحلي |
| kubectl | 1.28+ | الإنتاج (Kubernetes) |
| Helm | 3.12+ | نشر Kubernetes |
| Git | 2.40+ | إدارة الكود |
| Python | 3.12+ | تشغيل scripts محلياً |

### متطلبات الموارد

| البيئة | CPU | RAM | Disk |
|--------|-----|-----|------|
| Development | 4 cores | 8 GB | 20 GB |
| Staging | 4 cores | 16 GB | 50 GB |
| Production | 8+ cores | 32+ GB | 200+ GB |

---

## البيئات

```
development  →  docker-compose على الجهاز المحلي
staging      →  Docker Swarm + GitHub Actions
production   →  Kubernetes (Helm charts) على cloud provider
```

---

## التطوير المحلي — Development

### الإعداد الأول

```bash
# 1. استنساخ المستودع
git clone https://github.com/your-org/dealix.git
cd dealix

# 2. نسخ ملف البيئة
cp .env.example .env.local
# عدّل القيم في .env.local (أنظر قسم متغيرات البيئة)

# 3. بناء وتشغيل الخدمات
docker compose up --build

# 4. تنفيذ هجرات قاعدة البيانات
docker compose exec backend alembic upgrade head

# 5. إنشاء بيانات أولية (seed data)
docker compose exec backend python scripts/seed_dev_data.py
```

### الخدمات المُشغَّلة محلياً

| الخدمة | Port | URL |
|--------|------|-----|
| Frontend (Next.js) | 3000 | http://localhost:3000 |
| Backend (FastAPI) | 8000 | http://localhost:8000 |
| API Docs (Swagger) | 8000 | http://localhost:8000/docs |
| PostgreSQL | 5432 | localhost:5432 |
| Redis | 6379 | localhost:6379 |
| Celery Flower | 5555 | http://localhost:5555 |
| Mailhog (Dev email) | 8025 | http://localhost:8025 |

### أوامر Docker Compose المفيدة

```bash
# تشغيل الخدمات في الخلفية
docker compose up -d

# عرض السجلات
docker compose logs -f backend
docker compose logs -f celery-worker

# إعادة تشغيل خدمة محددة
docker compose restart backend

# تشغيل الاختبارات
docker compose exec backend pytest tests/ -v

# إيقاف وحذف الحاويات
docker compose down

# إيقاف وحذف كل شيء (بما في ذلك volumes)
docker compose down -v
```

---

## متغيرات البيئة

> الرجوع إلى ملف `.env.example` في جذر المستودع للقائمة الكاملة.

### المتغيرات الجوهرية

```bash
# ─── Application ───────────────────────────────────────
APP_ENV=development          # development | staging | production
APP_SECRET_KEY=<random-64-char-string>
DEBUG=true                   # false في production دائماً

# ─── Database ──────────────────────────────────────────
DATABASE_URL=postgresql+asyncpg://dealix:password@postgres:5432/dealix_db
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# ─── Redis ─────────────────────────────────────────────
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

# ─── LLM Providers ─────────────────────────────────────
GROQ_API_KEY=gsk_xxxxxxxxxxxx
GROQ_MODEL=llama-3.3-70b-versatile
OPENAI_API_KEY=sk-xxxxxxxxxxxx
OPENAI_FALLBACK_MODEL=gpt-4o-mini
LLM_TIMEOUT_SECONDS=30
LLM_MAX_RETRIES=3

# ─── WhatsApp Business API ──────────────────────────────
WHATSAPP_ACCESS_TOKEN=EAAxxxx
WHATSAPP_PHONE_NUMBER_ID=1234567890
WHATSAPP_VERIFY_TOKEN=<random-string>
WHATSAPP_WEBHOOK_SECRET=<random-string>

# ─── ZATCA ─────────────────────────────────────────────
ZATCA_ENVIRONMENT=sandbox    # sandbox | production
ZATCA_CERTIFICATE=<base64-cert>
ZATCA_PRIVATE_KEY=<base64-key>

# ─── Auth ──────────────────────────────────────────────
JWT_SECRET_KEY=<random-64-char-string>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# ─── Monitoring ────────────────────────────────────────
SENTRY_DSN=https://xxx@sentry.io/project_id
```

> **تحذير أمني:** لا تُضف `.env.local` أو أي ملف يحتوي على مفاتيح حقيقية إلى Git. ملف `.gitignore` يستثنيهما افتراضياً.

---

## Staging — بيئة الاختبار

### Docker Swarm

```bash
# تهيئة Swarm (مرة واحدة)
docker swarm init

# نشر الـ stack
docker stack deploy -c docker-compose.staging.yml dealix-staging

# عرض الخدمات
docker stack services dealix-staging

# تحديث خدمة محددة
docker service update --image dealix/backend:staging dealix-staging_backend
```

### GitHub Actions — CI/CD Pipeline

عند الدفع إلى فرع `staging`:
1. تشغيل الاختبارات (`pytest` + `jest`)
2. بناء Docker images
3. رفع الصور إلى Container Registry
4. نشر تلقائي عبر `docker stack deploy`
5. تشغيل smoke tests بعد النشر
6. إشعار Slack عند النجاح أو الفشل

---

## الإنتاج — Production (Kubernetes)

### هيكل Helm Chart (مبدئي)

```
helm/dealix/
├── Chart.yaml
├── values.yaml           ← القيم الافتراضية
├── values.production.yaml ← قيم الإنتاج
├── templates/
│   ├── deployment-backend.yaml
│   ├── deployment-frontend.yaml
│   ├── deployment-celery.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml          ← Horizontal Pod Autoscaler
│   └── pdb.yaml          ← Pod Disruption Budget
```

### النشر على Kubernetes

```bash
# إضافة مستودع Helm (مبدئي)
helm repo add dealix https://charts.dealix.sa

# نشر لأول مرة
helm install dealix ./helm/dealix \
  -f helm/dealix/values.production.yaml \
  --namespace dealix-prod \
  --create-namespace

# تحديث نشر موجود
helm upgrade dealix ./helm/dealix \
  -f helm/dealix/values.production.yaml \
  --namespace dealix-prod

# عرض حالة النشر
kubectl get pods -n dealix-prod
kubectl get services -n dealix-prod
```

### Zero-Downtime Deployments

تُنفَّذ التحديثات بـ **Rolling Update**:
```yaml
# في deployment.yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0      # لا توقف مطلقاً
    maxSurge: 1            # نسخة إضافية أثناء التحديث
```

```bash
# التحقق من تقدم Rolling Update
kubectl rollout status deployment/dealix-backend -n dealix-prod
```

---

## هجرة قاعدة البيانات — Alembic

```bash
# إنشاء هجرة جديدة
alembic revision --autogenerate -m "add_qualification_score_to_leads"

# تطبيق كل الهجرات المعلّقة
alembic upgrade head

# التراجع عن آخر هجرة
alembic downgrade -1

# عرض تاريخ الهجرات
alembic history --verbose

# في الإنتاج (عبر Kubernetes Job)
kubectl apply -f k8s/migrations-job.yaml
```

> **قاعدة:** كل migration يجب أن يمتلك `downgrade()` قابلاً للتنفيذ الآمن.

---

## Rollback Strategy

### Rollback تلقائي (Kubernetes)

```bash
# التراجع إلى الإصدار السابق
kubectl rollout undo deployment/dealix-backend -n dealix-prod

# التراجع إلى إصدار محدد
kubectl rollout undo deployment/dealix-backend \
  --to-revision=3 -n dealix-prod

# عرض تاريخ الإصدارات
kubectl rollout history deployment/dealix-backend -n dealix-prod
```

### Rollback قاعدة البيانات

```bash
# التراجع عن آخر هجرة
alembic downgrade -1

# التراجع إلى revision محدد
alembic downgrade abc123def456
```

> **تحذير:** Rollback قاعدة البيانات يجب اختباره في Staging أولاً. بعض الهجرات لا يمكن التراجع عنها بأمان (مثل حذف أعمدة).

---

## المراقبة — Monitoring

### Prometheus + Grafana

```bash
# نشر Prometheus Stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace

# الوصول لـ Grafana (محلياً)
kubectl port-forward svc/kube-prometheus-stack-grafana 3001:80 -n monitoring
# http://localhost:3001 | admin / admin
```

**لوحات Grafana المُعدَّة:**
- معدل طلبات API (requests/sec)
- زمن استجابة المئيل 95 و99
- معدل نجاح / فشل مهام Celery
- استخدام نماذج LLM (tokens/min)
- حالة قواعد البيانات (connections, query time)
- حالة WhatsApp API (messages sent/received)

### Sentry — تتبع الأخطاء

```python
# في backend/main.py
import sentry_sdk
sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=0.1,  # 10% في الإنتاج
    environment=settings.APP_ENV,
)
```

---

## السجلات — Logs

### صيغة JSON المنظّمة

جميع السجلات بصيغة JSON للتحليل الآلي:

```json
{
  "timestamp": "2025-01-15T10:30:00.123Z",
  "level": "INFO",
  "service": "dealix-backend",
  "tenant_id": "tenant_uuid",
  "user_id": "user_uuid",
  "request_id": "req_uuid",
  "message": "Lead qualification completed",
  "lead_id": "lead_uuid",
  "score": 78,
  "duration_ms": 2340
}
```

### ELK Stack (Elasticsearch + Logstash + Kibana)

```bash
# تشغيل ELK في Staging
docker compose -f docker-compose.elk.yml up -d

# Kibana: http://localhost:5601
# Index pattern: dealix-logs-*
```

**مستويات السجلات:**
- `DEBUG`: تفاصيل التطوير (لا تُفعَّل في الإنتاج)
- `INFO`: أحداث عادية (طلبات API، مهام مكتملة)
- `WARNING`: حالات غير متوقعة لا تؤثر على العمل
- `ERROR`: أخطاء تحتاج تدخلاً
- `CRITICAL`: أخطاء حرجة تُوقف الخدمة

---

## النسخ الاحتياطي — Backup

### النسخ اليومي لـ PostgreSQL

```bash
# نص pg_dump (يعمل عبر CronJob في Kubernetes)
#!/bin/bash
BACKUP_FILE="dealix-db-$(date +%Y%m%d-%H%M%S).sql.gz"
pg_dump $DATABASE_URL | gzip > /tmp/$BACKUP_FILE

# رفع إلى S3-compatible storage (MinIO / AWS S3 / Cloudflare R2)
aws s3 cp /tmp/$BACKUP_FILE s3://dealix-backups/postgres/$BACKUP_FILE \
  --endpoint-url $S3_ENDPOINT

# حذف النسخ الأقدم من 30 يوماً
aws s3 ls s3://dealix-backups/postgres/ | \
  awk '{print $4}' | \
  xargs -I{} sh -c 'aws s3 rm s3://dealix-backups/postgres/{}'
```

**جدول النسخ الاحتياطي:**
- يومياً: نسخة كاملة محفوظة 30 يوماً
- أسبوعياً: نسخة محفوظة 12 أسبوعاً
- شهرياً: نسخة محفوظة 12 شهراً

### اختبار الاستعادة

```bash
# استعادة تجريبية (في بيئة منفصلة)
gunzip -c dealix-db-20250115-020000.sql.gz | psql $TEST_DATABASE_URL
```

> **قاعدة:** يُختبر الاستعادة شهرياً في بيئة staging للتحقق من سلامة النسخ.

---

## إدارة الأسرار — Secrets Management

### خيار 1: Kubernetes Secrets (بيئة بسيطة)

```bash
# إنشاء Secret
kubectl create secret generic dealix-secrets \
  --from-literal=GROQ_API_KEY=gsk_xxx \
  --from-literal=OPENAI_API_KEY=sk_xxx \
  -n dealix-prod

# عرض الـ secrets (بدون قيم)
kubectl get secrets -n dealix-prod
```

### خيار 2: HashiCorp Vault (موصى به للإنتاج)

```bash
# تهيئة Vault مع Kubernetes auth
vault auth enable kubernetes
vault write auth/kubernetes/config \
  kubernetes_host="https://kubernetes.default.svc"

# إنشاء policy للخدمة
vault policy write dealix-backend ./vault/policies/backend.hcl

# استرجاع السر في الكود
import hvac
client = hvac.Client(url=settings.VAULT_URL, token=settings.VAULT_TOKEN)
secret = client.secrets.kv.read_secret_version(path="dealix/production")
```

---

## SSL/TLS

### Let's Encrypt + cert-manager (Kubernetes)

```bash
# تثبيت cert-manager
helm repo add jetstack https://charts.jetstack.io
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true

# إنشاء ClusterIssuer
kubectl apply -f k8s/cluster-issuer-letsencrypt.yaml
```

```yaml
# k8s/cluster-issuer-letsencrypt.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: ops@dealix.sa
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

```yaml
# في ingress.yaml
annotations:
  cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - api.dealix.sa
    secretName: dealix-tls
```

---

## الروابط والمراجع

- [البنية المعمارية](../ARCHITECTURE.md) — نظرة عامة على المكونات
- [API Reference](./API.md) — توثيق نقاط الطرفية
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Kubernetes Rolling Updates](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)
- [Alembic Migration Guide](https://alembic.sqlalchemy.org/en/latest/)
- [cert-manager Documentation](https://cert-manager.io/docs/)
- [Prometheus Operator](https://prometheus-operator.dev/)
