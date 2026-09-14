import { trustControlSnapshot } from "@/lib/trust-control-snapshot";

export default function TrustControlPage() {
  const data = trustControlSnapshot;
  return (
    <main className="grid mx-auto max-w-7xl p-8">
      <section className="card card-cyan dot-pattern">
        <p className="eyebrow">Dealix Trust Control</p>
        <h1>{data.verdict}</h1>
        <p style={{ maxWidth: 900 }}>{data.purpose}</p>
      </section>

      <section className="cards">
        <article className="card"><p className="stat-value">{data.checks.length}</p><p className="stat-label">checks</p></article>
        <article className="card"><p className="stat-value">{data.blocked_phrases.length}</p><p className="stat-label">blocked phrases</p></article>
        <article className="card"><p className="stat-value">{data.approved_language.length}</p><p className="stat-label">approved language</p></article>
        <article className="card"><p className="stat-value">{data.required_guardrails.length}</p><p className="stat-label">guardrails</p></article>
      </section>

      <section className="grid-2">
        <article className="card card-cyan">
          <p className="eyebrow">Checks</p>
          <h2>Trust review gates</h2>
          <ul>{data.checks.map((item) => <li key={item.name}>{item.name}: {item.goal}</li>)}</ul>
        </article>
        <article className="card">
          <p className="eyebrow">Guardrails</p>
          <h2>Required rules</h2>
          <ul>{data.required_guardrails.map((item) => <li key={item}>{item}</li>)}</ul>
        </article>
      </section>
    </main>
  );
}
