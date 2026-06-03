# Full Ops — Test Plan (Incremental)

**المرجع:** [`../strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md`](../strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md)

## وحدات اختبار مقترحة (أسماء ملفات)

| الملف | الغرض |
|--------|--------|
| `test_lead_scoring.py` | قواعد النقاط والعتبات A/B/nurture/archive |
| `test_stage_transitions.py` | انتقالات الحالة المسموحة فقط |
| `test_approval_policy.py` | يفرض موافقة عند `requires_approval: true` |
| `test_claim_guard.py` | يمنع ادّعاءات بلا مصدر؛ يفرض `is_estimate` |
| `test_evidence_events.py` | يسجّل الحقول الإلزامية لكل حدث |
| `test_invoice_guard.py` | لا فاتورة بدون نطاق معتمد؛ لا تسليم بدون دفع |
| `test_support_classifier.py` | intent + risk → مسار صحيح |
| `test_knowledge_base.py` | إجابات KB مرتبطة بملفات حقيقية |
| `test_affiliate_commissions.py` | احتساب بعد `invoice_paid` فقط |
| `test_affiliate_compliance.py` | إفصاح، ممنوعات، ICP |
| `test_partner_referrals.py` | إسناد صفقة لشريك بدون ازدواجية ضارة |
| `test_agent_orchestrator.py` | تشغيل وكيل → policy + evidence |
| `test_no_build_warning.py` | قواعد «ما نبني» من `no_build_rules.yaml` |
| `test_proof_pack_generator.py` | أقسام القالب +_missing data + `is_estimate` |

## اختبارات قبول (عينة)

1. High-fit lead → `qualified_A` + عنصر موافقة  
2. Low-fit → nurture/archive  
3. Security claim بدون مصدر → محظور  
4. `invoice_send` بدون `scope_approved` → محظور  
5. تسجيل إيراد بدون إثبات دفع → محظور  
6. `affiliate_payout` بدون `invoice_paid` → محظور  
7. دعم منخفض المخاطر → إجابة KB  
8. دعم عالي المخاطر → تصعيد  
9. تشغيل وكيل → سجل مصادر + نتيجة سياسة

## تشغيل

استخدم نطاقاً ضيقاً أثناء البناء: `APP_ENV=test pytest tests/test_<module>.py -q`

المجموعة السريعة الأوسع: راجع [`AGENTS.md`](../../AGENTS.md).
