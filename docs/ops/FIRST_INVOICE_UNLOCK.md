# First Invoice Unlock — ما الذي يتغيّر مع الفاتورة رقم ١
# Internal Ops Runbook — Wave 18 Founder Command Center

> **Audience / الجمهور:** Founder + ops lead only / المؤسس وقائد العمليات فقط.
> **Trigger / المحفّز:** Moyasar webhook confirms first paid invoice / تأكيد ويبهوك Moyasar لأول فاتورة مدفوعة.
> **Status / الحالة:** Active runbook — read before flipping the Moyasar live cutover flag.

---

## لماذا توجد هذه الوثيقة — Why this doc exists

### العربية

الفاتورة رقم ١ هي وحدة العمل التي تُقاس عليها خطة التفعيل التجاري لمدة ٩٠ يومًا بالكامل. قبل وصولها، كل التزام بالكود هو تكلفة — رواتب، استضافة، اشتراكات، وقت مؤسس. بعد وصولها، تبدأ حلقة تسجيل Capital Asset، ويصبح سطح PDF لـ Trust Pack أثرًا حقيقيًا (وليس قالبًا)، ويبدأ مجدوِل التجديد في `renewal_scheduler` في العدّ. هذه الوثيقة تصف بدقة ما يجب أن يكون صحيحًا قبل الفاتورة، وما يُطلَق تلقائيًا بعدها، وما لا يُطلَق أبدًا دون موافقة المؤسس.

### English

Invoice #1 is the unit of work the entire 90-day commercial activation plan is sized against. Until it lands, every commit is cost — payroll, hosting, subscriptions, founder time. After it lands, the Capital Asset registration loop begins, the Trust Pack PDF surface becomes a real artifact (not a template), and the renewal scheduler in `renewal_scheduler` starts ticking. This doc specifies exactly what must be true before the invoice, what fires automatically after it, and what never fires without founder approval.

---

## القائمة البوّابية قبل الفاتورة — Pre-invoice gating checklist

### العربية

لا تُولَّد أي فاتورة قبل أن تكون البنود التالية صحيحة جميعها. لا توجد استثناءات. أي تجاوز يُسجَّل كحدث Friction Log عالي الخطورة:

- **عميل مؤهَّل في CRM** — مرحلة "Qualified" أو أعلى، مع سجل اجتماع تأهيل.
- **عرض موقَّع في `data/proposals/`** — PDF موقَّع رقميًا، اسم الملف يطابق معرّف الارتباط.
- **Source Passport** — لكل مصدر بيانات في نطاق العمل، موثَّق ومحفوظ.
- **موافقة المؤسس مُسجَّلة** — في `decision_passport_log`، بختم زمني.
- **علم القطع الحي لـ Moyasar مُفعَّل** — عبر `scripts/moyasar_live_cutover.py`.
- **فحص ZATCA الأولي أخضر** — `scripts/zatca_preflight.py` يعيد كود خروج ٠.

إذا فشل أي بند، الفاتورة لا تُولَّد. النظام يرفض الإصدار، لا يحذّر فقط.

### English

No invoice is generated before all the following are true. No exceptions. Any override is logged as a high-severity Friction Log event:

- **Qualified lead in CRM** — stage "Qualified" or higher, with a qualification meeting record.
- **Signed proposal in `data/proposals/`** — digitally signed PDF, filename matching the engagement ID.
- **Source Passport** — per data source in scope, documented and stored.
- **Founder approval logged** — in `decision_passport_log` with a timestamp.
- **Moyasar live cutover flag flipped** — via `scripts/moyasar_live_cutover.py`.
- **ZATCA preflight green** — `scripts/zatca_preflight.py` returns exit code 0.

If any item fails, the invoice is not generated. The system refuses issuance — it does not just warn.

---

## سلسلة الفتح — The unlock cascade

### العربية

عند تأكيد ويبهوك Moyasar للدفع، تُطلَق الإجراءات الثمانية التالية بالترتيب. الإخفاق في أي خطوة يُوقف السلسلة ويستدعي تنبيه فوري:

1. **تسجيل Capital Asset عبر `capital_os.add_asset`** — إلزامي قبل بدء أي عمل تسليم. لا أصل = لا ارتباط. المرجع: `auto_client_acquisition/capital_os/capital_ledger.py`.
2. **توليد Trust Pack PDF تلقائيًا** — يُضاف إلى طابور التوليد، يحوي Promise + Source Passport + Decision Passport الافتتاحي.
3. **تفعيل مجدوِل الريتينر** — في `auto_client_acquisition/payment_ops/renewal_scheduler.py`، يبدأ العدّ من تاريخ الفاتورة.
4. **إصدار handle بوّابة العميل** — رابط دخول فريد، صلاحيات محدّدة بنطاق الارتباط فقط.
5. **إنشاء سير عمل Proof Pack** — `auto_client_acquisition/proof_os/proof_pack.py` يفتح حاوية أدلة فارغة.
6. **حدث Friction Log — معلَم تدقيق** — تسجيل "First invoice cleared" مع وقت الويبهوك ومعرّف الفاتورة.
7. **إشعار المؤسس** — بريد إلكتروني + مسوّدة WhatsApp فقط (لا إرسال مباشر، طبقًا للبند ٤).
8. **إعادة حساب وتيرة ARR في `/api/v1/founder/command-center`** — يحدِّث القيم العامة دون الكشف عن هوية العميل.

كل خطوة تُسجَّل في friction log حتى لو نجحت — للتدقيق اللاحق.

### English

When the Moyasar webhook confirms payment, the following eight actions fire in order. Failure at any step halts the chain and triggers an immediate alert:

