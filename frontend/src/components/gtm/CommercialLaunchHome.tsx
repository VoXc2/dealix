"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";

import { motion, useInView, useAnimation, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { InteractiveTechDemo } from "./InteractiveTechDemo";
import { HermesAgentWidget } from "./HermesAgentWidget";

const ORGANIZATION_JSON_LD = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Dealix",
  url: "https://dealix.me",
  logo: "https://dealix.me/brand/logo-mark.svg",
  description: "Saudi-first AI Business Operating System — governed revenue operations, PDPL native, ZATCA ready, approval-first.",
  foundingDate: "2024",
  areaServed: { "@type": "Country", name: "Saudi Arabia" },
  sameAs: [],
};

const SOFTWARE_JSON_LD = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "Dealix Revenue Operating System",
  applicationCategory: "BusinessApplication",
  operatingSystem: "Web",
  offers: { "@type": "Offer", price: "0", priceCurrency: "SAR", description: "Quote after discovery — no fixed pricing before scope" },
  featureList: "Evidence-governed revenue ops, L0-L5 proof ledger, approval-first automation, bilingual AR/EN, PDPL/ZATCA ready",
};


// ---------------------------------------------------------------------------
// Static data
// ---------------------------------------------------------------------------

const FEATURES = [
  {
    icon: "⚡",
    ar: "محرك الإيرادات الذكي",
    en: "AI Revenue Engine",
    descAr: "تحليل مسارات الإيراد وكشف التسرّب بالوقت الفعلي.",
    descEn: "Real-time revenue pathway analysis and leakage detection.",
  },
  {
    icon: "📊",
    ar: "لوحة تحكم تحليلية",
    en: "Analytics Dashboard",
    descAr: "رؤية موحّدة لكل مؤشرات الأداء في مكان واحد.",
    descEn: "Unified KPI visibility across every revenue motion.",
  },
  {
    icon: "🛡️",
    ar: "امتثال PDPL و ZATCA",
    en: "PDPL & ZATCA Compliance",
    descAr: "جاهزية تلقائية لمتطلبات الفوترة الإلكترونية وحماية البيانات.",
    descEn: "Automated readiness for e-invoicing and data protection.",
  },
  {
    icon: "🤝",
    ar: "إدارة العملاء (CRM)",
    en: "CRM Management",
    descAr: "CRM محكوم بالبيانات مع audit log كامل.",
    descEn: "Data-governed CRM with full audit trail.",
  },
  {
    icon: "📋",
    ar: "تقارير مخصصة",
    en: "Custom Reports",
    descAr: "تقارير ثنائية اللغة قابلة للتصدير بضغطة واحدة.",
    descEn: "One-click bilingual exportable reports.",
  },
  {
    icon: "🕐",
    ar: "تشغيل محكوم بالمراجعة",
    en: "Governed Human Review",
    descAr: "المخرجات الحساسة تمر بمراجعة وصلاحيات واضحة قبل أي أثر خارجي.",
    descEn: "Sensitive outputs pass explicit review and authority gates before external effect.",
  },
];

const LOGOS = [
  { initials: "✓", name: "تشخيص 7 أيام" },
  { initials: "✓", name: "Proof Pack" },
  { initials: "✓", name: "موافقة أولاً" },
  { initials: "✓", name: "Audit Log" },
  { initials: "✓", name: "PDPL أصيل" },
  { initials: "✓", name: "ZATCA جاهز" },
];

const STATS = [
  { valueAr: "L0-L5", valueEn: "L0-L5", labelAr: "مستويات الأدلة", labelEn: "Evidence Levels", target: 5 },
  { valueAr: "موافقة", valueEn: "Approval", labelAr: "بوابة موافقة لكل إرسال", labelEn: "Approval gate per send", target: 1 },
  { valueAr: "Audit", valueEn: "Audit", labelAr: "سجل تدقيق كامل", labelEn: "Full audit log", target: 1 },
  { valueAr: "AR+EN", valueEn: "AR+EN", labelAr: "عربي + إنجليزي أصيل", labelEn: "Native AR+EN", target: 2 },
];

const PRICING = [
  {
    tierAr: "المبدئي",
    tierEn: "Starter",
    priceAr: "السعر بعد جلسة الاكتشاف",
    priceEn: "Quote after discovery",
    periodAr: "بعد نطاق موثق",
    periodEn: "after a documented scope",
    featuresAr: ["Revenue Command Pilot لمدة 30 يومًا", "Proof Pack أسبوعي", "خط أساس تشغيلي", "تقرير ثنائي اللغة"],
    featuresEn: ["7-day diagnostic", "Proof Pack PDF", "Revenue map", "Bilingual report"],
    popular: false,
    ctaAr: "ابدأ الآن",
    ctaEn: "Get started",
    href: "/offer/lead-intelligence-sprint",
  },
  {
    tierAr: "النمو",
    tierEn: "Growth",
    priceAr: "السعر بعد جلسة الاكتشاف",
    priceEn: "Quote after discovery",
    periodAr: "بعد نطاق موثق",
    periodEn: "after a documented scope",
    featuresAr: ["كل ميزات المبدئي", "CRM محكوم", "تقارير أسبوعية", "دعم أولوية", "لوحة تحليلية", "امتثال ZATCA"],
    featuresEn: ["Everything in Starter", "Governed CRM", "Weekly reports", "Priority support", "Analytics dashboard", "ZATCA readiness review"],
    popular: true,
    ctaAr: "ابدأ النمو",
    ctaEn: "Start growing",
    href: "/book-call",
  },
  {
    tierAr: "المؤسسي",
    tierEn: "Enterprise",
    priceAr: "مخصص",
    priceEn: "Custom",
    periodAr: "",
    periodEn: "",
    featuresAr: ["كل ميزات النمو", "تكامل API مخصص", "مدير حساب مخصص", "SLA حسب النطاق المتفق عليه", "تدريب الفريق", "audit log كامل"],
    featuresEn: ["Everything in Growth", "Custom API integration", "Dedicated account manager", "SLA defined in agreed scope", "Team training", "Full audit log"],
    popular: false,
    ctaAr: "تحدث مع فريقنا",
    ctaEn: "Talk to our team",
    href: "/book-call",
  },
];

