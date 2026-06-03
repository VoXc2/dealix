# Service Readiness Board

كل صف = خدمة/عرض. كل عمود = أحد العشرة المكوّنات الإلزامية للبيع الرسمي.

| Service / Offer | 1 Offer | 2 Scope | 3 Intake | 4 Data request | 5 Delivery CL | 6 QA CL | 7 Product module | 8 Governance | 9 Proof pack | 10 Upsell | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Lead Intelligence Sprint | Y | Y | Y | Y | Y | Y | revenue_os + data_os | Y | Y | Y | Core |
| AI Quick Win Sprint | Y | Y | Y | Y | Y | Y | operations_os path | Y | Y | Y | Core |
| Company Brain Sprint | Y | Y | Y | Y | Y | Y | knowledge_os path | Y | Y | Y | Core |
| AI Support Desk Sprint | Y | Y | Y | Y | Y | Y | customer_os path | Y | Y | Y | Beta |
| AI Governance Program | Y | Y | Y | Y | Y | Y | governance_os | Y | partial | Y | Core |
| AI Ops Diagnostic | Y | Y | Y | partial | Y | Y | diagnostic only | Y | Y | Y | Entry |
| client_ai_policy_pack | Y | partial | partial | N/A | N/A | N/A | policy templates | Y | N/A | Y | Core |
| Data Readiness Assessment | Y | Y | Y | Y | Y | Y | data_os | Y | Y | Y | Core |

**Legend:** Y = موجود في `docs/services/<folder>/` أو مسار كود واضح؛ partial = يحتاج إكمال؛ N/A = لا ينطبق بنفس الشكل.

## Rule

- **Core** = مسموح البيع الرسمي عند اكتمال الصف.  
- **Beta** = بيع محدود + كشف صريح.  
- **Entry** = مدخل منخفض المخاطر؛ قد لا يتطلب نفس عمق المنتج.

حدّث هذا الجدول عند كل SKU جديد — لا SKU في الخريطة العامة بدون صف هنا.
