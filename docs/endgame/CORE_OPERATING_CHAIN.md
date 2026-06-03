# Dealix Core Operating Chain

السلسلة المرجعية:

`Signal → Capability Diagnostic → Productized Sprint → Governed Delivery → QA → Proof Pack → Retainer → Capital Asset → Product Module → Business Unit → Standard → Academy/Partner → Venture → Holding Company`

**قاعدة:** أي قفزة بدون المرحلة السابقة **خطرة** (مثلاً لا Partner Program بدون QA · لا SaaS بدون client pull · لا Enterprise بدون Trust Pack).

---

## Core OS — خرافة `auto_client_acquisition/`

مرجع الريبو: [`../architecture/CORE_OS.md`](../architecture/CORE_OS.md) · [`../architecture/MODULAR_MONOLITH.md`](../architecture/MODULAR_MONOLITH.md).

**قوانين تقنية:**

- لا استدعاء AI خارج `llm_gateway`.
- لا مخرج حساس خارج `governance_os`.
- لا إغلاق مشروع بدون `reporting_os` / Proof Pack.
- لا تكرار مسجّل بدون `capital_os` / productization ledger.
- لا قرار استراتيجي ناضج بدون `intelligence_os`.

**الكود:** `endgame_os/operating_chain.py` — `CORE_OPERATING_CHAIN` · `can_enter_step` · `chain_complete_through`.

**صعود:** [`ENDGAME_OPERATING_DOCTRINE.md`](ENDGAME_OPERATING_DOCTRINE.md)
