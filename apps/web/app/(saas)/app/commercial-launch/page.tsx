import { commercialLaunchControlSnapshot } from "@/lib/commercial-launch-control-snapshot";

export default function CommercialLaunchPage() {
  const data = commercialLaunchControlSnapshot;
  return (
    <main className="grid mx-auto max-w-7xl p-8">
      <section className="card card-cyan dot-pattern">
        <p className="eyebrow">Dealix Commercial Launch Control</p>
        <h1>{data.verdict}</h1>
        <p style={{ maxWidth: 900 }}>{data.release_name} — {data.release_mode}</p>
      </section>

      <section className="cards">
        <article className="card">
          <p className="stat-value">{data.launch_products.length}</p>
          <p className="stat-label">launch products</p>
        </article>
        <article className="card">
          <p className="stat-value">{data.commercial_sprint_packages.length}</p>
          <p className="stat-label">sprint packages</p>
        </article>
        <article className="card">
          <p className="stat-value">{data.targets_loaded}</p>
          <p className="stat-label">targets loaded</p>
        </article>
      </section>

      <section className="grid-2">
        <article className="card card-cyan">
          <p className="eyebrow">Products</p>
          <h2>Launch products</h2>
          <ul>
            {data.launch_products.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>
        <article className="card">
          <p className="eyebrow">Sprint Packages</p>
          <h2>Commercial offer ladder</h2>
          <ul>
            {data.commercial_sprint_packages.map((pkg) => (
              <li key={pkg.name}>
                <strong>{pkg.name}</strong> — {pkg.price_range_sar} SAR · {pkg.duration}
              </li>
            ))}
          </ul>
        </article>
      </section>
    </main>
  );
}
