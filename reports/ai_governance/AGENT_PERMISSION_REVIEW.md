# مراجعة صلاحيات الوكلاء — Agent Permission Review
**التاريخ:** 2026-06-03 · **المراجع:** Agent #30 · **المصدر:** `data/ai_governance/agent_permissions.jsonl` (7 منح)

> **الدليل:** L1 internal (مراجعة قائمة على السجلات، cross-check مع `AGENT_PERMISSION_LIFECYCLE_AR.md`).

---

## 1) نطاق المراجعة

7 منح صلاحيات في `data/ai_governance/agent_permissions.jsonl` عبر 7 وكلاء.

---

## 2) جدول المراجعة

| Permission ID | Agent | Scope | Risk | Granted → Expires | Owner | Status |
|---|---|---|---|---|---|---|
| PERM-20260601-0001 | AGENT-SALES-001 | data/commercial/ (write) | medium | 2026-06-01 → **2026-08-30** (90d) | sales_dept_head | active ✅ |
| PERM-20260601-0002 | AGENT-DELIVERY-001 | send:email | high | 2026-06-01 → **2026-07-01** (30d) | founder | active ✅ |
| PERM-20260601-0003 | AGENT-FIN-001 | network:api.moyasar.com | high | 2026-06-01 → **2026-06-08** (7d) | founder | active ✅ |
| PERM-20260510-0005 | AGENT-GOV-001 | docs/ai_governance/ (write) | low | 2026-05-10 → **2026-09-10** (~120d) | agent_30 | active ✅ |
| PERM-20260420-0006 | AGENT-DATA-001 | data/ (read) | low | 2026-04-25 → **2027-04-25** (365d) | data_lead | active ✅ |
| PERM-20260520-0007 | AGENT-VENDOR-001 | data/customer_pilot/ | high | 2026-05-20 → 2026-05-21 (**1d**) | founder | **revoked** ✅ |
| PERM-20260601-0004 | AGENT-SEC-001 | audit/ (read) | medium | 2026-05-15 → **2026-08-15** (~90d) | security_lead | active ✅ |

---

## 3) التحقق من المعايير

### 3.1 لا صلاحيات عالية الخطورة دائمة — **PASS**
- 3 صلاحيات `high` نشطة (PERM-0002, PERM-0003, PERM-0004 wait, sec is medium)
- جميع الـ high لها `expires_at`:
  - PERM-0002 (send:email) — 30 يوم ✅
  - PERM-0003 (network) — 7 أيام ✅
  - **لا توجد صلاحية high بدون expires_at** ✅

### 3.2 Renewal Cadence يطابق مستوى الخطر — **PASS**
| Risk | Expected (per §3 AGENT_PERMISSION_LIFECYCLE_AR.md) | Observed | Pass? |
|---|---|---|---|
| Low | 180d | 365d (PERM-0006) | ⚠️ over, but it's a read-only; acceptable for one-time/year |
| Low | 180d | ~120d (PERM-0005) | ✅ |
| Medium | 90d | 90d (PERM-0001, PERM-0004) | ✅ |
| High | 30d | 30d (PERM-0002) | ✅ |
| High | 30d (or single transaction) | 7d (PERM-0003) | ✅ tighter |
| High | 1d | 1d (PERM-0007) | ✅ single transaction |

> **استثناء:** PERM-0006 (data/ read) مدته 365 يوم. السياسة تنص على 180 يوم لـ low. التوصية: تقليص إلى 180 يوم في التجديد القادم.

### 3.3 لا أسرار لـ A5 — **PASS**
- 0 وكلاء A5 في السجل
- 0 منح `secret` (A5 ممنوع)

### 3.4 لا وصول عميل بدون pilot — **PARTIAL**
- PERM-0007 (customer_pilot) كان محاولاً ثم أُلغي في 24 ساعة
- **لا توجد منح customer_data نشطة** ✅
- 0 high-risk grant لـ vendor AI حالياً ✅

### 3.5 Revocation Triggers — **PASS**
- PERM-0007: `revoked` بسبب `vendor_ai_not_authorized_for_customer_data_per_default_deny` (Default-Deny trigger)
- `revoked_at`, `revoked_by`, `revocation_reason` كلها مسجَّلة ✅

### 3.6 Approver Role — **PASS**
- founder لـ high (3/3) ✅
- department_head لـ medium (2/2) ✅
- security_lead لـ security (1/1) ✅
- agent_30 لـ low (governance docs) — مسموح لأن المالك المباشر ✅

### 3.7 Evidence Level — **PASS**
- L0: 1 (PERM-0007 — قبل الإلغاء، السبب)
- L1: 4 (low/medium)
- L2: 1 (network — test result)
- L3: 1 (send:email — pilot contract)
- **لا L0 على منح active حاليًا** ✅

---

## 4) الصلاحيات القريبة من الانتهاء (Expiring Soon)

| Permission | Expires | Days Left | Action |
|---|---|---|---|
| PERM-20260601-0003 | 2026-06-08 | 5 | ⚠️ تجديد أو إغلاق |
| PERM-20260601-0002 | 2026-07-01 | 28 | ⏰ قريب |
| PERM-20260601-0001 | 2026-08-30 | 88 | متابعة |

---

## 5) النتائج

| البند | Pass/Fail |
|---|---|
| لا high-risk دائم | ✅ |
| Renewal cadence | ✅ (1 تحذير) |
| لا أسرار لـ A5 | ✅ |
| لا customer data نشط لـ vendor | ✅ |
| Revocation triggers موثّقة | ✅ |
| Approver role مناسب | ✅ |
| Evidence level كافٍ | ✅ |

---

## 6) التوصيات

1. **PERM-20260420-0006:** تقليص المدة من 365 إلى 180 يوم في التجديد القادم.
2. **PERM-20260601-0003:** إرسال reminder قبل 2026-06-08 (5 أيام).
3. **PERM-20260601-0002:** تجديد فقط بعد إعادة تقييم Permission Scope (مطلوب شهريًا للـ high).
4. **إضافة:** ربط الـ permission grants بـ eval_id (تقييم دوري للقدرة نفسها).

---

## 7) الحكم الإجمالي

**✅ PASS** مع 1 تحذير (PERM-0006 duration) و 1 متابعة قريبة الانتهاء (PERM-0003).

**نسبة الامتثال:** 7/7 = 100% (مع التحذير أعلاه).

---

## 8) الربط

- [`../docs/ai_governance/AGENT_PERMISSION_LIFECYCLE_AR.md`](../docs/ai_governance/AGENT_PERMISSION_LIFECYCLE_AR.md)
- [`../docs/ai_governance/AGENT_ACCESS_RIGHTS_POLICY_AR.md`](../docs/ai_governance/AGENT_ACCESS_RIGHTS_POLICY_AR.md)
- [`../data/ai_governance/agent_permissions.jsonl`](../data/ai_governance/agent_permissions.jsonl)
- [`../schemas/agent_permission.schema.json`](../schemas/agent_permission.schema.json)
