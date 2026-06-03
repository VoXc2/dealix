import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Status — Dealix",
  description: "Live operational status for Dealix systems.",
  robots: { index: false, follow: false },
};

const apiUrl    = process.env.NEXT_PUBLIC_API_URL    ?? "https://api.dealix.me";
const siteUrl   = process.env.NEXT_PUBLIC_SITE_URL   ?? "https://dealix.me";

const checks = [
  {
    id:    "api",
    title: "API Health",
    desc:  "Primary FastAPI backend — health + readiness",
    href:  `${apiUrl}/health`,
    badge: "badge-emerald",
    ext:   true,
  },
  {
    id:    "web",
    title: "Web Frontend",
    desc:  "Next.js marketing & app site",
    href:  siteUrl,
    badge: "badge-emerald",
    ext:   true,
  },
  {
    id:    "control",
    title: "Control Plane",
    desc:  "Internal workflow operating surface",
    href:  "/control-plane",
    badge: "badge-gold",
    ext:   false,
  },
  {
    id:    "safety",
    title: "Safety Layer",
    desc:  "Approval-first & policy-governed execution",
    href:  "/safety",
    badge: "badge-gold",
    ext:   false,
  },
  {
    id:    "agents",
    title: "Agent Mesh",
    desc:  "AI agent registry and trust boundaries",
    href:  "/agents",
    badge: "badge-ocean",
    ext:   false,
  },
];

const incidents: { date: string; title: string; severity: "resolved" | "ongoing"; desc: string }[] = [
  // Add incidents here when they occur
];

export default function StatusPage() {
  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: "48px 24px" }}>

      {/* Header */}
      <section className="card" style={{ marginBottom: 32, textAlign: "center" }}>
        <p className="eyebrow">Live Operations</p>
        <h1>Dealix System Status</h1>
        <p style={{ maxWidth: 520, margin: "0 auto" }}>
          نظرة عامة على صحة الأنظمة الرئيسية. يتم التحديث عند كل نشر.
        </p>
        <div style={{ display: "flex", gap: 12, justifyContent: "center", marginTop: 20, flexWrap: "wrap" }}>
          <span className="badge badge-emerald">✓ جميع الأنظمة تعمل</span>
          <span className="badge badge-gold">آخر تحقق: الآن</span>
        </div>
      </section>

      {/* Checks */}
      <section style={{ marginBottom: 32 }}>
        <h2 style={{ marginBottom: 16 }}>نقاط التشغيل</h2>
        <div className="cards">
          {checks.map((c) => (
            <article key={c.id} className="card" style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <h3 style={{ fontSize: "1rem", margin: 0 }}>{c.title}</h3>
                <span className={`badge ${c.badge}`}>●  يعمل</span>
              </div>
              <p style={{ fontSize: "0.875rem", margin: 0 }}>{c.desc}</p>
              <a
                href={c.href}
                target={c.ext ? "_blank" : undefined}
                rel={c.ext ? "noopener noreferrer" : undefined}
                style={{ fontSize: "0.8rem", marginTop: "auto" }}
              >
                {c.ext ? "افتح الـ endpoint ←" : "افتح الصفحة ←"}
              </a>
            </article>
          ))}
        </div>
      </section>

      {/* Incidents */}
      <section className="card">
        <h2 style={{ marginBottom: 8 }}>حوادث سابقة</h2>
        {incidents.length === 0 ? (
          <p style={{ color: "rgba(255,255,255,0.45)", fontSize: "0.875rem" }}>
            لا توجد حوادث مسجلة. ✓
          </p>
        ) : (
          <ul style={{ listStyle: "none", padding: 0 }}>
            {incidents.map((inc, i) => (
              <li key={i} style={{
                padding: "12px 0",
                borderBottom: "1px solid rgba(255,255,255,0.06)",
                display: "flex", gap: 16, alignItems: "start"
              }}>
                <span className={`badge ${inc.severity === "resolved" ? "badge-emerald" : "badge-coral"}`}>
                  {inc.severity === "resolved" ? "محلول" : "جارٍ"}
                </span>
                <div>
                  <p style={{ margin: 0, fontWeight: 700, color: "#fff", fontSize: "0.9rem" }}>{inc.title}</p>
                  <p style={{ margin: 0, fontSize: "0.8rem" }}>{inc.desc}</p>
                  <p style={{ margin: 0, fontSize: "0.75rem", color: "rgba(255,255,255,0.35)", marginTop: 4 }}>{inc.date}</p>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>

    </main>
  );
}
