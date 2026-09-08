"use client";

import Link from "next/link";

export default function Footer() {
  return (
    <footer style={{ textAlign: "center", paddingTop: "var(--sp-8)", borderTop: "1px solid rgba(255,255,255,0.07)" }}>
      <Link
        href="/"
        aria-label="Dealix Home"
        style={{ display: "inline-flex", justifyContent: "center", lineHeight: 0, marginBottom: "var(--sp-3)" }}
      >
        <img
          src="/dealix-logo-white.svg"
          alt="Dealix — AI Business Operating System"
          width="178"
          height="43"
          style={{ width: "178px", height: "auto" }}
        />
      </Link>
      <div style={{ display: "flex", justifyContent: "center", gap: "var(--sp-4)", marginBottom: "var(--sp-4)", flexWrap: "wrap" }}>
        <Link href="/sales-machine" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>آلة المبيعات</Link>
        <Link href="/services" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>الخدمات</Link>
        <Link href="/pricing" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>Engagement Path</Link>
        <Link href="/book" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>التشخيص المجاني</Link>
        <Link href="/safety" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>الثقة والأمان</Link>
        <Link href="/legal" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>Legal</Link>
      </div>
      <p style={{ fontSize: "0.82rem", color: "rgba(255,255,255,0.30)" }}>
        © 2026 Dealix · Signals into Action · Execution with Governance · Measurable Outcomes
      </p>
    </footer>
  );
}
