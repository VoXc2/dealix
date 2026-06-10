# Kill Criteria — معايير الإيقاف

القوة ليست في البناء فقط — **في الإيقاف** عندما لا يلتئم النموذج.

## إيقاف خدمة

إن تحققت إشارات مثل: معدل فوز منخفض، هامش منخفض، **scope creep** عالٍ، proof ضعيف، **لا مسار retainer**، مخاطر حوكمة عالية، تكرار منخفض — راجع `kill_service_recommended` في الكود للعتبات الافتراضية.

## إيقاف feature

إن لم يُعاد استخدامه، أو لا يوفّر وقتًا، أو غير مربوط بالإيراد، أو يسبب **عبء صيانة** — انظر `kill_feature_recommended`.

## إيقاف سوق/قناة

مشترون غير واضحون، بيانات **خطرة جدًا**، ميزانية ضعيفة، دورة مبيعات طويلة جدًا، **لا مسار proof** — انظر `kill_market_recommended`.

## الكود

`auto_client_acquisition/command_os/kill_criteria.py`

**صعود:** [`SOVEREIGN_COMMAND_SYSTEM.md`](SOVEREIGN_COMMAND_SYSTEM.md)
