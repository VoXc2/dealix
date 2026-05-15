# العربية

## جاهزية الحوكمة — الطبقة الخامسة

Owner: مالك طبقة الحوكمة (Governance Platform Lead) — قسم الخصوصية والثقة

### الغرض

الطبقة 5 تضمن أن كل إجراء يقوم به الذكاء الاصطناعي محكوم وقابل للتدقيق ومتناسب مع مخاطره. كل إجراء يحمل تصنيف مخاطر، والإجراءات عالية المخاطر لا تُنفَّذ دون موافقة بشرية موثَّقة، وكل موافقة وكل سياسة مُسجَّلة ومُصدَّرة. الهدف: أن نُثبت للعميل ما فعله الذكاء الاصطناعي، ولماذا، ومن وافق عليه. تتماشى الطبقة مع دورة حياة NIST AI RMF.

### قائمة الجاهزية

- [x] كل إجراء مقترح يحمل تصنيف مخاطر A/R/S عبر `dealix/classifications/__init__.py`.
- [x] الإجراءات عالية المخاطر (A1+ أو R3 أو S3) لا تُنفَّذ دون موافقة موثَّقة.
- [x] كل موافقة تُسجَّل بهوية المراجع ووقته وسببه عبر `dealix/trust/audit.py`.
- [x] كل قاعدة سياسة لها مُعرّف وإصدار ومالك في `auto_client_acquisition/governance_os/policies/default_registry.yaml`.
- [x] محرّك السياسات fail-closed: المجهول يُحجب أو يُصعّد.
- [x] القواعد غير القابلة للتفاوض مفعّلة: `no_fake_proof`, `no_guaranteed_claims`, `no_scraping`, `no_linkedin_automation`, `no_cold_whatsapp`, `no_pii_in_logs`, `external_action_requires_approval`, `no_source_no_answer`.
- [x] الإجراءات الخارجية المواجِهة للعميل مسوّدة فقط (draft-only).
- [ ] جدول تدقيق إلحاقي مقسّم في PostgreSQL (مُخطَّط للمرحلة 2).
- [ ] التحقق الدوري من سلامة سلسلة قيود التدقيق (مُخطَّط).
- [ ] لوحة فروقات إصدارات السياسات (مُخطَّطة).

### المقاييس

- نسبة الإجراءات عالية المخاطر التي تطلّبت موافقة: 100% (هدف).
- نسبة الإجراءات الحاملة لتصنيف صريح: 100% (هدف).
- تغطية قيود التدقيق: 100% من الموافقات والإجراءات S2/S3.
- نسبة القواعد ذات المالك والإصدار: 100%.
- زمن تقييم السياسة: أقل من 50 مللي ثانية لكل إجراء.
- متوسط زمن البتّ في الموافقة.

### خطاطيف المراقبة

- قيود التدقيق المكتوبة عبر `dealix/trust/audit.py`، ومراياها في `core/logging.py`.
- تتبّع كل قرار سياسة وموافقة عبر `dealix/observability/otel.py`.
- التقاط الأخطاء عبر `dealix/observability/sentry.py`.
- تنبيه عند: فشل كتابة قيد تدقيق، اكتشاف فجوة سلسلة، ارتفاع نسبة التصنيف الافتراضي، تجاوز طلب A3 نصف مهلته.

### قواعد الحوكمة

- كل إجراء A1+ أو R3 أو S3 يمر عبر مسار الموافقة في `dealix/trust/approval.py`؛ لا تنفيذ آلي.
- الإجراءات المدرجة في `NEVER_AUTO_EXECUTE` تُرفع للموافقة دائماً.
- كل قاعدة سياسة لها مالك مسمّى وإصدار؛ لا قاعدة مجهولة المالك.
- لا تفويض ذاتي؛ المراجع لا يوافق على إجراء اقترحه.
- لا إرسال رسائل خارجية نيابة عن العميل دون موافقته الصريحة.
- لا بيانات شخصية خام في السجلات (`no_pii_in_logs`).

### إجراء التراجع

