import { INDUSTRY_PLAYS } from "@/lib/industries/industry-pages";
import Link from "next/link";

interface Props {
  params: { id: string };
}

export function generateStaticParams() {
  return INDUSTRY_PLAYS.map((p) => ({ id: p.id }));
}

export function generateMetadata({ params }: Props) {
  const p = INDUSTRY_PLAYS.find((x) => x.id === params.id);
  return {
    title: p ? `${p.industry} — Dealix` : "Industry — Dealix",
    description: p ? p.painEn : "",
  };
}

export default function IndustryDetailPage({ params }: Props) {
  const p = INDUSTRY_PLAYS.find((x) => x.id === params.id);
  if (!p) {
    return <main className="p-10 text-white">Industry not found.</main>;
  }
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-4xl px-6 py-16">
        <Link href="/industries" className="text-xs text-amber-300/80">← All industries</Link>
        <header className="mt-4">
          <h1 className="text-4xl font-semibold">{p.industry}</h1>
          <p className="mt-1 text-white/60">{p.industryAr}</p>
        </header>

        <section className="mt-10 grid gap-6 md:grid-cols-2">
          <article className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <p className="text-xs uppercase tracking-widest text-rose-200">Pain</p>
            <p className="mt-2 text-sm">{p.painEn}</p>
            <p className="mt-1 text-xs text-white/60">{p.painAr}</p>
          </article>
          <article className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <p className="text-xs uppercase tracking-widest text-amber-200">Visible leakage</p>
            <p className="mt-2 text-sm">{p.visibleLeakageEn}</p>
            <p className="mt-1 text-xs text-white/60">{p.visibleLeakageAr}</p>
          </article>
        </section>

        <section className="mt-6 rounded-2xl border border-white/10 bg-white/5 p-6">
          <p className="text-xs uppercase tracking-widest text-emerald-200">Recommended offer</p>
          <p className="mt-2 text-2xl font-semibold text-amber-200">{p.recommendedOffer}</p>
          <p className="mt-3 text-sm text-white/80"><strong>First 7 days:</strong> {p.first7DayEn}</p>
          <p className="mt-1 text-xs text-white/60">{p.first7DayAr}</p>
        </section>

        <section className="mt-6 grid gap-6 md:grid-cols-2">
          <article className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <p className="text-xs uppercase tracking-widest text-white/50">Proof plan</p>
            <p className="mt-2 text-sm">{p.proofPlan}</p>
          </article>
          <article className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <p className="text-xs uppercase tracking-widest text-white/50">Governance</p>
            <p className="mt-2 text-sm">{p.governanceNote}</p>
          </article>
        </section>

        <section className="mt-8 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6 text-center">
          <p className="text-sm text-white/80">{p.ctaCopy}</p>
          <Link
            href="/book"
            className="mt-3 inline-block rounded-lg border border-amber-300/30 bg-amber-300/10 px-6 py-2 text-sm text-amber-200 hover:border-amber-300/60"
          >
            Book a Workflow Review
          </Link>
        </section>
      </div>
    </main>
  );
}
