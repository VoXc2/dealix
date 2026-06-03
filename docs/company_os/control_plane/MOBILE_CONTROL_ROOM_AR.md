# Dealix Mobile Control Room

## الهدف

غرفة تحكم تفتح من الجوال وتخليك تكلم مخ الشركة، تراجع الإنتاج، وتشغل أوامر بدون فتح Codespaces.

## رابط غرفة التحكم

https://web-production-380c3.up.railway.app/ar/control-room

## طريقة إرسال أمر للمخ من الجوال

1. افتح GitHub.
2. ادخل Dealix-sa/dealix.
3. افتح Actions.
4. اختر Brain Control Command.
5. اضغط Run workflow.
6. اكتب الأمر.
7. افتح Artifacts بعد التشغيل وشاهد الرد.

## أوامر مفيدة

- وش تشتغل عليه الشركة اليوم؟
- جهز خطة اليوم لتصريف P1 وفتح 3 مكالمات.
- راجع صفحات الموقع والعروض وحدد أهم 3 تحسينات تزيد التحويل.
- افحص الإنتاج والأمان والجاهزية.
- جهز مسودات رسائل warm outreach للمراجعة.

## تشغيل 24/7

أنشئ خدمة Railway داخلية:

- Name: company-brain
- Config file: railway.company-brain.toml
- Public networking: OFF

Variables:

AUTO_SEND_ENABLED=false
EXTERNAL_OUTREACH_ENABLED=false
AGENT_APPROVAL_MODE=required
COMPANY_BRAIN_INTERVAL_SECONDS=900

## قاعدة الأمان

AI drafts. Founder approves. Human sends.
