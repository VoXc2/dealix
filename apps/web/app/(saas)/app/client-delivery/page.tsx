import { clientDeliveryControlSnapshot } from "@/lib/client-delivery-control-snapshot";

export default function ClientDeliveryPage() {
  const data = clientDeliveryControlSnapshot;
  return (
    <main className="grid mx-auto max-w-7xl p-8">
      <section className="card card-cyan dot-pattern">
        <p className="eyebrow">Dealix Client Delivery Control</p>
        <h1>{data.verdict}</h1>
        <p style={{ maxWidth: 900 }}>{data.purpose}</p>
      </section>

      <section className="cards">
        <article className="card"><p className="stat-value">{data.stages.length}</p><p className="stat-label">stages</p></article>
        <article className="card"><p className="stat-value">{data.client_files_status.length}</p><p className="stat-label">template files</p></article>
        <article className="card"><p className="stat-value">{data.delivery_guardrails.length}</p><p className="stat-label">guardrails</p></article>
        <article className="card"><p className="stat-value">{data.delivery_method}</p><p className="stat-label">method</p></article>
      </section>

      <section className="card">
        <p className="eyebrow">Delivery stages</p>
        <h2>From sale to proof</h2>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {data.stages.map((stage) => (
            <article className="card hover-cyan" key={stage.name}>
              <h3>{stage.name}</h3>
              <p>{stage.goal}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="grid-2">
        <article className="card card-cyan">
          <p className="eyebrow">Next delivery actions</p>
          <h2>Operator queue</h2>
          <ul>{data.next_delivery_actions.map((item) => <li key={item}>{item}</li>)}</ul>
        </article>
        <article className="card">
          <p className="eyebrow">Guardrails</p>
          <h2>Delivery rules</h2>
          <ul>{data.delivery_guardrails.map((item) => <li key={item}>{item}</li>)}</ul>
        </article>
      </section>
    </main>
  );
}
