"use client";

import Link from "next/link";

export default function OfferCard({ icon, title, description, href, badge }: { icon: string; title: string; description: string; href: string; badge?: string }) {
  return (
    <article className="card" style={{ position: "relative" }}>
      {badge && (
        <span className="badge badge-cyan" style={{ position: "absolute", top: "var(--sp-4)", left: "var(--sp-4)" }}>
          {badge}
        </span>
      )}
      <div style={{ fontSize: "2rem", marginBottom: "var(--sp-3)", marginTop: badge ? "var(--sp-4)" : 0 }}>{icon}</div>
      <h3 style={{ color: "#fff", marginBottom: "var(--sp-2)" }}>{title}</h3>
      <p style={{ fontSize: "0.9rem", marginBottom: "var(--sp-5)" }}>{description}</p>
      <Link href={href} className="btn btn-secondary" style={{ fontSize: "0.82rem", minHeight: 36, padding: "0 16px", borderRadius: "var(--radius-md)" }}>
        اطلع على {title} →
      </Link>
    </article>
  );
}
