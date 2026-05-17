# 04 — التأهيل / Qualification (Layer 4)

## العربية

### نموذج تقييم الـ Lead

```
+4   decision maker
+3   founder / COO / CRO / head of ops
+3   B2B company
+3   has CRM or pipeline process
+3   uses or plans AI
+2   Saudi / GCC
+2   urgent within 30 days
+2   budget 5k+ SAR
+2   partner / referrer potential
-4   no company
-3   student / job seeker
-3   vague AI curiosity
-2   no clear pain
```

### الفئات

| الفئة | النطاق | المعنى |
|---|---|---|
| **A** | 15+ | book now |
| **B** | 10–14 | proof pack + nurture |
| **C** | 6–9 | educate أو partner route |
| **D** | أقل من 6 | ignore / archive |

### قواعد القرار

```
A        → meeting within 7 days
B        → proof pack + follow-up
C        → educational sequence
D        → no action
Partner  → partner sequence
```

### الربط بالنظام

- تقييم الـ lead الحالي في `auto_client_acquisition/crm_v10/lead_scoring.py`
  **حتمي (deterministic)** — fit + urgency، بدون LLM وبدون عشوائية.
- نموذج النقاط وفئات A/B/C/D أعلاه **جديد**؛ يُبنى في **المرحلة 2** كوحدة
  `sales_os/lead_tiering.py` **فوق** `lead_scoring.py` لا بدلاً منه — مع الحفاظ
  على الحتمية (شرط ثابت في المستودع).

---

## English

### Lead scoring model

```
+4   decision maker
+3   founder / COO / CRO / head of ops
+3   B2B company
+3   has CRM or pipeline process
+3   uses or plans AI
+2   Saudi / GCC
+2   urgent within 30 days
+2   budget 5k+ SAR
+2   partner / referrer potential
-4   no company
-3   student / job seeker
-3   vague AI curiosity
-2   no clear pain
```

### Tiers

| Tier | Range | Meaning |
|---|---|---|
| **A** | 15+ | book now |
| **B** | 10–14 | proof pack + nurture |
| **C** | 6–9 | educate or partner route |
| **D** | below 6 | ignore / archive |

### Decision rules

```
A        → meeting within 7 days
B        → proof pack + follow-up
C        → educational sequence
D        → no action
Partner  → partner sequence
```

### How it connects to the system

- Current lead scoring in `auto_client_acquisition/crm_v10/lead_scoring.py` is
  **deterministic** — fit + urgency, no LLM, no randomness.
- The points model and A/B/C/D tiers above are **new**; built in **Phase 2** as
  a `sales_os/lead_tiering.py` module **on top of** `lead_scoring.py`, not
  replacing it — and it must stay deterministic (a repo invariant).
