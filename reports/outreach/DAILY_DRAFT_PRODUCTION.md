# إنتاج المسودّات اليومي — Daily Draft Production (TEMPLATE)

> **قالب.** يُملأ يومياً الساعة 08:30 من `data/outreach/drafts.jsonl`. **إنتاج
> مسودّات فقط** — لا إرسال. الهدف 250/يوم.
> **الوضع الافتراضي:** `dry_run=true` · `approval_required=true` · `send_enabled=false`

- **التاريخ:** `YYYY-MM-DD`
- **إجمالي المنتَج:** `<count>` / 250
- **المصدر:** `data/outreach/drafts.jsonl`

---

## 1. الخلطة مقابل الهدف (Mix vs Target)

| `draft_type` | المنتَج | الهدف | الفارق | الحالة |
|--------------|---------|-------|--------|--------|
| `first_touch` | `0` | 100 | `0` | ⬜ |
| `follow_up_1` | `0` | 75 | `0` | ⬜ |
| `follow_up_2` | `0` | 50 | `0` | ⬜ |
| `proposal_intro` | `0` | 15 | `0` | ⬜ |
| `close_loop` | `0` | 10 | `0` | ⬜ |
| **الإجمالي** | **`0`** | **250** | **`0`** | ⬜ |

---

## 2. التوزيع حسب التخصيص (`personalization_score`)

| المستوى | العدد | يدخل الطابور؟ |
|---------|------|----------------|
| `P0` | `0` | لا — مرفوض (`below_p1`) |
| `P1` | `0` | نعم |
| `P2` | `0` | نعم |
| `P3` | `0` | نعم |
| `P4` | `0` | نعم |

> أرضية الطابور = P1. أي `P0` يُرفَض ولا يُحتسَب في الطابور.

---

## 3. التوزيع حسب فرضية الألم (`pain_hypothesis`)

| `pain_hypothesis` | العدد | العرض الغالب |
|-------------------|------|---------------|
| `lead_leakage` | `0` | `DLX-L1` |
| `follow_up_chaos` | `0` | `DLX-L1`/`DLX-L2` |
| `crm_data_disorder` | `0` | `DLX-L3` |
| `proposal_delay` | `0` | `DLX-L2` |
| `weak_reporting` | `0` | `DLX-L3` |
| `sales_team_inconsistency` | `0` | `DLX-L3` |
| `support_overload` | `0` | `DLX-L3` |

---

## 4. الحالة (Status)

| الحقل | القيمة المتوقّعة |
|-------|-------------------|
| `approval_status` | `pending` (الكل) |
| `send_status` | `not_sent` (الكل) |
| المُرسَل اليوم | **0** — الإرسال مُعطَّل |

---

## 5. ملاحظات السلامة (إلزامي)

- [ ] إنتاج مسودّات فقط — 0 إرسال (`send_enabled=false`).
- [ ] كل مسودّة مرّت البوّابات السبع (انظر `DRAFT_GATE_REVIEW.md`).
- [ ] 0 مسودّة `P0` في الطابور · كل بارد يحمل سطر الإلغاء.
- [ ] لا عملاء مخترَعين · لا أرقام ملفّقة · أسماء placeholder فقط.
- [ ] الأرقام أعلاه قالب — تُستبدَل بقيم `data/outreach/drafts.jsonl`.

---

*المصدر: `data/outreach/drafts.jsonl`. المرجع:
`docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md`. الطابور:
`reports/outreach/APPROVAL_QUEUE.md`.*
