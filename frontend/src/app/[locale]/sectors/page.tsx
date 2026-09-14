import type { Metadata } from "next";
import Link from "next/link";
import { ALL_SECTORS } from "@/content/solutions";

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "القطاعات — Dealix | كل القطاعات، تشغيل محكوم" : "Sectors — Dealix | All Sectors, Governed Execution",
    description: isAr
      ? "20 قطاع — كل قطاع له حلول موثوقة، تشخيص مجاني، وتنفيذ محكوم. اختر قطاعك وابدأ."
      : "20 sectors — each with trusted solutions, free diagnostic, governed execution. Pick yours.",
    alternates: {
      canonical: `https://dealix.me/${locale}/sectors`,
      languages: { ar: "https://dealix.me/ar/sectors", en: "https://dealix.me/en/sectors", "x-default": "https://dealix.me/ar/sectors" },
    },
  };
}

export default async function SectorsPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950" dir={isAr ? "rtl" : "ltr"}>
      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="inline-flex items-center gap-2 bg-cyan-500/10 border border-cyan-500/20 rounded-full px-4 py-1.5 mb-4">
          <span className="w-2 h-2 bg-cyan-500 rounded-full animate-pulse" aria-hidden />
          <span className="text-xs font-bold text-cyan-600 dark:text-cyan-400">{isAr ? "20 قطاع · تشخيص مجاني لكل قطاع" : "20 sectors · Free diagnostic per sector"}</span>
        </div>
        <h1 className="text-4xl font-bold tracking-tight mb-3">{isAr ? "القطاعات" : "Sectors"}</h1>
        <p className="text-muted-foreground mb-2 max-w-2xl">
          {isAr ? "كل قطاع كقدرة محكومة وموثقة — ليس صفحة SEO رقيقة. اختر قطاعك لترى المشاكل الحقيقية والفرص وما يمكن لـ Dealix تنفيذه فعلاً." : "Each sector as a governed, evidence-backed capability — not a thin SEO page. Pick your sector to see real problems, opportunities, and what Dealix can actually deliver."}
        </p>
        <p className="text-xs text-muted-foreground mb-8 max-w-2xl">
          {isAr ? "50 عائلة تشخيصية D0-D5 · خلايا اقتصادية · أذرع · قنوات · SaaS · تشغيل محكوم بالموارد" : "50 diagnostic families D0-D5 · economic cells · arms · channels · SaaS · resource-governed execution"}
        </p>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {ALL_SECTORS.map((s) => (
            <Link
              key={s.id}
              href={`/${locale}/solutions/${s.id}`}
              className="group rounded-2xl border border-border bg-card p-6 hover:border-cyan-500/30 hover:shadow-lg hover:shadow-cyan-500/5 transition-all"
            >
              <div className="text-3xl mb-3" aria-hidden>{s.icon}</div>
              <h3 className="font-bold group-hover:text-cyan-600 dark:group-hover:text-cyan-400 transition-colors">{isAr ? s.nameAr : s.nameEn}</h3>
              <p className="text-sm text-muted-foreground mt-1 line-clamp-2">{isAr ? s.problemsAr.slice(0, 2).join(" · ") : s.problemsEn.slice(0, 2).join(" · ")}</p>
              <p className="text-xs text-cyan-600 dark:text-cyan-400 mt-3 font-medium">
                {isAr ? `${s.servicesAr.length} خدمات` : `${s.servicesEn.length} services`} · {isAr ? "تشخيص مجاني" : "Free diagnostic"} →
              </p>
            </Link>
          ))}
        </div>
        <div className="mt-12 rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-6 text-center">
          <p className="font-semibold">{isAr ? "لم تجد قطاعك؟" : "Don't see your sector?"}</p>
          <p className="text-sm text-muted-foreground mt-1">{isAr ? "Dealix يعمل مع كل القطاعات — ابدأ بالتشخيص المجاني وسنخصص الحل." : "Dealix works across all sectors — start with the free diagnostic and we'll tailor the solution."}</p>
          <Link href={`/${locale}/dealix-diagnostic`} className="inline-flex mt-4 px-6 py-2.5 rounded-full bg-[#0C2742] text-white text-sm font-semibold hover:bg-[#06111f] transition-colors">
            {isAr ? "ابدأ التشخيص المجاني" : "Start Free Diagnostic"}
          </Link>
        </div>
      </div>
    </div>
  );
}
