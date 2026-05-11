# GO-LIVE SALES RUNBOOK — الخطة الشاملة للبيع الحقيقي اليومي

## الهدف
تحويل البيع من “مبادرات متفرقة” إلى **نظام يومي متكرر** يبدأ من:
- من نستهدف؟
- بأي باقة؟
- بأي KPI Promise؟
- متى نطلب التوقيع؟
- وما خطة ما بعد التوقيع لأول 60 يوم؟

## أوامر التشغيل اليومية
1. عرض خطة البيع اليومية للشريحة:
   - `python3 -m saudi_ai_provider go-live-sales --segment enterprise --lang ar --max-plays 5`
2. تقييم جاهزية طلب التوقيع:
   - `python3 -m saudi_ai_provider signature-readiness --stage contract_ready --buyer-commitment high --proof-level L4 --risk-status low --governance-contract-accepted yes`
3. توليد حزمة تنفيذ العميل:
   - `python3 -m saudi_ai_provider enterprise-playbook --service CUSTOMER_PORTAL_GOLD --intake-file intake/demo_customer_intake.json --profile hybrid_governed_execution --lang ar`

## التشغيل اليومي (Founder Loop)
### صباحًا
1. تصنيف 20 حساب مستهدف.
2. تشغيل `proposal-scorecard` للصفقات الأعلى احتمال.
3. اختيار Top 3 فرص لليوم.

### منتصف اليوم
1. توليد enterprise-playbook لكل فرصة نشطة.
2. إرسال العرض التنفيذي مع KPI + Governance Contract.
3. جمع blockers الفعلية من decision owner.

### مساءً
1. تحديث renewal/expansion queue.
2. تسجيل proof events الجديدة.
3. إعداد Founder Brief لليوم التالي.

## نموذج الاستهداف (مين تستهدف؟)
### SMB
- الأولوية:
  - `AI_CUSTOMER_OPERATIONS_PLATFORM`
  - `AI_WORKFLOW_AUTOMATION_FACTORY`
  - `AI_REVENUE_COMMAND_CENTER`

### Mid-Market
- الأولوية:
  - `AI_REVENUE_COMMAND_CENTER`
  - `AI_GOVERNANCE_OS`
  - `AI_OBSERVABILITY_PLATFORM`
  - `AI_CUSTOMER_OPERATIONS_PLATFORM`

### Enterprise
- الأولوية:
  - `AI_GOVERNANCE_OS`
  - `AI_RUNTIME_MANAGEMENT`
  - `AI_OBSERVABILITY_PLATFORM`
  - `EXECUTIVE_AI_INTELLIGENCE_SYSTEM`
  - `PDPL_AI_COMPLIANCE_PLATFORM`

## آلية اختيار العرض (بأي باقة؟)
1. استخدم `go-live-sales` لاختيار play مناسب حسب القطاع/المشتري/الألم التجاري.
2. استخدم `quote` لتسعير SKU.
3. استخدم `enterprise-playbook` لتوليد:
   - Proposal
   - SOW
   - KPI Contract
   - Governance Contract

## KPI Promise Framework (بأي KPI تعِد؟)
القاعدة الذهبية:
- لا وعد بدون baseline.
- لا KPI بدون proof target.
- لا signature بدون governance acceptance.

أمثلة وعود:
- Customer Ops: `ticket_deflection_rate >= 25%`
- Governance: `approval_trace_coverage = 100%`
- Observability: `incident_mttr -30%`
- Revenue: `pipeline_velocity +20%`

## توقيت طلب التوقيع (متى تطلب التوقيع؟)
اطلب التوقيع فقط إذا:
1. `stage` = `executive_alignment` أو `contract_ready`
2. `buyer_commitment` >= medium
3. `proof_level` >= L3
4. `risk_status` ≠ high
5. governance contract accepted = yes

## إذا لم يوقع العميل
- بعد 3 أيام: أرسل executive recap رقمي واضح.
- بعد 7 أيام: اعمل objection handling call.
- بعد 14 يوم: قدم phased pilot scope محكوم.

## خطة ما بعد التوقيع (أول 60 يوم)
### الأيام 1–14
- Discovery + KPI baseline + risk controls.

### الأيام 15–30
- Shadow mode + proof capture + governance adherence.

### الأيام 31–60
- Controlled production + executive weekly pack + expansion candidate shortlist.

## مؤشرات نجاح نظام البيع
- Demo-to-Proposal Conversion
- Proposal-to-Signature Conversion
- Median Days to Signature
- Gross Margin Quality
- First-60-Day KPI Achievement
- Expansion Readiness at Day 45/60

## حوكمة غير قابلة للكسر
- no_cold_whatsapp
- no_scraping
- no_linkedin_automation
- no_live_send_without_approval
- no_live_charge_without_approval
- no_public_proof_without_consent
