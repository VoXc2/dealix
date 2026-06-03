# مصفوفة الثقة والأمن — ربط استخبارات السوق بالمنتج

**آخر تحديث:** 2026-05-18

---

## مصفوفة التحكم

| تهديد / قلق سوق | ضابط Dealix | دليل | وثيقة |
|-----------------|-------------|------|--------|
| واتساب بارد | `NO_COLD_WHATSAPP` doctrine | tests doctrine | GOVERNED_AI |
| LinkedIn auto | `no_linkedin_auto` | AGENTS.md | GOVERNED_AI |
| Gmail خارجي | approval queue | `/ops/approvals` | digest |
| PII في logs | redaction middleware | http_stack | PDPL_LEGAL |
| upsell مبكر | anti-waste | revenue-os API | packages |
| أرقام وهمية | KPI import only | kpi yaml | METRICS |
| نقل بيانات | DPA + sub-processors | landing | CLOUD_CROSS_BORDER |
| خرق | breach runbook | pdpl.py | PDPL_LEGAL |
| تسويق تحت L4 | anti-waste check | API | governance gates |
| fake proof | evidence levels | Decision Passport | PROOF_STACK |

---

## مستويات أدلة (L0–L5) — تطبيق مبيعات

| مستوى | معنى | مسموح في المحتوى | مسموح في عرض سعر |
|-------|------|------------------|------------------|
| L0 | فرضية | لا | لا |
| L1 | انطباع | لا حملة | لا |
| L2 | ملاحظة داخلية | لا عام | بحذر |
| L3 | مصدر واحد | case draft | diagnostic |
| L4 | مصدران+ | LinkedIn | pilot |
| L5 | مدقّق | case study | growth |

---

## بوابات immutable (8)

من `dealix_founder_daily_brief.py` — لا تعطّل في الإنتاج:

`no_live_send` · `no_live_charge` · `no_cold_whatsapp` · `no_linkedin_auto` · `no_scraping` · `no_fake_proof` · `no_fake_revenue` · `no_blast`

---

## ربط API للتحقق السريع

```bash
curl -s http://localhost:8000/api/v1/decision-passport/evidence-levels -H "X-Admin-API-Key: $DEALIX_ADMIN_API_KEY"
curl -s -X POST http://localhost:8000/api/v1/revenue-os/anti-waste/check \
  -H "Content-Type: application/json" -H "X-Admin-API-Key: $DEALIX_ADMIN_API_KEY" \
  -d '{"proposed_action":"cold_whatsapp_blast","evidence_level":"L1"}'
```

---

## ربط

- [PROCUREMENT_FAQ](MARKET_INTELLIGENCE_PROCUREMENT_FAQ_AR.md)
- [../empire/TRUST_LAYER.md](../empire/TRUST_LAYER.md)
- [COMPLIANCE_CERTIFICATIONS](../legal/COMPLIANCE_CERTIFICATIONS.md)
