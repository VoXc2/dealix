# Dealix Agentic Revenue Factory (تشغيل محكوم)

هذا المستند يترجم العقيدة التشغيلية إلى قواعد قابلة للتنفيذ داخل النظام.

## الصيغة الحاكمة

Founder-led trust  
+ Proof-led funnel  
+ Automated revenue ops  
+ Agentic execution loops  
+ Disciplined approval system  
+ Evidence ledger  
+ Delivery-to-product learning  
+ Partner leverage  
+ Security-by-design

## السلسلة الحاكمة

Signal → Source → Approval → Action → Evidence → Decision → Value → Asset

أي إجراء خارج هذه السلسلة يعتبر **drift** ويتم حظره.

## مستويات الأتمتة

### Level 1 — Fully Automated
- تنفيذ داخلي آمن: capture, scoring, drafts, checklists, logging.
- لا إرسال خارجي مباشر.

### Level 2 — Agent-Assisted
- الوكيل يقترح: ICP, messaging angle, pricing, next action, upsell, partner.
- القرار النهائي للمؤسس.

### Level 3 — Founder Approval Required
- إرسال خارجي، إرسال scope، إرسال invoice، تشخيص نهائي، case study، security claim، إجراءات عالية الأثر.
- لا تنفيذ بدون موافقة صريحة.

## بوابات صارمة

- لا `invoice_send` بدون `scope_approved`.
- لا `delivery_start` بدون `invoice_paid`.
- لا `revenue_recognized` بدون `payment_proof`.
- لا `case_study_publish` بدون موافقة العميل.
- لا `security_claim_publish` بدون مصدر موثق.

## التنفيذ في الكود

- سياسة التشغيل: `auto_client_acquisition/governance_os/revenue_factory_policy.py`
- واجهة الاستدعاء: `evaluate_governed_action(...)`
- مخرجات القرار:
  - `allow`
  - `needs_founder_approval`
  - `blocked`

## الهدف التنفيذي

Dealix لا تشغّل Agents بلا ضوابط؛  
Dealix تشغّل الإيراد والذكاء الاصطناعي كتشغيل محكوم بالمصادر والموافقات والأدلة.

