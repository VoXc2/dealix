# Operating Algorithms — خوارزميات تشغيل Dealix

خوارزميات **قرار** قابلة للتنفيذ أسبوعيًا — تُغذّى من Ledgers و QA و Proof.

---

## 4.1 Offer Promotion Algorithm

**رفع ظهور/ترويج عرض** إذا:

- `win_rate >=` هدفك  
- `QA >= 85`  
- `proof_pack_rate = 100%` (حيث ينطبق المسار)  
- `margin >= 65%`  
- `governance critical incidents = 0`  
- يوجد مسار **retainer conversion** مثبت  

**مخرجات منطقية:** `promote_to_public_offer` · زيادة محتوى · صفحة مبيعات.

---

## 4.2 Price Increase Algorithm

**رفع سعر** إذا:

- الطلب **أعلى من سعة تسليم مريحة**  
- win rate لا يزال صحيًا  
- proof قوي  
- تسليم **متكرر**  
- قيمة العميل مرتفعة  

**قاعدة:** طلب جيد + تسليم ثابت + هامش مضغوط → **السعر** قبل **توسيع الفوضى**.

---

## 4.3 Productization Algorithm

**بناء feature** إذا:

- `manual_step_repeated >= 3`  
- `time_cost >= 2h/project` (أو عتبة تجعلها P0)  
- `linked_to_paid_offer`  
- يقلل خطرًا أو يرفع هامشًا  
- `testable`  

**مسار:** template → script → أداة داخلية → ميزة عميل → وحدة SaaS لاحقًا.

---

## 4.4 Retainer Conversion Algorithm

**عرض retainer** إذا:

- `proof_pack_score >= 80`  
- `client_health >= 70`  
- workflow متكرر  
- قيمة شهرية واضحة  
- مشاركة أصحاب قرار جيدة  

**أنواع:** Revenue proof → Monthly RevOps · Workflow → Monthly AI Ops · Knowledge → Monthly Company Brain · Governance → Governance retainer.

---

## 4.5 Venture Graduation Algorithm

**Venture candidate** إذا: **5+** عملاء · **2+** retainers · تسليم متكرر · **module مستخدم** · playbook **≥80** · هامش صحي · owner · مكتبة proof.

**مسار:** service line → BU → venture candidate → venture.

**الكود:** `venture_signal.py` · [`VENTURE_SIGNAL_MODEL.md`](VENTURE_SIGNAL_MODEL.md)

---

**مرافق:** [`../company/SERVICE_READINESS_GATE.md`](../company/SERVICE_READINESS_GATE.md) · [`../company/PRODUCTIZATION_GATE.md`](../company/PRODUCTIZATION_GATE.md) · [`../growth/PROOF_TO_RETAINER_SYSTEM.md`](../growth/PROOF_TO_RETAINER_SYSTEM.md)
