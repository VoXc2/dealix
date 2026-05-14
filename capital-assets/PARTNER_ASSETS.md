# أصول الشراكات — Partner Assets

> النوع: `partner_asset` | آخر مراجعة: 2026-05-14
> مصدر: [`capital_asset_registry.py`](../auto_client_acquisition/capital_os/capital_asset_registry.py)

أصول الشراكات هي الأدوات التي تُحوِّل علاقة شراكة محتملة من "مكالمة استكشاف" إلى "ورقة شروط موقّعة". أصل واحد مُسجَّل: CAP-009 (طقم تواصل الشريك الراسي).

Partner assets are the tools that convert a candidate partnership from a "discovery call" into a "signed term sheet". One registered: CAP-009 (anchor partner outreach kit).

---

## CAP-009 — Anchor Partner Outreach Kit

**Maturity:** live | **Proof level:** doc-backed | **Public:** False
**Files:**
- `docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md`
- `docs/40_partners/PARTNER_COVENANT.md`
- `scripts/seed_anchor_partner_pipeline.py`

### الدور الاستراتيجي (AR)
ثلاث مسوّدات تواصل ثنائية اللغة لثلاثة أرشيتايبات شريك + أجندة اجتماع ٦٠ دقيقة + ورقة شروط لمشاركة الإيرادات. كل ما يحتاجه المؤسس ليفتح محادثة شراكة جدّية في يوم واحد، بدون تخمين.

### Strategic role (EN)
Three bilingual outreach drafts for three partner archetypes + a 60-minute meeting agenda + a revenue-share term sheet. Everything the founder needs to open a serious partnership conversation in one day, without improvisation.

### Buyer relevance
استشارات Big 4 (Deloitte/PwC/KPMG/EY)، معالج مرخّص من SAMA، VC سعودي.

### استخدام تجاري (AR)
- تفعيل قناة الشريك.
- قالب عقد لمشاركة الإيرادات.

### Commercial use (EN)
- Partner channel activation.
- Rev-share contract template.

### متى تُظهره (AR)
**ليس** علناً. **ليس** قبل تأهيل الشريك. هذا أصل داخلي (`public=False`) يُفتح في تسلسل صارم:

1. تأهيل الشريك عبر مصفوفة الأرشيتايب (هل هو Big 4؟ معالج SAMA؟ VC؟).
2. إيميل تواصل أوّلي يأخذ المسوّدة المناسبة من الطقم.
3. اجتماع ٦٠ دقيقة بالأجندة الموحّدة — لا اجتماعات بدون أجندة.
4. ورقة شروط مشاركة الإيرادات تُرسل خلال ٤٨ ساعة من الاجتماع.

### When to surface (EN)
**Not** publicly. **Not** before partner qualification. This is an internal asset (`public=False`) opened in a strict sequence:

1. Qualify the partner against the archetype matrix (Big 4? SAMA-licensed? VC?).
2. Initial outreach email using the matching draft from the kit.
3. 60-minute meeting on the canonical agenda — no agenda-less meetings.
4. Rev-share term sheet sent within 48 hours of the meeting.

### الخطوط الحمراء المرتبطة (AR)
- `no_cold_whatsapp` — الطقم لا يحتوي على قوالب WhatsApp بارد. كل تواصل عبر قنوات مهنية مُعلَنة (إيميل، مقدّمة موثّقة).
- `no_external_action_without_approval` — أي إرسال نيابة عن Dealix يمرّ بسجل تدقيق (CAP-008).

### Linked non-negotiables (EN)
- `no_cold_whatsapp` — the kit contains no cold WhatsApp templates. All outreach goes through declared professional channels (email, documented warm introduction).
- `no_external_action_without_approval` — any send on behalf of Dealix passes through the audit chain (CAP-008).

---

## ميثاق الشريك (AR) / Partner covenant (EN)

- **AR:** ملف `PARTNER_COVENANT.md` هو وثيقة من صفحتين توضّح ماذا تَعِد Dealix به الشريك (تطبيق مرجعي، عقيدة منشورة، أصول رأسمالية قابلة للتدقيق)، وماذا يَعِد به الشريك Dealix (قناة، عناية واجبة، توزيع جغرافي). الميثاق ليس عقداً — هو مرساة قيمية تسبق العقد.
- **EN:** `PARTNER_COVENANT.md` is a two-page document stating what Dealix promises the partner (reference implementation, published doctrine, auditable capital assets) and what the partner promises Dealix (channel, due diligence rigour, geographic distribution). The covenant is not a contract — it is the values anchor that precedes the contract.

---

## أرشيتايب الشريك الراسي (AR) / Anchor archetypes (EN)

| Archetype | Distribution role | First conversation |
|---|---|---|
| Big 4 (Deloitte/PwC/KPMG/EY) | استشارات تنظيمية | عبر شريك Big 4 GCC practice |
| SAMA-licensed processor | تشغيل تنظيمي | عبر مقدّمة من بنك أو شركة دفع |
| Saudi VC (Sanabil/STV/Wa'ed) | إشارة سوق + رأس مال | عبر مستشار محفظة |

---

*Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.*
