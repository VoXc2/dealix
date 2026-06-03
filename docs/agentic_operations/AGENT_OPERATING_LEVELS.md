# Agent Operating Levels

| Level | الاسم | وصف مختصر |
|-------|--------|------------|
| 0 | No Agent | لا وكيل |
| 1 | Assistant Agent | مساعدة داخلية |
| 2 | Drafting Agent | مسودات |
| 3 | Recommendation Agent | توصيات |
| 4 | Approval Queue Agent | طابور موافقة |
| 5 | Internal Execution Agent | تنفيذ داخلي (ضوابط قوية) |
| 6 | External Action Agent | إجراءات خارجية (**enterprise-only**) |
| 7 | Autonomous External Agent | **ممنوع حاليًا** |

## قاعدة MVP

- **يسمح:** المستويات **1–4** فقط.  
- **Level 5:** يتطلب ضوابط داخلية قوية (خارج MVP الافتراضي).  
- **Level 6:** enterprise-only.  
- **Level 7:** ممنوع.

## القيمة المبكرة

الوكيل ينظّف، يصنّف، يرتّب، يقترح، يكتب draft، يشرح، **يرفع للموافقة** — دون تعريض السمعة والبيانات.

## الكود

`agentic_operations_os` — دالة `agent_operating_level_allowed_in_mvp`.
