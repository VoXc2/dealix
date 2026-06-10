# API Boundaries — تدفقات مسموحة وممنوعة

الهدف: منع «تكلم الوحدات بعضها عشوائيًا» بحيث تبقى **الحوكمة والإثبات والقيمة** قابلة للتدقيق.

## التدفق المسموح (مرجعي)

```
data_os → governance_os
governance_os → llm_gateway
llm_gateway → proof_os (ومخرجات موثّقة)
proof_os → value_os
value_os → intelligence_os
intelligence_os → command_os
```

في التنفيذ الحالي، يعبّر عن هذا غالبًا:

- تسجيل المصدر وجودة البيانات قبل قرار يسمح بـ AI (`data_os`، `sovereignty_os` / `institutional_control_os`، `standards_os`).
- قرار حوكمة ثم استدعاء نموذج عبر `llm_gateway_v10`.
- تجميع إثبات وقيمة في `proof_architecture_os` و`value_capture_os`.
- إشارات للوحة القرار في `board_decision_os`.

## سلوكيات ممنوعة (سياسة المنتج)

| الممنوع | السبب |
|---------|--------|
| `revenue_os` يرسل رسائل خارجية مباشرة | الإرسال خارجي **draft / موافقة فقط** |
| `agent_os` يتجاوز `governance_os` | لا وكيل فوق القرار التشغيلي |
| `brain_os` (`knowledge_os`) يجيب بلا سجل مصادر | «لا إجابة بلا مصدر» |
| `client_os` يعرض مخرجًا بلا حالة حوكمة | الشفافية للعميل |
| `proof_os` يُسوّق case study بلا proof score / verified | انظر `proof_allows_case_study` و`claim_may_appear_in_case_study` |

## ربط بالكود

- بوابة عدم الهدر في خط الأنابيب: `auto_client_acquisition/revenue_os/anti_waste.py` (مثال: لا إجراء خارجي بدون Decision Passport).
- سياسات القنوات: `auto_client_acquisition/compliance_trust_os/channel_policy.py`.
- سياسة «لا مصدر»: `auto_client_acquisition/knowledge_os/knowledge_eval.py`.

## ملاحظة تنفيذية

FastAPI يربط المسارات في `api/` — عند إضافة router جديد، حافظ على أن **الاستدعاءات الخارجية** تمر عبر طبقة الموافقة والمسودات الموثقة في المنتج.
