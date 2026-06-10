const steps = [
  "Choose ICP and offer",
  "Generate landing page and proof pack",
  "Launch campaign",
  "Score leads",
  "Run follow-up",
  "Report revenue movement",
  "Expand to another product family"
];

export default function GoToMarketPage() {
  return (
    <main className="grid">
      <section className="card">
        <p className="eyebrow">Dealix GTM System</p>
        <h1>From product idea to campaign, page, proof, and sales motion.</h1>
        <p>This is the commercial operating loop behind Dealix: productized services, executive messaging, campaign automation, and measurable proof.</p>
      </section>
      <section className="cards">
        {steps.map((step, index) => (
          <article className="card" key={step}>
            <p className="eyebrow">Step {index + 1}</p>
            <h2>{step}</h2>
          </article>
        ))}
      </section>
    </main>
  );
}
