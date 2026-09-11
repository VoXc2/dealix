import type { Metadata } from "next";
import Link from "next/link";

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "تأهيل SaaS — Dealix" : "SaaS Onboarding — Dealix",
    description: isAr ? "اختر قطاعك، أكمل تشخيص D1، واحصل على مساحة عمل معزولة" : "Choose sector, complete D1 diagnostic, get isolated workspace",
  };
}

export default async function OnboardingPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const sectors = [
    { id: "technology_saas_si", ar: "التقنية", en: "Technology" },
    { id: "government_b2g", ar: "حكومي", en: "Government" },
    { id: "finance_fintech_insurance", ar: "مالية", en: "Finance" },
    { id: "healthcare", ar: "صحة", en: "Healthcare" },
    { id: "construction_epc", ar: "إنشاءات", en: "Construction" },
  ];
  return (
    <div className="min-h-screen bg-navy-900 text-white" dir={isAr ? "rtl" : "ltr"}>
      <div className="max-w-4xl mx-auto px-6 py-12">
        <h1 className="text-4xl font-bold">{isAr ? "تأهيل SaaS" : "SaaS Onboarding"}</h1>
        <p className="text-white/60 mt-3">{isAr ? "اختر قطاعك → تشخيص D1 → مساحة عمل معزولة → فوترة" : "Choose sector → D1 diagnostic → isolated workspace → billing"}</p>
        <div className="grid gap-4 md:grid-cols-3 mt-8">
          {sectors.map((s) => (
            <Link key={s.id} href={`/${locale}/dealix-diagnostic?sector=${s.id}`} className="rounded-xl border border-white/10 bg-white/5 p-5 hover:bg-white/10">
              <div className="font-bold">{isAr ? s.ar : s.en}</div>
              <div className="text-xs text-white/40 mt-1">{s.id}</div>
              <div className="text-sm text-gold-400 mt-3">{isAr ? "ابدأ" : "Start"} →</div>
            </Link>
          ))}
        </div>
        <div className="mt-8 rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-5">
          <h3 className="font-bold text-emerald-400">{isAr ? "6 مراحل" : "6 Stages"}</h3>
          <p className="text-sm text-white/70 mt-2">ACCOUNT_CREATED → SECTOR_SELECTED → DIAGNOSTIC_COMPLETED → WORKSPACE_READY → FIRST_PROOF → BILLING_ACTIVE</p>
          <p className="text-xs text-white/40 mt-2">{isAr ? "عزل بيانات بمفتاح hash، استحقاقات per tier، موافقة" : "Data isolation via hash, entitlements per tier, consent"}</p>
        </div>
      </div>
    </div>
  );
}
