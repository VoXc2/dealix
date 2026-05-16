# غير قابل للتفاوض — The 11 Non-Negotiables

> المصدر الرسمي الوحيد. أي ملف آخر يذكر "غير قابل للتفاوض" يجب أن يحيل إلى هنا.
> Single source of truth. Enforced in code by `auto_client_acquisition/safe_send_gateway/doctrine.py`
> and by `tests/test_doctrine_guardrails.py`.

## الدور | Role

الحدود التي تبني الثقة وتمنع المخاطر التجارية والقانونية. لا يجوز تجاوزها — يُرفض الطلب
ويُقترح بديل آمن. These lines build trust and prevent commercial/legal risk. They are
never bypassed: refuse the request and propose a safe alternative.

## القائمة | The 11

| # | غير قابل للتفاوض | Non-negotiable | كود العقيدة / doctrine code |
|---|------------------|----------------|------------------------------|
| 1 | لا أنظمة scraping | No scraping systems | `no_scraping` |
| 2 | لا أتمتة واتساب باردة | No cold WhatsApp automation | `no_cold_whatsapp` |
| 3 | لا أتمتة LinkedIn | No LinkedIn automation | `no_linkedin_automation` |
| 4 | لا ادعاءات مزيّفة أو بلا مصدر | No fake / un-sourced claims | `no_fake_proof` |
| 5 | لا وعود مبيعات مضمونة | No guaranteed sales outcomes | `no_guaranteed_sales_claims` |
| 6 | لا بيانات شخصية في السجلات | No PII in logs | `no_pii_in_logs` |
| 7 | لا إجابة معرفية بلا مصدر | No source-less knowledge answers | `no_sourceless_answer` |
| 8 | لا إجراء خارجي بلا موافقة | No external action without approval | `external_action_requires_approval` |
| 9 | لا وكيل بلا هوية | No agent without identity | `no_agent_without_identity` |
| 10 | لا مشروع بلا Proof Pack | No project without a Proof Pack | `no_project_without_proof_pack` |
| 11 | لا مشروع بلا أصل رأسمالي | No project without a Capital Asset | `no_project_without_capital_asset` |

**امتداد تشغيلي للبند 8 | Operational extension of #8:** التواصل الجماعي الخارجي بدون
حوكمة وموافقة ممنوع (`no_bulk_outreach`).

## الإنفاذ | Enforcement

- **كود:** `safe_send_gateway/doctrine.py` — `enforce_doctrine_non_negotiables()` يرفع
  `ValueError` بتفاصيل ثنائية اللغة؛ الـrouters تترجمها إلى HTTP 403.
- **اختبارات:** `tests/test_doctrine_guardrails.py` — تغطّي الـ12 الكود.
- **القاعدة:** إذا خالف أي طلب أو عمل قيد التنفيذ بنداً من هذه القائمة → ارفض واقترح
  بديلاً آمناً. لا ارتجال حولها.

## روابط | Links

- [DEALIX_CONSTITUTION.md](DEALIX_CONSTITUTION.md)
- [WHAT_DEALIX_REFUSES.md](WHAT_DEALIX_REFUSES.md)
- [GOOD_REVENUE_BAD_REVENUE.md](GOOD_REVENUE_BAD_REVENUE.md)
