"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";

/* ─── Data ──────────────────────────────────────────── */

const VALUES = [
  {
    icon: "A",
    ar: { title: "الموافقة أولاً", desc: "كل إجراء خارجي يتطلب مراجعة بشرية وموافقة صريحة. لا أتمتة عمياء." },
    en: { title: "Approval First", desc: "Every external action requires human review and explicit approval. No blind automation." },
  },
  {
    icon: "E",
    ar: { title: "الأدلة قبل الادعاء", desc: "لا نتيجة بدون دليل موثّق. L0-L5: من الفرضية إلى الإثبات القابل للتدقيق." },
    en: { title: "Evidence Before Claim", desc: "No outcome without documented proof. L0-L5: from hypothesis to auditable proof." },
  },
  {
    icon: "T",
    ar: { title: "الثقة عبر الامتثال", desc: "PDPL و ZATCA ليسا قيوداً — هما ميزة تنافسية في سوق يشتري بالثقة." },
    en: { title: "Trust Through Compliance", desc: "PDPL and ZATCA are not restrictions — they are competitive advantages in a trust-first market." },
  },
  {
    icon: "S",
    ar: { title: "التوسع بعد الإثبات", desc: "لا upsell قبل Proof Pack مُسلَّم. كل توسّع مبني على نتيجة مُثبَتة." },
    en: { title: "Expansion After Proof", desc: "No upsell before delivered Proof Pack. Every expansion is built on a proven result." },
  },
];

const MARKET_FACTS = [
  {
    ar: { stat: "375,000+", label: "ريال سعودي — الحد الأدنى لـ ZATCA Wave 24" },
    en: { stat: "375,000+", label: "SAR — minimum threshold for ZATCA Wave 24" },
  },
  {
    ar: { stat: "5M", label: "ريال سعودي — الحد الأقصى لغرامات PDPL" },
    en: { stat: "5M", label: "SAR — maximum PDPL penalty" },
  },
  {
    ar: { stat: "30 يونيو", label: "2026 — الموعد النهائي لـ ZATCA Wave 24" },
    en: { stat: "June 30", label: "2026 — ZATCA Wave 24 final deadline" },
  },
  {
    ar: { stat: "B2B", label: "السوق الوحيد الذي نخدمه — تركيز مطلق" },
    en: { stat: "B2B", label: "The only market we serve — absolute focus" },
  },
];

const COMPLIANCE_POINTS = [
  {
    ar: { title: "PDPL أصيل", desc: "نظام حماية البيانات الشخصية مدمج في بنيتنا التقنية من اليوم الأول. لا add-on. لا patch." },
    en: { title: "PDPL Native", desc: "Personal Data Protection Law built into our technical architecture from day one. Not an add-on. Not a patch." },
  },
  {
    ar: { title: "ZATCA جاهز", desc: "تشخيص جاهزية الفوترة الإلكترونية في كل Proof Pack. نساعدك تعرف وضعك وتخطط خطواتك." },
    en: { title: "ZATCA Ready", desc: "E-invoicing readiness diagnostic in every Proof Pack. We help you understand your position and plan your steps." },
  },
  {
    ar: { title: "Audit Trail كامل", desc: "سجل تدقيق لكل قرار، كل إجراء، كل تعديل. جاهز للمراجعة الخارجية في أي وقت." },
    en: { title: "Full Audit Trail", desc: "Audit log for every decision, every action, every modification. Ready for external review at any time." },
  },
  {
    ar: { title: "لا outreach بارد", desc: "مبدأ غير قابل للتفاوض: لا واتساب آلي، لا LinkedIn automation، لا شراء قوائم." },
    en: { title: "No Cold Outreach", desc: "Non-negotiable principle: no automated WhatsApp, no LinkedIn automation, no list purchases." },
  },
];

/* ─── Component ─────────────────────────────────────── */

