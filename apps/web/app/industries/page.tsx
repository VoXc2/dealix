import Link from "next/link";
import { INDUSTRY_PLAYS } from "@/lib/industries/industry-pages";

export const metadata = {
  title: "Industries — Dealix",
  description: "Industry-specific plays: pain, leakage, recommended offer, and first 7-day workflow review.",
};

export default function IndustriesPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Industries</p>
          <h1 className="mt-3 text-4xl font-semibold">سبع صناعات، سبع plays مختلفة</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            كل صناعة عندها ضعف مرئي مختلف، والعرض المناسب مختلف. هنا تشوف play كامل لكل وحدة.
          </p>
        </header>

        <section className="mt-10 grid gap-4 md:grid-cols-2">
          {INDUSTRY_PLAYS.map((p) => (
            <Link
              key={p.id}
              href={`/industries/${p.id}`}
              className="rounded-2xl border border-white/10 bg-white/5 p-6 transition hover:border-amber-300/40"
            >
              <h2 className="text-lg font-semibold">{p.industry}</h2>
              <p className="text-xs text-white/60">{p.industryAr}</p>
              <p className="mt-3 text-sm text-white/80">{p.painEn}</p>
              <p className="mt-1 text-xs text-white/60">{p.painAr}</p>
              <p className="mt-3 text-xs text-amber-200">Best offer: {p.recommendedOffer}</p>
            </Link>
          ))}
        </section>
      </div>
    </main>
  );
}