const TESTIMONIALS = [
  {
    nameAr: "منهجية الإثبات",
    nameEn: "Proof Methodology",
    companyAr: "L0-L5 فصل النشاط عن القيمة",
    companyEn: "L0-L5 activity vs value separation",
    quoteAr: "كل تنفيذ يحمل دليلاً: مصدر، موافقة، سجل تدقيق. لا نرقّي عميلاً إلى CAPTURED REVENUE قبل PAYMENT_VERIFIED.",
    quoteEn: "Every execution carries evidence: source, approval, audit log. No promotion to captured revenue before PAYMENT_VERIFIED.",
    stars: 5,
  },
  {
    nameAr: "حوكمة PDPL",
    nameEn: "PDPL Governance",
    companyAr: "موافقة قبل أي إرسال خارجي",
    companyEn: "Approval before any external send",
    quoteAr: "Dealix داخلي يبني المسودات؛ الخارجي يبقى خلف Approval Center. لا scraping ولا تواصل بارد.",
    quoteEn: "Dealix builds drafts internally; external stays behind Approval Center. No scraping, no cold outreach.",
    stars: 5,
  },
  {
    nameAr: "مسار التوسع",
    nameEn: "Expansion Path",
    companyAr: "تشخيص → Pilot 30 يوم → Proof → توسع",
    companyEn: "Diagnostic → 30-day Pilot → Proof → Expand",
    quoteAr: "وسّع فقط بعد Proof Pack أسبوعي وقبول عميل موثق. كل توسع له kill/stop-loss واضح.",
    quoteEn: "Expand only after weekly Proof Pack and documented client acceptance. Every expansion has a clear kill/stop-loss.",
    stars: 5,
  },
];

const TRUST_BADGES = [
  { icon: "🔒", ar: "مراعٍ لـ PDPL في التصميم", en: "PDPL-aware by design" },
  { icon: "🧾", ar: "فحص جاهزية ZATCA", en: "ZATCA readiness checks" },
  { icon: "🇸🇦", ar: "صنع في السعودية", en: "Saudi-First" },
  { icon: "🚫", ar: "لا تسويق بارد آلي", en: "No Cold Outreach" },
  { icon: "📋", ar: "audit log كامل", en: "Full Audit Log" },
];

// ---------------------------------------------------------------------------
// Animation variants
// ---------------------------------------------------------------------------

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  visible: (i: number = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay: i * 0.08, ease: "easeOut" },
  }),
};

const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.09 } },
};

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function AnimatedNumber({ target, suffix = "" }: { target: number; suffix?: string }) {
  const [count, setCount] = useState(0);
  const ref = useRef<HTMLSpanElement>(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });

  useEffect(() => {
    if (!inView) return;
    const duration = 1600;
    const steps = 48;
    const increment = target / steps;
    let current = 0;
    const timer = setInterval(() => {
      current = Math.min(current + increment, target);
      setCount(Math.round(current * 10) / 10);
      if (current >= target) clearInterval(timer);
    }, duration / steps);
    return () => clearInterval(timer);
  }, [inView, target]);

  return (
    <span ref={ref}>
      {count % 1 === 0 ? count.toFixed(0) : count.toFixed(1)}
      {suffix}
    </span>
  );
}

