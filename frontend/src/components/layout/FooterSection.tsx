"use client";

import Link from "next/link";
import { useLocale } from "next-intl";

/* ─── Data ──────────────────────────────────────────── */

type NavColumn = {
  titleAr: string;
  titleEn: string;
  links: { ar: string; en: string; href: string }[];
};

const NAV_COLUMNS: NavColumn[] = [
  {
    titleAr: "الخدمات",
    titleEn: "Services",
    links: [
      { ar: "تشخيص مجاني", en: "Free Diagnostic", href: "/risk-score" },
      { ar: "Revenue Intelligence Sprint", en: "Revenue Intelligence Sprint", href: "/dealix-diagnostic" },
      { ar: "Agency Proof Pack", en: "Agency Proof Pack", href: "/dealix-diagnostic" },
      { ar: "Managed Ops Retainer", en: "Managed Ops Retainer", href: "/dealix-diagnostic" },
      { ar: "Custom AI Project", en: "Custom AI Project", href: "/dealix-diagnostic" },
    ],
  },
  {
    titleAr: "تعلّم",
    titleEn: "Learn",
    links: [
      { ar: "مكتبة المعرفة", en: "Knowledge Library", href: "/learn" },
      { ar: "دليل PDPL 2026", en: "PDPL Guide 2026", href: "/learn/pdpl-guide-saudi-b2b-2026" },
      { ar: "دليل ZATCA Wave 24", en: "ZATCA Wave 24 Guide", href: "/learn/zatca-wave-24-guide" },
      { ar: "حوكمة AI في B2B", en: "AI Governance in B2B", href: "/learn/ai-governance-saudi-b2b" },
      { ar: "كشف تسريب الإيراد", en: "Revenue Leakage Detection", href: "/learn/revenue-leakage-detection" },
    ],
  },
  {
    titleAr: "الشركة",
    titleEn: "Company",
    links: [
      { ar: "من نحن", en: "About Us", href: "/about" },
      { ar: "قصص النجاح", en: "Case Studies", href: "/about" },
      { ar: "الشركاء", en: "Partners", href: "/partners" },
      { ar: "تسعير الخدمات", en: "Pricing", href: "/pricing" },
    ],
  },
  {
    titleAr: "القانوني",
    titleEn: "Legal",
    links: [
      { ar: "الثقة والامتثال", en: "Trust & Compliance", href: "/trust" },
      { ar: "سياسة الخصوصية", en: "Privacy Policy", href: "/privacy" },
      { ar: "شروط الخدمة", en: "Terms of Service", href: "/privacy" },
      { ar: "PDPL — حقوقك", en: "PDPL — Your Rights", href: "/trust" },
    ],
  },
];

const TRUST_SIGNALS = [
  { ar: "PDPL أصيل", en: "PDPL Compliant" },
  { ar: "ZATCA جاهز", en: "ZATCA Ready" },
  { ar: "Approval-First", en: "Approval-First" },
  { ar: "لا outreach بارد", en: "No Cold Outreach" },
  { ar: "Audit Trail كامل", en: "Full Audit Trail" },
];

/* ─── Component ─────────────────────────────────────── */

interface FooterSectionProps {
  className?: string;
}

