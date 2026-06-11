export const metadata = {
  title: "Partner Room — Dealix",
  description: "Partner program: who we work with, what they get, and how to apply.",
};

const PARTNER_TYPES = [
  {
    id: "agency",
    name: "Agency Partner",
    nameAr: "شريك وكالات",
    description: "Marketing, PR, or creative agencies that serve Saudi SMEs and want a delivery OS for their clients.",
    benefits: ["White-labeled delivery layer", "Co-branded case studies", "Joint proposals"],
  },
  {
    id: "consulting",
    name: "Consulting Partner",
    nameAr: "شريك استشاري",
    description: "Strategy, ops, or finance consultants who need an execution layer after the diagnosis.",
    benefits: ["Referral fee", "Co-implementation", "Quarterly reviews"],
  },
  {
    id: "tech",
    name: "Technology Partner",
    nameAr: "شريك تقني",
    description: "CRMs, data platforms, or automation vendors that complement our stack.",
    benefits: ["API integration", "Joint GTM", "Co-sell motion"],
  },
  {
    id: "training",
    name: "Training Partner",
    nameAr: "شريك تدريب",
    description: "Bootcamps, training houses, and content creators who need a delivery OS for their cohorts.",
    benefits: ["Cohort delivery layer", "Joint curriculum", "Revenue share"],
  },
];

export default function PartnerRoomPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Partner Room</p>
          <h1 className="mt-3 text-4xl font-semibold">شراكات تخدم كل طرف</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            ما عندنا باب مفتوح للجميع. الشراكة معنا واضحة، الشروط واضحة، وقواعد الحوكمة واضحة.
          </p>
        </header>

        <section className="mt-10 grid gap-3 md:grid-cols-2">
          {PARTNER_TYPES.map((p) => (
            <article key={p.id} className="rounded-2xl border border-white/10 bg-white/5 p-5">
              <h2 className="text-lg font-semibold">{p.name}</h2>
              <p className="text-xs text-white/60">{p.nameAr}</p>
              <p className="mt-2 text-sm text-white/80">{p.description}</p>
              <ul className="mt-3 list-disc list-inside text-xs text-white/60">
                {p.benefits.map((b) => (
                  <li key={b}>{b}</li>
                ))}
              </ul>
            </article>
          ))}
        </section>
      </div>
    </main>
  );
}
