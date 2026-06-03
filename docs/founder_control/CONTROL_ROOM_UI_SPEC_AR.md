# مواصفة واجهة غرفة القيادة — Control Room UI Spec (عربي أولًا)

> مواصفة تنفيذية للواجهة فوق React + tRPC + shadcn القائمة. لا تنفيذ إرسال خارجي في v1.

---

## 1. المسار والتخطيط
- المسار: `/[locale]/ops/super-control` (RTL افتراضيًا للعربية).
- التخطيط: `Sidebar` (تبويبات) + رأس (أمر اليوم + القرار الحرج) + شبكة `Card` للبطاقات العلوية + `Tabs`/`Table` للطوابير.
- المكوّنات: `src/components/ui/{sidebar,tabs,card,table,badge,dialog,button,alert}.tsx` (موجودة).

## 2. مكوّنات مقترحة (أسماء)
```
SuperControlRoom/
  TopCommandBar        // أمر اليوم + قرار حرج واحد
  CardGrid             // 14 بطاقة علوية (Card + Badge للحالة/المخاطرة)
  QueueTable           // جدول عام للطوابير (approve/reject/edit/copy/mark-sent)
  ActionDrawer         // تفاصيل بطاقة + الإجراءات المفضّلة (Drawer)
  TabsNav              // 26 تبويبًا
  RiskPrivacySecurityPanel
```

## 3. حالة كل عنصر قابل للإجراء (Badges)
`risk_level` (low/medium/high/critical) · `evidence_level` · `approval_required` · `approved` · `dry_run` · `send_enabled`.
- `send_enabled=false` يُعرض دائمًا كشارة "إرسال مُعطّل (v1)".

## 4. الإجراءات في QueueTable / ActionDrawer
| الإجراء | الأثر | البوابة |
|---|---|---|
| approve | يضبط `approved=true` + `approved_by/at` (لا يرسل) | تسجيل ledger |
| reject | يضبط `status=rejected` + سبب | — |
| edit | يفتح المسودة للتحرير | — |
| copy | نسخ النص للتنفيذ اليدوي | — |
| mark sent manually | `status=sent_manually` بعد إرسال بشري | — |
| move to nurture | تحويل المحتمل لرعاية | GTM |
| do not contact | علم عدم التواصل | GTM |
| request human handoff | إنشاء `human_handoff` | `gate: human_handoff` |
| generate proposal/proof/payment | إنشاء مسودة (L4) | `gate: approval` |

## 5. الحارس على مستوى الواجهة (UI Guards)
- إخفاء/تعطيل أي زر إرسال خارجي ما دام `send_enabled=false`.
- منع عرض أي قيمة سرّية؛ تُعرض `secret_ref` كـ `portal://…` فقط.
- إخفاء أرقام الجوال (تُعرض `+9665XXXX####`).
- منع زر "اعتماد سعر نهائي" إن لم يكن العرض ضمن صلاحية المؤسس.

## 6. الوصول والأمن
- الدخول عبر Auth القائم (Kimi OAuth)، دور `admin` فقط لغرفة القيادة.
- تبويبات العميل (Portal) لا تُعرض بيانات عميل خام — ملخّصات فقط.

## 7. التنفيذ التدريجي
1. v1: قراءة الطوابير + approve/reject/edit/copy/mark-sent (بلا إرسال).
2. v2: ربط `generate_*` بمولّدات المسودات.
3. v3: تفعيل `send_enabled` بعد اكتمال البوابات (قرار مؤسس صريح).

---
*المرجع: `docs/founder_control/FOUNDER_SUPER_CONTROL_ROOM_AR.md` · الحاكم: `AGENTS.md`.*
