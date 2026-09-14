import Link from "next/link";
import { hubspotLaunchTasks, hubspotServiceCatalog, hubspotTargetGroups } from "@/lib/hubspot-commercial-os";

export const metadata = {
  title: "HubSpot Commercial OS — Dealix",
  description: "Dealix commercial, financial, and sales operating layer connected to HubSpot readiness.",
};

export default function HubSpotOSPage() {
  return (
    <main>
      <section className="card dot-pattern" style={{ textAlign: "center" }}>
        <p className="eyebrow">HubSpot Commercial OS</p>
        <h1>حوّل HubSpot إلى غرفة تشغيل تجارية ومالية ومبيعاتية</h1>
        <p style={{ maxWidth: 820, margin: "0 auto" }}>
          HubSpot يكون مصدر الحقيقة للـCRM، وDealix يكون طبقة الذكاء: scoring، pain mapping، sales drafts،
          negotiation، revenue command، financial tracking، وowner-approved write-back.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <Link href="/command-center">افتح غرفة القيادة</Link>
          <Link href="/sales-agent-lab">جرّب Sales Agent Lab</Link>
          <Link href="/services">شاهد الخدمات</Link>
        </div>
      </section>

      <section className="grid-3">
        <article className="card">
          <div className="stat-value">16</div>
          <p className="stat-label">HubSpot company records found</p>
        </article>
        <article className="card">
          <div className="stat-value">8</div>
          <p className="stat-label">high-value target groups</p>
        </article>
        <article className="card">
          <div className="stat-value">5</div>
          <p className="stat-label">launch tasks found</p>
        </article>
      </section>

      <section aria-labelledby="targets-title">
        <p className="eyebrow">Target groups</p>
        <h2 id="targets-title">قطاعات HubSpot الجاهزة للاستغلال التجاري</h2>
        <div className="cards">
          {hubspotTargetGroups.map((group) => (
            <article className="card" key={group.name}>
              <span className="badge badge-cyan">{group.industry}</span>
              <h3 style={{ marginTop: "var(--sp-4)" }}>{group.name}</h3>
              <p><strong>Sector:</strong> {group.sector}</p>
              <p><strong>Best offer:</strong> {group.offer}</p>
              <p><strong>Pain angle:</strong> {group.pain}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="grid-2">
        <article className="card card-cyan">
          <p className="eyebrow">Launch tasks</p>
          <h2>مهام موجودة وتدعم الإطلاق</h2>
          <ul>{hubspotLaunchTasks.map((task) => <li key={task}>{task}</li>)}</ul>
        </article>
        <article className="card">
          <p className="eyebrow">Write-back policy</p>
          <h2>التكامل الكامل لا يعني كتابة عشوائية</h2>
          <p>
            Dealix يجهز tasks, notes, deals, products, and line items كاقتراحات. أي تعديل داخل HubSpot يحتاج approval واضح.
          </p>
          <ul>
            <li>Stage 0: read-only intelligence</li>
            <li>Stage 1: proposed write-back</li>
            <li>Stage 2: confirmed tasks and notes</li>
            <li>Stage 3: confirmed deals and pipeline</li>
            <li>Stage 4: controlled communication queue</li>
          </ul>
        </article>
      </section>

      <section className="card" aria-labelledby="catalog-title">
        <p className="eyebrow">Financial and sales catalog</p>
        <h2 id="catalog-title">باقات قابلة للتحويل إلى Products داخل HubSpot</h2>
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={{ textAlign: "left", padding: 12, borderBottom: "1px solid rgba(255,255,255,0.12)" }}>Product</th>
                <th style={{ textAlign: "left", padding: 12, borderBottom: "1px solid rgba(255,255,255,0.12)" }}>Price</th>
                <th style={{ textAlign: "left", padding: 12, borderBottom: "1px solid rgba(255,255,255,0.12)" }}>Revenue model</th>
              </tr>
            </thead>
            <tbody>
              {hubspotServiceCatalog.map(([product, price, model]) => (
                <tr key={product}>
                  <td style={{ padding: 12, borderBottom: "1px solid rgba(255,255,255,0.07)" }}>{product}</td>
                  <td style={{ padding: 12, borderBottom: "1px solid rgba(255,255,255,0.07)" }}>{price}</td>
                  <td style={{ padding: 12, borderBottom: "1px solid rgba(255,255,255,0.07)" }}>{model}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="card" style={{ textAlign: "center" }}>
        <p className="eyebrow">Run locally</p>
        <h2>شغّل HubSpot Commercial OS report</h2>
        <pre style={{ textAlign: "left" }}>python scripts/commercial/generate_hubspot_commercial_os.py</pre>
        <p>ثم راجع reports/hubspot_os/latest.md قبل أي write-back داخل HubSpot.</p>
      </section>
    </main>
  );
}
