import { PREMIUM_OFFERS } from "@/lib/sales-machine/ultimate-sales-os";

export const metadata = {
  title: "Offers — Dealix",
  description: "Seven offers, from a free 20-min diagnostic to custom enterprise systems.",
};

export default function OffersPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Offer Ladder</p>
          <h1 className="mt-3 text-4xl font-semibold">سبع عروض، مسار واحد</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            كل عميل يدخل من التشخيص المجاني، ونقرر مع بعض أي عرض يناسبه. لا فخ تسعير، لا عقود
            طويلة قبل إثبات القيمة.
          </p>
        </header>

        <section className="mt-10 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {PREMIUM_OFFERS.map((o) => (
            <article key={o.id} className="flex flex-col rounded-2xl border border-white/10 bg-white/5 p-6">
              <p className="text-xs uppercase tracking-widest text-amber-300/80">{o.id}</p>
              <h2 className="mt-2 text-xl font-semibold">{o.name}</h2>
              <p className="text-xs text-white/60">{o.nameAr}</p>
              <div className="mt-4 flex items-baseline gap-2">
                <span className="text-2xl font-semibold text-amber-200">{o.setup}</span>
                <span className="text-xs text-white/60">setup</span>
              </div>
              <div className="mt-1 flex items-baseline gap-2">
                <span className="text-sm text-white/80">{o.monthly}</span>
                <span className="text-xs text-white/60">monthly</span>
              </div>
              <p className="mt-4 text-sm text-white/80">{o.positioning}</p>
              <p className="text-xs text-white/60">{o.positioningAr}</p>
              <ul className="mt-4 flex flex-wrap gap-2 text-[10px] text-white/60">
                {o.bestFor.map((b) => (
                  <li key={b} className="rounded-full border border-white/10 px-2 py-1">
                    {b}
                  </li>
                ))}
              </ul>
            </article>
          ))}
        </section>
      </div>
    </main>
  );
}
