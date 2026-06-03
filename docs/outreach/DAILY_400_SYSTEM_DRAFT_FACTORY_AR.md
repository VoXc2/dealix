# مصنع المسودات اليومي (400 مسودة/يوم)

يحوّل المصنع حزم الحسابات إلى **مسودات بريد** شخصية مبنية على النظام والاحتياج
والقطاع — لا قوالب عامة، ولا إرسال آلي.

## المخرجات

- `data/outreach/email_drafts.jsonl` — حتى 400 مسودة.
- `data/outreach/top_100_approval_queue.jsonl` — أفضل 100 للاعتماد.
- `reports/outreach/TOP_100_SYSTEM_APPROVAL_QUEUE.md` — تقرير للمؤسس.

## بنية المسودة

كل مسودة تحمل: `core_system`, `sector_specific_sprint`, `cta`,
`client_need_card_ref`, و`approval_required: true` دائمًا، و`status: draft`.

## بوابة جودة البريد

تفشل المسودة إذا:

- لا بطاقة احتياج (`client_need_card_ref`).
- لا نظام جوهري صالح.
- لا سبرنت قطاعي.
- لا CTA.
- وجود وعد مضمون («نضمن/مضمون/100%»).
- موضوع زائف يبدأ بـ `Re:`/`Fwd:`/`رد:`.
- الألم مكتوب كحقيقة بلا سؤال/تخفيف (نشترط وجود «؟»).
- الشركة في قائمة الكبح.

التطبيق: `scripts/checks/check_email_quality_gate.py` +
`docs/quality/EMAIL_QUALITY_GATE_AR.md`.

## القاعدة الذهبية

```
الوكيل يكتب مسودات فقط. المؤسس يعتمد. النظام يسجّل. لا إرسال آلي.
```
