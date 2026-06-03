# يوم الإطلاق التجاري — اتصالات المؤسس

**قاعدة:** لا إرسال خارجي تلقائي — مسودات + موافقة فقط.

## منشور LinkedIn (بعد المراجعة)

> معظم الفرق تملك أدوات؛ القليل يملك **سلسلة أدلة** من الإشارة إلى القرار.
>
> Dealix = **نظام تشغيل إيرادات محكوم**:
> - تشخيص مجاني → Sprint من **499 ر.س**
> - Proof Pack خلال 7 أيام — بلا واتساب بارد
>
> https://dealix.me/ar/dealix-diagnostic

## 3 لمسات War Room

1. P0 واحد من `/ar/ops/war-room`
2. مسودة لمسة دافئة — موافقة قبل الإرسال
3. سجّل `demo_booked` أو `payment_received` في evidence CSV (شركة حقيقية)

## مساء اليوم

```powershell
py -3 scripts/founder_evening_evidence.py
powershell -File scripts/verify_dealix_commercial_go_live.ps1
```