function StarRating({ count }: { count: number }) {
  return (
    <div className="flex gap-0.5">
      {Array.from({ length: count }).map((_, i) => (
        <span key={i} className="text-gold-400 text-sm">★</span>
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export function CommercialLaunchHome() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const dir = isAr ? "rtl" : "ltr";
  const base = `/${locale}`;

  const [name, setName] = useState("");
  const [company, setCompany] = useState("");
  const [email, setEmail] = useState("");
  const [emailSubmitted, setEmailSubmitted] = useState(false);
  const [emailSubmitting, setEmailSubmitting] = useState(false);
  const [emailError, setEmailError] = useState("");
  const [leadRef, setLeadRef] = useState("");

  const heroControls = useAnimation();
  const heroRef = useRef<HTMLDivElement>(null);
  const heroInView = useInView(heroRef, { once: true });

  useEffect(() => {
    if (heroInView) heroControls.start("visible");
  }, [heroInView, heroControls]);

  async function handleEmailSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim() || !company.trim() || !email.trim()) return;
    setEmailSubmitting(true);
    setEmailError("");
    try {
      const { data } = await api.postPublicLead({
        name: name.trim(),
        company: company.trim(),
        email: email.trim(),
        country: "Saudi Arabia",
        source: "landing/free-diagnostic",
        consent_marketing: false,
        consent_proof_pack: false,
        hold_stage: false,
      });
      setLeadRef(String(data.lead_id || ""));
      setEmailSubmitted(true);
    } catch {
      setEmailError(isAr ? "تعذّر تسجيل الطلب الآن. جرّب مرة أخرى أو استخدم صفحة التشخيص." : "Could not register the request. Try again or use the diagnostic page.");
    } finally {
      setEmailSubmitting(false);
    }
  }

  return (
    <div dir={dir} className="min-h-screen bg-navy-500 text-white overflow-x-hidden">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(ORGANIZATION_JSON_LD) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(SOFTWARE_JSON_LD) }}
      />
      {/* ------------------------------------------------------------------ */}
      {/* HERO                                                                */}
      {/* ------------------------------------------------------------------ */}
      <section
        ref={heroRef}
        className="relative min-h-screen flex flex-col items-center justify-center px-4 overflow-hidden"
        style={{ background: "linear-gradient(135deg, #001F3F 0%, #001830 40%, #000d1a 70%, #001020 100%)" }}
      >
        {/* Animated gradient orbs */}
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 overflow-hidden"
        >
          <motion.div
            animate={{ scale: [1, 1.15, 1], opacity: [0.18, 0.28, 0.18] }}
            transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
            className="absolute -top-32 -left-32 w-[520px] h-[520px] rounded-full"
            style={{ background: "radial-gradient(circle, rgba(212,175,55,0.25) 0%, transparent 70%)" }}
          />
          <motion.div
            animate={{ scale: [1, 1.2, 1], opacity: [0.12, 0.22, 0.12] }}
            transition={{ duration: 10, repeat: Infinity, ease: "easeInOut", delay: 2 }}
            className="absolute bottom-0 right-0 w-[600px] h-[600px] rounded-full"
            style={{ background: "radial-gradient(circle, rgba(16,185,129,0.18) 0%, transparent 70%)" }}
          />
          <motion.div
            animate={{ x: [0, 30, 0], y: [0, -20, 0], opacity: [0.08, 0.14, 0.08] }}
            transition={{ duration: 12, repeat: Infinity, ease: "easeInOut", delay: 1 }}
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] rounded-full"
            style={{ background: "radial-gradient(ellipse, rgba(0,31,63,0.6) 0%, transparent 70%)" }}
          />
          {/* Floating particles */}
          {[...Array(6)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute rounded-full bg-gold-400/20"
              style={{
                width: 4 + (i % 3) * 4,
                height: 4 + (i % 3) * 4,
                top: `${15 + i * 13}%`,
                left: `${10 + i * 14}%`,
              }}
              animate={{ y: [0, -18, 0], opacity: [0.2, 0.5, 0.2] }}
              transition={{ duration: 4 + i, repeat: Infinity, ease: "easeInOut", delay: i * 0.7 }}
            />
          ))}
        </div>

        {/* ZATCA countdown badge */}
        <motion.div
          initial={{ opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="relative z-10 mb-6"
        >
          <Badge className="border-gold-500/40 bg-gold-500/10 text-gold-300 text-xs px-4 py-1.5 rounded-full backdrop-blur-sm">
            <span className="inline-block w-2 h-2 rounded-full bg-gold-400 me-2 animate-pulse" />
            {isAr ? "ZATCA Wave 24 — الموعد النهائي يونيو 2026" : "ZATCA Wave 24 — Deadline June 2026"}
          </Badge>
        </motion.div>

        {/* Glassmorphism hero card */}
        <motion.div
          variants={stagger}
          initial="hidden"
          animate={heroControls}
          className="relative z-10 w-full max-w-3xl text-center"
        >
          <motion.div
            variants={fadeUp}
            className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-lg px-8 py-12 md:px-16 md:py-16 shadow-2xl"
            style={{ boxShadow: "0 8px 64px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.07)" }}
          >
            <motion.h1
              variants={fadeUp}
              custom={1}
              className="font-display text-[clamp(1.875rem,5vw,3rem)] sm:text-[clamp(2.25rem,4vw,3.5rem)] md:text-[clamp(2.5rem,3vw,4rem)] font-bold leading-[1.1] tracking-[-0.02em]"
              style={{ fontFamily: "'Space Grotesk', 'IBM Plex Arabic', sans-serif" }}
            >
              {isAr ? (
                <>
                  حوّل إشارات شركتك إلى{" "}
                  <span className="bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent">
                    تنفيذ حقيقي يمكن إثباته
                  </span>
                </>
              ) : (
                <>
                  Turn your company signals into{" "}
                  <span className="bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent">
                    real, provable execution
                  </span>
                </>
              )}
            </motion.h1>

            <motion.p
              variants={fadeUp}
              custom={2}
              className="mt-5 text-base md:text-lg text-white/70 max-w-xl mx-auto leading-relaxed"
            >
              {isAr
                ? "كشف تسرّب الإيراد · حوكمة الذكاء الاصطناعي · امتثال ZATCA & PDPL — كل شيء في منصة واحدة محكومة بالدليل."
                : "Revenue leakage detection · AI governance · ZATCA & PDPL compliance — all in one evidence-governed platform."}
            </motion.p>

            <motion.div
              variants={fadeUp}
              custom={3}
              className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3"
            >
              <Button
                asChild
                size="lg"
                className="w-full sm:w-auto bg-gradient-to-r from-gold-500 to-gold-400 text-navy-500 font-bold hover:from-gold-400 hover:to-gold-300 shadow-lg shadow-gold-500/25 text-base h-13 px-8"
              >
                <Link href={`${base}/offer/lead-intelligence-sprint`}>
                  {isAr ? "ابدأ تشخيصك المجاني" : "Start Free Diagnostic"}
                </Link>
              </Button>
              <Button
                asChild
                size="lg"
                variant="outline"
                className="w-full sm:w-auto border-gold-500/30 bg-gold-500/10 text-gold-400 hover:bg-gold-500/20 backdrop-blur-sm text-base h-13 px-8"
              >
                <Link href={`${base}/solutions`}>
                  {isAr ? "استكشف حلول القطاعات" : "Explore Sector Solutions"}
                </Link>
              </Button>
              <Button
                asChild
                size="lg"
                variant="outline"
                className="w-full sm:w-auto border-white/20 text-white hover:bg-white/10 backdrop-blur-sm text-base h-13 px-8"
              >
                <Link href={`${base}/market-control`}>
                  {isAr ? "لوحة السيطرة" : "Market Control"}
                </Link>
              </Button>
              <Button
                asChild
                size="lg"
                variant="outline"
                className="w-full sm:w-auto border-white/20 text-white hover:bg-white/10 backdrop-blur-sm text-base h-13 px-8"
              >
                <Link href={`${base}/demo`}>
                  {isAr ? "شاهد كيف يعمل" : "See How It Works"}
                </Link>
              </Button>
            </motion.div>

            <motion.p
              variants={fadeUp}
              custom={4}
              className="mt-5 text-xs text-white/40"
            >
              {isAr
                ? "لا إرسال آلي · لا ادّعاء إيراد قبل الدفع · PDPL compliant"
                : "No automated outbound · No revenue claims before payment · PDPL compliant"}
            </motion.p>
          </motion.div>
        </motion.div>

        {/* Scroll cue */}
        <motion.div
          className="absolute bottom-8 left-1/2 -translate-x-1/2"
          animate={{ y: [0, 8, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <div className="w-5 h-8 rounded-full border border-white/20 flex items-start justify-center pt-1.5">
            <div className="w-1 h-2 rounded-full bg-white/40" />
          </div>
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* LOGOS / SOCIAL PROOF STRIP                                          */}
      {/* ------------------------------------------------------------------ */}
      <section className="bg-navy-600 border-y border-white/5 py-10 overflow-hidden">
        <p className="text-center text-xs font-semibold text-white/40 uppercase tracking-widest mb-6">
          {isAr ? "ماذا نبني" : "What we build"}
        </p>
        <div className="relative">
          <motion.div
            className="flex gap-10 items-center"
            animate={{ x: isAr ? [0, "50%"] : [0, "-50%"] }}
            transition={{ duration: 22, repeat: Infinity, ease: "linear" }}
          >
            {[...LOGOS, ...LOGOS].map((logo, i) => (
              <div
                key={i}
                className="flex-shrink-0 flex items-center gap-3 px-6 py-3 rounded-xl border border-white/8 bg-white/4 backdrop-blur-sm"
              >
                <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-gold-500/30 to-gold-400/10 border border-gold-500/20 flex items-center justify-center text-gold-400 font-bold text-sm">
                  {logo.initials}
                </div>
                <span className="text-white/60 text-sm whitespace-nowrap font-medium">{logo.name}</span>
                <span className="text-emerald-400 text-xs">✓</span>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* FEATURES GRID                                                       */}
      {/* ------------------------------------------------------------------ */}
      <section className="py-20 px-4 max-w-6xl mx-auto">
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="text-center mb-12"
        >
          <motion.p variants={fadeUp} className="text-gold-400 text-sm font-semibold uppercase tracking-widest mb-3">
            {isAr ? "المنصة" : "Platform"}
          </motion.p>
          <motion.h2 variants={fadeUp} custom={1} className="text-3xl md:text-4xl font-bold">
            {isAr ? "كل ما تحتاجه لتنمية إيراداتك" : "Everything you need to grow revenue"}
          </motion.h2>
          <motion.p variants={fadeUp} custom={2} className="mt-3 text-white/60 max-w-xl mx-auto">
            {isAr
              ? "ست أدوات متكاملة تعمل معاً لتحقيق نتائج قابلة للقياس."
              : "Six integrated tools working together for measurable results."}
          </motion.p>
        </motion.div>

        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-40px" }}
          className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
        >
          {FEATURES.map((f, i) => (
            <motion.div
              key={f.en}
              variants={fadeUp}
              custom={i}
              whileHover={{ y: -4, transition: { duration: 0.2 } }}
              className="group rounded-2xl border border-white/8 bg-white/4 backdrop-blur-sm p-6 hover:border-gold-500/30 hover:bg-white/7 transition-colors cursor-default"
              style={{ boxShadow: "inset 0 1px 0 rgba(255,255,255,0.05)" }}
            >
              <div className="text-3xl mb-4">{f.icon}</div>
              <h3 className="font-bold text-lg mb-0.5">{isAr ? f.ar : f.en}</h3>
              <p className="text-xs text-white/50 font-medium mb-2">{isAr ? f.en : f.ar}</p>
              <p className="text-sm text-white/65 leading-relaxed">{isAr ? f.descAr : f.descEn}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* ANIMATED STATS                                                      */}
      {/* ------------------------------------------------------------------ */}
      <section
        className="py-20 px-4"
        style={{ background: "linear-gradient(180deg, #000d1a 0%, #001528 50%, #000d1a 100%)" }}
      >
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="max-w-4xl mx-auto text-center mb-12"
        >
          <motion.h2 variants={fadeUp} className="text-3xl md:text-4xl font-bold">
            {isAr ? "أرقام تتحدث بنفسها" : "Numbers that speak for themselves"}
          </motion.h2>
        </motion.div>

        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-40px" }}
          className="grid grid-cols-2 lg:grid-cols-4 gap-6 max-w-4xl mx-auto"
        >
          {STATS.map((s, i) => (
            <motion.div
              key={s.labelEn}
              variants={fadeUp}
              custom={i}
              className="text-center rounded-2xl border border-white/8 bg-white/4 backdrop-blur-sm py-8 px-4"
            >
              <div className="text-4xl md:text-5xl font-bold bg-gradient-to-br from-gold-300 to-gold-500 bg-clip-text text-transparent leading-none mb-3">
                {s.target <= 100 && s.labelEn.includes("Uptime") ? (
                  <span><AnimatedNumber target={99.9} suffix="%" /></span>
                ) : s.target <= 100 && s.labelEn.includes("Growth") ? (
                  <span><AnimatedNumber target={3.2} suffix="x" /></span>
                ) : s.target === 48 ? (
                  <span><AnimatedNumber target={48} suffix="h" /></span>
                ) : (
                  <span>+<AnimatedNumber target={500} /></span>
                )}
              </div>
              <p className="text-white/70 text-sm font-medium">{isAr ? s.labelAr : s.labelEn}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* PRICING                                                             */}
      {/* ------------------------------------------------------------------ */}
      <section className="py-20 px-4 max-w-6xl mx-auto">
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="text-center mb-12"
        >
          <motion.p variants={fadeUp} className="text-gold-400 text-sm font-semibold uppercase tracking-widest mb-3">
            {isAr ? "الأسعار" : "Pricing"}
          </motion.p>
          <motion.h2 variants={fadeUp} custom={1} className="text-3xl md:text-4xl font-bold">
            {isAr ? "خطة مناسبة لكل مرحلة" : "A plan for every stage"}
          </motion.h2>
          <motion.p variants={fadeUp} custom={2} className="mt-3 text-white/60 max-w-lg mx-auto">
            {isAr ? "ابدأ بتشخيص واحد، ثم قرر." : "Start with one diagnostic, then decide."}
          </motion.p>
        </motion.div>

        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-40px" }}
          className="grid gap-6 md:grid-cols-3 items-start"
        >
          {PRICING.map((plan, i) => (
            <motion.div
              key={plan.tierEn}
              variants={fadeUp}
              custom={i}
              className={`relative rounded-2xl border p-8 flex flex-col gap-5 ${
                plan.popular
                  ? "border-gold-500/50 bg-gradient-to-b from-gold-500/8 to-transparent shadow-xl shadow-gold-500/10"
                  : "border-white/8 bg-white/4"
              } backdrop-blur-sm`}
              style={plan.popular ? { boxShadow: "0 0 40px rgba(212,175,55,0.12), inset 0 1px 0 rgba(255,255,255,0.07)" } : {}}
            >
              {plan.popular && (
                <div className={`absolute -top-3.5 ${isAr ? "left-6" : "right-6"}`}>
                  <Badge className="bg-gold-500 text-navy-500 border-0 font-bold px-3 py-1 text-xs">
                    {isAr ? "الأكثر شيوعاً" : "Most Popular"}
                  </Badge>
                </div>
              )}

              <div>
                <p className="text-white/50 text-sm font-medium mb-1">{isAr ? plan.tierAr : plan.tierEn}</p>
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl font-bold">{isAr ? plan.priceAr : plan.priceEn}</span>
                  {plan.periodAr && (
                    <span className="text-white/50 text-sm">{isAr ? plan.periodAr : plan.periodEn}</span>
                  )}
                </div>
              </div>

              <ul className="space-y-2.5 flex-1">
                {(isAr ? plan.featuresAr : plan.featuresEn).map((feat) => (
                  <li key={feat} className="flex items-start gap-2 text-sm text-white/75">
                    <span className="text-emerald-400 mt-0.5 flex-shrink-0 text-base leading-none">✓</span>
                    {feat}
                  </li>
                ))}
              </ul>

              <Button
                asChild
                size="lg"
                className={`w-full font-semibold ${
                  plan.popular
                    ? "bg-gradient-to-r from-gold-500 to-gold-400 text-navy-500 hover:from-gold-400 hover:to-gold-300 shadow-md shadow-gold-500/20"
                    : "bg-white/8 border border-white/15 text-white hover:bg-white/14"
                }`}
              >
                <Link href={`${base}${plan.href}`}>
                  {isAr ? plan.ctaAr : plan.ctaEn}
                </Link>
              </Button>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      <section className="py-12 px-4 max-w-4xl mx-auto">
        <InteractiveTechDemo />
      <HermesAgentWidget />
      </section>

      {/* EXECUTION LOOP — SIGNAL → DECISION → ACTION → PROOF */}
      <section className="py-16 px-4 max-w-5xl mx-auto">
        <div className="text-center mb-8">
          <p className="text-cyan-400 text-sm font-semibold uppercase tracking-widest mb-3">
            {isAr ? "حلقة التنفيذ" : "Execution Loop"}
          </p>
          <h2 className="text-2xl md:text-3xl font-bold">
            {isAr ? "إشارة → قرار → إجراء → إثبات" : "Signal → Decision → Action → Proof"}
          </h2>
          <p className="text-white/50 text-sm mt-2 max-w-xl mx-auto">
            {isAr ? "كل إشارة تشغيلية تمر عبر قرار موثق، ثم إجراء محكوم، ثم إثبات يمكن قبوله" : "Every operational signal goes through a documented decision, then governed action, then acceptable proof"}
          </p>
        </div>
        <div className="grid gap-4 md:grid-cols-4">
          {[
            { step: "01", ar: "إشارة", en: "Signal", descAr: "إشارة تشغيلية حقيقية", descEn: "Real operational signal", color: "border-cyan-500/20 bg-cyan-500/10" },
            { step: "02", ar: "قرار", en: "Decision", descAr: "دليل + أولوية + اقتصاديات", descEn: "Evidence + priority + economics", color: "border-gold-500/20 bg-gold-500/10" },
            { step: "03", ar: "إجراء", en: "Action", descAr: "تنفيذ محكوم بصلاحية واضحة", descEn: "Governed execution with clear authority", color: "border-emerald-500/20 bg-emerald-500/10" },
            { step: "04", ar: "إثبات", en: "Proof", descAr: "خط أساس → دليل → قبول", descEn: "Baseline → evidence → acceptance", color: "border-violet-500/20 bg-violet-500/10" },
          ].map((s) => (
            <div key={s.step} className={`rounded-2xl border p-5 backdrop-blur card-interactive ${s.color}`}>
              <div className="text-xs font-bold text-white/40">{s.step}</div>
              <div className="font-bold mt-1">{isAr ? s.ar : s.en}</div>
              <div className="text-xs text-white/50 mt-1">{isAr ? s.descAr : s.descEn}</div>
            </div>
          ))}
        </div>
      </section>

      {/* FREE DIAGNOSTICS — EVIDENCE-FIRST                                           */}
      <section className="py-20 px-4 max-w-6xl mx-auto">
        <div className="text-center mb-10">
          <p className="text-gold-400 text-sm font-semibold uppercase tracking-widest mb-3">
            {isAr ? "تشخيصات مجانية قائمة على الدليل" : "Evidence-led Free Diagnostics"}
          </p>
          <h2 className="text-3xl md:text-4xl font-bold">
            {isAr ? "تشخيص مجاني يديره 5 وكلاء" : "Free Diagnostic Managed by 5 Agents"}
          </h2>
          <p className="text-white/50 mt-3 text-sm">
            {isAr ? "بداية مجانية عبر 20 قطاعًا — ثم مراجعة بشرية قبل أي نطاق مدفوع أو أثر خارجي" : "Free starting diagnostics across 20 sectors — with human review before any paid scope or external effect"}
          </p>
        </div>
        <div className="grid gap-6 md:grid-cols-3">
          {[
            { ar: "تشخيص مجاني 7 أيام — Proof Pack", en: "Free 7-Day Diagnostic — Proof Pack", valAr: "خريطة تسرّب محتمل + خط أساس + اختناقات", valEn: "Potential leakage map + baseline + bottlenecks", agents: "dealix-pm · dealix-sales · dealix-delivery · dealix-engineer · dealix-content" },
            { ar: "تقييم جاهزية AI مجاني", en: "Free AI Readiness Scan", valAr: "حوكمة AI + اقتصاديات", valEn: "AI governance + economics", agents: "dealix-engineer · dealix-pm" },
            { ar: "فحص جاهزية ZATCA مجاني", en: "Free ZATCA Readiness Check", valAr: "تشخيص فاتورة + تكامل", valEn: "Fatoora diagnostic + integration", agents: "dealix-engineer" },
          ].map((offer) => (
            <div key={offer.en} className="rounded-2xl border border-gold-500/20 bg-gradient-to-br from-gold-500/10 to-white/5 p-6 backdrop-blur">
              <h3 className="font-bold text-gold-400">{isAr ? offer.ar : offer.en}</h3>
              <p className="text-sm text-white/60 mt-1">{isAr ? offer.valAr : offer.valEn}</p>
              <p className="text-xs text-white/40 mt-3">{offer.agents} • {isAr ? "مجاني" : "Free"} • {isAr ? "لا وعود بنتيجة قبل القياس" : "No outcome claim before measurement"}</p>
            </div>
          ))}
        </div>
        <div className="mt-8 text-center">
          <Button asChild variant="outline" className="border-gold-500/30 text-gold-300 hover:bg-gold-500/10">
            <Link href={`${base}/solutions`}>
              {isAr ? "استعرض حلول 20 قطاعًا" : "Explore solutions across 20 sectors"}
            </Link>
          </Button>
        </div>
      </section>

      {/* TESTIMONIALS                                                        */}
      {/* ------------------------------------------------------------------ */}
      <section
        className="py-20 px-4"
        style={{ background: "linear-gradient(180deg, #000d1a 0%, #001528 100%)" }}
      >
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="max-w-6xl mx-auto"
        >
          <motion.div variants={fadeUp} className="text-center mb-12">
            <p className="text-gold-400 text-sm font-semibold uppercase tracking-widest mb-3">
              {isAr ? "كيف نثبت القيمة" : "How we prove value"}
            </p>
            <h2 className="text-3xl md:text-4xl font-bold">
              {isAr ? "منهجية الإثبات المُحكَمة" : "Governed proof methodology"}
            </h2>
          </motion.div>

          <motion.div
            variants={stagger}
            className="grid gap-6 md:grid-cols-3"
          >
            {TESTIMONIALS.map((t, i) => (
              <motion.div
                key={t.nameEn}
                variants={fadeUp}
                custom={i}
                className="rounded-2xl border border-white/8 bg-white/4 backdrop-blur-sm p-7 flex flex-col gap-4"
                style={{ boxShadow: "inset 0 1px 0 rgba(255,255,255,0.05)" }}
              >
                <StarRating count={t.stars} />
                <p className="text-white/80 text-sm leading-relaxed flex-1">
                  &ldquo;{isAr ? t.quoteAr : t.quoteEn}&rdquo;
                </p>
                <div className="flex items-center gap-3 pt-2 border-t border-white/8">
                  <div className="w-9 h-9 rounded-full bg-gradient-to-br from-gold-500/40 to-emerald-600/30 flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
                    {(isAr ? t.nameAr : t.nameEn)[0]}
                  </div>
                  <div>
                    <p className="text-sm font-semibold leading-tight">{isAr ? t.nameAr : t.nameEn}</p>
                    <p className="text-xs text-white/50 mt-0.5">{isAr ? t.companyAr : t.companyEn}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* TRUST CENTER STRIP                                                  */}
      {/* ------------------------------------------------------------------ */}
      <section className="py-10 px-4 border-y border-white/5 bg-navy-600 overflow-x-auto">
        <div className="flex gap-4 justify-start md:justify-center min-w-max mx-auto px-2">
          {TRUST_BADGES.map((badge) => (
            <div
              key={badge.en}
              className="flex items-center gap-2 px-5 py-3 rounded-xl border border-white/8 bg-white/4 backdrop-blur-sm flex-shrink-0"
            >
              <span className="text-xl">{badge.icon}</span>
              <span className="text-sm font-medium text-white/80 whitespace-nowrap">
                {isAr ? badge.ar : badge.en}
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* CTA SECTION                                                         */}
      {/* ------------------------------------------------------------------ */}
      <section
        className="py-24 px-4 relative overflow-hidden"
        style={{ background: "linear-gradient(135deg, #001830 0%, #002040 50%, #001830 100%)" }}
      >
        <div
          aria-hidden
          className="absolute inset-0 pointer-events-none"
          style={{ background: "radial-gradient(ellipse 80% 60% at 50% 50%, rgba(212,175,55,0.08) 0%, transparent 70%)" }}
        />
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="relative z-10 max-w-2xl mx-auto text-center"
        >
          <motion.h2
            variants={fadeUp}
            className="text-3xl md:text-5xl font-bold leading-tight mb-5"
            style={{ fontFamily: "'Noto Sans Arabic', 'IBM Plex Arabic', sans-serif" }}
          >
            {isAr ? (
              <>
                ابدأ رحلتك نحو{" "}
                <span className="bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent">
                  إيراد أكثر
                </span>
              </>
            ) : (
              <>
                Start your journey to{" "}
                <span className="bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent">
                  more revenue
                </span>
              </>
            )}
          </motion.h2>

          <motion.p variants={fadeUp} custom={1} className="text-white/60 mb-8 text-lg">
            {isAr
              ? "أرسل طلب الفحص المجاني؛ نسجله كـ inbound للمراجعة البشرية بدون دفع أو إرسال تسويقي تلقائي."
              : "Submit a free diagnostic request; it is captured as inbound for human review with no payment or automated marketing send."}
          </motion.p>

          <motion.form
            variants={fadeUp}
            custom={2}
            onSubmit={handleEmailSubmit}
            className={`flex flex-col sm:flex-row gap-3 max-w-md mx-auto ${isAr ? "sm:flex-row-reverse" : ""}`}
          >
            <AnimatePresence mode="wait">
              {!emailSubmitted ? (
                <motion.div
                  key="form"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="grid sm:grid-cols-2 gap-3 w-full"
                >
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                    autoComplete="name"
                    placeholder={isAr ? "الاسم" : "Name"}
                    className="h-12 rounded-xl bg-white/8 border border-white/15 px-4 text-white placeholder-white/40 text-sm focus:outline-none focus:border-gold-500/60 focus:bg-white/12 transition-colors"
                  />
                  <input
                    type="text"
                    value={company}
                    onChange={(e) => setCompany(e.target.value)}
                    required
                    autoComplete="organization"
                    placeholder={isAr ? "الشركة" : "Company"}
                    className="h-12 rounded-xl bg-white/8 border border-white/15 px-4 text-white placeholder-white/40 text-sm focus:outline-none focus:border-gold-500/60 focus:bg-white/12 transition-colors"
                  />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    autoComplete="email"
                    placeholder={isAr ? "البريد الإلكتروني للشركة" : "Work email address"}
                    className="h-12 rounded-xl bg-white/8 border border-white/15 px-4 text-white placeholder-white/40 text-sm focus:outline-none focus:border-gold-500/60 focus:bg-white/12 transition-colors"
                  />
                  <Button
                    type="submit"
                    size="lg"
                    disabled={emailSubmitting}
                    className="h-12 px-7 bg-gradient-to-r from-gold-500 to-gold-400 text-navy-500 font-bold hover:from-gold-400 hover:to-gold-300 whitespace-nowrap shadow-lg shadow-gold-500/25"
                  >
                    {emailSubmitting ? (isAr ? "جارٍ التسجيل…" : "Registering…") : (isAr ? "ابدأ مجاناً" : "Start Free")}
                  </Button>
                </motion.div>
              ) : (
                <motion.div
                  key="thanks"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="w-full text-center py-3 rounded-xl border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 font-medium text-sm"
                >
                  {isAr ? `تم تسجيل طلب الفحص للمراجعة البشرية${leadRef ? ` — المرجع: ${leadRef}` : ""}. لا دفع أو إرسال تسويقي تلقائي.` : `Diagnostic request registered for human review${leadRef ? ` — ref: ${leadRef}` : ""}. No payment or automated marketing send.`}
                </motion.div>
              )}
            </AnimatePresence>
          </motion.form>

          {emailError && (
            <p className="mt-3 text-sm text-red-300" role="alert">{emailError}</p>
          )}

          <motion.p variants={fadeUp} custom={3} className="mt-4 text-xs text-white/35">
            {isAr
              ? "إرسال هذا النموذج طلب inbound للفحص فقط، ولا يُعد موافقة على التسويق. نعالج البيانات وفق سياسة الخصوصية والضوابط المعمول بها."
              : "Submitting this form is an inbound diagnostic request only, not marketing consent. Data is handled under our privacy policy and applicable controls."}
          </motion.p>
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* FOOTER                                                              */}
      {/* ------------------------------------------------------------------ */}
      <footer
        className="py-12 px-4 border-t border-white/6"
        style={{ background: "#000d1a" }}
      >
        <div className="max-w-6xl mx-auto">
          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4 mb-10">
            {/* Brand */}
            <div className="lg:col-span-2">
              <div className="text-xl font-bold bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent mb-3">
                Dealix
              </div>
              <p className="text-white/50 text-sm leading-relaxed max-w-xs">
                {isAr
                  ? "منصة الإيرادات بالذكاء الاصطناعي للشركات السعودية. محكومة بالدليل، ملتزمة بـ PDPL."
                  : "AI revenue platform for Saudi enterprises. Evidence-governed, PDPL compliant."}
              </p>
            </div>

            {/* Links */}
            <div>
              <p className="text-white/30 text-xs uppercase tracking-widest font-semibold mb-3">
                {isAr ? "المنتج" : "Product"}
              </p>
              <ul className="space-y-2 text-sm text-white/55">
                {[
                  { ar: "التشخيص", en: "Diagnostic", href: "/dealix-diagnostic" },
                  { ar: "Proof Pack", en: "Proof Pack", href: "/proof-pack" },
                  { ar: "الأسعار", en: "Pricing", href: "#pricing" },
                  { ar: "الشركاء", en: "Partners", href: "/partners" },
                ].map((link) => (
                  <li key={link.href}>
                    <Link href={`${base}${link.href}`} className="hover:text-gold-400 transition-colors">
                      {isAr ? link.ar : link.en}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <p className="text-white/30 text-xs uppercase tracking-widest font-semibold mb-3">
                {isAr ? "الشركة" : "Company"}
              </p>
              <ul className="space-y-2 text-sm text-white/55">
                {[
                  { ar: "من نحن", en: "About", href: "/about" },
                  { ar: "احجز جلسة اكتشاف", en: "Book discovery", href: "/book-call" },
                  { ar: "سياسة الخصوصية", en: "Privacy", href: "/privacy" },
                ].map((link) => (
                  <li key={link.href}>
                    <Link href={`${base}${link.href}`} className="hover:text-gold-400 transition-colors">
                      {isAr ? link.ar : link.en}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="border-t border-white/6 pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-white/30">
            <p>
              {isAr
                ? `© ${new Date().getFullYear()} Dealix. جميع الحقوق محفوظة.`
                : `© ${new Date().getFullYear()} Dealix. All rights reserved.`}
            </p>
            <div className="flex gap-4">
              <span className="text-emerald-500/70">PDPL</span>
              <span className="text-gold-500/70">ZATCA Readiness</span>
              <span className="text-white/40">Saudi-First</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
