# العربية

## أدوات الوكيل التنفيذي

تستند فئات الأدوات إلى `auto_client_acquisition/agent_governance/schemas.py` وحدود الأدوات في `auto_client_acquisition/secure_agent_runtime_os/tool_boundary.py`.

### أدوات مسموحة (allowed)

| الأداة | الوصف |
|---|---|
| `read` / `analyze` | قراءة وتحليل المؤشرات المجمَّعة |
| `report.draft_executive` | صياغة ملخص تنفيذي أو مذكّرة قرار |
| `metrics.aggregate` | تجميع المؤشرات (لا PII، لا مؤشرات سرية) |
| `knowledge.search_internal` | البحث في المعرفة الداخلية |
| `queue_for_approval` | رفع مخرج للموافقة |

### أدوات تحتاج موافقة (requires_approval)

| الأداة | السبب |
|---|---|
| `report.publish_external` | نشر خارجي |
| `strategic_commitment` | التزام استراتيجي |
| `email.send_message` | إرسال خارجي |

### أدوات ممنوعة (forbidden)

`scrape_web`, `linkedin_automation`, `cold_whatsapp_send`, `send_whatsapp`, `export_pii_bulk` — مرفوضة دائماً عند حدود الأدوات.

---

# English

## Executive agent tools

Tool categories are based on `auto_client_acquisition/agent_governance/schemas.py` and the tool boundary in `auto_client_acquisition/secure_agent_runtime_os/tool_boundary.py`.

### Allowed tools

| Tool | Description |
|---|---|
| `read` / `analyze` | Read and analyze aggregated metrics |
| `report.draft_executive` | Draft an executive summary or decision memo |
| `metrics.aggregate` | Aggregate metrics (no PII, no confidential metrics) |
| `knowledge.search_internal` | Search internal knowledge |
| `queue_for_approval` | Raise an output for approval |

### Tools requiring approval

| Tool | Reason |
|---|---|
| `report.publish_external` | External publishing |
| `strategic_commitment` | Strategic commitment |
| `email.send_message` | External send |

### Forbidden tools

`scrape_web`, `linkedin_automation`, `cold_whatsapp_send`, `send_whatsapp`, `export_pii_bulk` — always rejected at the tool boundary.
