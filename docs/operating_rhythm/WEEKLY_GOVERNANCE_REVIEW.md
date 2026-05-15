# Weekly Governance Review — حوكمة الذكاء الاصطناعي والقنوات

الوكلاء و«الظل الذكي» مخاطر تشغيلية. المؤسسات تحتاج **تسجيلًا، مراقبة، وإيقافًا مركزيًا** للوكلاء والمخرجات.

## أسئلة المراجعة

- هل كل **AI runs** مسجّلة؟
- هل كل **outputs** لها governance status؟
- هل ظهرت **PII flags**؟
- هل تم رفض أي **claim** غير مدعوم؟
- هل طلب عميل **automation ممنوعة**؟
- هل وكيل طلب **صلاحية أعلى**؟
- هل وقع **حادث**؟

## قرارات صارمة

| الملاحظة | القرار |
|----------|--------|
| Output بلا governance status | **فشل QA** — إصلاح قبل التسليم |
| إجراء خارجي بلا موافقة | **حادث** — مسار incident |
| Agent autonomy > 3 في MVP | **حظر** |
| Claim غير مدعوم | إزالة + **قاعدة/اختبار** جديد |

## الكود

`auto_client_acquisition/operating_rhythm_os/governance_review.py`  
انظر أيضًا: `standards_os/agent_control_standard.py`، `compliance_trust_os/`، `llm_gateway_v10/`.
