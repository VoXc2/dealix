# Maturity-to-Offer Matrix

## الجدول المرجعي

| Level | العميل يحتاج | العرض المناسب | ممنوع / مؤجل |
|-------|----------------|----------------|---------------|
| 0 | ضبط الفوضى | AI Governance & Readiness Diagnostic | Agents، Platform، External automation، Outreach |
| 1 | وضوح | Capability Diagnostic (+ فرع Sprint حسب التشخيص) | Platform، Enterprise OS |
| 2 | تنفيذ أولي | Productized Sprint | Enterprise OS |
| 3 | حوكمة كاملة | Governance Runtime + Proof + Cadence | External automation بلا موافقة |
| 4 | تشغيل شهري | Monthly Retainer | Autonomous agents |
| 5 | طبقة تشغيل | Client Workspace + Proof + Value + Approvals | Complex enterprise features مبكرًا |
| 6 | توسع مؤسسي | Enterprise AI Operations Program | White-label |
| 7 | تحكم كامل | AI Control Plane + Enterprise Governance | **بدون** مسار audit واضح |

## Level 1 — اختيار أول Sprint (بعد Capability Diagnostic)

| الشرط | التوصية |
|--------|---------|
| الألم قريب من الإيراد | Revenue Intelligence Sprint |
| الخطر أعلى من القيمة | AI Governance Review |
| المعرفة مبعثرة | Company Brain Sprint |

يُنفَّذ في الكود عبر `level1_first_track(...)`.

## شروط Retainer (Level 4)

Proof Score ≥ 80، Adoption ≥ 70، وجود owner، cadence شهري، مخاطر حوكمة مسيطر عليها.

## شروط Level 7

3+ workflows، راعٍ تنفيذي، مالك حوكمة، حاجة audit، cadence شهري، ميزانية واضحة.

## الكود

`auto_client_acquisition/client_maturity_os/offer_matrix.py`