1. **Capital Asset registration via `capital_os.add_asset`** — mandatory before any delivery work begins. No asset = no engagement. Reference: `auto_client_acquisition/capital_os/capital_ledger.py`.
2. **Trust Pack PDF auto-generation queued** — added to the generation queue, contains Promise + Source Passport + opening Decision Passport.
3. **Retainer scheduler activated** — in `auto_client_acquisition/payment_ops/renewal_scheduler.py`, counter starts from invoice date.
4. **Customer Portal handle issued** — unique access link, scoped strictly to the engagement.
5. **Proof Pack workflow instantiated** — `auto_client_acquisition/proof_os/proof_pack.py` opens an empty evidence container.
6. **Friction Log audit milestone event** — logs "First invoice cleared" with webhook timestamp and invoice ID.
7. **Founder notification** — email plus WhatsApp draft only (no live send, per non-negotiable #4).
8. **ARR pacing recompute in `/api/v1/founder/command-center`** — updates public metrics without exposing customer identity.

Every step is logged to friction log even on success — for downstream audit.

---

## ما لا نفعله تلقائيًا — What we do NOT do automatically

### العربية

السلسلة أعلاه داخلية. لا يُطلَق أي إجراء خارجي تلقائيًا. تحديدًا:

- **لا تغريدات احتفال** — أي منشور علني يحتاج موافقة المؤسس مكتوبة.
- **لا نشر دراسة حالة** — يتطلب موافقة العميل الموقَّعة، حتى لو كانت مجهّلة الهوية.
- **لا تسلسل ترقية** — لا رسائل بيع تلقائية، لا "هل تريد ترقية إلى الحزمة التالية".
- **لا تحديث عدّادات عامة** — عدّاد العملاء، عدّاد الإيراد، أي رقم على landing page لا يتحرّك تلقائيًا.

كل إجراء خارجي يبقى محكومًا بالبند ٨ من Promise. المرجع: `docs/THE_DEALIX_PROMISE.md`.

### English

The cascade above is internal. No external action fires automatically. Specifically:

- **No celebration tweets** — any public post requires written founder approval.
- **No case study publication** — requires signed customer consent, even when anonymized.
- **No upsell sequence** — no automated sales messages, no "want to upgrade?" nudges.
- **No public counter updates** — customer counter, revenue counter, any landing-page number does not move automatically.

Every external action stays gated under Promise non-negotiable #8. Reference: `docs/THE_DEALIX_PROMISE.md`.

---

## قالب مراجعة الفاتورة الأولى — First-invoice retrospective template

### العربية

بعد إغلاق التسليم، يُكتب ملف `docs/case-studies/case_004_first_invoice.md` (تسمية موحَّدة). يلتقط الحقول التالية:

- **القطاع** (مجهّل: مثلًا "خدمات هندسية، الرياض").
- **زمن الإغلاق** (من أول لمسة إلى الفاتورة، بالأيام).
- **أحداث Friction Log** المسجَّلة خلال الارتباط.
- **Capital Asset المُسجَّل** (المعرّف، الفئة).
- **هل تجاوزت درجة الإثبات ٧٠/١٠٠** في Proof Pack النهائي.
- **هل وافق العميل على ريتينر متابعة** (نعم/لا/مؤجّل).
- **درس مؤسسي واحد** يستحق التدوين في عقيدة التسليم.

### English

After delivery closes, write `docs/case-studies/case_004_first_invoice.md` (standard naming). Capture these fields:

- **Sector** (anonymized, e.g. "Engineering services, Riyadh").
- **Time to close** (first touch to invoice, in days).
- **Friction Log events** logged during the engagement.
- **Capital Asset registered** (ID, category).
- **Did the proof score clear 70/100** in the final Proof Pack.
- **Did the customer agree to a follow-up retainer** (yes/no/deferred).
- **One institutional lesson** worth writing into delivery doctrine.

---

## مراجعة اليوم السابع بعد الفاتورة — Day-7 post-invoice review

### العربية

اجتماع ثابت مدته ٣٠ دقيقة في اليوم السابع بعد إغلاق التسليم. ثلاثة أسئلة فقط:

- هل سلَّمنا وفق التزام KPI المنصوص في `registry.py` لهذا العرض؟
- هل التزمنا بـ SLA ٢٤ ساعة على كل بند في Approval Queue؟
- هل وقع أي حدث Friction Log عالي الخطورة، وما خطة العلاج؟

النتيجة تُسجَّل في `docs/ops/POST_LAUNCH_SCORECARD.md`.

### English

Fixed 30-minute meeting on Day 7 after delivery closes. Three questions only:

- Did we deliver to the KPI commitment stated in `registry.py` for this offering?
- Did we meet the 24h SLA on every Approval Queue item?
- Did any high-severity Friction Log event occur, and what is the remediation plan?

Result is logged in `docs/ops/POST_LAUNCH_SCORECARD.md`.

---

## مراجع متشابكة — Cross-links

- `scripts/moyasar_live_cutover.py`
- `scripts/zatca_preflight.py`
- `auto_client_acquisition/capital_os/capital_ledger.py`
- `auto_client_acquisition/proof_os/proof_pack.py`
- `auto_client_acquisition/payment_ops/renewal_scheduler.py`
- `docs/THE_DEALIX_PROMISE.md`
- `docs/sales-kit/PRICING_REFRAME_2026Q2.md`
- `docs/sales-kit/INVESTOR_ONE_PAGER.md`
- `docs/ops/POST_LAUNCH_SCORECARD.md`

---

> **Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**
> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
