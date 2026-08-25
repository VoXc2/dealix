# GoDaddy DNS Swap Guide — dealix.me → Railway / دليل تبديل DNS
**EN + AR · Founder: ~10 minutes · Rollback included · Railway side already ACTIVE**

---

## ENGLISH — Step by step

**Before starting:** confirm in Railway → project **Dealix** → service `web` → Settings → Networking: both `dealix.me` and `www.dealix.me` show as ACTIVE (they already do — verified 2026-08-25). Click each domain; Railway displays the EXACT records it needs. Copy them exactly.

1. Log in to **GoDaddy** → My Products → DNS → manage **dealix.me**
2. **DELETE** these GitHub Pages records:
   - A record `@` → 185.199.108.153
   - A record `@` → 185.199.109.153
   - A record `@` → 185.199.110.153
   - A record `@` → 185.199.111.153
   - Any CNAME pointing apex/www at `<user>.github.io`
3. **ADD** the records Railway displays for `dealix.me` (typically an A record `@` → a Railway IP, and CNAME `www` → the shown target). Use Railway's values verbatim — do not guess.
4. Save. Propagation: usually 10–60 min (TTL dependent).

### Verify (after ~30 min)
```
curl -s -o /dev/null -w "%{http_code}\n" https://dealix.me/ar      # expect 200
curl -sI https://dealix.me | grep -i server                        # expect NOT github.com
bash scripts/post_redeploy_verify_dealix.py                        # full smoke
```

### ROLLBACK (instant)
Re-add the four GitHub A-records above → static site returns within minutes (it stays published on branch `pages-public`).

---

## العربية — خطوة بخطوة

**قبل البدء:** في Railway → مشروع Dealix → خدمة web → Settings → Networking: تأكّد أن النطاقين `dealix.me` و `www.dealix.me` يظهران ACTIVE (مفعّلان بالفعل — تم التحقق 2026-08-25). اضغط على كل نطاق وانسخ السجلات التي يعرضها Railway **حرفيًا**.

1. سجّل الدخول إلى **GoDaddy** → My Products → DNS → إدارة **dealix.me**
2. **احذف** سجلات GitHub Pages التالية:
   - A ‏`@` ← 185.199.108.153
   - A ‏`@` ← 185.199.109.153
   - A ‏`@` ← 185.199.110.153
   - A ‏`@` ← 185.199.111.153
   - وأي CNAME يشير الجذر أو www إلى `<user>.github.io`
3. **أضف** السجلات التي يعرضها Railway للنطاق `dealix.me` (عادةً A للجذر و CNAME لـwww بالقيم المعروضة). لا تخمّن القيم.
4. حفظ. الانتشار عادة 10–60 دقيقة.

### التحقق (بعد ~30 دقيقة)
```
curl -s -o /dev/null -w "%{http_code}\n" https://dealix.me/ar      # المتوقع 200
curl -sI https://dealix.me | grep -i server                        # ليس github.com
bash scripts/post_redeploy_verify_dealix.py
```

### التراجع فورًا
أعد إضافة سجلات GitHub الأربعة أعلاه — الموقع الثابت يبقى منشورًا على فرع `pages-public`.

### بعد نجاح الـcutover (خطوة أخيرة)
حوّل GitHub Pages إلى workflow build وأعد تشغيل deploy-pages مرة واحدة، ثم احذف فرع `pages-public`. الأمر جاهز في `docs/ops/PR_MERGE_ORDER_PACKET.md`.
