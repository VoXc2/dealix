import type { Metadata } from "next";
import Link from "next/link";

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "ديمو شامل — Dealix" : "Comprehensive Demo — Dealix",
    description: isAr ? "ديمو لكل شي: تشخيص، عرض، تسجيل، هرميس يقنع" : "Demo for everything: diagnostic, offer, register, Hermes convinces",
  };
}

export default async function DemoPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return (
    <div className="min-h-screen bg-navy-900 text-white" dir={isAr ? "rtl" : "ltr"}>
      <div className="max-w-5xl mx-auto px-6 py-12">
        <h1 className="text-4xl font-bold">{isAr ? "ديمو شامل — كلشي" : "Comprehensive Demo — Everything"}</h1>
        <p className="text-white/60 mt-3">{isAr ? "على نفس شكل هوبة ديلكس — لوقو، ألوان، أسلوب — ديمو لكل شي مع توضيح شامل، تسجيل حساب وكل حاجة" : "Same shape as Dealix brand — logo, colors, style — demo for everything with comprehensive explanation, account registration and everything"}</p>
        <div className="grid gap-6 md:grid-cols-2 mt-8">
          <div className="rounded-xl border border-white/10 bg-white/5 p-6">
            <h3 className="font-bold text-cyan-400">{isAr ? "التشخيص" : "Diagnostic"}</h3>
            <p className="text-sm text-white/60 mt-2">{isAr ? "50 عائلة (D0-D5)، 20 قطاع، تفاعلي تقني بدون شوائب" : "50 families (D0-D5), 20 sectors, interactive technical without impurities"}</p>
            <Link href={`/${locale}/dealix-diagnostic`} className="inline-block mt-4 bg-cyan-500 text-navy-900 px-4 py-2 rounded-lg font-bold">→</Link>
          </div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-6">
            <h3 className="font-bold text-cyan-400">{isAr ? "الحلول" : "Solutions"}</h3>
            <p className="text-sm text-white/60 mt-2">{isAr ? "20 قطاع، 3 خدمات لكل قطاع، تشغيل محكوم وموثق" : "20 sectors, 3 services per sector, governed & evidence-backed"}</p>
            <Link href={`/${locale}/solutions`} className="inline-block mt-4 bg-cyan-500 text-navy-900 px-4 py-2 rounded-lg font-bold">→</Link>
          </div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-6">
            <h3 className="font-bold text-cyan-400">{isAr ? "التسجيل" : "Register"}</h3>
            <p className="text-sm text-white/60 mt-2">{isAr ? "حساب شامل وكامل — SaaS 6 مراحل، عزل بمفتاح" : "Comprehensive account — SaaS 6 stages, isolation via key"}</p>
            <Link href={`/${locale}/onboarding`} className="inline-block mt-4 bg-cyan-500 text-navy-900 px-4 py-2 rounded-lg font-bold">→</Link>
          </div>
          <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-6">
            <h3 className="font-bold text-emerald-400">{isAr ? "هرميس على الشاشة" : "Hermes on Screen"}</h3>
            <p className="text-sm text-white/60 mt-2">{isAr ? "وكيل ذكي يقنع — يعطي كلشي يحتاجه بأفضل شكل، ذكي جداً" : "Smart agent convinces — gives everything needed in best form, very intelligent"}</p>
            <p className="text-xs text-white/40 mt-2">Governed • Resource-governed • L0-L5 proof</p>
          </div>
        </div>
        <div className="mt-8 rounded-xl border border-cyan-500/20 bg-cyan-500/10 p-6">
          <h3 className="font-bold text-cyan-400">{isAr ? "توضيح شامل" : "Comprehensive Explanation"}</h3>
          <p className="text-sm text-white/70 mt-2">{isAr ? "Dealix AI Business OS — محرك الإيرادات + حوكمة AI + إثبات — منفتح على كل القطاعات والحكومة، 20 شركة قطاعية مؤتمتة، 12 قناة، SaaS 20 مستأجر، أونلاين" : "Dealix AI Business OS — Revenue Engine + AI Governance + Proof — open to all sectors & government, 20 virtual companies, 12 channels, SaaS 20 tenants, online"}</p>
        </div>
      </div>
    </div>
  );
}