export function FooterSection({ className = "" }: FooterSectionProps) {
  const locale = useLocale();
  const isAr = locale === "ar";
  const base = `/${locale}`;
  const currentYear = new Date().getFullYear();

  return (
    <footer
      className={`border-t border-border/50 bg-background ${className}`}
      dir={isAr ? "rtl" : "ltr"}
    >
      <div className="mx-auto max-w-6xl px-6 py-12">

        {/* ── Top section ── */}
        <div className="grid gap-8 lg:grid-cols-5 mb-10">

          {/* Brand column */}
          <div className={`lg:col-span-1 ${isAr ? "text-right" : "text-left"}`}>
            <Link href={base} className="inline-flex items-center gap-2 mb-3">
              <div className="w-8 h-8 rounded-lg bg-[#0A1628] flex items-center justify-center">
                <span className="text-[#C9974B] font-bold text-sm">D</span>
              </div>
              <span className="font-bold text-lg text-foreground">Dealix</span>
            </Link>
            <p className="text-xs text-muted-foreground leading-relaxed">
              {isAr
                ? "عمليات AI محكومة للسوق السعودي"
                : "Governed AI Operations for the Saudi Market"}
            </p>
            <p className="mt-2 text-xs text-muted-foreground leading-relaxed">
              {isAr
                ? "B2B Revenue OS · رؤية 2030 · PDPL · ZATCA"
                : "B2B Revenue OS · Vision 2030 · PDPL · ZATCA"}
            </p>

            {/* Contact */}
            <div className="mt-4 space-y-1">
              <a
                href="mailto:hello@dealix.me"
                className="block text-xs text-muted-foreground hover:text-foreground transition-colors"
              >
                hello@dealix.me
              </a>
              <a
                href="https://wa.me/966500000000"
                className="block text-xs text-muted-foreground hover:text-foreground transition-colors"
                rel="noopener noreferrer"
                target="_blank"
              >
                {isAr ? "واتساب (على الموعد فقط)" : "WhatsApp (by appointment only)"}
              </a>
            </div>
          </div>

          {/* Nav columns */}
          <div className="lg:col-span-4 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {NAV_COLUMNS.map((col) => (
              <div key={col.titleEn} className={isAr ? "text-right" : "text-left"}>
                <p className="text-xs font-semibold uppercase tracking-wide text-foreground mb-3">
                  {isAr ? col.titleAr : col.titleEn}
                </p>
                <ul className="space-y-2">
                  {col.links.map((link) => (
                    <li key={link.href + (isAr ? link.ar : link.en)}>
                      <Link
                        href={`${base}${link.href}`}
                        className="text-xs text-muted-foreground hover:text-foreground transition-colors leading-relaxed"
                      >
                        {isAr ? link.ar : link.en}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* ── Trust signals bar ── */}
        <div className="border-t border-border/40 pt-6 pb-4">
          <div className="flex flex-wrap gap-2 justify-center">
            {TRUST_SIGNALS.map((sig) => (
              <span
                key={sig.en}
                className="rounded-full border border-emerald-500/30 bg-emerald-50/50 dark:bg-emerald-950/20 text-emerald-700 dark:text-emerald-300 px-3 py-1 text-xs font-medium"
              >
                {isAr ? sig.ar : sig.en}
              </span>
            ))}
          </div>
        </div>

        {/* ── Bottom bar ── */}
        <div className={`border-t border-border/40 pt-6 flex flex-col sm:flex-row items-start sm:items-center gap-3 sm:gap-0 ${isAr ? "text-right" : "text-left"}`}>
          <div className="flex-1">
            <p className="text-xs text-muted-foreground">
              {isAr
                ? `© ${currentYear} Dealix. جميع الحقوق محفوظة.`
                : `© ${currentYear} Dealix. All rights reserved.`}
            </p>
            <p className="text-xs text-muted-foreground mt-1">
              {isAr
                ? "شركة مسجّلة في المملكة العربية السعودية · خاضعة لأنظمة هيئة الاتصالات والفضاء والتقنية"
                : "Registered in the Kingdom of Saudi Arabia · Subject to CITC regulations"}
            </p>
          </div>
          <div className="flex items-center gap-3 sm:ms-auto">
            <Link href={`${base}/privacy`} className="text-xs text-muted-foreground hover:text-foreground transition-colors">
              {isAr ? "سياسة الخصوصية" : "Privacy Policy"}
            </Link>
            <span className="text-muted-foreground/40">·</span>
            <Link href={`${base}/trust`} className="text-xs text-muted-foreground hover:text-foreground transition-colors">
              {isAr ? "الثقة والامتثال" : "Trust & Compliance"}
            </Link>
            <span className="text-muted-foreground/40">·</span>
            <Link href={`${base}/learn`} className="text-xs text-muted-foreground hover:text-foreground transition-colors">
              {isAr ? "تعلّم" : "Learn"}
            </Link>
          </div>
        </div>

      </div>
    </footer>
  );
}
