"use client";
import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
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
  return (
    <div className="dealix-public min-h-screen flex flex-col" dir={isAr ? "rtl" : "ltr"}>
      <header className="border-b border-[var(--dealix-deep-green)]/15 bg-white/90 dark:bg-background/95 sticky top-0 z-20 backdrop-blur-sm">
        <div className="mx-auto max-w-6xl px-6 py-3 flex items-center justify-between gap-4">
          <Link href={base}><BrandLogo variant="full" priority className="h-8" /></Link>
          {!compactNav ? (
            <nav className="flex flex-wrap items-center gap-3 text-sm">
              <Link href={`${base}/services`} className="text-muted-foreground hover:text-[var(--dealix-deep-green)]">{isAr ? "الخدمات" : "Services"}</Link>
              <Link href={`${base}/pricing`} className="text-muted-foreground hover:text-[var(--dealix-deep-green)]">{isAr ? "التسعير" : "Pricing"}</Link>
              <Link href={`${base}/learn`} className="text-muted-foreground hover:text-[var(--dealix-deep-green)]">{t("navLearn")}</Link>
              <Link href={`${base}/about`} className="text-muted-foreground hover:text-[var(--dealix-deep-green)]">{isAr ? "عن Dealix" : "About"}</Link>
              <Link href={`${base}/trust`} className="text-muted-foreground hover:text-[var(--dealix-deep-green)]">{isAr ? "الثقة" : "Trust"}</Link>
              <Link href={`${base}/risk-score`} className="text-muted-foreground hover:text-[var(--dealix-deep-green)]">{t("ctaRiskScore")}</Link>
              <Link href={`${base}/login`} className="font-medium text-[var(--dealix-deep-green)]">{t("navLogin")}</Link>
              {adminKey ? <Link href={`${base}/ops/founder`} className="text-[var(--dealix-gold)]">{isAr ? "تشغيل المؤسس" : "Founder ops"}</Link> : null}
              <LocaleToggle />
            </nav>
          ) : (
            <div className="flex gap-3"><Link href={base}>{isAr ? "الرئيسية" : "Home"}</Link><LocaleToggle /></div>
          )}
        </div>
      </header>
      <div className="flex-1">{children}</div>
      <FooterSection />
    </div>
  );
}
