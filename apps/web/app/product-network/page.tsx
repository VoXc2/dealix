const families = [
  ["Revenue OS", "Pipeline, ICP scoring, follow-up, and founder sales cockpit."],
  ["Marketing OS", "Offer pages, campaigns, proof assets, and AI visibility."],
  ["Operations OS", "SLA rhythm, approvals, weekly reports, and execution visibility."],
  ["Trust OS", "Approval-first AI governance, evidence packs, and audit readiness."],
  ["Client Portal OS", "Client-facing progress, proof rooms, renewal triggers, and executive reports."]
];

export default function ProductNetworkPage() {
  return (
    <main className="grid">
      <section className="card">
        <p className="eyebrow">Dealix Product Network</p>
        <h1>One operating system. Five revenue-ready product families.</h1>
        <p>Dealix packages AI automation into clear business systems that can be sold, implemented, measured, and expanded.</p>
        <div className="actions">
          <a href="/revenue-os">Open Revenue OS</a>
          <a href="/go-to-market">View GTM system</a>
        </div>
      </section>
      <section className="cards">
        {families.map(([title, description]) => (
          <article className="card" key={title}>
            <h2>{title}</h2>
            <p>{description}</p>
          </article>
        ))}
      </section>
    </main>
  );
}
