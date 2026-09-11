import type { Metadata } from "next";
import Link from "next/link";
import { ALL_SECTORS } from "@/content/solutions";

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "السيطرة على السوق — Dealix" : "Market Control — Dealix",
    description: isAr ? "20 قطاع × 44 ذراع × SaaS — سيطرة شاملة" : "20 sectors × 44 arms × SaaS — comprehensive control",
  };
}

export default async function MarketControlPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return (
    <div className="min-h-screen bg-navy-900 text-white" dir={isAr ? "rtl" : "ltr"}>
      <div className="max-w-6xl mx-auto px-6 py-12">
        <h1 className="text-4xl font-bold">{isAr ? "السيطرة على السوق" : "Market Control"}</h1>
        <p className="text-white/60 mt-3">{isAr ? "20 قطاع × 44 ذراع × 12 قناة × SaaS 20 مستأجر × 500 خلية × DeepWIP 3" : "20 sectors × 44 arms × 12 channels × SaaS 20 tenants × 500 cells × DeepWIP 3"}</p>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mt-8">
          {ALL_SECTORS.map((s) => (
            <Link key={s.id} href={`/${locale}/solutions/${s.id}`} className="rounded-xl border border-white/10 bg-white/5 p-4 hover:bg-white/10">
              <div className="text-2xl">{s.icon}</div>
              <div className="font-bold mt-2 text-sm">{isAr ? s.nameAr : s.nameEn}</div>
              <div className="text-xs text-white/40 mt-1">3 {isAr ? "خدمات" : "services"} • {isAr ? "مؤتمت" : "automated"}</div>
            </Link>
          ))}
        </div>
        <div className="mt-6 flex gap-3">
          <Link href={`/${locale}/onboarding`} className="inline-block bg-emerald-500 text-white px-6 py-3 rounded-xl font-bold hover:bg-emerald-400">
            {isAr ? "ابدأ التأهيل" : "Start Onboarding"}
          </Link>
          <Link href={`/${locale}/solutions`} className="inline-block border border-white/20 text-white px-6 py-3 rounded-xl font-bold hover:bg-white/10">
            {isAr ? "استكشف الحلول" : "Explore Solutions"}
          </Link>
        </div>
        <div className="mt-10 rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-6">
          <h3 className="font-bold text-emerald-400">{isAr ? "كل الأذرع مفعلة" : "All Arms Activated"}</h3>
          <p className="text-sm text-white/70 mt-2">44 arms (42 ACTIVE) — pm 20, engineer 9, content 7, sales 5, delivery 3 — Large Capability Surface بدون 44 مشروع</p>
          <p className="text-xs text-white/40 mt-2">DeepWIP≤3 • 500 cells • 13 agents (5 core + 8 extended) • SaaS 20 tenants • 12 channels</p>
        </div>
      </div>
    </div>
  );
}
