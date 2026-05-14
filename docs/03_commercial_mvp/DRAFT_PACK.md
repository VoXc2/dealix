# مسودات التواصل (Draft Pack) — Revenue Intelligence Sprint

Dealix تُجهّز **مسودات فقط** (بريد، اتصال، متابعة، لينكدإن نصي) دون أي إرسال تلقائي.

## مبدأ التشغيل

- **Dealix تُحضّر — الإنسان يوافق — لا إرسال خارجي افتراضيًا.**
- واتساب: مسودة فقط عند `explicit_consent` أو `warm_intro`؛ لا واتساب بارد ولا أتمتة.
- لينكدإن: نص **draft-only**؛ لا أتمتة ولا رسائل جماعية عبر المنصة من Dealix.

## الكود

- `auto_client_acquisition/revenue_os/draft_pack.py` — `build_revenue_draft_pack`
- `auto_client_acquisition/revenue_os/followup_plan.py` — خطة متابعة بشرية (D+3 / D+7 / D+14)

## مؤشر النجاح

كل حزمة مسودات تمر ببوابة العقيدة (`enforce_doctrine_non_negotiables`) وتُسجَّل كـ`DRAFT_ONLY` على القنوات الخارجية في مسار الـ API.
