# Kill System — نظام الإيقاف

أقوى الشركات تعرف **ماذا توقف**.

## Kill Service

إشارات مثل: win rate منخفض · هامش منخفض · scope creep عالٍ · proof ضعيف · لا مسار retainer · مخاطر حوكمة عالية · تكرار منخفض — التفاصيل في [`../command/KILL_CRITERIA.md`](../command/KILL_CRITERIA.md).

## Kill Feature

إذا: لا يُعاد استخدامه · غير مربوط بالإيراد · يسبب عبء صيانة · **لا يقلل جهد التسليم** (حتى مع «توفير وقت» جزئي) — استخدم `kill_feature_recommended` مع `reduces_delivery_effort=False` عندما ينطبق.

## Kill Market / Channel

مشترون غير واضحين · ميزانية ضعيفة · بيانات خطرة جدًا · دورة مبيعات طويلة · لا مسار proof.

**الكود:** `enterprise_os/kill_system.py` → `command_os/kill_criteria.py`

**صعود:** [`SOVEREIGN_ENTERPRISE_ARCHITECTURE.md`](SOVEREIGN_ENTERPRISE_ARCHITECTURE.md)
