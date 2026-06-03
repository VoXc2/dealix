# غرفة قيادة المؤسس الفائقة — Founder Super Control Room (مواصفة)

> **الحالة:** مواصفة (Spec) — لا يوجد زر إرسال خارجي في v1 ما لم تكتمل كل البوابات.
> **المسار المقترح:** `/[locale]/ops/super-control` (مثال: `/ar/ops/super-control`).
> الواجهة الفعلية تُبنى فوق مكوّنات `src/components/ui/*` (tabs, card, table) وموجّهات `api/*-router.ts` القائمة.

---

## 1. الغاية
شاشة واحدة تجمع كل أنظمة Dealix لتعطي المؤسس **أمرًا واحدًا يوميًا** و**قرارًا حرجًا واحدًا**، مع القدرة على الاعتماد/الرفض/التعديل بضغطة — كل ذلك تحت سقف الموافقة-أولًا والتشغيل-التجريبي.

## 2. البطاقات العلوية (Top Cards)
1. أمر المؤسس اليوم (Today's Founder Command).
2. حالة إنتاج المسودات.
3. أهم إجراءات الموافقة.
4. الردود الإيجابية.
5. بطاقات واتساب (Action Cards).
6. طابور العروض.
7. تسليمات الدفع.
8. تسليمات (Sales→Delivery).
9. فرص التجديد/الترقية.
10. صحة النطاق (Domain health).
11. تنبيهات الخصوصية.
12. تنبيهات الأمن.
13. لقطة النقد/الـpipeline.
14. **قرار حرج واحد.**

## 3. التبويبات (Tabs)
GTM · Brand · Products · Sectors · Signals · Prospects · Drafts · Approvals · Sending · Replies · WhatsApp · Portal · Proposals · Proof Packs · Payments · Delivery · Renewals · Content · Press · Partners · Finance · Privacy · Security · Agents · Metrics · Risks.

> تبويبات GTM/Brand/Products/Sectors/Signals/Prospects/Content/Press/Partners تعرض مخرجات أساس Agent #1 (قراءة)، وتبويباتنا (WhatsApp/Portal/Proposals/Proof Packs/Payments/Delivery/Renewals) تعرض طوابيرنا.

## 4. الإجراءات المفضّلة (Preferred Actions)
`approve` · `reject` · `edit` · `copy` · `mark sent manually` · `move to nurture` · `do not contact` · `request human handoff` · `generate proposal` · `generate proof pack` · `prepare payment handoff`.

> **ممنوع في v1:** أي زر "إرسال خارجي" مباشر (واتساب/بريد/دفع) قبل اكتمال بوابات: موافقة موثّقة + تسليم بشري حيث يلزم + `send_enabled` مُفعّل بقرار صريح. البديل: `mark sent manually` بعد التنفيذ اليدوي.

## 5. مصادر البيانات لكل تبويب (للتنفيذ)
| التبويب | المصدر |
|---|---|
| Approvals | `company_os/governance/approval_queue.json` |
| Replies | مخرجات GTM + `data/whatsapp/sessions.jsonl` |
| WhatsApp | `data/whatsapp/action_cards.jsonl`, `reports/whatsapp/*` |
| Portal | `data/client_portal/*`, `reports/client_portal/*` |
| Proposals | `data/proposals/proposals.jsonl`, `reports/revenue_execution/PROPOSAL_QUEUE.md` |
| Proof Packs | `data/proof_packs/*`, `reports/revenue_execution/PROOF_PACK_QUEUE.md` |
| Payments | `data/payments/*`, `reports/revenue_execution/PAYMENT_HANDOFF_QUEUE.md` |
| Delivery | `data/delivery/*`, `reports/delivery/*` |
| Renewals | `data/renewals/*`, `reports/renewal/*` |
| Privacy/Security | `docs/privacy/*`, `docs/security/*`, فحص الأمن |
| Metrics | `reports/whatsapp/WHATSAPP_METRICS.md` |
| Risks | `reports/delivery/*RISK*`, `company_os/war_room/RISKS.md` |

## 6. الإيقاع
- يومي: `reports/founder/DAILY_SUPER_COMMAND.md`.
- أسبوعي: `reports/founder/WEEKLY_BOARD_REVIEW.md`.
- سجل: `reports/founder/DECISION_LOG.md`.

---
*المرجع الحاكم: `AGENTS.md` · الواجهة: `docs/founder_control/CONTROL_ROOM_UI_SPEC_AR.md`.*
