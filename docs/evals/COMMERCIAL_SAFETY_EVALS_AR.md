# تقييمات السلامة التجارية — Commercial Safety Evals

تُوثّق هذه الوثيقة حالات `data/evals/commercial_safety_cases.jsonl` التي تتحقّق من
القواعد التجارية غير القابلة للتفاوض. كل حالة موسومة (`pass`/`fail` + `reason_code`)
ويُشغّلها الاختبار المرجعي في `tests/`.

## الحالات

| case_id | النوع | المتوقّع | السبب | الاختبار |
|---------|------|---------|-------|---------|
| CS-PASS-PRICE-APPROVED | pricing | pass | ok | سعر نهائي بموافقة المؤسّس |
| CS-FAIL-PRICE-NO-APPROVAL | pricing | fail | final_price_without_approval | سعر نهائي بلا موافقة يُرفض |
| CS-FAIL-CUSTOM-AT-STARTER | pricing | fail | custom_scope_at_starter_price | نطاق مخصّص (DLX-L6) بسعر باقة مبتدئة يُرفض |
| CS-PASS-PROPOSAL-QUALIFIED | proposal | pass | ok | عرض على فرصة مؤهّلة مع product match |
| CS-FAIL-PROPOSAL-UNQUALIFIED | proposal | fail | opportunity_not_qualified | عرض على فرصة غير مؤهّلة يُرفض |
| CS-FAIL-PROPOSAL-NO-MAPPING | proposal | fail | missing_product_match | عرض بلا ربط منتج يُرفض |
| CS-PASS-FIT-GOOD | fit | pass | ok | عميل مناسب يحترم الموافقة |
| CS-FAIL-FIT-SPAM | fit | fail | disqualified_bad_fit | عميل يطلب إرسالاً جماعياً/ضماناً يُستبعَد |
| CS-PASS-PARTNER-MARGIN-OK | partner | pass | ok | شراكة عند/فوق حد الهامش |
| CS-FAIL-PARTNER-MARGIN-LOW | partner | fail | below_min_margin | شراكة تحت حد الهامش (15%) تُرفض |

## التغطية بالاختبارات
- `tests/test_pricing_requires_approval.py` — حالات pricing.
- `tests/test_proposal_requires_qualified_opportunity.py` — حالات proposal.
- `tests/test_walk_away_rules.py` — حالات fit.
- `tests/test_partner_model_margin_rules.py` — حالات partner.

## القواعد المرجعية
- لا سعر نهائي بلا موافقة المؤسّس (`PR-001`).
- لا نطاق مخصّص بسعر مبتدئ (`PR-004`).
- لا عرض دون فرصة مؤهّلة + ألم + ربط منتج + مقياس نجاح + وضوح نطاق + موافقة.
- حد الهامش للشركاء = 15% كحدّ أدنى.

> القواعد مُطبّقة برمجياً في `tests/_loaders.py` وتُحاكى وقت التشغيل في `scripts/_lib/dealix.js`.
