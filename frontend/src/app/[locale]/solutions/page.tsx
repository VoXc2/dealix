import type { Metadata } from "next";
import Link from "next/link";
import { getTranslations } from "next-intl/server";
import { ALL_SECTORS } from "@/content/solutions";

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "الحلول حسب القطاع — Dealix" : "Solutions by Sector — Dealix",
    description: isAr ? "اختر قطاعك وشاهد الخدمات المتاحة بتشغيل محكوم وموثق" : "Choose your sector and see available services with governed, evidence-backed execution",
    alternates: {
      canonical: `https://dealix.me/${locale}/solutions`,
      languages: { ar: "https://dealix.me/ar/solutions", en: "https://dealix.me/en/solutions", "x-default": "https://dealix.me/ar/solutions" },
    },
  };
}

export default async function SolutionsPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return (
    <div className="min-h-screen bg-navy-900 text-white" dir={isAr ? "rtl" : "ltr"}>
      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="inline-flex items-center gap-2 bg-gold-500/10 border border-gold-500/20 rounded-full px-4 py-1.5 mb-4">
          <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></span>
          <span className="text-xs font-bold text-gold-400">{isAr ? "المنتج الرئيسي: Dealix AI Business OS — منفتح على كلشي" : "Main Product: Dealix AI Business OS — Open to Everything"}</span>
        </div>
        <h1 className="text-4xl font-bold mb-3">{isAr ? "حلول لكل القطاعات" : "Solutions for Every Sector"}</h1>
        <p className="text-white/60 mb-2 max-w-2xl">
          {isAr ? "٢٠ قطاع — كل قطاع كقدرة مؤقتة محكومة وموثقة. اختر قطاعك وشاهد ماذا يقدم Dealix تقنياً." : "20 sectors — each as a temporary capability, governed & evidence-backed. Pick your sector to see what Dealix serves technically."}
        </p>
        <p className="text-xs text-white/40 mb-8 max-w-2xl">
          {isAr ? "القدرات: 50 عائلة تشخيصية (D0-D5) • خلايا اقتصادية • أذرع • قنوات • SaaS • تشغيل محكوم بالموارد — يخدم كل القطاعات والحكومة" : "Capabilities: 50 diagnostic families (D0-D5) • economic cells • arms • channels • SaaS • resource-governed — serves all sectors & government"}
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
