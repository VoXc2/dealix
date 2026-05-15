const links = [
  "/control-plane",
  "/agents",
  "/approvals",
  "/safety",
  "/sandbox",
  "/value-engine",
  "/self-evolving"
];

export default function HomePage() {
  return (
    <main className="grid">
      <h1>Dealix Enterprise Control Plane</h1>
      <div className="card">
        <p>نقطة دخول لوحات التحكم المؤسسية.</p>
        <ul>
          {links.map((href) => (
            <li key={href}>
              <a href={href}>{href}</a>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
