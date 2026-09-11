import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getSector, ALL_SECTORS } from "@/content/solutions";

export function generateStaticParams() {
  return ALL_SECTORS.map((s) => ({ sector: s.id }));
}

export async function generateMetadata({ params }: { params: Promise<{ locale: string; sector: string }> }): Promise<Metadata> {
  const { locale, sector } = await params;
  const s = getSector(sector);
  if (!s) return {};
  const isAr = locale === "ar";
  return {
    title: isAr ? `${s.nameAr} — حلول Dealix` : `${s.nameEn} — Dealix Solutions`,
    description: isAr ? s.problemsAr.join("، ") : s.problemsEn.join(", "),
  };
}

export default async function SectorPage({ params }: { params: Promise<{ locale: string; sector: string }> }) {
  const { locale, sector } = await params;
  const s = getSector(sector);
  if (!s) notFound();
  const isAr = locale === "ar";
  const buyers = isAr ? s.buyersAr : s.buyersEn;
  const problems = isAr ? s.problemsAr : s.problemsEn;
  const services = isAr ? s.servicesAr : s.servicesEn;
  return (
    <div className="min-h-screen bg-navy-900 text-white" dir={isAr ? "rtl" : "ltr"}>
      <div className="max-w-5xl mx-auto px-6 py-12">
        <Link href={`/${locale}/solutions`} className="text-sm text-white/40 hover:text-white">← {isAr ? "كل القطاعات" : "All sectors"}</Link>
        <div className="flex items-center gap-4 mt-6">
          <div className="text-4xl">{s.icon}</div>
          <div>
            <h1 className="text-3xl font-bold">{isAr ? s.nameAr : s.nameEn}</h1>
            <p className="text-white/50 text-sm mt-1">{buyers.join(" • ")}</p>
          </div>
        </div>

        <div className="mt-8 grid gap-6 md:grid-cols-3">
          <div className="rounded-xl border border-white/10 bg-white/5 p-5">
            <h3 className="font-semibold text-gold-400 text-sm mb-2">{isAr ? "المشاكل الرئيسية" : "Top Problems"}</h3>
            <ul className="space-y-1 text-sm text-white/70">
              {problems.map((p) => <li key={p}>• {p}</li>)}
            </ul>
          </div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-5">
            <h3 className="font-semibold text-gold-400 text-sm mb-2">{isAr ? "المشترون" : "Buyers"}</h3>
            <ul className="space-y-1 text-sm text-white/70">
              {buyers.map((b) => <li key={b}>• {b}</li>)}
            </ul>
          </div>
          <div className="rounded-xl border border-white/10 bg-white/5 p-5">
            <h3 className="font-semibold text-gold-400 text-sm mb-2">{isAr ? "قنوات التواصل" : "Channels"}</h3>
            <p className="text-sm text-white/70">{isAr ? "موقع، بريد، واتساب opt-in، دردشة، دعم، شريك، مناقصات" : "Website, email, WhatsApp opt-in, chat, support, partner, procurement"}</p>
            <p className="text-xs text-white/40 mt-2">{isAr ? "كل القنوات مؤتمتة ومحكومة" : "All channels automated & governed"}</p>
          </div>
        </div>

        <h2 className="text-2xl font-bold mt-10 mb-4">{isAr ? "الخدمات المتاحة" : "Available Services"}</h2>
        <p className="text-sm text-white/50 mb-4">{isAr ? "كل خدمة يديرها الاجينتس الخمسة بشكل مؤتمت بالكامل" : "Every service is fully automated by the 5 agents"}</p>
        <div className="grid gap-4 md:grid-cols-3">
          {services.map((svc) => (
            <div key={svc.title} className="rounded-2xl border border-white/10 bg-gradient-to-br from-white/10 to-white/5 p-6 backdrop-blur">
              <h3 className="font-bold">{svc.title}</h3>
              <p className="text-sm text-white/60 mt-1">{svc.desc}</p>
              <p className="text-xs text-gold-400 mt-3">{svc.agents}</p>
              <Link href={`/${locale}/dealix-diagnostic?sector=${s.id}`} className="inline-block mt-4 text-sm bg-gold-500 text-navy-900 px-4 py-2 rounded-lg font-semibold hover:bg-gold-400">
                {isAr ? "ابدأ التشخيص" : "Start Diagnostic"}
              </Link>
            </div>
          ))}
        </div>

        <div className="mt-10 rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-6">
          <h3 className="font-bold text-emerald-400">{isAr ? "كيف يديرها الاجينتس؟" : "How agents manage it"}</h3>
          <ul className="mt-3 space-y-1 text-sm text-white/70">
            <li>• dealix-pm: {isAr ? "تنسيق، أولويات، حوكمة" : "coordination, priorities, governance"}</li>
            <li>• dealix-sales: {isAr ? "علاقات، تأهيل، عروض" : "relationships, qualification, offers"}</li>
            <li>• dealix-delivery: {isAr ? "تنفيذ، إثبات، دعم" : "delivery, proof, support"}</li>
            <li>• dealix-engineer: {isAr ? "إنتاج، أتمتة، تكامل" : "production, automation, integration"}</li>
            <li>• dealix-content: {isAr ? "محتوى، توزيع، ثقة" : "content, distribution, trust"}</li>
          </ul>
          <p className="text-xs text-white/40 mt-3">{isAr ? "كل قطاع = شركة افتراضية مؤتمتة، ليس 20 مشروع منفصل. DeepWIP ≤3 يحافظ على التركيز." : "Each sector = virtual company (temporary capability), not 20 separate projects. DeepWIP ≤3 keeps focus."}</p>
        </div>
      </div>
    </div>
  );
}
