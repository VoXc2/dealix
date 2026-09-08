"use client";

import Link from "next/link";

export default function Footer() {
  return (
    <footer className="site-footer">
      <Link href="/" className="footer-logo" aria-label="Dealix Home">
        <img
          src="/dealix-logo-white.svg"
          alt="Dealix — AI Business Operating System"
          width="178"
          height="43"
        />
      </Link>
      <div className="footer-links">
        <Link href="/sales-machine">آلة المبيعات</Link>
        <Link href="/services">الخدمات</Link>
        <Link href="/pricing">Engagement Path</Link>
        <Link href="/book">التشخيص المجاني</Link>
        <Link href="/safety">الثقة والأمان</Link>
        <Link href="/legal">Legal</Link>
      </div>
      <p>
        © 2026 Dealix · Signals into Action · Execution with Governance · Measurable Outcomes
      </p>
    </footer>
  );
}
