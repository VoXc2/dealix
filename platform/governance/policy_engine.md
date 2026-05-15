# العربية

**Owner:** مالك طبقة الحوكمة (Governance Platform Lead).

## الغرض

محرّك السياسات هو البوابة التي يمرّ عبرها كل إجراء مقترح قبل التنفيذ. يأخذ إجراءً وسياقه ويُعيد قراراً واحداً من ثلاثة: `allow` (مسموح) أو `require_approval` (يتطلب موافقة) أو `block` (محجوب). لا قرار خارج هذه الثلاثة، ولا إجراء يتجاوز المحرّك.

## القواعد القابلة للإصدار

كل قاعدة ملف مستقل في `auto_client_acquisition/governance_os/rules/`، ولكل قاعدة مُعرّف ودرجة خطورة ومالك وإصدار. السجل الافتراضي `auto_client_acquisition/governance_os/policies/default_registry.yaml` يحدد القواعد المفعّلة. القواعد الأساسية المفعّلة:

- `no_fake_proof` — يمنع أي ادعاء إثبات بلا مصدر موثّق.
- `no_guaranteed_claims` — يمنع وعود نتائج مضمونة؛ يستبدلها بـ "فرص مُثبتة بأدلة".
- `no_scraping` — يمنع وصف أو تنفيذ استخراج بيانات غير مرخّص.
- `no_linkedin_automation` — يمنع أتمتة LinkedIn.
- `no_cold_whatsapp` — يمنع رسائل واتساب باردة غير مطلوبة.
- `no_pii_in_logs` — يمنع كتابة بيانات شخصية في السجلات.
- `external_action_requires_approval` — كل إجراء خارجي غير موافق عليه يُعاد بقرار `require_approval`.
- `no_source_no_answer` — لا إجابة موجّهة للعميل بلا مصدر.

## آلية التقييم

1. يُحمّل المحرّك القواعد عبر `auto_client_acquisition/governance_os/rules/loader.py`.
2. يستدعي `policy_check.py` كل قاعدة بترتيب درجة الخطورة (critical أولاً).
3. أول قاعدة تُعيد `block` تُنهي التقييم فوراً (fail-closed).
4. إذا لم يُحجب الإجراء لكنه خارجي أو R3، تُعاد `require_approval`.
5. `runtime_decision.py` يجمع النتيجة النهائية ويُمررها لمحرّك التدقيق.

المبدأ الحاكم: **fail-closed** — أي إجراء غير مصنّف أو غير معروف يُعامل بأمان افتراضي (A2/R2/S2) ولا يُنفَّذ آلياً.

## قائمة الجاهزية

- [x] كل قاعدة ملف مستقل بمُعرّف وإصدار ومالك.
- [x] السجل الافتراضي يحدد القواعد المفعّلة صراحةً.
- [x] التقييم fail-closed: المجهول يُحجب أو يُصعّد.
- [ ] لوحة فروقات إصدارات القواعد (مُخطَّطة).

## المقاييس

- نسبة الإجراءات التي مرّت عبر المحرّك: 100% (هدف).
- زمن تقييم السياسة: أقل من 50 مللي ثانية لكل إجراء.
- عدد القواعد المفعّلة مقابل المتوفرة في `default_registry.yaml`.

## إجراء التراجع

1. تحديد إصدار السجل المستقر السابق.
2. إعادة `default_registry.yaml` للإصدار السابق عبر سجل الإصدارات.
3. التحقق من أن القواعد الحرجة (`external_action_requires_approval`) لا تزال مفعّلة.
4. تسجيل التراجع كقيد تدقيق.

انظر أيضاً: `platform/governance/architecture.md` و`governance/policies/ai_usage_policy.md`.

---

# English

**Owner:** Governance Platform Lead.

## Purpose

The Policy Engine is the gate every proposed action passes before execution. It takes an action and its context and returns exactly one of three decisions: `allow`, `require_approval`, or `block`. No decision exists outside these three, and no action bypasses the engine.

## Versioned rules

Each rule is a standalone file in `auto_client_acquisition/governance_os/rules/`, and every rule has an id, severity, owner, and version. The default registry `auto_client_acquisition/governance_os/policies/default_registry.yaml` defines which rules are active. The core active rules:

- `no_fake_proof` — blocks any proof claim without a documented source.
- `no_guaranteed_claims` — blocks guaranteed-results promises; replaces them with "evidenced opportunities".
- `no_scraping` — blocks describing or performing unauthorized data extraction.
- `no_linkedin_automation` — blocks LinkedIn automation.
- `no_cold_whatsapp` — blocks unsolicited cold WhatsApp messages.
- `no_pii_in_logs` — blocks writing personal data to logs.
- `external_action_requires_approval` — any unapproved external action returns `require_approval`.
- `no_source_no_answer` — no customer-facing answer without a source.

## Evaluation mechanism

1. The engine loads rules via `auto_client_acquisition/governance_os/rules/loader.py`.
2. `policy_check.py` invokes each rule in severity order (critical first).
3. The first rule returning `block` ends evaluation immediately (fail-closed).
4. If the action is not blocked but is external or R3, `require_approval` is returned.
5. `runtime_decision.py` assembles the final result and passes it to the Audit Engine.

The governing principle is **fail-closed**: any unclassified or unknown action is treated with safe defaults (A2/R2/S2) and never auto-executes.

## Readiness checklist

- [x] Each rule is a standalone file with an id, version, and owner.
- [x] The default registry explicitly declares active rules.
- [x] Evaluation is fail-closed: the unknown is blocked or escalated.
- [ ] Rule version diff dashboard (planned).

## Metrics

- Share of actions passing through the engine: 100% (target).
- Policy evaluation time: under 50 ms per action.
- Active rules vs available rules in `default_registry.yaml`.

## Rollback procedure

1. Identify the previous stable registry version.
2. Restore `default_registry.yaml` to the prior version via the release log.
3. Verify critical rules (`external_action_requires_approval`) remain active.
4. Record the rollback as an audit entry.

See also: `platform/governance/architecture.md` and `governance/policies/ai_usage_policy.md`.
