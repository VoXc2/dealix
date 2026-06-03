# System Delivery Checklists — قوائم التسليم لكل نظام

لكل نظام من الخمسة: **متى نسلّمه؟** + **المدخلات المطلوبة** + **Delivery Pack** (المخرجات) + **معايير القبول**. هذه القوائم هي نفسها `required_inputs` في كرت الحاجة والعرض، ونفسها التي تفرضها بوابة التسليم.

---

## 1. Revenue Operating System
**متى؟** فرص/استفسارات/مبيعات تضيع أو بلا نظام موحد.

**Required Inputs:** مصادر الاستفسارات · ملف leads أو CRM export · مراحل البيع الحالية · قنوات التواصل · أمثلة رسائل حالية · صاحب القرار

**Delivery Pack:** Revenue Leakage Map · Opportunity Stage Model · Follow-up Workflow · Draft Templates · Weekly Revenue Report · Founder Next-Action List

**Acceptance:** كل فرصة لها status · كل status له next action · تقرير واضح للإدارة · follow-up workflow قابل للاستخدام

---

## 2. Executive Command OS
**متى؟** المؤسس/المدير لا يرى الصورة اليومية ولا يعرف أهم قرار.

**Required Inputs:** أهم أهداف الشركة · مؤشرات المبيعات الحالية · مصادر العملاء · أهم المخاطر · شكل التقارير الحالية · المسؤولون الداخليون

**Delivery Pack:** KPI Map · Daily Command Report · Risk/Priority Matrix · Decision Log · Executive Action Board · Weekly Executive Review Template

**Acceptance:** التقرير يوضح أهم قرار يومي · المخاطر مرتبة · الفرص مرتبة · يوجد decision log واضح

---

## 3. Follow-up Recovery OS
**متى؟** الفرص تضيع بعد أول تواصل.

**Required Inputs:** قائمة leads أو محادثات · آخر تواصل · حالة كل lead إن وجدت · قنوات المتابعة · أمثلة ردود العملاء

**Delivery Pack:** Follow-up Queue · Lead Status Model · Follow-up Message Set · Reminder Rhythm · Recovery Report · Escalation Rules

**Acceptance:** يوجد queue واضح · لكل lead message مناسب · المتابعة لها cadence · يوجد تقرير أسبوعي

---

## 4. WhatsApp Client OS
**متى؟** واتساب قناة رئيسية عند العميل.

**Required Inputs:** أنواع الطلبات في واتساب · أكثر الأسئلة تكرارًا · متى يحتاج العميل تصعيدًا لإنسان · الروابط/النماذج المستخدمة · سياسة الملفات والصلاحيات

**Delivery Pack:** WhatsApp Flow Map · Readiness Scan · Action Cards · Human Handoff Policy · Secure Portal Handoff Guide · Weekly WhatsApp Review

**Acceptance:** المحادثات لها flows · يوجد handoff واضح · لا يوجد طلب أسرار داخل واتساب · يوجد تقرير مراجعة أسبوعي

> ملاحظة: واتساب يحتاج workflow مضبوط لا «بوت عام مفتوح»، وWhatsApp Cloud API يُبنى فوقه أو عبر مزوّد حلول.

---

## 5. Proposal & Proof OS
**متى؟** العروض ضعيفة أو بطيئة أو بلا دليل.

**Required Inputs:** الخدمة أو المنتج · نموذج عرض سابق إن وجد · اعتراضات العملاء · أمثلة أعمال سابقة · نطاق الخدمة · الأسعار التقريبية

**Delivery Pack:** Proposal Template · Proof Pack Template · Scope / Out-of-scope · Risk & Assumption Block · Next-step Card · Proposal Review Checklist

**Acceptance:** العرض واضح · النطاق واضح · يوجد proof angle · يوجد next step · لا وعود مبالغ فيها

---

## ربط بالبيانات

هذه المدخلات تظهر في `data/delivery/pipelines.jsonl` ضمن `required_inputs` كأزواج `{name, provided}`. التسليم لا يبدأ قبل أن تكون كلها `provided = true` (الفحص **C05**).
