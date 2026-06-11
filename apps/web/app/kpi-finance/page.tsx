import { KPI_METRICS } from "@/lib/company-os/company-os";

export const metadata = {
  title: "KPI & Finance Control — Dealix",
  description: "Daily/weekly/monthly control of cash, retainers, conversion, delivery load, and expansion.",
};

function statusClasses(s: "on_track" | "watch" | "off_track") {
  if (s === "on_track") return "bg-emerald-500/10 text-emerald-200 border-emerald-400/30";
  if (s === "watch") return "bg-amber-500/10 text-amber-200 border-amber-400/30";
  return "bg-rose-500/10 text-rose-200 border-rose-400/30";
}

export default function KpiFinancePage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <header className="mb-10">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">KPI & Finance Control</p>
          <h1 className="mt-3 text-4xl font-semibold leading-tight">
            المؤشرات والتمويل — لا تترك القرار للحدس
          </h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            كل مؤشر له هدف، مالك، إيقاع، ومصدر بيانات. هذا الداشبورد يعطيك صورة فورية: وين أنت من
            الهدف، وشنو المالك اللي لازم يتحرك، ومتى آخر مرة تم تحديث الرقم.
          </p>
        </header>

        <section className="grid gap-4 md:grid-cols-2">
          {KPI_METRICS.map((k) => {
            const pct =
              k.target === 0
                ? 0
                : Math.max(0, Math.min(100, Math.round((k.current / Math.max(1, k.target)) * 100)));
            return (
              <article key={k.id} className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <div className="flex items-center justify-between">
                  <p className="text-xs uppercase tracking-widest text-white/50">{k.cadence}</p>
                  <span className={`rounded-full border px-2 py-1 text-[10px] ${statusClasses(k.status)}`}>
                    {k.status.replace("_", " ")}
                  </span>
                </div>
                <h2 className="mt-2 text-lg font-semibold">{k.label}</h2>
                <p className="text-xs text-white/60">{k.labelAr}</p>
                <div className="mt-4 flex items-baseline gap-2">
                  <span className="text-3xl font-semibold text-amber-200">
                    {k.current.toLocaleString()}
                  </span>
                  <span className="text-sm text-white/60">/ {k.target.toLocaleString()} {k.unit}</span>
                </div>
                <div className="mt-3 h-2 w-full rounded-full bg-white/10">
                  <div
                    className="h-2 rounded-full bg-amber-300/80"
                    style={{ width: `${pct}%` }}
                  />
                </div>
                <div className="mt-3 flex items-center justify-between text-xs text-white/60">
                  <span>Owner: {k.owner}</span>
                  <span>Source: {k.source}</span>
                </div>
              </article>
            );
          })}
        </section>

        <section className="mt-10 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6">
          <h2 className="text-lg font-semibold text-amber-200">قواعد التحكم</h2>
          <ul className="mt-3 space-y-2 text-sm text-white/80">
            <li>• إذا المؤشر <span className="text-rose-300">off_track</span>، يفتح incident صغير: ما المشكلة، مين المالك، متى الإصلاح.</li>
            <li>• لا توسعة بدون proof report مقبول من العميل.</li>
            <li>• كل رقم يجي من سكربت أو JSON موقّع، لا من الذاكرة.</li>
            <li>• الهدف الشهري للـ MRR يحدّث مع Founder Operating System كل شهر.</li>
          </ul>
        </section>
      </div>
    </main>
  );
}
