import type { Metadata } from "next";
import Link from "next/link";
import { getTranslations } from "next-intl/server";
import { ALL_SECTORS } from "@/content/solutions";

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "الحلول حسب القطاع — Dealix" : "Solutions by Sector — Dealix",
    description: isAr ? "اختر قطاعك وشاهد الخدمات المتاحة يديرها 5 وكلاء متخصصين" : "Choose your sector and see available services managed by 5 specialist agents",
    alternates: { canonical: `https://dealix.me/${locale}/solutions` },
  };
}

export default async function SolutionsPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return (
    <div className="min-h-screen bg-navy-900 text-white" dir={isAr ? "rtl" : "ltr"}>
      <div className="max-w-6xl mx-auto px-6 py-12">
        <h1 className="text-4xl font-bold mb-3">{isAr ? "حلول لكل القطاعات" : "Solutions for Every Sector"}</h1>
        <p className="text-white/60 mb-8 max-w-2xl">
          {isAr ? "٢٠ قطاع — كل قطاع له شركة افتراضية مؤتمتة بالكامل يديرها 5 وكلاء: pm, sales, delivery, engineer, content. اختر قطاعك وشاهد الخدمات." : "20 sectors — each as a fully automated virtual company managed by 5 agents: pm, sales, delivery, engineer, content. Pick your sector."}
        </p>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {ALL_SECTORS.map((s) => (
            <Link key={s.id} href={`/${locale}/solutions/${s.id}`} className="rounded-2xl border border-white/10 bg-white/5 p-6 hover:bg-white/10 transition backdrop-blur">
              <div className="text-3xl mb-3">{s.icon}</div>
              <h3 className="font-bold">{isAr ? s.nameAr : s.nameEn}</h3>
              <p className="text-sm text-white/50 mt-1">{isAr ? s.problemsAr.slice(0,2).join(" • ") : s.problemsEn.slice(0,2).join(" • ")}</p>
              <p className="text-xs text-gold-400 mt-3">{isAr ? s.servicesAr.length : s.servicesEn.length} {isAr ? "خدمات" : "services"} • {isAr ? "يديرها الاجينتس" : "managed by agents"}</p>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
