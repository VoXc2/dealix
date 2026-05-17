# Agentic Revenue OS

Dealix تعمل كـ **AI-native Revenue Operating Company** لكن بحوكمة مؤسس صريحة:

**Signal -> Source -> Approval -> Action -> Evidence -> Decision -> Value -> Asset**

أي خطوة خارجية بدون سلسلة الحوكمة تعتبر drift.

## العقيدة التنفيذية

- الوكلاء مسموح لهم: `draft`, `classify`, `score`, `recommend`, `monitor`, `log`.
- الوكلاء غير مسموح لهم: إرسال خارجي تلقائي، claims غير مثبتة، أو تنفيذ مالي بدون موافقة.
- جميع الأفعال عالية المخاطر تمر عبر Founder Approval.

## مستويات الأتمتة

1. **Fully Automated**  
   lead capture, scoring, tagging, drafts, reminders, evidence logging.
2. **Agent-Assisted**  
   best ICP, best message, best angle, best price, best next action.
3. **Founder Approval Required**  
   external sends, invoice send, scope send, final diagnosis, case study publish,
   security/compliance claims, أي فعل يؤثر على عميل أو مال أو سمعة.

## مكونات التنفيذ في الكود

- `auto_client_acquisition/revenue_factory_os/policy.py`
  - تصنيف الأتمتة (`classify_automation_level`)
  - بوابة الموافقات (`founder_approval_required`)
  - مصفوفة مخاطر الموافقات (`approval_risk_for_type`)
  - توجيه الأحداث بين الوكلاء (`route_event_to_agents`)
  - التحقق من سلسلة الحوكمة (`validate_governed_event_chain`)
  - عقود 15 وكيل تشغيلي (`DEFAULT_AGENT_CONTRACTS`)

- `tests/test_revenue_factory_policy.py`
  - تغطية قواعد الأتمتة، الموافقات، المخاطر، التوجيه، وسلامة عقود الوكلاء.

## قاعدة منع الفوضى الوكيلية

- لا يوجد autonomous external action.
- لا يوجد revenue recognition قبل payment proof.
- لا يوجد diagnostic final أو case study publish بلا approval مناسب.
