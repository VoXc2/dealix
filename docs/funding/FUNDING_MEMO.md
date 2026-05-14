# مذكرة التمويل — Funding Memo
## Dealix — Wave 19 — مذكرة المؤسس للمحادثة قبل البذرة

> **سطر واحد · One line.** Dealix طبقة عمليات ذكاء اصطناعي محوكمة (Governed AI Ops) للسوق المتوسط الخليجي المنظَّم، تبدأ من خدمات B2B السعودية، وتتوسّع بقيادة الشركاء. هذه المذكرة لبدء محادثة، ليست لإغلاق جولة.
>
> Dealix is a governed AI operations layer for the regulated GCC mid-market, starting with Saudi B2B services and expanding partner-led. This memo opens a conversation; it does not close a round.

---

## ١. ما هو Dealix · What Dealix is

**AR.** Dealix منصة عمليات تشغيلية تربط ثلاث طبقات: مصدر بيانات موثّق (Source Passport)، طبقة قرار محوكمة بموافقة بشرية، وطبقة إثبات قابلة للتدقيق. كل ارتباط مغلق يودع أصلاً رأسمالياً قابلاً لإعادة الاستخدام في الارتباط التالي. السلّم التجاري ثلاث درجات فقط:

- **التشخيص الاستراتيجي (مجاني، يوم عمل واحد)** — تدقيق وضع PDPL/NDMO + خطة ٩٠ يوم.
- **ريتينر العمليات المحوكمة (٤٬٩٩٩ ر.س / شهر، ٣ أشهر حد أدنى)** — تقرير قيمة شهري + Proof Pack + طابور موافقات يومي.
- **سبرنت ذكاء الإيرادات (٢٥٬٠٠٠ ر.س / ٣٠ يوم)** — دمج ٣ مصادر + نموذج تنبؤ + حزمة حوكمة قابلة للتدقيق.

**EN.** Dealix is an operating platform that binds three layers: a sourced-data layer (Source Passport), a governed decision layer with human approval, and an auditable proof layer. Every closed engagement deposits a reusable Capital Asset that the next engagement starts ahead of. The commercial ladder is three rungs only, defined in `auto_client_acquisition/service_catalog/registry.py`: Strategic Diagnostic (free, 1 working day), Governed Ops Retainer (4,999 SAR / month, 3-month minimum), Revenue Intelligence Sprint (25,000 SAR / 30 days). Source: [`docs/THE_DEALIX_PROMISE.md`](../THE_DEALIX_PROMISE.md) and [`docs/sales-kit/INVESTOR_ONE_PAGER.md`](../sales-kit/INVESTOR_ONE_PAGER.md).

---

## ٢. لماذا الآن · Why now

**AR.** تجتمع أربع قوى في ٢٠٢٦: PDPL في تطبيقها التشغيلي، NDMO يطلب مساراً مرئياً للبيانات، رؤية ٢٠٣٠ تضغط نحو التوطين التشغيلي، والاستثمار في البنية التحتية للذكاء الاصطناعي الخليجي (HUMAIN، MGX، استراتيجيات وطنية في قطر والبحرين والكويت وعُمان) يسبق وجود معيار تشغيلي علني. الفجوة ليست في الموديل، بل في طبقة الحوكمة التشغيلية بين الموديل والمشتري المنظَّم. هذه الفجوة "تنظيم لين" — يُسمح بالكثير، ولا يوجد مرجع واحد لما يُعدّ مقبولاً.

**EN.** Four forces converge in 2026: PDPL is now operational, NDMO requires visible data lineage, Vision 2030 pushes operational localization, and GCC AI infrastructure investment is well ahead of any public operational standard. The gap is not the model; it is the governance operations layer between the model and the regulated buyer. The regime is "soft regulation" — much is permitted, and no single reference exists for what counts as acceptable. See [`docs/funding/WHY_NOW_GCC_AI_OPS.md`](./WHY_NOW_GCC_AI_OPS.md).

---

## ٣. ما هو مبني وقابل للتحقق · What is built and verifiable

**AR.** المنصة قيد التشغيل، والمراجعون يستطيعون التحقق دون الاتصال بنا:

