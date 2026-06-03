# Dealix Execution Gates — بوابات التنفيذ

لا انتقال لمرحة لاحقة **بدون اجتياز البوابة**.

---

## Gate 1 — Market Pain

لا عرض بدون ألم سوقي واضح:

- العميل يصف الألم **بدون تعليم طويل**
- الألم **يتكرر** في أكثر من عميل
- الألم **قريب من المال أو الوقت أو المخاطر**

---

## Gate 2 — Offer

لا بيع خدمة إلا إذا اكتملت:

buyer · pain · promise · scope · exclusions · price · QA · governance · proof path · **next offer**

---

## Gate 3 — Delivery

لا بدء تنفيذ إلا إذا:

- مدخلات العميل **واضحة**
- **المالك** واضح
- **مقياس النجاح** واضح
- **مسار الموافقة** واضح

---

## Gate 4 — Governance

لا مخرج إلا إذا:

source status · PII status · allowed use · risk level · approval decision · audit event

---

## Gate 5 — Proof

لا إغلاق مشروع إلا إذا:

Proof Pack · Value metric · Limitations · Next recommendation · Capital asset

---

## Gate 6 — Productization

لا feature إلا إذا:

- خطوة يدوية **تُكرر 3+**
- تكلفة وقت **معنوية**
- **مرتبط بالإيراد**
- **يقلل خطر**
- **قابل للاختبار**
- **قابل لإعادة الاستخدام**

---

## Gate 7 — Retainer

لا عرض retainer إلا إذا:

proof score قوي · client health جيد · workflow متكرر · قيمة شهرية واضحة

---

## Gate 8 — Venture

لا فصل وحدة إلا إذا:

5+ عملاء مدفوعون · 2+ retainers · تسليم متكرر · استخدام product module · playbook maturity 80+ · owner موجود · هامش صحي

**الكود:** `auto_client_acquisition/execution_os/gates.py` — `ExecutionGate` · `evaluate_gate` · `all_gates_pass`.

**صعود:** [`../ventures/VENTURE_GRADUATION_GATE.md`](../ventures/VENTURE_GRADUATION_GATE.md) · [`EXECUTION_SUPREMACY_SYSTEM.md`](EXECUTION_SUPREMACY_SYSTEM.md)