export function AboutPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const base = `/${locale}`;

  return (
    <PublicGtmShell>
      <div
        className={`mx-auto max-w-5xl px-6 py-12 space-y-20 ${isAr ? "text-right" : "text-left"}`}
        dir={isAr ? "rtl" : "ltr"}
      >

        {/* ── Mission Hero ── */}
        <section className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-[#0A1628] to-[#0a2040] px-8 py-14 text-white shadow-xl">
          <div className="relative space-y-5">
            <Badge className="bg-white/10 text-white border-white/20 text-xs">
              {isAr ? "من نحن" : "About Us"}
            </Badge>
            <h1 className="text-4xl font-bold leading-tight md:text-5xl">
              {isAr
                ? <>عمليات AI محكومة<br /><span className="text-[#C9974B]">للسوق السعودي</span></>
                : <>Governed AI Operations<br /><span className="text-[#C9974B]">for the Saudi Market</span></>}
            </h1>
            <p className="max-w-2xl text-lg text-white/80 leading-relaxed">
              {isAr
                ? "Dealix ليس CRM آخر. نحن نظام تشغيل إيرادات يجمع الحوكمة والأدلة والامتثال في مكان واحد — مبني للسوق الذي يشتري بالثقة."
                : "Dealix is not another CRM. We are a revenue operating system that combines governance, evidence, and compliance in one place — built for a market that buys on trust."}
            </p>
          </div>
        </section>

        {/* ── Mission Statement ── */}
        <section className="grid gap-8 lg:grid-cols-2 items-center">
          <div>
            <p className="text-sm font-semibold text-[#C9974B] uppercase tracking-wide mb-3">
              {isAr ? "رسالتنا" : "Our Mission"}
            </p>
            <h2 className="text-3xl font-bold leading-snug">
              {isAr
                ? "كل قرار إيراد يجب أن يكون قابلاً للتدقيق"
                : "Every revenue decision must be auditable"}
            </h2>
            <p className="mt-4 text-muted-foreground leading-relaxed">
              {isAr
                ? "السوق السعودي يشتري بالثقة والعلاقات. الشركات التي تعمل بحوكمة واضحة وأدلة موثّقة تبني ثقة أسرع وتُغلق صفقات أكبر."
                : "The Saudi market buys on trust and relationships. Companies that operate with clear governance and documented evidence build trust faster and close larger deals."}
            </p>
            <p className="mt-4 text-muted-foreground leading-relaxed">
              {isAr
                ? "Dealix يُمكّن شركات B2B السعودية من بناء هذه الثقة المنهجية — عبر SOAEN Framework الذي يربط كل إشارة سوق بقرار موثّق."
                : "Dealix enables Saudi B2B companies to build this systematic trust — via the SOAEN Framework that links every market signal to a documented decision."}
            </p>
          </div>
          <Card className="p-6 bg-gradient-to-br from-card to-card/50 border-[#C9974B]/20">
            <p className="text-sm font-semibold text-[#C9974B] uppercase tracking-wide mb-4">
              {isAr ? "SOAEN Framework" : "SOAEN Framework"}
            </p>
            <div className="space-y-3">
              {[
                { l: "S", ar: "Signal — إشارة السوق مربوطة بقرار إيراد", en: "Signal — market signal tied to a revenue decision" },
                { l: "O", ar: "Offer — عرض واحد على السطح بحد أقصى 3", en: "Offer — one surface offer, maximum 3" },
                { l: "A", ar: "Action — إجراء خارجي بموافقة مسجّلة", en: "Action — external action with logged approval" },
                { l: "E", ar: "Evidence — دليل لكل لمسة مع العميل", en: "Evidence — proof for every customer touch" },
                { l: "N", ar: "Narrative — قصة إيراد موحّدة للمؤسس", en: "Narrative — unified revenue story for founder" },
              ].map((s) => (
                <div key={s.l} className="flex items-start gap-3">
                  <span className="flex-shrink-0 w-7 h-7 rounded-full bg-[#0A1628] text-[#C9974B] flex items-center justify-center text-xs font-bold">
                    {s.l}
                  </span>
                  <span className="text-sm">{isAr ? s.ar : s.en}</span>
                </div>
              ))}
            </div>
          </Card>
        </section>

        {/* ── Governed AI Difference ── */}
        <section className="rounded-2xl border border-[#C9974B]/20 bg-gradient-to-br from-[#C9974B]/5 to-card p-8">
          <p className="text-sm font-semibold text-[#C9974B] uppercase tracking-wide mb-3">
            {isAr ? "الفرق" : "The Difference"}
          </p>
          <h2 className="text-2xl font-bold mb-4">
            {isAr ? "AI محكوم — ليس AI غير مقيّد" : "Governed AI — Not Ungoverned AI"}
          </h2>
          <div className="grid gap-6 sm:grid-cols-2">
            <div className="space-y-3">
              <p className="font-semibold text-red-500 dark:text-red-400">
                {isAr ? "AI غير محكوم" : "Ungoverned AI"}
              </p>
              {(isAr ? [
                "يرسل واتساب بارد آلياً",
                "يُنتج محتوى بلا موافقة",
                "لا audit trail لقراراته",
                "يُعرّضك لغرامات PDPL",
                "يدمر علاقات العمل",
              ] : [
                "Sends automated cold WhatsApp",
                "Produces content without approval",
                "No audit trail for its decisions",
                "Exposes you to PDPL fines",
                "Destroys business relationships",
              ]).map((item) => (
                <div key={item} className="flex items-start gap-2 text-sm text-muted-foreground">
                  <span className="text-red-400 mt-0.5 flex-shrink-0">x</span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
            <div className="space-y-3">
              <p className="font-semibold text-emerald-500 dark:text-emerald-400">
                {isAr ? "AI محكوم — نهج Dealix" : "Governed AI — Dealix Approach"}
              </p>
              {(isAr ? [
                "Approval Center قبل كل إرسال خارجي",
                "AI يُقترح — الإنسان يُقرّر",
                "Audit trail لكل قرار",
                "PDPL native من البداية",
                "يبني ثقة طويلة الأمد",
              ] : [
                "Approval Center before every external send",
                "AI proposes — human decides",
                "Audit trail for every decision",
                "PDPL native from the start",
                "Builds long-term trust",
              ]).map((item) => (
                <div key={item} className="flex items-start gap-2 text-sm text-muted-foreground">
                  <span className="text-emerald-500 mt-0.5 flex-shrink-0">+</span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Values ── */}
        <section>
          <p className="text-sm font-semibold text-[#C9974B] uppercase tracking-wide mb-3">
            {isAr ? "قيمنا" : "Our Values"}
          </p>
          <h2 className="text-2xl font-bold mb-6">
            {isAr ? "مبادئ غير قابلة للتفاوض" : "Non-negotiable Principles"}
          </h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {VALUES.map((v) => {
              const content = isAr ? v.ar : v.en;
              return (
                <Card key={v.icon} className="p-5 border-border/60 bg-card/50">
                  <div className="flex items-start gap-3">
                    <div className="w-9 h-9 rounded-full bg-[#0A1628] text-[#C9974B] flex items-center justify-center font-bold text-sm flex-shrink-0">
                      {v.icon}
                    </div>
                    <div>
                      <p className="font-semibold">{content.title}</p>
                      <p className="text-sm text-muted-foreground mt-1 leading-relaxed">{content.desc}</p>
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        </section>

        {/* ── Saudi Market Expertise ── */}
        <section>
          <p className="text-sm font-semibold text-[#C9974B] uppercase tracking-wide mb-3">
            {isAr ? "خبرة السوق" : "Market Expertise"}
          </p>
          <h2 className="text-2xl font-bold mb-6">
            {isAr ? "مبني للسوق السعودي" : "Built for the Saudi Market"}
          </h2>
          <p className="text-muted-foreground leading-relaxed mb-8 max-w-2xl">
            {isAr
              ? "نحن لا نُطبّق نماذج غربية على السوق السعودي. Dealix مبني من الصفر للثقافة التجارية السعودية — حيث العلاقات والامتثال هما العملة الحقيقية."
              : "We don't apply Western models to the Saudi market. Dealix is built from scratch for Saudi business culture — where relationships and compliance are the real currency."}
          </p>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {MARKET_FACTS.map((f, i) => {
              const content = isAr ? f.ar : f.en;
              return (
                <div key={i} className="rounded-xl border border-border/60 bg-card/50 p-4 text-center">
                  <p className="text-2xl font-bold text-[#C9974B]">{content.stat}</p>
                  <p className="text-xs text-muted-foreground mt-2 leading-relaxed">{content.label}</p>
                </div>
              );
            })}
          </div>
        </section>

        {/* ── Compliance Commitment ── */}
        <section>
          <p className="text-sm font-semibold text-[#C9974B] uppercase tracking-wide mb-3">
            {isAr ? "الامتثال" : "Compliance"}
          </p>
          <h2 className="text-2xl font-bold mb-2">
            {isAr ? "PDPL + ZATCA — التزامنا" : "PDPL + ZATCA — Our Commitment"}
          </h2>
          <p className="text-muted-foreground mb-6 leading-relaxed max-w-2xl">
            {isAr
              ? "الامتثال ليس خياراً في السوق السعودي. هو الحد الأدنى للعمل التجاري الموثوق."
              : "Compliance is not optional in the Saudi market. It is the baseline for trusted business operations."}
          </p>
          <div className="grid gap-4 sm:grid-cols-2">
            {COMPLIANCE_POINTS.map((cp) => {
              const content = isAr ? cp.ar : cp.en;
              return (
                <Card key={content.title} className="p-5 border-border/60 bg-card/50">
                  <p className="font-semibold text-sm mb-2">{content.title}</p>
                  <p className="text-sm text-muted-foreground leading-relaxed">{content.desc}</p>
                </Card>
              );
            })}
          </div>
        </section>

        {/* ── Contact ── */}
        <section className="rounded-2xl bg-gradient-to-br from-[#0A1628] to-[#0a2040] text-white px-8 py-12">
          <h2 className="text-2xl font-bold mb-3">
            {isAr ? "تواصل معنا" : "Contact Us"}
          </h2>
          <p className="text-white/70 mb-6 max-w-xl">
            {isAr
              ? "لديك سؤال عن كيف يمكن Dealix مساعدة شركتك؟ ابدأ بتشخيص مجاني أو تواصل مباشرة."
              : "Have a question about how Dealix can help your company? Start with a free diagnostic or contact us directly."}
          </p>
          <div className="flex flex-wrap gap-3">
            <Button asChild size="lg" className="bg-[#C9974B] text-[#0A1628] hover:bg-[#b8863a] font-bold">
              <Link href={`${base}/dealix-diagnostic`}>
                {isAr ? "ابدأ التشخيص" : "Start Diagnostic"}
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline" className="border-white/30 text-white bg-white/10 hover:bg-white/20">
              <Link href={`${base}/risk-score`}>
                {isAr ? "Risk Score مجاني" : "Free Risk Score"}
              </Link>
            </Button>
          </div>
          <p className="mt-6 text-white/40 text-xs">
            {isAr
              ? "لا outreach بارد · لا scraping · PDPL أصيل · موافقة بشرية دائماً"
              : "No cold outreach · No scraping · PDPL native · Human approval always"}
          </p>
        </section>

      </div>
    </PublicGtmShell>
  );
}
