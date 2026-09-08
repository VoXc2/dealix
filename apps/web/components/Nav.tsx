"use client";

import Link from "next/link";

const links = [
  { href: "/", label: "الرئيسية" },
  { href: "/sales-machine", label: "آلة المبيعات" },
  { href: "/services", label: "الخدمات" },
  { href: "/pricing", label: "Engagement Path" },
  { href: "/book", label: "التشخيص المجاني" },
];

const commandLinks = [
  { href: "/founder/command-room", label: "غرفة القيادة" },
  { href: "/commercial-intelligence", label: "الذكاء التجاري" },
  { href: "/approvals", label: "الموافقات" },
  { href: "/evidence", label: "سجل الإثبات" },
];

export default function Nav() {
  return (
    <nav className="navbar" aria-label="Primary navigation">
      <Link href="/" className="navbar-brand" aria-label="Dealix Home">
        <img
          className="brand-logo"
          src="/dealix-logo-white.svg"
          alt="Dealix — AI Business Operating System"
          width="178"
          height="43"
        />
      </Link>
      <ul className="navbar-links" role="list">
        {links.map((link) => (
          <li key={link.href}><Link href={link.href}>{link.label}</Link></li>
        ))}
        <li className="nav-separator" aria-hidden="true">·</li>
        {commandLinks.map((link) => (
          <li key={link.href}><Link href={link.href}>{link.label}</Link></li>
        ))}
      </ul>
      <div className="actions nav-actions">
        <Link href="/founder/command-room" className="btn btn-ghost nav-secondary-action">
          غرفة القيادة
        </Link>
        <Link href="/book" className="nav-primary-action">
          ابدأ التشخيص
        </Link>
      </div>
    </nav>
  );
}
