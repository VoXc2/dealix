export const metadata = {
  title: "Resources — Dealix",
  description: "Free templates, checklists, and scorecards for Saudi B2B companies.",
};

const RESOURCES = [
  { title: "Workflow Leakage Checklist (AR)", href: "business/lead-magnets/WORKFLOW_LEAKAGE_CHECKLIST_AR.md" },
  { title: "Workflow Leakage Checklist (EN)", href: "business/lead-magnets/WORKFLOW_LEAKAGE_CHECKLIST_EN.md" },
  { title: "Revenue OS Readiness Scorecard (AR)", href: "business/lead-magnets/REVENUE_OS_READINESS_SCORECARD_AR.md" },
  { title: "Revenue OS Readiness Scorecard (EN)", href: "business/lead-magnets/REVENUE_OS_READINESS_SCORECARD_EN.md" },
  { title: "Review OS Audit Template (AR)", href: "business/lead-magnets/REVIEW_OS_AUDIT_TEMPLATE_AR.md" },
  { title: "Review OS Audit Template (EN)", href: "business/lead-magnets/REVIEW_OS_AUDIT_TEMPLATE_EN.md" },
  { title: "Command Center Requirements (AR)", href: "business/lead-magnets/COMMAND_CENTER_REQUIREMENTS_TEMPLATE_AR.md" },
  { title: "Command Center Requirements (EN)", href: "business/lead-magnets/COMMAND_CENTER_REQUIREMENTS_TEMPLATE_EN.md" },
];

export default function ResourcesPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-5xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Resources</p>
          <h1 className="mt-3 text-4xl font-semibold">قوالب مجانية — عربي وإنجليزي</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            ثمان قوالب قابلة للتنزيل. بدون signup، بدون auto-send. استخدمها كما تشاء.
          </p>
        </header>

        <section className="mt-10 grid gap-3 md:grid-cols-2">
          {RESOURCES.map((r) => (
            <a
              key={r.href}
              href={`https://github.com/VoXc2/dealix/blob/main/${r.href}`}
              target="_blank"
              rel="noreferrer"
              className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 p-4 transition hover:border-amber-300/40"
            >
              <p className="text-sm">{r.title}</p>
              <span className="text-xs text-white/40">open →</span>
            </a>
          ))}
        </section>
      </div>
    </main>
  );
}
