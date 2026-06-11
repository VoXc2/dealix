import { PREMIUM_PILLARS } from "@/lib/sales-machine/ultimate-sales-os";

export const metadata = {
  title: "Brand — Dealix",
  description: "Dealix brand system: positioning, voice, visual, and copy banks.",
};

export default function BrandPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-5xl px-6 py-16">
        <header className="text-center">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Brand System</p>
          <h1 className="mt-3 text-4xl font-semibold leading-tight">
            Dealix — هويتنا واضحة قبل ما نبيع
          </h1>
          <p className="mx-auto mt-3 max-w-2xl text-sm text-white/70">
            ثمانية أعمدة، صوت تنفيذي مباشر، لون Navy + Gold، ولا ادعاءات مبالغ فيها.
          </p>
        </header>

        <section className="mt-12 grid gap-6 md:grid-cols-3">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
            <p className="text-xs uppercase tracking-widest text-white/50">Voice</p>
            <ul className="mt-3 space-y-1 text-sm text-white/80">
              <li>• Executive</li>
              <li>• Direct</li>
              <li>• Saudi-rooted</li>
              <li>• Bilingual AR/EN</li>
              <li>• No hype, no fake ROI</li>
            </ul>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
            <p className="text-xs uppercase tracking-widest text-white/50">Visual</p>
            <ul className="mt-3 space-y-1 text-sm text-white/80">
              <li>• Navy #0E1A33</li>
              <li>• Gold #E2A53A</li>
              <li>• Inter / System Arabic</li>
              <li>• /public/dealix-logo.svg</li>
              <li>• /public/dealix-mark.svg</li>
            </ul>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
            <p className="text-xs uppercase tracking-widest text-white/50">Tagline</p>
            <ul className="mt-3 space-y-1 text-sm text-white/80">
              <li>AR: أنظمة تشغيل ذكية للشركات</li>
              <li>EN: AI Operating Systems for Companies</li>
              <li>Pillars: 8 modules</li>
              <li>Tone: proof-driven</li>
            </ul>
          </div>
        </section>

        <section className="mt-12">
          <h2 className="text-2xl font-semibold text-amber-300">8 Pillars</h2>
          <ul className="mt-4 grid gap-3 md:grid-cols-2">
            {PREMIUM_PILLARS.map((p) => (
              <li key={p.id} className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <p className="font-medium">{p.title} · {p.titleAr}</p>
                <p className="mt-2 text-sm text-white/80">{p.solution}</p>
                <p className="text-xs text-white/60">{p.solutionAr}</p>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </main>
  );
}
