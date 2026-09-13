"use client";

import Link from "next/link";

const links = [
  { href: "/company", label: "الشركة" },
  { href: "/services", label: "الخدمات" },
  { href: "/sectors", label: "القطاعات" },
  { href: "/products", label: "المنتجات" },
  { href: "/dealix-os", label: "Dealix OS" },
  { href: "/proof-vault", label: "Proof" },
];

export default function Nav() {
  return (
    <nav className="navbar" aria-label="Primary navigation">
      <Link href="/" className="navbar-brand brand-logo-link" aria-label="Dealix Home">
        <img className="brand-logo" src="/dealix-logo-white.svg" alt="Dealix" width="178" height="43" />
      </Link>
      <ul className="navbar-links" role="list">
        {links.map((link) => <li key={link.href}><Link href={link.href}>{link.label}</Link></li>)}
      </ul>
      <div className="actions nav-actions">
        <Link href="/safety" className="btn btn-ghost nav-secondary-action">الحوكمة</Link>
        <Link href="/book" className="nav-primary-action">التشخيص المجاني</Link>
      </div>
    </nav>
  );
}
