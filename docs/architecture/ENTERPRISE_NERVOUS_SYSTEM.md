# Dealix Enterprise Nervous System (ENS)

## الفكرة

Dealix لا يقاس بعدد features.  
Dealix يقاس بقدرته على العمل كـ **Enterprise Nervous System**:

- تنسيق الوكلاء
- تشغيل workflows
- توحيد الذاكرة المؤسسية
- فرض الحوكمة
- توليد ذكاء تنفيذي مستمر

المرجع التنفيذي في الكود: `auto_client_acquisition/enterprise_maturity_os/enterprise_nervous_system.py`.

---

## 20 Core Systems

1. Agent Operating System  
2. Workflow Orchestration System  
3. Organizational Memory System  
4. Governance Operating System  
5. Executive Intelligence System  
6. Organizational Graph System  
7. Execution System  
8. Evaluation System  
9. Observability System  
10. Transformation System  
11. Digital Workforce System  
12. Continuous Evolution System  
13. Identity & Access System  
14. Integration Fabric System  
15. Approval & Escalation System  
16. Policy / Risk / Compliance System  
17. Knowledge Retrieval System  
18. Value Proof System  
19. Adoption Enablement System  
20. Enterprise Scaling System

---

## 10 Organizational Capability Questions

هل Dealix يقدر:

1. redesign workflows  
2. execute workflows  
3. govern workflows  
4. evaluate workflows  
5. scale workflows  
6. supervise agents  
7. manage digital workforce  
8. generate executive intelligence  
9. measure operational impact  
10. improve continuously

---

## Scoring Logic

النظام يحسب:

- `overall_system_score` من الـ20 system
- `organizational_capability_score` من الـ10 قدرات
- `combined_score` (متوسط الاثنين)

ويستخدم نفس bands:

- `0-59` prototype
- `60-74` internal_beta
- `75-84` client_pilot
- `85-94` enterprise_ready
- `95+` mission_critical

---

## Readiness Verdicts

- `is_agentic_enterprise_ready = True` فقط إذا **كل** systems وcapabilities >= 85.
- `is_mission_critical_ready = True` فقط إذا **كل** systems وcapabilities >= 95.

بالإضافة إلى:

- `weak_systems` (أضعف 5 أنظمة)
- `weak_capabilities`
- `next_actions_ar` (خطوات تنفيذية قصيرة لإغلاق الفجوات)

---

## Usage

```python
from auto_client_acquisition.enterprise_maturity_os import (
    CoreSystemsSnapshot,
    OrganizationalCapabilitySnapshot,
    assess_enterprise_nervous_system,
)

assessment = assess_enterprise_nervous_system(
    systems=CoreSystemsSnapshot(...),
    capabilities=OrganizationalCapabilitySnapshot(...),
)

print(assessment.verdict_ar)
print(assessment.combined_score, assessment.combined_band.value)
```

---

## قاعدة القيادة التنفيذية

لا تسأل: "كم endpoint عندنا؟"  
اسأل: "هل المؤسسة أصبحت أذكى، أسرع، وأكثر انضباطًا بفضل النظام؟"
