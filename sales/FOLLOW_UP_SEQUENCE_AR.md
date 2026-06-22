# خطة المتابعة — Follow-up Sequence (Dealix)

## الهدف
متابعة منظمة لكل prospect تمر بـ مرحلة الاهتمام حتى الإغلاق بـ استخدام AI drafts + approval queue.

## المادة (Material)

### النموذج المستخدم
1. **رسائل Outreach** (email, WhatsApp, LinkedIn) — مخصصة بالعربية والإنجليزية
2. **تقارير Daily CEO** — لمراجعة أداء المتابعات
3. **Command Room HTML** — لمراقبة pipeline والقرارات

## المتابعة المتسلسلة

### Stage 1: Contacted (اليوم 0)
- **Action**: إرسال Email / WhatsApp (initial)
- **Goal**: طلب Diagnostic مجاني
- **Timing**: خلال 1-2 ساعة من الاستفسار
- **Draft**: "Outreach draft was generated on [date] — awaiting approval"

### Stage 2: Follow-up (اليوم 3)
- **Action**: Email / WhatsApp (followup)
- **Goal**: تذكير + ذكر قيمة
- **Timing**: 3 أيام بعد initial
- **Draft**: "تم توليد Follow-up draft [date] — awaiting approval"

### Stage 3: Value Add (اليوم 7)
- **Action**: Email + (case study / success story)
- **Goal**: بناء الثقة بالإثبات
- **Timing**: 7 أيام بعد initial
- **Draft**: "قصة نجاح من قطاع مشابه — awaiting approval"

### Stage 4: Final (اليوم 14)
- **Action**: Email + WhatsApp
- **Goal**: Last chance + scarcity
- **Timing**: 14 يوم بعد initial
- **Draft**: "آخر فرصة / Last chance sequence — awaiting approval"

### Stage 5: Overdue / Lost (اليوم 21)
- **Action**: إيقاف المتابعات
- **Goal**: تركيز على prospects الأخرى
- **Draft**: "Auto-stop — no response in 21 days"

## التحقق (Checkpoints)

- [ ] يوم 0: Initial sent (approved + signed)
- [ ] يوم 3: Follow-up draft reviewed
- [ ] يوم 7: Value add draft approved
- [ ] يوم 14: Final call sent
- [ ] يوم 21: Auto-stop marked
- [ ] أسبوعياً: CEO Daily Report reviewed

## السياسة (Policy)
- **لا إرسال آلي** بدون manual approval
- **كل draft يحمل [AI]** tag
- **OUTBOUND_MODE = draft_only** (default)
- **لا follow-up beyond 14 days** بدون explicit consent
- **لا unsolicited messages** — only response to inquiry or prior consent
