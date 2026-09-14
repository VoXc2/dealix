export const metadata = {
  title: "Brand System — Dealix",
  description:
    "Dealix masterbrand: AI Business Operating System, Signal → Decision → Action → Proof, visual system, proof classes, and brand guardrails.",
};

const proofLevels = [
  ["01", "Internal capability", "What Dealix can demonstrate internally."],
  ["02", "Synthetic / demo", "A bounded simulation or demonstration — never customer proof."],
  ["03", "Runtime / production", "Observed behavior in a running system with production evidence."],
  ["04", "Customer delivery", "A real customer delivery artifact with appropriate evidence."],
  ["05", "Customer outcome", "A verified customer outcome, published only with appropriate permission."],
] as const;

const buyingGroups = [
  ["Founder / GM", "Priority, control, speed and decision clarity"],
  ["Revenue", "Leakage, follow-up, pipeline execution and proof"],
  ["Operations", "Ownership, workflow burden and acceptance criteria"],
  ["Finance / Procurement", "Bounded economics, reversibility and commercial clarity"],
  ["IT / Security", "Integration boundaries, auditability and least privilege"],
  ["Legal / Governance", "Consent, provenance, suppression, approvals and evidence"],
] as const;

export default function BrandPage() {
  return (
    <main className="min-h-screen bg-[#F8FAFC] text-[#0F172A]">
      <section className="relative overflow-hidden border-b border-slate-200 bg-[#0F172A] text-[#F8FAFC]">
        <div className="absolute inset-0 opacity-70" aria-hidden="true">
          <div className="absolute left-1/2 top-[-18rem] h-[34rem] w-[34rem] -translate-x-1/2 rounded-full bg-cyan-400/10 blur-3xl" />
          <div className="absolute right-[-8rem] top-20 h-64 w-64 rounded-full bg-teal-700/20 blur-3xl" />
        </div>

        <div className="relative mx-auto max-w-6xl px-6 py-16 sm:py-20 lg:py-24">
          <div className="flex flex-wrap items-center justify-between gap-6">
            <img
              src="/dealix-logo-white.svg"
              width="400"
              height="96"
              alt="Dealix — AI Business Operating System"
              className="h-auto w-[190px] sm:w-[220px]"
            />
            <span className="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-4 py-2 text-xs font-semibold tracking-[0.18em] text-cyan-200">
              MASTERBRAND V2
            </span>
          </div>

          <div className="mt-16 max-w-4xl">
            <p className="text-sm font-semibold uppercase tracking-[0.22em] text-cyan-300">
              AI Business Operating System
            </p>
            <h1 className="mt-5 text-4xl font-semibold leading-[1.05] tracking-tight sm:text-6xl lg:text-7xl">
              Signals into Action.
              <span className="block text-cyan-300">Execution with Governance.</span>
              <span className="block text-white/90">Measurable Outcomes.</span>
            </h1>
            <p className="mt-7 max-w-2xl text-base leading-7 text-slate-300 sm:text-lg">
              Dealix turns fragmented business signals into governed execution and evidence-backed outcomes.
              The masterbrand is designed to feel calm, exact, premium and operational — not like a generic AI tool.
            </p>
            <div className="mt-8 flex flex-wrap gap-3 text-sm">
              <span className="rounded-full border border-white/10 bg-white/5 px-4 py-2">Revenue + Proof + Command</span>
              <span className="rounded-full border border-white/10 bg-white/5 px-4 py-2">Signal → Decision → Action → Proof</span>
              <span className="rounded-full border border-white/10 bg-white/5 px-4 py-2">Arabic + English</span>
            </div>
          </div>
        </div>
      </section>

      <div className="mx-auto max-w-6xl px-6 py-14 sm:py-20">
        <section>
          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-5">
            {[
              ["Ink Navy", "#0F172A", "Trust / executive depth"],
              ["Deep Teal", "#164E63", "Systems / operating control"],
              ["Signal Cyan", "#22D3EE", "Action / motion / active state"],
              ["Cloud", "#F8FAFC", "Clarity / proof readability"],
              ["Command Cyan", "#06B6D4", "Verified outcome accent only"],
            ].map(([name, hex, meaning]) => (
              <div key={hex} className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
                <div className="h-28" style={{ backgroundColor: hex }} aria-hidden="true" />
                <div className="p-4">
                  <p className="font-semibold">{name}</p>
                  <p className="mt-1 font-mono text-xs text-slate-500">{hex}</p>
                  <p className="mt-2 text-sm leading-5 text-slate-600">{meaning}</p>
                </div>
              </div>
            ))}
          </div>
          <p className="mt-4 text-sm text-slate-500">
            Public Dealix brand uses navy, cyan and neutrals only — no gold. Cyan is the single
            action/proof accent; amber is reserved for semantic status (pending/warning), never branding.
          </p>
        </section>

        <section className="mt-16 grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="rounded-[28px] border border-slate-200 bg-white p-7 shadow-sm sm:p-9">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[#0E7490]">Visual grammar</p>
            <h2 className="mt-3 text-3xl font-semibold tracking-tight">D + Forward Signal</h2>
            <p className="mt-4 max-w-2xl leading-7 text-slate-600">
              The mark combines a geometric D with a forward signal. The open direction represents opportunity becoming outcome;
              negative space represents governance and approval boundaries.
            </p>
            <div className="mt-7 grid gap-4 sm:grid-cols-2">
              <div className="rounded-2xl bg-slate-50 p-5">
                <p className="font-semibold">Use</p>
                <ul className="mt-3 space-y-2 text-sm text-slate-600">
                  <li>Forward vectors and controlled rails</li>
                  <li>Evidence nodes and signal convergence</li>
                  <li>Structured grids and generous whitespace</li>
                  <li>Calm data geometry and proof labels</li>
                </ul>
              </div>
              <div className="rounded-2xl bg-slate-50 p-5">
                <p className="font-semibold">Avoid</p>
                <ul className="mt-3 space-y-2 text-sm text-slate-600">
                  <li>Robot heads, brains and circuit clichés</li>
                  <li>Neon overload and decorative complexity</li>
                  <li>Fake dashboard numbers or customer metrics</li>
                  <li>A separate logo or palette for every product</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="rounded-[28px] bg-[#164E63] p-7 text-white shadow-sm sm:p-9">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-200">Typography</p>
            <div className="mt-6 space-y-7">
              <div>
                <p className="text-sm text-cyan-100/80">Latin</p>
                <p className="mt-1 text-4xl font-semibold tracking-tight">Inter</p>
              </div>
              <div lang="ar" dir="rtl" className="text-right">
                <p className="text-sm text-cyan-100/80">العربية</p>
                <p className="mt-1 text-4xl font-semibold">IBM Plex Sans Arabic</p>
              </div>
              <div>
                <p className="text-sm text-cyan-100/80">Evidence / technical</p>
                <p className="mt-1 font-mono text-xl">IBM Plex Mono</p>
              </div>
            </div>
          </div>
        </section>

        <section className="mt-16">
          <div className="max-w-3xl">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[#0E7490]">Proof system</p>
            <h2 className="mt-3 text-3xl font-semibold tracking-tight">Proof is a product surface, not decoration.</h2>
            <p className="mt-4 leading-7 text-slate-600">
              Every public result should state what class of evidence it is. Activity never becomes outcome by styling it more confidently.
            </p>
          </div>
          <div className="mt-7 grid gap-4 md:grid-cols-5">
            {proofLevels.map(([number, name, explanation]) => (
              <article key={number} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <p className="font-mono text-xs text-cyan-700">{number}</p>
                <h3 className="mt-3 font-semibold">{name}</h3>
                <p className="mt-2 text-sm leading-5 text-slate-600">{explanation}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="mt-16 rounded-[28px] border border-slate-200 bg-[#FAF8F5] p-7 sm:p-9">
          <div className="grid gap-8 lg:grid-cols-[0.85fr_1.15fr]">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[#0E7490]">B2B decision design</p>
              <h2 className="mt-3 text-3xl font-semibold tracking-tight">One masterbrand. Multiple decision lenses.</h2>
              <p className="mt-4 leading-7 text-slate-600">
                A material B2B asset is incomplete if it persuades only one champion. The evidence changes by role; the Dealix identity does not.
              </p>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              {buyingGroups.map(([role, concern]) => (
                <div key={role} className="rounded-2xl border border-[#E8DFD2] bg-white/80 p-4">
                  <p className="font-semibold">{role}</p>
                  <p className="mt-1 text-sm leading-5 text-slate-600">{concern}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="mt-16 grid gap-6 lg:grid-cols-2">
          <div className="rounded-[28px] bg-[#0F172A] p-7 text-white sm:p-9">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-300">Brand guardrails</p>
            <ul className="mt-6 space-y-3 text-sm leading-6 text-slate-300">
              <li>No fake proof, customers, logos, testimonials or outcomes.</li>
              <li>No guaranteed revenue or ROI.</li>
              <li>No unsupported “first Saudi”, market-leadership or government-access claim.</li>
              <li>No blanket compliance certification claim without exact evidence.</li>
              <li>No historical fixed pricing or checkout resurrected through old assets.</li>
              <li>No renderer or channel inventing a competing identity.</li>
            </ul>
          </div>
          <div className="rounded-[28px] border border-slate-200 bg-white p-7 shadow-sm sm:p-9">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[#0E7490]">Current commercial path</p>
            <ol className="mt-6 space-y-3 text-sm leading-6 text-slate-700">
              <li><strong>1.</strong> Free Mini Diagnostic</li>
              <li><strong>2.</strong> Qualified Discovery</li>
              <li><strong>3.</strong> Customer-Specific Quote</li>
              <li><strong>4.</strong> 30-Day Revenue Command Pilot</li>
              <li><strong>5.</strong> Proof Review</li>
              <li><strong>6.</strong> Stop / Expand / Redesign</li>
            </ol>
            <a
              href="/book"
              className="mt-7 inline-flex min-h-11 items-center justify-center rounded-full bg-[#22D3EE] px-5 py-2.5 text-sm font-semibold text-[#0F172A] transition hover:bg-[#67E8F9] focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:ring-offset-2"
            >
              Start the Execution Diagnostic
            </a>
          </div>
        </section>

        <footer className="mt-16 border-t border-slate-200 pt-6 text-sm text-slate-500">
          <p>
            Trademark clearance remains pending. Brand expression does not create consent, send authority, production authority, customer proof or payment truth.
          </p>
        </footer>
      </div>
    </main>
  );
}
