"use client";
import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
import { useState } from "react";
import type { ReactNode } from "react";
import { BrandLogo } from "@/components/brand/BrandLogo";
import { LocaleToggle } from "@/components/layout/LocaleToggle";
import { FooterSection } from "@/components/layout/FooterSection";

export function PublicLaunchShell({ children, compactNav = false }: { children: ReactNode; compactNav?: boolean }) {
  const locale = useLocale();
  const t = useTranslations("commercialLaunch");
  const isAr = locale === "ar";
  const base = `/${locale}`;
  const adminKey = typeof window !== "undefined" ? process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY || "" : "";
  const [mobileOpen, setMobileOpen] = useState(false);

  const navLinks = [
    { href: `${base}/solutions`, ar: "الحلول", en: "Solutions", label: "Solutions" },
    { href: `${base}/sectors`, ar: "القطاعات", en: "Sectors", label: "Sectors" },
    { href: `${base}/about`, ar: "كيف يعمل", en: "How it Works", label: "How it Works" },
    { href: `${base}/trust`, ar: "الإثبات", en: "Proof", label: "Proof" },
    { href: `${base}/learn`, ar: "تعلّم", en: "Learn", label: "Learn" },
  ];

  return (
    <div className="dealix-public min-h-screen flex flex-col" dir={isAr ? "rtl" : "ltr"}>
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:z-[100] focus:px-4 focus:py-2 focus:bg-[var(--dealix-navy)] focus:text-white focus:rounded-lg focus:left-4">
        {isAr ? "تخطي إلى المحتوى" : "Skip to content"}
      </a>
      {/* Top company explanation bar — slim premium strip */}
      <div className="bg-[var(--dealix-navy)] text-white text-[11px] sm:text-xs leading-none border-b border-white/10">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 py-2 flex items-center justify-between gap-3">
          <p className="truncate font-medium tracking-wide">
            <span className="font-semibold">Dealix</span>
            <span className="opacity-80 hidden sm:inline"> — {isAr ? "نظام تشغيل أعمال بالذكاء الاصطناعي للشركات في السعودية" : "Saudi-first AI Business Operating System"}</span>
            <span className="opacity-60 hidden lg:inline"> · {isAr ? "من الإشارة إلى التنفيذ والنتيجة الموثقة" : "From signal to governed execution and measurable outcomes"}</span>
          </p>
          <span className="hidden sm:inline-flex items-center gap-1.5 text-[10px] tracking-widest uppercase opacity-60 font-semibold flex-shrink-0">
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" aria-hidden />
            {isAr ? "تشغيل محكوم" : "Governed OS"}
          </span>
        </div>
      </div>
      <header className="border-b border-[var(--dealix-deep-green)]/15 bg-white/95 dark:bg-background/95 sticky top-0 z-30 backdrop-blur-md">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 py-3 flex items-center justify-between gap-4">
          <Link href={base} aria-label="Dealix — Home" className="flex-shrink-0">
            <BrandLogo variant="full" priority className="h-7 sm:h-8" />
          </Link>

          {/* Desktop nav */}
          {!compactNav ? (
            <nav className="hidden lg:flex flex-wrap items-center gap-3 text-sm" aria-label={isAr ? "التنقل الرئيسي" : "Primary navigation"}>
              {navLinks.map((l) => (
                <Link key={l.href} href={l.href} className="text-muted-foreground hover:text-[var(--dealix-deep-green)] transition-colors px-2 py-1.5 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--dealix-gold)]">
                  {isAr ? l.ar : l.en}
                </Link>
              ))}
              <Link href={`${base}/risk-score`} className="text-muted-foreground hover:text-[var(--dealix-deep-green)] transition-colors px-2 py-1.5 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--dealix-gold)]">
                {t("ctaRiskScore")}
              </Link>
              <Link href={`${base}/dealix-diagnostic`} className="bg-[var(--dealix-navy)] text-white px-4 py-2 rounded-full text-sm font-semibold hover:bg-[#000a1e] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--dealix-gold)]">
                {isAr ? "تشخيص مجاني" : "Free Diagnostic"}
              </Link>
              <LocaleToggle />
            </nav>
          ) : (
            <nav className="hidden sm:flex items-center gap-3 text-sm" aria-label="Funnel navigation">
              <Link href={base} className="text-muted-foreground hover:text-[var(--dealix-deep-green)] px-2 py-1.5 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--dealix-gold)]">
                {isAr ? "الرئيسية" : "Home"}
              </Link>
              <Link href={`${base}/solutions`} className="text-muted-foreground hover:text-[var(--dealix-deep-green)] hidden md:inline px-2 py-1.5 rounded-md">{isAr ? "الحلول" : "Solutions"}</Link>
              <Link href={`${base}/proof-pack`} className="text-muted-foreground hover:text-[var(--dealix-deep-green)] hidden md:inline px-2 py-1.5 rounded-md">{isAr ? "Proof Pack" : "Proof Pack"}</Link>
              <LocaleToggle />
            </nav>
          )}

          {/* Mobile controls */}
          <div className="flex items-center gap-2 lg:hidden">
            <LocaleToggle />
            <button
              type="button"
              onClick={() => setMobileOpen(!mobileOpen)}
              aria-expanded={mobileOpen}
              aria-controls="mobile-nav"
              aria-label={mobileOpen ? (isAr ? "إغلاق القائمة" : "Close menu") : isAr ? "فتح القائمة" : "Open menu"}
              className="w-10 h-10 rounded-xl flex items-center justify-center border border-border text-foreground hover:bg-muted transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--dealix-gold)]"
            >
              <span aria-hidden className="text-lg leading-none">{mobileOpen ? "✕" : "☰"}</span>
            </button>
          </div>
        </div>

        {/* Mobile drawer */}
        {mobileOpen && (
          <nav id="mobile-nav" className="lg:hidden border-t border-border bg-white dark:bg-background px-4 py-4 space-y-1" aria-label={isAr ? "قائمة الجوال" : "Mobile navigation"}>
            {(compactNav ? [{ href: base, ar: "الرئيسية", en: "Home" }, { href: `${base}/solutions`, ar: "الحلول", en: "Solutions" }, { href: `${base}/proof-pack`, ar: "Proof Pack", en: "Proof Pack" }] : navLinks).map((l) => (
              <Link
                key={l.href}
                href={l.href}
                onClick={() => setMobileOpen(false)}
                className="block px-3 py-3 rounded-xl text-sm font-medium text-foreground hover:bg-muted transition-colors min-h-[44px] flex items-center focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--dealix-gold)]"
              >
                {isAr ? l.ar : l.en}
              </Link>
            ))}
            {!compactNav && (
              <>
                <Link href={`${base}/risk-score`} onClick={() => setMobileOpen(false)} className="block px-3 py-3 rounded-xl text-sm font-medium text-foreground hover:bg-muted transition-colors min-h-[44px] flex items-center">
                  {t("ctaRiskScore")}
                </Link>
                <Link href={`${base}/dealix-diagnostic`} onClick={() => setMobileOpen(false)} className="block mt-2 px-3 py-3 rounded-xl text-center text-sm font-bold bg-[var(--dealix-navy)] text-white hover:bg-[#000a1e] transition-colors min-h-[44px] flex items-center justify-center">
                  {isAr ? "ابدأ تشخيصك المجاني" : "Start Free Diagnostic"}
                </Link>
              </>
            )}
          </nav>
        )}
      </header>
      <div id="main-content" className="flex-1" tabIndex={-1}>{children}</div>
      <FooterSection />
    </div>
  );
}
