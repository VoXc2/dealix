import type { Metadata } from "next";

const SITE = "https://dealix.me";
const OG_IMAGE = [{ url: `${SITE}/brand/og-dealix.svg`, width: 1200, height: 630, alt: "Dealix — Saudi B2B Revenue OS" }];

type FunnelKey = "diagnostic" | "proof-pack" | "risk-score" | "partners" | "services" | "learn" | "privacy";

const FUNNEL_META: Record<FunnelKey, { path: string; ar: { title: string; desc: string }; en: { title: string; desc: string } }> = {
  diagnostic: {
    path: "/dealix-diagnostic",
    ar: { title: "Dealix — تشخيص 7 أيام بالأدلة", desc: "تشخيص محكوم لإيرادات شركتك — Proof Pack كامل خلال 7 أيام. PDPL & ZATCA compliant." },
    en: { title: "Dealix — 7-Day Evidence-Governed Diagnostic", desc: "Governed diagnostic for your company's revenue — Full Proof Pack in 7 days. PDPL & ZATCA compliant." },
  },
  "proof-pack": {
    path: "/proof-pack",
    ar: { title: "Dealix — عيّنة Proof Pack", desc: "حزمة إثبات كاملة بأربعة أقسام ومستويات L0-L5 — لا upsell قبل الإثبات. شاهد العيّنة." },
    en: { title: "Dealix — Proof Pack Sample", desc: "Complete proof bundle with four sections and L0-L5 levels — no upsell before proof. View the sample." },
  },
  "risk-score": {
    path: "/risk-score",
    ar: { title: "Dealix — AI & Revenue Ops Risk Score", desc: "احسب نقاط مخاطر العمليات لشركتك مجاناً — تشخيص فوري لجاهزية ZATCA وPDPL والإيراد." },
    en: { title: "Dealix — AI & Revenue Ops Risk Score", desc: "Calculate your company's operations risk score for free — instant ZATCA, PDPL, and revenue readiness diagnostic." },
  },
  partners: {
    path: "/partners",
    ar: { title: "Dealix — برنامج الشركاء 15-30%", desc: "انضم لشبكة شركاء Dealix — Referral أو Implementation أو Co-sell. عمولة على كل تشخيص وRetainer." },
    en: { title: "Dealix — Partner Program 15-30%", desc: "Join Dealix partner network — Referral, Implementation, or Co-sell. Commission on every diagnostic and retainer." },
  },
  services: {
    path: "/services",
    ar: { title: "Dealix — خدمات وأسعار · سلم العروض الخمسة", desc: "من التشخيص المجاني إلى مشاريع AI المخصصة — خمسة مستويات تبني على الإثبات. أسعار بالريال السعودي." },
    en: { title: "Dealix — Services & Pricing · Five-Tier Offer Ladder", desc: "From free diagnostic to custom AI projects — five tiers built on proof. All prices in SAR." },
  },
  learn: {
    path: "/learn",
    ar: { title: "Dealix — مكتبة Revenue Ops بالعربية", desc: "تعلّم Revenue Ops، حوكمة AI، PDPL، وZATCA — محتوى عربي متخصص لشركات B2B السعودية." },
    en: { title: "Dealix — Arabic Revenue Ops Library", desc: "Learn Revenue Ops, AI governance, PDPL, and ZATCA — specialized Arabic content for Saudi B2B companies." },
  },
  privacy: {
    path: "/privacy",
    ar: { title: "Dealix — سياسة الخصوصية وPDPL", desc: "Dealix مبني أصلاً لـ PDPL — لا outreach بارد، لا scraping، موافقة قبل أي إرسال خارجي." },
    en: { title: "Dealix — Privacy & PDPL Policy", desc: "Dealix is built natively for PDPL — no cold outreach, no scraping, approval before any external send." },
  },
};

export function buildFunnelMetadata(locale: string, key: FunnelKey): Metadata {
  const isAr = locale === "ar";
  const meta = FUNNEL_META[key];
  const content = isAr ? meta.ar : meta.en;
  const url = `${SITE}/${locale}${meta.path}`;
  return {
    title: content.title,
    description: content.desc,
    openGraph: { title: content.title, description: content.desc, url, images: OG_IMAGE },
    twitter: { card: "summary_large_image", title: content.title, description: content.desc },
    alternates: { canonical: url, languages: { ar: `${SITE}/ar${meta.path}`, en: `${SITE}/en${meta.path}` } },
    icons: { icon: "/brand/logo-mark.svg" },
  };
}

export function buildHomeMetadata(locale: string): Metadata {
  const isAr = locale === "ar";
  const title = isAr
    ? "Dealix — نظام تشغيل الإيرادات B2B السعودي | PDPL · ZATCA"
    : "Dealix — Saudi B2B Revenue Operating System | PDPL · ZATCA";
  const description = isAr
    ? "وحّد قرار الإيراد. أثبت كل لمسة. وسّع فقط بعد Proof. مبني للسوق السعودي — PDPL أصيل، ZATCA جاهز، موافقة أولاً."
    : "Unify revenue decisions. Prove every touch. Expand only after proof. Built for Saudi market — PDPL native, ZATCA ready, approval-first.";
  const url = `${SITE}/${locale}`;
  return {
    title,
    description,
    keywords: isAr
      ? ["Revenue Ops", "PDPL", "ZATCA", "B2B Saudi", "حوكمة AI", "نظام الإيرادات"]
      : ["Revenue Ops", "PDPL", "ZATCA", "B2B Saudi Arabia", "AI Governance", "Revenue OS"],
    openGraph: { title, description, url, images: OG_IMAGE, type: "website", locale: isAr ? "ar_SA" : "en_US" },
    twitter: { card: "summary_large_image", title, description },
    alternates: { canonical: url, languages: { ar: `${SITE}/ar`, en: `${SITE}/en` } },
    icons: { icon: "/brand/logo-mark.svg", apple: "/brand/logo-mark.svg" },
    robots: { index: true, follow: true },
  };
}

export function buildArticleMetadata(locale: string, titleAr: string, titleEn: string, descAr: string, descEn: string, slug: string): Metadata {
  const isAr = locale === "ar";
  const title = isAr ? titleAr : titleEn;
  const description = isAr ? descAr : descEn;
  const url = `${SITE}/${locale}/learn/${slug}`;
  return {
    title: `${title} — Dealix`,
    description,
    openGraph: { title, description, url, images: OG_IMAGE, type: "article" },
    alternates: { canonical: url, languages: { ar: `${SITE}/ar/learn/${slug}`, en: `${SITE}/en/learn/${slug}` } },
  };
}
