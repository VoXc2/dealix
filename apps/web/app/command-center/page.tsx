import { KPI_METRICS } from "@/lib/company-os/company-os";

export const metadata = {
  title: "Command Center — Dealix",
  description: "Founder command center: 5 KPIs, 1 owner per metric, daily standup template.",
};

function statusClasses(s: "on_track" | "watch" | "off_track") {
  if (s === "on_track") return "bg-emerald-500/10 text-emerald-200 border-emerald-400/30";
  if (s === "watch") return "bg-amber-500/10 text-amber-200 border-amber-400/30";
  return "bg-rose-500/10 text-rose-200 border-rose-400/30";
}

export default function CommandCenterPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Command Center</p>
          <h1 className="mt-3 text-4xl font-semibold">غرفة القيادة — صفحة واحدة، خمسة مؤشرات فقط</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            الفكرة بسيطة: ما في داشبورد فيه 30 مؤشر. هنا خمسة مؤشرات، مالك لكل واحد، وstandup يومي
            ومراجعة أسبوعية.
          </p>
        </header>

        <section className="mt-10 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {KPI_METRICS.slice(0, 5).map((k) => (
            <article key={k.id} className="rounded-2xl border border-white/10 bg-white/5 p-5">
              <div className="flex items-center justify-between">
                <p className="text-xs uppercase tracking-widest text-white/50">{k.cadence}</p>
                <span className={`rounded-full border px-2 py-1 text-[10px] ${statusClasses(k.status)}`}>
                  {k.status.replace("_", " ")}
                </span>
              </div>
              <h2 className="mt-2 text-lg font-semibold">{k.label}</h2>
              <p className="text-xs text-white/60">{k.labelAr}</p>
              <div className="mt-3 flex items-baseline gap-2">
                <span className="text-2xl font-semibold text-amber-200">{k.current.toLocaleString()}</span>
                <span className="text-xs text-white/60">/ {k.target.toLocaleString()} {k.unit}</span>
              </div>
              <p className="mt-2 text-xs text-white/60">Owner: {k.owner}</p>
            </article>
          ))}
        </section>

        <section className="mt-10 rounded-2xl border border-white/10 bg-white/5 p-6">
          <h2 className="text-lg font-semibold text-amber-300">Daily standup (5 minutes)</h2>
          <ol className="mt-3 space-y-2 text-sm text-white/80 list-decimal list-inside">
            <li>ما الذي تغيّر أمس في الأرقام الخمسة؟</li>
            <li>أين أكبر bottleneck اليوم؟</li>
            <li>ما الـ single thing اللي لازم يتحرك اليوم؟</li>
          </ol>
        </section>
      </div>
    </main>
  );
}
