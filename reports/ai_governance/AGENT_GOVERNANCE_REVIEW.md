# مراجعة حوكمة الوكلاء — Agent Governance Review
**التاريخ:** 2026-06-03 · **المراجع:** Agent #30 (AI Governance) · **المصدر:** `data/ai_governance/agent_registry.jsonl` (7 وكلاء) + `AGENT_EVAL_CADENCE_AR.md`

> **الدليل:** L1 internal (مراجعة قائمة على السجلات، لم تُجرَ مقابلات مع المالكين بعد).

---

## 1) نطاق المراجعة

تمت مراجعة **7 وكلاء** مُسجَّلين في `data/ai_governance/agent_registry.jsonl`، تغطي 6 personas: sales، delivery، finance، security، governance، data، + 1 vendor external.

---

## 2) جدول المراجعة لكل وكيل

| Agent ID | Persona | Autonomy | Risk | Eval Cadence | Owner | الحكم |
|---|---|---|---|---|---|---|
| AGENT-SALES-001 | Sales Outreach Prep | A3 | medium | weekly | sales_dept_head | ✅ متوافق |
| AGENT-DELIVERY-001 | Pilot Delivery Report | A4 | high | daily | delivery_dept_head | ✅ متوافق |
| AGENT-FIN-001 | ZATCA Invoice Sender | A4 | high | daily | finance_dept_head | ✅ متوافق |
| AGENT-SEC-001 | Security Monitoring | A4 | high | daily | security_lead | ✅ متوافق |
| AGENT-GOV-001 | Governance Policy Reviewer | A2 | low | weekly | agent_30 | ✅ متوافق |
| AGENT-DATA-001 | Data Quality Observer | A1 | low | monthly | data_lead | ✅ متوافق |
| AGENT-VENDOR-001 | Vendor AI (Sales Assist) | A2 | medium | weekly | agent_30 | ⚠️ متوافق + external_vendor boundary |

---

## 3) التحقق من المعايير

### 3.1 مستوى الاستقلالية (Autonomy Level) — Pass
- A1: 1 (AGENT-DATA-001) — مناسب للمراقبة فقط
- A2: 2 (AGENT-GOV-001, AGENT-VENDOR-001) — مسودة فقط
- A3: 1 (AGENT-SALES-001) — queue
- A4: 3 (AGENT-DELIVERY-001, AGENT-FIN-001, AGENT-SEC-001) — تنفيذ بموافقة
- A5: **0** — لا يوجد (متوافق مع Hard Constraint)
- **0 وكلاء في A5** ✅

### 3.2 Risk Level ↔ Eval Cadence — Pass
- low ↔ monthly: 1/1 ✅
- low ↔ weekly: 1 (AGENT-GOV-001) — متوافق (governance policy reviewer يستحق weekly حسب §6)
- medium ↔ weekly: 2/2 ✅
- high ↔ daily: 3/3 ✅

### 3.3 Owner Assignment — Pass
- 7/7 لديهم `owner` محدد
- 4/7 department_head
- 1/7 security_lead
- 1/7 data_lead
- 1/7 agent_30

### 3.4 Status — Pass
- 7/7 `status=active`
- 0 frozen, 0 retired, 0 paused (متوازن)

### 3.5 External Action Capability — Pass
- 0 `external_blocked` لوكلاء داخليين
- AGENT-VENDOR-001 = `external_blocked` ✅
- 4 وكلاء A4 = `external_with_approval` ✅
- 2 (A1, A2) = `none` ✅

### 3.6 External Vendor Boundary — Pass
- AGENT-VENDOR-001 مُسجَّل بـ `external_vendor.name=VendorCo`
- `dpa_signed=true`
- `vendor_due_diligence_id=VDD-2026-014`
- النطاق المُسموح محدود بـ `reports/vendor_assist/` (لا customer data)

### 3.7 Forbidden File Areas — Pass
- 7/7 لديهم `forbidden_file_areas` غير فارغ
- الأسرار (`.env*`, `secrets/`) مذكورة في 7/7
- `data/production/` مذكورة في 5/7 (المشروعة: 2 لا تحتاج production — A1 read-only data quality، A2 governance drafter)

---

## 4) النتائج حسب Persona

| Persona | عدد الوكلاء | A-Level | الحكم |
|---|---|---|---|
| Sales | 1 | A3 | ✅ |
| Delivery | 1 | A4 | ✅ |
| Finance | 1 | A4 | ✅ |
| Security | 1 | A4 | ✅ |
| Governance | 1 | A2 | ✅ |
| Data | 1 | A1 | ✅ |
| Vendor (external) | 1 | A2 | ✅ |

---

## 5) الاستثناءات والتوصيات

### 5.1 لا استثناءات حرجة
كل الوكلاء يطابقون السياسة.

### 5.2 توصيات
1. **AGENT-VENDOR-001:** توثيق إضافي مطلوب حول ما يطابقه (VENDORCO) في `data/procurement/` — تأكد من تحديث سنوي.
2. **AGENT-GOV-001:** عند أول اختبار حقيقي لتغيير سياسة، تأكد من backup_owner مسجَّل.
3. **AGENT-DATA-001:** منخفض الاستخدام — مراقبة `idle` ربع سنوي.

### 5.3 المتابعة
- ربع سنوي: Agent #30 يعيد المراجعة
- عند أي تغيير: سجل في `agent_registry.jsonl` بـ `changelog_event`
- التدريب: مالك جديد يحتاج توقيع على السياسة قبل تولّي المسؤولية

---

## 6) الحكم الإجمالي

**✅ PASS** — كل الوكلاء السبعة يطابقون السياسة. لا يحتاج أي منهم ترقية/تخفيض/إيقاف فوري.

**التوصية:** استمرار المراقبة بالوتيرة المحددة. التركيز على تحويل الأدلة من L1 إلى L2 بقياس أسبوعي خلال 30 يوم.

---

## 7) الربط

- [`../docs/ai_governance/AGENT_AUTONOMY_LEVELS_AR.md`](../docs/ai_governance/AGENT_AUTONOMY_LEVELS_AR.md)
- [`../docs/ai_governance/AGENT_EVAL_CADENCE_AR.md`](../docs/ai_governance/AGENT_EVAL_CADENCE_AR.md)
- [`../data/ai_governance/agent_registry.jsonl`](../data/ai_governance/agent_registry.jsonl)
- [`../schemas/agent_registry.schema.json`](../schemas/agent_registry.schema.json)
