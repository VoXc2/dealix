# Compliance-by-Design — Dealix

> **Dealix لا تضيف الامتثال في النهاية. تُبنى بحيث يكون الامتثال والإثبات والتدقيق جزءًا من التشغيل نفسه.**

## لماذا الآن؟

السوق يتحرك من «اعتماد AI» إلى **تشغيل AI محكوم**. استخدام واسع خارج إشراف IT (shadow AI) مع شعور محدود بالثقة في الإدارة — مرجع سياقي: [TechRadar — Lenovo / unmanaged AI and organizational control](https://www.techradar.com/pro/organizations-need-to-stop-workarounds-and-regain-control-report-finds-many-firms-dont-know-what-their-workers-are-sharing-with-ai-tools).

الحوكمة تنتقل من وثائق فقط إلى **telemetry وقرارات وقت تشغيل** — [arXiv:2604.04749 — AI Trust OS](https://arxiv.org/abs/2604.04749).

## موقف Dealix

```text
Compliance-by-design
Governance-by-runtime
Proof-by-default
Audit-ready
```

## مبادئ Compliance-by-Design

1. **No invisible AI** — كل تشغيل مسجّل.  
2. **No unknown data** — كل مصدر له Source Passport.  
3. **No unowned agent** — owner + purpose + autonomy.  
4. **No unsupported claim** — proof أو إزالة.  
5. **No external action without approval** — إرسال/تواصل/تعديل خارجي بموافقة.  
6. **No compliance theater** — قرارات وقت تشغيل + audit trail، لا سياسة ورقية فقط.

الاتجاه البحثي: امتثال كطبقة تشغيل مستمرة تعتمد على observability — [arXiv:2604.04749](https://arxiv.org/abs/2604.04749).

## خريطة الوثائق

| ملف | موضوع |
|-----|--------|
| [TRUST_OPERATIONS_MODEL.md](TRUST_OPERATIONS_MODEL.md) | Discover → Improve |
| [COMPLIANCE_ARCHITECTURE.md](COMPLIANCE_ARCHITECTURE.md) | مسار كل مخرج |
| [SOURCE_PASSPORT_V2.md](SOURCE_PASSPORT_V2.md) | جواز المصدر |
| [AI_AGENT_COMPLIANCE.md](AI_AGENT_COMPLIANCE.md) | Registry + Card |
| [TRUST_ARTIFACTS.md](TRUST_ARTIFACTS.md) | أدلة الثقة |
| [COMPLIANCE_REPORT.md](COMPLIANCE_REPORT.md) | تقرير مشروع/retainer |
| [CLAIM_COMPLIANCE.md](CLAIM_COMPLIANCE.md) | ادعاءات (حالات) + `claim_safety` في الكود |
| [INCIDENT_RESPONSE_V2.md](INCIDENT_RESPONSE_V2.md) | حوادث |
| [REGULATORY_READINESS.md](REGULATORY_READINESS.md) | جاهزية تنظيمية |
| [SAUDI_COMPLIANCE_LAYER.md](SAUDI_COMPLIANCE_LAYER.md) | PDPL وعربي |
| [COMPLIANCE_METRICS.md](COMPLIANCE_METRICS.md) | عتبات قياس |
| [COMPLIANCE_DASHBOARD.md](COMPLIANCE_DASHBOARD.md) | لوحة |
| [COMPLIANCE_TO_SALES_ADVANTAGE.md](COMPLIANCE_TO_SALES_ADVANTAGE.md) | ميزة مبيعات |

## الكود

`auto_client_acquisition/compliance_trust_os/` — يشمل: `policy_registry` · `source_passport_v2` · `pii_classifier` · `allowed_use_checker` · `claim_compliance` · **`claim_safety`** · **`channel_policy`** · `approval_engine` · `audit_trail` · `incident_response` · `compliance_report` · `compliance_dashboard`.

## صعود

[`../risk_resilience/STRATEGIC_RISK_COMPLIANCE_RESILIENCE.md`](../risk_resilience/STRATEGIC_RISK_COMPLIANCE_RESILIENCE.md) · [`../trust/ENTERPRISE_TRUST_PACK.md`](../trust/ENTERPRISE_TRUST_PACK.md) · [`../board_decision_system/AGENT_DECISION_GOVERNANCE.md`](../board_decision_system/AGENT_DECISION_GOVERNANCE.md)

## الخلاصة

> **Dealix تفوز عندما لا يضطر العميل أن يسأل “هل هذا آمن؟” لأن النظام نفسه يثبت الأمان: بالمصادر، الموافقات، السجلات، الـProof، والحدود قبل أي توسع.**
