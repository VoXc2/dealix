# العربية

## أدوات وكيل المبيعات

تستند فئات الأدوات إلى `auto_client_acquisition/agent_governance/schemas.py` وحدود الأدوات في `auto_client_acquisition/secure_agent_runtime_os/tool_boundary.py`.

### أدوات مسموحة (allowed)

| الأداة | الوصف |
|---|---|
| `read` / `analyze` | قراءة وتحليل بيانات العميل والمنتج |
| `crm.create_lead_draft` | إنشاء مسودة عميل محتمل في CRM |
| `crm.update_account_draft` | تحديث مسودة حساب |
| `whatsapp.draft_message` | صياغة مسودة رسالة WhatsApp — لا إرسال |
| `email.draft_message` | صياغة مسودة بريد — لا إرسال |
| `calendar.create_booking_request` | طلب حجز اجتماع |
| `proposal.draft` | صياغة عرض ثنائي اللغة |
| `queue_for_approval` | رفع مخرج للموافقة |

### أدوات تحتاج موافقة (requires_approval)

| الأداة | السبب |
|---|---|
| `whatsapp.send_message` | إرسال خارجي |
| `email.send_message` | إرسال خارجي |
| `discount_offer` | التزام تجاري |
| `contract_commitment` | التزام تعاقدي |
| `charge_payment_live` | التزام مالي |

### أدوات ممنوعة (forbidden)

`scrape_web`, `linkedin_automation`, `cold_whatsapp_send`, `export_pii_bulk` — مرفوضة دائماً عند حدود الأدوات.

---

# English

## Sales agent tools

Tool categories are based on `auto_client_acquisition/agent_governance/schemas.py` and the tool boundary in `auto_client_acquisition/secure_agent_runtime_os/tool_boundary.py`.

### Allowed tools

| Tool | Description |
|---|---|
| `read` / `analyze` | Read and analyze customer and product data |
| `crm.create_lead_draft` | Create a draft lead in the CRM |
| `crm.update_account_draft` | Update a draft account |
| `whatsapp.draft_message` | Draft a WhatsApp message — no send |
| `email.draft_message` | Draft an email — no send |
| `calendar.create_booking_request` | Request a meeting booking |
| `proposal.draft` | Draft a bilingual proposal |
| `queue_for_approval` | Raise an output for approval |

### Tools requiring approval

| Tool | Reason |
|---|---|
| `whatsapp.send_message` | External send |
| `email.send_message` | External send |
| `discount_offer` | Commercial commitment |
| `contract_commitment` | Contractual commitment |
| `charge_payment_live` | Financial commitment |

### Forbidden tools

`scrape_web`, `linkedin_automation`, `cold_whatsapp_send`, `export_pii_bulk` — always rejected at the tool boundary.
