# Playbook تسليم Enterprise AI Transformation

برنامج تسليم **Enterprise AI Operating System** — 90 يومًا، 6 مراحل ببوابات تحقق.
البنية المرجعية في الكود: `auto_client_acquisition/enterprise_os/enterprise_program.py`.

## الدور

Audit → Foundation → First Agents → Integrations → Executive Layer → Scale Plan.
كل مرحلة لها مالك ومدخل ومخرج وبوابة. لا تُفوتر مرحلة قبل اجتياز بوابتها.

## المراحل

| # | المرحلة | الأسابيع | البوابة (Gate) |
|---|---------|----------|----------------|
| 1 | AI Audit — تدقيق الذكاء الاصطناعي | 1–2 | AI Opportunity Map معتمدة من المؤسس |
| 2 | Foundation — التأسيس | 3–4 | قواعد الحوكمة + audit logging تعمل |
| 3 | First Agents — الوكلاء الأوائل | 5–6 | أول وكيل يجتاز eval؛ draft-first مؤكَّد |
| 4 | Integrations — التكاملات | 7–8 | عقود التكامل موقّعة؛ لا live-send |
| 5 | Executive Layer — الطبقة التنفيذية | 9–10 | ROI dashboard موصول بـ value ledger |
| 6 | Scale Plan — خطة التوسع | 11–12 | حزمة التسليم مقبولة؛ Proof Pack مُجمَّع |

## نقاط تشغيلية

- **Audit:** مقابلات أصحاب المصلحة، تحليل العمليات والبيانات، خريطة الفرص،
  خريطة المخاطر، roadmap 30/60/90. المخرج وثيقة AI Opportunity Map.
- **Foundation:** workspace + auth/users، إدخال المعرفة، dashboard أساسي،
  قواعد حوكمة، append-only audit log.
- **First Agents:** وكيل مبيعات أو دعم (draft-first فقط)، Company Brain v1،
  مسار human handoff، workflows موافقة.
- **Integrations:** عقود تكامل WhatsApp / CRM / Email / Drive — تعريف العقد
  بدون تفعيل إرسال مباشر.
- **Executive Layer:** ROI dashboard موصول بـ value ledger، تقارير تنفيذية،
  risk dashboard، decision memos.
- **Scale Plan:** تدريب الفريق، حزمة التسليم، خطة التبني، roadmap 6 أشهر،
  عرض retainer.

## الحوكمة (لا يُتجاوز)

- لا إرسال أو تنفيذ تلقائي — `approval_required` على كل إجراء خارجي.
- لا proof مزيّف ولا أرقام إيراد مزيّفة — كل رقم `is_estimate`.
- كل مخرج يحمل `governance_decision` وسجل تدقيق.
- لا بيع رسمي للخدمة قبل اجتياز بوابات `DEALIX_READINESS.md`.

## روابط

- [REVENUE_INTELLIGENCE_DELIVERY_PLAYBOOK.md](REVENUE_INTELLIGENCE_DELIVERY_PLAYBOOK.md)
- [DELIVERY_QA_CHECKLIST.md](DELIVERY_QA_CHECKLIST.md)
- [CLIENT_HANDOFF_CHECKLIST.md](CLIENT_HANDOFF_CHECKLIST.md)
- [../OFFER_LADDER_AND_PRICING.md](../OFFER_LADDER_AND_PRICING.md)

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
