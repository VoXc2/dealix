"use client";

import Link from "next/link";

const links = [
  ["/company", "الشركة"], ["/services", "الخدمات"], ["/sectors", "القطاعات"],
  ["/products", "المنتجات"], ["/dealix-os", "Dealix OS"], ["/proof-vault", "Proof"],
  ["/pricing", "Engagement Path"], ["/safety", "الحوكمة"], ["/legal", "Legal"],
] as const;

export default function Footer() {
  return (
    <footer style={{ textAlign: "center", padding: "var(--sp-12) var(--sp-6)", borderTop: "1px solid rgba(255,255,255,0.07)" }}>
      <Link href="/" aria-label="Dealix Home" style={{ display: "inline-flex", lineHeight: 0, marginBottom: "var(--sp-4)" }}>
        <img src="/dealix-logo-white.svg" alt="Dealix" width="178" height="43" style={{ width: 178, height: "auto" }} />
      </Link>
      <p style={{ maxWidth: 720, margin: "0 auto var(--sp-4)" }}>
        Saudi-first B2B strategy, systems, intelligence and products. Signal → Decision → Action → Proof.
      </p>
      <div style={{ display: "flex", justifyContent: "center", gap: "var(--sp-4)", marginBottom: "var(--sp-4)", flexWrap: "wrap" }}>
        {links.map(([href, label]) => <Link key={href} href={href} style={{ color: "rgba(255,255,255,0.46)", fontWeight: 600, fontSize: "0.82rem" }}>{label}</Link>)}
      </div>
      <div className="actions" style={{ justifyContent: "center", marginTop: "var(--sp-4)" }}><Link href="/book">ابدأ Free Execution Diagnostic</Link></div>
      <p style={{ marginTop: "var(--sp-5)", fontSize: "0.78rem", color: "rgba(255,255,255,0.30)" }}>
        لا fixed public pricing أو ROI guarantee. Research لا يساوي Relationship، وDemo لا يساوي Customer Proof.
      </p>
      <p style={{ fontSize: "0.78rem", color: "rgba(255,255,255,0.30)" }}>© 2026 Dealix</p>
    </footer>
  );
}
