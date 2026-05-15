# العربية

**Owner:** مالك منصة وقت تشغيل الوكلاء (Agent Runtime Platform Lead).

## الغرض

سجل الأدوات يصنّف كل أداة قد يستدعيها وكيل إلى ثلاث فئات صلاحية: `allowed` (مسموح آلياً)، `requires_approval` (يحتاج موافقة بشرية)، `forbidden` (ممنوع نهائياً). هذا التصنيف هو الآلية التي تفرض اللاءات الإحدى عشرة.

## فئات الأدوات

تستند الفئات إلى `ToolCategory` في `auto_client_acquisition/agent_governance/schemas.py` وقوائم `auto_client_acquisition/agent_os/tool_permissions.py`.

| الأداة | الفئة | السبب |
|---|---|---|
| `read` / `analyze` | allowed | قراءة وتحليل بلا أثر خارجي |
| `draft_message` / `draft_email` / `draft_whatsapp_reply` | allowed | إنشاء مسودة فقط، لا إرسال |
| `generate_proof_pack` | allowed | مخرَج داخلي |
| `create_invoice_draft` | allowed | مسودة فاتورة، لا تحصيل |
| `queue_for_approval` | allowed | يرفع للموافقة |
| `send_email_live` | requires_approval | إرسال خارجي |
| `send_whatsapp_live` | requires_approval | إرسال خارجي |
| `charge_payment_live` | requires_approval | التزام مالي |
| `linkedin_automation` | forbidden | أتمتة LinkedIn ممنوعة |
| `scrape_web` | forbidden | الكشط ممنوع |
| `export_pii_bulk` | forbidden | تصدير PII بالجملة ممنوع |

## قائمة الجاهزية

- [x] كل أداة مصنّفة في إحدى الفئات الثلاث.
- [x] كل أداة إرسال خارجي تحت `requires_approval` أو `forbidden`، لا `allowed`.
- [x] أدوات الكشط وأتمتة LinkedIn و WhatsApp البارد في `forbidden`.
- [ ] فحص آلي يرفض أي وكيل يطلب أداة `forbidden`.

## المقاييس

- عدد استدعاءات الأدوات لكل فئة.
- عدد محاولات استدعاء أداة `forbidden` (هدف: صفر).
- متوسط زمن الموافقة على أدوات `requires_approval`.

## خطافات المراقبة

- كل استدعاء أداة يُسجَّل عبر `auto_client_acquisition/agent_observability/trace.py` مع `guardrail_result`.
- تنبيه فوري عند أي محاولة استدعاء أداة `forbidden`.

## قواعد الحوكمة

- لا تُنفَّذ أداة `requires_approval` قبل موافقة موثَّقة عبر `auto_client_acquisition/governance_os/approval_policy.py`.
- أدوات `forbidden` مرفوضة عند حدود الأدوات في `auto_client_acquisition/secure_agent_runtime_os/tool_boundary.py`.
- نقل أداة من `requires_approval` إلى `allowed` يتطلب موافقة مالك المنصة وقائد الحوكمة.

## إجراء التراجع

عند خطأ تصنيف: أعد الأداة فوراً إلى `forbidden`، أوقف الوكلاء التي تستخدمها، ثم أعد التصنيف الصحيح.

## درجة الجاهزية الحالية

**78 / 100 — client pilot.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

---

# English

**Owner:** Agent Runtime Platform Lead.

## Purpose

The Tool Registry classifies every tool an agent may call into three permission classes: `allowed` (auto-permitted), `requires_approval` (needs human approval), `forbidden` (never). This classification is the mechanism that enforces the eleven non-negotiables.

## Tool categories

Categories are based on `ToolCategory` in `auto_client_acquisition/agent_governance/schemas.py` and the lists in `auto_client_acquisition/agent_os/tool_permissions.py`.

| Tool | Class | Reason |
|---|---|---|
| `read` / `analyze` | allowed | Read and analyze, no external effect |
| `draft_message` / `draft_email` / `draft_whatsapp_reply` | allowed | Draft creation only, no send |
| `generate_proof_pack` | allowed | Internal output |
| `create_invoice_draft` | allowed | Invoice draft, no charge |
| `queue_for_approval` | allowed | Raises for approval |
| `send_email_live` | requires_approval | External send |
| `send_whatsapp_live` | requires_approval | External send |
| `charge_payment_live` | requires_approval | Financial commitment |
| `linkedin_automation` | forbidden | LinkedIn automation forbidden |
| `scrape_web` | forbidden | Scraping forbidden |
| `export_pii_bulk` | forbidden | Bulk PII export forbidden |

## Readiness checklist

- [x] Every tool is classified into one of the three classes.
- [x] Every external-send tool is `requires_approval` or `forbidden`, never `allowed`.
- [x] Scraping, LinkedIn automation, and cold WhatsApp tools are `forbidden`.
- [ ] Automated check that rejects any agent requesting a `forbidden` tool.

## Metrics

- Tool call count per class.
- Count of attempts to call a `forbidden` tool (target: zero).
- Median approval time for `requires_approval` tools.

## Observability hooks

- Every tool call recorded via `auto_client_acquisition/agent_observability/trace.py` with `guardrail_result`.
- Immediate alert on any attempt to call a `forbidden` tool.

## Governance rules

- A `requires_approval` tool does not execute before a documented approval via `auto_client_acquisition/governance_os/approval_policy.py`.
- `forbidden` tools are rejected at the tool boundary in `auto_client_acquisition/secure_agent_runtime_os/tool_boundary.py`.
- Moving a tool from `requires_approval` to `allowed` requires both Platform Lead and Governance Lead approval.

## Rollback procedure

On a misclassification: immediately move the tool back to `forbidden`, stop agents that use it, then re-apply the correct class.

## Current readiness score

**78 / 100 — client pilot.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
