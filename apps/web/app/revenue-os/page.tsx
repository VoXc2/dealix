const packages = [
  ["Launch", "Customer-specific quote", "One focused system shipped fast."],
  ["Growth", "Customer-specific quote", "Revenue + marketing + operations connected."],
  ["Enterprise", "Customer-specific quote", "Full OS with governance, proof, portals, integrations, and reporting."]
];

export default function RevenueOSPage() {
  return (
    <main className="grid">
      <section className="card">
        <p className="eyebrow">Dealix Revenue OS</p>
        <h1>Turn scattered business work into pipeline, proof, and controlled automation.</h1>
        <p>Dealix Revenue OS helps founders identify opportunities, prioritize follow-up, ship offer pages, and prove revenue movement.</p>
        <div className="actions">
          <a href="/book">Start free diagnostic</a>
          <a href="/products">See products</a>
        </div>
      </section>
      <section className="cards">
        {packages.map(([tier, price, description]) => (
          <article className="card" key={tier}>
            <h2>{tier}</h2>
            <p><strong>{price}</strong></p>
            <p>{description}</p>
          </article>
        ))}
      </section>
    </main>
  );
}
