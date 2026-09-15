export const metadata = {
  title: "Enterprise Readiness — Dealix",
  description:
    "Governance, human approval, evidence boundaries, and buyer-inspectable Dealix operating artifacts.",
};

const PILLARS = [
  {
    title: "Evidence before claims",
    body: "Security, compliance, delivery, and commercial claims must map to current evidence for the exact scope being discussed.",
    link: "/trust-center",
  },
  {
    title: "AI governance",
    body: "Dealix separates model output from authority and keeps material actions behind explicit policy and approval gates.",
    link: "/safety",
  },
  {
    title: "Human approval",
    body: "Customer-facing sends, public publishing, payments, contracts, and production mutations are authority-bound actions.",
    link: "/safety",
  },
  {
    title: "Data boundaries",
    body: "Data handling is scoped to the agreed workflow and evidence requirements. Public pages do not claim blanket certification or compliance status.",
    link: "/safety",
  },
  {
    title: "Delivery proof",
    body: "Delivery is measured against explicit acceptance criteria, evidence, and customer-validated outcomes rather than marketing promises.",
    link: "/cases",
  },
  {
    title: "Buyer diligence",
    body: "Procurement and security teams can review the relevant Dealix policies and artifacts before a customer-specific engagement is agreed.",
    link: "/book",
  },
];

export default function EnterpriseReadinessPage() {
  return (
    <main className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-semibold tracking-tight">Enterprise Readiness</h1>
      <p className="mt-3 max-w-3xl text-neutral-600">
        Dealix uses evidence-governed execution: claims are scoped, material actions are approval-bound,
        and commercial terms are defined for the customer after discovery rather than published as fixed authority.
      </p>

      <section className="mt-10 grid gap-5 md:grid-cols-2">
        {PILLARS.map((pillar) => (
          <article key={pillar.title} className="rounded-2xl border border-neutral-200 p-6">
            <h2 className="text-lg font-semibold">{pillar.title}</h2>
            <p className="mt-2 text-sm text-neutral-700">{pillar.body}</p>
            <a href={pillar.link} className="mt-3 inline-block text-sm font-medium text-blue-700 hover:underline">
              View →
            </a>
          </article>
        ))}
      </section>

      <section className="mt-12 rounded-2xl bg-neutral-900 p-8 text-neutral-50">
        <h2 className="text-xl font-semibold">Start with a free execution diagnostic</h2>
        <p className="mt-2 max-w-2xl text-sm text-neutral-300">
          We first establish the workflow, evidence gaps, baseline, decision owner, and proof criteria.
          Any implementation scope, timeline, and price is customer-specific after qualified discovery.
        </p>
        <a
          href="/book"
          className="mt-4 inline-block rounded-full bg-white px-5 py-2 text-sm font-medium text-neutral-900"
        >
          Start the free diagnostic
        </a>
      </section>
    </main>
  );
}
