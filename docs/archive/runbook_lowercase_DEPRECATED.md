# Operations Runbook

Operational playbook for running AI Company Saudi in production.

---

## 🚨 Incident response

### Service down (500s or unreachable)

```bash
# 1. Check health endpoint
curl -fv http://localhost:8000/health

# 2. Check systemd (if bare metal)
sudo systemctl status ai-company
sudo journalctl -u ai-company -n 200 --no-pager

# 3. Check Docker (if containerized)
docker compose ps
docker compose logs --tail=200 app

# 4. Restart
sudo systemctl restart ai-company  # or: docker compose restart app
```

### High error rate

1. Check `usage_summary()` from the model router — which provider is failing?
2. If one LLM is down, fallback chain should handle it — but confirm in logs.
3. Check provider status pages (Anthropic, OpenAI, Google, Groq).
4. If persistent: set `PREFERRED_PROVIDER` via env override to bypass the broken one.

### Rate limit errors from an LLM

- Groq and DeepSeek have generous limits but strict bursts.
- Anthropic: switch to fallback (OpenAI) temporarily.
- Long-term: enable prompt caching (Anthropic) or request a limit increase.

### Webhook failures

Check:
- `WHATSAPP_VERIFY_TOKEN` matches what Meta is sending
- `WHATSAPP_APP_SECRET` is set for signature verification
- The public URL is reachable (test from a second host)

---

## 🔑 Secret rotation

**Quarterly rotation schedule** (recommended):

1. Generate new key in the provider's dashboard
2. Update `.env` or secrets manager
3. Redeploy (`docker compose up -d` or `systemctl restart ai-company`)
4. Verify `/health` shows the provider still in `providers` list
5. Revoke the old key

**Emergency rotation** (after suspected leak):
- Do it **immediately** — don't wait for the deployment
- Revoke old key BEFORE generating new one if exposure is severe
- Run `gitleaks detect --source . --log-level debug` on git history
- Scan GitHub → Settings → Security → Secret scanning alerts

---

## 📊 Monitoring targets

| Metric | Target | Alert threshold |
| --- | --- | --- |
| `/health` uptime | 99.9% | < 99.5% in 24h |
| API p50 latency | < 2s | > 5s for 10min |
| API p95 latency | < 10s | > 20s for 5min |
| Error rate | < 1% | > 5% for 5min |
| LLM fallback rate | < 5% | > 20% for 10min |
| DB connection pool | < 80% | > 95% for 5min |

---

## 💾 Backups

### PostgreSQL

Daily backup cron (example for `postgres` container):

```bash
# /etc/cron.daily/ai-company-backup
#!/bin/bash
BACKUP_DIR=/var/backups/ai-company
DATE=$(date +%Y%m%d_%H%M%S)
docker exec ai-company-postgres pg_dump -U ai_user ai_company | gzip > "$BACKUP_DIR/ai_company_$DATE.sql.gz"
# Keep 30 days
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +30 -delete
```

### Restore

```bash
gunzip -c backup.sql.gz | docker exec -i ai-company-postgres psql -U ai_user ai_company
```

---

## 🧹 Maintenance windows

- **Dependencies**: review Dependabot PRs weekly (Monday mornings Riyadh time)
- **LLM model versions**: review quarterly (Claude, Gemini, Llama all release updates frequently)
- **Infrastructure**: OS + Docker updates monthly
- **Certificate renewal**: Let's Encrypt auto-renews; monitor via `certbot renew --dry-run`

---

## 📈 Scaling

### Vertical (single-node)

Start with 2 workers × 1 CPU × 1 GB RAM. Scale workers linearly with CPU cores:
```bash
uvicorn api.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### Horizontal (multi-node)

Requirements before scaling out:
- Move from in-process dedup cache (`IntakeAgent._seen_hashes`) to Redis
- Ensure Postgres connection pooling is tuned (`pool_size`, `max_overflow`)
- Put nginx / cloud LB in front

---

## 🔧 Common tasks

### Rerun a lead through the pipeline

```python
# In a Python shell with venv activated:
import asyncio
from auto_client_acquisition.pipeline import AcquisitionPipeline

p = AcquisitionPipeline()
result = asyncio.run(p.run(payload={"company":"Test","name":"X","message":"test"}))
print(result.to_dict())
```

### Test an LLM provider manually

```python
import asyncio
from core.config.models import Task
from core.llm import get_router

router = get_router()
print(router.available_providers())

response = asyncio.run(
    router.run(task=Task.REASONING, messages="Say hi in Arabic.")
)
print(response.content)
print(router.usage_summary())
```

### Generate a proposal for an existing lead

```bash
curl -X POST http://localhost:8000/api/v1/sales/proposal \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "شركة التجريب",
    "sector": "healthcare",
    "pain_points": ["بطء المواعيد","فوضى السجلات"],
    "budget_hint": 45000,
    "locale": "ar",
    "region": "Saudi Arabia"
  }'
```

---

## 🔗 Useful links

- FastAPI docs: https://fastapi.tiangolo.com
- Anthropic API: https://docs.anthropic.com
- Gemini API: https://ai.google.dev
- Groq API: https://console.groq.com/docs
- DeepSeek API: https://api-docs.deepseek.com
- WhatsApp Cloud API: https://developers.facebook.com/docs/whatsapp/cloud-api
- HubSpot API: https://developers.hubspot.com
