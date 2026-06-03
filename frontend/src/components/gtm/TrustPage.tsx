"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";

/* ─── Data ──────────────────────────────────────────── */

const DATA_COLLECTED = [
  {
    ar: { title: "بيانات التشخيص", desc: "اسم الشركة، القطاع، التحدي التشغيلي — يُستخدم فقط لإنتاج Proof Pack الخاص بك." },
    en: { title: "Diagnostic data", desc: "Company name, sector, operational challenge — used only to produce your Proof Pack." },
  },
  {
    ar: { title: "بيانات التواصل", desc: "الاسم، البريد الإلكتروني — للتواصل البشري المباشر فقط. لا أتمتة تسويقية." },
    en: { title: "Contact data", desc: "Name, email — for direct human communication only. No marketing automation." },
  },
  {
    ar: { title: "بيانات الاستخدام", desc: "الصفحات المُشاهَدة، مدة الجلسة — عبر PostHog مع إعدادات خصوصية مشدّدة." },
    en: { title: "Usage data", desc: "Pages viewed, session duration — via PostHog with strict privacy settings." },
  },
];

const NEVER_DO = [
  { ar: "لا نشتري قوائم leads أو قواعد بيانات جهات اتصال", en: "We never buy lead lists or contact databases" },
  { ar: "لا نُرسل واتساب أو LinkedIn آلي للعملاء المحتملين", en: "We never send automated WhatsApp or LinkedIn to prospects" },
  { ar: "لا نُشارك بياناتك مع طرف ثالث بدون موافقة صريحة مكتوبة", en: "We never share your data with third parties without explicit written consent" },
  { ar: "لا نُنشئ ملفات شخصية من بيانات عامة بدون علمك", en: "We never build profiles from public data without your knowledge" },
  { ar: "لا نُرسل أي تواصل تجاري بدون إذن مسبق صريح", en: "We never send any commercial communication without prior explicit permission" },
  { ar: "لا نستخدم scraping على أي موقع أو منصة", en: "We never use scraping on any website or platform" },
];

const PDPL_RIGHTS = [
  {
    ar: { right: "الوصول", desc: "طلب نسخة كاملة من بياناتك المحفوظة لدينا" },
    en: { right: "Access", desc: "Request a complete copy of your stored data with us" },
  },
  {
    ar: { right: "التصحيح", desc: "تصحيح أي بيانات غير دقيقة فوراً" },
    en: { right: "Correction", desc: "Correct any inaccurate data immediately" },
  },
  {
    ar: { right: "الحذف", desc: "طلب حذف بياناتك — نفّذه خلال 30 يوماً" },
    en: { right: "Deletion", desc: "Request deletion of your data — executed within 30 days" },
  },
  {
    ar: { right: "التصدير", desc: "تصدير بياناتك بصيغة قابلة للقراءة الآلية" },
    en: { right: "Portability", desc: "Export your data in a machine-readable format" },
  },
  {
    ar: { right: "سحب الموافقة", desc: "إلغاء موافقتك على المعالجة فوراً عند الطلب" },
    en: { right: "Withdraw consent", desc: "Cancel your processing consent immediately upon request" },
  },
  {
    ar: { right: "الاعتراض", desc: "الاعتراض على أي عملية معالجة بعينها" },
    en: { right: "Object", desc: "Object to any specific processing activity" },
  },
];

const GUARANTEE_ITEMS = [
  {
    ar: { title: "لا Proof Pack — لا دفع", desc: "إذا لم نُسلّم Proof Pack مكتمل خلال المدة المتفق عليها، نُعيد المبلغ كاملاً." },
    en: { title: "No Proof Pack — No Payment", desc: "If we don't deliver a complete Proof Pack within the agreed timeframe, we refund in full." },
  },
  {
    ar: { title: "شفافية كاملة في الـ Scope", desc: "كل مشروع يبدأ بـ Scope document موقّع. لا عمل خارج الـ Scope بدون موافقتك الصريحة." },
    en: { title: "Full Scope Transparency", desc: "Every project starts with a signed Scope document. No work outside Scope without your explicit approval." },
  },
  {
    ar: { title: "Approval Center لكل خطوة", desc: "لا إجراء خارجي يُنفَّذ دون مرور بـ Approval Center. أنت تُقرّر، الـ AI يُقترح." },
    en: { title: "Approval Center at Every Step", desc: "No external action executed without going through Approval Center. You decide, AI proposes." },
  },
  {
    ar: { title: "لا upsell قبل الإثبات", desc: "لا نقترح توسعاً قبل تسليم Proof Pack ناجح. هذا مبدأ غير قابل للتفاوض." },
    en: { title: "No Upsell Before Proof", desc: "We never suggest expansion before delivering a successful Proof Pack. This is non-negotiable." },
  },
];