1. تحديد التغيير المسبّب للخلل: قاعدة، أو مصفوفة موافقات، أو منطق تصنيف.
2. استعادة الإصدار المستقر السابق من السجل أو الملف المعني عبر سجل الإصدارات.
3. التحقق من بقاء القواعد الحرجة مفعّلة: `external_action_requires_approval`, `no_pii_in_logs`.
4. إعادة تقييم الإجراءات والموافقات المعلّقة المتأثرة.
5. تسجيل التراجع كقيد تدقيق وإبلاغ مالك الطبقة.

### درجة الجاهزية الحالية

**الدرجة: 79 / 100 — تجريبي للعميل (Client Pilot).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

الفجوات التي تحدّ الدرجة: جدول التدقيق الإلحاقي في PostgreSQL والتحقق من سلامة السلسلة لم يُنفَّذا بعد؛ لوحة فروقات السياسات مُخطَّطة. هذه الفجوات تمنع بلوغ نطاق "جاهز للمؤسسات".

# English

## Governance Readiness — Layer 5

Owner: Governance Platform Lead — Privacy & Trust Plane

### Purpose

Layer 5 ensures every AI action is governed, auditable, and proportionate to its risk. Every action carries a risk classification, high-risk actions do not execute without a documented human approval, and every approval and every policy is logged and versioned. The goal: prove to a customer what the AI did, why, and who approved it. The layer aligns with the NIST AI RMF lifecycle.

### Readiness checklist

- [x] Every proposed action carries an A/R/S risk classification via `dealix/classifications/__init__.py`.
- [x] High-risk actions (A1+, R3, or S3) do not execute without a documented approval.
- [x] Every approval is logged with reviewer identity, time, and reason via `dealix/trust/audit.py`.
- [x] Every policy rule has an id, version, and owner in `auto_client_acquisition/governance_os/policies/default_registry.yaml`.
- [x] The Policy Engine is fail-closed: the unknown is blocked or escalated.
- [x] Non-negotiable rules are active: `no_fake_proof`, `no_guaranteed_claims`, `no_scraping`, `no_linkedin_automation`, `no_cold_whatsapp`, `no_pii_in_logs`, `external_action_requires_approval`, `no_source_no_answer`.
- [x] External, customer-facing actions are draft-only.
- [ ] Append-only, partitioned audit table in PostgreSQL (planned for Phase 2).
- [ ] Periodic verification of audit chain integrity (planned).
- [ ] Policy version diff dashboard (planned).

### Metrics

- Share of high-risk actions that required approval: 100% (target).
- Share of actions carrying an explicit classification: 100% (target).
- Audit entry coverage: 100% of approvals and S2/S3 actions.
- Share of rules with an owner and version: 100%.
- Policy evaluation time: under 50 ms per action.
- Mean time-to-decision for approvals.

### Observability hooks

- Audit entries written via `dealix/trust/audit.py`, mirrored in `core/logging.py`.
- Every policy decision and approval traced via `dealix/observability/otel.py`.
- Error capture via `dealix/observability/sentry.py`.
- Alert on: a failed audit write, a detected chain gap, a rising default-classification share, an A3 request crossing half its TTL.

### Governance rules

- Every A1+, R3, or S3 action passes through the approval path in `dealix/trust/approval.py`; no auto-execution.
- Actions on the `NEVER_AUTO_EXECUTE` list are always raised for approval.
- Every policy rule has a named owner and a version; no owner-less rule.
- No self-approval; a reviewer does not approve an action they proposed.
- No external messages are sent on a customer's behalf without their explicit approval.
- No raw personal data in logs (`no_pii_in_logs`).

### Rollback procedure

1. Identify the change that caused the fault: a rule, the approval matrix, or classification logic.
2. Restore the prior stable version of the relevant registry or file via the release log.
3. Verify critical rules remain active: `external_action_requires_approval`, `no_pii_in_logs`.
4. Re-evaluate affected pending actions and approvals.
5. Record the rollback as an audit entry and notify the layer owner.

### Current readiness score

**Score: 79 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.

Gaps capping the score: the append-only PostgreSQL audit table and chain-integrity verification are not yet implemented; the policy diff dashboard is planned. These gaps keep the layer below the enterprise-ready band.