- `GET /api/v1/dealix-promise` — ١١ التزاماً + اختبارات CI مرتبطة بكل التزام (CAP-001).
- `GET /api/v1/doctrine` — العقيدة العامة + خريطة الضوابط (CAP-003).
- `GET /api/v1/commercial-map` — السلّم التجاري الكامل من العرض إلى الإثبات (CAP-005).
- `GET /api/v1/founder/command-center` — لوحة المؤسس: النشر + العقيدة + السلّم + الإيرادات (CAP-014).
- `GET /api/v1/capital-assets/public` — الأصول الرأسمالية العامة CAP-001…CAP-015.

**EN.** The platform is in production. Reviewers can verify without contacting us via the endpoints above. Each endpoint is backed by tests cited in [`docs/funding/CAPITAL_ASSET_TRACTION.md`](./CAPITAL_ASSET_TRACTION.md). The 11 commitments in [`docs/THE_DEALIX_PROMISE.md`](../THE_DEALIX_PROMISE.md) are not marketing copy; they are CI tests that fail the build if violated.

---

## ٤. ما لم يُبنَ بعد · What is not yet built

**AR.** الفاتورة الأولى لا تزال أمامنا. الإيراد المتكرر لم يبدأ التراكم. تكاليف اكتساب العميل غير مقيسة بعد كمية لأن المؤسس يدير القناة يدوياً. فريق التسليم لم يُوظَّف، والتوظيف مشروط بالإيراد، لا بالتمويل.

**EN.** Invoice #1 is still ahead. Recurring revenue has not begun to compound. Customer acquisition cost is not yet quantified because the founder runs the channel manually. The delivery team is not hired; hiring is gated on revenue, not on funding. See [`docs/funding/FIRST_3_HIRES.md`](./FIRST_3_HIRES.md).

---

## ٥. الفريق · The team

**AR.** مؤسس فردي. القاعدة التشغيلية: ٤ ساعات بيع / يوم، ٢ ساعة تسليم / يوم، ٠ ساعة كود — Claude يكتب الكود. التوظيف يبدأ عند ٥٠٬٠٠٠ ر.س ARR (مهندس عمليات AI)، ثم ١٠٠٬٠٠٠ ر.س ARR (مشغل تسليم/RevOps)، ثم ٢٥٠٬٠٠٠ ر.س ARR أو أول قطاع منظَّم موقَّع (مشغل شراكات خليجي). التفاصيل في [`FIRST_3_HIRES.md`](./FIRST_3_HIRES.md).

**EN.** Solo founder. Operating cadence: 4h sell, 2h deliver, 0h code per day — Claude writes the code. Hiring is revenue-gated, not funding-gated: ≥ 50K SAR ARR for Hire #1, ≥ 100K SAR ARR for Hire #2, ≥ 250K SAR ARR or first regulated-sector signed for Hire #3.

---

## ٦. الطلب · The ask

**AR.** هذه محادثة قبل البذرة، لا ورقة شروط. ما نطلبه:

1. تعريف بشريك مرسٍ واحد (Big 4 خليجي، أو معالج مرخّص من SAMA، أو CISO في خدمات B2B سعودية).
2. مستشار استراتيجي واحد بسجل تنفيذي مُثبَت في عمليات منظَّمة سعودية أو خليجية.
3. مراجعة لاحقة عندما تصل الفاتورة #٢ — تقدير، وليس وعداً.

**EN.** This is a pre-seed conversation, not a term sheet. The ask: one anchor partner intro (Big 4 GCC practice, SAMA-licensed processor, or Saudi B2B services CISO), one strategic advisor with executed track record in regulated Saudi or GCC operations, and a revisit when Invoice #2 lands — an estimate, not a promise.

---

## مراجع · References

- [`docs/THE_DEALIX_PROMISE.md`](../THE_DEALIX_PROMISE.md) — ١١ التزاماً.
- [`docs/sales-kit/INVESTOR_ONE_PAGER.md`](../sales-kit/INVESTOR_ONE_PAGER.md) — صفحة واحدة.
- [`docs/funding/USE_OF_FUNDS.md`](./USE_OF_FUNDS.md) — السيناريوهان.
- [`docs/funding/CAPITAL_ASSET_TRACTION.md`](./CAPITAL_ASSET_TRACTION.md) — الجرّ بالأصول.
- [`docs/funding/INVESTOR_QA.md`](./INVESTOR_QA.md) — ١٢ سؤالاً صعباً.

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