/* ─── Component ─────────────────────────────────────── */

export function TrustPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const base = `/${locale}`;
  return (
    <PublicGtmShell>
      <div
        className={`mx-auto max-w-4xl px-6 py-12 space-y-16 ${isAr ? "text-right" : "text-left"}`}
        dir={isAr ? "rtl" : "ltr"}
      >

        {/* ── Hero ── */}
        <header>
          <Badge className="bg-emerald-100 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300 text-xs mb-4">
            {isAr ? "PDPL أصيل" : "PDPL Native"}
          </Badge>
          <h1 className="text-4xl font-bold mt-2">
            {isAr ? "الثقة والامتثال" : "Trust & Compliance"}
          </h1>
          <p className="mt-4 text-muted-foreground leading-relaxed text-lg max-w-2xl">
            {isAr
              ? "Dealix مبني على الثقة والامتثال كقيم جوهرية — لا كإضافة. PDPL أصيل، ZATCA جاهز، Approval-First في كل خطوة."
              : "Dealix is built on trust and compliance as core values — not as add-ons. PDPL native, ZATCA ready, Approval-First at every step."}
          </p>
          <div className="mt-4 flex flex-wrap gap-3">
            {(isAr ? [
              "PDPL أصيل",
              "ZATCA جاهز",
              "Approval-First",
              "لا outreach بارد",
              "Audit Trail كامل",
            ] : [
              "PDPL Native",
              "ZATCA Ready",
              "Approval-First",
              "No Cold Outreach",
              "Full Audit Trail",
            ]).map((tag) => (
              <span
                key={tag}
                className="rounded-full border border-emerald-500/30 bg-emerald-50/50 dark:bg-emerald-950/20 text-emerald-700 dark:text-emerald-300 px-3 py-1 text-xs font-medium"
              >
                {tag}
              </span>
            ))}
          </div>
        </header>

        {/* ── PDPL Compliance ── */}
        <section>
          <h2 className="text-2xl font-bold mb-2">{isAr ? "PDPL — نظام حماية البيانات" : "PDPL — Data Protection Law"}</h2>
          <p className="text-muted-foreground mb-6 leading-relaxed">
            {isAr
              ? "نظام حماية البيانات الشخصية السعودي يُلزم كل شركة تعالج بيانات أشخاص في المملكة. Dealix مُصمَّم من الصفر للامتثال الكامل."
              : "Saudi PDPL obliges every company processing personal data in the Kingdom. Dealix is designed from scratch for full compliance."}
          </p>
          <div className="grid gap-4 sm:grid-cols-3 mb-6">
            {DATA_COLLECTED.map((item) => {
              const content = isAr ? item.ar : item.en;
              return (
                <Card key={content.title} className="p-4 border-border/60 bg-card/50">
                  <p className="font-semibold text-sm mb-1">{content.title}</p>
                  <p className="text-xs text-muted-foreground leading-relaxed">{content.desc}</p>
                </Card>
              );
            })}
          </div>
          <div className="rounded-xl border border-red-500/20 bg-red-50/30 dark:bg-red-950/10 p-5">
            <p className="font-semibold text-sm mb-3">{isAr ? "ما لا نفعله — مطلقاً" : "What We Never Do"}</p>
            <div className="space-y-2">
              {NEVER_DO.map((item) => (
                <div key={isAr ? item.ar : item.en} className="flex items-start gap-2 text-sm text-muted-foreground">
                  <span className="text-red-500 mt-0.5 flex-shrink-0">x</span>
                  <span>{isAr ? item.ar : item.en}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Your PDPL Rights ── */}
        <section>
          <h2 className="text-2xl font-bold mb-2">{isAr ? "حقوقك بموجب PDPL" : "Your PDPL Rights"}</h2>
          <p className="text-muted-foreground mb-6 text-sm">
            {isAr
              ? "لممارسة أي من هذه الحقوق، تواصل معنا عبر البريد الإلكتروني. نستجيب خلال 72 ساعة."
              : "To exercise any of these rights, contact us by email. We respond within 72 hours."}
          </p>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {PDPL_RIGHTS.map((r) => {
              const content = isAr ? r.ar : r.en;
              return (
                <div key={content.right} className="rounded-lg border border-border/50 bg-card/50 p-3">
                  <p className="font-semibold text-sm">{content.right}</p>
                  <p className="text-xs text-muted-foreground mt-0.5 leading-relaxed">{content.desc}</p>
                </div>
              );
            })}
          </div>
        </section>

        {/* ── ZATCA Readiness ── */}
        <section className="rounded-xl border border-amber-500/20 bg-amber-50/30 dark:bg-amber-950/10 p-6">
          <div className="flex items-start gap-3 mb-4">
            <div className="w-9 h-9 rounded-full bg-amber-500 text-white flex items-center justify-center font-bold text-sm flex-shrink-0">
              Z
            </div>
            <div>
              <h2 className="text-xl font-bold">{isAr ? "ZATCA Wave 24 — الاستعداد" : "ZATCA Wave 24 — Readiness"}</h2>
              <p className="text-sm text-muted-foreground mt-1">
                {isAr ? "الموعد النهائي: 30 يونيو 2026" : "Deadline: June 30, 2026"}
              </p>
            </div>
          </div>
          <p className="text-sm text-muted-foreground leading-relaxed mb-4">
            {isAr
              ? "ZATCA Wave 24 تُلزم الشركات التي تجاوزت 375,000 ر.س إيراداً في 2022 بتطبيق الفوترة الإلكترونية المتكاملة (Phase 2) قبل 30 يونيو 2026. Dealix يُدمج تشخيص جاهزية ZATCA في كل Proof Pack تلقائياً."
              : "ZATCA Wave 24 mandates companies exceeding 375,000 SAR revenue in 2022 to implement integrated e-invoicing (Phase 2) before June 30, 2026. Dealix integrates ZATCA readiness diagnostics into every Proof Pack automatically."}
          </p>
          <Button asChild size="sm" variant="outline" className="border-amber-500/40 text-amber-700 dark:text-amber-300 hover:bg-amber-50 dark:hover:bg-amber-950/30">
            <Link href={`${base}/risk-score`}>
              {isAr ? "افحص جاهزية ZATCA" : "Check ZATCA Readiness"}
            </Link>
          </Button>
        </section>

        {/* ── Approval-First ── */}
        <section>
          <h2 className="text-2xl font-bold mb-4">
            {isAr ? "Approval-First Architecture" : "Approval-First Architecture"}
          </h2>
          <p className="text-muted-foreground leading-relaxed mb-6">
            {isAr
              ? "كل إجراء حرج في Dealix — إرسال بريد، مسودة واتساب، تحليل بيانات عميل — يمر عبر Approval Center قبل التنفيذ. هذا المبدأ مُضمَّن في البنية التقنية، لا فقط في السياسة."
              : "Every critical action in Dealix — sending email, WhatsApp draft, client data analysis — goes through the Approval Center before execution. This principle is embedded in the technical architecture, not just in policy."}
          </p>
          <div className="grid gap-3 sm:grid-cols-3">
            {(isAr ? [
              { step: "١", title: "AI يُقترح", desc: "الذكاء الاصطناعي يُنتج مسودة أو توصية" },
              { step: "٢", title: "مراجعة بشرية", desc: "أنت تراجع المسودة في Approval Center" },
              { step: "٣", title: "إرسال يدوي", desc: "تُقرّر الإرسال — الـ AI لا يُرسل وحده" },
            ] : [
              { step: "1", title: "AI proposes", desc: "AI generates draft or recommendation" },
              { step: "2", title: "Human review", desc: "You review the draft in Approval Center" },
              { step: "3", title: "Manual send", desc: "You decide to send — AI never sends alone" },
            ]).map((s) => (
              <div key={s.step} className="rounded-xl border border-border/60 bg-card/50 p-4 text-center">
                <div className="w-8 h-8 rounded-full bg-[#0A1628] text-[#C9974B] flex items-center justify-center font-bold text-sm mx-auto mb-3">
                  {s.step}
                </div>
                <p className="font-semibold text-sm">{s.title}</p>
                <p className="text-xs text-muted-foreground mt-1 leading-relaxed">{s.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ── No Cold Outreach ── */}
        <section className="rounded-xl border border-border/60 bg-card/50 p-6">
          <h2 className="text-xl font-bold mb-3">
            {isAr ? "سياسة لا outreach بارد" : "No Cold Outreach Policy"}
          </h2>
          <p className="text-muted-foreground leading-relaxed text-sm mb-4">
            {isAr
              ? "Dealix لا يُرسل رسائل واتساب أو LinkedIn أو بريد إلكتروني بارد آلياً. لا نشتري قوائم. لا نعتمد على cold outreach لأن PDPL يمنع ذلك وثقة السوق السعودي تتطلب نهجاً مختلفاً."
              : "Dealix never sends automated cold WhatsApp, LinkedIn, or email messages. We don't buy lists. We don't rely on cold outreach because PDPL prohibits it and Saudi market trust requires a different approach."}
          </p>
          <div className="rounded-lg border border-emerald-500/20 bg-emerald-50/30 dark:bg-emerald-950/10 p-4">
            <p className="text-sm font-medium text-emerald-700 dark:text-emerald-300">
              {isAr
                ? "بدلاً من ذلك: قوائم warm معتمدة + مسودات من AI + مراجعة بشرية + إرسال يدوي مسجّل في Audit Trail."
                : "Instead: approved warm lists + AI drafts + human review + manual send logged in Audit Trail."}
            </p>
          </div>
        </section>

        {/* ── Guarantees ── */}
        <section>
          <h2 className="text-2xl font-bold mb-6">
            {isAr ? "ضماناتنا" : "Our Guarantees"}
          </h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {GUARANTEE_ITEMS.map((g) => {
              const content = isAr ? g.ar : g.en;
              return (
                <Card key={content.title} className="p-5 border-[#C9974B]/20 bg-gradient-to-br from-[#C9974B]/5 to-card">
                  <p className="font-semibold mb-2">{content.title}</p>
                  <p className="text-sm text-muted-foreground leading-relaxed">{content.desc}</p>
                </Card>
              );
            })}
          </div>
        </section>

        {/* ── Data Retention ── */}
        <section>
          <h2 className="text-xl font-bold mb-4">{isAr ? "الاحتفاظ بالبيانات" : "Data Retention"}</h2>
          <div className="rounded-xl border border-border/60 bg-card/50 p-5 space-y-2 text-sm">
            {(isAr ? [
              "بيانات التشخيص: تُحتفظ 12 شهراً من تاريخ الإنشاء",
              "بيانات التواصل: تُحذف فور طلب صاحبها",
              "سجلات Audit Trail: تُحتفظ 36 شهراً للامتثال القانوني",
              "Soft deletes: لا حذف مادي فوري — تُعلَّم محذوفة وتُعزل",
            ] : [
              "Diagnostic data: retained 12 months from creation date",
              "Contact data: deleted upon owner's request",
              "Audit Trail logs: retained 36 months for legal compliance",
              "Soft deletes: no immediate physical deletion — marked deleted and isolated",
            ]).map((item) => (
              <div key={item} className="flex items-start gap-2">
                <span className="text-primary mt-0.5 flex-shrink-0">-</span>
                <span className="text-muted-foreground">{item}</span>
              </div>
            ))}
          </div>
        </section>

        {/* ── Legal Notice ── */}
        <section className="rounded-xl border border-border/60 bg-muted/20 p-6">
          <h2 className="text-lg font-bold mb-3">{isAr ? "ملاحظة قانونية" : "Legal Notice"}</h2>
          <p className="text-xs text-muted-foreground leading-relaxed">
            {isAr
              ? "تخضع هذه الخدمة لأنظمة المملكة العربية السعودية ذات الصلة بما فيها نظام حماية البيانات الشخصية (PDPL)، ونظام التجارة الإلكترونية، وأنظمة الزكاة والضريبة والجمارك (ZATCA). أي نزاع ينشأ عن استخدام هذه الخدمة يخضع للقضاء السعودي. آخر تحديث: مايو 2026."
              : "This service is subject to applicable Saudi Arabian regulations including the Personal Data Protection Law (PDPL), E-Commerce Regulations, and ZATCA (Zakat, Tax and Customs Authority) regulations. Any dispute arising from the use of this service is subject to Saudi jurisdiction. Last updated: May 2026."}
          </p>
          <div className="mt-4 flex flex-wrap gap-3">
            <Link
              href={`${base}/privacy`}
              className="text-xs text-primary hover:underline"
            >
              {isAr ? "سياسة الخصوصية" : "Privacy Policy"}
            </Link>
            <Link
              href={`${base}/trust`}
              className="text-xs text-primary hover:underline"
            >
              {isAr ? "صفحة الثقة والامتثال" : "Trust & Compliance Page"}
            </Link>
          </div>
        </section>

      </div>
    </PublicGtmShell>
  );
}
