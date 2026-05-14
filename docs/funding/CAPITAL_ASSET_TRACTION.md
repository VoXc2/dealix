# جرّ الأصول الرأسمالية — Capital Asset Traction
## أَظهِر، لا تَدَّعِ — Show, don't tell

---

## ١. الفرضية · The premise

**AR.** المستثمر الذي يَطلب أدلة لا يَكتفي بشرائح. هذا الملف يَعرض الجرّ كأصول قابلة للتحقق: كل أصل له معرّف (CAP-XXX)، ومسار ملف، وحالة، ومستوى إثبات. الأصول المُسجَّلة في `auto_client_acquisition/capital_os/capital_asset_registry.py` وقابلة للقراءة عَبْر `GET /api/v1/capital-assets/public` للأصول العامّة.

**EN.** An evidence-first investor does not stop at slides. This doc presents traction as verifiable assets. Each asset has an ID (CAP-XXX), a file path, a maturity, and a proof level. The registry is the single source of truth and the public subset is readable via `GET /api/v1/capital-assets/public`.

---

## ٢. الأصول العامّة · Public assets

**AR.** هذه الأصول قابلة للتحقق دون الاتصال بنا:

| المعرّف | الاسم | النوع | الإثبات |
|---|---|---|---|
| CAP-001 | Dealix Promise API | trust | test-backed |
| CAP-002 | The Dealix Promise (Manifesto) | doctrine | doc-backed |
| CAP-003 | Open Doctrine Framework | doctrine | doc-backed |
| CAP-004 | 3-Offer Commercial Ladder | sales | test-backed |
| CAP-005 | Commercial Map API | sales | test-backed |
| CAP-012 | GCC Standardization Pack | standard | test-backed |
| CAP-015 | GCC Market Intel Public API | market | test-backed |

**EN.** These seven assets are verifiable without contacting us. Five are test-backed (the validator enforces that the cited file paths exist and the tests pass in CI). Two are doc-backed (canonical bilingual manifesto + open framework). The mapping from each asset to its file paths is in `capital_asset_registry.py`.

---

## ٣. الأصول الداخلية · Internal-facing assets

**AR.** أصول التشغيل الداخلي — تُكشَف للشركاء والمستثمرين عند المحادثة، لا للعموم:

| المعرّف | الاسم | النوع | الإثبات |
|---|---|---|---|
| CAP-006 | Proof Pack Assembler | proof | test-backed |
| CAP-007 | Trust Pack PDF Renderer | trust | code-backed |
| CAP-008 | Audit Chain + Evidence Control Plane | trust | code-backed |
| CAP-009 | Anchor Partner Outreach Kit | partner | doc-backed |
| CAP-010 | Investor One-Pager + Funding Memo | investor | doc-backed |
| CAP-011 | First 3 Hires + Hiring Scorecards | hiring | doc-backed |
| CAP-013 | First Invoice Unlock Runbook | revenue_ops | doc-backed |
| CAP-014 | Founder Command Center | product | test-backed |

**EN.** Eight internal-facing assets. CAP-006 and CAP-014 are test-backed (Proof Pack required + Founder Command Center endpoint tests). CAP-007 and CAP-008 are code-backed (live in production, used internally, not exposed publicly because they carry per-engagement data). The rest are doc-backed playbooks. Each asset cites real file paths; the validator script `scripts/validate_capital_assets.py` enforces path existence.

---

## ٤. ما تَعنيه مستويات الإثبات · What proof levels mean

**AR.** ثلاثة مستويات صريحة:

- **test-backed.** الأصل يَملك اختبار CI واحد على الأقل يَفشل البناء عند الإخلال.
- **code-backed.** الأصل يَملك كود إنتاج، لكن لا اختبار CI واحد يَفشل بشكل صريح (الإثبات في الكود وليس في الاختبار).
- **doc-backed.** الأصل وثيقة عقيدة أو دليل تشغيل، لا كود إنتاج. الإثبات في النَصّ.

نَفرّق بين الثلاثة لأن "موَثَّق" ليس "مُختبَر" وليس "مُشغَّل". الادّعاء يَطابق الواقع.

**EN.** Three explicit levels. Test-backed means a CI test fails the build on violation. Code-backed means production code exists but no single CI test is the explicit gate (proof is in the code, not the test). Doc-backed means doctrine or playbook, not production code. We distinguish them because "documented" is not "tested" and "tested" is not "operated at scale". The claim matches the reality.

---

## ٥. حالة النضج · Maturity status

**AR.** ١٣ من ١٥ أصلاً بحالة `live`. أصلان بحالة `draft`:

- CAP-010 — Investor One-Pager + Funding Memo (هذا الملف وأخواته، قيد المراجعة).
- CAP-011 — First 3 Hires + Scorecards (مكتمل، لكن لم يَنتقِل بعد إلى تنفيذ).

نُسرد الـ draft علناً لأن إخفاءه يَخرق الالتزام #٤ (لا ادعاء بلا مصدر).

**EN.** Thirteen of fifteen assets are `live`. Two are `draft`: CAP-010 (this memo and siblings, under review) and CAP-011 (First 3 Hires + Scorecards — complete but not yet executed). We name them as `draft` publicly because hiding draft state would violate commitment #4 (no unsourced claims). Source: `auto_client_acquisition/capital_os/capital_asset_registry.py` line-by-line.

---

## ٦. ما لا نَدّعيه هنا · What we do not claim here

**AR.** لا نَدّعي أن الأصول وحدها تَصنع إيرادات. الأصول هي بنية تحتية للإيراد، لا الإيراد ذاته. الفاتورة #١ لا تَزال أمامنا، ونُسرد ذلك صراحة في [`docs/funding/FUNDING_MEMO.md`](./FUNDING_MEMO.md). الأصول تُظهر أن البنية موجودة عند وصول الفاتورة، لا أنها أتت.

**EN.** We do not claim assets alone produce revenue. Assets are the infrastructure for revenue, not the revenue itself. Invoice #1 is still ahead; this is stated openly in the funding memo. The assets show that the infrastructure is in place for revenue when it arrives — they do not assert that revenue has arrived.

---

## ٧. كيف تتحقق · How to verify

**AR.** ثلاث خطوات:

```bash
# ١. اقرأ السجل العام
curl https://api.dealix.me/api/v1/capital-assets/public | jq .

# ٢. اقرأ العقيدة + الاختبارات المرتبطة بها
curl https://api.dealix.me/api/v1/dealix-promise | jq .commitments

# ٣. اقرأ السلّم التجاري والمصدر
curl https://api.dealix.me/api/v1/commercial-map | jq .
```

**EN.** Three steps shown above. No API key needed for any of the three. Each endpoint reads from the same Python module the CI tests consume, so the public response and the test-protected source agree by construction.

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
