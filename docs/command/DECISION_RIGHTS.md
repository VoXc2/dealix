# Decision Rights — حقوق القرار

**المبدأ:** لا قرارات «سريعة» **خارج البوابات**. السرعة من **وضوح البوابات** لا من تجاوزها — حتى في فريق صغير، افصل المقاعد ذهنيًا.

## المصفوفة

| نوع القرار | مقعد المالك | البوابة |
|------------|-------------|---------|
| Sell service | CEO/Growth | Service Readiness |
| Accept project | CEO/Delivery | Project Acceptance |
| Use client data | Governance | Data Gate |
| Deliver output | QA/Governance | QA + Governance |
| Build feature | Product | Productization Gate |
| Offer retainer | CEO/CS | Proof + Client Health |
| Create BU | CEO/Strategy | Unit Maturity |
| Spin venture | Group Strategy | Venture Gate |
| Publish claim | Trust/Marketing | Proof Gate |

## الكود المرجعي

`auto_client_acquisition/command_os/decision_rights.py` — `DECISION_RIGHTS_ROWS` و`decision_right_for_key()`.

**صعود:** [`SOVEREIGN_COMMAND_SYSTEM.md`](SOVEREIGN_COMMAND_SYSTEM.md)
