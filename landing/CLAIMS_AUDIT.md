# Landing v2 — Claims Audit

> Cross-check of every claim on the landing against `marketing/CLAIMS_REGISTRY_AR.md`.
> Generated: 2026-04-18

---

## 1. Claims used (mapped to APPROVED ids)

| Location | Claim text (AR, excerpted) | Claim ID | Status |
|---|---|---|---|
| Hero title | «نظام تشغيل مؤسسي للإيراد والصفقات والشراكات والاعتمادات والتنفيذ» | **CLM-001** | ✅ Approved |
| Announce bar + pricing note | «في مرحلة البايلوت — نبحث عن ٥ شركاء تأسيسيين» | **CLM-012** | ✅ Approved |
| Pillar 1 | «نرفع سرعة القرار — الموافقات التي تستغرق أسابيع تُنجز في ساعات» | **CLM-009** | ✅ Approved |
| Pillar 1 bullet | «تقرير audit جاهز بضغطة واحدة» | **CLM-014** | ✅ Approved |
| Pillar 2 | «نرفع جودة التنفيذ — كل صفقة وشراكة وعقد موثّق بمسار تدقيق كامل» | **CLM-010** | ✅ Approved |
| Pillar 2 bullet | «كل قرار يمر في مسار موثّق — لا موافقة بدون سجل رسمي» | **CLM-003** | ✅ Approved |
| Pillar 3 | «نخفض الفوضى والمخاطر — نُلغي تشتت الموافقات بين Excel وWhatsApp وSlack» | **CLM-011** | ✅ Approved |
| Pillar 3 bullet | «يعمل فوق أنظمتكم الحالية — لا يستبدل CRM أو ERP» | **CLM-007** | ✅ Approved |
| Sectors (banking) | «مُراعٍ لمتطلبات SAMA و SDAIA و NCA و ZATCA في التصميم» | **CLM-008** | ✅ Approved (softened from "معتمد" → "مُراعٍ في التصميم") |
| How it works callout | «API-first — يتكامل مع بنيتكم الحالية، لا يستلزم استبدال الأنظمة» | **CLM-015** | ✅ Approved |
| Trust — PDPL card | «مصمّم للتوافق مع PDPL — حقوق الوصول والحذف والتنقل مدمجة في النظام» | **CLM-006** | ✅ Approved |
| Trust — SAMA/SDAIA/NCA card | «مُراعٍ لمتطلبات الجهات الرقابية الخليجية في التصميم» | **CLM-008** | ✅ Approved |
| Trust — encryption card | «نتبع ممارسات أمنية موثّقة — تشفير في الراحة وفي النقل» | **CLM-005** | ✅ Approved |
| Trust — hash chain card | «audit trail بـ hash chain — قيد التطوير ضمن مرحلة Pilot» | **CLM-004** | ✅ Approved (explicitly labeled "قيد التطوير" per note in registry) |
| FAQ CRM | «Dealix لا يحل محل CRM» | **CLM-007** | ✅ Approved |
| FAQ integration | «API-first … أيام لا أشهر» | **CLM-015** | ✅ Approved |
| FAQ PDPL | «PDPL مدمج في التصميم» | **CLM-006** | ✅ Approved |
| FAQ references | «في مرحلة Pilot … شروط الشريك التأسيسي» | **CLM-012** | ✅ Approved |
| FAQ SAMA | «لا ندّعي اعتماد SAMA — مُصمَّمون وفق متطلباتها» | **CLM-008** | ✅ Approved |

All `data-claim-id` attributes render as invisible HTML metadata.

---

## 2. Claims softened (moved from Forbidden → Approved alternative)

| Original (if we had written it) | Replaced by | Forbidden ID | Approved ID used |
|---|---|---|---|
| "SOC 2 certified" / "ISO 27001 معتمدون" | "نتبع ممارسات أمنية موثّقة — شهادات رسمية في خارطة الطريق" | CLM-F001, CLM-F002 | CLM-005 |
| "bank-grade security" | "تشفير AES-256 في الراحة و TLS 1.3 في النقل" | CLM-F008 | CLM-005 |
| "GDPR certified" / "GDPR compliant" | "مصمّم للتوافق مع PDPL" + explicit disclaimer in trust-note | CLM-F004 | CLM-006 |
| "AI-powered" (generic) | "مدعوم بـ Groq llama-3.3-70b + OpenAI كنسخة احتياطية" (in FAQ answers) | CLM-F014 | — |
| "fully autonomous" | "AI يُنظّم والإنسان يوافق — human-in-the-loop" | CLM-F016 | — |
| "100% accurate" / "بدون أخطاء" | "دقة عالية مع آلية مراجعة بشرية" | CLM-F006, CLM-F011 | — |
| "SAMA معتمد / شركاء SAMA" | "مُصمَّم وفق متطلبات SAMA — اعتماد رسمي في خارطة الطريق" | CLM-F018 | CLM-008 |
| "industry-leading" / "الأفضل في فئته" | Removed — replaced with specific feature claims | CLM-F013 | — |
| "enterprise-grade" (vague) | "workflow موافقة متعددة المستويات" | CLM-F010 | — |
| "10x revenue" / "يُضاعف الإيرادات" | "يُحسّن رؤية الإيراد ويُقلّص تسرب الهامش" | CLM-F015 | — |

---

## 3. NEEDS-PROOF claims — deliberately **NOT used** on the landing

These claims require Pilot evidence before going public. None appear on the landing page:

- CLM-101 «يُقلّص وقت الموافقات بنسبة X%»
- CLM-102 «يرفع معدل إغلاق الصفقات بنسبة X%»
- CLM-103 «يُقلّص تسرب الهامش من الخصومات بـ X ر.س/شهر»
- CLM-104 «يُنبّه 100% من عقود التجديد قبل 90 يوم»
- CLM-105 «يُوفّر X ساعة أسبوعياً من إعداد التقارير اليدوية»
- CLM-106 «معدل استجابة WhatsApp >30%»
- CLM-107 «تحوّل الموافقات من أسابيع إلى ساعات في بيئة العميل الحقيقية»
- CLM-108 «نسبة خطأ AI <5%»

**Note:** Pillar 1 uses CLM-009 "نرفع سرعة القرار — الموافقات التي تستغرق أسابيع تُنجز في ساعات مع مسار واضح" which is Approved (design-column claim, not outcome-percentage claim). CLM-107 (which is the outcome version with pilot proof) is explicitly **not** used.

---

## 4. Honest placeholders

- **No fake customer logos** — replaced with 5 dashed "[شريك N]" placeholders labelled "نبحث عن أول ٥ شركاء تأسيسيين".
- **Trust bar** shows real counts from `SERVICE_READINESS_MATRIX.yaml` (0 live · 8 in-dev · 24 roadmap).
- **Status page** (`/status.html`) exposes full per-service readiness — this is Tier-1 differentiation.
- **Announce bar** states the product phase explicitly.
- **Pricing** shows tier names only; no fake prices. Every tier CTA = "تواصل معنا".
- **FAQ** answers are direct from `OBJECTION_HANDLING_AR.md` OBJ-01…OBJ-18 with softened claims per registry.

---

## 5. Machine-checkable metadata

Every copy block on the landing that carries a registry claim has a `data-claim-id="CLM-XXX"` attribute on the containing element. Automated audit:

```bash
grep -oE 'data-claim-id="CLM-[0-9]+"' landing/index.html | sort -u
# Expected output: CLM-001, CLM-003, CLM-004, CLM-005, CLM-006, CLM-007,
#                  CLM-008, CLM-009, CLM-010, CLM-011, CLM-012, CLM-014, CLM-015
```
