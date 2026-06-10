# AEO Content Calendar — Answer Engine Optimization

**الهدف:** عندما يُسأل ChatGPT/Google «كيف أثبت ماذا حدث بعد الحملة؟» — Dealix مرجع.

**المرحلة:** 4 · **هيكل كل صفحة:** تعريف → متى تحتاجه → خطوات → قالب/CTA → Risk Score أو Sample Proof Pack.

**CTA موحّد:** Risk Score مجاني · [Sample Proof Pack](sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md)

---

## جدول النشر (12 أسبوعاً — ابدأ بالأولوية)

| أسبوع | slug مقترح | عنوان (AR) | سؤال AEO | أصل Sales Kit |
|-------|------------|--------------|----------|---------------|
| 1 | `post-lead-revenue-ops` | ما هو Post-Lead Revenue Ops؟ | What is Post-Lead Revenue Ops? | [dealix_onepager.md](../../sales-kit/dealix_onepager.md) |
| 2 | `what-is-proof-pack` | ما هو Proof Pack؟ | What is a Proof Pack? | [PROOF_PACK_TEMPLATE.md](../../delivery/PROOF_PACK_TEMPLATE.md) |
| 3 | `audit-lead-follow-up` | كيف تراجع متابعة الـ leads؟ | How to audit lead follow-up? | Discovery §7 في Scale System |
| 4 | `ai-approval-sales` | سياسة موافقة AI للمبيعات | AI approval policy for sales teams | [dealix_security_faq.md](../../sales-kit/dealix_security_faq.md) |
| 5 | `saudi-agency-follow-up-checklist` | قائمة متابعة leads للوكالات السعودية | Saudi agency lead follow-up checklist | Motion A scope |
| 6 | `no-cold-whatsapp-policy` | سياسة عدم الواتساب البارد | No cold WhatsApp growth policy | Governance gates |
| 7 | `crm-vs-revenue-ops` | CRM مقابل Revenue Ops | CRM vs Revenue Ops | objection `crm_exists` |
| 8 | `agency-proof-for-clients` | كيف تثبت الوكالة ما بعد الحملة؟ | How agencies prove post-campaign | Sample Proof Pack |
| 9 | `soaen-standard` | معيار SOAEN | Dealix SOAEN standard | Scale System §4 |
| 10 | `10-lead-audit` | لماذا نبدأ بـ 10 leads؟ | Why start with 10 leads only | objection `price_high` |
| 11 | `govern-ai-before-scale` | حوكمة AI قبل التوسع | Govern AI actions before scale | objection `internal_ai` |
| 12 | `revenue-leakage-after-ads` | أين يضيع الإيراد بعد الإعلانات؟ | Where revenue leaks after ads | [dealix_blog_post_1.md](../../sales-kit/dealix_blog_post_1.md) |

---

## قالب صفحة (انسخ لكل slug)

```markdown
# [العنوان AR]

## التعريف
[فقرة واحدة — جملة واضحة للمقتطفات]

## متى تحتاجه
- [نقطة 1–3]

## خطوات عملية
1. ...
2. ...

## قالب مجاني
[رابط Sample Proof أو checklist]

## CTA
- Risk Score · Sample Proof Pack · ديمو 10 دقائق

## Trust
No cold WhatsApp. Human approval. No fake proof.
```

---

## ربط Objection Engine

كل مقال مرتبط بـ [objection_engine_registry.yaml](objection_engine_registry.yaml) — عند `objection_received` أنشئ `content_asset` بنفس slug.

---

## تنفيذ Frontend (لاحقاً)

- مسار مقترح: `/[locale]/learn/[slug]`  
- حتى التنفيذ: انشر كـ `docs/commercial/operations/aeo_drafts/` أو LinkedIn longform من [dealix_content_calendar.md](../../sales-kit/dealix_content_calendar.md).
