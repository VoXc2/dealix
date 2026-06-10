const packages = [
  ["Launch", "SAR 2,500/mo", "One focused system shipped fast."],
  ["Growth", "SAR 7,500/mo", "Revenue + marketing + operations connected."],
  ["Enterprise", "SAR 15,000+/mo", "Full OS with governance, proof, portals, integrations, and reporting."]
];

export default function RevenueOSPage() {
  return (
    <main className="grid">
      <section className="card">
        <p className="eyebrow">Dealix Revenue OS</p>
        <h1>Turn scattered business work into pipeline, proof, and controlled automation.</h1>
        <p>Dealix Revenue OS helps founders identify opportunities, prioritize follow-up, ship offer pages, and prove revenue movement.</p>
        <div className="actions">
          <a href="/go-to-market">Start GTM plan</a>
          <a href="/product-network">See product network</a>
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
