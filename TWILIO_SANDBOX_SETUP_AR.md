# ربط Twilio Sandbox بـ Dealix Webhook — خطوة واحدة فقط

## الحالة الحالية

- ✅ Webhook شغال محلياً على port 8001
- ✅ Cloudflare Tunnel يعطي URL عام: `https://pat-pmc-pushing-mechanism.trycloudflare.com`
- ✅ Groq (llama-3.3-70b) مربوط ويرد بالعربي
- ✅ SQLite يحفظ كل lead + كل رسالة
- ⚠️ ربط Twilio Sandbox بالـ webhook **يدوي** (Twilio لا يسمح بذلك عبر API)

## الخطوة المطلوبة منك

1. افتح: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. اضغط **"Sandbox settings"**
3. في حقل **"When a message comes in"** الصق:
   ```
   https://pat-pmc-pushing-mechanism.trycloudflare.com/webhook/whatsapp
   ```
4. الطريقة: **POST**
5. احفظ

## اختبار مباشر

بعد الحفظ، أرسل رسالة واتساب من `+966597788539` إلى `+14155238886`:
- مثال: "مرحبا"
- خلال ثواني يرد Groq بالعربي باسم Dealix
- كل الرسائل محفوظة في `/home/user/workspace/dealix-clean/dealix_leads.db`

## لعرض Leads المجمعة

```bash
curl https://pat-pmc-pushing-mechanism.trycloudflare.com/leads
```

أو محلياً:
```bash
sqlite3 /home/user/workspace/dealix-clean/dealix_leads.db "SELECT * FROM leads;"
sqlite3 /home/user/workspace/dealix-clean/dealix_leads.db "SELECT phone, direction, substr(body,1,60), created_at FROM messages ORDER BY id DESC LIMIT 20;"
```

## ملاحظة مهمة

الـ Cloudflare Tunnel **مجاني ومؤقت** — الرابط يتغير كل مرة تعيد تشغيله. للإنتاج نحتاج:
- دومين مدفوع (dealix.sa أو dealix.com)
- Hetzner VPS
- Cloudflare Tunnel دائم (أو Nginx عادي)

هذه الخطوات في `LAUNCH_GUIDE_AR.md`.
