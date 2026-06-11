export const metadata = {
  title: "Enterprise Readiness — Dealix",
  description: "Security, data boundaries, AI governance, human review, SLA — for enterprise buyers.",
};

const DOCS = [
  { title: "Security Questionnaire", href: "business/enterprise/SECURITY_QUESTIONNAIRE_TEMPLATE.md" },
  { title: "Data Boundary Statement", href: "business/enterprise/DATA_BOUNDARY_STATEMENT.md" },
  { title: "AI Governance Statement", href: "business/enterprise/AI_GOVERNANCE_STATEMENT.md" },
  { title: "Human Review Statement", href: "business/enterprise/HUMAN_REVIEW_STATEMENT.md" },
  { title: "Service Level Boundaries", href: "business/enterprise/SERVICE_LEVEL_BOUNDARIES.md" },
  { title: "Implementation Assurance Plan", href: "business/enterprise/IMPLEMENTATION_ASSURANCE_PLAN.md" },
  { title: "Enterprise Buyer FAQ (AR)", href: "business/enterprise/ENTERPRISE_BUYER_FAQ_AR.md" },
  { title: "Enterprise Buyer FAQ (EN)", href: "business/enterprise/ENTERPRISE_BUYER_FAQ_EN.md" },
];

export default function EnterpriseReadinessPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-5xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Enterprise Readiness</p>
          <h1 className="mt-3 text-4xl font-semibold">جاهزية المؤسسة — للمستثمرين والشركاء</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            ثمان وثائق تغطي الأمان، البيانات، الحوكمة، المراجعة البشرية، SLA، والتطبيق.
          </p>
        </header>

        <section className="mt-10 grid gap-3 md:grid-cols-2">
          {DOCS.map((d) => (
            <a
              key={d.href}
              href={`https://github.com/VoXc2/dealix/blob/main/${d.href}`}
              target="_blank"
              rel="noreferrer"
              className="rounded-2xl border border-white/10 bg-white/5 p-4 transition hover:border-amber-300/40"
            >
              <p className="text-sm font-medium">{d.title}</p>
              <p className="mt-1 text-[10px] text-white/40">{d.href}</p>
            </a>
          ))}
        </section>
      </div>
    </main>
  );
}
