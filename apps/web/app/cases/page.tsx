import { SECTOR_DIAGNOSTIC_CATALOG } from "@/lib/sales-machine/sector-diagnostic-catalog";

export const metadata = {
  title: "Sector Diagnostics — Dealix",
  description: "Evidence-bound diagnostic plays across 20 sectors, from economic problem to governed execution.",
};

export default function CasesPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white" dir="rtl">
      <div className="mx-auto max-w-7xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Sector Diagnostics</p>
          <h1 className="mt-3 text-4xl font-semibold">تشخيص تشغيلي لكل قطاع</h1>
          <p className="mt-3 max-w-3xl text-sm leading-7 text-white/70">
            خريطة Dealix التجارية لـ20 قطاعًا: نبدأ بإشارة ومشكلة اقتصادية قابلة للتحقق،
            ثم نحدد العملية والمشتري وKPI والعرض المناسب. هذه ليست case studies أو وعود نتائج.
          </p>
        </header>

        <section className="mt-10 grid gap-5 lg:grid-cols-2">
          {SECTOR_DIAGNOSTIC_CATALOG.map((sector) => (
            <article key={sector.id} className="rounded-2xl border border-white/10 bg-white/5 p-6">
              <div className="flex flex-wrap items-baseline justify-between gap-2">
                <h2 className="text-xl font-semibold">{sector.nameAr}</h2>
                <span className="text-xs text-white/50" dir="ltr">{sector.nameEn}</span>
              </div>
              <div className="mt-5 grid gap-4 md:grid-cols-2">
                <div>
                  <p className="text-xs uppercase text-white/50">إشارات التشخيص</p>
                  <ul className="mt-2 space-y-1 text-sm text-white/80">
                    {sector.signals.map((item) => <li key={item}>• {item}</li>)}
                  </ul>
                </div>
                <div>
                  <p className="text-xs uppercase text-white/50">المشكلة الاقتصادية</p>
                  <ul className="mt-2 space-y-1 text-sm text-white/80">
                    {sector.economicProblems.map((item) => <li key={item}>• {item}</li>)}
                  </ul>
                </div>
                <div>
                  <p className="text-xs uppercase text-white/50">مسارات العمل</p>
                  <ul className="mt-2 space-y-1 text-sm text-white/80">
                    {sector.priorityWorkflows.map((item) => <li key={item}>• {item}</li>)}
                  </ul>
                </div>
                <div>
                  <p className="text-xs uppercase text-white/50">كيف تفيد Dealix</p>
                  <ul className="mt-2 space-y-1 text-sm text-amber-100/90">
                    {sector.dealixOffers.map((item) => <li key={item}>• {item}</li>)}
                  </ul>
                </div>
              </div>
              <div className="mt-5 border-t border-white/10 pt-4">
                <p className="text-xs text-white/60">مؤشرات التحقق: {sector.kpis.join(" · ")}</p>
                <p className="mt-2 text-xs text-white/50">المشترون المحتملون: {sector.buyers.join(" · ")}</p>
              </div>
              <p className="mt-4 text-xs text-emerald-200">
                الخطوة التالية: تشخيص تنفيذ مجاني وتحديد baseline قبل أي نطاق أو مدة أو عرض مالي.
              </p>
            </article>
          ))}
        </section>
      </div>
    </main>
  );
}
