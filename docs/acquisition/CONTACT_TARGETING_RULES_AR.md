# Contact Targeting Rules — مَن نتواصل معه؟

**الهدف:** لكل نظام من الأنظمة الخمسة، نحدّد **الدور** الذي نتواصل معه أولًا، مع بديل، ومع تخصيص حسب القطاع. النتيجة: لا أحد يسأل «أكلّم مين؟» — الجواب محسوب مسبقًا في كل Company Intelligence Pack وكل Call Brief.

- **Schema:** [`schemas/contact_target.schema.json`](../../schemas/contact_target.schema.json)
- **البيانات (مصدر الحقيقة):** [`data/acquisition/contact_targets.jsonl`](../../data/acquisition/contact_targets.jsonl)

---

## 1. الخريطة حسب النظام

| النظام | الدور الأول | البديل |
|--------|-------------|--------|
| Revenue Operating System | Head of Sales / Founder / General Manager | Marketing Manager |
| Executive Command OS | Founder / CEO / General Manager | Operations Manager |
| Follow-up Recovery OS | Sales Manager / Marketing Manager | Founder |
| WhatsApp Client OS | Operations Manager / Customer Service Manager | Founder |
| Proposal & Proof OS | Founder / Sales Lead / Business Development Manager | Marketing Manager |

## 2. التخصيص حسب القطاع (sector_overrides)

| القطاع | يُفضّل أول تواصل مع |
|--------|----------------------|
| Marketing Agency | Owner / Business Development / Account Director |
| Training Company | Training Manager / Marketing Manager / Owner |
| B2B Services | Head of Sales / Partner / Customer Service Manager (حسب النظام) |

> القاعدة العامة (للقطاعات الأخرى): عيادة → Clinic Manager · عقار → Sales Manager / Broker Owner · استشارات → Founder / Partner · توظيف → Recruitment Manager.

---

## 3. كيف يُحَل الدور؟

```python
# scripts/generate_acquisition_packs.py
def resolve_contact_role(system, sector, targets):
    target = targets[system]
    if sector in target["sector_overrides"]:
        return target["sector_overrides"][sector]   # تخصيص القطاع أولًا
    return target["primary_roles"][0]                # ثم الدور الأول للنظام
```

أمثلة فعلية من البيانات المولّدة:

```txt
Revenue OS      + B2B Services      → Head of Sales        (CloudShift, Nexus IT)
Follow-up OS    + Marketing Agency  → Account Director     (BrandCraft, Growth Labs)
WhatsApp OS     + Training Company  → Operations Manager   (TrainMe KSA)
Executive OS    + B2B Services      → Founder              (TechVenture)
Proposal OS     + Marketing Agency  → Business Development (MediaPulse, Saudi Marketing Pro)
```

---

## 4. قواعد صارمة

- **أدوار فقط** — لا أسماء أشخاص في أي مكان (خصوصية + PDPL).
- كل نظام مستخدم **يجب** أن يكون له تعيين دور غير فارغ — يفرضه الفحص **C02** في [`acquisition_delivery_check.py`](../../scripts/acquisition_delivery_check.py).
- إذا أُضيف نظام جديد، أضِف صفًّا في `contact_targets.jsonl` وإلا يفشل الفحص.
